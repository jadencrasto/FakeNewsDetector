import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit


def main():
    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "processed"
        / "news_ml_ready.csv"
    )

    output_dir = (
        project_root
        / "data"
        / "processed"
    )

    train_path = output_dir / "train.csv"
    test_path = output_dir / "test.csv"

    # ---------------------------------------------------------
    # Load dataset
    # ---------------------------------------------------------

    df = pd.read_csv(input_path)

    print("=" * 60)
    print("GROUP-AWARE TRAIN / TEST SPLIT")
    print("=" * 60)

    print(f"\nTotal articles: {len(df)}")
    print(f"Unique titles: {df['title'].nunique()}")

    # ---------------------------------------------------------
    # Group-aware split
    # ---------------------------------------------------------

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=42
    )

    train_indices, test_indices = next(
        splitter.split(
            df,
            y=df["label"],
            groups=df["title"]
        )
    )

    train_df = df.iloc[train_indices].copy()
    test_df = df.iloc[test_indices].copy()

    # ---------------------------------------------------------
    # Check title leakage
    # ---------------------------------------------------------

    train_titles = set(train_df["title"])
    test_titles = set(test_df["title"])

    overlapping_titles = train_titles.intersection(test_titles)

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print("\n===== SPLIT SIZE =====")

    print(f"Training articles: {len(train_df)}")
    print(f"Testing articles:  {len(test_df)}")

    print("\n===== SPLIT PROPORTIONS =====")

    print(
        f"Training: {len(train_df) / len(df) * 100:.2f}%"
    )

    print(
        f"Testing:  {len(test_df) / len(df) * 100:.2f}%"
    )

    print("\n===== CLASS DISTRIBUTION =====")

    print("\nTraining:")
    print(train_df["label"].value_counts())

    print("\nTesting:")
    print(test_df["label"].value_counts())

    print("\nTraining proportions:")
    print(
        train_df["label"]
        .value_counts(normalize=True)
        .round(4)
    )

    print("\nTesting proportions:")
    print(
        test_df["label"]
        .value_counts(normalize=True)
        .round(4)
    )

    print("\n===== TITLE LEAKAGE CHECK =====")

    print(
        f"Overlapping titles: {len(overlapping_titles)}"
    )

    if len(overlapping_titles) == 0:
        print("✓ No title leakage detected")
    else:
        print("⚠ WARNING: title leakage detected")

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print("\n===== FILES SAVED =====")
    print(f"Training: {train_path}")
    print(f"Testing:  {test_path}")


if __name__ == "__main__":
    main()