## A Real CVE-Backed Benchmark for WordPress Plugin Vulnerability Detection: Re-Evaluating Static and Learning-Based Detectors Under Leakage-Controlled Evaluation

> **Takeaway:** On real PHP vulnerabilities in WordPress plugins, with copies removed, no detector does well (best macro-F1 0.601), a one-number "function length" baseline almost matches the neural models, and only 48.8% of cleaned "vulnerable" labels are genuine [@tashenova2026real, p. 8; @tashenova2026real, p. 11]. Its static analyser is an unnamed in-house tool that misses about 98% of vulnerabilities, so it says nothing about standard PHP static analysis tools, and no LLM was tested [@tashenova2026real, p. 13].

| Item | Detail |
|---|---|
| Authors | Zhuldyz Tashenova, Aisultan Aitmagambetuly, Altyn Urynbassarova, Askhat Zhetkerbay, Shirin Amanzholova, Akerke Kerim |
| Year | 2026 |
| Venue | Big Data and Cognitive Computing |
| Status | Peer-reviewed (journal article) |
| Identifier | DOI 10.3390/bdcc10090303 |
| Paper type | Benchmark construction and comparative evaluation (in-house static analyser, classical machine learning, neural models, trivial baselines; no LLMs) |
| Relevance to us | Medium (RQ2 mainly; RQ1 for static analysis vs machine learning only; RQ4; RQ5) |

### In plain words
WordPress is a widely used website system. Its plugins are add-ons written in PHP, a web programming language. Many plugins have publicly reported vulnerabilities. The same authors earlier reported about 93% accuracy on 600 synthetic code snippets [@tashenova2026real, p. 2]. This paper re-checks that claim on real vulnerabilities, after carefully removing duplicate code. It is partly a self-correction after reviewers audited the first data release [@tashenova2026real, p. 2; @tashenova2026real, p. 14]. The result is sobering: real performance is far lower.

### How they did it
- Ten detector setups were tested with five-fold cross-validation grouped by plugin [@tashenova2026real, p. 5; @tashenova2026real, p. 6]. Cross-validation splits the data into five parts; each part serves once as the test set. Grouping by plugin keeps all code from one plugin in the same part.
- Static analysis arm: a "two-pass intra-procedural analyzer" that does taint tracking [@tashenova2026real, p. 5]. Taint tracking follows untrusted user input to see if it reaches a dangerous operation without being cleaned. Intra-procedural means it looks inside one function only. The tool is unnamed and unversioned; the authors call it "intra-procedural and lexical" [@tashenova2026real, p. 13].
- Classical machine learning: Random Forest and a linear SVM, fed counts of short character sequences (TF-IDF) [@tashenova2026real, p. 5; @tashenova2026real, p. 6].
- Neural models: LSTM variants, a type of network that reads code as a sequence, plus one model that combines the taint verdict with an LSTM [@tashenova2026real, p. 5].
- Three trivial baselines: always predict the most common class, a simple source/sink rule, and a one-feature model using only function length in tokens [@tashenova2026real, p. 5].
- No LLMs or transformer models were run. CodeBERT was skipped because the machine had no GPU [@tashenova2026real, p. 13].

### Data and setup
- 1757 CVEs in 1281 plugins could be rebuilt as before-fix and after-fix code. About 54% of indexed CVEs were lost because old versions were deleted [@tashenova2026real, p. 3]. A CVE is a public ID for a known vulnerability.
- Labels come from the fix: functions changed by the fix are "vulnerable". Variant A uses the fixed version as the safe example; Variant B uses untouched functions from the same plugin [@tashenova2026real, p. 3].
- Copies and near-copies were removed. Final folds share no code hashes, no clone families and no plugins. This left 15,294 (A) and 24,917 (B) functions from 30,860 each [@tashenova2026real, p. 4; @tashenova2026real, p. 5].
- [I] By our calculation, 74.5% (A) and 46.2% (B) of functions are vulnerable, far more than in real code.
- There is no time-based split [@tashenova2026real, p. 3]. Everything ran on CPU with one random seed [@tashenova2026real, p. 6; @tashenova2026real, p. 7]. Labels and folds are released [@tashenova2026real, p. 14].

