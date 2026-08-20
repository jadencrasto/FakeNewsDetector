import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def main():

    project_root = Path(__file__).resolve().parents[2]

    train_path = (
        project_root
        / "data"
        / "processed"
        / "train.csv"
    )

    train_df = pd.read_csv(train_path)

    print("=" * 60)
    print("MODEL FEATURE ANALYSIS")
    print("=" * 60)

    # ---------------------------------------------------------
    # Prepare training text
    # ---------------------------------------------------------

    train_text = (
        train_df["title"].fillna("")
        + " "
        + train_df["text"].fillna("")
    )

    y_train = train_df["label"]

    # ---------------------------------------------------------
    # TF-IDF
    # ---------------------------------------------------------

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2,
        max_features=100000,
        sublinear_tf=True
    )

    X_train = vectorizer.fit_transform(train_text)

    # ---------------------------------------------------------
    # Train same baseline model
    # ---------------------------------------------------------

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train, y_train)

    # ---------------------------------------------------------
    # Feature names and coefficients
    # ---------------------------------------------------------

    feature_names = vectorizer.get_feature_names_out()

    coefficients = model.coef_[0]

    feature_data = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefficients
    })

    # ---------------------------------------------------------
    # Strongest FAKE indicators
    # ---------------------------------------------------------

    fake_features = (
        feature_data
        .sort_values("coefficient", ascending=False)
        .head(30)
    )

    # ---------------------------------------------------------
    # Strongest REAL indicators
    # ---------------------------------------------------------

    real_features = (
        feature_data
        .sort_values("coefficient", ascending=True)
        .head(30)
    )

    print("\n" + "=" * 60)
    print("TOP REAL-ASSOCIATED FEATURES")
    print("=" * 60)

    print(fake_features.to_string(index=False))

    print("\n" + "=" * 60)
    print("TOP FAKE-ASSOCIATED FEATURES")
    print("=" * 60)

    print(real_features.to_string(index=False))

    # ---------------------------------------------------------
    # Specific artifact checks
    # ---------------------------------------------------------

    interesting_terms = [
        "reuters",
        "video",
        "youtube",
        "twitter",
        "facebook",
        "breaking",
        "washington",
        "according",
        "president",
        "trump"
    ]

    print("\n" + "=" * 60)
    print("SELECTED FEATURE COEFFICIENTS")
    print("=" * 60)

    for term in interesting_terms:

        matches = feature_data[
            feature_data["feature"] == term
        ]

        if len(matches) > 0:

            coefficient = matches.iloc[0]["coefficient"]

            direction = (
                "REAL"
                if coefficient > 0
                else "FAKE"
            )

            print(
                f"{term:15s} "
                f"{coefficient: .6f} "
                f"→ {direction}"
            )


if __name__ == "__main__":
    main()