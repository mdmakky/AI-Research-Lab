---
key: du2026reducing
status: complete
evidence_basis: full-text
design: Industrial empirical study at Tencent: interviews + offline evaluation of LLM prompting, hybrid LLM+static-analysis and DL methods for SAT alarm triage
dataset: 433 alarms from Tencent's proprietary SAT BkCheck on AMS codebases (mostly C/C++), Sep 2024-Jun 2025; NPD, OOB, DBZ bug types; confidential
sample_size: 433 alarms (328 FP, 105 TP); 5 interviewees
metrics: Accuracy, precision, recall, F1 (real bug = positive); FPR_P / FPR_R (precision/recall on false alarms); time and USD per alarm
main_finding: Hybrid LLM4PFA removes 94-98% of false alarms (recall of real bugs 0.75-0.88) at $0.0025-$0.12 per alarm; prompting-only and DL baselines are far weaker.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Reducing False Positives in Static Bug Detection with LLMs: An Empirical Study in Industry

- Authors: Du, Xueying; Feng, Jiayi; Zou, Yi; Xu, Wei; Ma, Jie; Zhang, Wei; Liu, Sisi; Peng, Xin; Lou, Yiling
- Year / venue: 2026, Proceedings of the IEEE/ACM 48th International Conference on Software Engineering: Software Engineering in Practice (published)
- DOI: 10.1145/3786583.3786910 · URL: https://doi.org/10.1145/3786583.3786910
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

**Version note:** our text is arXiv 2601.18844 **v1 (26 Jan 2026)** in a generic ACM template ("Conference'17, July 2017, Washington, DC, USA" running header, p. 2). It is not the ICSE-SEIP 2026 camera-ready recorded in metadata; final numbers may differ.

**Scope note:** the bug types are **general static-analysis bug classes, not classic security-vulnerability classes**: Null Pointer Dereference (NPD), Out-of-Bounds (OOB) and Divide-by-Zero (DBZ), reported by Tencent's quality-oriented SAT BkCheck (p. 2, p. 4). The paper itself calls them "memory safety bugs" (p. 10) and does not map them to CWEs or rate exploitability. [I] They overlap with CWE-476 / CWE-125/787 / CWE-369, so the study is indirect evidence for security-vulnerability triage; weight it accordingly.

## 1. Research objective
- [A] Find out how well LLM-based false-alarm reduction techniques work on real proprietary enterprise code and an enterprise-customised static analyser, since earlier work used open-source or synthetic benchmarks (p. 1–2).

## 2. Research questions / hypotheses
- [V] RQ1: prevalence of false positives in industrial practice; RQ2: effectiveness of LLM-based techniques (2.a plain LLMs, 2.b advanced prompting, 2.c hybrid LLM + static analysis, 2.d vs traditional learning-based methods); RQ3: time and money costs; RQ4: per-bug-type breakdown and failure-case analysis (p. 4–6).

## 3. Methodology
- Research design: [V] Industrial empirical study: developer interviews (RQ1) plus offline evaluation of LLM and DL techniques on a labelled set of historical alarms (RQ2–RQ4) (p. 4–6).
- Approach / model / intervention: [V] LLMs: GPT-4o, Claude-Opus-4, Qwen-3-Coder, DeepSeek-R1 (p. 5). Prompting: basic, Chain-of-Thought, few-shot, bug-type augmentation (p. 5). Hybrid LLM + static analysis: LLM4SA (LLM sees the warning plus callers/callees and hundreds of lines of context) and LLM4PFA (static-analysis path constraints plus agent-driven feasibility reasoning) (p. 5). [V] IRIS and LLMDFA were excluded: IRIS needs a compilable repository for CodeQL, LLMDFA does not support the bug types (p. 5).
- Baselines or comparison conditions: [V] The SAT alone (all alarms reported); DL methods Devign, ReGVD (GNN), LLMAO, LineVul (fine-tuned PLMs), applied with models trained on their original datasets, without retraining (p. 5–6).

