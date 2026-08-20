from backend.llm.base import LLMClient
from backend.schemas.claim_schema import ClaimExtractionResult


class ClaimExtractor:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def extract(self, article_text: str) -> ClaimExtractionResult:

        prompt = f"""
You are a factual claim extraction system.

Your task is to identify important claims from the
provided article.

Extract only claims that can be objectively verified.

Do NOT determine whether the claims are true or false.

Do NOT add information that is not present in the article.

Article:
{article_text}
"""

        return self.llm.generate_structured(
            prompt,
            ClaimExtractionResult
        )