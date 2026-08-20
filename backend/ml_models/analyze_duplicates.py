import pandas as pd
from pathlib import Path

def main():
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "processed" / "news_clean.csv"

    df = pd.read_csv(dataset_path)

    # Find titles that occur more than once
    title_counts = df["title"].value_counts()

    duplicate_titles = title_counts[title_counts > 1]

    print("===== DUPLICATE TITLE ANALYSIS =====")
    print(f"Unique titles: {df['title'].nunique()}")
    print(f"Titles appearing more than once: {len(duplicate_titles)}")
    print(f"Rows belonging to duplicate-title groups: {duplicate_titles.sum()}")

    print("\n===== LABEL CONFLICTS =====")

    conflicts = []

    for title in duplicate_titles.index:
        labels = df.loc[df["title"] == title, "label"].unique()

        if len(labels) > 1:
            conflicts.append(title)

    print(f"Titles appearing with BOTH labels: {len(conflicts)}")

    if conflicts:
        print("\nExamples:")
        for title in conflicts[:10]:
            rows = df[df["title"] == title][
                ["title", "subject", "label"]
            ]

            print("\n", rows.to_string(index=False))

    print("\n===== MOST COMMON DUPLICATE TITLES =====")

    for title, count in duplicate_titles.head(10).items():
        labels = df.loc[df["title"] == title, "label"].value_counts()

        print(f"\nTitle: {title}")
        print(f"Occurrences: {count}")
        print(f"Labels: {labels.to_dict()}")

    df["word_count"] = df["text"].str.split().str.len()
    print("\n===== VERY SHORT ARTICLES =====")
    short_articles = df[df["word_count"] < 20].copy()

    print(f"Short articles: {len(short_articles)}")

    print("\nLabel distribution:")
    print(short_articles["label"].value_counts())

    print("\nExamples:")

    print(
        short_articles[
            ["title", "text", "label"]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()