# Complete Workflow: Trace Example

This document walks through a complete end-to-end trace of a scam message analysis request, detailing the exact variables, code paths, and outcomes.

---

## 1. Trace Scenario
- **User input submitted**: 
  `"🎉 Congratulations! You have won ₹50,00,000 in KBC Bumper Lottery! Your lucky number is 7845. Click here to claim: http://kbc-winner.tk Enter your bank details, Aadhar number, and OTP to verify."`
- **Application Mode**: `Scam Detection` (default)

---

## 2. Step-by-Step Execution Trace

### Step 1: Frontend Input Capture
- The user pastes the text into the text area in [InputSection.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/InputSection.tsx).
- The text is bound to the `input` state in [index.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/index.tsx).

### Step 2: Client Request Dispatch
- The user clicks the **"Analyze Message"** button.
- The `analyze()` function in [index.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/index.tsx#L19-L91) triggers.
- It sets `loading` to `true` and dispatches an HTTP POST request:
  - **URL**: `http://localhost:5000/api/analyze`
  - **Headers**: `{"Content-Type": "application/json"}`
  - **Body**: `{"input": "🎉 Congratulations! You have won ₹50,00,000 in KBC Bumper Lottery!..."}`

### Step 3: Flask Route Routing
- The request reaches Flask and is routed to `analyze()` in [routes.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/api/routes.py#L68-L119).
- The handler extracts the JSON payload and validates:
  - The input is not empty (length > 0).
  - The input is within limits (length <= 5000 characters).
- It calls `analyzer.analyze(input_text)` on the global `ScamAnalyzer` instance.

### Step 4: Core Analysis Init
- `ScamAnalyzer.analyze()` in [analyzer.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/detector/analyzer.py#L23-L88) initializes a default result dictionary:
  - `input`: Truncated preview of the text.
  - `input_hash`: Generated SHA-256 hash identifier snippet (`8e7a6f23b2c...`).
  - `indicators`: `[]`
  - `recommendations`: `[]`
  - `urls_found`: `[]`

### Step 5: URL Checker Processing
- `ScamAnalyzer` calls `self.url_checker.analyze_all_urls(input_text)` in [url_checker.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/detector/url_checker.py#L208-L224).
- `URLChecker.extract_urls()` scans the input with regular expressions:
  - Matches and extracts the URL: `http://kbc-winner.tk`.
- `URLChecker.analyze_url()` evaluates the URL:
  - Domain extraction yields domain `kbc-winner` and suffix `tk`.
  - **HTTP Check**: Detects the scheme is `http` (not `https`), adding **+15** points and creating a `security` indicator.
  - **Suspicious TLD Check**: Suffix `.tk` is matched in `SUSPICIOUS_TLDS`, adding **+35** points and creating a `domain` indicator.
  - **Typosquatting Check**: Scans for brand names in `LEGITIMATE_DOMAINS`. No targets found (score does not change).
  - **Keywords Check**: Scans URL characters for keywords like `verify`, `secure`. No keywords found.
  - **Sum of URL Metrics**: `15 + 35 = 50` points.
  - **Cap Application**: The score is capped at the maximum allowed URL component score of **40** points.
- Returns `url_score = 40`, two indicators, and list of URLs.

### Step 6: Text Analyzer Processing
- `ScamAnalyzer` calls `self.text_analyzer.analyze_text(input_text)` in [text_analyzer.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/detector/text_analyzer.py#L62-L167).
- `TextAnalyzer` processes the message:
  - **Legitimacy Check**: `_check_legitimate_patterns()` returns `false` (no bank transaction, tracking numbers, or official contact matches).
  - **Dictionary Keyword Matching**:
    - **Money Offer**: Matches `congratulations`, `won`, `₹`, and `lottery` (adds **+35** capped points; appends a `money_offer` indicator).
    - **Action Request**: Matches `click`, `verify`, and `enter` (adds **+35** capped points; appends an `action_request` indicator).
    - **Threats**: No matches.
    - **Personal Information**: Matches `bank`, `aadhar`, and `otp` (adds **+35** capped points; appends a critical `personal_info_request` indicator).
    - **Payments**: No matches.
    - **Unrealistic Offer**: Matches `won` and cash amounts (adds **+18** points; appends an `unrealistic_offer` indicator).
    - **Formatting**: Detects multiple exclamation marks and emojis (adds **+13** points; appends a `formatting` indicator).
  - **Text Scoring Cap**: The text analyzer sums these indicators and caps the text score at **60** points.

### Step 7: Score Aggregation & Classification
- `ScamAnalyzer` aggregates component scores: `url_score (40) + text_score (60) = 100`.
- The final `risk_score` is set to **100**.
- The classification is computed via `_classify(100)`: since `100 > 60` (SUSPICIOUS_THRESHOLD), the classification is set to **'scam'**.
- Actionable recommendations are compiled:
  - Since it is a `'scam'`, it appends standard scam warnings (e.g. "DO NOT click any links", "DO NOT share OTP/PIN/password").
  - Due to specific indicators (`personal_info_request`, `url_structure`), it inserts critical warnings to the top of the recommendation list:
    - *"CRITICAL: Never share OTP, PIN, or passwords via message/call"*
    - *"Suspicious link detected - do not click"*

### Step 8: Database Logging
- Back in [routes.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/api/routes.py#L97-L109), the caller appends `ip_address` (from `request.remote_addr`).
- It calls `db.save_scan(result)`.
- `Database.save_scan()` in [models.py](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/backend/database/models.py#L34-L80) performs:
  - Generates an MD5 input hash: `input_hash`.
  - Executes a PostgreSQL SQL command inserting the raw text, risk score, classification, and JSON payloads.
  - Commits the transaction and returns a unique `scan_id` (e.g. `45`).

### Step 9: Server Response
- The backend appends `scan_id: 45` to the JSON dict.
- Returns the payload to the frontend with an HTTP 200 JSON payload:
  ```json
  {
    "scan_id": 45,
    "input": "🎉 Congratulations! You have won ₹50,00,000...",
    "risk_score": 100,
    "classification": "scam",
    "indicators": [
      {"type": "security", "severity": "medium", "description": "URL not using HTTPS..."},
      {"type": "domain", "severity": "critical", "description": "Suspicious domain extension..."},
      {"type": "money_offer", "severity": "critical", "description": "..."},
      {"type": "personal_info_request", "severity": "critical", "description": "..."}
    ],
    "recommendations": [
      "CRITICAL: Never share OTP, PIN, or passwords via message/call",
      "Suspicious link detected - do not click",
      "🚫 DO NOT click any links in this message",
      "🚫 DO NOT share personal information (OTP, PIN, password)"
    ],
    "urls_found": ["http://kbc-winner.tk"],
    "analysis_time_ms": 14,
    "timestamp": "2026-08-09 02:00:00"
  }
  ```

### Step 10: Client UI Refresh
- The React component receives the JSON object and stores it in `result` state.
- `loading` is set to `false`.
- [ResultsSection.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/ResultsSection.tsx) is rendered:
  - The [RiskMeter.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/RiskMeter.tsx) animates its dial to 100%, styled in crimson.
  - The threat severity badge is set to `DANGER / SCAM`.
  - Indicators are rendered as warning cards.
  - Recommendations are listed with copy and block-sender prompts.
- Sub-dashboards ([AnalyticsDashboard.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/AnalyticsDashboard.tsx)) update their statistics cards by requesting new GET queries.
