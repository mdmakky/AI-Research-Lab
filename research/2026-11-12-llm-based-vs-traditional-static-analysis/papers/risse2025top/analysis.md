---
key: risse2025top
status: complete
evidence_basis: full-text
design: Literature survey (81 ML4VD papers) + manual expert labelling study + word-count classifier probe for spurious correlations
dataset: BigVul, Devign, DiverseVul (C/C++ function-level benchmarks)
sample_size: 300 vulnerable-labelled + 90 secure-labelled functions manually analysed (2 annotators); 81 surveyed papers
metrics: Label accuracy, share context-dependent, Cohen's kappa, F1 / accuracy of word-count Gradient Boosting
main_finding: Only 39-65% of vulnerable labels correct; all 151 truly vulnerable functions need external context; word counts alone give F1 0.86 on BigVul (SOTA 0.96).
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Top Score on the Wrong Exam: On Benchmarking in Machine Learning for Vulnerability Detection

- Authors: Risse, Niklas; Liu, Jing; Böhme, Marcel
- Year / venue: 2025, Proceedings of the ACM on Software Engineering (published)
- DOI: 10.1145/3728887 · URL: https://doi.org/10.1145/3728887
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] To examine whether the dominant problem statement of machine learning for vulnerability detection (ML4VD) — "given a function, does it contain a security flaw?" — is well-defined, by measuring how often function vulnerability can be decided without external context in popular datasets, and to explain why ML4VD models nevertheless score highly (p. 1–2).

## 2. Research questions / hypotheses
- [A] Survey questions: what proportion of ML4VD papers use a function-level problem statement; which datasets they use (p. 3).
- [A] RQ.1 Can vulnerability detection be cast as function-level binary classification? (a) noisy labels, (b) context-dependent vulnerability, (c) context-dependent security of secure-labelled functions. RQ.2 Can high classification performance be achieved when the vulnerability's root cause is hidden (spurious features)? (p. 5).
- [A] Hypothesis: vulnerability of a function often cannot be decided without context (p. 1).

## 3. Methodology
- Research design: [V] (1) Literature survey of 2020–2024 ML4VD papers at ICSE, FSE, ASE, ISSTA, S&P, USENIX Security, NDSS, CCS, TSE, TOSEM, TIFS, TDSC, following Kitchenham/Petersen guidelines; >2,500 candidates → 109 by title → 81 by abstract/full text, filtered by one co-author (p. 3–4). (2) Manual labelling study by two security researchers with a 15-minute decision cap per function, plus a second round on context dependence (p. 6–7). (3) Constructing artificial vulnerable contexts for secure-labelled functions (p. 10). (4) Training a Gradient Boosting Classifier on word counts only (p. 7, p. 11).
- Approach / model / intervention: [V] Gradient Boosting Classifier on word-count features with no code structure, no pre-training; trained on each dataset's training subset and evaluated on its evaluation subset (p. 7, p. 11).
- Baselines or comparison conditions: [V] Published state-of-the-art scores: SNOPY 67.86% F1 and PDBERT 67.61% accuracy on Devign; DeepDFA 96.46% F1 on BigVul; CodeT5 Small 48.28% F1 on DiverseVul (Chen et al. benchmark) (p. 7). [V] SOTA values are taken from the literature, not re-run. [V] No LLM or static-analysis tool is evaluated experimentally (p. 7).

## 4. Dataset and sample
- Data source(s): [V] BigVul, Devign (most used in survey) and DiverseVul (recent, widely used in preprints); ReVeal excluded because it lacks patch-commit IDs/CVEs (p. 6).
- Sample size (N) and unit: [V] 100 randomly sampled vulnerable-labelled functions per dataset (300 total) from patch commits 2010–2022 covering 80 projects (BigVul 25, Devign 2, DiverseVul 60) (p. 6). 30 secure-labelled functions per dataset (90 total) for RQ.1-c (p. 10). Survey: 81 papers (p. 4). Class balance: Devign 47.9%, BigVul 4.5%, DiverseVul 5.4% vulnerable (p. 7).
- Sampling / selection method: [V] Random sampling; sample size "inspired by" Croft et al. (n=70) (p. 6). No power analysis.
- Data availability (public? link?): [A] Scripts, sampled functions, labels and explanations at https://github.com/niklasrisse/TopScoreWrongExam (p. 6–7, p. 13).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Annotators reviewed patch commit and, where available, CVE report; >150 hours total; labels Secure / Vulnerable / No decision; ambiguous callee-vs-caller fixes labelled callee only (p. 6). [V] Inter-rater agreement: 82% (Cohen's κ = 0.64) for vulnerable/secure; 98% (κ = 0.96) for context dependence; disagreements resolved by discussion (p. 6). [V] Annotators: 3 and 5 years security research experience; second annotator co-discovered three CVEs present in the datasets (p. 6–7). [V] Classifier training+evaluation took 30 minutes on a MacBook Pro (p. 11). GBC hyper-parameters and the exact train/evaluation splits: not reported in the paper text.
- Code availability: [A] GitHub repository above (p. 7).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] F1 as primary metric because it dominates the surveyed literature; accuracy only for balanced Devign, omitted for imbalanced BigVul/DiverseVul (p. 7). [V] Labelling outcomes reported as proportions; Cohen's kappa for agreement (p. 6).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): not reported beyond Cohen's kappa; no CIs on proportions.

