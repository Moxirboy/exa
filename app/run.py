import grpc

from config import settings
from logger import logger
from concurrent.futures import ThreadPoolExecutor

import typesense
from misollar_service.misollar_service_pb2_grpc import MisollarServiceServicer,add_MisollarServiceServicer_to_server
from misollar_service import misollar_service_pb2
import re

def remove_punctuation(text):
    cleaned = re.sub(r'[?!.,;:\'\"()\[\]{}]', '', text)
    return cleaned.rstrip()

class MisollarService(MisollarServiceServicer):

    def __init__(self, api_key):
        self.client = typesense.Client({
            'nodes': [{
                'host': '172.20.0.2',
                'port': '8108',
                'protocol': 'http'
            }],
            'api_key': api_key,
            'connection_timeout_seconds': 2000
        })

    def lookup_phrase_table(self, src_phrase, src_lang, tgt_lang,collection_name,limit):
        search_params = {
            'q': f'{src_phrase}',
            'query_by': 'src_phrase,tgt_lang',
            'filter_by': f'tgt_lang:{tgt_lang}',
            'facet_by': 'src_lang,tgt_lang',
            'per_page': 250,
            'num_typos': 0,
            'drop_tokens_threshold': 1,
            'exact_on_single_word_query': False,
            'exhaustive_search': False
        }
        try:
            return self.client.collections[collection_name].documents.search(search_params)
        except Exception as e:
            logger.error(f"Error searching phrase table: {e}")
            return {}
    
    def lookup_completed_phrase(self, src_phrase, tgt_lang, collection_name):
        completed_phrases = set()
        seen_phrases = set()
        for i in range(1,10):
            search_params = {
            'q': src_phrase,
            'query_by': 'src_phrase',
            'prefix': 'true',
            'per_page': 50,
            'page': i,
            }

            try:
                result = self.client.collections[collection_name].documents.search(search_params)
                filtered = [
                    hit for hit in result['hits']
                    if remove_punctuation(hit['document']['src_phrase']).lower().startswith(remove_punctuation(src_phrase).lower())
                    and remove_punctuation(hit['document']['src_phrase']) not in seen_phrases
                ]
                for hit in filtered:
                    seen_phrases.add(remove_punctuation(hit['document']['src_phrase']))
                    completed_phrases.add(remove_punctuation(hit['document']['src_phrase']))
                if len(completed_phrases) >=10:
                    break
            except Exception as e:
                logger.error(f"Error fetching single-word suggestions: {e}")
                return []

        # Return up to 10 unique src_phrase strings
        return sorted(completed_phrases, key=len)

    def lookup_sent(self, sent_id):
        search_params = {
            'q': sent_id,
            'query_by': 'sent_id',
        }
        try:
            return self.client.collections['dataset'].documents.search(search_params)
        except Exception as e:
            logger.error(f"Error searching sentences: {e}")
            return {}

    def get_misollar_complete(self,request,context):
        src_phrase = request.src_phrase
        tgt_lang = request.tgt_lang
        with ThreadPoolExecutor() as executor:
            future_phrase = executor.submit(self.lookup_completed_phrase, src_phrase, tgt_lang, 'auto_complete')

            phrases = future_phrase.result()
        return misollar_service_pb2.CompleteResponse(src_phrase=phrases) 

    
    def get_misollar_query(self, request, context):
        src_phrase = request.src_phrase
        src_lang = request.src_lang
        tgt_lang = request.tgt_lang

        with ThreadPoolExecutor() as executor:
            future_phrase = executor.submit(self.lookup_phrase_table, src_phrase, src_lang, tgt_lang, 'phrase_table', 5)
            future_lemma = executor.submit(self.lookup_phrase_table, src_phrase, src_lang, tgt_lang, 'lemma_phrase_table',10)

            phrases = future_phrase.result()
            lemma_phrases = future_lemma.result()

        if not phrases and not lemma_phrases:
            return misollar_service_pb2.MisollarResponse(hits=[])

        merged_hits = []
        for hit in (lemma_phrases.get('hits', []) if lemma_phrases else []):
            merged_hits.append(hit)

        for hit in (phrases.get('hits', []) if phrases else []):
            merged_hits.append(hit)

        sent_ids = list({hit['document']['sent_id'] for hit in merged_hits})

        with ThreadPoolExecutor() as executor:
            sentence_futures = {sent_id: executor.submit(self.lookup_sent, sent_id) for sent_id in sent_ids}
        sent_map = {}
        for sent_id, future in sentence_futures.items():
            result = future.result()
            if result and 'hits' in result and result['hits']:
                doc = result['hits'][0]['document']
                sent_map[sent_id] = doc

        response_hits = []
        for phrase_hit in merged_hits:
            phrase_doc = phrase_hit['document']
            sent_id = phrase_doc['sent_id']
            
            sentence_data = sent_map.get(sent_id, {})
            src_sent = sentence_data.get('src_sent', '') if isinstance(sentence_data, dict) else ''
            tgt_sent = sentence_data.get('tgt_sent', '') if isinstance(sentence_data, dict) else ''
            src_spans = []
            if 'src_spans' in phrase_doc and isinstance(phrase_doc['src_spans'], list):
                for span in phrase_doc['src_spans']:
                    if isinstance(span, list):
                        src_spans.append(misollar_service_pb2.Span(start=span[0], end=span[1]))

            tgt_spans = []
            if 'tgt_spans' in phrase_doc and isinstance(phrase_doc['tgt_spans'], list):
                for span in phrase_doc['tgt_spans']:
                    if isinstance(span, list):
                        tgt_spans.append(misollar_service_pb2.Span(start=span[0], end=span[1]))

            document = misollar_service_pb2.Document(
                id=phrase_doc.get('id', ''),
                sent_id=phrase_doc.get('sent_id', ''),
                src_lang=phrase_doc.get('src_lang', ''),
                src_phrase=phrase_doc.get('src_phrase', ''),
                src_sentence=src_sent,
                tgt_lang=phrase_doc.get('tgt_lang', ''),
                tgt_phrase=phrase_doc.get('tgt_phrase', ''),
                tgt_sentence=tgt_sent,
                src_spans=src_spans,
                tgt_spans=tgt_spans,
            )

            response_hits.append(document)

        return misollar_service_pb2.MisollarResponse(hits=response_hits)





def execute_server() -> None:
    logger.info("Starting service...")

    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_MisollarServiceServicer_to_server(MisollarService(settings.API_KEY), server)
    server.add_insecure_port(f"10.128.0.17{settings.SERVICE_PORT}")
    server.start()

    logger.info(f"{settings.SERVICE_NAME} is up and running at {settings.SERVICE_PORT}...")
    server.wait_for_termination()


if __name__ == "__main__":
    try:
        execute_server()
    except KeyboardInterrupt:
        logger.error(f"{settings.SERVICE_NAME} has been stopped.")
