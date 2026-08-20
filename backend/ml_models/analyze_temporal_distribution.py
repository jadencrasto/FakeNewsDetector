import pandas as pd
from pathlib import Path


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
    print("TEMPORAL DISTRIBUTION INVESTIGATION")
    print("=" * 60)

    # ---------------------------------------------------------
    # Parse dates
    # ---------------------------------------------------------

    df["parsed_date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    print("\nDate parsing:")

    print(
        f"Total rows: {len(df)}"
    )

    print(
        f"Valid dates: "
        f"{df['parsed_date'].notna().sum()}"
    )

    print(
        f"Invalid dates: "
        f"{df['parsed_date'].isna().sum()}"
    )

    # ---------------------------------------------------------
    # Date range
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("DATE RANGE")
    print("=" * 60)

    print(
        f"Earliest date: "
        f"{df['parsed_date'].min()}"
    )

    print(
        f"Latest date: "
        f"{df['parsed_date'].max()}"
    )

    # ---------------------------------------------------------
    # Year distribution
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("YEAR DISTRIBUTION")
    print("=" * 60)

    year_distribution = pd.crosstab(
        df["parsed_date"].dt.year,
        df["label"]
    )

    year_distribution.columns = [
        "FAKE",
        "REAL"
    ]

    print(year_distribution)

    # ---------------------------------------------------------
    # Month distribution
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("YEAR-MONTH DISTRIBUTION")
    print("=" * 60)

    df["year_month"] = (
        df["parsed_date"]
        .dt.to_period("M")
    )

    monthly = pd.crosstab(
        df["year_month"],
        df["label"]
    )

    monthly.columns = [
        "FAKE",
        "REAL"
    ]

    print(monthly)

    # ---------------------------------------------------------
    # Label distribution by year
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("LABEL PROPORTIONS BY YEAR")
    print("=" * 60)

    year_proportions = pd.crosstab(
        df["parsed_date"].dt.year,
        df["label"],
        normalize="index"
    ) * 100

    year_proportions.columns = [
        "FAKE %",
        "REAL %"
    ]

    print(
        year_proportions.round(2)
    )

    # ---------------------------------------------------------
    # Subject distribution by year
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("SUBJECT DISTRIBUTION BY YEAR")
    print("=" * 60)

    subject_year = pd.crosstab(
        df["parsed_date"].dt.year,
        df["subject"]
    )

    print(subject_year)

    print("\n" + "=" * 60)
    print("INVESTIGATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()