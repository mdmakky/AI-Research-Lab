## Revisiting the Performance of Deep Learning-Based Vulnerability Detection on Realistic Datasets

> **Takeaway:** When four well-known deep-learning detectors scan whole real projects instead of hand-picked functions, their precision falls to 1–10%, so almost every alarm is false. Retraining on realistic data does not fix this, and the small comparison with two fine-tuned LLMs favours neither side clearly [@chakraborty2024revisiting, p. 7; @chakraborty2024revisiting, p. 9; @chakraborty2024revisiting, p. 12].

| Item | Detail |
|---|---|
| Authors | Partha Chakraborty, Krishna Kanth Arumugam, Mahmoud Alfadel, Meiyappan Nagappan, Shane McIntosh |
| Year | 2024 |
| Venue | IEEE Transactions on Software Engineering |
| Status | Peer-reviewed (journal). Our copy is the arXiv author pre-print (2407.03093v1), so page numbers follow the arXiv PDF |
| Identifier | DOI 10.1109/tse.2024.3423712; arXiv 2407.03093 |
| Paper type | Replication and re-evaluation study with a new dataset (Real-Vul) |
| Relevance to us | High (RQ1, RQ2, RQ4, RQ5) |

### In plain words
Deep-learning (DL) detectors are neural networks trained on many examples of vulnerable and safe code. Some reported scores up to 99%. But they were tested on functions taken from code changes that fixed flaws, with roughly as many vulnerable as safe examples. Real use is different. A tool scans every function in a project, and vulnerable ones are rare. The share of truly vulnerable code is called prevalence. This paper builds a test set, Real-Vul, that mimics a whole-project scan. It then re-tests four detectors on it.

### How they did it
- Detectors: LineVul, which reads code as a sequence of words using the CodeBERT model, and three graph-based models (DeepWukong, ReVeal, IVDetect) [@chakraborty2024revisiting, p. 4; @chakraborty2024revisiting, p. 5]. Graph-based models turn code into a network of statements and data flows.
- Step 1: re-run each model on its original dataset with a random 80/20 split [@chakraborty2024revisiting, p. 5; @chakraborty2024revisiting, p. 6].
- Step 2: test those models on Real-Vul (RQ1). Step 3: retrain them on Real-Vul, with and without balancing the classes (RQ2) [@chakraborty2024revisiting, p. 6; @chakraborty2024revisiting, p. 8].
- Step 4: side analyses, including "dead-code" augmentation, results per weakness group and severity, and two fine-tuned LLMs [@chakraborty2024revisiting, p. 10; @chakraborty2024revisiting, p. 12]. Dead-code augmentation adds harmless unused code to training examples so the model learns to ignore surface details.
- No static analysis tool was tested [@chakraborty2024revisiting, p. 13].

### Data and setup
- Real-Vul uses the 10 projects with the most vulnerabilities in the BigVul dataset, including Chromium, Linux, FFmpeg and OpenSSL. They cover 73% of BigVul's vulnerable samples [@chakraborty2024revisiting, p. 3; @chakraborty2024revisiting, p. 4].
- It has 5,528 vulnerable functions (4,418 train, 1,110 test) and 1,682,713 "uncertain" functions (769,464 train, 913,249 test) [@chakraborty2024revisiting, p. 4].
- "Uncertain" means every other function in the project snapshot that does not match a known vulnerable function. These are not proven safe [@chakraborty2024revisiting, p. 4].
- Time split: vulnerable functions are sorted by fix date; the first 80% train the model and the last 20% test it [@chakraborty2024revisiting, p. 4].
- Training was not repeated; the authors say repeats were not feasible [@chakraborty2024revisiting, p. 13]. LLM fine-tuning settings are not reported [@chakraborty2024revisiting, p. 12]. Data and scripts are released [@chakraborty2024revisiting, p. 2].

