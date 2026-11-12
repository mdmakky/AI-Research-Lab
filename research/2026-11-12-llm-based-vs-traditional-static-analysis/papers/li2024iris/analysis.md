---
key: li2024iris
status: complete
evidence_basis: full-text
design: Tool proposal + benchmark evaluation (LLM-inferred taint specs + CodeQL + LLM alert triage) vs SAST baselines; 7 LLMs; ablations
dataset: CWE-Bench-Java (new; 120 manually validated CVEs in real-world Maven Java projects; CWE-22/78/79/94) + 30 latest-version projects
sample_size: 120 vulnerabilities (one per project); 30 projects for new-bug search; 960 manually checked spec labels; 50 manually checked alarms
metrics: #Detected / detection rate; average false discovery rate (AvgFDR); average per-project F1; spec recall/precision
main_finding: IRIS+GPT-4 detects 55/120 vs CodeQL 27/120, AvgFDR 84.82% vs 90.03%; smaller LLMs add detections but mostly worsen FDR.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# IRIS: LLM-Assisted Static Analysis for Detecting Security Vulnerabilities

- Authors: Li, Ziyang; Dutta, Saikat; Naik, Mayur
- Year / venue: 2024, arXiv (preprint)
- DOI: 10.48550/arxiv.2405.17238 · URL: https://arxiv.org/abs/2405.17238
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

**Version note:** our text is arXiv **v3 (6 Apr 2025)**, whose header reads "Published as a conference paper at ICLR 2025" (p. 1). rlab records the arXiv copy (`venue_kind: preprint`); in substance it is the ICLR 2025 camera-ready. All numbers below are from v3 only.

## 1. Research objective
- [A] Address two weaknesses of static taint analysis, missing taint specifications for third-party APIs (false negatives) and missing contextual reasoning (false positives), by combining LLMs with static analysis for whole-repository security vulnerability detection (p. 1, p. 2).
- [A] Test whether LLMs can be combined with static analysis, given that method-level LLM detection fails on context-dependent vulnerabilities (p. 2).

## 2. Research questions / hypotheses
- [V] RQ1: how many previously known vulnerabilities IRIS detects; RQ2: whether it finds new, previously unknown vulnerabilities; RQ3: quality of the inferred source/sink specifications; RQ4: effectiveness of individual components (p. 7).
- [A] Hypothesis: LLMs pre-trained on internet-scale data know the behaviour of widely used library APIs and can label them as sources/sinks (p. 14).

## 3. Methodology
- Research design: [V] Tool proposal with quantitative benchmark evaluation against SAST baselines, a 7-LLM comparison, ablations, and a manual search for new bugs (p. 7–10).
- Approach / model / intervention: [V] Four stages: (1) CodeQL extracts candidate external APIs and internal public-function parameters; (2) an LLM labels them as CWE-specific sources/sinks (few-shot, usually 3-shot, for external APIs; zero-shot plus README/JavaDoc for internal APIs; batched JSON prompts); (3) labels become CodeQL predicates and a CWE-specific taint query runs; (4) "contextual analysis": an LLM classifies each reported path as true/false positive from CWE info, ±5 lines around source and sink and up to S=10 intermediate steps (p. 4–6, p. 15–16). [V] Sanitizer specifications are not inferred (p. 5). [V] CodeQL 2.15.3 was patched with an extra dataflow edge from `throw` to the nearest enclosing try-catch (p. 20).
- Baselines or comparison conditions: [V] CodeQL 2.15.3 built-in security queries (union of all queries per CWE, all alarm levels counted, described as "To CodeQL's advantage"), Facebook Infer, SpotBugs, Snyk (p. 7, p. 20). [V] Ablations swap LLM sources or sinks for CodeQL's and compare with/without contextual analysis (p. 9–10). No LLM-only or deep-learning detector baseline is evaluated (p. 7–10).

