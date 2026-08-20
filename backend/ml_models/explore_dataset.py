import pandas as pd
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "processed" / "news_clean.csv"

    df = pd.read_csv(dataset_path)

    # Calculate text lengths
    df["title_length"] = df["title"].str.len()
    df["text_length"] = df["text"].str.len()
    df["word_count"] = df["text"].str.split().str.len()

    print("===== DATASET OVERVIEW =====")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    print("\n===== CLASS DISTRIBUTION =====")
    print(df["label"].value_counts())
    print(df["label"].value_counts(normalize=True))

    print("\n===== TITLE LENGTH =====")
    print(df.groupby("label")["title_length"].describe())

    print("\n===== TEXT LENGTH =====")
    print(df.groupby("label")["text_length"].describe())

    print("\n===== WORD COUNT =====")
    print(df.groupby("label")["word_count"].describe())

    print("\n===== DUPLICATE TITLES =====")
    duplicate_titles = df["title"].duplicated().sum()
    print(f"Duplicate title rows: {duplicate_titles}")

    print("\n===== VERY SHORT ARTICLES =====")
    short_articles = (df["word_count"] < 20).sum()
    print(f"Articles with fewer than 20 words: {short_articles}")

    print("\n===== VERY SHORT TITLES =====")
    short_titles = (df["title_length"] < 10).sum()
    print(f"Titles shorter than 10 characters: {short_titles}")


if __name__ == "__main__":
    main()