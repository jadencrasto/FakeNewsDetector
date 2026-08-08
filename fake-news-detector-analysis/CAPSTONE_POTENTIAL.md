# Capstone Potential: AI Agent Upgrade Plan

This document details how the current Fake News & Scam Detector can be transformed into an **Autonomous Misinformation Investigation & Threat Analysis System**.

---

## 1. What Can Be Reused from the Current Project

### Frontend Interface
- The dashboard UI (built with Tailwind, React, and shadcn/ui) is highly polished. The **Risk Meter**, **Indicators Cards**, and **Recommendations list** can be reused to show agent outputs.
- The **Analytics Dashboard** (Recharts) can be repurposed to visualize agent operations, such as:
  - Agent confidence levels.
  - Distribution of verified vs. debunked claims.
  - Timeline of investigated campaigns.
- The **Scan History** list can remain as a feed of recent investigations.

### Database Layer
- The PostgreSQL schema (`schema.sql`) provides a solid foundation.
- The `scans` table can be extended to store detailed agent traces, reasoning logs, and evidence links in the `indicators` and `score_breakdown` JSONB columns.
- The `user_reports` table can be reused as a mechanism for human-in-the-loop triggers.

### PDF Report Generator
- The ReportLab engine (`pdf_generator.py`) can be reused to export formal "Fact-Check Reports" compiled by the agent, replacing the current static PDF fields with LLM-generated summaries and evidence bibliographies.

---

## 2. What Should Be Replaced or Upgraded

### Core Analysis Layer
- The local regular-expression matching and dictionary lookups in `text_analyzer.py` and `url_checker.py` should be replaced by LLM-based semantic parsers.
- The simulated/mocked search checks in `news_analyzer.py` must be replaced by live, agent-controlled search engine integrations.

### API Middleware
- The synchronous, simple request-response logic in Flask routes should be replaced with an **asynchronous event-driven task queue** (such as Celery, FastAPI WebSockets, or background threads) since agent reasoning runs can take several seconds to complete.

---

## 3. Proposed Multi-Agent Architecture

To create a system that autonomously investigates claims, we propose a multi-agent system using Google ADK or LangGraph:

```
                            [ User Input ]
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │    Supervisor Agent      │ ◄── Orchestrates the workflow
                    └──────┬────────────┬──────┘
                           │            │
            ┌──────────────┘            └──────────────┐
            ▼                                          ▼
┌───────────────────────┐                  ┌───────────────────────┐
│     Search Agent      │                  │  Threat Intel Agent   │
│   Queries Google,     │                  │ Queries VirusTotal,   │
│  Tavily, Wikipedia    │                  │  Whois, DNS records   │
└───────────┬───────────┘                  └───────────┬───────────┘
            │                                          │
            └──────────────┐            ┌──────────────┘
                           ▼            ▼
                    ┌──────────────────────────┐
                    │  Cross-Reference Agent   │ ◄── Compares sources &
                    │                          │     identifies contradictions
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │   Verification Agent     │ ◄── Reasoning Loop (ReAct)
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │   Drafting & Report Agent│ ──► Saves JSON & compiles PDF
                    └──────────────────────────┘
```

### New Agents to Add
1. **Supervisor / Orchestrator Agent**: Receives the claim, plans the investigation steps, delegates tasks to specialized agents, and determines when the evidence is sufficient.
2. **Web Investigation & Search Agent**: Formulates search queries, extracts text from news reports and fact-checking archives (e.g. Snopes, AltNews, BoomLive), and retrieves page contents.
3. **Threat Intel & URL Agent**: Conducts network lookups (DNS records, Whois registration dates) and queries security databases (VirusTotal, Google Safe Browsing) to analyze links.
4. **Cross-Reference & Debate Agent**: Compares articles retrieved by the search agent, detects contradictions, identifies logical fallacies, and flags biased language.
5. **Verification & Audit Agent**: A self-reflection agent that double-checks the final findings, reviews sources to ensure no hallucination occurred, and grades the confidence score.

---

## 4. Key Agent Tools to Add
- **Web Search Tool**: Google Custom Search, Tavily, or Brave Search to fetch live search results.
- **Web Scraper Tool**: Firecrawl, Jina AI Reader, or Playwright to extract clean markdown text from news pages.
- **Fact-Checking APIs**: Query API access to established repositories (such as the Google Fact Check Tools API).
- **Network Diagnostic Tools**: Whois lookup, DNS resolver, and SSL certificate checker tools to investigate domain ages (newly registered domains are a major indicator of scam websites).

---

## 5. Agentic Workflows & Decision Loops

### 1. Verification Loop (Self-Correction)
Before rendering a decision, the **Verification Agent** checks the final output:
- It runs a verification check: *"Does the retrieved evidence directly support the final decision?"*
- If the verification fails or finds contradictions, the agent modifies the search query and directs the **Search Agent** to collect further sources.

### 2. Source Credibility Assessment
Instead of checking a static list of domains, the agent evaluates source credibility dynamically:
- Queries Whois tools to check domain age (e.g., if a domain claims to be SBI but was registered 2 days ago, it is flagged).
- Evaluates the reputation of the hosting server and counts previous complaints associated with the IP.

### 3. Human-in-the-Loop Approval (HITL)
To make the capstone system practical and secure:
- **Flagged scams**: If the agent calculates a high-severity scam score but with low confidence, it pauses and prompts an administrator via a dashboard review screen.
- **Fact-checking edits**: Allows users to write in clarifications or upload additional screenshots of WhatsApp forwards, prompting the agent to refine its research vector.
