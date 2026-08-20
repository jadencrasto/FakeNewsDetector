from backend.evidence.search import EvidenceSearcher


def main():
    searcher = EvidenceSearcher(max_results=5)

    query = "scientists discovered new planet 20 light years from Earth"

    print("=" * 60)
    print("EVIDENCE SEARCH TEST")
    print("=" * 60)

    results = searcher.search(query)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("-" * 40)
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Snippet:", result["snippet"])


if __name__ == "__main__":
    main()