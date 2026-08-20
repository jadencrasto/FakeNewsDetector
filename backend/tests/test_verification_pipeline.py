from backend.evidence.verification_pipeline import VerificationPipeline


def main():

    title = "Scientists Discover New Planet 20 Light Years From Earth"

    text = """
    Scientists have discovered a new planet located 20 light years from Earth.
    The newly discovered planet is similar to Earth and could support life.
    Researchers say the planet remains permanently inside the habitable zone.
    Scientists estimate that the planet has approximately 3 billion inhabitants.
    """

    print("=" * 60)
    print("END-TO-END EVIDENCE VERIFICATION TEST")
    print("=" * 60)

    pipeline = VerificationPipeline()

    result = pipeline.analyze_article(
        title=title,
        text=text
    )

    print("\n" + "=" * 40)
    print("FINAL VERIFICATION REPORT")
    print("=" * 40)

    print(f"\nArticle: {result['title']}")

    print(f"\nClaims verified: {len(result['claims'])}")

    for i, claim_result in enumerate(result["claims"], start=1):

        verification = claim_result["verification"]

        print("\n" + "-" * 40)
        print(f"CLAIM {i}")
        print("-" * 40)

        print(f"Claim:")
        print(claim_result["claim"])

        print(f"\nType:")
        print(claim_result.get("type"))

        print(f"\nVerdict:")
        print(verification.get("verdict"))

        print(f"\nConfidence:")
        print(verification.get("confidence"))

        print(f"\nReason:")
        print(verification.get("reason"))

        print("\nSupporting Evidence:")

        for evidence in verification.get(
            "supporting_evidence", []
        ):
            print(f"- {evidence}")


if __name__ == "__main__":
    main()