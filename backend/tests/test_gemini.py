from backend.llm.gemini_client import GeminiClient


def main():

    client = GeminiClient()

    title = "Scientists discover a new planet that may support life"

    text = """
    Scientists have reportedly discovered a new planet located
    20 light years from Earth. Researchers say the planet has
    conditions that could potentially support life.

    The research team used advanced telescopes to study the planet
    and believes its atmosphere may contain conditions similar to
    those found on Earth.
    """

    result = client.extract_claims(title, text)

    print("\n========================================")
    print("GEMINI CLAIM EXTRACTION")
    print("========================================")

    for index, claim in enumerate(result.claims, start=1):

        print(f"\nClaim {index}:")
        print("Claim:", claim.claim)
        print("Type:", claim.claim_type)
        print("Verification needed:", claim.verification_needed)
        print("Reason:", claim.reason)

    print("\n========================================")


if __name__ == "__main__":
    main()