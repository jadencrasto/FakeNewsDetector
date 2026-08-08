# Capstone Feature Specifications

This document defines the concrete features that can transform the current Fake News & Scam Detector into an advanced AI Agent capstone project.

---

## 1. MVP (Minimum Viable Product) Features
These features are necessary to establish a functional, LLM-backed baseline.

### 1. Semantic Scam Classification
- **What It Does**: Evaluates raw input text to understand its meaning, intent, and context (e.g., distinguishing between a real bank warning and a phishing SMS), replacing the static keyword-checking engine.
- **Handling Agent**: *Triage Agent* / *Scam Analysis Agent*
- **Tools/APIs Needed**: Gemini 2.5 Flash API (for fast extraction and classification).
- **Why It Improves the Project**: Drastically reduces false positives by introducing contextual language understanding.

### 2. Live Web Fact-Checking
- **What It Does**: Conducts Google queries for news claims and checks fact-checking databases in real-time.
- **Handling Agent**: *Search Agent*
- **Tools/APIs Needed**: Tavily Search API / Google Custom Search API.
- **Why It Improves the Project**: Replaces simulated news credibility checks with verified, live source analysis.

---

## 2. Strong Capstone Features
These features introduce autonomous workflows, agent coordination, and self-correction loops.

### 3. Dynamic WHOIS & Domain Reputation Verification
- **What It Does**: Automatically queries domain registration data for extracted links, flagging sites registered within the last 30 days or using anonymous proxy registrars.
- **Handling Agent**: *Network Intel Agent*
- **Tools/APIs Needed**: Whois lookup tool (built using Python's `python-whois` library) + VirusTotal URL Report API.
- **Why It Improves the Project**: Adds a layer of technical network forensics, allowing the agent to flag scam sites that haven't been indexed by search engines.

### 4. Cross-Reference & Conflict Debate
- **What It Does**: Compares reports from multiple news agencies on the same topic, identifying contradictions in timelines, quotes, or statistics.
- **Handling Agent**: *Cross-Reference Agent* (debating with the *Verification Agent*)
- **Tools/APIs Needed**: Jina Reader API (for scraping markdown from pages) + Gemini 2.5 Pro.
- **Why It Improves the Project**: Enables the system to explain *how* sources conflict and what elements of a claim are disputed.

### 5. Multi-Step Self-Reflection & Verification Loop
- **What It Does**: The agent drafts its conclusion, checks it against the retrieved source texts, identifies potential gaps or hallucinations, and updates its search criteria to collect missing data before returning the final report.
- **Handling Agent**: *Verification Agent* (audits the *Search Agent*)
- **Tools/APIs Needed**: Gemini 2.5 Pro reasoning loops.
- **Why It Improves the Project**: Ensures high-fidelity, explainable fact-checking outputs and demonstrates agentic self-reflection.

---

## 3. Advanced Features (Competition Quality)
These features incorporate advanced safety components and automation.

### 6. Interactive Conversational Debunker Chatbot
- **What It Does**: Allows users to chat with the agent after an analysis, asking follow-up questions, testing counterarguments, or requesting deeper source details.
- **Handling Agent**: *Orchestration Agent* (in session state mode)
- **Tools/APIs Needed**: ADK Session state persistence + Gemini 2.5 Pro.
- **Why It Improves the Project**: Enhances the user experience, transforming a static dashboard into an educational, interactive assistant.

### 7. Automated Cybercrime Portal Reporting
- **What It Does**: If a scam domain is verified with 99% confidence, the agent automatically compiles a detailed threat report (including domain WHOIS info, screenshots, and extracted text) and drafts a formal complaint format to be submitted to cybercrime portals (e.g. cybercrime.gov.in) or domain registrars for takedown.
- **Handling Agent**: *Reporting Agent*
- **Tools/APIs Needed**: Selenium / Playwright (for automated browser interaction) + ReportLab PDF compiler.
- **Why It Improves the Project**: Shows an agent taking real-world, helpful actions to secure the web ecosystem, making it a standout capstone project.

### 8. Image and Deepfake Media Analysis
- **What It Does**: Enables users to upload screenshots of social media posts, WhatsApp chats, or images, extracting text via OCR and scanning image metadata/reverse image databases to identify altered media.
- **Handling Agent**: *Multimodal Agent*
- **Tools/APIs Needed**: Gemini 2.5 Multimodal API (processing images) + Google Cloud Vision OCR.
- **Why It Improves the Project**: Extends the threat detection from text-only inputs to images and social media screenshots, where a large portion of misinformation is shared.
