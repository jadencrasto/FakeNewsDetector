from backend.evidence.web_fetcher import WebFetcher


def main():

    fetcher = WebFetcher()

    url = "https://science.nasa.gov/universe/exoplanets/discovery-alert-super-earth-swings-from-super-heated-to-super-chill/"

    print("=" * 60)
    print("WEB FETCHER TEST")
    print("=" * 60)

    result = fetcher.fetch(url)

    print("\nStatus:", result["status_code"])
    print("URL:", result["url"])

    print("\nExtracted text:")
    print("-" * 60)
    print(result["text"][:5000])


if __name__ == "__main__":
    main()