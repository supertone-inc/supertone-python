#!/usr/bin/env python3
"""
Smoke/behavior tests for apply_pronunciation_dictionary().

Run:
  python custom_test/test_pronunciation_dictionary.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supertone.custom_utils import (  # noqa: E402
    PronunciationDictionaryValidationError,
    apply_pronunciation_dictionary,
)


class TestPronunciationDictionary(unittest.TestCase):
    def test_none_dictionary_returns_original(self):
        self.assertEqual(apply_pronunciation_dictionary("hello", None), "hello")

    def test_empty_dictionary_returns_original(self):
        self.assertEqual(apply_pronunciation_dictionary("hello", []), "hello")

    def test_basic_exact_word_boundary_english_punct(self):
        text = "This is Supertone."
        d = [{"text": "Supertone", "pronunciation": "super tone", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "This is super tone.")

    def test_exact_match_does_not_replace_partial(self):
        text = "This is Supertone."
        d = [{"text": "Super", "pronunciation": "X", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "This is Supertone.")

    def test_partial_match_true_replaces_substrings_including_hyphenated(self):
        text = "K-TTS is different from TTSAPI."
        d = [{"text": "TTS", "pronunciation": "text to speech", "partial_match": True}]
        self.assertEqual(
            apply_pronunciation_dictionary(text, d),
            "K-text to speech is different from text to speechAPI.",
        )

    def test_multiple_occurrences(self):
        text = "TTS and TTS and TTS."
        d = [{"text": "TTS", "pronunciation": "text to speech", "partial_match": True}]
        self.assertEqual(
            apply_pronunciation_dictionary(text, d),
            "text to speech and text to speech and text to speech.",
        )

    def test_exact_match_with_quotes_parentheses_commas(self):
        text = 'He said, "Supertone", (Supertone)!'
        d = [{"text": "Supertone", "pronunciation": "super tone", "partial_match": False}]
        self.assertEqual(
            apply_pronunciation_dictionary(text, d),
            'He said, "super tone", (super tone)!',
        )

    def test_exact_match_does_not_match_inside_underscore_word(self):
        text = "API_test API test_API"
        d = [{"text": "API", "pronunciation": "A P I", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "API_test A P I test_API")

    def test_exact_match_numbers_and_cplusplus(self):
        text = "C++ is old, C++11 is newer."
        d = [{"text": "C++", "pronunciation": "cplusplus", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "cplusplus is old, C++11 is newer.")

    def test_partial_match_with_regex_metacharacters_in_src(self):
        text = "a(b)c a(b)c"
        d = [{"text": "a(b)c", "pronunciation": "X", "partial_match": True}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "X X")

    def test_overlapping_matches_are_non_overlapping_left_to_right(self):
        text = "aaaa"
        d = [{"text": "aa", "pronunciation": "b", "partial_match": True}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "bb")

    def test_rule_order_changes_result_when_sources_overlap(self):
        text = "AAAA"
        d1 = [
            {"text": "AA", "pronunciation": "B", "partial_match": True},
            {"text": "A", "pronunciation": "C", "partial_match": True},
        ]
        d2 = [
            {"text": "A", "pronunciation": "C", "partial_match": True},
            {"text": "AA", "pronunciation": "B", "partial_match": True},
        ]
        self.assertEqual(apply_pronunciation_dictionary(text, d1), "BB")
        self.assertEqual(apply_pronunciation_dictionary(text, d2), "CCCC")

    def test_no_resubstitution_but_later_rules_can_apply_to_other_original_parts(self):
        text = "NY is not New Jersey."
        d = [
            {"text": "NY", "pronunciation": "New York", "partial_match": False},
            {"text": "New", "pronunciation": "Old", "partial_match": False},
        ]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "New York is not Old Jersey.")

    def test_order_priority_overlap_ap_apec_bad_order(self):
        text = "이번 APEC 은 한국에서 열립니다"
        d = [
            {"text": "AP", "pronunciation": "에이피", "partial_match": True},
            {"text": "APEC", "pronunciation": "에이팩", "partial_match": True},
        ]
        self.assertEqual(
            apply_pronunciation_dictionary(text, d),
            "이번 에이피EC 은 한국에서 열립니다",
        )

    def test_order_priority_overlap_apec_first_good(self):
        text = "이번 APEC 은 한국에서 열립니다"
        d = [
            {"text": "APEC", "pronunciation": "에이팩", "partial_match": True},
            {"text": "AP", "pronunciation": "에이피", "partial_match": True},
        ]
        self.assertEqual(
            apply_pronunciation_dictionary(text, d),
            "이번 에이팩 은 한국에서 열립니다",
        )

    def test_no_resubstitution_inside_previous_pronunciation(self):
        text = "Supertone tone"
        d = [
            {"text": "Supertone", "pronunciation": "super tone", "partial_match": False},
            {"text": "tone", "pronunciation": "TONE", "partial_match": False},
        ]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "super tone TONE")

    def test_partial_match_can_match_inside_korean_sentence(self):
        text = "TTS와 TTSAPI는 다릅니다."
        d = [{"text": "TTS", "pronunciation": "text to speech", "partial_match": True}]
        self.assertEqual(
            apply_pronunciation_dictionary(text, d),
            "text to speech와 text to speechAPI는 다릅니다.",
        )

    def test_exact_match_does_not_work_for_no_whitespace_scripts_adjacent(self):
        text = "東京TTS東京"
        d = [{"text": "TTS", "pronunciation": "text to speech", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "東京TTS東京")

    def test_exact_match_false_is_almost_useless_in_japanese_sentences_without_spaces(self):
        text = "これはTTSです。東京TTS東京でもTTSです"
        d = [{"text": "TTS", "pronunciation": "text to speech", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), text)

    def test_exact_match_can_work_in_japanese_if_punctuation_creates_boundaries(self):
        text = "これは「TTS」です。"
        d = [{"text": "TTS", "pronunciation": "text to speech", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "これは「text to speech」です。")

    def test_partial_match_works_for_no_whitespace_scripts_adjacent(self):
        text = "東京TTS東京"
        d = [{"text": "TTS", "pronunciation": "text to speech", "partial_match": True}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "東京text to speech東京")

    def test_token_collision_in_input_text_is_handled(self):
        token_like = "\uE000PD0\uE001"
        text = f"X {token_like} Supertone"
        d = [{"text": "Supertone", "pronunciation": "super tone", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), f"X {token_like} super tone")

    def test_validation_dictionary_must_be_list(self):
        with self.assertRaises(PronunciationDictionaryValidationError):
            apply_pronunciation_dictionary("hi", {"text": "a"})  # type: ignore[arg-type]

    def test_validation_entry_must_be_object(self):
        with self.assertRaises(PronunciationDictionaryValidationError):
            apply_pronunciation_dictionary(
                "hi",
                ["not-an-object"],  # type: ignore[list-item]
            )

    def test_validation_text_must_be_str(self):
        with self.assertRaises(PronunciationDictionaryValidationError):
            apply_pronunciation_dictionary(
                "hi",
                [{"text": 123, "pronunciation": "b", "partial_match": True}],  # type: ignore[list-item]
            )

    def test_validation_pronunciation_must_be_str(self):
        with self.assertRaises(PronunciationDictionaryValidationError):
            apply_pronunciation_dictionary(
                "hi",
                [{"text": "a", "pronunciation": None, "partial_match": True}],  # type: ignore[list-item]
            )

    def test_validation_missing_field(self):
        with self.assertRaises(PronunciationDictionaryValidationError):
            apply_pronunciation_dictionary(
                "hi", [{"text": "a", "pronunciation": "b"}]
            )

    def test_validation_wrong_type(self):
        with self.assertRaises(PronunciationDictionaryValidationError):
            apply_pronunciation_dictionary(
                "hi",
                [{"text": "a", "pronunciation": "b", "partial_match": "true"}],  # type: ignore[list-item]
            )

    def test_validation_empty_string(self):
        with self.assertRaises(PronunciationDictionaryValidationError):
            apply_pronunciation_dictionary(
                "hi", [{"text": "", "pronunciation": "b", "partial_match": True}]
            )

        with self.assertRaises(PronunciationDictionaryValidationError):
            apply_pronunciation_dictionary(
                "hi", [{"text": "a", "pronunciation": "", "partial_match": True}]
            )

    def test_word_boundary_unicode_note(self):
        text = "TTS와 TTS."
        d = [{"text": "TTS", "pronunciation": "text to speech", "partial_match": False}]
        self.assertEqual(apply_pronunciation_dictionary(text, d), "TTS와 text to speech.")


if __name__ == "__main__":
    unittest.main(verbosity=2)


