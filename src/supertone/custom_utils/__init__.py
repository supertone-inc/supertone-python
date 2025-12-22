"""
TTS Custom Utilities

Custom implementation utilities for automatic text chunking and audio
merging. These utilities are part of the enhanced TTS functionality and
are designed to be stateless, reusable, and easily testable.

Modules:
    - constants: Audio format and text processing constants
    - text_utils: Text segmentation and NDJSON processing
    - pronunciation_utils: Pronunciation dictionary substitutions
    - audio_utils: WAV and MP3 audio binary manipulation
"""

# Constants
from .constants import (
    WAV_HEADER_SIZE,
    WAV_RIFF_HEADER_SIZE,
    WAV_CHUNK_HEADER_SIZE,
    MP3_ID3V2_HEADER_SIZE,
    MP3_ID3V1_TAG_POS,
    DEFAULT_STREAM_CHUNK_SIZE,
    DEFAULT_MAX_TEXT_LENGTH,
    MAX_PARALLEL_WORKERS,
)

# Text utilities
from .text_utils import (
    chunk_text,
    extract_audio_from_ndjson,
)

# Pronunciation utilities
from .pronunciation_utils import (
    apply_pronunciation_dictionary,
    PronunciationDictionaryValidationError,
)

# Audio utilities
from .audio_utils import (
    merge_wav_binary,
    merge_mp3_binary,
    remove_wav_header,
    remove_mp3_header,
    detect_audio_format,
    extract_audio_from_response,
    extract_audio_from_response_async,
    extract_audio_from_responses,
    extract_audio_from_responses_async,
)

# Phoneme utilities
from .phoneme_utils import (
    merge_phoneme_data,
    adjust_phoneme_timing,
    create_empty_phoneme_dict,
)

# Logger utilities
from .logger_utils import (
    get_logger,
    enable_debug_logging,
    disable_logging,
)

__all__ = [
    # Constants
    "WAV_HEADER_SIZE",
    "WAV_RIFF_HEADER_SIZE",
    "WAV_CHUNK_HEADER_SIZE",
    "MP3_ID3V2_HEADER_SIZE",
    "MP3_ID3V1_TAG_POS",
    "DEFAULT_STREAM_CHUNK_SIZE",
    "DEFAULT_MAX_TEXT_LENGTH",
    "MAX_PARALLEL_WORKERS",
    # Text utilities
    "chunk_text",
    "extract_audio_from_ndjson",
    # Pronunciation utilities
    "apply_pronunciation_dictionary",
    "PronunciationDictionaryValidationError",
    # Audio utilities
    "merge_wav_binary",
    "merge_mp3_binary",
    "remove_wav_header",
    "remove_mp3_header",
    "detect_audio_format",
    "extract_audio_from_response",
    "extract_audio_from_response_async",
    "extract_audio_from_responses",
    "extract_audio_from_responses_async",
    # Phoneme utilities
    "merge_phoneme_data",
    "adjust_phoneme_timing",
    "create_empty_phoneme_dict",
    # Logger utilities
    "get_logger",
    "enable_debug_logging",
    "disable_logging",
]
