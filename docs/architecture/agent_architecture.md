# Fake News & Scam Detection Agent
## Agent Architecture

### Project Goal

The goal of this project is to build an evidence-grounded
AI agent capable of investigating news claims and determining
whether available evidence supports, contradicts, or fails to
verify those claims.

The system should not rely solely on an ML classifier or an
LLM's internal knowledge. Instead, it should combine machine
learning signals, claim extraction, external evidence retrieval,
source evaluation, and LLM-based evidence analysis.

### Classical ML Baseline

The project includes a TF-IDF + Logistic Regression baseline.

Test performance:

- Accuracy: 99.12%
- F1 Score: 99.11%

However, dataset investigation identified substantial source
and metadata leakage. In particular, the subject field alone
predicts the label with 100% accuracy.

Therefore, the baseline is treated as an experimental benchmark
rather than evidence of real-world fake-news detection ability.

### Agent Goal

The agent will investigate claims using external evidence and
produce an evidence-backed structured verdict.

Possible verdicts include:

- SUPPORTED
- CONTRADICTED
- PARTIALLY_SUPPORTED
- UNVERIFIED
- CONFLICTING

## Initial Architecture

User
  ↓
Verification Agent
  ↓
Claim Extraction
  ↓
Evidence Retrieval
  ↓
Evidence Analysis
  ↓
Source Evaluation
  ↓
Classical ML Signal
  ↓
Final Verdict
  ↓
Structured Result

## Agent Contract

### Inputs

The verification agent can accept either:

1. A complete news article containing:
   - title
   - body
   - optional URL

2. An individual claim supplied directly by the user.

### Processing

The agent should:

1. Identify important factual claims.
2. Determine which claims require verification.
3. Retrieve relevant external evidence.
4. Evaluate the relevance and reliability of evidence.
5. Compare claims against available evidence.
6. Optionally use the classical ML model as an additional signal.
7. Produce an evidence-grounded assessment.

### Output

The agent should return a structured result containing:

- verdict
- confidence
- extracted claims
- evidence
- source assessment
- reasoning summary
- limitations

### Possible Verdicts

- SUPPORTED
- CONTRADICTED
- PARTIALLY_SUPPORTED
- UNVERIFIED
- CONFLICTING

### Important Principle

The agent must not treat the classical ML classifier as the final authority.

The ML model is one signal among multiple sources of evidence.

The agent should also avoid presenting an unsupported claim as
fact merely because the LLM has prior knowledge about it.