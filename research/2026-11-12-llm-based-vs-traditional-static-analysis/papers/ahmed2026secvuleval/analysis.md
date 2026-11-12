---
key: ahmed2026secvuleval
status: complete
evidence_basis: full-text
design: Benchmark construction + empirical evaluation of 5 LLMs in a multi-agent detection pipeline (manual statement-level judging)
dataset: SecVulEval (NVD C/C++ CVEs 1999-2024, 707 projects, 145 CWEs); detection evaluated on 300-function subset from Top-25 CWEs
sample_size: 25,440 functions (10,998 vulnerable / 14,442 non-vulnerable; 5,867 CVEs); detection experiment 300 functions (~120 vulnerable)
metrics: Precision, recall, F1 at function level and statement level (statement TP requires correct reasoning); context-identification accuracy
main_finding: Best LLM (Claude-3.7-Sonnet) reaches only 23.83% statement-level F1 on real C/C++ CVEs; function-level F1 at most 53.89%; no static or DL baselines.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# SecVulEval: Context-Aware Benchmarking of LLMs for Vulnerability Detection

- Authors: Ahmed, Md Basim Uddin; Harzevili, Nima Shiri; Shin, Jiho; Pham, Hung Viet; Wang, Song
- Year / venue: 2026, Proceedings of the 3rd ACM International Conference on AI-Powered Software (published)
- DOI: 10.1145/3805760.3814932 · URL: https://doi.org/10.1145/3805760.3814932
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

> Version note: the text analysed is the arXiv preprint 2505.19828v1 (26 May 2025), titled "SecVulEval: Benchmarking LLMs for Real-World C/C++ Vulnerability Detection", marked "Preprint. Under review." (p. 1). The published AIware 2026 version may differ in title, numbers and content. See Analyst notes.

## 1. Research objective
- [A] Build a C/C++ vulnerability benchmark with statement-level labels, rich metadata and program context (function arguments, external functions, type declarations, globals, execution environment), and use it to test how well current LLMs detect and localise real vulnerabilities (p. 1, p. 2).
- [A] Motivation: existing datasets (BigVul, CVEFixes, DiverseVul, PrimeVul, MegaVul, etc.) are function-level only, lack context, contain duplicates/mislabels, and line-level labels (BigVul, CVEFixes, SVEN) are line fragments rather than statements (p. 2, p. 3).

## 2. Research questions / hypotheses
- No formal RQs or hypotheses. Two experiments: (1) LLM vulnerability detection at function and statement level; (2) LLM identification of the context needed for detection (p. 6, p. 7).

## 3. Methodology
- Research design: benchmark construction from NVD + GitHub commits, followed by an empirical evaluation of 5 LLMs inside a multi-agent pipeline, with manual judging of statement-level outputs (p. 4-p. 8).
- Approach / model / intervention: five-agent pipeline: Normalization Agent (tree-sitter AST, no LLM), Planning Agent (function summary + checklist of up to 8 red-flag cues), Context Agent (asks for up to 6 external symbols per round, max 3 rounds; definitions fetched with tree-sitter), Detection Agent (verdict + vulnerable statements + reason), Validation Agent (agrees or disagrees; Detection reruns up to 3 times) (p. 7, p. 14-p. 16). [A] Authors claim it is the first LLM multi-agent pipeline applied to vulnerability detection (p. 7).
- Models: Qwen2.5-Coder-32B-Instruct, Deepseek-Coder-33B-Instruct, Codestral-22B-v0.1 (open weights, HuggingFace), GPT-4.1, Claude-3.7-Sonnet (p. 8).
- Baselines or comparison conditions: only the 5 LLMs are compared. No static-analysis tool, no fine-tuned DL/PLM detector, no single-LLM (non-agent) baseline, and no with/without-context ablation for detection (not reported).

