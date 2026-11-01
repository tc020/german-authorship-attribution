# Data

36 German literary texts by five authors, 983,624 words in total. All of them are in the public domain and come from [Project Gutenberg](https://www.gutenberg.org).

| Path | Content |
|---|---|
| [`corpus/`](corpus/) | the 36 texts that all analyses use, one file per text, cleaned as described [below](#cleaning) |
| [`raw/`](raw/) | the texts as collected for the original study, before the cleaning |
| [`features.csv`](features.csv) | 12 style features per text |

File names follow the pattern `author-title.txt`. The notebooks read the author label from the part before the first hyphen. All files are UTF-8 with a byte order mark, so read them with `encoding="utf-8-sig"`.

## Texts

The word counts refer to the cleaned texts and were counted with the NLTK tokenizer (NLTK 3.10). Every token that contains at least one letter counts as a word, so punctuation marks and numbers are left out:

```python
from nltk.tokenize import word_tokenize

tokens = word_tokenize(text, language="german")
n_words = sum(any(char.isalpha() for char in token) for token in tokens)
```

### Arthur Achleitner

5 texts, 264,658 words

| File | Work | Project Gutenberg | Words |
|---|---|---|--:|
| `achleitner-Aus_Kroatien.txt` | *Aus Kroatien: Skizzen und Erzählungen* | [#15734](https://www.gutenberg.org/ebooks/15734) | 33,137 |
| `achleitner-Bergrichters_Erdenwallen.txt` | *Bergrichters Erdenwallen* | [#14225](https://www.gutenberg.org/ebooks/14225) | 46,033 |
| `achleitner-Celsissimus.txt` | *Celsissimus: Salzburger Roman* | [#13953](https://www.gutenberg.org/ebooks/13953) | 67,975 |
| `achleitner-Im_gruenen_Tann.txt` | *Im grünen Tann* | [#14105](https://www.gutenberg.org/ebooks/14105) | 54,174 |
| `achleitner-Unter_den_Hohen_Tauern.txt` | *Unter den Hohen Tauern: Ein Roman aus der Steiermark* | [#63802](https://www.gutenberg.org/ebooks/63802) | 63,339 |

### Anonymous: *Der Luftpirat und sein lenkbares Luftschiff*

6 texts, 73,984 words

| File | Work | Project Gutenberg | Words |
|---|---|---|--:|
| `anonymous-Der Luftpirat und sein lenkbares Luftschiff 01.txt` | Issue 1 | [#56064](https://www.gutenberg.org/ebooks/56064) | 12,827 |
| `anonymous-Der Luftpirat und sein lenkbares Luftschiff 40.txt` | Issue 40 | [#56065](https://www.gutenberg.org/ebooks/56065) | 13,048 |
| `anonymous-Der Luftpirat und sein lenkbares Luftschiff 42.txt` | Issue 42 | [#56066](https://www.gutenberg.org/ebooks/56066) | 13,087 |
| `anonymous-Der Luftpirat und sein lenkbares Luftschiff 56.txt` | Issue 56 | [#56067](https://www.gutenberg.org/ebooks/56067) | 11,758 |
| `anonymous-Der Luftpirat und sein lenkbares Luftschiff 63.txt` | Issue 63 | [#56068](https://www.gutenberg.org/ebooks/56068) | 11,464 |
| `anonymous-Der Luftpirat und sein lenkbares Luftschiff 66.txt` | Issue 66 | [#56069](https://www.gutenberg.org/ebooks/56069) | 11,800 |

### Johann Wolfgang von Goethe

7 texts, 261,779 words

| File | Work | Project Gutenberg | Words |
|---|---|---|--:|
| `goethe-die_leiden_des_jungen_werther_band1.txt` | *Die Leiden des jungen Werther*, Band 1 | [#2407](https://www.gutenberg.org/ebooks/2407) | 17,751 |
| `goethe-die_leiden_des_jungen_werther_band2.txt` | *Die Leiden des jungen Werther*, Band 2 | [#2408](https://www.gutenberg.org/ebooks/2408) | 21,525 |
| `goethe-faust1.txt` | *Faust: Der Tragödie erster Teil* | [#2229](https://www.gutenberg.org/ebooks/2229) | 30,887 |
| `goethe-faust2.txt` | *Faust: Der Tragödie zweiter Teil* | [#2230](https://www.gutenberg.org/ebooks/2230) | 45,715 |
| `goethe-wahlverwandtschaften.txt` | *Die Wahlverwandtschaften* | [#2403](https://www.gutenberg.org/ebooks/2403) | 79,119 |
| `goethe-wilhelm_meisters_lehrjahre_band1.txt` | *Wilhelm Meisters Lehrjahre*, Band 1 | [#2335](https://www.gutenberg.org/ebooks/2335) | 21,308 |
| `goethe-wilhelm_meisters_wanderjahre_band1.txt` | *Wilhelm Meisters Wanderjahre*, Band 1 | [#2409](https://www.gutenberg.org/ebooks/2409) | 45,474 |

### Franz Kafka

8 texts, 137,631 words

| File | Work | Project Gutenberg | Words |
|---|---|---|--:|
| `kafka-betrachtung.txt` | *Betrachtung* | [#23532](https://www.gutenberg.org/ebooks/23532) | 5,863 |
| `kafka-das_urteil.txt` | *Das Urteil: Eine Geschichte* | [#21593](https://www.gutenberg.org/ebooks/21593) | 3,995 |
| `kafka-der-heizer-ein-fragment.txt` | *Der Heizer: Ein Fragment* | [#16304](https://www.gutenberg.org/ebooks/16304) | 10,168 |
| `kafka-der_prozess.txt` | *Der Prozess: Roman* | [#69327](https://www.gutenberg.org/ebooks/69327) | 71,619 |
| `kafka-die_verwandlung.txt` | *Die Verwandlung* | [#22367](https://www.gutenberg.org/ebooks/22367) | 19,151 |
| `kafka-hungerkünstler.txt` | *Ein Hungerkünstler* | [#30655](https://www.gutenberg.org/ebooks/30655) | 3,422 |
| `kafka-in_der_strafkolonie.txt` | *In der Strafkolonie* | [#25791](https://www.gutenberg.org/ebooks/25791) | 10,275 |
| `kafka-landarzt.txt` | *Ein Landarzt: Kleine Erzählungen* | [#21989](https://www.gutenberg.org/ebooks/21989) | 13,138 |

### Friedrich Schiller

10 texts, 245,572 words

| File | Work | Project Gutenberg | Words |
|---|---|---|--:|
| `schiller-Der Neffe als Onkel.txt` | *Der Neffe als Onkel* | [#6503](https://www.gutenberg.org/ebooks/6503) | 12,729 |
| `schiller-Die Braut von Messina.txt` | *Die Braut von Messina* | [#6496](https://www.gutenberg.org/ebooks/6496) | 20,972 |
| `schiller-Die Jungfrau von Orleans.txt` | *Die Jungfrau von Orleans* | [#6383](https://www.gutenberg.org/ebooks/6383) | 25,713 |
| `schiller-Die Piccolomini.txt` | *Die Piccolomini* | [#6525](https://www.gutenberg.org/ebooks/6525) | 21,437 |
| `schiller-Die Verschwörung des Fiesco zu Genua.txt` | *Die Verschwörung des Fiesco zu Genua* | [#6499](https://www.gutenberg.org/ebooks/6499) | 30,257 |
| `schiller-Kabale und Liebe.txt` | *Kabale und Liebe* | [#6498](https://www.gutenberg.org/ebooks/6498) | 31,052 |
| `schiller-Turandot Prinzessin von China.txt` | *Turandot, Prinzessin von China* | [#6505](https://www.gutenberg.org/ebooks/6505) | 21,423 |
| `schiller-Wallensteins Lager.txt` | *Wallensteins Lager* | [#6518](https://www.gutenberg.org/ebooks/6518) | 9,010 |
| `schiller-Wallensteins Tod.txt` | *Wallensteins Tod* | [#6549](https://www.gutenberg.org/ebooks/6549) | 31,813 |
| `schiller-raeuber.txt` | *Die Räuber: Ein Schauspiel* | [#47804](https://www.gutenberg.org/ebooks/47804) | 41,166 |

### Things to know about the corpus

- **Genre.** All ten Schiller texts and both parts of *Faust* are plays, all other texts are prose. Genre and author are therefore partly confounded, see the [findings](../README.md#findings) in the main README.
- **Translations and adaptations.** *Turandot, Prinzessin von China* is Schiller's adaptation of a play by Carlo Gozzi, and *Der Neffe als Onkel* is his translation of *Encore des Ménechmes* by Louis-Benoît Picard. Part of their style comes from the original authors.
- **Recurring names.** The two *Werther* files are the two books of one novel, *Faust I* and *II* belong together, the three Wallenstein plays form a trilogy and the six *Luftpirat* issues are one series. Names such as Lotte, Mephistopheles, Wallenstein and Kapitän Mors recur across these files, so a model that learns from the words themselves can match them by content rather than by style.
- **Parts of longer works.** Only Band 1 of *Wilhelm Meisters Lehrjahre* and of *Wilhelm Meisters Wanderjahre* is included. *Der Heizer* is the first chapter of Kafka's unfinished novel *Der Verschollene*. The file of *Die Jungfrau von Orleans* begins with the first act; the prologue is missing.
- **Length.** The texts range from 3,422 words (*Ein Hungerkünstler*) to 79,119 words (*Die Wahlverwandtschaften*). Length-dependent measures such as the type-token ratio fall as texts get longer.

## Cleaning

When the texts were collected, their Project Gutenberg headers and licence texts were removed. A later check of all texts removed what was left, along with everything else that was not written by the author, so that the features only measure the author's style.

**Removed**

- remaining Project Gutenberg headers, licence text and notes
- title pages, tables of contents, publisher imprints and a dedication
- publishers' advertisements
- introductions, afterwords and notes by editors
- notes by transcribers, `[Illustration]` placeholders and music notation code
- emphasis markup of the transcriptions: `_text_`, `~text~`, `=text=`

**Kept on purpose:** the authors' own prefaces and footnotes. Achleitner signs some of his footnotes "D.V." (*der Verfasser*, the author), and *Die Räuber* contains one footnote by Schiller.

| File | Removed |
|---|---|
| `achleitner-Aus_Kroatien.txt` | byline; emphasis markup |
| `achleitner-Bergrichters_Erdenwallen.txt` | `[Illustration]` placeholder; LilyPond music code in footnote 11; emphasis markup |
| `achleitner-Celsissimus.txt` | transcriber's note; emphasis markup |
| `achleitner-Im_gruenen_Tann.txt` | emphasis markup |
| `achleitner-Unter_den_Hohen_Tauern.txt` | Project Gutenberg header and licence, title page, table of contents; publisher's advertisements at the end; emphasis markup |
| `anonymous-Der Luftpirat und sein lenkbares Luftschiff 40.txt` | cover page (price, picture caption, publisher); transcriber's notes |
| `anonymous-Der Luftpirat und sein lenkbares Luftschiff 42.txt` | legend of the picture on the back cover |
| `goethe-faust1.txt` | title and table of contents |
| `goethe-faust2.txt` | title and table of contents |
| `kafka-der_prozess.txt` | afterword by Max Brod |
| `kafka-landarzt.txt` | title page, publisher, copyright notice, table of contents, dedication |
| `schiller-Die Braut von Messina.txt` | note on the Gutenberg-DE source; two editor's notes and their markers |
| `schiller-Die Jungfrau von Orleans.txt` | author and title lines |
| `schiller-Die Verschwörung des Fiesco zu Genua.txt` | notes on the Gutenberg-DE source at the beginning and the end |
| `schiller-raeuber.txt` | title page of the 1805 edition with motto; publisher's advertisements; emphasis markup |
| `schiller-Wallensteins Lager.txt` | introduction by the editor (K. Goedeke); editor's note at the end; emphasis markup |

The other 20 texts needed no changes. Two more changes concern the corpus as a whole:

- The original study contained *Das Urteil* and *Die Verwandlung* twice, under different file names. A duplicate can end up in a training fold and a test fold at the same time, so only one copy of each is left.
- `kafka_der-heizer-ein-fragment.txt` was renamed to `kafka-der-heizer-ein-fragment.txt`, so that the author can be read from the file name.

**Note for text-based models:** footnote markers such as `[24]` only occur in Achleitner's texts. Remove or mask them before training on words or character n-grams, otherwise a model can recognise the author by the brackets.

## features.csv

One row per text with the 12 style features the models use. `scripts/evaluate.py` reads this file. The formulas are explained under [Features](../README.md#features) in the main README.

| Column | Meaning |
|---|---|
| `file` | file name without `.txt` |
| `author` | label: Achleitner, Anonymous, Goethe, Kafka or Schiller |
| `AverageWordLength` | characters per word |
| `AverageSentenceLength` | words per sentence |
| `AverageSyllables` | syllables per word |
| `WienerSachtextFormel` | first Wiener Sachtextformel |
| `FRE_Ger` | Flesch Reading Ease, German version by Amstad |
| `TTR` | type-token ratio |
| `Avg !`, `Avg ?`, `Avg .`, `Avg ,`, `Avg ;`, `Avg :` | punctuation marks per token |

## License

The texts in `corpus/` are in the public domain. All authors died more than 70 years ago (the last of them, Arthur Achleitner, in 1927), and the *Luftpirat* issues appeared anonymously between 1908 and 1911. The links in the tables above lead to the original Project Gutenberg ebooks.