## 7. Key findings
1. 88% of 81 surveyed ML4VD papers (2020–2024) define ML4VD as function-level binary classification (SE conferences 92%, security conferences 75%, journals 85%); 95% in 2024 — [V] (p. 5, Fig. 2a).
2. BigVul and Devign are each used by 36 papers and ReVeal by 22; 53 of 81 papers use at least one of the three — [V] (p. 5, Fig. 3).
3. Label accuracy of vulnerable-labelled functions: BigVul 39%, Devign 47%, DiverseVul 65% actually vulnerable (Devign 3% no decision) — [V] (p. 7–8, Fig. 6).
4. Reasons for wrong labels: patch-commit identification (BigVul 21%, Devign 54%, DiverseVul 3%), structural changes caused by the fix (48%, 38%, 66%), unrelated changes (31%, 8%, 31%) — [V] (p. 8, Table I).
5. All 151 truly vulnerable functions were context-dependent; none could be decided from the function alone — [V] (p. 9).
6. Types of context dependence: external functions 43–52%, function arguments 40–47%, globals 2–10%, type declarations 0–3%, execution environment 0–3% — [V] (p. 9, Table II).
7. For 82 of 90 secure-labelled functions the authors could construct a context in which the function is vulnerable — [V] (p. 10).
8. Word-count Gradient Boosting vs SOTA: BigVul F1 0.86 vs 0.96; Devign F1 0.62 vs 0.68 and accuracy 0.63 vs 0.68; DiverseVul F1 0.11 vs 0.48 — [V] (p. 11, Table III).
9. Authors conclude the function-level problem statement is ill-defined, "there is currently no evidence that ML4VD techniques are actually capable of identifying security vulnerabilities at the function-level", and high scores likely reflect spurious correlations — [A] (p. 2, p. 11–12).
10. Authors argue intra-procedural static analysis faces the same context-dependency problem and that combining static analysis with ML is promising — [A] (p. 2, p. 12–13).

## 8. Limitations stated by the authors
- [A] Selection bias from random sampling of 100 functions per dataset (p. 11).
- [A] Manual labelling is subjective; some human error may remain despite cross-labelling (p. 11–12).
- [A] Only three datasets; may not generalise to other datasets or real-world systems (p. 12).
- [A] Datasets are mainly C; may not generalise to other languages (p. 12).
- [A] Only the function-level problem statement studied; other granularities need similar study (p. 12).
- [A] Spurious correlation shown only with word counts; other spurious features need study (p. 12). The GBC result shows datasets can be exploited, not that SOTA models actually do so (p. 11).
- [A] Secure functions were not verified to be truly non-vulnerable (p. 10).

