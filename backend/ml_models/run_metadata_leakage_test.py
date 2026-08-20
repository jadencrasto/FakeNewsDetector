import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


def evaluate(train_text, test_text, y_train, y_test, name):

    print("\n" + "=" * 60)
    print(name)
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

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    y_train = train_df["label"]
    y_test = test_df["label"]

    # ---------------------------------------------------------
    # 1. TEXT ONLY
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

    text_accuracy, text_f1 = evaluate(
        train_text,
        test_text,
        y_train,
        y_test,
        "EXPERIMENT 1 — TITLE + BODY"
    )

    # ---------------------------------------------------------
    # 2. SUBJECT ONLY
    # ---------------------------------------------------------

    train_subject = train_df["subject"].fillna("")
    test_subject = test_df["subject"].fillna("")

    subject_vectorizer = TfidfVectorizer()

    X_train_subject = subject_vectorizer.fit_transform(
        train_subject
    )

    X_test_subject = subject_vectorizer.transform(
        test_subject
    )

    subject_model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    subject_model.fit(
        X_train_subject,
        y_train
    )

    subject_predictions = subject_model.predict(
        X_test_subject
    )

    subject_accuracy = accuracy_score(
        y_test,
        subject_predictions
    )

    subject_f1 = f1_score(
        y_test,
        subject_predictions
    )

    print("\n" + "=" * 60)
    print("EXPERIMENT 2 — SUBJECT ONLY")
    print("=" * 60)

    print(
        f"Accuracy: {subject_accuracy:.4f} "
        f"({subject_accuracy * 100:.2f}%)"
    )

    print(
        f"F1 Score: {subject_f1:.4f}"
    )

    # ---------------------------------------------------------
    # 3. TEXT + SUBJECT
    # ---------------------------------------------------------

    train_combined = (
        train_df["title"].fillna("")
        + " "
        + train_df["text"].fillna("")
        + " SUBJECT_"
        + train_df["subject"].fillna("")
    )

    test_combined = (
        test_df["title"].fillna("")
        + " "
        + test_df["text"].fillna("")
        + " SUBJECT_"
        + test_df["subject"].fillna("")
    )

    combined_accuracy, combined_f1 = evaluate(
        train_combined,
        test_combined,
        y_train,
        y_test,
        "EXPERIMENT 3 — TITLE + BODY + SUBJECT"
    )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("METADATA LEAKAGE SUMMARY")
    print("=" * 60)

    print(
        f"\nText only:       "
        f"{text_accuracy:.4f}"
    )

    print(
        f"Subject only:    "
        f"{subject_accuracy:.4f}"
    )

    print(
        f"Text + subject:  "
        f"{combined_accuracy:.4f}"
    )

    print("\nF1 scores:")

    print(
        f"Text only:       "
        f"{text_f1:.4f}"
    )

    print(
        f"Subject only:    "
        f"{subject_f1:.4f}"
    )

    print(
        f"Text + subject:  "
        f"{combined_f1:.4f}"
    )


if __name__ == "__main__":
    main()