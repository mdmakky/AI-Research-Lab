---
key: shu2026evaluating
status: complete
evidence_basis: full-text
design: Empirical comparison of 8 fine-tuned/embedding PLMs vs 5 LLMs (zero-shot, BM25 few-shot, instruction tuning) at function and line level, 7 languages
dataset: REEF (NVD + Mend CVEs 2016-2023; C, C++, C#, Go, Java, JavaScript, Python), functions ≤512 tokens; plus 2024-2025 time-split and imbalanced variants
sample_size: Function level 20,165 functions (test 2,026, balanced); line level 8,134 vulnerable functions (test 810); imbalanced test 6,051; time-split test 3,138 / 1,328
metrics: Accuracy, precision, recall, F1, FPR, FNR, MCC, AUC (pooled over languages); per-CWE and per-severity correct-detection counts; API/TCO cost
main_finding: Fine-tuned GPT-4o + few-shot beats CodeT5P (acc 0.7196 vs 0.6037; line F1 0.6641 vs 0.4841) on balanced data, but PLMs win on imbalanced data.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Evaluating large language models for multilingual vulnerability detection at dual granularities

- Authors: Shu, Honglin; Fu, Michael; Yu, Junji; Wang, Dong; Tantithamthavorn, Chakkrit; Chen, Junjie; Kamei, Yasutaka
- Year / venue: 2026, Empirical Software Engineering (published)
- DOI: 10.1007/s10664-026-10832-4 · URL: https://doi.org/10.1007/s10664-026-10832-4
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

> Version note: the text analysed is arXiv 2506.07503v2 (10 Mar 2026, 53 pages, journal "manuscript No." template) (p. 1), not the typeset EMSE version. Page refs are PDF pages of this preprint.

## 1. Research objective
- [A] Evaluate how well pre-trained code language models (PLMs) and large language models (LLMs) detect vulnerabilities across seven programming languages, at both function level and line level. Prior work focused on C/C++ and function-level detection (p. 1, p. 3, p. 4).
- [A] Working hypothesis: LLMs with suitable learning strategies (instruction tuning, few-shot prompting) improve multilingual function- and line-level detection (p. 4).
- [A] The paper extends the authors' ISSTA'25 workshop paper (Yu et al. 2025b) with embedding models, few-shot prompting and instruction tuning, line-level detection, CWE/severity analyses, and model size/reasoning experiments (p. 5).

## 2. Research questions / hypotheses
- RQ1: How effective are PLMs and LLMs at detecting multilingual vulnerabilities at function level? (p. 4)
- RQ2: ... at line level? (p. 4)
- RQ3: What are the strengths and weaknesses of PLMs and LLMs in multilingual detection? (p. 4)
- Discussion experiments: code-structure analysis, model size (70B), reasoning LLMs, time-split leakage check, imbalanced setting, deployment cost (p. 32-p. 43).

## 3. Methodology
- Research design: controlled empirical comparison on a fixed random 8:1:1 split, stratified by language, of the REEF dataset (p. 7, p. 8).
- Approach / model / intervention:
  - PLMs (function level): CodeBERT, CodeT5, CodeT5P, UniXcoder and LineVul, fully fine-tuned with an MLP head on the [CLS] token. OpenAI Text-Embedding-Ada-002 / 3-Small / 3-Large are used as frozen encoders with a trained classifier head (p. 9, p. 16).
  - PLMs (line level): CodeBERT, UniXcoder, CodeT5, CodeT5P, with up to 113 lines x 31 tokens per function, GRU per line, per-line sigmoid, threshold 0.5. LineVul and the embedding models are excluded at line level (p. 22).
  - LLMs: DeepSeek-Coder 6.7B, Code Llama 7B, Llama 3 8B (HuggingFace), GPT-3.5-Turbo (gpt-3.5-turbo-0125), GPT-4o (gpt-4o-2024-08-06) (p. 10, p. 15). Strategies: zero-shot; few-shot with 3 BM25-retrieved training examples; instruction tuning (LoRA) followed by zero-shot or few-shot prompting (p. 12, p. 14). GRACE (AST-enhanced LLM, zero-shot) is added as a baseline at function level (p. 10, p. 11).
  - Line-level LLM prompts state that the function is vulnerable, and lines are tagged "Line N:" (p. 11, p. 23).
  - Extra models: Code Llama 70B and Llama 3 70B (p. 35); reasoning LLMs DeepSeek-R1 (671B) and QwQ-plus, zero-shot only (p. 37).
- Baselines or comparison conditions: dummy classifiers that predict all-vulnerable or all-clean (p. 11). **No static-analysis (SAST) tool and no GNN/RNN detector is evaluated.** GNNs/RNNs are excluded because ASTs are language-specific and PLMs were previously shown to be better (p. 9, p. 10). MSIVD and Vul-RAG are excluded for lack of multilingual knowledge/explanations (p. 11).

## 4. Dataset and sample
- Data source(s): REEF (Wang et al. 2023a): 4,466 CVEs, 30,987 patches, NVD + Mend CVE list, 2016-2023, seven languages (p. 6).
- Sampling / selection method: comments removed; functions extracted with Tree-sitter; the pre-change function is labelled vulnerable and the post-change function clean (matched by name, then by edit distance); functions longer than 512 removed (PLM input limit) (p. 6). Line labels come from deleted lines (difflib); vulnerable functions fixed by additions only are dropped (p. 6, p. 7). Split: 8:1:1 stratified random sampling per language (p. 7, p. 8). "Exact-match filtering" against leakage (p. 44).
- Sample size (N) and unit:
  - Function level: 20,165 functions (10,133 vulnerable / 10,032 clean); train 16,126 / val 2,013 / test 2,026. Per language: C 3,056; C++ 1,792; C# 427; Go 2,905; Java 3,235; JavaScript 5,468; Python 3,282. Test sets per language: C 307, C++ 181, C# 44, Go 292, Java 325, JavaScript 548, Python 329 (p. 7, Table 1).
  - Line level: 8,134 vulnerable functions (train 6,513 / val 811 / test 810); 25,161 vulnerable vs 150,607 non-vulnerable lines. C# test set has only 13 functions (p. 8, Table 2).
  - Tree-sitter extraction check: 377 random samples, 93% / 92% judged correct by two authors, Cohen's kappa 0.9448 (p. 7).
  - Severity: 1.2% low, 41.12% high, 25.09% critical (CVSS v4.0) (p. 8).
  - Time-split set (2024-2025, same pipeline): 3,138 function-level samples (balanced) and 1,328 line-level samples (p. 38).
  - Imbalanced set (benign functions mined from unchanged functions): train 48,219 / val 6,012 / test 6,051; test = 1,019 vulnerable + 5,032 benign (p. 39).
- Data availability (public? link?): data, training and evaluation scripts on GitHub (SpanShu96/Large-Language-Model-for-Multilingual-Vulnerability-Detection) (p. 48).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: PLMs replicated following Steenhoek et al. 2024a, using the original authors' hyper-parameters (p. 15, p. 43). LoRA for instruction tuning (p. 14, p. 16). Hardware: Xeon Gold 6342, 512 GB RAM, 2 x A800 GPUs (p. 16). Detailed hyper-parameters (learning rate, epochs, LoRA rank, temperature/decoding) are not reported in the paper; it refers to the replication package (p. 16). How GPT-3.5/GPT-4o were instruction-tuned is not described explicitly, but Table 12 lists per-token training costs for them (p. 41).
- Metrics are pooled over all test samples across languages, not averaged per language (p. 15).
- Code availability: yes (p. 48).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: Accuracy, precision, recall, F1 (binary), FPR, FNR, MCC, AUC (trapezoidal) (p. 14, p. 15). Accuracy is the primary metric at function level because the data is balanced; F1 is primary at line level because the data is imbalanced (p. 17, p. 23). RQ3 uses the share of correct detections per Top-25 CWE (2023 list) and per CVSS severity, plus Venn diagrams of unique correct/incorrect predictions (p. 27, p. 28).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): **none.** No significance tests, confidence intervals or repeated runs/seeds are reported. The words "significantly" and "significant" are used without tests (e.g. p. 21, p. 26, p. 38).