## 4. Dataset and sample
- Data source(s): [V] CWE-Bench-Java, curated from the GitHub Advisory Database, cross-checked with libraries.io and snyk.io, built with Maven (p. 7, p. 19).
- Sample size (N) and unit: [V] 120 vulnerabilities, one per project: CWE-22 = 55, CWE-78 = 13, CWE-79 = 31, CWE-94 = 21; average 300K SLOC, max 7M SLOC; 10 projects over 1M lines (p. 2, p. 7). [V] RQ2: latest versions of 30 Java projects (p. 8). [V] RQ3 precision: 960 manually inspected spec labels (30 per CWE×LLM) (p. 8).
- Sampling / selection method: [V] Funnel 1065 initial CVEs → 430 with GitHub URL/version → 265 with fix commit → 149 compilable → 144 with Java-code fixes → 120 after manual validation by two co-authors who cross-checked each other (p. 19). How the 30 RQ2 projects were chosen: not reported.
- Data availability (public? link?): [V] Dataset and build scripts at https://github.com/iris-sast/cwe-bench-java (p. 2).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] LLMs: GPT-4 (gpt-4-0125-preview), GPT-3.5 (gpt-3.5-turbo-0125), Llama-3 8B/70B Instruct, Qwen-2.5-Coder 32B, Gemma-2 27B, DeepSeekCoder 7B (p. 21). [V] OpenAI queries ran April–May 2024 (p. 20). [V] Temperature 0, max tokens 2048, top-p 1; seed fixed for GPT models; batch sizes 20 (internal) and 30 (external) APIs (p. 20–21). [V] Open models ran on a 4× RTX 2080 Ti machine and an 8× A100 machine (p. 20). [V] A vulnerability counts as detected if at least one reported path passes through a fix location (patched method) (p. 6, p. 18).
- Code availability: [V] https://github.com/iris-sast/iris (p. 1).

## 6. Evaluation metrics
- [V] #Detected / detection rate: projects where at least one path hits the patched location; measures recall of known CVEs (p. 6).
- [V] AvgFDR: mean over projects with ≥1 alarm of (1 − path precision); measures false-alarm burden (p. 6). [A] Authors call it an upper bound, since unknown true vulnerabilities count as false positives (p. 7).
- [V] AvgF1: per-project F1 averaged over all projects (p. 6).
- [V] Spec recall against CodeQL's own specifications, and spec precision on manually labelled samples (p. 8).
- Statistical testing: not reported (no significance tests or confidence intervals; number of runs not reported, settings are deterministic: temperature 0, fixed seed for GPT models, p. 21).

## 7. Key findings
1. [V] IRIS+GPT-4 detects 55/120 (45.83%) vs CodeQL 27/120 (22.50%); AvgFDR 84.82% vs 90.03%; AvgF1 0.177 vs 0.076 (Table 1, p. 8).
2. [V] Other LLMs: GPT-3.5 47 (FDR 90.42%), L3 8B 41 (95.55%), L3 70B 54 (90.96%), Q2.5C 32B 47 (92.38%), G2 27B 45 (91.23%), DSC 7B 52 (95.40%). Only GPT-4 brings FDR below CodeQL; L3 8B and DSC 7B have lower AvgF1 than CodeQL (Table 1, p. 8).
3. [V] Other SAST baselines detect fewer: Infer 0, SpotBugs 4, Snyk 23 of 120 (Table 2, p. 8).
4. [V] Per CWE (GPT-4 vs CodeQL): CWE-22 31 vs 22 of 55; CWE-78 3 vs 1 of 13; CWE-79 13 vs 4 of 31; CWE-94 8 vs 0 of 21 (Table 2, p. 8). [A] CWE-78 stays hard because of gadget chains and side effects that static analysis cannot track (p. 8).
5. [V] Manual check of 50 random IRIS+GPT-4 alarms found 27/50 with potential attack surfaces, giving an estimated FDR of 46% (p. 7).
6. [V] On the latest versions of 30 projects, IRIS+GPT-4 found 4 previously unknown vulnerabilities (3 CWE-22, 1 CWE-94) among the 16 projects with alerts; CodeQL alone did not detect them (p. 8). Developer confirmation or CVE assignment: not reported.
7. [V] LLM sink specs recover 87.11% (GPT-4) of CodeQL's sinks; source recall is lower (60.58% GPT-4, 25.67% GPT-3.5). GPT-4 spec precision is 75.73% (sources) / 69.12% (sinks); other LLMs about 29–42% (Fig. 6–7, p. 9).
8. [V] Ablation (GPT-4): CodeQL sources+sinks 27; GPT-4 sources + CodeQL sinks 36; CodeQL sources + GPT-4 sinks 24; both from GPT-4 55 (Table 3, p. 10).
9. [V] LLM triage (contextual analysis) raises avg precision/F1 only for GPT-4 (+0.074/+0.073), GPT-3.5 and Llama-3 70B; it slightly lowers them for L3 8B and DSC 7B (Fig. 9, p. 10). [A] Smaller models answer "vulnerable" more often (p. 9).
10. [V] Runtime with Llama-3 8B ranges from 43 s to 4 h per project (e.g., aws-sdk-java 7.72M SLOC: 38 min; keycloak: 3–4 h) (Table 10, p. 22–24). Dollar or token cost: not reported.

