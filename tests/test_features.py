"""Tests for src/features.py. Run them from the project folder with:  python -m pytest"""
import pytest

from src.features import (FEATURES, feature_table, flesch_reading_ease_ger, number_sentences,
                          punctuations, syllables, ttr, wiener_sachtext_formel, words)


def test_flesch_known_value():
    # 180 - 10 - 58.5 * 1.5 = 82.25
    assert flesch_reading_ease_ger(asl=10, asw=1.5) == 82.25


def test_syllables_of_single_words():
    assert syllables("haus") == 1
    assert syllables("katze") == 2
    assert syllables("sonnenschein") == 3


def test_words_ignore_punctuation_and_dashes():
    assert words("Er ging -- leise.") == ["er", "ging", "leise"]


def test_german_sentence_splitting():
    # The English model would also end a sentence after "1." and count 3 sentences.
    assert number_sentences("Am 1. Januar kam er. Er blieb.") == 2


def test_wiener_sachtextformel_by_hand():
    # 7 words, 2 sentences: MS 0 %, SL 3.5, IW 2 of 7 (schläft, draußen), ES 5 of 7  ->  1.08
    assert wiener_sachtext_formel("Der Hund schläft. Die Katze spielt draußen.") == 1.08


def test_punctuation_shares():
    tokens = ["ja", "!", "nein", ",", "gut", "."]
    assert punctuations(tokens) == pytest.approx((1 / 6, 0, 1 / 6, 1 / 6, 0, 0))


def test_type_token_ratio():
    assert ttr(["a", "b", "a", "b"]) == 0.5
    assert ttr([]) == 0


def test_feature_table_reads_author_from_file_name(tmp_path):
    (tmp_path / "kafka-test.txt").write_text("Er kam. Er ging.", encoding="utf-8")
    (tmp_path / "goethe-test.txt").write_text("Sie kam. Sie blieb.", encoding="utf-8-sig")  # utf-8-sig writes a BOM
    table = feature_table(tmp_path)
    assert list(table.columns) == ["file", "author"] + FEATURES
    assert list(table["file"]) == ["goethe-test", "kafka-test"]
    assert list(table["author"]) == ["Goethe", "Kafka"]
