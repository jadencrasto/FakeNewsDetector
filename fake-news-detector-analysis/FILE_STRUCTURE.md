# Project File Structure

Below is the directory tree of the relevant files in the Fake News & Scam Detector project, excluding dependencies, virtual environments, and caches.

---

## 1. Directory Tree

```
FakeNews/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── schema.sql
│   ├── detector/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── indicators.py
│   │   ├── news_analyzer.py
│   │   ├── text_analyzer.py
│   │   └── url_checker.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   └── pdf_generator.py
│   ├── .env.example
│   ├── app.py
│   ├── check_schema.py
│   ├── config.py
│   ├── requirements.txt
│   ├── run_all_tests.py
│   ├── test_cases.py
│   └── view_scans.py
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── ScamDetector/
    │   │       ├── AnalyticsDashboard.tsx
    │   │       ├── Footer.tsx
    │   │       ├── Header.tsx
    │   │       ├── InputSection.tsx
    │   │       ├── ResultsSection.tsx
    │   │       ├── RiskMeter.tsx
    │   │       ├── SeverityBadge.tsx
    │   │       ├── StatsSection.tsx
    │   │       ├── index.tsx
    │   │       └── types.ts
    │   ├── App.tsx
    │   ├── index.css
    │   └── main.tsx
    ├── index.html
    ├── package.json
    ├── tailwind.config.ts
    └── vite.config.ts
```

---

## 2. File Explanations

### Backend Files
- [app.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/app.py): The main Flask server entry point that creates and runs the application.
- [config.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/config.py): Contains environment configs, database paths, and API key placeholders.
- [requirements.txt](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/requirements.txt): Lists all Python packages required to run the backend application.
- [routes.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/api/routes.py): Defines REST API endpoints for scanning inputs, checking statistics, logging feedback, and exporting reports.
- [models.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/database/models.py): Establishes database connection workflows and manages database transactions for scans and user feedback.
- [schema.sql](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/database/schema.sql): Defines the PostgreSQL database structure containing tables for scans, domain blacklists, and reports.
- [analyzer.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/detector/analyzer.py): Main coordinator that combines URL and text analytics to compute a final risk classification.
- [indicators.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/detector/indicators.py): Holds dictionaries containing scam-related keywords, urgency tokens, bank listings, and platform brand names.
- [news_analyzer.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/detector/news_analyzer.py): Checks news claims and headlines for clickbait patterns, conspiracy text, and source credibility metrics.
- [text_analyzer.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/detector/text_analyzer.py): Scans SMS and messages for fraud keywords (urgency, bank threats, OTP requests) while accounting for legitimate notifications.
- [url_checker.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/detector/url_checker.py): Audits URLs to identify suspicious TLDs, IP links, shortened addresses, and domain typosquatting.
- [analytics.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/utils/analytics.py): Queries the database to aggregate data points and formats them for the dashboard charts.
- [pdf_generator.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/utils/pdf_generator.py): Compiles analysis scores and recommendations into styled PDF documents using ReportLab flowables.
- [run_all_tests.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/run_all_tests.py): Executes test cases from `test_cases.py` to evaluate backend accuracy.
- [test_cases.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/test_cases.py): Contains standard text messages and headlines used to validate threat ratings.
- [view_scans.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/view_scans.py): Utility script that prints current statistics and recent scan logs from the database.

### Frontend Files
- [index.html](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/index.html): Standard HTML shell file for loading the React SPA client.
- [package.json](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/package.json): Lists Node tasks, commands, and dependency packages for frontend operation.
- [tailwind.config.ts](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/tailwind.config.ts): Configures styling definitions and themes for Tailwind CSS components.
- [vite.config.ts](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/vite.config.ts): Holds plugins and building scripts for bundling files with Vite.
- [main.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/main.tsx): Initializes and mounts the React application tree to the DOM node.
- [App.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/App.tsx): Configures router endpoints and registers the global layout components.
- [index.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/index.tsx): Controls state variables, connects with the backend API, and coordinates the dashboard layout.
- [InputSection.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/InputSection.tsx): UI layout containing the main form text area, URL inputs, and active mode toggles.
- [ResultsSection.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/ResultsSection.tsx): Renders color-coded risk alerts, triggered keywords, and recommended actions.
- [AnalyticsDashboard.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/AnalyticsDashboard.tsx): Uses Recharts to visualize classification trends, scan volumes, and common scam metrics.
- [RiskMeter.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/RiskMeter.tsx): Custom SVG gauge indicating the severity of threat scores.
- [SeverityBadge.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/SeverityBadge.tsx): Renders a colored pill label according to classification levels.
- [StatsSection.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/StatsSection.tsx): Renders small metric cards showing total scans and average risk ratings.
