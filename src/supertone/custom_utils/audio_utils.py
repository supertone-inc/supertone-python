"""
TTS Audio Processing Utilities

Stateless utility functions for WAV and MP3 audio manipulation.
Provides binary-level audio processing without external dependencies.
"""

import struct
from typing import List, Any
from .constants import (
    WAV_HEADER_SIZE,
    WAV_RIFF_HEADER_SIZE,
    WAV_CHUNK_HEADER_SIZE,
    MP3_ID3V2_HEADER_SIZE,
    MP3_ID3V1_TAG_POS,
)


def merge_wav_binary(audio_chunks: List[bytes]) -> bytes:
    """
    Merge binary WAV data chunks into a single WAV file.

    Extracts audio data from each chunk, combines them, and creates a new
    WAV header with correct file size information. Preserves audio format
    parameters (channels, sample rate, etc.) from the first chunk.

    :param audio_chunks: List of binary WAV data to merge
    :return: Merged WAV file as binary data
    """
    if not audio_chunks:
        return b""

    first_audio_data = audio_chunks[0]

    # Parse WAV header from first chunk
    wav_header = first_audio_data[:WAV_HEADER_SIZE]
    channels = struct.unpack("<H", wav_header[22:24])[0]
    sample_rate = struct.unpack("<I", wav_header[24:28])[0]
    byte_rate = struct.unpack("<I", wav_header[28:32])[0]
    block_align = struct.unpack("<H", wav_header[32:34])[0]
    bits_per_sample = struct.unpack("<H", wav_header[34:36])[0]

    # Collect all audio data (skip headers)
    all_audio_data = b""
    for audio_data in audio_chunks:
        # Skip WAV header and extract only audio data
        if len(audio_data) >= WAV_HEADER_SIZE and audio_data[:4] == b"RIFF":
            # Find data chunk
            pos = WAV_RIFF_HEADER_SIZE
            while pos < len(audio_data) - WAV_CHUNK_HEADER_SIZE:
                chunk_id = audio_data[pos : pos + 4]
                chunk_size = struct.unpack("<I", audio_data[pos + 4 : pos + 8])[0]
                if chunk_id == b"data":
                    all_audio_data += audio_data[pos + 8 : pos + 8 + chunk_size]
                    break
                pos += 8 + chunk_size
        else:
            all_audio_data += audio_data

    # Create new WAV file header
    total_length = len(all_audio_data)
    file_size = total_length + WAV_RIFF_HEADER_SIZE

    merged_wav = bytearray()
    merged_wav.extend(b"RIFF")
    merged_wav.extend(struct.pack("<I", file_size))
    merged_wav.extend(b"WAVE")
    merged_wav.extend(b"fmt ")
    merged_wav.extend(struct.pack("<I", 16))  # fmt chunk size
    merged_wav.extend(struct.pack("<H", 1))  # audio format (PCM)
    merged_wav.extend(struct.pack("<H", channels))
    merged_wav.extend(struct.pack("<I", sample_rate))
    merged_wav.extend(struct.pack("<I", byte_rate))
    merged_wav.extend(struct.pack("<H", block_align))
    merged_wav.extend(struct.pack("<H", bits_per_sample))
    merged_wav.extend(b"data")
    merged_wav.extend(struct.pack("<I", total_length))
    merged_wav.extend(all_audio_data)

    return bytes(merged_wav)


def merge_mp3_binary(audio_chunks: List[bytes]) -> bytes:
    """
    Merge MP3 audio chunks using simple concatenation.

    This is a practical approach for MP3 merging. For more advanced
    MP3 merging with proper frame handling, consider using external
    libraries like pydub or ffmpeg.

    :param audio_chunks: List of binary MP3 data to merge
    :return: Concatenated MP3 data
    """
    return b"".join(audio_chunks)


def remove_wav_header(audio_data: bytes) -> bytes:
    """
    Remove WAV header from audio data.

    Used for intermediate chunks when merging multiple WAV files.
    Finds the "data" chunk and returns only the audio data portion.

    :param audio_data: Binary WAV data with header
    :return: Binary audio data without header
    """
    if len(audio_data) >= WAV_HEADER_SIZE and audio_data[:4] == b"RIFF":
        # Find "data" chunk
        data_pos = audio_data.find(b"data")
        if data_pos > 0:
            # Skip "data" + 4-byte size info
            return audio_data[data_pos + 8 :]
    return audio_data


