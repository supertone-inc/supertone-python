#!/usr/bin/env python3
"""
Smoke test for multilingual sentence punctuation splitting in chunk_text().

This is intentionally lightweight (no external test runner required).
Run:
  python custom_test/test_text_utils_chunk_text_punctuation.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supertone.custom_utils.text_utils import chunk_text  # noqa: E402


def _assert_splits(text: str, expected_chunks: list[str], *, max_length: int):
    got = chunk_text(text, max_length=max_length)
    assert got == expected_chunks, f"\ntext={text!r}\nexpected={expected_chunks!r}\ngot={got!r}"


def main():
    # English / many EU languages
    _assert_splits("Hello. World!", ["Hello. ", "World!"], max_length=8)

    # Korean (mostly ASCII punctuation in practice, plus ellipsis)
    _assert_splits(
        "안...반가… 네.", ["안...", "반가… ", "네."], max_length=4
    )

    # Japanese
    _assert_splits(
        "こんにちは。元気ですか？はい！", ["こんにちは。", "元気ですか？", "はい！"], max_length=6
    )

    # Arabic
    _assert_splits(
        "مر؟ نعم۔ لا؛ حس،", ["مر؟ ", "نعم۔ ", "لا؛ ", "حس،"], max_length=5
    )

    # Hindi
    _assert_splits("ना।ठी।हाँ॥", ["ना।", "ठी।", "हाँ॥"], max_length=4)

    # Greek question mark (U+037E)
    _assert_splits("Γεια;Καλά.", ["Γεια;", "Καλά."], max_length=5)

    print("OK: chunk_text punctuation smoke test passed")


if __name__ == "__main__":
    main()