## 7. Key findings
1. Function level, balanced (Table 3): best LLM = GPT-4o with instruction tuning + few-shot (ITFSP): Acc 0.7196, P 0.7454, R 0.6722, F1 0.7069, FPR 0.2324, MCC 0.4360, AUC 0.7169. Best PLM = CodeT5P: Acc 0.6037, P 0.5626, R 0.9529, F1 0.7075, FPR 0.7496, MCC 0.2860, AUC 0.6015 — [V] (p. 17). F1 is essentially tied (0.7069 vs 0.7075); the gap is in accuracy/precision/FPR/MCC.
2. Every other LLM configuration at function level is near chance: zero-shot accuracy 0.4827-0.5061 (GRACE 0.5061), MCC −0.0585 to 0.0244; few-shot without tuning lowers accuracy for all but GPT-4o (e.g. GPT-3.5 0.3618, DeepSeek-Coder 0.3870); best instruction-tuned zero-shot is GPT-4o at 0.5874 — [V] (p. 17, p. 19).
3. Text-embedding models, CodeBERT and LineVul are near random at function level (Acc 0.5030-0.5173, AUC 0.50-0.51; LineVul and CodeBERT rows identical) — [V] (p. 17).
4. Per language, function level (Acc): GPT-4o ITFSP — C 0.7557, C# 0.7273, C++ 0.7901, Go 0.8082, JavaScript 0.6642, Java 0.7169, Python 0.6626. CodeT5P — C 0.5081, C# 0.6136, C++ 0.5249, Go 0.6062, JavaScript 0.7062, Java 0.6031, Python 0.5623 — [V] (p. 21). In JavaScript, CodeT5P (0.7062) and CodeT5 (0.6898) beat GPT-4o (0.6642). This contradicts the claim that GPT-4o "outperformed all other PLMs and LLMs across all seven studied languages" (p. 22) — [V] (p. 21, p. 22).
5. Line level (Table 4): GPT-4o ITFSP F1 0.6641 (P 0.7012, R 0.6307, MCC 0.6563, AUC 0.8116) vs best PLM CodeT5P F1 0.4841 (P 0.3536, R 0.7673, MCC 0.5029, AUC 0.8644). GPT-4o few-shot without tuning already gives F1 0.6050. Zero-shot LLM F1 is 0.2254-0.3313 — [V] (p. 23, p. 25, p. 26). CodeT5P has the higher AUC — [V] (p. 26).
6. Per language, line level (F1): GPT-4o ITFSP — C 0.5478, C# 0.4348, C++ 0.5774, Go 0.7078, JavaScript 0.7815, Java 0.6391, Python 0.6055. CodeT5P — C 0.3727, C# 0.4750, C++ 0.4768, Go 0.4146, JavaScript 0.6556, Java 0.4167, Python 0.4519 — [V] (p. 26). CodeT5P wins in C# (13 test functions) — [V] (p. 8, p. 26).
7. Imbalanced function-level setting (~17% vulnerable; Table 11): the ranking reverses. Best F1 is UniXcoder 0.4626 (MCC 0.3495); CodeT5P has the highest MCC 0.3627; GPT-4o ITFSP reaches F1 0.4010, MCC 0.2774. The authors conclude the PLM "remains superior in overall classification balance" in the imbalanced setting — [V] (p. 40, p. 41). Instruction-tuned GPT-4o zero-shot has P 0.9659 but R 0.0834 — [V] (p. 40).
8. Top-25 CWEs (function level, per-CWE accuracy over vulnerable + clean functions, 1,119 test items): GPT-4o ITFSP 75.87% vs CodeT5P 61.13%. It is best on 23 of 25 CWEs (CodeT5P leads or ties on 7); e.g. CWE-787 82.93% vs 56.1%, CWE-79 78.28% vs 63.13%, CWE-89 78.26% vs 58.7% — [V] (p. 29, p. 30, Table 5).
9. Top-25 CWEs (line level, 441 items): GPT-4o ITFSP 50.79% vs CodeT5P 21.77%. Memory-safety CWEs are hardest: CWE-787 1/16 (6.25%), CWE-119 21.74%, CWE-125 27.27% — [V] (p. 30, Table 6). The authors find 11 CWEs, including CWE-787, CWE-125 and CWE-22, are "detected" at function level but not at line level — [A] (p. 31).
10. Severity: at function level GPT-4o ITFSP has 630 correct High-severity detections vs CodeT5P 514, but fewer Critical (305 vs 321). At line level, 134 Critical vs 76 — [V] (p. 32).
11. Complementarity: CodeT5P has the most unique correct function-level detections (108 vs 28 for GPT-4o ITFSP), but GPT-4o ITFSP has the fewest unique incorrect detections (11 vs 136) — [V] (p. 29). In 608 LLM-only-correct vs 370 PLM-only-correct functions, the LLM-only set has higher median cyclomatic complexity (4.0 vs 2.0), tokens (135.5 vs 96.0) and LOC (19 vs 15), but lower nesting (2.0 vs 3.0) — [V] (p. 32, p. 34).
12. Model size: 70B Code Llama / Llama 3 bring no function-level gain (accuracies 0.4659-0.5093). At line level, Llama 3 70B few-shot F1 is 0.5214 vs 0.2822 for 8B, while Code Llama 70B gets worse (0.2267 vs 0.3257) — [V] (p. 35, p. 36).
13. Reasoning LLMs (zero-shot): DeepSeek-R1 Acc 0.5217 / line F1 0.2746; QwQ-plus Acc 0.5346 / line F1 0.3136. Only slightly above random, and not better than non-reasoning LLMs at line level — [V] (p. 37, p. 38).
14. Time-split check (2024-2025 CVEs): GPT-4o ITFSP function-level Acc 0.7874, F1 0.7804, MCC 0.5767; line-level F1 0.3450, MCC 0.3301 (down from 0.6641 in-distribution) — [V] (p. 38, p. 39, Table 10). The authors conclude the LLM "does not merely memorize" — [A] (p. 39).
15. Cost: GPT-4o instruction tuning $86.07 (function) / $59.42 (line); inference input ≈$1.65 / $0.95 for the test set. A local A6000 PLM training run costs ≈$5.59 (≈15x cheaper), with break-even after 58 fine-tuning runs — [V] (p. 41, p. 42). The authors recommend PLMs for organisations with privacy constraints or only consumer GPUs — [A] (p. 42, p. 43).