def remove_mp3_header(mp3_data: bytes) -> bytes:
    """
    Remove MP3 ID3 tags (v1 and v2) from audio data.

    Handles both ID3v2 tags (at the beginning) and ID3v1 tags (at the end).
    Returns pure MPEG audio data without metadata.

    :param mp3_data: Binary MP3 data with headers
    :return: Binary MP3 data without ID3 tags
    """
    # Remove ID3v2 tag (at beginning)
    if len(mp3_data) >= MP3_ID3V2_HEADER_SIZE and mp3_data[:3] == b"ID3":
        size = (
            (mp3_data[6] << 21) | (mp3_data[7] << 14) | (mp3_data[8] << 7) | mp3_data[9]
        )
        header_size = MP3_ID3V2_HEADER_SIZE
        if mp3_data[5] & 0x10:  # Footer present
            header_size += MP3_ID3V2_HEADER_SIZE
        mp3_data = mp3_data[header_size + size :]

    # Remove ID3v1 tag (at end of file)
    if (
        len(mp3_data) >= MP3_ID3V1_TAG_POS
        and mp3_data[-MP3_ID3V1_TAG_POS : -MP3_ID3V1_TAG_POS + 3] == b"TAG"
    ):
        mp3_data = mp3_data[:-MP3_ID3V1_TAG_POS]

    return mp3_data


def detect_audio_format(audio_data: bytes) -> str:
    """
    Detect audio format from binary data.

    Examines the first few bytes to determine if the data is WAV, MP3,
    or unknown format.

    :param audio_data: Binary audio data
    :return: Format string: 'wav', 'mp3', or 'unknown'
    """
    if len(audio_data) >= 4 and audio_data[:4] == b"RIFF":
        return "wav"
    elif len(audio_data) >= 3 and audio_data[:3] == b"ID3":
        return "mp3"
    elif len(audio_data) >= 2 and (
        audio_data[:2] == b"\xff\xfb" or audio_data[:2] == b"\xff\xfa"
    ):
        return "mp3"
    return "unknown"


async def extract_audio_from_response_async(response: Any) -> bytes:
    """
    Extract audio data from httpx response (async version).

    Handles various response types and caches the result in _content
    to prevent multiple reads of the same stream.

    :param response: Response object with result attribute
    :return: Binary audio data
    """
    # Check if already cached
    if hasattr(response.result, "_content") and response.result._content is not None:
        return response.result._content

    # Read from async iterator
    if hasattr(response.result, "aiter_bytes"):
        chunks = []
        async for chunk in response.result.aiter_bytes():
            chunks.append(chunk)
        audio_data = b"".join(chunks)
        # Cache for reuse
        response.result._content = audio_data
        return audio_data

    # Fallback to sync read (shouldn't happen in async context)
    if hasattr(response.result, "read"):
        return response.result.read()

    # Last resort: convert to bytes
    return bytes(response.result)


def extract_audio_from_response(response: Any) -> bytes:
    """
    Extract audio data from httpx response (sync version).

    :param response: Response object with result attribute
    :return: Binary audio data
    """
    if hasattr(response.result, "read"):
        return response.result.read()
    elif hasattr(response.result, "content"):
        return response.result.content
    else:
        return bytes(response.result)


async def extract_audio_from_responses_async(responses: List[Any]) -> List[bytes]:
    """
    Extract audio data from multiple responses (async version).

    Processes each response and returns a list of binary audio data.
    This is useful for batch audio extraction in parallel TTS operations.

    :param responses: List of response objects with result attribute
    :return: List of extracted binary audio data
    """
    audio_chunks = []
    for response in responses:
        audio_data = await extract_audio_from_response_async(response)
        audio_chunks.append(audio_data)
    return audio_chunks


def extract_audio_from_responses(responses: List[Any]) -> List[bytes]:
    """
    Extract audio data from multiple responses (sync version).

    Processes each response and returns a list of binary audio data.
    This is useful for batch audio extraction in parallel TTS operations.

    :param responses: List of response objects with result attribute
    :return: List of extracted binary audio data
    """
    audio_chunks = []
    for response in responses:
        audio_data = extract_audio_from_response(response)
        audio_chunks.append(audio_data)
    return audio_chunks
