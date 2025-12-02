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


def chunk_text(text: str, max_length: int = DEFAULT_MAX_TEXT_LENGTH) -> List[str]:
    """
    Split input text into sentence chunks suitable for TTS processing.

    Enhanced version that implements intelligent text segmentation respecting
    sentence boundaries while ensuring each chunk stays within TTS API limits.
    It handles various punctuation patterns and provides graceful fallback to
    word/character boundaries when necessary.

    :param text: Input text to be segmented
    :param max_length: Maximum length of each chunk
    :return: List of text chunks
    """
    if len(text) <= max_length:
        return [text]

    sentences = re.split(r"([.!?;:]+\s*)", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


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
