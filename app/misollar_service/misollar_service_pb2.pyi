from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompleteResponse(_message.Message):
    __slots__ = ("src_phrase",)
    SRC_PHRASE_FIELD_NUMBER: _ClassVar[int]
    src_phrase: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, src_phrase: _Optional[_Iterable[str]] = ...) -> None: ...

class MisollarRequest(_message.Message):
    __slots__ = ("src_phrase", "src_lang", "tgt_lang")
    SRC_PHRASE_FIELD_NUMBER: _ClassVar[int]
    SRC_LANG_FIELD_NUMBER: _ClassVar[int]
    TGT_LANG_FIELD_NUMBER: _ClassVar[int]
    src_phrase: str
    src_lang: str
    tgt_lang: str
    def __init__(self, src_phrase: _Optional[str] = ..., src_lang: _Optional[str] = ..., tgt_lang: _Optional[str] = ...) -> None: ...

class Span(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: int
    end: int
    def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class Document(_message.Message):
    __slots__ = ("id", "sent_id", "src_lang", "src_phrase", "src_sentence", "src_spans", "tgt_lang", "tgt_phrase", "tgt_sentence", "tgt_spans", "source")
    ID_FIELD_NUMBER: _ClassVar[int]
    SENT_ID_FIELD_NUMBER: _ClassVar[int]
    SRC_LANG_FIELD_NUMBER: _ClassVar[int]
    SRC_PHRASE_FIELD_NUMBER: _ClassVar[int]
    SRC_SENTENCE_FIELD_NUMBER: _ClassVar[int]
    SRC_SPANS_FIELD_NUMBER: _ClassVar[int]
    TGT_LANG_FIELD_NUMBER: _ClassVar[int]
    TGT_PHRASE_FIELD_NUMBER: _ClassVar[int]
    TGT_SENTENCE_FIELD_NUMBER: _ClassVar[int]
    TGT_SPANS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    sent_id: str
    src_lang: str
    src_phrase: str
    src_sentence: str
    src_spans: _containers.RepeatedCompositeFieldContainer[Span]
    tgt_lang: str
    tgt_phrase: str
    tgt_sentence: str
    tgt_spans: _containers.RepeatedCompositeFieldContainer[Span]
    source: str
    def __init__(self, id: _Optional[str] = ..., sent_id: _Optional[str] = ..., src_lang: _Optional[str] = ..., src_phrase: _Optional[str] = ..., src_sentence: _Optional[str] = ..., src_spans: _Optional[_Iterable[_Union[Span, _Mapping]]] = ..., tgt_lang: _Optional[str] = ..., tgt_phrase: _Optional[str] = ..., tgt_sentence: _Optional[str] = ..., tgt_spans: _Optional[_Iterable[_Union[Span, _Mapping]]] = ..., source: _Optional[str] = ...) -> None: ...

class MisollarResponse(_message.Message):
    __slots__ = ("hits",)
    HITS_FIELD_NUMBER: _ClassVar[int]
    hits: _containers.RepeatedCompositeFieldContainer[Document]
    def __init__(self, hits: _Optional[_Iterable[_Union[Document, _Mapping]]] = ...) -> None: ...