## 8. Limitations stated by the authors
- [A] Only the REEF dataset and seven languages; generalisation to other languages is unknown (p. 43).
- [A] The 512-token limit of the PLMs restricts context for longer code (p. 43).
- [A] Single-language specialised LLM detectors (mostly C/C++) are excluded, which limits comparison with customised tools (p. 43).
- [A] Tree-sitter may misidentify functions (sanity check done) (p. 43).
- [A] Leakage from the same project/developer across splits is possible; only exact-match filtering is applied (p. 44).
- [A] Tangled commits add label noise; heuristics reduce it, but line-level manual verification is future work (p. 44).
- [A] Reasoning LLMs were not fine-tuned with RL (p. 38).

## 9. Limitations we identified
- [I] **No static-analysis tool is compared.** For our RQ1, this paper supports only LLM-vs-DL/PLM claims, not LLM-vs-SAST. Based on §3 (p. 9-p. 11).
- [I] **The headline result rests on one configuration.** GPT-4o ITFSP is the only LLM setting clearly above chance at function level (next best 0.5874). Few-shot hurts every other model, and the paper gives no explanation, ablation, seed variation or test. A single strong outlier without variance estimates is fragile. Based on Table 3 (p. 17).
- [I] **Possible leakage via paired functions and BM25 retrieval.** The split is random at function level (p. 7), and each vulnerable function has its fixed twin labelled clean (p. 6). Twins and functions from the same CVE/project can fall on opposite sides of the split, and BM25 few-shot retrieval from the training set could then return a near-identical twin with the opposite label. Only exact-match filtering is applied (p. 44). This could favour the few-shot + fine-tuned setting. It is a hypothesis only; the paper gives no retrieval-overlap statistics. Counter-evidence: BM25 examples come from the "REEF training dataset" (p. 12), and the time-split run evaluates the model "trained on the original dataset" (p. 38). If the same 2016–2023 pool was used for retrieval, twins of the 2024–2025 test functions cannot be in it, yet function-level accuracy stays high (0.7874 ≥ 0.7196; Table 10, p. 39; p. 17). That argues against twin/BM25 leakage driving the function-level advantage. The line-level drop (0.6641 → 0.3450, p. 39) remains compatible with the hypothesis. The paper does not state the retrieval pool for the time-split run (p. 38), so this counter-evidence is conditional. Strength stays weak.
- [I] **Line-level accuracy/FPR are probably inflated by padding.** The DummyClf_vul precision on the line-level test set is 0.0267 (p. 23), i.e. 2.67% vulnerable lines. But Table 2 implies about 14.3% vulnerable lines (25,161 / 175,768) (p. 8). 810 test functions x 113 padded line slots ≈ 91,530 slots, and 2.67% of that ≈ 2,440 vulnerable lines, close to the ≈2,500 expected from the dataset average (3.1 per function). This suggests metrics are computed over padded 113-line slots. If so, accuracy (≈0.95-0.98) and FPR are inflated and not comparable to other papers. F1/precision/recall are less affected. Our arithmetic, unconfirmed by the authors.
- [I] The line-level task is easier than real use: only known-vulnerable functions are given, the LLM prompt says the function is vulnerable (p. 11), and only functions with deleted lines are kept (p. 7).
- [I] Short functions only: functions over 512 tokens are removed (p. 6), and median LOC in the divergent samples is 9-36 (p. 33). Scale effects (RQ4) are not tested.
- [I] The 2024-2025 time-split accuracy (0.7874) is higher than in-distribution (0.7196) (p. 39, p. 17). This is unusual and unexplained. Line-level F1 halves (0.6641 → 0.3450), which suggests that localisation does not generalise well over time (p. 39).
- [I] Text vs. table mismatches: CodeBERT Acc 0.5163 in the text vs 0.5173 in the table (p. 18 vs p. 17); GPT-3.5 zero-shot 0.4758 vs 0.4827 (p. 19 vs p. 17); UniXcoder MCC 0.3475 vs 0.3495 (p. 41 vs p. 40); GPT-4o imbalanced zero-shot F1 "0.1264" in the text vs 0.2036 in the table (p. 40). The model is called "GPT-4" in places (p. 21, p. 38). Minor issues, but signs of limited proofreading.
- [I] The per-CWE "correct detection" percentage mixes vulnerable and clean items. At line level, what counts as "correct" for a function is not defined (p. 29, p. 30).
- [I] Pooled metrics are dominated by JavaScript (548 of 2,026 function-level test items) (p. 7, p. 15). C# results rest on 44 / 13 test functions (p. 7, p. 8).

