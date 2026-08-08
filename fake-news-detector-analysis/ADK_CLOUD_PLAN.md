# Google ADK and Cloud Migration Plan

This document provides a system design for rebuilding and deploying the Fake News & Scam Detector using **Google's Agent Development Kit (ADK)** and **Google Cloud Platform (GCP)**.

---

## 1. Google ADK Integration Architecture

The Google Agent Development Kit (ADK) provides the tools to build, orchestrate, and deploy conversational agents powered by Gemini models. 

### Core Agent Design
The backend will be rebuilt using ADK's orchestrator to manage agent definitions and tool bindings:

```
                          ┌────────────────────────┐
                          │   ADK Agent Runtime    │
                          └───────────┬────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
   ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
   │  Gemini 2.5 Pro    │  │  Gemini 2.5 Flash  │  │     ADK Tools      │
   │  (Lead Reasoning   │  │  (Extraction &     │  │   (Search, WHOIS,  │
   │  & Fact-Checking)  │  │  Text Parsing)     │  │    Threat Intel)   │
   └────────────────────┘  └────────────────────┘  └────────────────────┘
```

- **Primary Orchestrator**: Manages session state and decides which specialized sub-agent or tool to trigger.
- **Model Selection**:
  - **Gemini 2.5 Flash**: Handled lightweight tasks (extracting URLs from messages, summarizing long web articles, and classifying sentiment/urgency).
  - **Gemini 2.5 Pro**: Used for multi-step reasoning, validating cross-referenced fact-checking websites, and resolving contradictions in source claims.

### Tool Declarations via ADK
Using ADK, developer tools can be bound directly to the agents:
- **`google_custom_search`**: Enables agents to search the web for fact-checking reports.
- **`whois_checker`**: Inspects domain registration details (identifying newly-created spoof domains).
- **`security_scanner`**: Connects with Google Safe Browsing and VirusTotal APIs to inspect domain integrity.

---

## 2. Session and State Management
- **Stateful Context**: Rebuilding the app with ADK sessions will allow users to have interactive conversations with the investigator (e.g. asking: *"Why do you think this is a scam?"* or *"What sources did you use to verify this?"*).
- **History Persistence**: Session state, user message history, and agent reasoning traces will be stored in PostgreSQL or Cloud Firestore, allowing users to return to past sessions via their `scan_id`.

---

## 3. Google Cloud Architecture Plan

Below is the serverless deployment pattern proposed for Google Cloud:

```
[ User Browser ] ──► [ Cloud Load Balancer / DNS ]
                              │
                              ▼
                 ┌───────────────────────────┐
                 │      Google Cloud Run     │ ◄── Pulls image from Artifact Registry
                 │   (FastAPI + ADK Engine)  │
                 └────────────┬──────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│    Cloud SQL     │ │  Secret Manager  │ │  Cloud Storage   │
│   (PostgreSQL)   │ │  (API Keys & DB) │ │ (PDF & Images)   │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### 1. Google Cloud Run (Compute)
- **Containerized Runtime**: The Python backend (migrated to FastAPI to natively support asynchronous operations) will be packaged as a Docker image and deployed to Cloud Run.
- **Serverless Scaling**: Scales to zero when inactive (reducing costs) and scales up during high-traffic viral news cycles.

### 2. Cloud SQL for PostgreSQL (Database)
- **Database Engine**: A fully managed PostgreSQL database hosting the `scans`, `known_scams`, `blacklisted_domains`, and `user_reports` tables.
- **Connection Security**: Accessed securely using the Cloud SQL Auth Proxy, removing the need to expose PostgreSQL ports to the public internet.

### 3. Cloud Secret Manager (Security & Credentials)
- **Key Storage**: Eliminates `.env` files by securely storing:
  - Gemini API keys.
  - VirusTotal and Google Safe Browsing API keys.
  - PostgreSQL database connection strings.
- **Access Control**: Handled via IAM service account roles, ensuring only the Cloud Run runtime has permission to resolve the secrets.

### 4. Cloud Storage (GCS)
- **Document Store**: Stores generated PDF credibility reports and scraped web screenshots. GCS bucket lifecycle rules will automatically clean up temporary PDF files after 7 days to manage storage costs.

### 5. Artifact Registry (Delivery Pipeline)
- **Container Repository**: Builds and stores Docker images during deployment.

---

## 4. Migration Roadmap Summary
1. **Phase 1: API Upgrades**: Replace the Flask API with an asynchronous FastAPI application.
2. **Phase 2: ADK Integration**: Implement the agent orchestrator, define Gemini 2.5 models, and convert the python helper scripts (`url_checker.py`, `text_analyzer.py`) into ADK-compliant tools.
3. **Phase 3: Database Migration**: Deploy a PostgreSQL instance on Cloud SQL and run `schema.sql` to initialize tables.
4. **Phase 4: Secret Management**: Load all third-party API keys into GCP Secret Manager.
5. **Phase 5: Cloud Deployment**: Package the FastAPI agent app into a Docker container, push it to Artifact Registry, and deploy it to Cloud Run.