## 4. Dataset and sample
- Data source(s): NVD CVEs (non-REJECTED) for products previously identified as C/C++ in BigVul, CVEFixes and PrimeVul, plus NVD keyword search ("C++", "C language", ".cpp"); only CVEs with an NVD "Patch" reference to a commit in the original (non-forked) repository; commit data via GitHub REST API (p. 4).
- Sampling / selection method: non-C/C++ files removed; only single-commit fixes kept (43 multi-commit CVEs dropped); files with no function changes removed; tangled changes filtered by keeping only functions solely modified in a file or named in the CVE/commit message; de-duplication by md5 of whitespace-normalised function text (p. 5). Detection experiment: 300 functions randomly selected from the Top-25 CWE types, manually validated; 120 of them vulnerable (p. 8, p. 12, p. 13).
- Sample size (N) and unit: 25,440 functions = 10,998 vulnerable + 14,442 non-vulnerable; 5,867 CVEs, 707 projects, 145 CWEs, CVEs from 1999-2024 (p. 6, p. 9). Function size 4-541 lines (2.5-97.5 percentile), median 44 lines; on average about 4 statements deleted and 6 added per function (p. 6). Linux alone contributes 1,920 CVEs and 2,793 vulnerable functions (p. 5).
- Non-vulnerable functions: the exact definition (fixed versions of vulnerable functions vs. other unchanged functions) is not stated explicitly. The text says both "vulnerable version" and "fixed version" copies are kept for each changed function (p. 5).
- Context labels: generated automatically by GPT-4.1 from CWE, function body, patch, commit message and CVE description. A manual check of 100 random samples (4 excluded as N/A) gave 82.98 ± 9.68% accuracy (99% CI) (p. 6).
- Data availability: dataset on HuggingFace (arag0rn/SecVulEval) and code on GitHub (basimbd/SecVulEval) (p. 3); "friendly license" for research and commercial use (p. 12).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: pass@1, temperature 0.1; Intel Xeon Gold 6442Y CPU, 4 x NVIDIA L40S GPUs, 250 GiB RAM; open models via transformers.pipeline (p. 8, p. 17). Prompts for all four LLM agents are given verbatim. They were rewritten to stress *defensive* research after models refused to answer (p. 13-p. 16). Function and AST inputs "could be truncated if too long" (p. 14); the truncation limit is not reported.
- Statement-level TP rules (manual): exact vulnerable statements with correct reasoning; or at least one of several fix locations; or correct statements plus at most two unrelated ones; or only the sink statement / sink + source with correct reasoning (p. 8). Function level is judged automatically from the `is_vulnerable` field (p. 8).
- Number and independence of manual raters, and inter-rater agreement: not reported.
- Cost/time: open models take 4.97-7.99 minutes per function in total (Codestral 4.97, Qwen 6.03, Deepseek 7.99) (p. 17). Time for the proprietary models and API cost are not reported (p. 17).
- Code availability: GitHub repository (p. 3).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: precision, recall and F1 at function level (is the function vulnerable?) and statement level (are the vulnerable statements identified with correct reasoning?). A function-level TP with wrong reasoning is defined as a statement-level FN (p. 7). Context identification: accuracy per context type versus dataset ground truth, which is itself GPT-4.1-generated (p. 6, p. 7, p. 9).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): one-sided Mann-Whitney U tests compare the function length of detected vs. missed vulnerable functions (p. 12, p. 13). The detection metrics have no confidence intervals or significance tests, and repeated runs are not reported.

## 7. Key findings
1. Statement-level detection is poor for all models: F1 = Claude-3.7-Sonnet 23.83%, GPT-4.1 22.38%, Codestral-22B 15.31%, Qwen2.5-Coder-32B 13.57%, Deepseek-Coder-33B 7.14% — [V] (p. 8, Table 3).
2. Function-level F1: Claude 53.89%, GPT-4.1 52.25%, Codestral 46.61%, Deepseek 45.71%, Qwen 35.20%. Function-level precision is only 35.48-47.41% for every model — [V] (p. 8, Table 3).
3. The proprietary models are more "aggressive": function-level recall is 75.63% (Claude) and 73.11% (GPT-4.1), but precision is 41.86% and 40.65%, lower than Codestral (47.41%) and Deepseek (45.16%). Of 300 samples (120 vulnerable), GPT-4.1 and Claude flagged 214 and 215 as vulnerable vs. 116-124 for the open models — [V] (p. 8, p. 13).
4. Statement-level precision is 5.65-15.35% for all models, i.e. most flagged statements/reasons are wrong — [V] (p. 8, Table 3).
5. Detected vulnerable functions are much shorter than missed ones: median 14-33 LoC detected vs. 64-71 LoC missed; one-sided Mann-Whitney U p = 0.000197-0.0168 for all five models — [V] (p. 12, p. 13, Table 5).
6. Over-detection concentrates on CWE-476 (NULL dereference, flagged even when an explicit null check exists), CWE-416 (any `free()`/`kfree()` treated as use-after-free) and CWE-190 (arithmetic flagged as overflow without analysis), especially for GPT-4.1 and Claude. This is qualitative, from manual validation; no counts are given — [A] (p. 13).
7. LLMs identify the needed context poorly. The best per type is Claude (external functions 37.00%, type definitions 41.33%, globals 34.53%). Function-argument accuracy is 0-5.31% for all models, and no model identified any environment-level context (1.5% of all contexts) — [V] (p. 9, Table 4).
8. GPT-4.1 identifies the required context with 82.98 ± 9.68% accuracy when given the patch, CVE and commit message. This is the dataset-construction setting, not detection — [V] (p. 6).
9. SecVulEval has 0.0% duplicates vs. 18.9% (CVEFixes), 12.7% (BigVul) and 3.3% (DiverseVul) as reported by PrimeVul. The SecVulEval figure is the authors' own; the others are cited from their ref. [5] — [V] (p. 3, Table 1).

