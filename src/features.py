"""Stylometric features for the authorship attribution of German literary texts.

The notebooks and scripts import their features from this module, so a fix applies everywhere.

    from src.features import FEATURES, feature_table
    corp = feature_table("data/corpus")    # one row per text: file, author, 12 features
"""
import re
from collections import Counter
from pathlib import Path

import nltk
import pandas as pd
import pyphen

FEATURES = [
    "AverageWordLength", "AverageSentenceLength", "AverageSyllables",
    "WienerSachtextFormel", "FRE_Ger", "TTR",
    "Avg !", "Avg ?", "Avg .", "Avg ,", "Avg ;", "Avg :",
]
PUNCTUATION = ["!", "?", ".", ",", ";", ":"]

_dic = pyphen.Pyphen(lang="de_DE")


# ---------------------------------------------------------------- loading
def load_corpus(folder):
    """All .txt files of a folder, sorted by file name: {file name without .txt: text}.

    Sorting by the name string gives the same order on every operating system.
    """
    files = sorted(Path(folder).glob("*.txt"), key=lambda p: p.name)
    return {p.stem: p.read_text(encoding="utf-8-sig") for p in files}


def author_of(file_name):
    """Author label from the file name: 'goethe-faust1' -> 'Goethe'."""
    return file_name.split("-")[0].capitalize()


# ---------------------------------------------------------------- words, sentences, syllables
def words(text):
    """All words of a text in lower case, without punctuation."""
    return re.findall(r"\b\w+\b", text.lower())


def syllables(word):
    """Number of syllables of one word, from the Pyphen hyphenation dictionary."""
    return len(_dic.inserted(word).split("-"))


def number_words(text):
    return len(words(text))


def number_sentences(text):
    return len(nltk.sent_tokenize(text, language="german"))


# ---------------------------------------------------------------- the 12 features
def avg_word_len(text):
    """Average word length in characters."""
    w = words(text)
    return round(sum(len(x) for x in w) / len(w), 1)


def avg_sen_len(text):
    """Average sentence length in words."""
    return round(number_words(text) / number_sentences(text), 1)


def avg_syllables_per_word(text):
    """Average number of syllables per word."""
    w = words(text)
    return round(sum(syllables(x) for x in w) / len(w), 1)


def flesch_reading_ease_ger(asl, asw):
    """Flesch Reading Ease, German version by Amstad: 180 - ASL - 58.5 * ASW."""
    return round(180 - asl - 58.5 * asw, 2)


def wiener_sachtext_formel(text):
    """First Wiener Sachtextformel (Bamberger & Vanecek)."""
    w = words(text)
    n = len(w)
    syl = [syllables(x) for x in w]
    ms = sum(s >= 3 for s in syl) / n * 100        # % words with three or more syllables
    sl = avg_sen_len(text)                         # words per sentence
    iw = sum(len(x) > 6 for x in w) / n * 100      # % words with more than six letters
    es = sum(s == 1 for s in syl) / n * 100        # % words with one syllable
    return round(0.1935 * ms + 0.1672 * sl + 0.1297 * iw - 0.0327 * es - 0.875, 2)


def ttr(tokens):
    """Type-token ratio: distinct tokens / all tokens."""
    return len(set(tokens)) / len(tokens) if tokens else 0


def punctuations(tokens):
    """Share of the tokens that are ! ? . , ; : (in this order)."""
    counts = Counter(tokens)
    return tuple(counts[p] / len(tokens) for p in PUNCTUATION)


def text_features(text):
    """The 12 features of one text, as {feature name: value} in the order of FEATURES."""
    tokens = nltk.word_tokenize(text.lower(), language="german")
    asl = avg_sen_len(text)
    asw = avg_syllables_per_word(text)
    values = [
        avg_word_len(text), asl, asw,
        wiener_sachtext_formel(text), flesch_reading_ease_ger(asl, asw),
        round(ttr(tokens), 2),
        *(round(share, 3) for share in punctuations(tokens)),
    ]
    return dict(zip(FEATURES, values))


def feature_table(folder):
    """One row per text of a folder: file, author and the 12 features."""
    rows = [{"file": name, "author": author_of(name), **text_features(text)}
            for name, text in load_corpus(folder).items()]
    return pd.DataFrame(rows)
