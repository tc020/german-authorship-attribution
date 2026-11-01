# Authorship attribution for German literature

In this university project from 2025 I taught myself the basics of NLP and machine learning, from the first chapters of the NLTK book to cross-validated classifiers, and later re-evaluated my own results more rigorously.

![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154F5B)
![License: MIT](https://img.shields.io/badge/License-MIT-blue)

## At a glance

- **Task:** assign 36 public-domain texts to five authors (Goethe, Schiller, Kafka, Arthur Achleitner and an anonymous pulp series) using only *how* they are written, not *what* they are about.
- **Features:** 12 stylometric measures per text, including two German readability indices I implemented from scratch.
- **Models:** Decision Tree, Random Forest, linear SVM and a majority-vote ensemble (scikit-learn).
- **Result:** the Random Forest reaches **89% accuracy** in repeated stratified cross-validation, against a 28% majority baseline (permutation test p = 0.005).
- **Most interesting finding:** the models partly learned *genre* instead of *author*. All three classify Goethe's *Faust I* as Schiller.

## Results

Repeated stratified 5-fold cross-validation (20 repeats) on 36 texts:

| Model | Accuracy (mean ± SD) | Macro-F1 |
|---|---|---|
| Majority baseline | 28% ± 1% | 0.09 |
| Decision Tree | 68% ± 16% | 0.66 |
| **Random Forest** | **89% ± 10%** | **0.87** |
| Linear SVM | 81% ± 12% | 0.79 |
| Linear SVM, 2 features (word + sentence length) | 56% ± 9% | 0.43 |
| Voting ensemble (DT + RF + SVM) | 84% ± 12% | 0.83 |

Permutation test (Random Forest): 92% accuracy with the real labels vs. 22% with shuffled labels, p = 0.005.

<p align="center">
    <img src="figures/confusion_matrix_rf_loo.png" width="520" alt="Confusion matrix of the Random Forest in leave-one-out validation: 32 of 36 texts correct. Errors: Faust I predicted as Schiller, Wilhelm Meisters Lehrjahre as Kafka, Die Verwandlung and Ein Hungerkünstler as Goethe.">
</p>

### Findings

**1. The models partly learn genre, not author.** Every Schiller text in this corpus is a drama, and dramas consist of short dialogue lines. All ten Schiller plays and *Faust I* average fewer than 10 words per sentence, while no prose text averages fewer than 12.7. As a result, the Decision Tree, the Random Forest and the SVM all classify Goethe's *Faust I* as Schiller in leave-one-out validation. *Faust II*, at 13.6 words per sentence, falls among the shortest prose texts, and none of the models takes it for Schiller.

![Average sentence length per text by author: the Schiller plays and Faust I are below 10 words per sentence, all prose texts above 12; Faust II lies among the shortest prose texts](figures/sentence_length_by_genre.png)

**2. Goethe vs. Kafka is the hard case.** Three of the Random Forest's four leave-one-out errors are Goethe ↔ Kafka confusions. Besides *Faust I*, two texts are misclassified by all three models: *Wilhelm Meisters Lehrjahre* as Kafka and *Ein Hungerkünstler* as Goethe. In their prose, both authors average about 22 words per sentence, against about 15 for Achleitner and the *Luftpirat* series, and both use more commas. These surface features cannot tell them apart.

**3. The ensemble does not help.** On a single 8-text test split, the majority vote fixed every individual model's error (8 of 8 correct). Under repeated cross-validation it reaches 84%, slightly below the Random Forest alone (89%), probably because the two weaker models can outvote it.

## How it works

```mermaid
flowchart LR
    A["36 texts<br/>Project Gutenberg"] --> B["Cleaning<br/>headers removed"]
    B --> C["12 style features<br/>per text"]
    C --> D["Decision Tree<br/>Random Forest<br/>Linear SVM"]
    D --> E["Majority vote"]
    D -.-> F["Evaluation<br/>repeated stratified CV,<br/>baseline, permutation test"]
    E -.-> F
```

### Corpus

| Author | Lived | Texts | What |
|---|---|---|---|
| Johann Wolfgang von Goethe | 1749–1832 | 7 | *Werther* (2 parts), *Die Wahlverwandtschaften*, *Wilhelm Meisters Lehrjahre* and *Wanderjahre* (vol. 1 each), *Faust I* and *II* |
| Friedrich Schiller | 1759–1805 | 10 | dramas only (*Die Räuber*, *Kabale und Liebe*, *Wallenstein*, …) |
| Arthur Achleitner | 1858–1927 | 5 | regional novels and stories |
| Franz Kafka | 1883–1924 | 8 | stories, novellas, *Der Process* |
| Anonymous | – | 6 | issues of the pulp series *Der Luftpirat und sein lenkbares Luftschiff* (1908–1911) |

Goethe and Schiller were included on purpose: they were close friends and influenced each other's writing.

### Features

| Group | Feature | Definition |
|---|---|---|
| Surface | Average word length | characters per word |
| | Average sentence length | words per sentence (NLTK sentence tokenizer) |
| | Syllables per word | Pyphen hyphenation dictionary (`de_DE`) |
| | Punctuation rates | `!` `?` `.` `,` `;` `:` per token (6 features) |
| Lexical | Type-token ratio | distinct tokens / all tokens |
| Readability | Flesch Reading Ease, German (Amstad) | 180 − ASL − 58.5 × ASW |
| | Wiener Sachtextformel (1st) | 0.1935 × MS + 0.1672 × SL + 0.1297 × IW − 0.0327 × ES − 0.875 |

ASL/SL: words per sentence · ASW: syllables per word · MS: % of words with three or more syllables · IW: % of words with more than six letters · ES: % of one-syllable words.

Content words were left out on purpose. The anonymous series mentions *Luft* constantly, and a model that learns topics would not generalise to other texts.

## Run it yourself

```bash
git clone https://github.com/tc020/german-authorship-attribution.git
cd german-authorship-attribution
python -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m nltk.downloader punkt_tab
python -m spacy download de_core_news_sm   # only for the exploration notebook
python -m nltk.downloader book             # only for the exercises in learning/
python -m spacy download en_core_web_sm    # only for the exercises in learning/

python scripts/evaluate.py             # results table and figures, about 2 minutes
jupyter lab                            # notebooks
```

## Repository structure

```
├── data/                  # sources and cleaning: data/README.md
│   ├── corpus/            # 36 cleaned texts
│   ├── raw/               # texts before cleaning
│   └── features.csv       # 36 × 12 feature table
├── notebooks/             # feature exploration, one notebook per model, ensemble
├── scripts/evaluate.py    # cross-validation, baseline, permutation test, figures
├── figures/
├── learning/              # how I got here: NLTK book exercises, playground, notes
└── requirements.txt
```

## Limitations and next steps

- **Small data.** 36 texts by five authors; results vary by about ±11 points between folds.
- **Chunks instead of whole books.** Splitting texts into segments of about 2,000 words, cross-validated by work, would give hundreds of samples. It would also answer the question that started this project: how short can a text be and still be attributed?
- **Classic stylometry features.** Function-word frequencies (Burrows' Delta) and character n-grams.
- **Genre balance.** Adding Schiller's prose (*Der Geisterseher*) and more Goethe dramas (*Egmont*, *Iphigenie auf Tauris*) would separate author from genre.
- **Vocabulary richness that doesn't depend on length**, such as MATTR instead of the type-token ratio.
- **A real open question.** The authorship of the *Luftpirat* series is disputed; one attribution names Oskar Hoffmann. That would be a fitting follow-up.

## Ethics

Stylometry is dual-use. The methods that attribute historical texts can also de-anonymise whistleblowers, activists or pseudonymous authors. Countermeasures (adversarial stylometry) exist and can be abused in turn, for example to imitate someone else's style. This project only uses public-domain literature.

## Data and license

The texts are in the public domain and come from [Project Gutenberg](https://www.gutenberg.org). The Gutenberg headers and license text were removed before the analysis; [data/README.md](data/README.md) lists the source, cleaning steps and word count of every text. The code is released under the [MIT License](LICENSE).

## Author

**Timucin Cicek** · [GitHub](https://github.com/tc020)
<!-- optional: LinkedIn / e-mail -->
