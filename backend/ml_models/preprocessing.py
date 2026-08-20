import pandas as pd
from pathlib import Path
def load_dataset(fake_path, true_path):
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    fake_df["label"] = 0
    true_df["label"] = 1

    df = pd.concat([fake_df, true_df], ignore_index=True)
    return df

def clean_dataset(df):
    df = df.copy()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Normalize text columns
    for column in ["title", "text", "subject", "date"]:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()

    # Remove exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)

    # Remove rows where title or text is empty
    before = len(df)

    df = df[
        (df["title"].str.strip() != "") &
        (df["text"].str.strip() != "")
    ]

    empty_removed = before - len(df)

    # Combine title and article text
    df["combined_text"] = (
        df["title"] + " " + df["text"]
    )

    return df, duplicates_removed, empty_removed

def remove_non_article_records(df):
    df = df.copy()

    # Calculate approximate word count
    word_count = df["text"].str.split().str.len()

    # Remove records with fewer than 20 words.
    # These records in this dataset are predominantly
    # URL-only, video, social-media, or scraped fragments.
    mask = word_count >= 20

    removed = (~mask).sum()

    df = df[mask].copy()

    return df, removed

def main():
    project_root = Path(__file__).resolve().parents[2]

    fake_path = project_root / "data" / "Fake.csv"
    true_path = project_root / "data" / "True.csv"

    output_dir = project_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "news_ml_ready.csv"

    df = load_dataset(fake_path, true_path)

    print(f"Rows before cleaning: {len(df)}")

    df, duplicates_removed, empty_removed = clean_dataset(df)

    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Empty rows removed: {empty_removed}")

    df, non_article_removed = remove_non_article_records(df)

    print(f"Non-article records removed: {non_article_removed}")
    print(f"Rows after cleaning: {len(df)}")

    print("\nClass distribution:")
    print(df["label"].value_counts())

    df.to_csv(output_path, index=False)

    print(f"\nML-ready dataset saved to: {output_path}")

if __name__ == "__main__":
    main()