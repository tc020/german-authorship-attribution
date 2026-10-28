"""Re-evaluate the stylometric classifiers on the exported feature table.

Usage
-----
    python scripts/evaluate.py                       # defaults below
    python scripts/evaluate.py --features data/features.csv --figures figures

Input: a CSV with one row per text -> columns `file`, `author` and the 12 features.

What it does
------------
1. Repeated stratified 5-fold cross-validation (20 repeats) for every model,
   compared against a majority-class baseline.
2. A permutation test: is the Random Forest better than chance?
3. Leave-one-out predictions of the Random Forest -> confusion matrix + list of errors.
4. A dot plot of average sentence length per text (drama vs. prose).
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # render to files, no window needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import confusion_matrix, f1_score, make_scorer
from sklearn.model_selection import (LeaveOneOut, RepeatedStratifiedKFold,
                                     StratifiedKFold, cross_val_predict,
                                     cross_validate, permutation_test_score)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parents[1]
SEED = 42
FEATURES = [
    "AverageWordLength", "AverageSentenceLength", "AverageSyllables",
    "WienerSachtextFormel", "FRE_Ger", "TTR",
    "Avg !", "Avg ?", "Avg .", "Avg ,", "Avg ;", "Avg :",
]
# In this corpus every Schiller text is a drama; Goethe's two Faust parts are
# the only other dramas. Everything else is prose.
OTHER_DRAMAS = ("goethe-faust1", "goethe-faust2")

# Chart styling: light surface, quiet axes, two validated series colours.
SURFACE, INK, INK_2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
PROSE_COLOR, DRAMA_COLOR = "#2a78d6", "#eb6834"
BLUES = ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def build_models():
    svm = make_pipeline(StandardScaler(), SVC(kernel="linear", C=1))
    return {
        "Majority baseline": (DummyClassifier(strategy="most_frequent"), FEATURES),
        "Decision Tree": (DecisionTreeClassifier(random_state=SEED), FEATURES),
        "Random Forest": (RandomForestClassifier(n_estimators=300, random_state=SEED), FEATURES),
        "Linear SVM": (svm, FEATURES),
        "Linear SVM, 2 features (word + sentence length)": (svm, FEATURES[:2]),
        # Hard majority vote; the SVM's weight of 1.5 only matters when all three
        # models disagree -> then the SVM decides (same rule as the original ensemble).
        "Voting ensemble (DT + RF + SVM)": (VotingClassifier(
            [("dt", DecisionTreeClassifier(random_state=SEED)),
             ("rf", RandomForestClassifier(n_estimators=300, random_state=SEED)),
             ("svm", svm)],
            voting="hard", weights=[1, 1, 1.5]), FEATURES),
    }


def cross_validated_scores(df):
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=SEED)
    scoring = {"accuracy": "accuracy",
               "f1_macro": make_scorer(f1_score, average="macro", zero_division=0)}
    rows = []
    for name, (model, cols) in build_models().items():
        s = cross_validate(model, df[cols], df["author"], cv=cv, scoring=scoring, n_jobs=-1)
        rows.append([name,
                     f"{s['test_accuracy'].mean():.0%} ± {s['test_accuracy'].std():.0%}",
                     f"{s['test_f1_macro'].mean():.2f}"])
    return markdown_table(["Model", "Accuracy", "Macro-F1"], rows)


def markdown_table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


def style_axes(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=INK_2, labelcolor=INK_2)


def plot_confusion(y_true, y_pred, labels, path):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(6.4, 5.4), facecolor=SURFACE)
    cmap = LinearSegmentedColormap.from_list("blues", BLUES)
    # 2px surface-coloured gaps between the cells instead of borders
    ax.pcolormesh(cm, cmap=cmap, vmin=0, vmax=cm.max(), edgecolors=SURFACE, linewidth=2)
    for i in range(len(labels)):
        for j in range(len(labels)):
            v = cm[i, j]
            colour = MUTED if v == 0 else ("#ffffff" if v > cm.max() * 0.45 else INK)
            ax.text(j + 0.5, i + 0.5, v, ha="center", va="center", color=colour, fontsize=12)
    ax.set_xticks(np.arange(len(labels)) + 0.5, labels)
    ax.set_yticks(np.arange(len(labels)) + 0.5, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Predicted author", color=INK_2)
    ax.set_ylabel("True author", color=INK_2)
    style_axes(ax)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    correct = int(np.trace(cm))
    ax.set_title(f"Random Forest, leave-one-out: {correct} of {cm.sum()} texts correct",
                 color=INK, loc="left", fontsize=12, pad=12)
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def plot_sentence_length(df, path):
    df = df.assign(genre=np.where(df["author"].eq("Schiller") | df["file"].isin(OTHER_DRAMAS),
                                  "drama", "prose"))
    asl = df["AverageSentenceLength"]
    order = df.groupby("author")["AverageSentenceLength"].median().sort_values().index.tolist()
    ypos = {a: i for i, a in enumerate(order)}
    # small vertical offsets so texts with (almost) the same value don't hide each other
    rank = df.groupby("author")["AverageSentenceLength"].rank(method="first").astype(int)
    jitter = np.array([-0.2, 0.0, 0.2])[rank.to_numpy() % 3]

    fig, ax = plt.subplots(figsize=(8, 4.2), facecolor=SURFACE)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for genre, colour, marker, size in (("prose", PROSE_COLOR, "o", 70), ("drama", DRAMA_COLOR, "^", 95)):
        m = df["genre"].eq(genre)
        ax.scatter(asl[m], df.loc[m, "author"].map(ypos) + jitter[m.to_numpy()],
                   s=size, color=colour, marker=marker, edgecolors=SURFACE, linewidths=1.5, zorder=3)

    max_drama = asl[df["genre"].eq("drama")].max()
    min_prose = asl[df["genre"].eq("prose")].min()
    if max_drama < min_prose:  # only draw the split if it really is clean
        cut = (max_drama + min_prose) / 2
        ax.axvline(cut, color=INK_2, linewidth=1, zorder=2)
        ax.text(cut + 0.4, len(order) - 0.55, f"{cut:.0f} words", color=INK_2, fontsize=9)
        title = "Every drama has shorter sentences than every prose text"
    else:
        title = "Average sentence length per text: drama vs. prose"

    for f, label in zip(OTHER_DRAMAS, ("Faust I", "Faust II")):  # label the story points only
        row = df.index[df["file"].eq(f)]
        if len(row):
            r = row[0]
            ax.annotate(label, (asl[r], ypos[df.at[r, "author"]] + jitter[df.index.get_loc(r)]),
                        xytext=(8, 6), textcoords="offset points", color=INK_2, fontsize=9)

    ax.set_yticks(range(len(order)), order)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlabel("Average sentence length (words per sentence)", color=INK_2)
    style_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    handles = [Line2D([], [], marker="o", linestyle="", color=PROSE_COLOR, markersize=8, label="prose"),
               Line2D([], [], marker="^", linestyle="", color=DRAMA_COLOR, markersize=8, label="drama")]
    ax.legend(handles=handles, frameon=False, loc="lower right", labelcolor=INK_2)
    ax.set_title(title, color=INK, loc="left", fontsize=12, pad=12)
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--features", type=Path, default=ROOT / "data" / "features.csv")
    parser.add_argument("--figures", type=Path, default=ROOT / "figures")
    args = parser.parse_args()
    args.figures.mkdir(parents=True, exist_ok=True)

    # Sort by file name so the result does not depend on the operating system's file order.
    df = (pd.read_csv(args.features)
            .rename(columns={"Author": "author"})
            .sort_values("file", ignore_index=True))
    X, y = df[FEATURES], df["author"]
    print(f"{len(df)} texts, {y.nunique()} authors: {y.value_counts().to_dict()}\n")

    print("Repeated stratified 5-fold CV (20 repeats), mean ± SD over folds:\n")
    print(cross_validated_scores(df), "\n")

    score, perm_scores, p = permutation_test_score(
        RandomForestClassifier(n_estimators=100, random_state=SEED), X, y,
        cv=StratifiedKFold(5, shuffle=True, random_state=SEED),
        n_permutations=200, random_state=SEED, n_jobs=-1)
    print(f"Permutation test (Random Forest): accuracy {score:.0%} vs. "
          f"{perm_scores.mean():.0%} with shuffled labels, p = {p:.3f}\n")

    print("Leave-one-out errors:")
    models = build_models()
    loo_pred = {}
    for name in ("Decision Tree", "Random Forest", "Linear SVM"):
        model, cols = models[name]
        pred = cross_val_predict(model, df[cols], y, cv=LeaveOneOut(), n_jobs=-1)
        loo_pred[name] = pred
        print(f"  {name}: {(pred == y).sum()} of {len(y)} correct")
        for f, t, p_ in zip(df["file"], y, pred):
            if t != p_:
                print(f"    {f}: {t} -> predicted {p_}")

    plot_confusion(y, loo_pred["Random Forest"], sorted(y.unique()),
                   args.figures / "confusion_matrix_rf_loo.png")
    plot_sentence_length(df, args.figures / "sentence_length_by_genre.png")
    print(f"\nFigures written to {args.figures}")


if __name__ == "__main__":
    main()