## 9. Limitations we identified
- [I] The context-dependence criterion is very permissive: almost any function that dereferences a pointer or uses an argument can be made vulnerable by an adversarial caller (e.g. passing NULL, Fig. 11, p. 10). The 100% / 82-of-90 results are partly a consequence of this definition and say more about the problem framing than about any detector.
- [I] Word-count GBC vs SOTA compares a model the authors trained with literature numbers produced under possibly different splits and preprocessing (p. 7, p. 11); no re-run of SOTA models on identical splits, no repeated runs, and GBC settings are not given.
- [V] On DiverseVul word counts reach only 0.11 F1 vs SOTA 0.48 (p. 11). [A] The authors say this "suggests that the dataset may contain fewer exploitable spurious features. However, this is not definitive proof" (p. 11). DiverseVul is the least noisy of the three by the authors' own audit (65% correct vs 39%/47%, p. 8); it is not the least leaky (exact-copy rate 3.3% vs 0.6% for CodeXGLUE/Devign [@ding2025vulnerability, p. 4]). [I] Our inference, resting on Table III (p. 11): the spurious-feature argument is strongest for BigVul/Devign and is not universal.
- [I] Label-accuracy samples are small (n=100; ~±10 pp at 95% binomial CI by our calculation) and κ = 0.64 for the first step is only "substantial"; the 15-minute cap may bias towards "secure" for complex cases.
- [I] Survey screening was done by a single author (p. 4), a risk for selection consistency.
- [I] No LLM or SAST experiment: relevance to LLM-vs-SAST is through benchmark validity, not head-to-head numbers.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Random sampling and released labels are strengths; single-screener survey and annotators' prior work on ML4VD critique (refs [19], [24]) could bias judgements towards the hypothesis.
- External (generalisability of sample/context): [I] Three C/C++ datasets; Devign sample spans only 2 projects (p. 6); results may differ for Java/Python or curated datasets such as PrimeVul.
- Construct (do metrics measure the concept?): [I] "Context-dependent" is not a measure of detector failure; a context-dependent vulnerability may still be statistically predictable from code patterns. The word-count probe tests exploitability of datasets, not model behaviour.
- Statistical conclusion (power, multiple comparisons, variance): [I] No CIs; per-dataset proportions from n=100 (vulnerable) and n=30 (secure).
- Reproducibility (data/code/setup reported?): [A] Full artifact (scripts, samples, labels, explanations) released (p. 13).

## 11. Future research directions
- Stated by authors [A] (p. 12–13): binary classification with abstention; other base units (lines, files, modules, inter-procedural slices); context-conditional classification with the full repository at the patch commit as context; replacing classification by generating a vulnerable context or an ML-assisted proof-of-vulnerability test case; combining static analysis and ML; methods to detect spurious correlations in benchmarks.
- Suggested by us [I]: test whether LLMs given repository-level context (or tool-augmented with static analysis) reduce the context-dependency problem on the released labelled subset; repeat the word-count probe on PrimeVul and Real-Vul.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2, RQ3, RQ5.
- How it informs our work [I]: Key methodological critique for RQ2 — explains why high F1 on BigVul/Devign (used by most DL and many LLM papers) is weak evidence of detection ability: labels are 39–65% accurate, vulnerability is context-dependent, and word counts reach near-SOTA scores. Supports interpreting fu2023chatgpt's 94% F1 for fine-tuned models as benchmark-inflated. For RQ3/RQ5 it argues for context-aware formulations and static-analysis + ML combinations, but provides no experimental evidence on hybrids.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | 88% of 81 ML4VD papers (2020–2024, top venues) frame detection as function-level binary classification; 53/81 use BigVul, Devign or ReVeal | 5 | V | moderate |
| RQ2 | Only 39% (BigVul), 47% (Devign) and 65% (DiverseVul) of sampled vulnerable-labelled functions are actually vulnerable (n=100 each) | 8 | V | moderate |
| RQ2 | All 151 truly vulnerable functions required context beyond the function (mainly external functions 43–52% and arguments 40–47%) | 9 | V | moderate |
| RQ2 | A word-count Gradient Boosting classifier reaches F1 0.86 on BigVul (SOTA 0.96) and 0.62 on Devign (SOTA 0.68), but only 0.11 on DiverseVul (SOTA 0.48) | 11 | V | moderate |
| RQ5 | Authors argue there is currently no evidence that ML4VD techniques can identify vulnerabilities at function level | 2 | A | moderate |
| RQ3 | Authors argue function-level static analysis faces the same context problem and propose combining static analysis with ML | 12 | A | weak |

## 14. Key quotes
> "there is currently no evidence that ML4VD techniques are actually capable of identifying security vulnerabilities at the function-level" (p. 2)

> "All 151 vulnerable functions in our empirical study required additional context to be identified." (p. 9)

## Analyst notes
- Reading coverage: whole paper read (survey, study design, results, threats, discussion, data availability); reference list skimmed. Survey figures (Fig. 2–4) read via text values.
- Source version: arXiv 2408.12986v2 (23 Apr 2025); published in Proceedings of the ACM on Software Engineering (FSE 2025), DOI above. Page refs are to the arXiv PDF.
- Uncertainties: GBC hyper-parameters and the exact train/evaluation splits used for the word-count probe are not stated in the paper text (may be in the artifact). The abstract's ">90% of functions" combines vulnerable (151/151) and secure (82/90) results.
