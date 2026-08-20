import re

from backend.llm.gemini_client import GeminiClient
from backend.evidence.search import EvidenceSearcher
from backend.evidence.web_fetcher import WebFetcher
from backend.evidence.claim_verifier import ClaimVerifier


class VerificationPipeline:
    """
    End-to-end evidence verification pipeline.

    Flow:
        Article
          ↓
        Claim Extraction
          ↓
        Context-Aware Web Search
          ↓
        Evidence Relevance Filtering
          ↓
        Web Fetching
          ↓
        Claim Verification
          ↓
        Final Results
    """

    def __init__(self):
        self.gemini = GeminiClient()
        self.searcher = EvidenceSearcher()
        self.fetcher = WebFetcher()
        self.verifier = ClaimVerifier()

    def analyze_article(self, title, text):
        """
        Analyze an article by extracting claims and verifying them
        against relevant web evidence.

        All claims are collected first and then verified using ONE
        Gemini request to reduce API usage.
        """

        # ---------------------------------------------------------
        # STEP 1: Extract claims
        # ---------------------------------------------------------
        claims_result = self.gemini.extract_claims(title, text)

        claims = claims_result.claims

        if not claims:
            return {
                "title": title,
                "claims": []
            }

        # ---------------------------------------------------------
        # STEP 2: Collect evidence for every claim
        # ---------------------------------------------------------
        claim_evidence = []

        for claim_data in claims:

            claim = claim_data.claim

            if not claim:
                continue

            # -----------------------------------------------------
            # STEP 3: Context-aware search
            # -----------------------------------------------------
            query = self._build_search_query(
                title=title,
                claim=claim
            )

            try:
                search_results = self.searcher.search(query)

                print("\n========== SEARCH QUERY ==========")
                print(query)

                print("\n========== SEARCH RESULTS ==========")

                for i, result in enumerate(search_results, start=1):
                    print(f"\nRESULT {i}")
                    print("Title:", result.get("title", ""))
                    print("URL:", result.get("url", ""))
                    print("Snippet:", result.get("snippet", "")[:500])

            except Exception as e:
                print("SEARCH ERROR:", e)
                search_results = []

            # -----------------------------------------------------
            # STEP 4: Rank/filter search results
            # -----------------------------------------------------
            relevant_results = self._rank_results(
                search_results=search_results,
                title=title,
                article_text=text,
                claim=claim
            )

            evidence = []

            # -----------------------------------------------------
            # STEP 5: Fetch relevant web pages
            # -----------------------------------------------------
            for result in relevant_results[:3]:

                url = result.get("url")

                if not url:
                    continue

                try:
                    fetched = self.fetcher.fetch(url)

                except Exception:
                    # A blocked/unavailable website should not
                    # terminate the entire verification pipeline.
                    continue

                if fetched.get("status_code") == 200:

                    evidence.append({
                        "title": result.get("title", ""),
                        "url": url,
                        "content": fetched.get("text", "")
                    })

            claim_evidence.append({
                "claim_data": claim_data,
                "claim": claim,
                "evidence": evidence
            })

        # ---------------------------------------------------------
        # STEP 6: Prepare data for ONE verification request
        # ---------------------------------------------------------

        verification_claims = [
            item["claim_data"]
            for item in claim_evidence
        ]

        # Combine evidence while preserving the source information.
        all_evidence = []

        for item in claim_evidence:

            for evidence_item in item["evidence"]:

                all_evidence.append({
                    "claim": item["claim"],
                    "title": evidence_item.get("title", ""),
                    "url": evidence_item.get("url", ""),
                    "content": evidence_item.get("content", "")
                })

        # ---------------------------------------------------------
        # STEP 7: Verify ALL claims using ONE Gemini request
        # ---------------------------------------------------------
        verification_response = self.verifier.verify_claims(
            claims=verification_claims,
            evidence=all_evidence
        )

        print("\n========== RAW VERIFICATION RESPONSE ==========")
        print(type(verification_response))
        print(verification_response)
        print("===============================================\n")

        import json
        import re

        try:
            if hasattr(verification_response, "text"):
                verification_response = verification_response.text

            verification_response = str(
                verification_response
            ).strip()

            # Extract JSON array even if Gemini wraps it in
            # markdown fences or adds surrounding text.
            match = re.search(
                r"\[\s*\{.*\}\s*\]",
                verification_response,
                re.DOTALL
            )

            if not match:
                raise ValueError(
                    "No JSON array found in Gemini response."
                )

            json_text = match.group(0)

            verification_results = json.loads(json_text)

            if not isinstance(verification_results, list):
                raise ValueError(
                    "Gemini verification response is not a JSON list."
                )

        except (json.JSONDecodeError, TypeError, ValueError) as e:

            print(
                f"WARNING: Failed to parse verification response: {e}"
            )

            verification_results = []

        # Create lookup by claim index.
        verification_by_index = {}

        for result in verification_results:

            if not isinstance(result, dict):
                continue

            claim_index = result.get("claim_index")

            if isinstance(claim_index, int):
                verification_by_index[claim_index] = result

        # ---------------------------------------------------------
        # STEP 9: Build final results
        # ---------------------------------------------------------

        results = []

        for index, item in enumerate(claim_evidence, start=1):

            claim_data = item["claim_data"]

            verification = verification_by_index.get(
                index,
                {
                    "verdict": "INSUFFICIENT",
                    "confidence": 0.0,
                    "reason": "No valid verification result was returned.",
                    "supporting_evidence": []
                }
            )

            results.append({
                "claim": item["claim"],
                "type": claim_data.claim_type,
                "verification_needed": claim_data.verification_needed,
                "reason": claim_data.reason,
                "verification": verification
            })

        # ---------------------------------------------------------
        # STEP 10: Return complete analysis
        # ---------------------------------------------------------

        return {
            "title": title,
            "claims": results
        }

    def _build_search_query(self, title, claim):
        """
        Build a context-aware search query.

        The article title is deliberately included so that claims
        containing ambiguous terms such as "the planet", "the company",
        "the president", etc. retain their article context.
        """

        title = self._clean_query(title)
        claim = self._clean_query(claim)

        return f'"{title}" {claim}'

    # =============================================================
    # RESULT RANKING
    # =============================================================

    def _rank_results(
        self,
        search_results,
        title,
        article_text,
        claim
    ):
        """
        Rank search results according to relevance to the article
        and claim.

        This is a lightweight retrieval filter.

        It does NOT determine whether a claim is true or false.

        Its purpose is only to prevent obviously unrelated sources
        from being sent to the claim verifier.
        """

        if not search_results:
            return []

        # Build context from the article title and the beginning
        # of the article.
        article_context = f"{title} {article_text[:5000]}"

        context_tokens = self._important_tokens(article_context)
        claim_tokens = self._important_tokens(claim)

        ranked = []

        for result in search_results:

            result_title = result.get("title", "") or ""
            snippet = result.get("snippet", "") or ""

            result_text = f"{result_title} {snippet}"

            result_tokens = self._important_tokens(result_text)

            if not result_tokens:
                continue

            # -----------------------------------------------------
            # Claim overlap
            # -----------------------------------------------------
            claim_overlap = len(
                claim_tokens.intersection(result_tokens)
            )

            # -----------------------------------------------------
            # Article context overlap
            # -----------------------------------------------------
            context_overlap = len(
                context_tokens.intersection(result_tokens)
            )

            # -----------------------------------------------------
            # Weighted score
            # -----------------------------------------------------
            #
            # Claim-specific terms are more important than generic
            # article terms.
            #
            score = (
                claim_overlap * 3
                + context_overlap
            )

            # Strong bonus when the result contains important
            # multi-word phrases from the article title.
            title_phrases = self._important_phrases(title)

            for phrase in title_phrases:
                if phrase in result_text.lower():
                    score += 5

            result_copy = dict(result)
            result_copy["_relevance_score"] = score

            ranked.append(result_copy)

        # Highest relevance first.
        ranked.sort(
            key=lambda item: item.get("_relevance_score", 0),
            reverse=True
        )

        return ranked

    # =============================================================
    # TEXT UTILITIES
    # =============================================================

    def _clean_query(self, text):
        """
        Clean text before sending it to the search engine.
        """

        text = re.sub(r"\s+", " ", text or "")
        return text.strip()

    def _important_tokens(self, text):
        """
        Extract meaningful tokens.

        Very common English words are removed because words such as
        "the", "planet", "has", "new", etc. are not useful for
        distinguishing entities.
        """

        stopwords = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "is",
            "are",
            "was",
            "were",
            "has",
            "have",
            "had",
            "this",
            "that",
            "these",
            "those",
            "from",
            "with",
            "for",
            "into",
            "about",
            "after",
            "before",
            "their",
            "there",
            "they",
            "them",
            "its",
            "it",
            "on",
            "in",
            "of",
            "to",
            "by",
            "as",
            "at",
            "be",
            "could",
            "would",
            "should",
            "new",
            "scientists",
            "scientist",
            "discovered",
            "discover",
            "claim",
            "claims",
        }

        tokens = re.findall(
            r"\b[a-zA-Z0-9][a-zA-Z0-9\-]*\b",
            (text or "").lower()
        )

        return {
            token
            for token in tokens
            if len(token) >= 3 and token not in stopwords
        }

    def _important_phrases(self, title):
        """
        Extract useful multi-word phrases from the article title.

        Example:
            "Scientists Discover New Planet 20 Light Years From Earth"

        produces useful phrases such as:
            "20 light years"
            "light years"
            "new planet"
        """

        words = re.findall(
            r"\b[a-zA-Z0-9][a-zA-Z0-9\-]*\b",
            (title or "").lower()
        )

        phrases = []

        for size in (4, 3, 2):
            for i in range(len(words) - size + 1):

                phrase_words = words[i:i + size]

                # Skip phrases made almost entirely from stopwords.
                meaningful = [
                    word
                    for word in phrase_words
                    if word not in {
                        "the",
                        "a",
                        "an",
                        "and",
                        "or",
                        "from",
                        "of",
                        "to",
                        "in",
                        "on",
                        "with",
                    }
                ]

                if len(meaningful) >= 2:
                    phrases.append(" ".join(phrase_words))

        return phrases


if __name__ == "__main__":
    print("VerificationPipeline module loaded successfully.")