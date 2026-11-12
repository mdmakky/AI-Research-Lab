## Open or Frontier? A Cost- and Energy-Aware Benchmark of Large Language Models for Software Vulnerability Detection

> **Takeaway:** On the same 1,549 real C/C++ functions, a small fine-tuned CodeBERT beat all eight zero-shot LLMs, and at the real-world rate of about one vulnerable function per 44 safe ones every LLM's precision (2.3–3.8%, or 2.8–4.6% in a budget-matched re-run) was barely above flagging everything (2.21%). Open models matched or beat frontier models at a small fraction of the cost.

| Item | Detail |
|---|---|
| Authors | Patrick Deininger, Wolfgang Slany |
| Year | 2026 |
| Venue | Computers (journal) |
| Status | Peer-reviewed |
| Identifier | DOI 10.3390/computers15090623 |
| Paper type | Empirical benchmark with cost and energy measurement |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ5 |

### In plain words
Companies can use frontier LLMs (the newest paid models, such as Claude, GPT and Gemini) or open-weight LLMs (models whose files are public, so anyone can run them). This paper asks which is better for finding vulnerable code, counting money and electricity as well as accuracy. It also tests three classic static analysis (SAST) tools and two CodeBERT detectors on the very same functions. CodeBERT is a small deep-learning model that can be fine-tuned, meaning given extra training on labelled examples.

Note that the paper does include SAST (Flawfinder, Cppcheck and Semgrep). That makes it one of very few studies that test all three families on identical code.

### How they did it
Each model gets one C/C++ function and must answer YES or NO: does it contain a vulnerability? The LLMs were used zero-shot (no examples, no extra training), at temperature 0, which makes answers as repeatable as possible [@deininger2026open, p. 6]. The main score is balanced accuracy, the average of the share of vulnerable functions caught and the share of safe functions correctly cleared. It is used because both trivial rules, "always safe" and "always vulnerable", score exactly 0.5 on it [@deininger2026open, p. 6].

The authors then re-scored everything at the natural prevalence of 1:44. Prevalence is how common vulnerable code is; here about one vulnerable function for every 44 safe ones [@deininger2026open, p. 8]. Differences are tested with a paired bootstrap (resampling to see whether a gap could be chance) and corrected for running many comparisons [@deininger2026open, p. 6].

### Data and setup
- The data is PrimeVul, a C/C++ dataset with carefully cleaned labels. Its test split has 24,788 functions, 549 of them vulnerable [@deininger2026open, p. 4].
- The sample is all 549 vulnerable plus 1,000 random safe functions, 1,549 in total [@deininger2026open, p. 4]. [I] That is 35.4% vulnerable, not 50/50, although the text once calls it "balanced by construction" [@deininger2026open, p. 8].
- Eight LLMs were tested: three frontier (Claude Sonnet 5, GPT-5.1, Gemini 3.1 Pro) and five open-weight (DeepSeek-V3.2, GLM-5, Llama-3.3-70B, Qwen3-Coder-30B, Gemma-3-4B) [@deininger2026open, p. 4].
- SAST: Flawfinder 2.0.20, Cppcheck 2.21 and Semgrep 1.175 [@deininger2026open, p. 10]. CodeQL could not run, because isolated functions cannot be built (compiled) [@deininger2026open, p. 10].
- Energy was measured on a GPU for some open models and estimated from computation counts (FLOP estimates) for the rest [@deininger2026open, p. 5].

