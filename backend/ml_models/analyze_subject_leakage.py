import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def main():

    project_root = Path(__file__).resolve().parents[2]

    train_path = project_root / "data" / "processed" / "train.csv"
    test_path = project_root / "data" / "processed" / "test.csv"

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print("=" * 60)
    print("SUBJECT / SOURCE STRUCTURE INVESTIGATION")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Subject distribution
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("1. SUBJECT DISTRIBUTION")
    print("=" * 60)

    subject_distribution = pd.crosstab(
        train_df["subject"],
        train_df["label"]
    )

    subject_distribution.columns = ["FAKE", "REAL"]

    print(subject_distribution)

    # ---------------------------------------------------------
    # 2. Label purity by subject
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("2. SUBJECT LABEL PURITY")
    print("=" * 60)

    subject_purity = (
        train_df.groupby("subject")["label"]
        .agg(["count", "mean"])
    )

    subject_purity["real_percentage"] = (
        subject_purity["mean"] * 100
    )

    subject_purity["fake_percentage"] = (
        100 - subject_purity["real_percentage"]
    )

    print(
        subject_purity[
            [
                "count",
                "fake_percentage",
                "real_percentage"
            ]
        ].round(2)
    )

    # ---------------------------------------------------------
    # 3. Perfectly label-pure subjects
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("3. SUBJECTS WITH ONLY ONE LABEL")
    print("=" * 60)

    for subject, group in train_df.groupby("subject"):

        labels = group["label"].unique()

        if len(labels) == 1:

            label_name = (
                "FAKE"
                if labels[0] == 0
                else "REAL"
            )

            print(
                f"{subject}: "
                f"{len(group)} articles → {label_name}"
            )

    # ---------------------------------------------------------
    # 4. Subject-only classifier
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("4. SUBJECT-ONLY CLASSIFIER")
    print("=" * 60)

    # Learn the majority label for each subject
    subject_majority = (
        train_df.groupby("subject")["label"]
        .agg(lambda x: x.mode()[0])
    )

    predictions = test_df["subject"].map(
        subject_majority
    )

    # Handle unseen subjects
    global_majority = train_df["label"].mode()[0]

    predictions = predictions.fillna(
        global_majority
    )

    accuracy = accuracy_score(
        test_df["label"],
        predictions
    )

    print(
        f"Subject-only accuracy: "
        f"{accuracy:.4f} "
        f"({accuracy * 100:.2f}%)"
    )

    # ---------------------------------------------------------
    # 5. Can article text predict subject?
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("5. TEXT → SUBJECT PREDICTION")
    print("=" * 60)

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

    subject_model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    subject_model.fit(
        X_train,
        train_df["subject"]
    )

    subject_predictions = subject_model.predict(
        X_test
    )

    subject_accuracy = accuracy_score(
        test_df["subject"],
        subject_predictions
    )

    print(
        f"Text → subject accuracy: "
        f"{subject_accuracy:.4f} "
        f"({subject_accuracy * 100:.2f}%)"
    )

    print("\nClassification report:")

    print(
        classification_report(
            test_df["subject"],
            subject_predictions
        )
    )

    # ---------------------------------------------------------
    # 6. Subject overlap between train and test
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("6. SUBJECT OVERLAP")
    print("=" * 60)

    train_subjects = set(
        train_df["subject"].dropna().unique()
    )

    test_subjects = set(
        test_df["subject"].dropna().unique()
    )

    overlap = train_subjects.intersection(
        test_subjects
    )

    print(
        f"Training subjects: {len(train_subjects)}"
    )

    print(
        f"Testing subjects:  {len(test_subjects)}"
    )

    print(
        f"Overlapping subjects: {len(overlap)}"
    )

    print("\nShared subjects:")

    for subject in sorted(overlap):
        print(f"  - {subject}")

    print("\n" + "=" * 60)
    print("INVESTIGATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()