# LLM-based vs Traditional Static Analysis and Deep Learning Approaches for Source Code Vulnerability Detection: A Comparative Review

- Project id: `2026-11-12-llm-based-vs-traditional-static-analysis`
- Started: 2026-11-12
- Owner: the user (beginner researcher). Claude manages the workflow.

## Topic in plain language
Software vulnerabilities (security bugs such as SQL injection or buffer overflows) are usually found with *static application security testing* (SAST) tools — programs like CodeQL or Semgrep that scan source code with hand-written rules — or with deep-learning (DL) models trained on labelled vulnerable code. Since 2023, large language models (LLMs such as GPT-4, Claude, CodeLlama) are also used to find vulnerabilities, sometimes alone, sometimes combined with SAST. Practitioners and researchers want to know: which approach actually finds more real vulnerabilities, with fewer false alarms, at what cost? Published results disagree, partly because studies use different benchmarks and metrics. This project collects and compares that evidence side by side.

## Scope
- In scope: detection of vulnerabilities in *source code* (any language) by (a) LLMs (prompting, fine-tuning, agentic/reasoning), (b) SAST tools, (c) DL/transformer detectors (e.g. Devign, LineVul), and (d) hybrids of LLM + static analysis; empirical comparisons, benchmarks, and surveys that compare these families.
- Out of scope: binary/malware analysis, fuzzing and dynamic analysis as the main method, vulnerability *repair* only (no detection), network intrusion detection, LLM security itself (jailbreaks, prompt injection).
- Time window (publication years): 2020–2026 (LLM studies mostly 2023+; 2020–2022 only for key DL/SAST baselines and benchmarks).
- Disciplines / venues of interest: software engineering and security (ICSE, FSE, ASE, ISSTA, TSE, TOSEM, USENIX Security, CCS, S&P, IEEE Access, EMSE, IST).
- Target size for the first pass: up to 20 included papers (raise only with a reason).

## Objectives
1. Compare the detection performance (precision, recall, F1, false-positive rate) of LLM-based, SAST and DL approaches as reported in head-to-head studies.
2. Compare *how* they were evaluated (benchmarks, languages, CWE types, data-leakage control, realistic vs. synthetic code) to judge how far the results can be trusted and generalised.
3. Assess whether hybrid LLM + static-analysis designs outperform either family alone, and at what cost (compute, API cost, time).
4. Identify evidence-backed gaps and practical guidance for choosing an approach.

## Inclusion / exclusion criteria
| Include if | Exclude if |
|---|---|
| peer-reviewed journal/conference paper, or a preprint that is highly relevant and flagged as such | not about the topic; no empirical or methodological contribution; retracted; duplicate version |
| empirically evaluates LLM-based source-code vulnerability detection against at least one SAST or DL baseline, OR is a benchmark/dataset study used for such comparisons, OR is a survey/SLR comparing these families | LLM-only evaluation with no baseline (unless a central benchmark/realism study); detection of non-security bugs only; binary code only; repair-only |
| reports quantitative detection metrics or a structured comparison | no quantitative results and no structured comparison; low-quality/predatory venue |

## Search strategy
- Sources: OpenAlex, Crossref, arXiv (+ PubMed for biomedical topics)
- Query strings (one per facet):
  - F1 head-to-head: "large language model versus static application security testing vulnerability detection"
  - F2 LLM vs DL detectors: "large language model vulnerability detection deep learning baseline LineVul benchmark"
  - F3 hybrids: "LLM static analysis combined vulnerability detection false positive reduction CodeQL"
  - F4 evaluation realism: "vulnerability detection dataset data leakage label noise realistic evaluation PrimeVul"
  - F5 reasoning/agentic: "LLM agent reasoning vulnerability detection evaluation 2025"
  - F6 surveys: "survey large language models software vulnerability detection" 
- Snowballing: references/citations of the most central papers.
- Every executed search is recorded automatically in `search/search-log.md`.

## Key decisions
<!-- Append: date — decision — reason (in plain language). -->
- 2026-11-12 — Topic chosen by user from 4 candidates (LLM vs SAST vulnerability detection) — recent (most work 2025–26), manageable size (~155 title-matching papers since 2023 on OpenAlex), clear comparison axis, high practical value.
- 2026-11-12 — Paper type: comparative literature review (no own experiments) — user choice; easiest to finish while still publishable.
- 2026-11-12 — Defaults: 2020–2026 window, peer-reviewed first, ≤20 included papers; preprints allowed only if central and flagged.
- 2026-11-12 — 20 papers included from 6 facets (3 parallel scouts, ~19 searches, snowballing from PrimeVul, IRIS, zhou2024comparison). VulnLLM-R dropped (preprint without venue) to hold the 20-paper target. IRIS (ICLR 2025) and RepoAudit (ICML 2025) are peer-reviewed although rlab records them as arXiv preprints (those venues issue no DOIs).
- 2026-11-12 — Second pass approved by user: +4 papers from gap analysis (competitor review qin2026review; lu2025lab; tashenova2026real; deininger2026open), target raised 20 → 24 — needed for positioning (competitor must be cited) and to test gaps G2/G5/G6 against the closest evidence.
