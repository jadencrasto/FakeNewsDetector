import pandas as pd
import re
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parents[2]
    dataset_path = project_root / "data" / "processed" / "news_ml_ready.csv"

    df = pd.read_csv(dataset_path)

    print("=" * 60)
    print("DATASET ARTIFACT INVESTIGATION")
    print("=" * 60)

    print(f"\nTotal articles: {len(df)}")

    # ---------------------------------------------------------
    # 1. SUBJECT DISTRIBUTION
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("1. SUBJECT DISTRIBUTION")
    print("=" * 60)

    subject_table = pd.crosstab(
        df["subject"],
        df["label"]
    )

    subject_table.columns = ["FAKE", "REAL"]

    print(subject_table)

    print("\nSubject distribution within each label:")

    for label, label_name in [(0, "FAKE"), (1, "REAL")]:
        print(f"\n{label_name}:")
        print(
            df[df["label"] == label]["subject"]
            .value_counts(normalize=True)
            .mul(100)
            .round(2)
        )

    # ---------------------------------------------------------
    # 2. REUTERS MARKER
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("2. REUTERS MARKER")
    print("=" * 60)

    text_lower = df["text"].fillna("").str.lower()

    df["has_reuters"] = text_lower.str.contains(
        r"\breuters\b",
        regex=True
    )

    reuters_table = pd.crosstab(
        df["has_reuters"],
        df["label"]
    )

    reuters_table.columns = ["FAKE", "REAL"]

    print(reuters_table)

    print("\nPercentage containing Reuters:")

    print(
        df.groupby("label")["has_reuters"]
        .mean()
        .mul(100)
        .round(2)
    )

    # ---------------------------------------------------------
    # 3. URL PRESENCE
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("3. URL PRESENCE")
    print("=" * 60)

    df["has_url"] = text_lower.str.contains(
        r"https?://|www\.",
        regex=True
    )

    url_table = pd.crosstab(
        df["has_url"],
        df["label"]
    )

    url_table.columns = ["FAKE", "REAL"]

    print(url_table)

    print("\nPercentage containing URLs:")

    print(
        df.groupby("label")["has_url"]
        .mean()
        .mul(100)
        .round(2)
    )

    # ---------------------------------------------------------
    # 4. SOCIAL MEDIA MARKERS
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("4. SOCIAL MEDIA MARKERS")
    print("=" * 60)

    markers = {
        "twitter": r"\btwitter\b|twitter\.com|pic\.twitter",
        "youtube": r"\byoutube\b|youtu\.be",
        "facebook": r"\bfacebook\b",
        "video": r"\bvideo\b",
    }

    for name, pattern in markers.items():

        df[f"has_{name}"] = text_lower.str.contains(
            pattern,
            regex=True
        )

        percentages = (
            df.groupby("label")[f"has_{name}"]
            .mean()
            .mul(100)
            .round(2)
        )

        print(f"\n{name.upper()}:")
        print(f"FAKE: {percentages.get(0, 0)}%")
        print(f"REAL: {percentages.get(1, 0)}%")

    # ---------------------------------------------------------
    # 5. COMMON PREFIXES
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("5. COMMON ARTICLE PREFIXES")
    print("=" * 60)

    prefixes = [
        "washington",
        "london",
        "new york",
        "moscow",
        "beijing",
        "berlin",
    ]

    for prefix in prefixes:

        mask = text_lower.str.startswith(prefix)

        if mask.sum() == 0:
            continue

        distribution = df.loc[mask, "label"].value_counts()

        print(f"\n'{prefix}':")
        print(distribution.to_dict())

    # ---------------------------------------------------------
    # 6. SUBJECT-ONLY BASELINE
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("6. SUBJECT-ONLY BASELINE")
    print("=" * 60)

    # For each subject, predict its majority class.
    subject_majority = (
        df.groupby("subject")["label"]
        .agg(lambda x: x.mode()[0])
    )

    predictions = df["subject"].map(subject_majority)

    accuracy = (predictions == df["label"]).mean()

    print(
        f"Accuracy using ONLY subject: "
        f"{accuracy:.4f} ({accuracy * 100:.2f}%)"
    )

    # ---------------------------------------------------------
    # 7. TOP WORDS IN TITLES
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("7. COMMON TITLE TERMS")
    print("=" * 60)

    for label, label_name in [(0, "FAKE"), (1, "REAL")]:

        titles = (
            df[df["label"] == label]["title"]
            .fillna("")
            .str.lower()
        )

        words = (
            titles
            .str.findall(r"\b[a-z]{4,}\b")
            .explode()
        )

        print(f"\nTop title terms — {label_name}:")
        print(words.value_counts().head(20))

    print("\n" + "=" * 60)
    print("INVESTIGATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()