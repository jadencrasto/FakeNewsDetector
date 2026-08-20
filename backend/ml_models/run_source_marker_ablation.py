import pandas as pd
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


def remove_source_markers(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # Remove obvious source/style markers
    markers = [
        "reuters",
        "youtube",
        "youtu",
        "twitter",
        "facebook",
        "instagram",
        "soundcloud",
        "video",
        "watch",
        "read more",
        "featured image",
        "getty",
        "pic.twitter"
    ]

    for marker in markers:

        text = re.sub(
            re.escape(marker),
            " ",
            text,
            flags=re.IGNORECASE
        )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def evaluate_model(
    train_text,
    test_text,
    y_train,
    y_test,
    experiment_name
):

    print("\n" + "=" * 60)
    print(experiment_name)
    print("=" * 60)

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_features=100000,
        sublinear_tf=True
    )

    X_train = vectorizer.fit_transform(
        train_text
    )

    X_test = vectorizer.transform(
        test_text
    )

    print(
        f"Training matrix: {X_train.shape}"
    )

    print(
        f"Testing matrix:  {X_test.shape}"
    )

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions
    )

    print(
        f"Accuracy: {accuracy:.4f} "
        f"({accuracy * 100:.2f}%)"
    )

    print(
        f"F1 Score: {f1:.4f}"
    )

    return accuracy, f1


def main():

    project_root = Path(__file__).resolve().parents[2]

    train_path = (
        project_root
        / "data"
        / "processed"
        / "train.csv"
    )

    test_path = (
        project_root
        / "data"
        / "processed"
        / "test.csv"
    )

    train_df = pd.read_csv(
        train_path
    )

    test_df = pd.read_csv(
        test_path
    )

    y_train = train_df["label"]
    y_test = test_df["label"]

    # ---------------------------------------------------------
    # ORIGINAL BODY
    # ---------------------------------------------------------

    original_train = (
        train_df["title"].fillna("")
        + " "
        + train_df["text"].fillna("")
    )

    original_test = (
        test_df["title"].fillna("")
        + " "
        + test_df["text"].fillna("")
    )

    original_accuracy, original_f1 = evaluate_model(
        original_train,
        original_test,
        y_train,
        y_test,
        "EXPERIMENT 1 — ORIGINAL TITLE + BODY"
    )

    # ---------------------------------------------------------
    # SOURCE-CLEANED
    # ---------------------------------------------------------

    cleaned_train = original_train.apply(
        remove_source_markers
    )

    cleaned_test = original_test.apply(
        remove_source_markers
    )

    cleaned_accuracy, cleaned_f1 = evaluate_model(
        cleaned_train,
        cleaned_test,
        y_train,
        y_test,
        "EXPERIMENT 2 — SOURCE-MARKER REDUCED"
    )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("SOURCE-MARKER ABLATION SUMMARY")
    print("=" * 60)

    print(
        f"\nOriginal accuracy: "
        f"{original_accuracy:.4f}"
    )

    print(
        f"Cleaned accuracy:  "
        f"{cleaned_accuracy:.4f}"
    )

    print(
        f"Accuracy difference: "
        f"{original_accuracy - cleaned_accuracy:.4f}"
    )

    print(
        f"\nOriginal F1: "
        f"{original_f1:.4f}"
    )

    print(
        f"Cleaned F1:  "
        f"{cleaned_f1:.4f}"
    )

    print(
        f"F1 difference: "
        f"{original_f1 - cleaned_f1:.4f}"
    )

if __name__ == "__main__":
    main()