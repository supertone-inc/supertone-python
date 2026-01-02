"""
Pronunciation dictionary substitution utilities.

Provides a small, stateless helper for applying a client-side pronunciation
dictionary before sending text to the TTS API. This keeps logic reusable and
testable while matching the existing custom_utils style.
"""

from typing import Any, Dict, List, Mapping, Optional
import re
import uuid


class PronunciationDictionaryValidationError(ValueError):
    """Raised when pronunciation_dictionary payload is invalid."""


def apply_pronunciation_dictionary(
    text: str,
    pronunciation_dictionary: Optional[List[Mapping[str, Any]]] = None,
) -> str:
    """
    Apply pronunciation dictionary substitutions to `text`.

    Rules:
    - Entries are applied in the order provided.
    - partial_match=False: replace exact word-boundary matches only.
    - partial_match=True: replace all substring matches (no boundary checks).
    - Prevent re-substitution: replaced segments are protected via opaque tokens.

    Validation:
    - pronunciation_dictionary is optional; None returns the original text.
    - Expected shape: list of objects with text(str), pronunciation(str),
      partial_match(bool). Empty strings are invalid.
    """

    if not pronunciation_dictionary:
        return text

    if not isinstance(text, str):
        raise PronunciationDictionaryValidationError(
            f"`text` must be str, got {type(text).__name__}"
        )

    if not isinstance(pronunciation_dictionary, list):
        raise PronunciationDictionaryValidationError(
            "`pronunciation_dictionary` must be a list of objects"
        )

    # Prevent re-substitution by replacing matches with opaque tokens first,
    # then expanding tokens into final pronunciations at the end.
    token_to_pronunciation: Dict[str, str] = {}
    working = text

    for idx, raw_entry in enumerate(pronunciation_dictionary):
        entry = _validate_dictionary_entry(raw_entry, idx)
        src = entry["text"]
        dst = entry["pronunciation"]
        partial_match = entry["partial_match"]

        if partial_match:
            pattern = re.escape(src)
        else:
            # Word-boundary match using Unicode \w semantics.
            pattern = rf"(?<!\w){re.escape(src)}(?!\w)"

        compiled = re.compile(pattern)

        # Generate token only after confirming a match exists.
        # Use subn() to replace and count matches in a single pass.
        token = _make_unique_token(idx, working, token_to_pronunciation)
        working, count = compiled.subn(token, working)

        if count == 0:
            continue

        token_to_pronunciation[token] = dst

    # Expand tokens into pronunciations.
    for token, pronunciation in token_to_pronunciation.items():
        working = working.replace(token, pronunciation)

    return working


def _validate_dictionary_entry(raw_entry: Any, idx: int) -> Dict[str, Any]:
    if not isinstance(raw_entry, Mapping):
        raise PronunciationDictionaryValidationError(
            f"pronunciation_dictionary[{idx}] must be an object, got {type(raw_entry).__name__}"
        )

    missing = [
        k for k in ("text", "pronunciation", "partial_match") if k not in raw_entry
    ]
    if missing:
        raise PronunciationDictionaryValidationError(
            f"pronunciation_dictionary[{idx}] missing required field(s): {', '.join(missing)}"
        )

    src = raw_entry["text"]
    dst = raw_entry["pronunciation"]
    partial = raw_entry["partial_match"]

    if not isinstance(src, str):
        raise PronunciationDictionaryValidationError(
            f"pronunciation_dictionary[{idx}].text must be str, got {type(src).__name__}"
        )
    if not isinstance(dst, str):
        raise PronunciationDictionaryValidationError(
            f"pronunciation_dictionary[{idx}].pronunciation must be str, got {type(dst).__name__}"
        )
    if not isinstance(partial, bool):
        raise PronunciationDictionaryValidationError(
            f"pronunciation_dictionary[{idx}].partial_match must be bool, got {type(partial).__name__}"
        )

    if src == "":
        raise PronunciationDictionaryValidationError(
            f"pronunciation_dictionary[{idx}].text must not be empty"
        )
    if dst == "":
        raise PronunciationDictionaryValidationError(
            f"pronunciation_dictionary[{idx}].pronunciation must not be empty"
        )

    return {"text": src, "pronunciation": dst, "partial_match": partial}


def _make_unique_token(idx: int, working: str, existing: Mapping[str, str]) -> str:
    # Use Private Use Area characters to avoid collisions with normal text.
    base = f"\ue000PD{idx}\ue001"
    if base not in working and base not in existing:
        return base
    while True:
        token = f"\ue000PD{idx}_{uuid.uuid4().hex}\ue001"
        if token not in working and token not in existing:
            return token
