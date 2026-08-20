from typing import Literal
from pydantic import BaseModel, Field


class Claim(BaseModel):
    claim: str = Field(
        description="A specific factual statement that can be verified."
    )

    claim_type: Literal[
        "factual",
        "statistical",
        "event",
        "quote",
        "prediction"
    ]

    importance: Literal[
        "high",
        "medium",
        "low"
    ]


class ClaimExtractionResult(BaseModel):
    claims: list[Claim]