from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf.internal import python_message as _python_message
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrainerSpec(_message.Message):
    __slots__ = ("input", "input_format", "model_prefix", "model_type", "vocab_size", "accept_language", "self_test_sample_size", "enable_differential_privacy", "differential_privacy_noise_level", "differential_privacy_clipping_threshold", "character_coverage", "input_sentence_size", "shuffle_input_sentence", "mining_sentence_size", "training_sentence_size", "seed_sentencepiece_size", "shrinking_factor", "max_sentence_length", "num_threads", "num_sub_iterations", "max_sentencepiece_length", "split_by_unicode_script", "split_by_number", "split_by_whitespace", "treat_whitespace_as_suffix", "allow_whitespace_only_pieces", "split_digits", "pretokenization_delimiter", "control_symbols", "user_defined_symbols", "required_chars", "byte_fallback", "vocabulary_output_piece_score", "hard_vocab_limit", "use_all_vocab", "unk_id", "bos_id", "eos_id", "pad_id", "unk_piece", "bos_piece", "eos_piece", "pad_piece", "unk_surface", "train_extremely_large_corpus", "seed_sentencepieces_file")
    Extensions: _python_message._ExtensionDict
    class ModelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNIGRAM: _ClassVar[TrainerSpec.ModelType]
        BPE: _ClassVar[TrainerSpec.ModelType]
        WORD: _ClassVar[TrainerSpec.ModelType]
        CHAR: _ClassVar[TrainerSpec.ModelType]
    UNIGRAM: TrainerSpec.ModelType
    BPE: TrainerSpec.ModelType
    WORD: TrainerSpec.ModelType
    CHAR: TrainerSpec.ModelType
    INPUT_FIELD_NUMBER: _ClassVar[int]
    INPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    MODEL_PREFIX_FIELD_NUMBER: _ClassVar[int]
    MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    VOCAB_SIZE_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SELF_TEST_SAMPLE_SIZE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_DIFFERENTIAL_PRIVACY_FIELD_NUMBER: _ClassVar[int]
    DIFFERENTIAL_PRIVACY_NOISE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    DIFFERENTIAL_PRIVACY_CLIPPING_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_COVERAGE_FIELD_NUMBER: _ClassVar[int]
    INPUT_SENTENCE_SIZE_FIELD_NUMBER: _ClassVar[int]
    SHUFFLE_INPUT_SENTENCE_FIELD_NUMBER: _ClassVar[int]
    MINING_SENTENCE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_SENTENCE_SIZE_FIELD_NUMBER: _ClassVar[int]
    SEED_SENTENCEPIECE_SIZE_FIELD_NUMBER: _ClassVar[int]
    SHRINKING_FACTOR_FIELD_NUMBER: _ClassVar[int]
    MAX_SENTENCE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    NUM_THREADS_FIELD_NUMBER: _ClassVar[int]
    NUM_SUB_ITERATIONS_FIELD_NUMBER: _ClassVar[int]
    MAX_SENTENCEPIECE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SPLIT_BY_UNICODE_SCRIPT_FIELD_NUMBER: _ClassVar[int]
    SPLIT_BY_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SPLIT_BY_WHITESPACE_FIELD_NUMBER: _ClassVar[int]
    TREAT_WHITESPACE_AS_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    ALLOW_WHITESPACE_ONLY_PIECES_FIELD_NUMBER: _ClassVar[int]
    SPLIT_DIGITS_FIELD_NUMBER: _ClassVar[int]
    PRETOKENIZATION_DELIMITER_FIELD_NUMBER: _ClassVar[int]
    CONTROL_SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_CHARS_FIELD_NUMBER: _ClassVar[int]
    BYTE_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    VOCABULARY_OUTPUT_PIECE_SCORE_FIELD_NUMBER: _ClassVar[int]
    HARD_VOCAB_LIMIT_FIELD_NUMBER: _ClassVar[int]
    USE_ALL_VOCAB_FIELD_NUMBER: _ClassVar[int]
    UNK_ID_FIELD_NUMBER: _ClassVar[int]
    BOS_ID_FIELD_NUMBER: _ClassVar[int]
    EOS_ID_FIELD_NUMBER: _ClassVar[int]
    PAD_ID_FIELD_NUMBER: _ClassVar[int]
    UNK_PIECE_FIELD_NUMBER: _ClassVar[int]
    BOS_PIECE_FIELD_NUMBER: _ClassVar[int]
    EOS_PIECE_FIELD_NUMBER: _ClassVar[int]
    PAD_PIECE_FIELD_NUMBER: _ClassVar[int]
    UNK_SURFACE_FIELD_NUMBER: _ClassVar[int]
    TRAIN_EXTREMELY_LARGE_CORPUS_FIELD_NUMBER: _ClassVar[int]
    SEED_SENTENCEPIECES_FILE_FIELD_NUMBER: _ClassVar[int]
    input: _containers.RepeatedScalarFieldContainer[str]
    input_format: str
    model_prefix: str
    model_type: TrainerSpec.ModelType
    vocab_size: int
    accept_language: _containers.RepeatedScalarFieldContainer[str]
    self_test_sample_size: int
    enable_differential_privacy: bool
    differential_privacy_noise_level: float
    differential_privacy_clipping_threshold: int
    character_coverage: float
    input_sentence_size: int
    shuffle_input_sentence: bool
    mining_sentence_size: int
    training_sentence_size: int
    seed_sentencepiece_size: int
    shrinking_factor: float
    max_sentence_length: int
    num_threads: int
    num_sub_iterations: int
    max_sentencepiece_length: int
    split_by_unicode_script: bool
    split_by_number: bool
    split_by_whitespace: bool
    treat_whitespace_as_suffix: bool
    allow_whitespace_only_pieces: bool
    split_digits: bool
    pretokenization_delimiter: str
    control_symbols: _containers.RepeatedScalarFieldContainer[str]
    user_defined_symbols: _containers.RepeatedScalarFieldContainer[str]
    required_chars: str
    byte_fallback: bool
    vocabulary_output_piece_score: bool
    hard_vocab_limit: bool
    use_all_vocab: bool
    unk_id: int
    bos_id: int
    eos_id: int
    pad_id: int
    unk_piece: str
    bos_piece: str
    eos_piece: str
    pad_piece: str
    unk_surface: str
    train_extremely_large_corpus: bool
    seed_sentencepieces_file: str
    def __init__(self, input: _Optional[_Iterable[str]] = ..., input_format: _Optional[str] = ..., model_prefix: _Optional[str] = ..., model_type: _Optional[_Union[TrainerSpec.ModelType, str]] = ..., vocab_size: _Optional[int] = ..., accept_language: _Optional[_Iterable[str]] = ..., self_test_sample_size: _Optional[int] = ..., enable_differential_privacy: bool = ..., differential_privacy_noise_level: _Optional[float] = ..., differential_privacy_clipping_threshold: _Optional[int] = ..., character_coverage: _Optional[float] = ..., input_sentence_size: _Optional[int] = ..., shuffle_input_sentence: bool = ..., mining_sentence_size: _Optional[int] = ..., training_sentence_size: _Optional[int] = ..., seed_sentencepiece_size: _Optional[int] = ..., shrinking_factor: _Optional[float] = ..., max_sentence_length: _Optional[int] = ..., num_threads: _Optional[int] = ..., num_sub_iterations: _Optional[int] = ..., max_sentencepiece_length: _Optional[int] = ..., split_by_unicode_script: bool = ..., split_by_number: bool = ..., split_by_whitespace: bool = ..., treat_whitespace_as_suffix: bool = ..., allow_whitespace_only_pieces: bool = ..., split_digits: bool = ..., pretokenization_delimiter: _Optional[str] = ..., control_symbols: _Optional[_Iterable[str]] = ..., user_defined_symbols: _Optional[_Iterable[str]] = ..., required_chars: _Optional[str] = ..., byte_fallback: bool = ..., vocabulary_output_piece_score: bool = ..., hard_vocab_limit: bool = ..., use_all_vocab: bool = ..., unk_id: _Optional[int] = ..., bos_id: _Optional[int] = ..., eos_id: _Optional[int] = ..., pad_id: _Optional[int] = ..., unk_piece: _Optional[str] = ..., bos_piece: _Optional[str] = ..., eos_piece: _Optional[str] = ..., pad_piece: _Optional[str] = ..., unk_surface: _Optional[str] = ..., train_extremely_large_corpus: bool = ..., seed_sentencepieces_file: _Optional[str] = ...) -> None: ...

