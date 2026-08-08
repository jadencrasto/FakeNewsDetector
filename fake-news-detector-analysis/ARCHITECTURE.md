# System Architecture: Fake News & Scam Detector

This document describes the runtime components, data flows, and structural relationships of the Fake News & Scam Detector.

---

## 1. High-Level Architecture Diagram
The diagram below illustrates the actual components and data flow of the application.

```
       [ User Web Browser ]
                 │
                 ▼ (Interacts with React UI)
   ┌────────────────────────────┐
   │    Vite React Frontend     │
   │   (Tailwind, shadcn, CSS)  │
   └─────────────┬──────────────┘
                 │
                 ▼ HTTP requests: POST /api/analyze | POST /api/verify-news
   ┌────────────────────────────┐
   │      Flask Backend         │  ◄── Loads configurations from .env
   │       (app.py API)         │
   └─────────────┬──────────────┘
                 │
                 ├──► Routing & Middleware (Flask CORS, Limiter)
                 │
                 ├──► Analysis Modules (detector/)
                 │    ├── ScamAnalyzer (combines Text & URL checks)
                 │    │     ├── TextAnalyzer (Heuristic regex engine)
                 │    │     └── URLChecker (TLD & typosquatting validator)
                 │    └── FakeNewsAnalyzer (Headline heuristics & source checks)
                 │
                 ├──► Database Operations (database/)
                 │    └── RealDictCursor / psycopg2 Connection Pool
                 │         │
                 │         ▼
                 │    ┌───────────────────────────┐
                 │    │    PostgreSQL Database    │
                 │    │   - scans table           │
                 │    │   - known_scams seed      │
                 │    │   - blacklisted_domains   │
                 │    │   - user_reports table    │
                 │    └───────────────────────────┘
                 │
                 └──► Reporting Utilities (utils/)
                      └── PDFReportGenerator (via ReportLab PDF platypus)
```

---

## 2. Architecture Components

### Frontend (User Interface)
- **Vite React SPA**: Served as a Single Page Application.
- **Form Handling & State Management**: Standard React hooks (`useState`) track mode selection (`scam` vs `news`), text input area, and active analysis responses.
- **Analytics Visualization**: Recharts parses the stats payloads fetched from `/api/analytics` to render:
  - Classification Breakdown (Pie chart of Safe vs Suspicious vs Scam).
  - Scan Timeline (Line chart of historical scans in the last 7 days).
  - Top Scam Types (Bar chart of detected categories).
- **Graceful Fallbacks**: If the backend is offline, the React codebase catches the network error and loads detailed hardcoded sample mock results to show how the UI functions.

### Backend (Flask REST API)
- **Application Factory (`app.py`)**: Configures the Flask instance, applies global CORS headers allowing cross-origin requests, binds rate limiters, and maps blueprints.
- **API Blueprints (`api/routes.py`)**: Exposes public endpoints:
  - `POST /api/analyze`: Passes text inputs to `ScamAnalyzer` and saves logs to the database.
  - `POST /api/verify-news`: Passes headlines and source URLs to `FakeNewsAnalyzer`.
  - `POST /api/report`: Inserts user feedback/reporting regarding scams.
  - `POST /api/export-pdf`: Takes scan results and returns compiled PDF files.
  - `GET /api/stats` / `GET /api/analytics`: Pulls PostgreSQL aggregates to feed dashboard charts.
  - `GET /api/history`: Returns the 10 most recent scans.

### Analysis & Core Logic Layer (`detector/`)
- **ScamAnalyzer (`analyzer.py`)**: Aggregates URL check results (weighted at 40%) and text content results (weighted at 60%) to compute an overall risk score (capped at 100).
- **TextAnalyzer (`text_analyzer.py`)**: Operates on a prioritized dictionary of keywords (defined in `indicators.py`). It sequentially rates the presence of keywords in categories: Urgency, Money Offers, Action Requests, Threats, Personal Info requests, and Payment Methods. It also applies a negative score modifier if legitimate bank notification formats are detected.
- **URLChecker (`url_checker.py`)**: Uses regular expressions and TLD tools to extract domains. It flags suspicious top-level domains (e.g. `.tk`, `.ml`, `.xyz`), checks for IP-based links, and identifies domain typosquatting using a list of popular brands.
- **FakeNewsAnalyzer (`news_analyzer.py`)**: Uses string-matching search stubs and text pattern analyzers to grade news articles. It penalizes clickbait phrasing, sensationalist buzzwords, conspiracy indicators, formatting anomalies (caps ratio, exclamation marks), and uncredited source declarations. It increases credibility ratings if specific dates or attributions are found.

### Database Layer (`database/`)
- **psycopg2 Connector**: Establishes database connections with PostgreSQL using connection-context wrappers to commit transactions and rollback on exceptions automatically.
- **Database Schema (`schema.sql`)**: Defines four tables:
  1. `scans`: Tracks the history of analyses with columns for metadata, inputs, hashes, and classification JSON payloads.
  2. `known_scams`: Stores verified scam signatures (used for seeding).
  3. `blacklisted_domains`: Holds domains that are flagged as malicious.
  4. `user_reports`: Logs user feedback submissions.

### Reporting Layer (`utils/pdf_generator.py`)
- **ReportLab Platypus Flowables**: Generates styled PDF files on-the-fly inside an in-memory `io.BytesIO` buffer, which is streamed directly back as a file attachment download.

---

## 3. Core Data Flow
Below is the execution flow when a user submits content:

```
User Input ──► React Client ──► Flask Route ──► Analysis Modules ──► Database Logging ──► PDF Utility (optional) ──► JSON Response ──► Dashboard UI
```

1. The client sends a JSON body to the Flask backend containing the input string.
2. The Flask route extracts the string, verifies length constraints (1 to 5000 characters), and invokes the analysis module.
3. The analysis modules parse URLs, evaluate domain structures, look up brand lists, count keywords, and determine risk levels.
4. The backend generates a SHA-256 hash of the input, saves the results (JSON metadata, classification, recommendations) to the PostgreSQL database, and gets a unique `scan_id`.
5. If the database insertion fails, the backend catches the error, logs it to stderr, and proceeds so the user receives a result.
6. The REST endpoint responds with status `200 OK` and a detailed JSON payload of the result.
7. The React client updates its dashboard states, displaying results, recommendations, and refreshed chart trends.
