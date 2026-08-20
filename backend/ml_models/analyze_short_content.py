import pandas as pd
import re
from pathlib import Path

def looks_like_url_only(text):
    text = str(text).strip()

    # Remove whitespace
    normalized = re.sub(r"\s+", "", text)

    # Check if the entire content is basically a URL
    return bool(
        re.fullmatch(
            r"https?://\S+",
            normalized
        )
    )


def main():
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "processed" / "news_clean.csv"

    df = pd.read_csv(dataset_path)

    df["word_count"] = df["text"].str.split().str.len()

    short = df[df["word_count"] < 20].copy()

    short["url_only"] = short["text"].apply(looks_like_url_only)

    print("===== SHORT CONTENT ANALYSIS =====")
    print(f"Short records: {len(short)}")

    print("\nURL-only records:")
    print(short["url_only"].sum())

    print("\nShort records by label:")
    print(short["label"].value_counts())

    print("\n===== SHORT RECORDS =====")

    for _, row in short.head(30).iterrows():
        print("\n--------------------------------")
        print(f"Label: {row['label']}")
        print(f"Title: {row['title']}")
        print(f"Text: {row['text']}")


if __name__ == "__main__":
    main()