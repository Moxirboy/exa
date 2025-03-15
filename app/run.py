import grpc

from config import settings
from logger import logger
from concurrent.futures import ThreadPoolExecutor

import typesense
from query_service.query_service_pb2_grpc import QueryServiceServicer
from utils import dict_or_list_to_value


class QueryService(QueryServiceServicer):

    def __init__(self, api_key):
        # Initialize Typesense client
        self.client = typesense.Client({
            'nodes': [{
                'host': 'localhost',
                'port': '8108',
                'protocol': 'http'
            }],
            'api_key': api_key,
            'connection_timeout_seconds': 2
        })

    def lookup_phrase_table(self, src_phrase, src_lang, tgt_lang):
        search_params = {
            'q': src_phrase,
            'query_by': 'src_phrase',
            'filter_by': f"src_lang:{src_lang} && tgt_lang:{tgt_lang}"
        }
        try:
            return self.client.collections['phrase_table'].documents.search(search_params)
        except Exception as e:
            logger.error(f"Error searching phrase table: {e}")
            return {}

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

    def get_query(self, request, context):
        src_phrase = request.src_phrase
        src_lang = request.src_lang
        tgt_lang = request.tgt_lang
        
        phrases = self.lookup_phrase_table(src_phrase, src_lang, tgt_lang)
        if not phrases or not phrases.get('hits'):
            return query_response(hits=[])

        sent_ids = [hit['document']['sent_id'] for hit in phrases['hits']]
        sentences = []
        for sent_id in sent_ids:
            sentences.append(self.lookup_sent(sent_id))
        sent_map = {hit['document']['sent_id']: hit['document'] for hit in sentences.get('hits', [])}

        response_hits = []
        for phrase_hit in phrases['hits']:
            phrase_doc = phrase_hit['document']
            sent_id = phrase_doc['sent_id']
            src_sent = sent_map.get(sent_id, {}).get('src_sent', '')
            tgt_sent = sent_map.get(sent_id, {}).get('tgt_sent', '')

            response_hit = {
                'src_phrase': phrase_doc['src_phrase'],
                'tgt_phrase': phrase_doc['tgt_phrase'],
                'src_spans': phrase_doc['src_spans'],
                'tgt_spans': phrase_doc['tgt_spans'],
                'src_sent': src_sent,
                'tgt_sent': tgt_sent,
            }
            response_hits.append(response_hit)

        return query_response(hits=dict_or_list_to_value(response_hits))



def execute_server() -> None:
    logger.info("Starting service...")

    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_QueryServiceServicer_to_server(QueryService(), server)
    server.add_insecure_port(f"[::]{settings.SERVICE_PORT}")
    server.start()

    logger.info(f"{settings.SERVICE_NAME} is up and running at {settings.SERVICE_PORT}...")
    server.wait_for_termination()


if __name__ == "__main__":
    try:
        execute_server()
    except KeyboardInterrupt:
        logger.error(f"{settings.SERVICE_NAME} has been stopped.")