### Key findings
- [V] LLM balanced accuracy is 0.511–0.676 in the first run, with DeepSeek-V3.2 best [@deininger2026open, p. 7], and 0.568–0.711 in a second, budget-matched run seven weeks later [@deininger2026open, p. 17].
- [V] A fine-tuned CodeBERT (125 million parameters) beats every LLM, with balanced accuracy 0.765 [@deininger2026open, p. 11]. With the default decision rule it looked like an "always safe" classifier, despite a ROC-AUC (ranking quality, independent of the cut-off) of 0.845; the authors nearly reported this artefact as a real result [@deininger2026open, p. 11].
- [V] Precision is the share of warnings that are real flaws. At 1:44 prevalence, every LLM's precision is 2.3–3.8%, against 2.21% for flagging everything. Each true finding comes with 25.6–41.9 false alarms [@deininger2026open, p. 8]. In the budget-matched run, precision is 2.8–4.6% [@deininger2026open, p. 17].
- [V] SAST is more precise but finds little. At 1:44, Semgrep's precision is 26.0% (95% confidence interval 5.7–66.9%) and Flawfinder's is 6.2–13.4%; Cppcheck (2.46–3.77%) sits in the LLM range [@deininger2026open, p. 10]. Semgrep flagged only 19 of 1,549 functions [@deininger2026open, p. 11].
- [V] The open model DeepSeek-V3.2 significantly beats all three frontier models, by 0.054–0.060 balanced accuracy [@deininger2026open, p. 27]. In the second run, the small Gemma-3-4B matches Claude's quality at 1/66 of the cost [@deininger2026open, p. 17].
- [V] Rewording the prompt moves balanced accuracy by up to 0.088 and produces three different winners [@deininger2026open, p. 20].
- [V] Compute cost per true positive (a correctly flagged vulnerable function) at 1:44 is USD 0.003–0.212, and energy is 3.7–119.6 kJ [@deininger2026open, p. 8]. [V] Caveat: the kJ values for Qwen and Llama come from FLOP estimates, not from the measured 88 J and 738 J per task [@deininger2026open, p. 7; @deininger2026open, p. 14].
- [V] Recall is 7–15 points higher on pre-2020 vulnerabilities than on 2021–2022 ones, which the authors call "consistent with some memorization" [@deininger2026open, p. 24].

### Limitations and weaknesses
- [I] The SAST arm is lightweight, function-level tools only. There is no CodeQL or other whole-program analyser, so this is not a test against the strongest SAST.
- [A] All vulnerabilities date from 2008–2022 and predate the models' training cutoff, so scores may be optimistic [@deininger2026open, p. 24].
- [A] CodeBERT was trained on PrimeVul's own training data, while the LLMs had none; the authors say the two need different prerequisites [@deininger2026open, p. 11].
- [A] One dataset, one language family, function level only [@deininger2026open, p. 25].
- [V] LLM inputs were cut at 8,000 characters, which affects 15.8% of the vulnerable functions [@deininger2026open, p. 4].
- [I] Cost per true positive leaves out human checking time. With 25.6–41.9 false alarms per real find, analyst time would plausibly dominate the cost of a few cents.
- [I] Revision left some prose inconsistencies, so cite table values rather than the text.

### Gaps and future work this paper leaves open
- [A] The authors plan tests on vulnerabilities newer than the models' training cutoff, a second dataset, other languages and line-level localisation [@deininger2026open, p. 24; @deininger2026open, p. 25].
- [I] Gap G1: it reports trivial baselines and realistic-prevalence scores for its own results, but does not re-score other studies.
- [I] Gap G2 is narrowed by this paper. A function-level C/C++ three-family test now exists. Still missing: code newer than the training cutoff, file or repository context, and a semantic SAST tool such as CodeQL.
- [I] Gap G6 is narrowed too. Compute cost per true positive now exists for eight LLMs. Still missing: human triage time and a costed SAST and DL arm.
- [I] Gap G5: no PHP or Go.

### Why it matters for your research
This is the strongest single answer in our set to RQ1, because all three families face identical functions with proper statistics. It shows that the winner depends on the metric. On balanced accuracy, fine-tuned CodeBERT leads and LLMs beat lightweight SAST. On precision at a realistic vulnerability rate, Flawfinder and Semgrep beat every LLM. The paper's own verdict is that none of the methods is ready for independent use [@deininger2026open, p. 26]. It is also the only paper here that prices each true finding.

### Connections to other papers
- Contradiction C1 (fine-tuned vs GPT-4): its CodeBERT win and decision-rule artefact may help explain why fine-tuned models look near chance in ding2025vulnerability [@ding2025vulnerability, p. 9].
- Contradiction C3: on balanced accuracy LLMs beat lightweight SAST; on realistic precision they lose. This fits the small-code LLM wins [@gnieciak2025large, p. 10] and the project-scale noise in li2026llm [@li2026llm, p. 11].
- Contradiction C4: reasoning helps frontier models but lowers DeepSeek's specificity from 0.52 to 0.37 [@deininger2026open, p. 20], against CASTLE's claim [@dubniczky2025castle, p. 14].
- Contradiction C8: its time-split CodeBERT holds up, while DL detectors collapse on 2025 vulnerabilities in lu2025lab [@lu2025lab, p. 13].
- Agreement G1 and agreement G10: performance collapses at realistic prevalence, and trivial baselines are competitive, as in lu2025lab and tashenova2026real [@lu2025lab, p. 14; @tashenova2026real, p. 8].
- Agreement G11 (cost per true positive) rests on this single study.
