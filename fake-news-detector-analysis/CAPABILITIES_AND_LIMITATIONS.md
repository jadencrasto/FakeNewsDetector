# Capabilities and Limitations: Fake News & Scam Detector

This document outlines the current capabilities, limitations, and weaknesses of the Fake News & Scam Detector project.

---

## 1. Current Capabilities
- **Fast Local Evaluation**: Computes results in less than 20 milliseconds by processing regex and keyword searches locally without making network calls.
- **Urgency & Threat Detection**: Effectively flags common urgency keywords and pressure tactics (e.g. "urgent", "account will be blocked", "within 24 hours") in incoming text.
- **Basic Brand & Indian Context Impersonation Check**: Recognizes mentions of major Indian banks (SBI, HDFC, ICICI), payment systems (Paytm, PhonePe, UPI), and brands (Amazon, Flipkart) to flag suspicious messages referencing them.
- **Typosquatting Identification**: Automatically alerts users if a domain tries to mimic a popular brand (e.g. `sbi-verify-india.com` or `paytm-prize.tk`).
- **Suspicious Domain Filtering**: Detects insecure `http://` configurations and extensions commonly used in scams (e.g. `.tk`, `.ml`, `.xyz`).
- **Visual Analytics**: Collects scan history in a PostgreSQL database and parses it to render dashboard statistics and historical trend charts (scans over time, scam types distribution) using Recharts.
- **On-the-fly PDF Generation**: Generates clean, formatted summary reports on demand using ReportLab.
- **Resilient UI Failover**: The frontend contains fallback mechanisms to show realistic demo payloads if the backend is offline.

---

## 2. Current Limitations
- **No Semantic Comprehension**: Evaluates text on a word-by-word basis. The system cannot understand contextual meaning, sentiment, or grammar.
- **Fake News Check is Simulated**: The `FakeNewsAnalyzer` claims verification is a mock method that checks for numbers or dates locally instead of conducting web queries or calling fact-checking databases.
- **No Real-Time API Verifications**: The system is configured for Google Safe Browsing and VirusTotal APIs in `config.py`, but they are not implemented in the scanning logic. The server does not perform live checks against external lists of malicious sites.
- **Static Lists**: The system lists of scam keywords, trusted domains, and bad TLDs are hardcoded. As new brands are targetted or new fraud mechanisms appear, the code must be modified.
- **Input Character Limits**: The backend restricts submissions to 5000 characters, preventing the analysis of long articles or email bodies.

---

## 3. Current Weaknesses
- **High False Positive Rate**: Since it relies on simple keyword mapping, legitimate security warning messages (e.g., *"Do not share your UPI PIN with anyone"*) will be classified as scams because they contain keywords like `UPI PIN`.
- **Easily Bypassed by Scammers**: A scammer can bypass the keyword checks by introducing minor spelling modifications (e.g. using `U.P.I. P-I-N` instead of `UPI PIN` or `Urgent!` written with special symbols).
- **Vulnerabilities in URL Extraction**: URL checking is easily tricked if URLs use complex routing, redirects, subdirectories, or link-shorteners that hide the target domain.
- **Local DB Dependencies**: Requires active connection pools with PostgreSQL. If the database connection drops, Flask endpoints print traceback errors to stderr, although they continue processing by returning transient responses.

---

## 4. Agentic Limitations
The application is non-agentic due to several structural limitations:
- **No Planning or Reasoning**: The system does not possess a reasoning loop (like ReAct). It follows a deterministic path and cannot decide to gather more evidence or select different analysis approaches based on input content.
- **No Tool Execution Capabilities**: There is no concept of tools. The system cannot run web searches, execute web scraping, query Whois databases, or query threat intel platforms dynamically.
- **No Memory or Context**: Each scan is independent. The analyzer cannot reference previous logs to recognize repeating campaigns or track coordinate threat actors.
- **No Self-Correction or Loops**: The analysis runs once. The code cannot evaluate its own output, double check findings, trace errors, or ask for clarifications.
- **No Autonomy**: The system is completely passive. It only executes when a user clicks the submit button, and cannot dynamically crawl the web, flag malicious domains automatically, or file complaints on cyber-crime sites.
