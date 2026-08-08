# Agent Analysis: Fake News & Scam Detector

This document evaluates the agentic capabilities of the Fake News & Scam Detector project.

---

## 1. Do Agents Exist in the Current Project?
> [!IMPORTANT]
> **No agents exist in the current project.** 

The application is a standard, deterministic web application. It does not use LLMs, foundation models, prompt engineering, or agentic frameworks. The classification of scams and fake news is performed using **rule-based heuristics, regular expressions, and string-matching comparisons**.

---

## 2. Evaluation of Agentic Elements

To assist the receiving AI assistant in understanding how far the current codebase is from an agentic implementation, we evaluate standard agentic dimensions below:

| Agentic Dimension | Current Implementation Status |
| :--- | :--- |
| **Agent Roles** | **None**. There are no defined agents (e.g., search agents, verifiers, summarizers). The system uses two helper Python classes: `ScamAnalyzer` and `FakeNewsAnalyzer`. |
| **Instructions / Prompts** | **None**. No LLMs are called; hence, there are no prompt templates, system instructions, or context windows. |
| **Inputs & Outputs** | **Inputs**: Raw strings (user messages or headlines) and optional source URLs.<br>**Outputs**: Structured JSON payloads with risk scores, classifications, indicators, and recommendations. |
| **Tools Available** | **None**. The analyzers have no ability to execute external tools. They use local Python library functions (`tldextract`, `re`, `validators`) to parse strings locally. |
| **Agent Communication** | **None**. There are no agents to coordinate, message, or pass variables to one another. |
| **Hierarchies / Orchestration** | **None**. Execution is linear and procedural: Frontend ──► Flask Route ──► Procedural Code ──► Response. |
| **Loops & Retries** | **None**. Analysis runs exactly once per request. There are no self-reflection loops, validation retries, or execution feedback mechanisms. |
| **Memory & State** | **Static Storage Only**. The database logs past scans (`scans` table) and reports, but the analysis engine does not pull, reference, or learn from previous scans to inform the current analysis. |
| **Human-in-the-Loop** | **Passive Only**. Users can submit scam reports to flag items, which are stored as `user_reports` in the database, but there is no interactive loop where a human approves or guides the analysis step. |
| **Autonomous Action** | **None**. The system cannot take autonomous actions (e.g., calling an external API to block a domain or posting a correction to a platform). It only calculates a score and returns it to the client. |
| **Workflow Paradigm** | **Deterministic Request-Response**. The workflow is a standard HTTP `POST` request. The backend runs a fixed set of local regex checks and keyword counts, saves the result, and returns it. |

---

## 3. Why the Project is Non-Agentic

The system lacks the fundamental components of an AI Agent:
1. **No Autonomy/Decision Making**: The code cannot choose *how* to analyze a message. It always runs the exact same checks in the exact same sequence.
2. **No Semantic Reasoning**: It cannot comprehend context. For example, if a message says *"Please do not send your UPI PIN under any circumstances,"* the system may flag it as a scam because it contains the keywords `UPI PIN`.
3. **No External Integration**: It does not query live databases, web search engines, or domain threat portals to check if a claim is currently active or verified.
4. **No Adaptability**: If a scammer changes a single word (e.g., using `U.P.I.` instead of `UPI`), the static keyword lists may fail to flag it, and the system has no capability to dynamically adapt or realize the semantic similarity.