## 8. Limitations stated by the authors
- [A] Context labels were produced by an LLM; manual validation covered only 100 samples; "relevant context" is subjective; repository-wide / transitive context is not covered (p. 12).
- [A] Manual statement-level judging is subjective and labour-intensive, which limits scale (p. 12).
- [A] Only the largest runnable size of each model was evaluated; conclusions may not hold for smaller sizes (p. 12).
- [A] Multi-commit fixes were excluded for simplicity (p. 5).
- [A] The dataset could be misused to train models to exploit vulnerabilities (p. 12).

## 9. Limitations we identified
- [I] There is no non-LLM baseline at all (no SAST tool, no fine-tuned DL/PLM model, no single-prompt LLM). So the paper cannot say whether the multi-agent design helps or hurts, or how LLMs compare with traditional tools. Based on §3/§5 above.
- [I] The statement-level recall in Table 3 appears not to follow the stated definition. We reconstructed integer counts from Table 3 and the flag counts on p. 13 (e.g. Claude: 215 flagged, 90 function-level TP, 119 positives, 33 statement-level TP). Every reported statement-level recall is reproduced exactly as TP_stat / (TP_stat + function-level FN). That means "right function, wrong reasoning" cases were not counted as FN, contrary to the definition on p. 7. Under the stated definition, Claude's statement-level recall would be about 27.7% (33/119), not 53.23%, and its F1 about 19.8%, not 23.83%. The same pattern holds for all five models (GPT-4.1: about 26.1% vs. 49.21%). This is our arithmetic on the paper's tables (p. 8, p. 13). It makes the headline numbers optimistic, not pessimistic.
- [I] The implied number of vulnerable functions differs by model (119-126), although the paper says 120 of 300 are vulnerable (p. 13). This suggests unreported per-model exclusions (e.g. failed outputs). Same reconstruction as above.
- [I] The detection evaluation uses only 300 functions (about 1.2% of the benchmark), drawn from Top-25 CWEs only, with no uncertainty reported. Gaps of a few points between models (e.g. Claude vs. GPT-4.1, 23.83% vs. 22.38%) are probably within sampling noise. Based on p. 8.
- [I] Experiment 2 is circular: the context "ground truth" was generated by GPT-4.1 (p. 6), and GPT-4.1 is also one of the evaluated models (p. 9). This makes the context accuracies hard to interpret.
- [I] The task differs from SAST use. The pipeline gets one function plus LLM-requested definitions, not the whole repository or build. The results describe LLM review of single functions, not project-scale scanning.
- [I] The 300-sample set is 40% vulnerable, far more than in real codebases, so precision would likely drop further in deployment. This rests on the 120/300 count (p. 13).
- [I] Data contamination is not discussed: CVEs up to 2024 and their public fixes may be in the training data of all five models, and there is no time-split analysis.

## 10. Threats to validity
- Internal (confounds, leakage, selection): the manual judging rules are lenient (sink-only counts as TP; up to two extra statements allowed) (p. 8). The number of raters and their agreement are not reported. There is also the recall inconsistency in §9. Heuristics reduce label noise, but noise in the vulnerability labels is never measured; only the context labels were validated (p. 5, p. 6). De-duplication removes exact duplicates only (p. 5).
- External (generalisability of sample/context): C/C++ only. Linux is a large share (2,793 of 10,998 vulnerable functions) (p. 5). The evaluation covers only Top-25 CWEs and 300 samples (p. 8), and five specific LLM versions at temperature 0.1 (p. 8).
- Construct (do metrics measure the concept?): "correct reasoning" is a human judgement with no stated protocol beyond the four rules (p. 8). Function-level detection is judged without checking whether the stated reason is right (p. 7, p. 8).
- Statistical conclusion (power, multiple comparisons, variance): only one run per model is reported, with no confidence intervals or tests on Table 3. The Mann-Whitney tests run across five models without multiple-comparison correction, but all p < 0.017, so they are likely robust (p. 13).
- Reproducibility (data/code/setup reported?): the dataset, code and full prompts are released (p. 3, p. 14-p. 16), and hardware and temperature are reported (p. 8, p. 17). Whether the manual judgements for the 300 samples are released is not stated.

