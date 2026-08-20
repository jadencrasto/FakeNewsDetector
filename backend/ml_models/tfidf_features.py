import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    project_root = Path(__file__).resolve().parents[2]

    train_path = project_root / "data" / "processed" / "train.csv"
    test_path = project_root / "data" / "processed" / "test.csv"

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print("=" * 60)
    print("TF-IDF FEATURE EXTRACTION")
    print("=" * 60)

    # ---------------------------------------------------------
    # Combine title + text
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

    print(f"\nTraining documents: {len(train_text)}")
    print(f"Testing documents:  {len(test_text)}")

    # ---------------------------------------------------------
    # Create vectorizer
    # ---------------------------------------------------------

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_features=100000,
        sublinear_tf=True
    )

    # ---------------------------------------------------------
    # FIT ONLY ON TRAINING DATA
    # ---------------------------------------------------------

    print("\nFitting TF-IDF on training data...")

    X_train = vectorizer.fit_transform(train_text)

    print("Transforming test data...")

    X_test = vectorizer.transform(test_text)

    # ---------------------------------------------------------
    # Results
    # ---------------------------------------------------------

    print("\n===== TF-IDF RESULTS =====")

    print(f"Training matrix shape: {X_train.shape}")
    print(f"Testing matrix shape:  {X_test.shape}")

    print(
        f"\nVocabulary size: "
        f"{len(vectorizer.vocabulary_)}"
    )

    print(
        f"Non-zero training values: "
        f"{X_train.nnz:,}"
    )

    print(
        f"Non-zero testing values: "
        f"{X_test.nnz:,}"
    )

    # ---------------------------------------------------------
    # Show sample vocabulary
    # ---------------------------------------------------------

    feature_names = vectorizer.get_feature_names_out()

    print("\n===== SAMPLE FEATURES =====")

    for feature in feature_names[:50]:
        print(feature)


if __name__ == "__main__":
    main()