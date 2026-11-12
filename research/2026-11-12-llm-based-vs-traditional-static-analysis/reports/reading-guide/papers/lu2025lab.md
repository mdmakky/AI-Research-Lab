## From Lab to Reality: A Practical Evaluation of Deep Learning Models and LLMs for Vulnerability Detection

> **Takeaway:** On real Linux and Chromium vulnerabilities disclosed from May 2025, deep-learning detectors that scored F1 above 90 in the lab fall to F1 3.47–8.65, and four open LLMs score 0.79–5.36 [@lu2025lab, p. 12; @lu2025lab, p. 13; @lu2025lab, p. 14]. By our calculation, simply flagging every function would score about 3.87, so both families sit close to that "flag everything" level.

| Item | Detail |
|---|---|
| Authors | Chaomeng Lu, Bert Lagaisse |
| Year | 2025 (arXiv); 2026 (journal) |
| Venue | Journal of Systems and Software (2026); first posted on arXiv |
| Status | Peer-reviewed (JSS 2026); our copy is the arXiv accepted manuscript (v4), so page numbers follow arXiv v4 |
| Identifier | DOI 10.1016/j.jss.2026.113185 (journal, checked via Crossref on 2026-11-12); arXiv 2512.10485 |
| Paper type | Empirical evaluation with a new benchmark (VentiVul) |
| Relevance to us | High (RQ1, RQ2, RQ4, RQ5) |

### In plain words
Vulnerability detectors often look excellent on standard test sets. This paper asks whether that holds in "the real world". The authors collect brand-new vulnerabilities, published after the models were built. This is called temporal separation: the test data comes from a later time than the training data. Data from a different source or period is called out-of-distribution. They then test two kinds of model. Deep-learning (DL) detectors are neural networks trained on older labelled code. Large language models (LLMs) are big general AI models, here used without any extra training.

### How they did it
- Stage 1: check whether the models' internal view of code separates vulnerable from safe code, using t-SNE, a method that draws complex data as a 2D picture [@lu2025lab, p. 6; @lu2025lab, p. 8].
- Stage 2: train four DL models on each of four datasets and test each on all four. This compares "same dataset" with "different dataset" results [@lu2025lab, p. 7].
- Stage 3: test on the new VentiVul set. Only two DL models (ReVeal, LineVul) were taken to this stage [@lu2025lab, p. 7].
- LLMs: Qwen2.5-Coder-32B, DeepSeek-Coder-V2-Lite, Qwen3-30B-A3B (thinking turned off) and Mistral-Small-24B. All are open-weight (downloadable) and were released before May 2025 [@lu2025lab, p. 5; @lu2025lab, p. 8].
- Prompts: zero-shot (instructions only), few-shot (with worked examples) and chain-of-thought (asked to reason step by step) [@lu2025lab, p. 8].
- Every model sees one function at a time, with no surrounding code [@lu2025lab, p. 7; @lu2025lab, p. 8].
- Scores: F1 balances precision (share of alarms that are real) and recall (share of real flaws found). CDR is the share of vulnerabilities where at least one affected function is flagged. PACC is the share of pairs where the vulnerable version is flagged and its fixed version is not [@lu2025lab, p. 9].
- For LLMs, "conservative" scoring counts unreadable answers as wrong [@lu2025lab, p. 8].

### Data and setup
- Training sets, all C/C++: Juliet (synthetic, 253,002 functions, 37% vulnerable), Devign (27,318, 46%), BigVul (188,636, 6%) and ICVul (15,396, 41%) [@lu2025lab, p. 3]. ICVul is the authors' own dataset [I].
- VentiVul: 100 CVEs each from Linux and Chromium, disclosed from 1 May 2025 and checked by hand [@lu2025lab, p. 4]. A CVE is a public ID for a known vulnerability.
- It holds 13,326 functions, 200 CVEs, 39 CWEs and 263 vulnerable–fixed pairs. Other functions from the same files are labelled not vulnerable, to keep a realistic mix [@lu2025lab, p. 4]. A CWE is a standard weakness category.
- [I] By our calculation, 263 of 13,326 functions (1.97%) are vulnerable.
- LLMs ran with temperature 0 and seed 42, so each answer is repeatable [@lu2025lab, p. 8]. Data and code are public [@lu2025lab, p. 2].

