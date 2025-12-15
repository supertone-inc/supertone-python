"""
TTS Text Processing Utilities

Stateless utility functions for text segmentation and NDJSON processing.
These functions are designed to be pure functions without side effects.
"""

import re
import json
import base64
from typing import List
from .constants import DEFAULT_MAX_TEXT_LENGTH


SENTENCE_SPLIT_PUNCTUATION = (
    # Latin/basic punctuation (commonly used across English + many European languages)
    ".!?;:"
    # Ellipsis variants
    "…‥"
    # CJK punctuation (Japanese)
    "。！？、"
    # Fullwidth forms (often appear in JP/KR text)
    "；：．"
    # Halfwidth ideographic full stop (sometimes used in Japanese)
    "｡"
    # Arabic punctuation
    "؟؛۔،"
    # Devanagari danda (Hindi) + double danda
    "।॥"
    # Greek question mark (U+037E, looks like a semicolon)
    ";"
)

_SENTENCE_SPLIT_RE = re.compile(rf"([{re.escape(SENTENCE_SPLIT_PUNCTUATION)}]+\s*)")


def _split_by_words(text: str, max_length: int) -> List[str]:
    """
    Split text by word boundaries when text exceeds max_length.

    Used as fallback when sentence-based splitting produces chunks that are too long.
    Splits on whitespace and ensures each chunk stays within the limit.

    :param text: Input text to split
    :param max_length: Maximum length of each chunk
    :return: List of text chunks split by words
    """
    words = text.split()
    if not words:
        # No spaces found, fall back to character-based splitting
        return _split_by_characters(text, max_length)

    chunks = []
    current_chunk = ""

    for word in words:
        # Check if adding this word would exceed the limit
        test_chunk = f"{current_chunk} {word}".strip() if current_chunk else word

        if len(test_chunk) <= max_length:
            current_chunk = test_chunk
        else:
            # Current chunk is complete, save it
            if current_chunk:
                chunks.append(current_chunk)

            # Check if the word itself exceeds max_length
            if len(word) > max_length:
                # Split the long word by characters
                word_chunks = _split_by_characters(word, max_length)
                # Add all but the last chunk
                chunks.extend(word_chunks[:-1])
                # Start new chunk with the last part
                current_chunk = word_chunks[-1] if word_chunks else ""
            else:
                current_chunk = word

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def _split_by_characters(text: str, max_length: int) -> List[str]:
    """
    Split text by character count when no word boundaries are available.

    Used for languages without spaces (e.g., Japanese, Chinese) or when
    a single word exceeds the maximum length.

    :param text: Input text to split
    :param max_length: Maximum length of each chunk
    :return: List of text chunks split by characters
    """
    if not text:
        return []

    chunks = []
    for i in range(0, len(text), max_length):
        chunks.append(text[i : i + max_length])

    return chunks


def _has_word_boundaries(text: str) -> bool:
    """
    Check if text contains word boundaries (spaces).

    Used to determine whether to use word-based or character-based splitting.

    :param text: Input text to check
    :return: True if text contains spaces, False otherwise
    """
    return " " in text


def _ensure_chunk_within_limit(chunk: str, max_length: int) -> List[str]:
    """
    Ensure a single chunk is within the max_length limit.

    If the chunk exceeds the limit, splits it using word boundaries first,
    then falls back to character-based splitting for languages without spaces.

    :param chunk: Input chunk that may exceed max_length
    :param max_length: Maximum allowed length
    :return: List of chunks, each within the limit
    """
    if len(chunk) <= max_length:
        return [chunk]

    # Try word-based splitting first
    if _has_word_boundaries(chunk):
        return _split_by_words(chunk, max_length)
    else:
        # No spaces (e.g., Japanese, Chinese) - split by characters
        return _split_by_characters(chunk, max_length)


def chunk_text(text: str, max_length: int = DEFAULT_MAX_TEXT_LENGTH) -> List[str]:
    """
    Split input text into sentence chunks suitable for TTS processing.

    Enhanced version that implements intelligent text segmentation respecting
    sentence boundaries while ensuring each chunk stays within TTS API limits.
    It handles various punctuation patterns and provides graceful fallback to
    word/character boundaries when necessary.

    Fallback strategies:
    1. Primary: Split by sentence punctuation (multilingual Unicode set)
    2. Secondary: Split by word boundaries (spaces) for long sentences
    3. Tertiary: Split by character count for languages without spaces (e.g., Japanese)

    :param text: Input text to be segmented
    :param max_length: Maximum length of each chunk
    :return: List of text chunks, each guaranteed to be <= max_length
    """
    if len(text) <= max_length:
        return [text]

    # Step 1: Split by sentence punctuation
    sentences = _SENTENCE_SPLIT_RE.split(text)

    # Step 2: Combine sentence parts and accumulate
    preliminary_chunks = []
    current_chunk = ""

    for sentence in sentences:
        if not sentence:
            continue
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence
        else:
            if current_chunk:
                preliminary_chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        preliminary_chunks.append(current_chunk)

    # Step 3: Ensure all chunks are within limit (handle long sentences)
    final_chunks = []
    for chunk in preliminary_chunks:
        if len(chunk) <= max_length:
            final_chunks.append(chunk)
        else:
            # Chunk exceeds limit - apply fallback splitting
            sub_chunks = _ensure_chunk_within_limit(chunk, max_length)
            final_chunks.extend(sub_chunks)

    return final_chunks


def extract_audio_from_ndjson(ndjson_str: str) -> bytes:
    """
    Extract audio data from NDJSON response.

    Handles both single JSON object and NDJSON (multiple lines) formats.
    Decodes base64-encoded audio data and returns as binary.

    :param ndjson_str: NDJSON string containing audio_base64 field
    :return: Decoded binary audio data
    """
    # Check if it's a single JSON object
    try:
        data = json.loads(ndjson_str)
        if "audio_base64" in data:
            return base64.b64decode(data["audio_base64"])
    except json.JSONDecodeError:
        pass

    # Process NDJSON (multiple lines)
    lines = ndjson_str.strip().split("\n")
    audio_data = b""

    for line in lines:
        if line.strip():
            try:
                data = json.loads(line)
                if "audio_base64" in data:
                    audio_data += base64.b64decode(data["audio_base64"])
            except (json.JSONDecodeError, Exception):
                continue

    return audio_data