## 8. Limitations stated by the authors
- [A] Many vulnerabilities remain undetected; tighter integration of the two tools may help (p. 10).
- [A] IRIS makes many LLM calls, increasing analysis cost (p. 10).
- [A] Only Java evaluated; performance on other languages is unknown (p. 10).
- [A] Gap between IRIS reports and what developers want to see (p. 10).
- [A] FDR is an upper bound because unknown true vulnerabilities count as false positives (p. 7).
- [A] Misses come from vulnerabilities not expressible as simple taint flows, side-effect dataflow (e.g., via temp files), library-only flows, and missing LLM propagator/source/sink labels (p. 22).
- [A] Only some source/sink kinds are handled (not, e.g., protected overridden methods, impure-function arguments, thrown exceptions) (p. 14).

## 9. Limitations we identified
- [I] Possible training-data contamination: the CVEs and fixes are public and older than the 2024 queries (p. 20), and the paper does not discuss leakage (a text search for contamination/memorisation finds nothing). GPT-4's API labels may partly reflect memorised advisories.
- [I] Precision stays low in absolute terms: AvgFDR 84.82% means most reported paths are not the known vulnerability. The refined 46% estimate rests on only 50 alarms, with the labelling process not described.
- [I] Possible confound: IRIS runs on a patched CodeQL 2.15.3 (extra throw→catch edge, p. 20); the baseline uses the built-in 2.15.3 Security queries (p. 20, C.2), but it is unclear whether the baseline ran on the patched or the unpatched engine. The ablation row "SrcQL + SnkQL" equals the baseline (27, p. 10), which suggests the patch adds little, but the paper does not say so explicitly.
- [I] The "detected" criterion is lenient (any path touching the patched method), so a coincidental path can count as a detection.
- [I] No LLM-only or deep-learning baseline, so the paper does not show IRIS beats those families on this benchmark (matters for RQ1).
- [I] Number of runs not reported (deterministic settings, p. 21), no variance or significance tests; the 28-detection gap is large, but smaller gaps between LLMs are untested.
- [I] Cost is not quantified in tokens or dollars, which limits its use for RQ3 trade-offs.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Patched CodeQL for IRIS, unclear whether also used for the baseline (p. 20); possible memorisation of public CVEs (not discussed); dataset curated by the tool's own authors (p. 19).
- External (generalisability of sample/context): [I] Java/Maven only, four CWE classes, compilable libraries only (p. 7, p. 19); vulnerabilities fixed in non-Java files excluded (p. 19).
- Construct (do metrics measure the concept?): [I] FDR counts unknown real bugs as false positives (acknowledged, p. 7); "detected" relies on fix-location overlap.
- Statistical conclusion (power, multiple comparisons, variance): [I] No tests, number of runs not reported; N=120 overall but small per-CWE cells (CWE-78 N=13).
- Reproducibility (data/code/setup reported?): [V] Code, dataset, model IDs and hyper-parameters are reported (p. 1, p. 2, p. 20–21). [I] Pinned OpenAI model snapshots may be retired, which limits exact replication.

