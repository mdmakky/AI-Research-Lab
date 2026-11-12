## Top Score on the Wrong Exam: On Benchmarking in Machine Learning for Vulnerability Detection

> **Takeaway:** In three popular C/C++ benchmarks, only 39–65% of functions labelled "vulnerable" really are, and every truly vulnerable function needed code outside it to judge. A simple word-counting model gets close to top published scores, so high benchmark scores are weak evidence that a detector understands vulnerabilities [@risse2025top, p. 8; @risse2025top, p. 9; @risse2025top, p. 11].

| Item | Detail |
|---|---|
| Authors | Niklas Risse, Jing Liu, Marcel Böhme |
| Year | 2025 |
| Venue | Proceedings of the ACM on Software Engineering (FSE 2025) |
| Status | Peer-reviewed. Our copy is the arXiv version (2408.12986v2), so page numbers follow the arXiv PDF |
| Identifier | DOI 10.1145/3728887; arXiv 2408.12986 |
| Paper type | Literature survey (81 papers), manual expert labelling study, and a simple-model probe experiment |
| Relevance to us | High (RQ2, RQ3, RQ5) |

### In plain words
Machine learning for vulnerability detection (ML4VD) trains models to find security flaws in code. Most of this research asks one question: "given one function, does it contain a flaw?" A function is a small, named block of code. This paper asks whether that question even makes sense. Two security experts checked samples from popular benchmarks by hand. Benchmarks are the shared test collections everyone reports scores on. The authors also built a deliberately simple model that only counts words. If such a model scores well, the benchmark is rewarding shortcuts rather than real understanding.

### How they did it
- Survey: they searched 2020–2024 papers at top software engineering and security venues. Over 2,500 candidates were narrowed to 81 papers; one co-author did the screening [@risse2025top, p. 3; @risse2025top, p. 4].
- Expert labelling: two security researchers (3 and 5 years of experience) judged each function with a 15-minute limit. They read the code change that fixed the flaw and, where available, the CVE report [@risse2025top, p. 6; @risse2025top, p. 7]. A CVE is a public ID for a known vulnerability.
- Agreement was 82% (Cohen's kappa 0.64) on vulnerable vs secure and 98% (kappa 0.96) on context dependence [@risse2025top, p. 6]. Cohen's kappa measures agreement beyond chance: 0 is chance level, 1 is perfect.
- Context test: for functions labelled "secure", they tried to write calling code that would make the function vulnerable [@risse2025top, p. 10].
- Probe: a Gradient Boosting classifier, a standard simple method that combines many small decision trees, trained on word counts only [@risse2025top, p. 7; @risse2025top, p. 11].
- No LLM or static analysis tool was tested [@risse2025top, p. 7].

### Data and setup
- Benchmarks: BigVul, Devign and DiverseVul, all C/C++ [@risse2025top, p. 6].
- 100 "vulnerable" functions per benchmark (300 in total) from 80 projects, plus 30 "secure" functions per benchmark (90 in total) [@risse2025top, p. 6; @risse2025top, p. 10].
- Share of vulnerable functions: Devign 47.9%, BigVul 4.5%, DiverseVul 5.4% [@risse2025top, p. 7].
- Labelling took over 150 hours; the probe ran in 30 minutes on a laptop [@risse2025top, p. 6; @risse2025top, p. 11]. Probe settings and exact data splits are not reported in the paper text. Labels and scripts are released [@risse2025top, p. 13].

### Key findings
- [V] 88% of the 81 surveyed papers frame the task as a yes/no decision on one function, rising to 95% in 2024 [@risse2025top, p. 5].
- [V] Only 39% (BigVul), 47% (Devign) and 65% (DiverseVul) of sampled "vulnerable" functions really are vulnerable [@risse2025top, p. 8].
- [V] A common reason for wrong labels is that a function was changed only as a side effect of the fix (48%, 38% and 66% of wrong labels) [@risse2025top, p. 8].
- [V] All 151 truly vulnerable functions needed context from outside the function. Most often this was other functions they call (43–52%) or the values passed in (40–47%) [@risse2025top, p. 9].
- [V] For 82 of 90 "secure" functions, the authors could write a caller that makes the function vulnerable [@risse2025top, p. 10].
- [V] The word-count model reaches F1 0.86 on BigVul against a best published 0.96, and 0.62 on Devign against 0.68. On DiverseVul it reaches only 0.11 against 0.48 [@risse2025top, p. 11]. F1 is a 0–1 score balancing false alarms and missed flaws.
- [A] The authors conclude "there is currently no evidence that ML4VD techniques are actually capable of identifying security vulnerabilities at the function-level" [@risse2025top, p. 2].
- [A] They argue that static analysis limited to one function faces the same context problem, and that combining static analysis with machine learning is promising [@risse2025top, p. 12].

### Limitations and weaknesses
- [A] The authors list: random samples of 100 per benchmark, subjective labelling, only three mainly-C benchmarks, only the function-level question, and only one kind of shortcut (word counts) [@risse2025top, p. 11; @risse2025top, p. 12]. The probe shows the data can be exploited, not that top models actually exploit it [@risse2025top, p. 11].
- [A] "Secure" functions were not checked to be truly safe [@risse2025top, p. 10].
- [I] The context rule is very broad. Almost any function that uses a pointer can be made vulnerable by a hostile caller (for example one passing NULL) [@risse2025top, p. 10]. So the 151-of-151 and 82-of-90 results say more about how the question is framed than about any detector.
- [I] The best published scores were copied from other papers, not re-run on the same splits [@risse2025top, p. 7].
- [I] The shortcut argument is weak for DiverseVul, where word counts do poorly [@risse2025top, p. 11].
- [I] With 100 functions per benchmark, label figures carry about plus or minus 10 points of uncertainty. A kappa of 0.64 is only "substantial" agreement. A single person screened the survey.

### Gaps and future work this paper leaves open
- Gap G1 (no shared evaluation protocol with trivial baselines): a word-count model near the top score shows why every result needs a simple baseline [@risse2025top, p. 11].
- Gap G2 (no fair, context-aware three-family comparison): missing context is the root problem here. The gap report's study design borrows this paper's two-rater manual check with Cohen's kappa [I].
- [A] Authors' future work: let models abstain, use other units (lines, files, slices across functions), give the whole repository as context, and combine static analysis with ML [@risse2025top, p. 12; @risse2025top, p. 13].

### Why it matters for your research
This paper explains why a high F1 on BigVul or Devign proves little. For RQ2, it is a central source on label noise and on missing context. For RQ3 and RQ5, it argues for context-aware and hybrid methods, but tests neither. If you build your own test set, verify labels by hand with two raters and report a simple baseline.

### Connections to other papers
- Agreement G2 (noisy labels): ding2025vulnerability finds 24–36% correct labels in its own audit [@ding2025vulnerability, p. 4]; tashenova2026real finds 48.8% genuine in PHP [@tashenova2026real, p. 11]; chakraborty2024revisiting finds 15% of ReVeal's vulnerable samples also listed as non-vulnerable [@chakraborty2024revisiting, p. 3].
- Agreement G6 (missing context): ahmed2026secvuleval finds LLMs identify the needed context type at most 41.33% of the time [@ahmed2026secvuleval, p. 9]; li2026llm traces all 108 RepoAudit misses to API modelling [@li2026llm, p. 7].
- Contradiction C1: this paper's shortcut finding helps explain why fine-tuned models in fu2023chatgpt score 94% F1 on BigVul [@fu2023chatgpt, p. 4] [I].
- tashenova2026real reaches a similar result with a function-length baseline in PHP [@tashenova2026real, p. 8].