class NormalizerSpec(_message.Message):
    __slots__ = ("name", "precompiled_charsmap", "add_dummy_prefix", "remove_extra_whitespaces", "escape_whitespaces", "normalization_rule_tsv")
    Extensions: _python_message._ExtensionDict
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRECOMPILED_CHARSMAP_FIELD_NUMBER: _ClassVar[int]
    ADD_DUMMY_PREFIX_FIELD_NUMBER: _ClassVar[int]
    REMOVE_EXTRA_WHITESPACES_FIELD_NUMBER: _ClassVar[int]
    ESCAPE_WHITESPACES_FIELD_NUMBER: _ClassVar[int]
    NORMALIZATION_RULE_TSV_FIELD_NUMBER: _ClassVar[int]
    name: str
    precompiled_charsmap: bytes
    add_dummy_prefix: bool
    remove_extra_whitespaces: bool
    escape_whitespaces: bool
    normalization_rule_tsv: str
    def __init__(self, name: _Optional[str] = ..., precompiled_charsmap: _Optional[bytes] = ..., add_dummy_prefix: bool = ..., remove_extra_whitespaces: bool = ..., escape_whitespaces: bool = ..., normalization_rule_tsv: _Optional[str] = ...) -> None: ...

class SelfTestData(_message.Message):
    __slots__ = ("samples",)
    Extensions: _python_message._ExtensionDict
    class Sample(_message.Message):
        __slots__ = ("input", "expected")
        INPUT_FIELD_NUMBER: _ClassVar[int]
        EXPECTED_FIELD_NUMBER: _ClassVar[int]
        input: str
        expected: str
        def __init__(self, input: _Optional[str] = ..., expected: _Optional[str] = ...) -> None: ...
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    samples: _containers.RepeatedCompositeFieldContainer[SelfTestData.Sample]
    def __init__(self, samples: _Optional[_Iterable[_Union[SelfTestData.Sample, _Mapping]]] = ...) -> None: ...