## 11. Future research directions
- Stated by authors [A]: use the statement-level and context labels to train and evaluate detection models (p. 10); test smaller model sizes (p. 12); "advancing statement-level detection is essential" (p. 9).
- Suggested by us [I]: run SAST tools (e.g. CodeQL, Cppcheck) and fine-tuned DL detectors on the same 300-sample subset; report statement-level recall under the stated definition with confidence intervals; compare the multi-agent pipeline against a single prompt, with and without context; split by CVE date to check for contamination.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2 (benchmark quality, granularity, duplication), RQ4 (C/C++, CWE-specific over-detection, function length), RQ5 (context, localisation, false positives). Indirectly RQ3 (agentic LLM pipeline with AST/tree-sitter context; execution time) and RQ1 (absolute effectiveness of LLMs alone, no head-to-head comparison).
- How it informs our work [I]: strong evidence that function-level LLM scores overstate real capability. When the correct root cause is required, F1 drops by more than half. Useful for the "evaluation realism" argument and for CWE-level weaknesses (false alarms on CWE-476/416/190). It cannot answer RQ1 directly because there is no SAST or DL comparison.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Best LLM (Claude-3.7-Sonnet, multi-agent) reaches 23.83% statement-level F1 and 53.89% function-level F1 on real C/C++ CVEs; function-level precision ≤47.41% for all 5 LLMs; no SAST/DL baseline | p. 8 | V | moderate |
| RQ2 | Requiring correct vulnerable statements + reasoning cuts F1 by more than half vs. function-level labels (e.g. GPT-4.1 52.25% → 22.38%) | p. 8 | V | moderate |
| RQ2 | SecVulEval: 25,440 de-duplicated C/C++ functions, 5,867 CVEs, 145 CWEs, statement-level + context labels; prior datasets have up to 18.9% duplicates | p. 3, p. 6 | V | moderate |
| RQ2 | Statement-level recall appears computed without counting wrong-reasoning cases as FN; under the stated definition Claude's recall would be ~27.7% (not 53.23%) and F1 ~19.8% | p. 7, p. 8, p. 13 | I | moderate |
| RQ4 | All 5 LLMs detect short functions and miss long ones (median 14-33 vs. 64-71 LoC; Mann-Whitney p ≤ 0.0168) | p. 13 | V | moderate |
| RQ4 | GPT-4.1 and Claude over-flag CWE-476, CWE-416 and CWE-190 (e.g. null deref despite explicit null check) | p. 13 | A | weak |
| RQ5 | LLMs identify required context poorly (≤41.33% per type; function arguments ≤5.31%; environment context 0%) | p. 9 | V | moderate |
| RQ3 | Multi-agent pipeline with open 22-33B models costs ~5-8 min per function on 4 x L40S | p. 17 | V | moderate |

## 14. Key quotes
> "The best-performing Claude-3.7-Sonnet model achieves 23.83% F1-score for detecting vulnerable statements with correct reasoning, with GPT-4.1 closely behind." (p. 1)

> "If the model correctly identifies a function as vulnerable, but the reasoning is incorrect, we consider this a True Positive for function-level detection but a False Negative for statement-level detection" (p. 7)

> "every model is significantly more successful at recognizing vulnerabilities in compact, shorter functions and consistently misses them in the longer ones." (p. 13)

## Analyst notes
- Reading coverage: the whole preprint was read (pp. 1-17), including appendices A-E (limitations, failure analysis, prompts, execution time). References were skimmed.
- Version / identity: `metadata.json` describes the AIware 2026 proceedings paper "SecVulEval: Context-Aware Benchmarking of LLMs for Vulnerability Detection" (DOI 10.1145/3805760.3814932). The PDF is arXiv 2505.19828v1, titled "SecVulEval: Benchmarking LLMs for Real-World C/C++ Vulnerability Detection", with the same five authors (Ahmed, Shiri Harzevili, Shin, Pham, Wang; York University); confirmed on PDF p. 1. rlab flagged identity UNCONFIRMED only because the title changed. This analysis is based on the preprint, so numbers in the published version may differ. If the published version becomes accessible, re-check Table 3 and the recall definition.
- Uncertainties: (1) The Table 3 reconstruction (§9) uses the smallest integer counts consistent with all reported percentages and with the flag counts on p. 13 (for Codestral, GPT-4.1 and Claude). It reproduces all 30 percentages, but it is our inference, not something the authors state. (2) The definition of non-vulnerable functions (fixed versions vs. unrelated functions) is not explicit. (3) The appendix calls Qwen "Qwen2.5-Coder-33B" (p. 13), while elsewhere it is 32B (p. 8); this looks like a typo. (4) Our reconstruction implies Qwen flagged 124 functions and Deepseek 124, while p. 13 says 121 and 124.
- Tier: published (AIware 2026, peer-reviewed conference), but the analysed text is the preprint, which was not peer-reviewed.
