# Project Overview: Fake News & Scam Detector

This document describes the core functionality, architecture, and technology stack of the Fake News & Scam Detector project.

---

## 1. What the Project Does
The **AI Scam Detector & Fake News Verifier** is a Web application that scans messages, links, and news articles to assess their credibility and security risk. It determines whether a piece of content is:
- **A scam/fraud attempt**: Such as fake lotteries (e.g., KBC), customer care helpline scams, or UPI cashback schemes.
- **A phishing link**: Typo-squatted URLs mimicking trusted domains.
- **Fake news/misinformation**: Clickbait, conspiracy theories, or sensationalized reporting.

---

## 2. The Problem It Solves
Digital fraud and misinformation are rampant, especially in fast-growing digital economies like India's. Scammers use urgent language, brand impersonation, and unrealistic promises to trick users into clicking links, sharing OTPs/PINs, or sending money via UPI. Meanwhile, clickbait and sensational headlines spread panic and misinformation. 

This project provides a fast, centralized interface where users can paste questionable text or URLs and receive a risk classification (Safe, Suspicious, or Scam/False), detailed indicators of why it was flagged, and actionable recommendations.

---

## 3. The Intended User
The application is designed for:
- **Everyday internet users** who want to verify suspicious SMS messages, WhatsApp forwards, or news links.
- **Vulnerable groups** (e.g., senior citizens, new internet users) who may not recognize social engineering tactics.
- **Security analysts** who want to track recent scam trends and types.

---

## 4. End-to-End User Flow
From the moment a user submits text or a news headline until they receive results:
1. **User Input**: The user pastes a suspicious message/link in the Scam Detector or a news article headline/URL in the News Verifier.
2. **Client Request**: The React frontend sends a JSON payload to the Flask backend's `/api/analyze` or `/api/verify-news` endpoint.
3. **Backend Analysis**:
   - For scams, the `ScamAnalyzer` runs the input through `URLChecker` (extracts URLs and analyzes TLDs, typosquatting, security protocols) and `TextAnalyzer` (checks against keyword dictionaries for urgency, money, threats, and personal information requests).
   - For news, the `FakeNewsAnalyzer` checks content for sensationalism and clickbait click-patterns, evaluates source domain credibility, and scores details.
4. **Database Logging**: The backend saves the scan details (input text, risk score, classification, detected indicators, recommendations, client IP) into a PostgreSQL database.
5. **Response Delivery**: The backend returns a JSON payload containing the score, classification, and details.
6. **UI Rendering**: The frontend displays an interactive dashboard:
   - A visual **Risk Meter** (color-coded red/yellow/green).
   - A list of **Threat Indicators** showing why it was flagged.
   - **Safety Recommendations** on how to proceed.
   - Updates to the **Analytics Dashboard** charts (classification breakdown, scan timelines).
7. **Report Export (Optional)**: The user can click "Export PDF" to generate and download a professional PDF summary compiled on-the-fly by the backend using ReportLab.

---

## 5. Main Features
- **Scam Detection**: Multi-faceted parsing of SMS and text messages for financial and social-engineering threats.
- **News Verification**: Analysis of headlines for clickbait patterns, capitalization, conspiracy words, and source credibility.
- **Typosquatting & Domain Checks**: Detection of deceptive domains trying to impersonate popular brands (e.g., `sbi-verify-india.com`).
- **Interactive Analytics Dashboard**: Live metrics on total scans, average risk scores, scan timelines, and top scam types.
- **PDF Report Generation**: Generation and download of styled security reports.
- **Scan History Logs**: Real-time listing of the last 10 scans in the system database.

---

## 6. Technology Stack

### Frontend Technology
- **Framework**: React (v18.3) built with Vite and TypeScript.
- **Styling**: Tailwind CSS with custom fonts and modern shadcn/ui primitives.
- **Animations**: Framer Motion for interactive transitions.
- **Charts**: Recharts for dashboard analytics visualization.
- **Toasts**: Sonner for real-time success/error alerts.

### Backend Technology
- **Framework**: Flask (v3.0) REST API.
- **Web Server**: Gunicorn (for production) / Werkzeug dev server (for development).
- **Libraries**:
  - `psycopg2-binary` for PostgreSQL database connectivity.
  - `tldextract` and `validators` for URL domain parsing.
  - `reportlab` for compiling PDF reports.
  - `Flask-Limiter` for rate limiting API abuse.
  - `Flask-CORS` for cross-origin configuration.

### AI & Models Used
- **None**: Despite references to "AI" in titles, the current system is entirely rule-based and deterministic. It uses regular expressions and custom keyword dictionary heuristics.

### APIs / Services Used
- **VirusTotal API** & **Google Safe Browsing API**: Configurations exist in `config.py` and `.env` files, but they are stubbed/not utilized in the core analysis files (`url_checker.py`).

### Database / Storage
- **PostgreSQL**: Used to store scans, blacklisted domains, user-submitted scam reports, and preloaded known scam signatures.

---

## 7. How the Application is Started

### Backend Server
1. Navigate to the `backend` directory.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with configurations (specifically `DATABASE_URL`).
4. Start the application:
   ```bash
   python app.py
   ```
   *The server runs locally at `http://localhost:5000`.*

### Frontend Server
1. Navigate to the `frontend` directory.
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The client runs locally at `http://localhost:5173` or `http://localhost:8080`.*

---

## 8. How the Application is Deployed
- **Frontend**: Designed to be published on the Lovable platform (click Share -> Publish) or built as a static bundle using `npm run build` and hosted on static hosting providers (Vercel, Netlify, Cloudflare Pages).
- **Backend**: Designed to be run inside a Docker container or deployed on cloud platforms like Cloud Run, Heroku, or Render using Gunicorn.
- **Database**: Hosted on PostgreSQL database clouds (e.g., Neon, AWS RDS, Supabase, Google Cloud SQL).
