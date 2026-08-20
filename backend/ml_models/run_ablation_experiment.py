import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


def train_and_evaluate(train_text, test_text, y_train, y_test, experiment_name):

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

    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"F1 Score: {f1:.4f}")

    return accuracy, f1


def main():

    project_root = Path(__file__).resolve().parents[2]

    train_path = project_root / "data" / "processed" / "train.csv"
    test_path = project_root / "data" / "processed" / "test.csv"

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    y_train = train_df["label"]
    y_test = test_df["label"]

    results = []

    # ---------------------------------------------------------
    # Experiment 1: Full text
    # ---------------------------------------------------------

    accuracy, f1 = train_and_evaluate(
        train_df["title"].fillna("") + " " + train_df["text"].fillna(""),
        test_df["title"].fillna("") + " " + test_df["text"].fillna(""),
        y_train,
        y_test,
        "EXPERIMENT 1 — TITLE + BODY"
    )

    results.append(
        ["Title + Body", accuracy, f1]
    )

    # ---------------------------------------------------------
    # Experiment 2: Title only
    # ---------------------------------------------------------

    accuracy, f1 = train_and_evaluate(
        train_df["title"].fillna(""),
        test_df["title"].fillna(""),
        y_train,
        y_test,
        "EXPERIMENT 2 — TITLE ONLY"
    )

    results.append(
        ["Title Only", accuracy, f1]
    )

    # ---------------------------------------------------------
    # Experiment 3: Body only
    # ---------------------------------------------------------

    accuracy, f1 = train_and_evaluate(
        train_df["text"].fillna(""),
        test_df["text"].fillna(""),
        y_train,
        y_test,
        "EXPERIMENT 3 — BODY ONLY"
    )

    results.append(
        ["Body Only", accuracy, f1]
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    results_df = pd.DataFrame(
        results,
        columns=["Experiment", "Accuracy", "F1"]
    )

    print("\n" + "=" * 60)
    print("ABLATION EXPERIMENT SUMMARY")
    print("=" * 60)

    print(
        results_df.to_string(
            index=False,
            formatters={
                "Accuracy": "{:.4f}".format,
                "F1": "{:.4f}".format
            }
        )
    )


if __name__ == "__main__":
    main()