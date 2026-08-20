from backend.evidence.claim_verifier import ClaimVerifier


def run_test(verifier, number, claim, evidence):
    print("\n" + "=" * 60)
    print(f"TEST {number}")
    print("=" * 60)

    print(f"\nClaim:\n{claim}")

    result = verifier.verify_claim(
        claim,
        evidence
    )

    print(f"\nVerdict: {result['verdict']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reason: {result['reason']}")

    print("\nSupporting Evidence:")

    for item in result.get("supporting_evidence", []):
        print(f"- {item}")


def main():

    verifier = ClaimVerifier()

    nasa_evidence = [
        {
            "title": "NASA - HD 20794 Super-Earth",
            "url": "https://science.nasa.gov/",
            "text": """
The newly confirmed planet is the outermost of three detected so far
around a star called HD 20794, just 20 light-years from Earth.

The planet spends a good chunk of its year in the habitable zone
around its star, the orbital distance that would allow liquid water
to form on the surface under the right atmospheric conditions.

But because of its eccentric orbit, it moves to a distance interior
to the inner edge of the habitable zone when closest to the star,
and outside the outer edge when farthest away.

At its closest, the planet's distance from the star is comparable
to Venus's distance from the Sun; at its farthest point, it is nearly
twice the distance from Earth to the Sun.
"""
        }
    ]

    # TEST 1 — Directly supported
    run_test(
        verifier,
        1,
        "Scientists have discovered a new planet located 20 light years from Earth.",
        nasa_evidence
    )

    # TEST 2 — Partially supported
    run_test(
        verifier,
        2,
        "Scientists have discovered a new Earth-like planet that definitely supports life.",
        nasa_evidence
    )

    # TEST 3 — Contradicted
    run_test(
        verifier,
        3,
        "The newly discovered planet remains permanently inside the habitable zone.",
        nasa_evidence
    )

    # TEST 4 — Insufficient evidence
    run_test(
        verifier,
        4,
        "The newly discovered planet has exactly 3 billion inhabitants.",
        nasa_evidence
    )


if __name__ == "__main__":
    main()