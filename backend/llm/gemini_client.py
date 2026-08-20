import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from typing import Literal


# Load variables from backend/.env
load_dotenv()

class Claim(BaseModel):
    """A factual claim extracted from an article."""

    claim: str = Field(
        description="A specific factual statement made by the article."
    )

    claim_type: Literal[
        "factual",
        "scientific",
        "political",
        "statistical",
        "historical",
        "opinion",
        "other"
    ] = Field(
        description="The type of claim."
    )

    verification_needed: bool = Field(
        description="Whether this claim should be independently verified."
    )

    reason: str = Field(
        description="Why this claim does or does not require verification."
    )

class ClaimExtraction(BaseModel):
    """Collection of claims extracted from an article."""

    claims: list[Claim] = Field(
        description="Important factual or potentially verifiable claims found in the article."
    )

class ArticleAnalysis(BaseModel):
    """Structured analysis returned by Gemini."""

    assessment: Literal[
        "likely_fake",
        "likely_real",
        "uncertain"
    ] = Field(
        description="Overall assessment based on the article content alone."
    )

    confidence: float = Field(
        description="Confidence from 0.0 to 1.0."
    )

    reasoning: str = Field(
        description="Brief explanation of why the article received this assessment."
    )

    suspicious_claims: list[str] = Field(
        description="Specific claims that should be independently verified."
    )

    verification_needed: bool = Field(
        description="Whether external evidence should be checked."
    )


class GeminiClient:
    """Client for Gemini-based news analysis."""

    MODEL = "gemini-3.6-flash"

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in backend/.env"
            )

        self.client = genai.Client(api_key=api_key)

    def extract_claims(self, title: str, text: str) -> ClaimExtraction:
        """Extract important claims from a news article."""

        prompt = f"""
    Analyze the following news article and extract its important claims.

    TITLE:
    {title}

    ARTICLE:
    {text}

    Instructions:

    1. Extract specific claims that could potentially be checked against
    external evidence.
    2. Do not extract every sentence.
    3. Focus on claims that matter to the article's main message.
    4. Separate factual claims from opinions.
    5. Preserve the meaning of the original claim.
    6. Do not invent information that is not present in the article.
    7. A claim does not automatically mean the article is false.
    8. Mark verification_needed as true when the claim should be checked
    against an independent source.
    9. Do not judge the overall article yet.

    The goal is CLAIM EXTRACTION, not final fact checking.
    """

        interaction = self.client.interactions.create(
            model=self.MODEL,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": ClaimExtraction.model_json_schema(),
            },
        )

        return ClaimExtraction.model_validate_json(
            interaction.output_text
        )

    def generate_text(self, prompt: str) -> str:
        """
        Send a general-purpose prompt to Gemini
        and return the generated text.
        """

        response = self.client.models.generate_content(
            model=self.MODEL,
            contents=prompt
        )

        return response.text


    def analyze_article(self, title: str, text: str) -> ArticleAnalysis:
        """Analyze a news article using Gemini."""

        prompt = f"""
Analyze the following news article.

Your task is to assess the article's reliability based ONLY on the
information provided in the title and article text.

Do NOT assume that something is false merely because:
- the writing is emotional,
- the article is politically biased,
- the article contains unusual wording,
- the article comes from an unfamiliar source.

Distinguish between:
1. suspicious writing/style,
2. unsupported claims,
3. claims that require external verification.

Do not claim that an article is definitely true or definitely false
without sufficient evidence.

TITLE:
{title}

ARTICLE:
{text}
"""

        interaction = self.client.interactions.create(
            model=self.MODEL,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": ArticleAnalysis.model_json_schema(),
            },
        )

        return ArticleAnalysis.model_validate_json(
            interaction.output_text
        )
    
    