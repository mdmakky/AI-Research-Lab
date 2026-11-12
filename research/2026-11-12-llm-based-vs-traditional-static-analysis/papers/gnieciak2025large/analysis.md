---
key: gnieciak2025large
status: complete
evidence_basis: full-text
design: Head-to-head benchmark, 3 SAST tools (SonarQube, CodeQL, Snyk Code) vs 3 prompted LLMs (GPT-4.1, Mistral Large, DeepSeek V3)
dataset: 10 small author-prepared C# projects with seeded vulnerabilities (SQLi, XSS, secrets, command injection, weak crypto, outdated deps)
sample_size: 10 projects, 63 vulnerabilities, 3-10 files and 3,145-5,317 characters per project; single run per tool
metrics: Precision, recall, F1 (per-project, macro-averaged), false-positive ratio, execution time
main_finding: LLMs reach mean F1 0.75-0.80 vs 0.26-0.55 for SAST, driven by recall; LLMs mislocate lines and hallucinate outdated dependencies.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Large Language Models Versus Static Code Analysis Tools: A Systematic Benchmark for Vulnerability Detection

- Authors: Gnieciak, Damian; Szandala, Tomasz
- Year / venue: 2025, IEEE Access (published)
- DOI: 10.1109/access.2025.3635168 · URL: https://doi.org/10.1109/access.2025.3635168
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] A head-to-head quantitative and qualitative evaluation of three rule-based SAST tools (SonarQube, CodeQL, Snyk Code) and three LLMs on the GitHub Models platform (GPT-4.1, Mistral Large, DeepSeek V3) for vulnerability detection, measuring precision, recall, F1, latency and developer effort (p. 1–2).
- [A] Extends earlier work that compared GPT-3.5 Turbo and GPT-4o with SonarQube only (p. 4).

## 2. Research questions / hypotheses
- Not reported as formal RQs or hypotheses. [A] Stated contributions: a unified benchmark and protocol, a quantitative comparison, qualitative insight from "thematic analysis of model rationales and tool reports", and practitioner guidance (p. 2).

## 3. Methodology
- Research design: [V] Benchmark experiment: each tool/model runs once on each of 10 projects; every reported finding is manually checked against a reference list of known vulnerabilities (p. 6, p. 8).
- Approach / model / intervention: [V] LLMs accessed via GitHub Models API through the authors' tool ProjectAnalyzer, which concatenates all project files (.cs, .csproj, .sln) into a single prompt and converts the JSON answer to SARIF (p. 5). [V] System prompt asks the model to act as "a static code analysis engine", lists 10 vulnerability types (SQLi, XSS, command injection, insecure deserialization, auth, hard-coded secrets, input validation, outdated libraries, weak crypto, file handling) and requests a JSON array with rule, message, path, line and column fields (p. 7). Zero-shot only; no fine-tuning.
- Baselines or comparison conditions: [V] SonarQube, CodeQL, Snyk Code, all run with default configuration settings (p. 4, p. 8). [A] Snyk Code is described as using machine learning, i.e., a hybrid of ML and static analysis (p. 4, p. 9). Model and tool versions: not reported (GitHub Models endpoints named only by model name).

