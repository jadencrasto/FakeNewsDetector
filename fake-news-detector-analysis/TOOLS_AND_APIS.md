# External Tools & APIs: Fake News & Scam Detector

This document catalogs the external tools, APIs, services, and databases used by the project.

---

## 1. Database Services

### PostgreSQL Database
- **Name**: PostgreSQL Database
- **Purpose**: Persists scan history logs, preloaded scam lists, domain blacklists, and user-submitted feedback.
- **Where It Is Used**: Managed in [models.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/database/models.py) using connection pools via `psycopg2`.
- **Data Received**:
  - Raw scanned strings, hashes, threat classifications (`safe`, `suspicious`, `scam`), client IP addresses, analysis processing durations, list of extracted URLs, and lists of triggered indicators and recommendations.
  - User feedback payloads (scan references, report types, comments).
- **Data Returned**:
  - Serial primary keys (`scan_id`, `report_id`).
  - Aggregated metrics (total count, scan counts per category, average risk score).
  - Dict arrays containing the 10 most recent logs.
- **Why the Project Needs It**:
  - To support the live UI analytics charts.
  - To show users a history of recent scans.
  - To record user-reported scams to improve future checks.

---

## 2. Document Utilities

### ReportLab (PDF Generation Engine)
- **Name**: ReportLab (Python Library)
- **Purpose**: Generates styled PDF files containing analysis details on-the-fly.
- **Where It Is Used**: Defined in [pdf_generator.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/utils/pdf_generator.py) and invoked by the `/api/export-pdf` route.
- **Data Received**: Analysis results dict (scores, classification levels, timestamps, inputs, indicators list, recommendations list).
- **Data Returned**: In-memory byte array stream (`bytes`) representing the compiled PDF document.
- **Why the Project Needs It**: Enables users to export, download, and share physical credibility reports of suspicious messages or news.

---

## 3. Configured but Unused APIs (Stubs)

The following services have environment variables and configuration objects declared, but **are not currently implemented or called** in the core code logic:

| Service / API Name | Config Location | Intended Purpose | Current Status in Code |
| :--- | :--- | :--- | :--- |
| **VirusTotal API** | `VIRUSTOTAL_API_KEY` in `config.py` | Verify if extracted URLs are flagged as malicious by malware engines. | **Unused**. Not imported or invoked by the analysis modules. |
| **Google Safe Browsing API** | `GOOGLE_SAFE_BROWSING_KEY` in `config.py` | Check extracted URLs against Google's index of unsafe websites (phishing/malware). | **Unused**. Not imported or invoked by the analysis modules. |
| **Web Scraping / Search** | `BeautifulSoup` and `requests` in `news_analyzer.py` | Fetch web search results to cross-check news claims against fact-checkers. | **Mocked**. The libraries are imported, but `_verify_claim` only checks for numbers/dates locally without performing HTTP requests. |
