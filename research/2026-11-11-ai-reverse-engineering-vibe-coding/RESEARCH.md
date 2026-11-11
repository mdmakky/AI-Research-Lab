# Evaluating AI-Assisted Reverse Engineering for Software Application Reconstruction through Vibe Coding: Functional Fidelity, Code Quality, and Maintainability

- Project id: `2026-11-11-ai-reverse-engineering-vibe-coding`
- Started: 2026-11-11
- Owner: the user (beginner researcher). Claude manages the workflow.

## Topic in plain language
*Vibe coding* means building software mainly by describing what you want to an AI model in natural language and accepting the code it writes, with little manual coding. This project asks what happens when that is used for *reverse engineering*: rebuilding an existing application only from what can be observed about it (its screens, its behaviour when used, its documentation), without access to its source code. Three questions matter for anyone relying on such a rebuild: does the new app behave like the original (*functional fidelity*), is the generated code well written (*code quality*), and can it be understood and changed later (*maintainability*)? The project reviews what the research literature already knows about each, and where the evidence is missing.

## Scope
- In scope: AI/LLM-assisted reconstruction or generation of software applications from observable artefacts (UI screenshots, designs, webpages, interaction traces, natural-language specifications/documentation); vibe-coding studies; evaluation of functional correctness/fidelity, visual fidelity, code quality and maintainability of LLM-generated application code; benchmarks and evaluation methods for these.
- Out of scope: binary/bytecode decompilation; source-to-source code translation and legacy migration (used only as contrast if needed); reverse engineering outside software (e.g. biology); general multimodal model architecture papers; security exploitation; education studies that only measure perceptions, not code outcomes.
- Time window (publication years): 2020–2026 (the LLM code-generation era); seminal earlier work allowed as background (flagged as such).
- Disciplines / venues of interest: software engineering (ICSE, FSE, ASE, ESEM, MSR, TOSEM, TSE, EMSE), NLP/ML (ACL, EMNLP, NAACL, NeurIPS, ICLR), HCI (CHI, UIST).
- Target size for the first pass: up to 20 included papers (raise only with a reason).

## Objectives
1. O1 — Map the approaches and tools used to reconstruct or generate applications from observable behaviour/UI with AI, and how they relate to vibe-coding workflows.
2. O2 — Synthesise the evidence on functional fidelity, code quality and maintainability of AI-reconstructed / AI-generated application code.
3. O3 — Appraise how these outcomes are evaluated: benchmarks, metrics, study designs, sample sizes, reproducibility.
4. O4 — Identify evidence-backed, novelty-checked research gaps and propose a feasible evaluation study.

## Inclusion / exclusion criteria
| Include if | Exclude if |
|---|---|
| peer-reviewed journal/conference paper, or a preprint that is highly relevant and flagged as such | not about the topic; no empirical or methodological contribution; retracted; duplicate version |
| empirical study, benchmark, method or systematic review on AI/LLM generation or reconstruction of applications/UIs from observable artefacts | binary decompilation; source-to-source translation as the main subject |
| empirical study of vibe coding or LLM-generated code that measures correctness, quality or maintainability | opinion/position pieces without evidence (background only); perception-only surveys |
| evaluation methods/metrics for fidelity, quality or maintainability of generated code | non-software "reverse engineering"; model-architecture papers without code-generation evaluation |

## Search strategy
- Sources: OpenAlex, Crossref, arXiv (+ web search for very recent work).
- Query strings (one per facet):
  - F1 vibe coding: `vibe coding large language models software quality`; `vibe coding empirical study`
  - F2 UI-to-code reconstruction: `screenshot to code generation multimodal LLM web application`; `design to code webpage generation benchmark`; `interactive webpage generation LLM benchmark`
  - F3 application-level generation & functional fidelity: `LLM full application generation benchmark functional correctness`; `end-to-end software development benchmark LLM agents`
  - F4 quality & maintainability: `maintainability code smells LLM-generated code empirical study`; `code quality static analysis AI-generated code`
  - F5 black-box / GUI reverse engineering: `LLM reverse engineering GUI application reimplementation behavior`; `GUI reverse engineering model extraction app`
- Snowballing: references/citations of the most central papers (OpenAlex).
- Every executed search is recorded automatically in `search/search-log.md`.

## Key decisions
- 2026-11-11 — "Reverse engineering" means reconstruction from behaviour/UI/documentation, not from source code or binaries — chosen by the user; closest to rebuilding an app by vibe coding.
- 2026-11-11 — Preprints included but flagged and weighted lower — chosen by the user, because vibe coding (term from 2025) is studied mostly in preprints so far.
- 2026-11-11 — Time window 2020–2026, ~20 papers first pass — default assumption; LLM code generation became practical around 2021.
- 2026-11-11 — Pilot searches found very little work that combines LLMs with black-box application reverse engineering directly; the review therefore combines adjacent literatures (UI-to-code, app generation, code quality of LLM output, vibe coding). Whether this combination is itself a gap must be confirmed by a novelty check.
- 2026-11-11 — First pass raised from 20 to 23 papers — the topic joins five separate literatures (vibe coding, UI-to-code, app-level generation, code quality, black-box reverse engineering); each needs ≥4 papers to compare. 22 further relevant papers kept as reserves in search/screening.md.
- 2026-11-11 — SusVibes (zhao2025vibe) is recorded as arXiv preprint but was published at ICML 2026 (PMLR v306, no DOI); treat as peer-reviewed in synthesis.
- 2026-11-11 — All 23 full texts obtained legally (arXiv, ACL Anthology, Springer OA). For 9 published papers the open copy is the arXiv version; page citations refer to the PDF we hold (`papers/<key>/paper.pdf`), not the publisher's pagination.