## 4. Dataset and sample
- Data source(s): [V] 10 C# projects "prepared" for the study, each with "a random number of vulnerabilities" from six categories: SQL injection, XSS, hard-coded secrets, command injection, weak encryption algorithms, deprecated dependencies (p. 5). [A] The abstract calls them "real-world C# projects" (p. 1). [I] The methods text and sizes (3,145–5,317 characters) suggest small purpose-built projects with seeded vulnerabilities rather than real-world software (based on p. 5–6).
- Sample size (N) and unit: [V] 10 projects, 3–10 files each, 3,145–5,317 characters, 1–13 vulnerabilities per project, 63 vulnerabilities in total (Table 3, p. 6). Unit of evaluation = reported finding matched to a known vulnerability.
- Sampling / selection method: [A] Project size (up to 10 files) chosen to match the most common change size in source-control history (p. 5). How vulnerabilities were chosen or inserted: not reported. CWE mapping: not reported.
- Data availability (public? link?): [V] ProjectAnalyzer code at https://github.com/Damian0401/ProjectAnalyzer (p. 1). [A] The abstract says an "open benchmark and JSON-based result harness" is released (p. 1); a separate dataset link is not given in the text.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Uniform execution environment; default configurations; execution time recorded in seconds to three decimals (p. 7–8). [V] LLM pricing (per 1M tokens): GPT-4.1 $2 in / $8 out; DeepSeek V3 $0.27 / $1.10; Mistral Large $2 / $6; context windows 1,047,576 / 64,000 / 32,000 tokens (p. 5–6). [V] SAST licence prices: SonarQube free Community / $65 per month Team; CodeQL $4 or $21 per user per month; Snyk Code from $25 per user per month (p. 5). Temperature, sampling settings, number of repetitions, hardware: not reported. Actual token usage or run cost: not reported.
- Code availability: [V] ProjectAnalyzer on GitHub (p. 1).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] TP = reported finding matching a known vulnerability (manually verified); FP = reported − TP; FN = known − TP; precision, recall and F1 computed per project and then averaged across projects (p. 6–7, p. 10). [V] Exception: for LLMs, wrong line/column locations were not counted against them (p. 6). [V] FP ratio (share of a tool's reports that are false) shown in Fig. 4 (p. 9). [V] Execution time per run (p. 7, p. 9).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): not reported. [V] When a tool reported nothing on a project, its precision is recorded as 0.000 and enters the average (e.g., SonarQube S04, S05, S08, S10) (p. 9).

## 7. Key findings
1. [V] Mean precision / recall / F1 (macro over 10 projects): SonarQube 0.567 / 0.187 / 0.260; CodeQL 0.625 / 0.284 / 0.386; Snyk Code 0.686 / 0.523 / 0.546; GPT-4.1 0.757 / 0.877 / 0.797; Mistral Large 0.783 / 0.783 / 0.753; DeepSeek V3 0.723 / 0.847 / 0.750 (Table 13, p. 10).
2. [V] Raw counts (reported / TP over 63 known vulnerabilities): SonarQube 15 / 13; CodeQL 26 / 21; Snyk Code 57 / 42; GPT-4.1 74 / 55; Mistral Large 61 / 48; DeepSeek V3 70 / 52 (summed from Tables 4–5, p. 8). [I] Pooled over all projects this gives precision/recall/F1 of about 0.87/0.21/0.33 (SonarQube), 0.81/0.33/0.47 (CodeQL), 0.74/0.67/0.70 (Snyk), 0.74/0.87/0.80 (GPT-4.1), 0.79/0.76/0.77 (Mistral), 0.74/0.83/0.78 (DeepSeek) — our arithmetic from Tables 4–5; pooled SAST precision is higher than the macro averages suggest.
3. [A] The LLM advantage comes from higher recall, attributed to reasoning over broader code context (p. 1, p. 12).
4. [A] SonarQube and CodeQL have the lowest FP ratios; DeepSeek V3 has the highest FP ratio; Snyk Code lies between SAST tools and LLMs, explained by its hybrid ML + static approach (p. 9).
5. [V] Execution time per project: CodeQL 185.9–213.1 s; SonarQube 30.2–63.9 s; Snyk Code 13.9–29.3 s; GPT-4.1 3.5–17.8 s; Mistral Large 10.2–67.3 s; DeepSeek V3 5.8–29.9 s (Table 6, p. 9). [A] Project size in this range does not substantially affect runtime (p. 8).
6. [A] All LLMs identified the correct file but always reported an incorrect line/column location, likely due to BPE tokenisation (p. 11).
7. [V] LLMs hallucinated outdated-dependency findings for current library versions (e.g., Mistral Large flagged Microsoft.Data.Sqlite 9.0.5; GPT-4.1 flagged Newtonsoft.Json 13.0.3) (Table 14, p. 12).
8. [A] Recommendation: LLMs for early, broad triage during development; deterministic SAST for high-assurance audits in critical systems (p. 1, p. 12).

## 8. Limitations stated by the authors
- [A] LLMs cannot give correct line/column locations, which may preclude their use in SARIF-based pipelines (p. 11–12).
- [A] LLMs hallucinate findings such as outdated dependencies, which classical tools avoid through maintained deprecation lists (p. 11–12).
- [A] Higher sensitivity of LLMs comes with more false positives, which can cause alert fatigue (p. 11–12).
- [A] GPT-4.1 not publicly accessible, hence the use of GitHub Models for equal conditions (p. 5).
- No dedicated threats-to-validity section (p. 11).

## 9. Limitations we identified
- [I] Tiny, author-built benchmark: 10 projects, 63 vulnerabilities, each project ≤5,317 characters and ≤10 files (p. 6). The whole project fits easily in one prompt, which favours LLMs and does not reflect real repository scale. The "real-world" label in the abstract (p. 1) is not supported by the dataset description (p. 5).
- [I] Lenient scoring asymmetry: LLM findings count as TP even with wrong line/column locations (p. 6), while SAST tools are judged normally. This inflates LLM precision/recall relative to SAST.
- [I] Averaging choice penalises SAST: projects where a tool reports nothing get precision 0.000 and are averaged in (p. 9). Pooled counts (our calculation from Tables 4–5, p. 8) give SAST precision 0.74–0.87 vs LLM 0.74–0.79, and Snyk pooled F1 ≈ 0.70 near the LLMs. The FP-ratio ranking (DeepSeek highest) also depends on per-project averaging; pooled, GPT-4.1 has the most FPs (19) and Snyk's FP share (15/57) is similar to the LLMs'.
- [I] Single run per LLM with no temperature reported; LLM nondeterminism is not addressed, so results may not replicate.
- [I] Default SAST configurations only; e.g., SonarQube default profiles are not security-focused, and "deprecated dependencies" are normally the job of SCA tools rather than SAST, which disadvantages SonarQube/CodeQL on one of six categories.
- [I] Possible contamination: small synthetic C# examples of classic vulnerabilities resemble training data; not discussed.
- [I] Abstract claims measurement of "developer effort required to vet true positives" (p. 1) and contributions mention thematic analysis of rationales (p. 2); neither is reported as a measured result. Per-category (CWE) results are not given.
- [I] Run cost in dollars is not reported even though per-token prices are listed (p. 5–6).

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Same authors created the projects, the prompt and the matching; lenient location rule for LLMs only (p. 6); no blinding of manual TP verification.
- External (generalisability of sample/context): [I] One language (C#), six vulnerability categories, very small projects; cloud-hosted frontier LLMs only; three SAST tools with default rules.
- Construct (do metrics measure the concept?): [I] Detection without correct location is counted as success for LLMs; macro-average with zero-precision imputation distorts precision.
- Statistical conclusion (power, multiple comparisons, variance): [I] N = 10 projects, 63 vulns, single runs, no tests or CIs; per-project F1 varies widely (e.g., S04 with 1 vulnerability).
- Reproducibility (data/code/setup reported?): [I] Harness code public (p. 1); prompt published (p. 7); model versions, temperature and dataset link not reported.

## 11. Future research directions
- Stated by authors [A]: study prompt engineering effects; build a hybrid using classical tools and LLMs to prioritise and verify findings (p. 11).
- Suggested by us [I]: larger real-world C# corpora with CVE ground truth; strict location-aware scoring for all tools; repeated LLM runs; per-CWE breakdown; measured triage effort and cost per true positive.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4.
- How it informs our work [I]: A rare head-to-head comparison of commercial-grade SAST with frontier LLMs, reporting full precision/recall/F1 and runtime, in an under-studied language (C#). Its LLM-favourable result is useful but rests on a tiny, purpose-built benchmark and asymmetric scoring, so it should be treated as weak evidence and contrasted with larger real-world studies.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Macro mean F1: GPT-4.1 0.797, Mistral Large 0.753, DeepSeek V3 0.750 vs Snyk Code 0.546, CodeQL 0.386, SonarQube 0.260 on 10 C# projects (63 vulns) | 10 | V | weak |
| RQ1 | Macro mean recall: LLMs 0.783–0.877 vs SAST 0.187–0.523; macro precision LLMs 0.723–0.783 vs SAST 0.567–0.686 | 10 | V | weak |
| RQ1 | Pooled from raw counts, SAST precision 0.74–0.87 vs LLM 0.74–0.79 and Snyk F1 ≈ 0.70; macro averaging with zero-precision imputation widens the gap | 8–9 | I | weak |
| RQ2 | LLM findings counted as TP despite wrong line/column; SAST tools on default configs; single run; 10 author-prepared small projects | 5–6, 8 | V | moderate |
| RQ3 | Runtime per project: CodeQL ~186–213 s, SonarQube ~30–64 s, Snyk ~14–29 s, GPT-4.1 ~3.5–18 s, Mistral ~10–67 s, DeepSeek ~6–30 s | 9 | V | weak |
| RQ3 | Authors recommend a hybrid: LLMs for early broad triage, deterministic SAST for high-assurance audits (no hybrid tested) | 1, 11–12 | A | weak |
| RQ3 | LLMs always mislocate line/column and hallucinate outdated-dependency findings, limiting explainability and SARIF integration | 11–12 | A | weak |
| RQ4 | Evidence is for C# web-style vulnerabilities (SQLi, XSS, secrets, command injection, weak crypto, outdated deps); no per-category results | 5 | V | weak |
| RQ5 | Open problems: localisation precision, hallucinated findings, false-positive noise, prompt sensitivity | 11–12 | A | weak |

## 14. Key quotes
> "All of the large language models tested were unable to determine it correctly." (p. 11)

> "Each of project has a random number of vulnerabilities," (p. 5)

> "The only exception to this rule was the location region of the results produced by the large language models." (p. 6)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–13) including all result tables; Figures 1–7 are images not in the text layer and were not needed because Tables 4–13 carry the numbers.
- Source version: arXiv v1 (2508.04448, 6 Aug 2025). Published version: IEEE Access 2025 (DOI 10.1109/access.2025.3635168, from metadata). The arXiv PDF uses the IEEE Access template with placeholder DOI; numbers may differ from the published version — check before final citation if possible.
- Uncertainties: whether the projects are synthetic (author-written) or derived from real software; the text says "prepared" and "random number of vulnerabilities" (p. 5), the abstract says "real-world" (p. 1). The pooled metrics in section 7 item 2 are our arithmetic, not the authors'. The future-work subsection refers to "this thesis" (p. 11), suggesting a thesis origin.