## 10. Threats to validity
- Internal (confounds, leakage, selection): random function-level split, not split by CVE, project or time (p. 7); possible twin/BM25 leakage (§9); possible padding effect on line-level metrics (§9); PLMs are reproduced from original hyper-parameters, while LLM prompt templates differ across strategies (p. 11, p. 13, p. 43).
- External (generalisability of sample/context): REEF only; seven languages; short functions (≤512 tokens) (p. 6, p. 43); balanced test (50/50) by default (p. 7). The imbalanced variant (p. 39) changes the conclusion.
- Construct (do metrics measure the concept?): the line-level task presupposes a known-vulnerable function (p. 11). Labels come from fix commits (pre-change = vulnerable, post-change = clean) with known tangling noise (p. 6, p. 44). The authors report that two raters judged 92-93% of 377 extracted functions correct (p. 7).
- Statistical conclusion (power, multiple comparisons, variance): no tests, confidence intervals or seeds. Many configurations (≈30) are compared on one split, and the best is chosen post hoc. Per-language and per-CWE cells are small (e.g. C# 44/13; CWE-862 n = 1) (p. 7, p. 8, p. 30).
- Reproducibility (data/code/setup reported?): data and scripts are released (p. 48), and model versions are given for the OpenAI models (p. 15). Hyper-parameters, decoding settings and GPT fine-tuning details are not in the paper (p. 16).
- Funding: Chinese and Japanese public grants; no conflict of interest declared (p. 48).

## 11. Future research directions
- Stated by authors [A]: larger multilingual benchmarks; intermediate representations that unify code across languages; better PLM/LLM learning strategies such as multi-task learning or meta-learning to close the gap between high- and low-resource languages (p. 47); RL fine-tuning of reasoning LLMs (p. 38); line-level manual verification of labels (p. 44); adding specialised models as they support more languages (p. 43).
- Suggested by us [I]: add SAST baselines (CodeQL/Semgrep) on the same multilingual test split; split by CVE/project/time; repeat the GPT-4o ITFSP run with several seeds and BM25-overlap controls; compute line-level metrics on real lines only; evaluate realistic class ratios as the main setting.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (LLM vs DL/PLM head-to-head; no SAST), RQ2 (balanced vs imbalanced reversal; time split; pooled metrics; line-level setup), RQ3 (cost/TCO of API LLM vs local PLM; no hybrid), RQ4 (per-language, per-CWE, per-severity, function complexity), RQ5 (leakage, granularity, imbalance).
- How it informs our work [I]: one of the few multilingual, two-granularity LLM-vs-PLM comparisons. Its main lesson for the review is conditional: only a fine-tuned frontier LLM with retrieved examples beats fine-tuned PLMs, and only on balanced data. Under realistic imbalance, fine-tuned PLMs match or beat it. Prompt-only LLMs are near chance at function level. This supports a "results depend on setup" answer to RQ2.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | On balanced REEF (7 languages), fine-tuned GPT-4o + BM25 few-shot beats best PLM CodeT5P at function level (Acc 0.7196 vs 0.6037; MCC 0.4360 vs 0.2860; F1 tied 0.7069 vs 0.7075) | p. 17 | V | moderate |
| RQ1 | Prompt-only LLMs (zero-/few-shot, incl. GPT-4o, GRACE, DeepSeek-R1, QwQ-plus) are near chance at function level (Acc 0.36-0.53, MCC ≤0.07) | p. 17, p. 37 | V | moderate |
| RQ1 | Line level: GPT-4o ITFSP F1 0.6641 vs CodeT5P 0.4841 (but CodeT5P AUC 0.8644 > 0.8116) | p. 23, p. 26 | V | moderate |
| RQ2 | Under realistic imbalance (~17% vulnerable), PLMs outperform the best LLM (UniXcoder F1 0.4626 / CodeT5P MCC 0.3627 vs GPT-4o ITFSP F1 0.4010 / MCC 0.2774) — conclusion flips with class ratio | p. 40, p. 41 | V | moderate |
| RQ2 | Time-split (2024-2025) GPT-4o ITFSP keeps function-level Acc 0.7874 but line-level F1 drops to 0.3450 from 0.6641 | p. 39 | V | moderate |
| RQ2 | Random function-level split with paired vulnerable/fixed twins and BM25 few-shot retrieval from train; only exact-match dedup — possible leakage favouring ITFSP. Counter-evidence: time-split function-level Acc stays 0.7874 (retrieval pool for that run not stated); line-level drop to 0.3450 still compatible | p. 6, p. 7, p. 12, p. 38–39, p. 44 | I | weak |
| RQ2 | Line-level dummy precision 0.0267 vs ~14% vulnerable lines in dataset suggests metrics over padded 113-line slots, inflating accuracy/FPR | p. 8, p. 22, p. 23 | I | weak |
| RQ3 | GPT-4o instruction tuning costs $86.07 (function) vs ≈$5.59 per local A6000 PLM training run (~15x cheaper); authors recommend PLMs under privacy/limited hardware | p. 42 | V | moderate |
| RQ4 | GPT-4o ITFSP per-language function Acc: Go 0.8082 (best) to Python 0.6626 (worst); CodeT5P beats it in JavaScript (0.7062 vs 0.6642) | p. 21 | V | moderate |
| RQ4 | Line-level F1 by language: JavaScript 0.7815 best, C# 0.4348 worst (CodeT5P better in C#, n = 13) | p. 8, p. 26 | V | weak |
| RQ4 | Memory-safety CWEs are hardest to localise: line-level correct rate CWE-787 6.25%, CWE-119 21.74%, CWE-125 27.27% (best model) | p. 30 | V | weak |
| RQ4 | LLM-only correct functions are more complex/longer (median CC 4.0 vs 2.0; 135.5 vs 96 tokens) than PLM-only correct ones; PLM handles deeper nesting | p. 34 | V | weak |

## 14. Key quotes
> "GPT-4o with instruction tuning and few-shot prompting demonstrates superior performance, achieving the highest accuracy (0.7196) at function-level compared to the best-performing CodeT5P (0.6037)" (p. 4)

> "the PLM remains superior in overall classification balance for this imbalanced dataset." (p. 41)

> "the size of LLMs is not the decisive factor affecting performance on multilingual vulnerability detection, and the use of reasoning LLMs does not lead to significant improvements." (p. 4)

## Analyst notes
- Reading coverage: pp. 1-48 read in full (all sections, tables 1-12, threats, conclusion, declarations). The reference list (pp. 48-53) was skimmed. Figures 4, 5 and 8-10 are bar charts garbled by text extraction; we rely on the numbers the authors give in the text for them (p. 21, p. 26, p. 32, p. 34).
- Version: metadata = EMSE 2026 (DOI 10.1007/s10664-026-10832-4). The analysed text is arXiv 2506.07503v2 (10 Mar 2026), identity matched by arXiv id. The typeset journal version may differ slightly. The running header reads "W. Dong et al.", a template artifact.
- Uncertainties: (1) The padding hypothesis and the twin/BM25 leakage hypothesis (§9) are our inference from reported numbers; the replication package could settle both. (2) How GPT-3.5/GPT-4o were instruction-tuned (OpenAI fine-tuning API vs. other) is not stated; we infer the API from the Table 12 training costs (p. 41). (3) "Break-even after 58 runs" (p. 42) is reproducible as $4,650 / ($86.07 − $5.59) ≈ 57.8. It assumes a fresh GPU purchase and ignores PLM inference and engineering cost.
