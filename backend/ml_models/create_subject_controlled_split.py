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

    output_path = (
        project_root
        / "data"
        / "processed"
        / "subject_controlled.csv"
    )

    df = pd.read_csv(input_path)

    print("=" * 60)
    print("SUBJECT-CONTROLLED DATASET")
    print("=" * 60)

    print(f"\nOriginal articles: {len(df)}")

    # ---------------------------------------------------------
    # Show subject counts
    # ---------------------------------------------------------

    print("\nOriginal subject distribution:")

    print(
        pd.crosstab(
            df["subject"],
            df["label"]
        )
    )

    # ---------------------------------------------------------
    # Find subjects for each label
    # ---------------------------------------------------------

    fake_subjects = (
        df[df["label"] == 0]["subject"]
        .value_counts()
    )

    real_subjects = (
        df[df["label"] == 1]["subject"]
        .value_counts()
    )

    print("\nFAKE subjects:")
    print(fake_subjects)

    print("\nREAL subjects:")
    print(real_subjects)

    # ---------------------------------------------------------
    # Create controlled sample
    #
    # We select an equal number of articles from each
    # available subject within each label.
    # ---------------------------------------------------------

    fake_subject_count = len(fake_subjects)
    real_subject_count = len(real_subjects)

    print(
        f"\nFake subject groups: {fake_subject_count}"
    )

    print(
        f"Real subject groups: {real_subject_count}"
    )

    # Use the two real subjects and select two fake subjects
    # with the largest populations.
    #
    # This creates matched numbers of subject groups.
    # This is a diagnostic experiment, not a replacement
    # for the original dataset.

    selected_fake_subjects = (
        fake_subjects
        .sort_values(ascending=False)
        .head(real_subject_count)
        .index
        .tolist()
    )

    selected_real_subjects = (
        real_subjects
        .sort_values(ascending=False)
        .head(real_subject_count)
        .index
        .tolist()
    )

    print("\nSelected FAKE subjects:")
    for subject in selected_fake_subjects:
        print(f"  - {subject}")

    print("\nSelected REAL subjects:")
    for subject in selected_real_subjects:
        print(f"  - {subject}")

    # ---------------------------------------------------------
    # Determine balanced sample size
    # ---------------------------------------------------------

    selected_groups = []

    for subject in (
        selected_fake_subjects
        + selected_real_subjects
    ):

        group = df[
            df["subject"] == subject
        ]

        selected_groups.append(
            group
        )

    smallest_group_size = min(
        len(group)
        for group in selected_groups
    )

    print(
        f"\nSmallest selected subject group: "
        f"{smallest_group_size}"
    )

    # ---------------------------------------------------------
    # Sample equal number from every selected subject
    # ---------------------------------------------------------

    samples = []

    for subject in (
        selected_fake_subjects
        + selected_real_subjects
    ):

        group = df[
            df["subject"] == subject
        ]

        sampled = group.sample(
            n=smallest_group_size,
            random_state=42
        )

        samples.append(
            sampled
        )

    controlled_df = pd.concat(
        samples,
        ignore_index=True
    )

    # Shuffle
    controlled_df = controlled_df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # Results
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("CONTROLLED DATASET RESULTS")
    print("=" * 60)

    print(
        f"\nTotal articles: "
        f"{len(controlled_df)}"
    )

    print("\nLabel distribution:")

    print(
        controlled_df["label"]
        .value_counts()
    )

    print("\nSubject distribution:")

    print(
        pd.crosstab(
            controlled_df["subject"],
            controlled_df["label"]
        )
    )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    controlled_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nSaved to:\n{output_path}"
    )


if __name__ == "__main__":
    main()