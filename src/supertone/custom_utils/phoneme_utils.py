"""
TTS Phoneme Processing Utilities

Stateless utility functions for phoneme data merging and timing adjustment.
These functions handle the synchronization of phoneme timing data across
multiple audio chunks.
"""

from typing import List, Dict, Any


def merge_phoneme_data(
    phoneme_chunks: List[Dict[str, List[Any]]],
) -> Dict[str, List[Any]]:
    """
    Merge multiple phoneme data chunks with automatic time offset
    adjustment.

    Handles the merging of phoneme data from multiple TTS chunks, ensuring
    continuous timing by adjusting start times and maintaining duration
    offsets. The first chunk's start time is normalized to 0, and
    subsequent chunks are offset accordingly.

    :param phoneme_chunks: List of phoneme dictionaries, each containing:
                          - symbols: List of phoneme symbols
                          - durations_seconds: List of phoneme durations
                          - start_times_seconds: List of start times
    :return: Merged phoneme dictionary with adjusted timing
    """
    merged: Dict[str, List[Any]] = {
        "symbols": [],
        "durations_seconds": [],
        "start_times_seconds": [],
    }

    if not phoneme_chunks:
        return merged

    first_chunk_start_time = None
    current_time_offset = 0.0

    for phoneme_data in phoneme_chunks:
        if not phoneme_data:
            continue

        # Add symbols
        symbols = phoneme_data.get("symbols", [])
        merged["symbols"].extend(symbols)

        # Add durations
        durations = phoneme_data.get("durations_seconds", [])
        merged["durations_seconds"].extend(durations)

        # Adjust and add start times
        if (
            "start_times_seconds" in phoneme_data
            and phoneme_data["start_times_seconds"]
        ):
            original_start_times = phoneme_data["start_times_seconds"]

            if first_chunk_start_time is None:
                # First chunk: normalize to start from 0
                first_chunk_start_time = original_start_times[0]
                adjusted_start_times = [
                    t - first_chunk_start_time for t in original_start_times
                ]
            else:
                # Subsequent chunks: apply accumulated offset
                adjusted_start_times = [
                    (t - first_chunk_start_time) + current_time_offset
                    for t in original_start_times
                ]

            merged["start_times_seconds"].extend(adjusted_start_times)

            # Update offset for next chunk
            if durations:
                current_time_offset += sum(durations)

    return merged


def adjust_phoneme_timing(
    phoneme_data: Dict[str, List[Any]], offset: float
) -> Dict[str, List[Any]]:
    """
    Apply time offset to phoneme start times.

    Creates a new phoneme dictionary with start times shifted by the
    specified offset. Useful for sequential streaming scenarios.

    :param phoneme_data: Phoneme dictionary with timing data
    :param offset: Time offset in seconds to add to all start times
    :return: New phoneme dictionary with adjusted start times
    """
    adjusted = phoneme_data.copy()

    if "start_times_seconds" in adjusted and adjusted["start_times_seconds"]:
        adjusted["start_times_seconds"] = [
            t + offset for t in phoneme_data["start_times_seconds"]
        ]

    return adjusted


def create_empty_phoneme_dict() -> Dict[str, List[Any]]:
    """
    Create an empty phoneme dictionary with standard structure.

    :return: Empty phoneme dictionary
    """
    return {
        "symbols": [],
        "durations_seconds": [],
        "start_times_seconds": [],
    }