### Key findings
- [V] In the lab, LineVul reaches F1 94.52 on Juliet and 91.00 on BigVul [@lu2025lab, p. 11; @lu2025lab, p. 12].
- [V] Accuracy can hide failure. On BigVul, ReVeal, Devign and VulBERTa reach accuracy 87.45, 94.09 and 94.39 but F1 only 23.58, 16.90 and 0.19 [@lu2025lab, p. 11].
- [V] Across datasets, LineVul trained on BigVul scores F1 0 on Juliet, 1.90 on Devign and 13.05 on ICVul [@lu2025lab, p. 12].
- [V] On VentiVul, the 8 DL setups score F1 3.47–8.65. The best is ReVeal trained on BigVul (precision 5.25%, recall 24.43%) [@lu2025lab, p. 13].
- [V] The LLMs score conservative F1 0.79–5.36. The best is Mistral few-shot (F1 5.36, CDR 46%, PACC 5.75%) [@lu2025lab, p. 13; @lu2025lab, p. 14]. LLM precision and recall are not reported.
- [I] Flagging every function would give F1 about 3.87. Seven of the 12 LLM results fall below that, and all DL results are at most 4.8 points above it (our calculation from [@lu2025lab, p. 4; @lu2025lab, p. 13; @lu2025lab, p. 14]).
- [V] Finding a CVE is not the same as understanding it. Some DL setups reach CDR 94.59–100% but PACC 0–0.76% [@lu2025lab, p. 13]. [I] All PACC values (5.75% or less) are far below the up to 25% a random labeller could reach.
- [V] Prompting effects vary: few-shot helps only Mistral [@lu2025lab, p. 13].

### Limitations and weaknesses
- [A] The authors note: few models and no commercial LLMs; release dates cannot rule out that LLMs saw this code during training; C/C++ only; "unrelated" functions may hide flaws; and VentiVul does not include every vulnerability in those versions [@lu2025lab, p. 17].
- [I] The paper reports no simple baseline, such as "flag everything", so its weak results are never compared with chance.
- [I] The DL vs LLM comparison is uneven. DL models were trained; the LLMs were mid-size open models with no extra training and Qwen3's thinking mode turned off [@lu2025lab, p. 8]. Nothing here speaks to frontier or fine-tuned LLMs.
- [I] There are single runs and no confidence intervals, and the families were scored on slightly different function sets [@lu2025lab, p. 7; @lu2025lab, p. 8].
- [I] No static analysis tool is tested, although the introduction frames learning methods as a complement to static analysis [@lu2025lab, p. 1]. We read the arXiv copy, not the paywalled journal version.

### Gaps and future work this paper leaves open
- Gap G1 (no shared protocol with trivial baselines): the "flag everything" comparison above is ours, not the paper's. [A] The authors ask for cross-dataset and time-separated testing plus pair-based scores [@lu2025lab, p. 16].
- Gap G2 (no same-benchmark LLM vs static analysis vs DL comparison on new code): this is post-cutoff evidence, but without a static analysis arm. The gap report suggests a low-cost study that reuses VentiVul and adds a static analysis arm, an LLM with file context and a "flag everything" baseline [I].
- Gap G5 (missing languages): VentiVul is C/C++ only [@lu2025lab, p. 17].

### Why it matters for your research
This is peer-reviewed evidence that lab scores do not survive new, real vulnerabilities (RQ1, RQ2). It also varies by project, which matters for RQ4: LineVul trained on BigVul finds 76% of Chromium CVEs but none in Linux [@lu2025lab, p. 13]. Its public data makes it a good base for a first study of your own.

### Connections to other papers
- Agreement G1 (realistic tests collapse scores): see ding2025vulnerability [@ding2025vulnerability, p. 7] and chakraborty2024revisiting [@chakraborty2024revisiting, p. 7].
- Agreement G10 (trivial baselines are competitive): deininger2026open finds an always-vulnerable F1 of 0.523 against LLM F1 0.405–0.615 [@deininger2026open, p. 7]; tashenova2026real finds a similar result in PHP [@tashenova2026real, p. 8].
- Contradiction C7: LineVul scores F1 91.00 on BigVul here, but ding2025vulnerability reports 62.88 for CodeBERT [@ding2025vulnerability, p. 7]. [I] Lab BigVul numbers are not comparable across papers.
- Contradiction C8: a fine-tuned detector in deininger2026open holds balanced accuracy 0.765 on later PrimeVul data [@deininger2026open, p. 11], unlike the collapse here. Unresolved.
- ding2025vulnerability also finds pair scores far below random (22.70%) [@ding2025vulnerability, p. 9].