## 4. Dataset and sample
- Data source(s): [V] Alarms from BkCheck, Tencent's proprietary SAT (no compilation needed; rules include null dereference, logic defects, divide-by-zero, memory leaks), on the Advertising and Marketing Services (AMS) repositories, Sep 2024–Jun 2025; labels from Tencent's two-round routine code review (p. 3–4). [A] Data are "primarily" C/C++ (p. 10).
- Sample size (N) and unit: [V] 433 alarms: NPD 136 (107 FP / 29 TP), DBZ 158 (139 / 19), OOB 139 (82 / 57); total 328 FP / 105 TP (Table 1, p. 4). [V] Interviews: 5 participants (2 developers, 3 reviewers, >5 years' experience) (p. 4).
- Sampling / selection method: [V] All records of the three most frequent categories (≈52%, 24%, 10% of warnings, 86% total) in the period, minus deprecated code, incomplete context, unresolved cases and duplicates (p. 4). How many records were removed: not reported.
- Data availability (public? link?): [V] Dataset not released (confidentiality); methods and detailed results in a replication package at https://github.com/LLM4SFPR/static-bug-false-positives-reduction-in-practice (p. 2, p. 11).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Each LLM query run three times per case with majority vote (p. 6). DL models used as trained on their original datasets (p. 6). Temperature, prompt texts, few-shot example source and context lengths: not reported in the paper (prompts said to be in the replication package, p. 5). [V] IRB approval for the interviews (p. 4).
- Code availability: [V] Replication package (p. 2, p. 11).

## 6. Evaluation metrics
- [V] Accuracy, precision, recall, F1 with the real bug as positive class; FPR_P = TN/(TN+FN) and FPR_R = TN/(TN+FP), i.e., precision and recall on false alarms (FPR_R = share of false alarms removed) (p. 6).
- [V] Cost: average response time (s) and API cost (USD) per alarm (p. 5–6, p. 8).
- Statistical testing: not reported (no significance tests, CIs or variance across the three runs).

## 7. Key findings
1. [V] SAT alone: 76% of alarms in the final dataset are false (328/433) (p. 6). [A] Counting excluded records, the false-positive rate exceeds 90% (p. 6); how this was computed is not reported.
2. [A] Interviews: every alarm is manually reviewed, false alarms get a second review; about 10 minutes per round, 10–20 minutes per alarm (p. 6).
3. [V] Hybrid LLM4PFA: accuracy 0.93–0.94, precision 0.83–0.93, recall 0.75–0.88, F1 0.83–0.86, FPR_R 0.94–0.98 across the four LLMs (e.g., GPT-4o: P 0.93, R 0.75, FPR_R 0.98; Claude-Opus-4: P 0.83, R 0.88, FPR_R 0.94) (Table 2, p. 8).
4. [V] Hybrid LLM4SA: accuracy 0.86–0.92, recall 0.65–0.86, FPR_R 0.84–0.96 (Table 2, p. 8).
5. [V] Prompting-only LLMs are much weaker: basic prompt accuracy 0.40–0.55, precision 0.26–0.29, FPR_R 0.26–0.52; few-shot is the best prompting strategy (accuracy 0.50–0.72, FPR_R 0.43–0.72); CoT is weakest (FPR_R 0.24–0.40) (Table 2, p. 8).
6. [V] DL baselines: Devign accuracy 0.44, ReGVD 0.36 (recall 0.87 but FPR_R 0.19), LLMAO 0.36, LineVul 0.76 only because it labels every alarm a false positive (precision/recall 0.00) (Table 3, p. 8; p. 7).
7. [V] Cost per alarm, LLM4PFA: 12.6–58.3 s and $0.0025–$0.12 (Claude-Opus-4 most expensive); overall range for all LLM methods 2.1–109.5 s and $0.0011–$0.12 (Table 4, p. 8). Cost per project or per scan: not reported.
8. [V] By bug type, most methods do best on DBZ and worst on NPD (p. 8; Fig. 3, p. 9).
9. [V] Failure cases: functions in all-methods-failed cases are 95.6 lines longer than the dataset average and contain 21 more conditional statements (p. 9).
10. [A] LLM explanations cut the time to validate a warning from about 10 to about 3 minutes (p. 10); how this was measured is not reported.

## 8. Limitations stated by the authors
- [A] Recall stays below the 90% enterprise threshold, so manual review is still needed; LLMs can replace at least one review round (p. 9).
- [A] Long-context and complex cascaded-constraint reasoning remain weak; strong results partly reflect short code fragments in this analyser's warnings (p. 9–10).
- [A] Study focuses on memory-safety bugs; other bug types are an open question (p. 10).
- [A] LLM randomness; majority voting recommended (p. 10).
- [A] LLMs can only filter, not find bugs beyond the analyser's coverage (p. 10).
- [A] Label reliability, limited dataset scope (433 cases, 10 months), and one company, mostly C/C++ (p. 10).

## 9. Limitations we identified
- [I] Conflict of interest: LLM4PFA, the winning method, is the authors' own earlier work (ref [15], same first and last authors, p. 3, p. 11), and the dataset is private, so the result cannot be checked independently.
- [I] Industry conflict of interest: four of the nine authors (Wei Xu, Jie Ma, Wei Zhang, Sisi Liu) are Tencent employees with Tencent addresses (p. 1), and the study evaluates Tencent's own analyser (BkCheck) on Tencent data (p. 1–2). Funding: not reported (no acknowledgements section found). Based on the author affiliations and contact list on p. 1.
- [I] Bug classes are reliability/memory-safety bugs from a quality-oriented analyser, not security vulnerabilities from a SAST tool; transfer to RQ1–RQ4 on vulnerabilities is indirect.
- [I] The DL comparison is unfair: Devign, ReGVD, LineVul are function-level vulnerability detectors (and LLMAO a fault localiser) used without retraining on alarm triage; poor results show domain shift, not that DL triage cannot work.
- [I] Model identity is unclear: references cite Claude 3.5 Sonnet for "Claude-Opus-4" [8], DeepSeek-Coder-V2 for "DeepSeek-R1" [13], GPT-4 Turbo for "GPT-4o" [21] and Qwen2.5-Coder-32B for "Qwen-3-Coder" [45] (p. 11–12).
- [I] Prompting-only precision (0.26–0.29) is barely above the base rate of real bugs (105/433 ≈ 0.24, our arithmetic from Table 1), so plain LLMs add little signal here.
- [I] Few-shot examples were "manually constructed" (p. 10); whether they came from the evaluation set is not reported, so leakage cannot be ruled out.
- [I] The ">90%" false-positive figure and the "10 → 3 minutes" saving lack described measurement.
- [I] The text is the v1 preprint, not the peer-reviewed camera-ready.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Author-built method wins; filtering of records with incomplete context may remove the hardest cases; possible few-shot leakage.
- External (generalisability of sample/context): [I] One company, one business line, one proprietary analyser, three bug types, mostly C/C++ (p. 4, p. 10).
- Construct (do metrics measure the concept?): [I] Labels come from routine review (p. 4); the authors argue true positives are unlikely to be discarded (p. 4), but this is not tested.
- Statistical conclusion (power, multiple comparisons, variance): [I] N=433 with only 105 TPs (19 for DBZ); no tests; differences of 0.01–0.02 between LLM4PFA backbones are within noise.
- Reproducibility (data/code/setup reported?): [V] Code and results public, data confidential (p. 2). [I] Cannot be replicated on the same data.

## 11. Future research directions
- Stated by authors [A]: knowledge-enhanced LLMs (e.g., RAG of historical cases); decomposing complex constraint reasoning and hybrid pipelines for long context (p. 10); using LLMs to find bugs beyond analyser coverage (p. 10); more business lines and languages (p. 10).
- Suggested by us [I]: replicate on security-relevant SAST alerts (CWE-tagged) and on public industrial-like data; independent evaluation of LLM4PFA.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ3, RQ4, RQ5.
- How it informs our work [I]: Real-world industrial evidence that hybrid static analysis + LLM post-filtering beats prompting-only LLMs and off-the-shelf DL detectors for alarm triage, with per-alarm cost. Relevance is medium rather than high because the bugs are general static bugs, not security vulnerabilities, and the data are private.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1/RQ3 | Industrial SAT alone: 76% of alarms false (328/433); hybrid LLM4PFA removes 94–98% of false alarms, keeping 75–88% of real bugs (precision 0.83–0.93) | p. 6, p. 8 | V | moderate |
| RQ3 | Hybrid (LLM4SA, LLM4PFA; accuracy 0.86–0.94) beats prompting-only LLMs (accuracy 0.40–0.72) on the same alarms | p. 8 | V | moderate |
| RQ1 | Off-the-shelf DL detectors (Devign, ReGVD, LLMAO, LineVul) fail at alarm triage (accuracy 0.36–0.44; LineVul labels all as FP) | p. 7–8 | V | weak |
| RQ3 | Cost per alarm: LLM4PFA 12.6–58.3 s, $0.0025–$0.12; all LLM methods 2.1–109.5 s, $0.0011–$0.12 vs 10–20 min manual | p. 6, p. 8 | V | moderate |
| RQ4 | Best on Divide-by-Zero, worst on Null Pointer Dereference; failures tied to long functions and many conditionals | p. 8–9 | V | weak |
| RQ5 | Recall below 90% enterprise threshold; LLMs can only filter, not find bugs beyond analyser coverage | p. 9–10 | A | moderate |
| RQ2 | Scope: general bug classes (NPD/OOB/DBZ), proprietary C/C++ data, author-built winning method | p. 4, p. 10 | I | weak |

## 14. Key quotes
> "hybrid techniques of LLM and static analysis eliminate 94–98% of false positives with high recall" (p. 1)
> "recall remains below the enterprise-expected threshold of 90%, indicating that some degree of manual review is still necessary" (p. 9)
> "their capacity to discover new bugs remains bounded by the detection capabilities of static analyzers themselves" (p. 10)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–10 text, pp. 11–12 references). Fig. 3 (per-bug-type bars, p. 9) is garbled in the text layer; only the prose summary of it is cited.
- Version: arXiv v1 preprint with placeholder conference header; metadata records the ICSE-SEIP 2026 version. Re-check numbers against the published version if it becomes available.
- Uncertainties: exact model versions (reference mismatch, see §9); number of records removed by filtering; temperature and prompt content not in the paper.