### Key findings
- [V] On their original data, DeepWukong reaches F1 93% and LineVul 90% [@chakraborty2024revisiting, p. 6]. F1 balances precision (share of alarms that are real) and recall (share of real flaws found).
- [V] On Real-Vul, precision falls to 1% (DeepWukong, LineVul), 2% (IVDetect) and 10% (ReVeal), while recall stays at 80–90%. F1 is 2–17% [@chakraborty2024revisiting, p. 7].
- [V] Precision drops by up to 95 percentage points and F1 by up to 91 points [@chakraborty2024revisiting, p. 1; @chakraborty2024revisiting, p. 7].
- [V] Retrained on Real-Vul as is, DeepWukong and LineVul label everything as not vulnerable: F1 0% and AUC 50% [@chakraborty2024revisiting, p. 8]. AUC measures how well a model ranks vulnerable above safe code; 50% is coin-flip level.
- [V] Retrained on balanced data, F1 is 2–36% and AUC 51.3–52.3% [@chakraborty2024revisiting, p. 9].
- [V] Dead-code augmentation lifts LineVul F1 from 20% to 46% and AUC from 51.4% to 81.8% [@chakraborty2024revisiting, p. 10].
- [V] Fine-tuned CodeLlama reaches F1 42% and AUC 67%; Mixtral reaches F1 46% and AUC 71%. [A] The authors conclude that LineVul outperforms general LLMs [@chakraborty2024revisiting, p. 12].
- [V] Information-leak flaws are found best (F1 up to 33.6%). High-severity flaws are hardest (F1 9.06–10.89%) [@chakraborty2024revisiting, p. 11].

### Limitations and weaknesses
- [A] The authors note that some BigVul labels may be wrong, only 10 projects are used, "uncertain" functions may hide real flaws, balancing used one random sample, and only DL models were tested [@chakraborty2024revisiting, p. 13].
- [I] Some numbers do not fit together. IVDetect shows precision 39% and recall 63% but F1 24% [@chakraborty2024revisiting, p. 6]. Project sizes total 270,919 functions, while the text gives 1,682,713 uncertain functions [@chakraborty2024revisiting, p. 4; @chakraborty2024revisiting, p. 13]. The story holds, but exact figures are less reliable.
- [I] The LLM comparison is thin. Mixtral's F1 (46%) equals augmented LineVul's; only AUC favours LineVul. The LLM results also seem to come from a less imbalanced test set, which is not described [@chakraborty2024revisiting, p. 10; @chakraborty2024revisiting, p. 12].
- [I] Vulnerable labels come from BigVul, where an independent audit found only 39% correct [@risse2025top, p. 8].
- [I] There are no confidence intervals for the main results. False-positive counts use different units per model, so they cannot be compared directly [@chakraborty2024revisiting, p. 7].

### Gaps and future work this paper leaves open
- Gap G2 (no same-benchmark comparison of LLMs, static analysis and DL on realistic code): [A] the authors themselves ask for static and dynamic analysis tools to be tested on Real-Vul [@chakraborty2024revisiting, p. 13]. Real-Vul could serve as that benchmark.
- Gap G1 (results not re-scored at realistic prevalence): this paper shows why prevalence matters. Its precision figures are the kind of number most studies never report [I].
- [A] Other author directions: better detection of high-severity flaws and better LLM specificity, meaning fewer false alarms on safe code [@chakraborty2024revisiting, p. 11; @chakraborty2024revisiting, p. 12].

### Why it matters for your research
This is the strongest evidence in our set that realistic prevalence destroys precision (RQ2). It also gives results per weakness group and severity (RQ4). If you compare tools, always report precision at a realistic share of vulnerable code, not only F1 on balanced data.

### Connections to other papers
- Agreement G1 (realistic evaluation collapses performance): ding2025vulnerability finds the same with cleaner labels [@ding2025vulnerability, p. 7]; lu2025lab finds ReVeal and LineVul at F1 3.47–8.65 on 2025 vulnerabilities [@lu2025lab, p. 13].
- Agreement G2 (noisy labels): this paper's 15% inconsistency in ReVeal [@chakraborty2024revisiting, p. 3] sits beside risse2025top's 39–65% correct labels [@risse2025top, p. 8].
- ding2025vulnerability focuses on wrong labels and copies; this paper focuses on prevalence. Together they explain most of the gap between lab and real scores [I].