### Key findings
- [V] The best binary macro-F1 is 0.563 (A, SVM) and 0.601 (B, stacked model). No neural model leads in any of six settings [@tashenova2026real, p. 7; @tashenova2026real, p. 8]. Macro-F1 averages the F1 score of the "safe" and "vulnerable" classes; F1 balances false alarms and misses.
- [V] The function-length baseline matches or beats the Random Forest in 4 of 6 settings. On Variant B it scores 0.572, against 0.573 for the Bi-LSTM and 0.578 for the best neural model [@tashenova2026real, p. 8].
- [V] The in-house taint analyser finds only 1.7–1.8% of vulnerabilities [@tashenova2026real, p. 9]. Its macro-F1 is 0.366 against 0.350 for always guessing the common class on Variant B, and below that baseline on Variant A [@tashenova2026real, p. 8].
- [A] The authors say this low recall "reflects that implementation rather than taint analysis in general" [@tashenova2026real, p. 13].
- [V] Aggregate scores hide broken models. On Variant A the Random Forest calls 15,068 of 15,294 functions vulnerable; its accuracy (0.747) barely beats always guessing (0.745) [@tashenova2026real, p. 9].
- [V] An expert review of 400 functions found only 48.8% of cleaned "vulnerable" labels genuine [@tashenova2026real, p. 11].
- [V] Before cleaning, 166 (A) and 151 (B) groups of duplicate code crossed folds, and 730 and 456 groups had conflicting labels. Cleaning cut the data by 50.4% (A) and 19.3% (B) [@tashenova2026real, p. 4; @tashenova2026real, p. 5].

### Limitations and weaknesses
- [A] The authors note: copies are controlled, but not provably all removed; lost CVEs may bias the sample; rare classes are unreliable; neural models were small and CPU-trained; no transformer was tested; labels are only about half right; one annotator did the expert review [@tashenova2026real, p. 11; @tashenova2026real, p. 13].
- [I] The static analysis arm is too weak to stand for PHP static analysis in general. No established PHP tool was run. Do not quote the "misses about 98%" figure as a statement about static analysis tools.
- [I] Label accuracy of the full test data is not reported and is probably below 48.8%, since that figure is for the cleaned subset [@tashenova2026real, p. 11].
- [I] Macro-F1 cannot be compared with the vulnerable-class F1 used by most other papers. Testing is per function, never at realistic prevalence (the true share of vulnerable code).
- [I] One seed and overlapping confidence intervals mean many model gaps may be noise [@tashenova2026real, p. 8]. The earlier ~93% claim should not be cited [@tashenova2026real, p. 2].

### Gaps and future work this paper leaves open
- Gap G1 (no shared protocol with trivial baselines): [A] the authors say future detectors "should be required to clear such trivial baselines" [@tashenova2026real, p. 13].
- Gap G2 (no fair three-family comparison): this is PHP evidence without an LLM or a standard static analysis tool.
- Gap G5 (no real-CVE LLM vs standard static analysis evidence for PHP and Go): this is the only PHP study in our corpus. Its released expert-checked subset of 125 vulnerable and 247 safe functions is a ready data source [@tashenova2026real, p. 11]. [I] The gap report notes LLM-only WordPress evidence elsewhere that we know only from an abstract.

### Why it matters for your research
For RQ2 it shows that leakage, label noise and model stacking shape scores more than the model type does. For RQ4 it adds PHP, where learned models find XSS (script injection) much better than rare remote-code-execution flaws [@tashenova2026real, p. 9]. It is also the natural starting point if you study gap G5.

### Connections to other papers
- Agreement G2 (noisy labels): matches risse2025top [@risse2025top, p. 8] and ding2025vulnerability [@ding2025vulnerability, p. 4].
- Agreement G10 (trivial baselines are competitive): see deininger2026open [@deininger2026open, p. 7], lu2025lab [@lu2025lab, p. 14] and shu2026evaluating [@shu2026evaluating, p. 11]; risse2025top's word-count model makes the same point [@risse2025top, p. 11].
- Contradiction C5 (class balance flips results): here, changing how safe examples are chosen flips which way the same Random Forest fails [@tashenova2026real, p. 9].
- Agreement G1 (realistic tests collapse scores): [I] its best macro-F1 of 0.601 fits the pattern seen in C/C++ [@tashenova2026real, p. 8].

