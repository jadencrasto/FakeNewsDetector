# AI Models & Prompts: Fake News & Scam Detector

This document catalogs the artificial intelligence models, prompt templates, and system instructions present in the application.

---

## 1. AI Model Calls & Prompts Status
> [!IMPORTANT]
> **There are no AI models, prompt templates, system instructions, or LLM integrations in the current project.**

The codebase is entirely built using traditional string matching, regular expressions, and hardcoded heuristic rule lists.

---

## 2. Mock AI Behavior in Frontend Client
In the React client code ([components/ScamDetector/index.tsx](file:///c:/Users/jason/OneDrive/Desktop/FakeNews/frontend/src/components/ScamDetector/index.tsx#L48-L87)), if the frontend fails to connect to the Flask server (e.g. if the backend service is offline), the client catches the error and serves a hardcoded "demo" mock result with static indicators:
- **Scam Detection Mock Output**:
  - `risk_score`: 85
  - `classification`: `"scam"`
  - `indicators`: Urgency keywords, financial lure (₹50,000), and suspicious links.
- **News Verification Mock Output**:
  - `risk_score`: 30 (credibility score)
  - `classification`: `"unverified"`
  - `indicators`: Clickbait language, missing source attributions, and emotional wording.

These mock payloads are hardcoded in the frontend JavaScript/TypeScript state and do not represent actual inference or LLM processing.

---

## 3. Recommended Migration to LLM / Prompt Engineering

To upgrade this application into a true AI Agent Capstone, we propose replacing the regex engines with actual LLM calls. Below is a conceptual design of the prompt templates that should be integrated:

### Proposed Scam Analysis Prompt
- **Model**: `gemini-2.5-flash` or `gemini-2.5-pro`
- **Temperature**: `0.0` (for high consistency)
- **Output Format**: Structured JSON matching the schema of the `scans` table.
- **System Instruction**:
  ```text
  You are an expert cybersecurity analyst specializing in social engineering and phishing detection.
  Analyze the user's input text for security risks, including financial scams, phishing URLs, UPI fraud, brand impersonation, and pressure tactics.
  
  You must output a valid JSON object matching the following structure:
  {
    "risk_score": <integer from 0 to 100>,
    "classification": <"safe" | "suspicious" | "scam">,
    "indicators": [
      {
        "type": "<string representation of category>",
        "severity": "<low | medium | high | critical>",
        "description": "<detailed sentence explaining why this was flagged>"
      }
    ],
    "recommendations": [
      "<actionable safety advice 1>",
      "<actionable safety advice 2>"
    ]
  }
  ```

### Proposed Fake News Analysis Prompt
- **Model**: `gemini-2.5-flash`
- **Output Format**: Structured JSON.
- **System Instruction**:
  ```text
  You are an expert fact-checking AI. Compare the provided news claim against known credible news standards.
  Assess the text for sensationalism, emotional bias, formatting manipulation, and clickbait patterns.
  Return a credibility score (0-100, where 100 is highly credible), classification ("verified", "unverified", "false"), and recommendations for verification.
  ```
