---
key: chakraborty2024revisiting
status: complete
evidence_basis: full-text
design: Replication + re-evaluation of 4 DL detectors (and 2 fine-tuned LLMs) on a new whole-project, time-split dataset (Real-Vul)
dataset: Real-Vul (C/C++, top-10 Big-Vul projects, full-codebase snapshots, temporal split); SARD, Big-Vul, ReVeal, IVDetect for replication
sample_size: 5,528 vulnerable functions (4,418 train / 1,110 test) + 1,682,713 uncertain functions (769,464 / 913,249)
metrics: Accuracy, precision, recall, F1, AUC; per-CWE-cluster and per-severity F1
main_finding: On whole-project realistic test data, DL detectors' precision falls to 1-10% (drops up to 95 pp) and F1 by up to 91 pp; fine-tuned LLMs trail LineVul on AUC.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Revisiting the Performance of Deep Learning-Based Vulnerability Detection on Realistic Datasets

- Authors: Chakraborty, Partha; Arumugam, Krishna Kanth; Alfadel, Mahmoud; Nagappan, Meiyappan; McIntosh, Shane
- Year / venue: 2024, IEEE Transactions on Software Engineering (published)
- DOI: 10.1109/tse.2024.3423712 · URL: https://doi.org/10.1109/tse.2024.3423712
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] To test whether deep-learning vulnerability detectors that report up to 99% recall/F1 still perform in a realistic setting where the model scans entire codebases rather than only functions from fixing commits, and to provide a dataset (Real-Vul) for such evaluation (p. 1–2).

## 2. Research questions / hypotheses
- [A] RQ1: How do DeepWukong, LineVul, ReVeal and IVDetect perform in a realistic evaluation setting compared with the setting of the original studies? RQ2: How do they perform when also trained on a similar realistic training dataset? (p. 5).
- [A] Implicit hypothesis: prior datasets (synthetic SARD; commit-sampled Big-Vul/ReVeal with near-balanced ratio and label inconsistency) overestimate performance (p. 3).

## 3. Methodology
- Research design: [V] (1) Replication of four DL models on their original datasets with an 80/20 random split (p. 5–6); (2) evaluation of these models on the Real-Vul test set (RQ1, p. 6–7); (3) retraining on Real-Vul, imbalanced and balanced (RQ2, p. 8–9); (4) discussion analyses: project size vs FPR, cyclomatic complexity, LIME token analysis, dead-code augmentation, per-CWE-cluster and per-severity F1, and two fine-tuned LLMs (p. 9–12).
- Approach / model / intervention: [V] LineVul (CodeBERT, token-based), DeepWukong (GNN on XFG slices), ReVeal (GNN on code property graphs, uses SMOTE), IVDetect (graph-based with interpretation) (p. 4–5). [V] CodeLlama (7B) and Mixtral ("7B" per the paper) fine-tuned with parameter-efficient fine-tuning on Real-Vul (p. 12).
- Baselines or comparison conditions: [V] Each model's performance on its own original dataset (Table 2) is the baseline for the realistic setting (p. 6). [V] No static-analysis tool is evaluated; authors list this as future work (p. 13).

## 4. Dataset and sample
- Data source(s): [V] Real-Vul built from the 10 Big-Vul projects with the most vulnerabilities (Chromium, FFmpeg, ImageMagick, Jasper, Krb5, Linux, OpenSSL, php-src, QEMU, tcpdump), covering 73% of Big-Vul's vulnerable samples (p. 3–4, Table 1).
- Sample size (N) and unit: [V] Function. 5,528 vulnerable functions (4,418 train, 1,110 test) (p. 4); 1,682,713 uncertain functions (769,464 train, 913,249 test) (p. 4). Table 1 project sizes sum to 270,919 functions and p. 13 states "270,919 samples, of which 5,528 are vulnerable" (p. 4, p. 13).
- Sampling / selection method: [V] Vulnerable functions ordered by fix date; first 80% to train, last 20% to test. Uncertain functions = all functions in a repository snapshot taken after the last training fix date (train) and after the test period (test) whose MD5 hash matches no vulnerable function, avoiding label inconsistency (p. 4). [V] Authors found 15% of vulnerable samples in ReVeal also listed as uncertain (p. 3).
- Data availability (public? link?): [A] Real-Vul and scripts released at https://zenodo.org/record/8206635 (p. 2).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] DeepWukong 50 epochs, LineVul 10 epochs, ReVeal max 100, IVDetect max 50 epochs, early stopping after 5 epochs without F1 gain (p. 6). For RQ1, DeepWukong is retrained on Big-Vul (28,294 vulnerable / 639,047 uncertain XFGs) to be comparable (p. 7). Balanced training = random undersampling of uncertain samples to equal vulnerable count (p. 8). Augmentation: eleven dead-code insertion strategies (details in online appendix) (p. 10). LLM fine-tuning hyper-parameters: not reported beyond "parameter-efficient fine-tuning" (p. 12). Seeds/repeats: not reported; authors state repeated training was not feasible (p. 13).
- Code availability: [A] scripts released (p. 2).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] Accuracy, precision, recall, F1 and AUC, each defined in the paper (p. 5). Per-SFP-cluster (CWE group) and per-severity F1 (p. 10–11).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V] Mann-Whitney U tests for cyclomatic complexity (TP vs FP p = 0.043; TN vs FN p = 0.014) and for LIME positive-token ratio in FP vs TP (p = 0.13, α = 0.05) (p. 10). No CIs or tests for the main performance comparisons.

