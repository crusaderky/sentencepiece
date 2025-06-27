from google.protobuf.internal import containers as _containers
from google.protobuf.internal import python_message as _python_message
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SentencePieceText(_message.Message):
    __slots__ = ("text", "pieces", "score")
    Extensions: _python_message._ExtensionDict
    class SentencePiece(_message.Message):
        __slots__ = ("piece", "id", "surface", "begin", "end")
        Extensions: _python_message._ExtensionDict
        PIECE_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        SURFACE_FIELD_NUMBER: _ClassVar[int]
        BEGIN_FIELD_NUMBER: _ClassVar[int]
        END_FIELD_NUMBER: _ClassVar[int]
        piece: str
        id: int
        surface: str
        begin: int
        end: int
        def __init__(self, piece: _Optional[str] = ..., id: _Optional[int] = ..., surface: _Optional[str] = ..., begin: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...
    TEXT_FIELD_NUMBER: _ClassVar[int]
    PIECES_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    text: str
    pieces: _containers.RepeatedCompositeFieldContainer[SentencePieceText.SentencePiece]
    score: float
    def __init__(self, text: _Optional[str] = ..., pieces: _Optional[_Iterable[_Union[SentencePieceText.SentencePiece, _Mapping]]] = ..., score: _Optional[float] = ...) -> None: ...

class NBestSentencePieceText(_message.Message):
    __slots__ = ("nbests",)
    NBESTS_FIELD_NUMBER: _ClassVar[int]
    nbests: _containers.RepeatedCompositeFieldContainer[SentencePieceText]
    def __init__(self, nbests: _Optional[_Iterable[_Union[SentencePieceText, _Mapping]]] = ...) -> None: ...
