# Fake News & Scam Detector - Project Summary

## 1. Project Overview
The **AI Scam Detector & Fake News Verifier** is a web-based application designed to help users identify and flag online threats, including:
- **SMS/UPI scams**: Fraudulent messages pressuring users to make transactions, share OTPs, or click suspicious links.
- **Phishing attempts**: Typosquatting and impersonation of popular Indian banks (e.g., SBI, HDFC) and brands (e.g., Amazon, Paytm).
- **Fake News & Misinformation**: Credibility scoring of headlines and claims.

The project addresses the growing threat of social engineering, banking fraud, and misinformation in the Indian digital ecosystem by offering a clean, real-time dashboard and downloadable PDF safety reports.

---

## 2. Current Architecture
The system employs a classic decoupled **Client-Server Architecture**:
```
User  <-->  Vite + React (Frontend)  <-->  Flask API (Backend)  <-->  PostgreSQL (Database)
                                                    |
                                                    +--> ReportLab (PDF Generator)
```
- **Frontend**: A React application built with TypeScript, Tailwind CSS, shadcn/ui components, and Framer Motion. It handles user inputs (text or URLs), displays risk meters, renders historical scan analytics charts using Recharts, and exposes endpoints to download PDF reports.
- **Backend**: A Python Flask REST API that routes requests to custom analysis modules, manages database connection pools, generates PDF reports, and provides rate limiting.
- **Database**: PostgreSQL storing scans (input, hash, classification, indicators, recommendations, score breakdown) and user reports.

---

## 3. Current AI/Agent Setup
Despite being named "AI Scam Detector," the project **does not contain any active AI models, LLM APIs, or AI Agents**. The current system is entirely deterministic and relies on:
1. **Regular Expressions & Wordlists**: Keyword mapping for urgency, threats, payment portals, and personal details (defined in `detector/indicators.py`).
2. **Deterministic Typo-squatting Checks**: String edit distance/impersonation checks on extracted domains (e.g., detecting `gooogle.com` or `paytm-prize.tk`).
3. **Mock/Heuristic Credibility Scoring**: Fake news checking using hardcoded lists of credible sources (e.g., `thehindu.com`, `reuters.com`), satire/unreliable sites (`theonion.com`), and simple clickbait keywords.

There is **no** autonomy, memory, planning, self-verification, or prompt-based orchestration.

---

## 4. Main Technologies
- **Frontend**: React (18.3), Vite, TypeScript, Tailwind CSS, Radix UI (shadcn), Recharts, Framer Motion, Sonner.
- **Backend**: Flask (3.0), PostgreSQL (via `psycopg2-binary`), Python Dotenv, Validators, tldextract, ReportLab (for PDF generation), Spacy (loaded in requirements but unused in core code).

---

## 5. Biggest Strengths
- **Rich User Interface**: Sleek dark-themed design with smooth animations, interactive risk gauges, live scan logs, and analytical dashboards.
- **Fast Execution**: Because it uses local regex and keyword parsing, analysis takes less than 20 milliseconds.
- **Structured Database & Reporting**: Clean PostgreSQL schema and automated PDF report compilation using ReportLab.

---

## 6. Biggest Weaknesses
- **"AI" Label Disconnection**: The application lacks any machine learning or generative AI logic, making it easily bypassed by paraphrasing or novel scam tactics.
- **Primitive Search/Verification**: The news verifier uses simulated web searches and basic keyword matching rather than retrieving real-time fact-checking sources.
- **Static Configurations**: Relies heavily on hardcoded list definitions that require manual code updates as new scams emerge.

---

## 7. Promising Capstone Direction: "Autonomous Misinformation & Scam Investigator"
The project can be upgraded into a multi-agent system that autonomously investigates suspicious claims:
- **Search & Verification Agents**: Querying search engines and fact-checking APIs (e.g., Snopes, AltNews) to gather live evidence.
- **Cross-Reference & Debate Agents**: Analyzing source conflicts and debating credibility.
- **Verdict & Reporting Agents**: Formulating explainable safety scores, drafting detailed summaries, and optionally submitting flagged entities to cyber-crime APIs.

---

## 8. Recommended Next Steps
1. **Integrate Google ADK / Gemini**: Rebuild backend analysis engines with Google's Agent Development Kit, leveraging Gemini 2.5 Flash/Pro for deep semantic threat understanding.
2. **Add Search Tooling**: Incorporate Tavily or Google Search API to verify news claims in real-time.
3. **Upgrade Database & Session Management**: Store conversation histories and multi-step agent logs inside the PostgreSQL database.