## 7. Key findings
1. Replication on original datasets: DeepWukong (SARD) P 87 / R 98 / F1 93 / AUC 88; LineVul (Big-Vul) P 96 / R 84 / F1 90 / AUC 85; ReVeal P 29 / R 59 / F1 38; IVDetect P 39 / R 63 / F1 24 (%) — [V] (p. 6, Table 2).
2. RQ1, original-trained models on Real-Vul test: DeepWukong P 1 / R 87 / F1 2 / AUC 62; LineVul P 1 / R 90 / F1 2 / AUC 58; ReVeal P 10 / R 80 / F1 17 / AUC 61; IVDetect P 2 / R 84 / F1 2 / AUC 59 (%) — [V] (p. 7, Table 3).
3. Drops vs original setting: precision −86 (DeepWukong), −95 (LineVul), −19 (ReVeal), −37 (IVDetect) pp; F1 −91, −88, −21, −22 pp — [V] (p. 7).
4. False positives on Real-Vul test: DeepWukong 439,494; LineVul 114,629; ReVeal 320,128; IVDetect 512,284 — [V] (p. 7).
5. RQ2, trained on imbalanced Real-Vul: DeepWukong and LineVul P/R/F1 0%, AUC 50% (predict everything uncertain); ReVeal F1 3%; IVDetect F1 0% — [V] (p. 8, Table 4).
6. RQ2, trained on balanced Real-Vul: F1 DeepWukong 2%, LineVul 20% (P 11, R 99), ReVeal 36% (P 31, R 45), IVDetect 6%; AUC 51.3–52.3% — [V] (p. 9, Table 5).
7. Dead-code augmentation: LineVul F1 20 → 46%, AUC 51.4 → 81.8%, precision 11 → 37%, recall 99 → 65%; smaller gains for graph models (DeepWukong F1 7%, ReVeal 38%, IVDetect 16%) — [V] (p. 10, Table 6).
8. Fine-tuned LLMs (with augmented training data): CodeLlama P 34 / R 54 / F1 42 / AUC 67; Mixtral P 38 / R 59 / F1 46 / AUC 71 (%). AUC lags LineVul by 14.8 and 10.8 pp; authors conclude "specialized tools (LineVul) outperform general large language models (LLMs)" — [V] numbers, [A] conclusion (p. 12, Table 8).
9. Per-CWE cluster: best F1 for information-leak (SFP 895, up to 33.6%) and tainted-input (896, 23.31%) clusters; worst for path resolution (893), predictability (905) and miscellaneous (907, no detections) — [V] (p. 10–11, Fig. 5). Cluster frequency strongly uneven (890 32%, 896 25%, 892 14%; 907 0.003%) — [V] (p. 11).
10. Per severity F1: high-severity vulnerabilities hardest (9.06–10.89%) vs medium (17.46–26.57%) and low (15.08–21.66%); only 5% of vulnerabilities are high severity — [V] (p. 10–11, Table 7).
11. Larger projects show lower false-positive rates (Fig. 4); higher cyclomatic complexity associated with FPs (p = 0.043) — [V] (p. 9–10).

## 8. Limitations stated by the authors
- [A] Some Big-Vul vulnerable samples may be mislabelled, though Big-Vul labels were manually verified by Fan et al. (p. 13).
- [A] Only ten open-source projects; may not represent all real-world scenarios (p. 13).
- [A] "Uncertain" functions may contain undiscovered vulnerabilities (p. 13).
- [A] Balanced datasets use one random undersample; multiple runs were not feasible due to compute (p. 13).
- [A] Hash-based label-consistency check may miss whitespace variants despite regex normalisation (p. 13).
- [A] Only DL techniques evaluated; static and dynamic analysis tools left for future work (p. 13).

