import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def main():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    prompt = """
Search the web and verify this claim:

"Scientists have discovered a new planet located 20 light years
from Earth that may have conditions capable of supporting life."

Use Google Search to find current, reliable evidence.

Explain:
1. Whether the claim is supported, contradicted, or unclear.
2. What evidence you found.
3. Which sources support your conclusion.
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        tools=[
            {
                "type": "google_search"
            }
        ],
    )

    print("\n========================================")
    print("GOOGLE SEARCH GROUNDING TEST")
    print("========================================")

    print("\nOUTPUT:")
    print(interaction.output_text)

    print("\n========================================")
    print("INTERACTION DETAILS")
    print("========================================")

    print(interaction)


if __name__ == "__main__":
    main()