## 11. Future research directions
- Stated by authors [A]: tighter LLM–static-analysis integration, other languages, better developer-facing reports (p. 10); dynamic approaches for CWE-78 (p. 8); probability estimates for specifications (p. 10); more source/sink kinds (p. 14).
- Suggested by us [I]: contamination-controlled evaluation on post-cutoff CVEs; head-to-head with LLM-only and DL detectors on CWE-Bench-Java; per-project token/dollar cost reporting.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]: A central hybrid study ("LLM inside SAST") with a real SAST baseline on repository-scale, real-world Java. It shows the hybrid roughly doubles recall of known CVEs over CodeQL, while precision stays poor and the gain depends on model strength. It also contributes CWE-Bench-Java, relevant to RQ2.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1/RQ3 | IRIS+GPT-4 detects 55/120 CVEs vs CodeQL 27/120; AvgFDR 84.82% vs 90.03%; AvgF1 0.177 vs 0.076 | p. 8 | V | moderate |
| RQ1 | Other SAST tools on CWE-Bench-Java: Infer 0, SpotBugs 4, Snyk 23 of 120 | p. 8 | V | moderate |
| RQ3 | Hybrid gain depends on the LLM: only GPT-4 lowers FDR below CodeQL; L3 8B/DSC 7B FDR ~95%; LLM triage hurts small models | p. 8, p. 10 | V | moderate |
| RQ3 | Both LLM-inferred sources and sinks are needed (ablation 27 / 36 / 24 / 55) | p. 10 | V | moderate |
| RQ3 | Runtime 43 s to 4 h per project (Llama-3 8B); dollar cost not reported | p. 22–24 | V | moderate |
| RQ4 | Per-CWE: CWE-94 0→8, CWE-79 4→13, CWE-22 22→31, CWE-78 1→3 (hard for all tools) | p. 8 | V | moderate |
| RQ2 | New benchmark CWE-Bench-Java: 120 compilable, manually vetted real-world Java CVEs, avg 300K SLOC | p. 7, p. 19 | V | moderate |
| RQ2/RQ5 | Data contamination of public CVEs is not addressed | p. 7–10 | I | weak |
| RQ5 | Authors: many vulnerabilities still undetected; many LLM calls raise cost; Java only | p. 10 | A | moderate |

## 14. Key quotes
> "A state-of-the-art static analysis tool CodeQL detects only 27 of these vulnerabilities whereas IRIS with GPT-4 detects 55 (+28)" (p. 1)
> "the reported FDR is an upper bound" (p. 7)
> "IRIS makes numerous calls to LLMs for specification inference and filtering false positives, increasing the potential cost of analysis." (p. 10)

## Analyst notes
- Reading coverage: whole paper read (main text, appendices A–D incl. Table 10). Figures 6, 7 and 9 were read from PDF page images (p. 9–10) because their values are not in the text layer.
- Version: arXiv v3, 6 Apr 2025, ICLR 2025 header (p. 1). We did not have v1; earlier versions reportedly gave different numbers, so no v1 figure is cited. When other papers quote IRIS numbers, check which version they used.
- Venue: metadata says preprint; the text is the ICLR 2025 version. Treat as a peer-reviewed conference paper in substance, while citing the arXiv record.
- Uncertainties: Fig. 6/7/9 values read from bar labels in the PDF image; per-model precision/F1 before triage is only shown as deltas (Fig. 9).