class ModelProto(_message.Message):
    __slots__ = ("pieces", "trainer_spec", "normalizer_spec", "self_test_data", "denormalizer_spec")
    Extensions: _python_message._ExtensionDict
    class SentencePiece(_message.Message):
        __slots__ = ("piece", "score", "type")
        Extensions: _python_message._ExtensionDict
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            NORMAL: _ClassVar[ModelProto.SentencePiece.Type]
            UNKNOWN: _ClassVar[ModelProto.SentencePiece.Type]
            CONTROL: _ClassVar[ModelProto.SentencePiece.Type]
            USER_DEFINED: _ClassVar[ModelProto.SentencePiece.Type]
            BYTE: _ClassVar[ModelProto.SentencePiece.Type]
            UNUSED: _ClassVar[ModelProto.SentencePiece.Type]
        NORMAL: ModelProto.SentencePiece.Type
        UNKNOWN: ModelProto.SentencePiece.Type
        CONTROL: ModelProto.SentencePiece.Type
        USER_DEFINED: ModelProto.SentencePiece.Type
        BYTE: ModelProto.SentencePiece.Type
        UNUSED: ModelProto.SentencePiece.Type
        PIECE_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        piece: str
        score: float
        type: ModelProto.SentencePiece.Type
        def __init__(self, piece: _Optional[str] = ..., score: _Optional[float] = ..., type: _Optional[_Union[ModelProto.SentencePiece.Type, str]] = ...) -> None: ...
    PIECES_FIELD_NUMBER: _ClassVar[int]
    TRAINER_SPEC_FIELD_NUMBER: _ClassVar[int]
    NORMALIZER_SPEC_FIELD_NUMBER: _ClassVar[int]
    SELF_TEST_DATA_FIELD_NUMBER: _ClassVar[int]
    DENORMALIZER_SPEC_FIELD_NUMBER: _ClassVar[int]
    pieces: _containers.RepeatedCompositeFieldContainer[ModelProto.SentencePiece]
    trainer_spec: TrainerSpec
    normalizer_spec: NormalizerSpec
    self_test_data: SelfTestData
    denormalizer_spec: NormalizerSpec
    def __init__(self, pieces: _Optional[_Iterable[_Union[ModelProto.SentencePiece, _Mapping]]] = ..., trainer_spec: _Optional[_Union[TrainerSpec, _Mapping]] = ..., normalizer_spec: _Optional[_Union[NormalizerSpec, _Mapping]] = ..., self_test_data: _Optional[_Union[SelfTestData, _Mapping]] = ..., denormalizer_spec: _Optional[_Union[NormalizerSpec, _Mapping]] = ...) -> None: ...
