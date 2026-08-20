import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


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

    print("=" * 60)
    print("FAKE NEWS BASELINE MODEL")
    print("=" * 60)

    # ---------------------------------------------------------
    # Prepare text
    # ---------------------------------------------------------

    train_text = (
        train_df["title"].fillna("")
        + " "
        + train_df["text"].fillna("")
    )

    test_text = (
        test_df["title"].fillna("")
        + " "
        + test_df["text"].fillna("")
    )

    y_train = train_df["label"]
    y_test = test_df["label"]

    print(f"\nTraining documents: {len(train_text)}")
    print(f"Testing documents:  {len(test_text)}")

    # ---------------------------------------------------------
    # TF-IDF
    # ---------------------------------------------------------

    print("\nCreating TF-IDF representation...")

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

    # ---------------------------------------------------------
    # Logistic Regression
    # ---------------------------------------------------------

    print("\nTraining Logistic Regression...")

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train, y_train)

    print("Training complete.")

    # ---------------------------------------------------------
    # Predictions
    # ---------------------------------------------------------

    print("\nGenerating predictions...")

    predictions = model.predict(X_test)

    # ---------------------------------------------------------
    # Accuracy
    # ---------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\n" + "=" * 60)
    print("BASELINE RESULTS")
    print("=" * 60)

    print(
        f"\nAccuracy: {accuracy:.4f}"
        f" ({accuracy * 100:.2f}%)"
    )

    # ---------------------------------------------------------
    # Classification report
    # ---------------------------------------------------------

    print("\n===== CLASSIFICATION REPORT =====")

    print(
        classification_report(
            y_test,
            predictions,
            target_names=["FAKE", "REAL"],
            digits=4
        )
    )

    # ---------------------------------------------------------
    # Confusion matrix
    # ---------------------------------------------------------

    print("===== CONFUSION MATRIX =====")

    cm = confusion_matrix(
        y_test,
        predictions
    )

    print(cm)

    print("\nMatrix format:")
    print("[[True Fake,  Fake classified as Real]")
    print(" [Real classified as Fake, True Real]]")


if __name__ == "__main__":
    main()