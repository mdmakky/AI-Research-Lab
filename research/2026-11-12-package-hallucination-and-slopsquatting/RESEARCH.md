# Package Hallucination and Slopsquatting in LLM Coding Assistants: Measuring Hallucinated Dependencies, Their Exploitability on PyPI/npm, and Lightweight Defences

- Project id: `2026-11-12-package-hallucination-and-slopsquatting`
- Started: 2026-11-12
- Owner: the user (beginner researcher). Claude manages the workflow.

## Topic in plain language
AI coding assistants (ChatGPT, Copilot, Claude Code, Cursor) sometimes recommend software packages that do not exist; this is called *package hallucination*. If an attacker registers that made-up name on a public package registry (PyPI for Python, npm for JavaScript) and fills it with malware, every developer who trusts the AI and runs `pip install` / `npm install` gets infected; this attack is called *slopsquatting*. It is a new kind of *software supply-chain attack* (an attack through the third-party code a project depends on). This project reviews how often hallucinated packages occur, how exploitable they are, and which defences work, so that a small laptop-scale measurement + defence study can be designed.

## Scope
- In scope: package/dependency/import hallucination by LLMs and coding agents; its exploitation (slopsquatting, registry squatting) on package registries (PyPI, npm, others); detection, measurement methods and mitigations (model-side and tool-side); closely related supply-chain background (typosquatting, malicious packages) only where needed for the attack model.
- Out of scope: general LLM hallucination in natural language; general code-correctness hallucination unless it reports package/API-existence results; general software-supply-chain work with no LLM link (except 1–2 background papers).
- Time window (publication years): 2023–2026 (the topic emerged with ChatGPT-era code assistants); older supply-chain background allowed if seminal.
- Disciplines / venues of interest: software engineering (ICSE, FSE, ASE, TSE, TOSEM), security (USENIX Security, CCS, S&P, NDSS), NLP (ACL/EMNLP) and arXiv preprints (flagged).
- Target size for the first pass: up to 20 included papers (raise only with a reason).

## Objectives
1. O1 — Map the evidence on how often LLMs and coding agents hallucinate packages, and what drives it (model, language, prompt, quantization, agentic setting). (RQ1)
2. O2 — Understand the attack model: persistence/repeatability of hallucinated names and evidence of real-world exploitability on registries. (RQ2)
3. O3 — Compare existing defences (model-side and tool/registry-side) on effectiveness, cost and deployability on ordinary hardware. (RQ3)
4. O4 — Consolidate measurement methodology and identify a novelty-checked, laptop-scale implementation gap (measurement and/or lightweight defence). (RQ4, RQ5)

## Inclusion / exclusion criteria
| Include if | Exclude if |
|---|---|
| peer-reviewed journal/conference paper, or a preprint that is highly relevant and flagged as such | not about the topic; no empirical or methodological contribution; retracted; duplicate version |

## Search strategy
- Sources: OpenAlex, Crossref, arXiv (+ PubMed for biomedical topics)
- Query strings (one per facet):
  - F1 measurement: "package hallucination large language model code generation", "LLM hallucinated dependencies import nonexistent library"
  - F2 exploitation: "slopsquatting", "LLM package confusion supply chain attack PyPI npm", "typosquatting malicious packages registry"
  - F3 defences: "mitigating package hallucination", "package hallucination unlearning model editing retrieval", "LLM API hallucination mitigation retrieval documentation"
  - F4 agents/tools: "coding agent dependency installation security", "AI coding assistant supply chain security dependencies"
  - F5 benchmarks/testing: "code hallucination benchmark taxonomy", "fuzzing LLM package hallucination"
- Snowballing: references/citations of the most central papers.
- Every executed search is recorded automatically in `search/search-log.md`.

## Key decisions
- 2026-11-12 — Topic chosen by the user from four candidate security topics (option A, slopsquatting) — fits low-compute, short-time, implementation-oriented goal; small literature (~33 title hits since 2024 in OpenAlex).
- 2026-11-12 — Defaults: 2023–2026, peer-reviewed first, ≤20 papers, preprints allowed but flagged — the field is young, so many key works are arXiv preprints.
- 2026-11-12 — Novelty check to be run early (during gap phase) because the field moves fast.