## 9. Limitations we identified
- [I] Internal numerical inconsistencies: (a) IVDetect replication reports P 39 / R 63 but F1 24 (the harmonic mean of 39 and 63 is ~48) (p. 6, Table 2); (b) Table 1 project sizes total 270,919 functions while the text reports 1,682,713 uncertain functions (p. 4, p. 13); (c) balanced LineVul shows R 99% with AUC 51.4% (p. 9, Table 5), which is hard to reconcile with high recall at ~99% accuracy. These do not change the qualitative story but make exact numbers less reliable.
- [I] The LLM comparison is thin and partly contradicts its own conclusion: Mixtral's F1 (46%) equals augmented LineVul's F1 (46%) and its precision (38%) is higher than LineVul's (37%); only AUC favours LineVul (p. 10, p. 12). The LLM accuracy of 80–83% at 34–38% precision implies a test set far less imbalanced than the 1,110 / 913,249 Real-Vul test set, so the LLM test set appears to differ from the DL test set (inferred from Table 8 vs p. 4); test-set composition and hyper-parameters are not reported. Mixtral is described as "7 B parameter", which [I] understates its 8×7B mixture-of-experts size.
- [I] RQ1 conflates two shifts: from commit-sampled to whole-project negatives (realistic base rate) and from original training data to a different test distribution; RQ2 isolates the first, and still yields F1 ≤ 36%.
- [I] Big-Vul is the label source for Real-Vul vulnerable functions; only ~25% of Big-Vul vulnerable labels are correct according to Chen et al., as reported by [@ding2025vulnerability, p. 4] (Risse et al.'s own audit gives 39% [@risse2025top, p. 7]), so the authors' reliance on Fan et al.'s verification (p. 13) is optimistic.
- [I] Absolute false-positive counts are reported in different units (XFGs, chunks, CPGs, PDGs) per model (p. 7), so they are not directly comparable across models.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Temporal split and MD5-based label consistency reduce leakage; near-duplicates and inherited Big-Vul label noise remain. Single random undersample for balancing.
- External (generalisability of sample/context): [I] Ten large C/C++ projects dominated by Chromium and Linux; only function-level DL models plus two 7B-class LLMs; no SAST tools; no other languages.
- Construct (do metrics measure the concept?): [I] Precision at realistic base rate is the practically relevant metric and is the paper's key contribution; AUC values near 50% with high recall suggest threshold effects. "Uncertain" negatives may hide real vulnerabilities, depressing measured precision.
- Statistical conclusion (power, multiple comparisons, variance): [I] No CIs or repeated runs for performance; Mann-Whitney tests only in side analyses, no multiple-comparison correction.
- Reproducibility (data/code/setup reported?): [A] Dataset and scripts on Zenodo (p. 2); [I] augmentation strategies and LLM fine-tuning settings only in an online appendix / not reported.

## 11. Future research directions
- Stated by authors [A] (p. 10–13): augmentations inducing structural/data-flow changes for graph models; better data strategies and architectures for contextual and system-level vulnerabilities; improving detection of high-severity vulnerabilities; improving LLM specificity for vulnerability detection; evaluating static and dynamic analysis tools on Real-Vul.
- Suggested by us [I]: run SAST tools and prompted/fine-tuned LLMs on the identical Real-Vul test set and report precision at a fixed alert budget; combine Real-Vul's whole-project negatives with PrimeVul-style label verification.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ4, RQ5.
- How it informs our work [I]: Strongest evidence in our set that base-rate realism (whole-project scanning) destroys precision of DL detectors (to 1–10%), complementing Ding et al.'s label/duplication findings. Gives per-CWE-cluster and severity breakdowns for RQ4, and a small fine-tuned-LLM vs LineVul comparison for RQ1 whose conclusion depends on the metric (AUC favours LineVul, F1 tied). Explicitly names SAST comparison on Real-Vul as missing (RQ5).

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | Evaluated on whole-project, time-split Real-Vul, DL detectors' precision drops by up to 95 pp (to 1–10%) and F1 by up to 91 pp vs their original benchmarks | 7 | V | moderate |
| RQ2 | 15% of vulnerable samples in the ReVeal dataset also appear as uncertain (label inconsistency) | 3 | V | weak |
| RQ1 | Even trained on balanced Real-Vul, DL detectors reach only F1 2–36% and AUC 51–52% on realistic test data | 9 | V | moderate |
| RQ1 | Fine-tuned CodeLlama/Mixtral F1 42%/46%, AUC 67%/71% vs augmented LineVul F1 46%, AUC 81.8% (LLM test-set composition unclear) | 12 | V | weak |
| RQ4 | DL detectors detect information-leak and tainted-input CWE clusters best (F1 up to 33.6%) and path-traversal/predictability/misc clusters worst (none detected for SFP 907) | 11 | V | moderate |
| RQ4 | High-severity vulnerabilities get the lowest F1 (9.06–10.89%) across all four models | 11 | V | moderate |
| RQ1 | Dead-code augmentation raises LineVul F1 20 → 46% and AUC 51.4 → 81.8% on Real-Vul | 10 | V | weak |
| RQ5 | Authors call for evaluating static and dynamic analysis tools on Real-Vul (not done) | 13 | A | weak |

## 14. Key quotes
> "precision declining by up to 95 percentage points and F1 scores dropping by up to 91 percentage points" (p. 1)

> "The study shows that specialized tools (LineVul) outperform general large language models (LLMs) in vulnerability detection" (p. 12)

## Analyst notes
- Reading coverage: whole paper read (abstract to conclusion, references skimmed, author bios skipped). Scatter plots (Fig. 2–3) and the per-cluster bar charts (Fig. 5) were interpreted from the text only; cluster F1 maxima taken from the text on p. 10–11.
- Source version: arXiv 2407.03093v1 (3 Jul 2024), an "Author pre-print copy" of the TSE 2024 paper (p. 1). Page refs are to the arXiv PDF.
- Uncertainties: the numerical inconsistencies listed in section 9; how the LLM test set in Table 8 was built; "Real-Vul" uncertain-function count (1.68M vs 270,919).
