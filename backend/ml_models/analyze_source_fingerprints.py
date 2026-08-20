import pandas as pd
from pathlib import Path
from collections import Counter
import re


def main():

    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "processed"
        / "news_ml_ready.csv"
    )

    df = pd.read_csv(input_path)

    print("=" * 60)
    print("SOURCE FINGERPRINT INVESTIGATION")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Subject + label relationship
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("1. SUBJECT → LABEL MAPPING")
    print("=" * 60)

    mapping = (
        df.groupby("subject")["label"]
        .agg(["count", "mean"])
    )

    mapping["label_name"] = mapping["mean"].map({
        0: "FAKE",
        1: "REAL"
    })

    print(mapping)

    # ---------------------------------------------------------
    # 2. Date availability by subject
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("2. DATE AVAILABILITY BY SUBJECT")
    print("=" * 60)

    df["parsed_date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    date_stats = (
        df.groupby("subject")["parsed_date"]
        .agg(
            total="count",
            valid_dates=lambda x: x.notna().sum()
        )
    )

    date_stats["date_percentage"] = (
        date_stats["valid_dates"]
        / date_stats["total"]
        * 100
    )

    print(
        date_stats.round(2)
    )

    # ---------------------------------------------------------
    # 3. URL/domain fingerprints
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("3. URL / DOMAIN FINGERPRINTS")
    print("=" * 60)

    url_pattern = re.compile(
        r"https?://([^/\s]+)",
        re.IGNORECASE
    )

    domain_counts = {}

    for label, group in df.groupby("label"):

        domains = []

        for text in group["text"].fillna(""):

            matches = url_pattern.findall(text)

            for domain in matches:
                domains.append(
                    domain.lower()
                )

        counts = Counter(domains)

        domain_counts[label] = counts

        label_name = (
            "FAKE"
            if label == 0
            else "REAL"
        )

        print(
            f"\nTop domains — {label_name}:"
        )

        for domain, count in counts.most_common(20):

            print(
                f"{domain:<40} {count}"
            )

    # ---------------------------------------------------------
    # 4. Reuters distribution
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("4. REUTERS DISTRIBUTION")
    print("=" * 60)

    df["has_reuters"] = (
        df["text"]
        .fillna("")
        .str.contains(
            "reuters",
            case=False,
            regex=False
        )
    )

    print(
        pd.crosstab(
            df["subject"],
            df["has_reuters"]
        )
    )

    # ---------------------------------------------------------
    # 5. Common text markers by subject
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("5. SOURCE / STYLE MARKERS")
    print("=" * 60)

    markers = [
        "reuters",
        "http",
        "https",
        "youtube",
        "twitter",
        "facebook",
        "video",
        "watch",
        "read more",
        "featured image",
        "getty",
        "pic.twitter"
    ]

    for subject, group in df.groupby("subject"):

        print(
            f"\n--- {subject} ---"
        )

        total = len(group)

        for marker in markers:

            matches = (
                group["text"]
                .fillna("")
                .str.contains(
                    marker,
                    case=False,
                    regex=False
                )
                .sum()
            )

            percentage = (
                matches / total * 100
            )

            if percentage >= 1:

                print(
                    f"{marker:<20} "
                    f"{percentage:6.2f}%"
                )

    # ---------------------------------------------------------
    # 6. Subject × year
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("6. SUBJECT × YEAR")
    print("=" * 60)

    subject_year = pd.crosstab(
        df["parsed_date"].dt.year,
        df["subject"]
    )

    print(subject_year)

    # ---------------------------------------------------------
    # 7. Summary
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("SOURCE FINGERPRINT INVESTIGATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()