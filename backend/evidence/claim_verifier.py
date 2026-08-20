import json
from backend.llm.gemini_client import GeminiClient


class ClaimVerifier:
    """
    Verifies an individual claim against gathered web evidence.

    Possible verdicts:
        SUPPORTED
        PARTIALLY_SUPPORTED
        CONTRADICTED
        INSUFFICIENT
    """

    def __init__(self):
        self.gemini = GeminiClient()

    def verify_claim(self, claim, evidence):
        """
        Verify a claim against supplied evidence.

        Args:
            claim (str): The claim extracted from the article.
            evidence (list): List of evidence dictionaries.

        Returns:
            dict: Verification result.
        """

        if not evidence:
            return {
                "claim": claim,
                "verdict": "INSUFFICIENT",
                "confidence": 0.0,
                "reason": "No usable evidence was found.",
                "evidence": []
            }

        evidence_text = self._format_evidence(evidence)

        prompt = f"""
You are an evidence verification system for a fake-news detection agent.

Your task is to determine whether the CLAIM is supported by the provided
WEB EVIDENCE.

IMPORTANT RULES:
1. Do not assume the claim is true just because the evidence discusses
   a similar topic.
2. Check the specific facts in the claim.
3. Distinguish between direct support, partial support, contradiction,
   and lack of evidence.

4. Mark CONTRADICTED when the evidence establishes that an important
   part of the claim is false or that the opposite is true.

5. A claim does NOT need to be explicitly called "false" in the source
   to be considered CONTRADICTED. Infer contradiction when the evidence
   clearly establishes the opposite factual condition.

6. Mark INSUFFICIENT only when the available evidence genuinely does
   not provide enough information to determine whether the claim is
   supported or contradicted.

7. Do not treat absence of evidence as evidence of contradiction.

8. Do not use your own world knowledge as the primary evidence.

9. Base the decision only on the supplied evidence.

10. Be conservative. When evidence is ambiguous, prefer INSUFFICIENT.

11. Consider the meaning of the complete evidence, not only exact
    keyword matches. If the evidence describes a factual condition that
    logically conflicts with the claim, classify the claim as
    CONTRADICTED.

12. When evidence contains multiple relevant facts, consider them together
    before deciding the verdict.

13. Before deciding the verdict, identify the main entity or subject of the
    CLAIM and determine whether each piece of WEB EVIDENCE refers to that
    same entity.

14. Evidence about a different person, organization, planet, location,
    event, product, study, or other entity must NOT be used as direct
    support or contradiction for the CLAIM.

15. Do not transfer facts from one entity to another merely because they
    are in the same topic or category.

16. If the evidence discusses a different entity and provides no reliable
    information about the entity in the CLAIM, treat that evidence as
    irrelevant for verification.

17. If all available evidence is about a different entity, return
    INSUFFICIENT rather than SUPPORTED or CONTRADICTED.

18. A contradiction requires evidence about the same entity as the CLAIM.
    For example, evidence that Earth's population is 8 billion does not
    contradict a claim about the population of another planet.

19. Similarly, evidence that another exoplanet is habitable does not
    directly support a claim that a specific different exoplanet is
    habitable.

20. When the identity of the entity is ambiguous, prefer INSUFFICIENT
    rather than assuming that two entities are the same.

VERDICTS:

SUPPORTED
The evidence about the SAME ENTITY directly supports the important factual
parts of the claim.

PARTIALLY_SUPPORTED
Evidence about the SAME ENTITY supports some important parts of the claim
but not all of them, or the claim contains an exaggeration or missing
qualification.

CONTRADICTED
The evidence about the SAME ENTITY directly conflicts with an important
factual part of the claim OR establishes that the opposite condition is true.

Evidence about a different entity cannot be used to classify a claim as
CONTRADICTED.

INSUFFICIENT
The evidence does not provide enough information to determine whether
the claim is true or false. The absence of information alone is not
contradiction.

Before determining the verdict, perform this reasoning internally:

A. Identify the main entity/entities in the CLAIM.
B. For each SOURCE, determine what entity the evidence is actually about.
C. Ignore evidence that concerns a different entity.
D. Only use evidence referring to the same entity when determining
   support or contradiction.
E. Do not expose this internal reasoning in the JSON response.

CLAIM:
{claim}

WEB EVIDENCE:
{evidence_text}

Return ONLY valid JSON using this exact structure:

{{
    "verdict": "SUPPORTED | PARTIALLY_SUPPORTED | CONTRADICTED | INSUFFICIENT",
    "confidence": 0.0,
    "reason": "Short explanation based only on the evidence.",
    "supporting_evidence": [
        "Specific evidence supporting or contradicting the claim."
    ]
}}

The confidence must be a number between 0.0 and 1.0.
"""

        try:
            response = self.gemini.generate_text(prompt)

            result = self._parse_response(response)

            result["claim"] = claim
            result["evidence"] = evidence

            return result

        except Exception as e:
            return {
                "claim": claim,
                "verdict": "INSUFFICIENT",
                "confidence": 0.0,
                "reason": f"Verification failed: {str(e)}",
                "evidence": evidence
            }
    
    def verify_claims(self, claims, evidence):
        """
        Verify multiple claims using a single Gemini API request.
        """

        if not claims:
            return []

        claims_text = "\n".join(
            f"CLAIM {i + 1}: {claim.claim}"
            for i, claim in enumerate(claims)
        )

        evidence_text = "\n\n".join(
            f"SOURCE {i + 1}\n"
            f"Claim this source was retrieved for: {item.get('claim', '')}\n"
            f"Title: {item.get('title', '')}\n"
            f"URL: {item.get('url', '')}\n"
            f"Content: {item.get('content', item.get('text', item.get('snippet', '')))}"
            for i, item in enumerate(evidence)
        )

        prompt = f"""
You are an evidence verification system for a fake-news detection agent.

Your task is to verify ALL claims using ONLY the supplied web evidence.

IMPORTANT RULES:

1. Verify each claim independently.
2. Match evidence to the exact entity, event, place, person, or object
   mentioned in the claim.
3. NEVER combine evidence about different entities as though they refer
   to the same entity.
4. Do not assume a claim is true because the evidence discusses a similar
   topic.
5. Do not use your own world knowledge as evidence.
6. Absence of evidence is NOT contradiction.
7. Mark CONTRADICTED only when the evidence establishes that an important
   part of the claim is false or the opposite condition is true.
8. Mark INSUFFICIENT when the evidence does not provide enough information.
9. Mark PARTIALLY_SUPPORTED when only part of the claim is supported or
   the claim contains an exaggeration.
10. Be conservative.

VERDICTS:

SUPPORTED
The evidence directly supports the important factual parts of the claim.

PARTIALLY_SUPPORTED
The evidence supports some important parts but not all of them, or the
claim contains an exaggeration or missing qualification.

CONTRADICTED
The evidence directly conflicts with an important factual part of the
claim or establishes the opposite condition.

INSUFFICIENT
The evidence does not provide enough information to determine whether
the claim is true or false.

IMPORTANT:

Evidence about Earth, another planet, another person, or another event
must NOT be treated as evidence about the entity in the claim.

For example, if the claim concerns a newly discovered planet and a source
discusses Earth's population, that source does NOT contradict a claim
about the population of the newly discovered planet. It is simply
irrelevant evidence, so the correct verdict is INSUFFICIENT.

CLAIMS:

{claims_text}

WEB EVIDENCE:

{evidence_text}

Return a JSON array containing exactly one result for every claim.

Each result must contain:

{{
    "claim_index": integer,
    "verdict": "SUPPORTED" | "PARTIALLY_SUPPORTED" | "CONTRADICTED" | "INSUFFICIENT",
    "confidence": number between 0.0 and 1.0,
    "reason": string,
    "supporting_evidence": array of strings
}}

The claim_index must correspond to the CLAIM number above.
"""

        response = self.gemini.generate_text(prompt)
        
        if hasattr(response, "text"):
            return response.text

        return str(response)

    def _format_evidence(self, evidence):
        """
        Convert search/fetch results into a compact text representation.
        """

        formatted = []

        for i, item in enumerate(evidence, start=1):
            title = item.get("title", "Unknown source")
            url = item.get("url", "")
            text = item.get(
                "content",
                item.get("text", item.get("snippet", ""))
            )

            # Prevent enormous prompts if a webpage is very large.
            text = text[:8000]

            formatted.append(
                f"""
SOURCE {i}
Title: {title}
URL: {url}

Evidence:
{text}
"""
            )

        return "\n".join(formatted)

    def _parse_response(self, response):
        """
        Parse Gemini's JSON response safely.
        """

        if hasattr(response, "text"):
            response = response.text

        response = response.strip()

        # Remove markdown JSON fences if Gemini returns them.
        if response.startswith("```"):
            response = response.replace("```json", "", 1)
            response = response.replace("```", "", 1)
            response = response.strip()

        try:
            result = json.loads(response)

        except json.JSONDecodeError:
            return {
                "verdict": "INSUFFICIENT",
                "confidence": 0.0,
                "reason": "Gemini returned an invalid verification response.",
                "supporting_evidence": []
            }

        # Validate verdict.
        valid_verdicts = {
            "SUPPORTED",
            "PARTIALLY_SUPPORTED",
            "CONTRADICTED",
            "INSUFFICIENT"
        }

        verdict = result.get("verdict", "INSUFFICIENT")

        if verdict not in valid_verdicts:
            verdict = "INSUFFICIENT"

        # Safely handle confidence.
        try:
            confidence = float(result.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0

        confidence = max(0.0, min(1.0, confidence))

        return {
            "verdict": verdict,
            "confidence": confidence,
            "reason": result.get(
                "reason",
                "No explanation provided."
            ),
            "supporting_evidence": result.get(
                "supporting_evidence",
                []
            )
        }


if __name__ == "__main__":
    print("ClaimVerifier module loaded successfully.")