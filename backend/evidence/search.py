from ddgs import DDGS


class EvidenceSearcher:
    def __init__(self, max_results=5):
        self.max_results = max_results

    def search(self, query):
        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=self.max_results
            )

            for result in search_results:
                results.append({
                    "title": result.get("title"),
                    "url": result.get("href"),
                    "snippet": result.get("body")
                })

        return results