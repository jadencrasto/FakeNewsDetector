import pandas as pd
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


def remove_artifacts(text):
    """
    Replace obvious source/style artifacts with neutral tokens.
    """

    text = str(text)

    # URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " URL ",
        text,
        flags=re.IGNORECASE
    )

    # Reuters
    text = re.sub(
        r"\breuters\b",
        " SOURCE ",
        text,
        flags=re.IGNORECASE
    )

    # YouTube
    text = re.sub(
        r"\byoutube\b",
        " VIDEO_PLATFORM ",
        text,
        flags=re.IGNORECASE
    )

    # Twitter
    text = re.sub(
        r"\btwitter\b",
        " SOCIAL_MEDIA ",
        text,
        flags=re.IGNORECASE
    )

    # Facebook
    text = re.sub(
        r"\bfacebook\b",
        " SOCIAL_MEDIA ",
        text,
        flags=re.IGNORECASE
    )

    # Video
    text = re.sub(
        r"\bvideo\b",
        " MEDIA ",
        text,
        flags=re.IGNORECASE
    )

    return text


def train_and_evaluate(
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

    X_train = vectorizer.fit_transform(train_text)
    X_test = vectorizer.transform(test_text)

    print(f"Training matrix: {X_train.shape}")
    print(f"Testing matrix:  {X_test.shape}")

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

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

    print(f"F1 Score: {f1:.4f}")

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

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    y_train = train_df["label"]
    y_test = test_df["label"]

    # ---------------------------------------------------------
    # Original body
    # ---------------------------------------------------------

    original_train = train_df["text"].fillna("")
    original_test = test_df["text"].fillna("")

    original_accuracy, original_f1 = train_and_evaluate(
        original_train,
        original_test,
        y_train,
        y_test,
        "ORIGINAL BODY"
    )

    # ---------------------------------------------------------
    # Artifact-reduced body
    # ---------------------------------------------------------

    cleaned_train = (
        train_df["text"]
        .fillna("")
        .apply(remove_artifacts)
    )

    cleaned_test = (
        test_df["text"]
        .fillna("")
        .apply(remove_artifacts)
    )

    cleaned_accuracy, cleaned_f1 = train_and_evaluate(
        cleaned_train,
        cleaned_test,
        y_train,
        y_test,
        "ARTIFACT-REDUCED BODY"
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("ARTIFACT ABLATION SUMMARY")
    print("=" * 60)

    print(
        f"\nOriginal body accuracy: "
        f"{original_accuracy:.4f}"
    )

    print(
        f"Cleaned body accuracy:  "
        f"{cleaned_accuracy:.4f}"
    )

    print(
        f"\nAccuracy difference: "
        f"{original_accuracy - cleaned_accuracy:.4f}"
    )

    print(
        f"\nOriginal body F1: "
        f"{original_f1:.4f}"
    )

    print(
        f"Cleaned body F1:  "
        f"{cleaned_f1:.4f}"
    )


if __name__ == "__main__":
    main()