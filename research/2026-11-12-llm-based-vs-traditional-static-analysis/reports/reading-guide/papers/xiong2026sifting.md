## Sifting the Noise: A Comparative Study of LLM Agents in Vulnerability False Positive Filtering

> **Takeaway:** LLM agents that check SAST warnings can remove most false alarms (on a synthetic Java benchmark the best setup cut the false-positive rate from 98.3% to 6.3%), but the same setup threw away 22.25% of the real vulnerabilities, with the highest miss rates in cryptography-related weakness types. The authors conclude that agents should support human reviewers, not silently suppress warnings.

| Item | Detail |
|---|---|
| Authors | Yunpeng Xiong, Ting Zhang |
| Year | 2026 |
| Venue | Proceedings of the ACM on Software Engineering (ISSTA 2026 issue) |
| Status | Peer-reviewed (journal-style proceedings). Our copy is arXiv version 3 (23 July 2026), formatted as the published article |
| Identifier | doi:10.1145/3832100 (arXiv 2601.22952) |
| Paper type | Comparative empirical study |
| Relevance to us | High: RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
SAST tools (static application security testing) read source code without running it and warn about possible vulnerabilities. Most of their warnings are false positives: warnings about code that is actually safe. Checking them by hand is slow.

This paper tests whether LLM agents can filter out the false warnings. A large language model (LLM) is an AI model trained on huge amounts of text and code. An agent is an LLM that works in several steps: it can open files, search the code and run tools before giving an answer. The authors compare agents with "vanilla" prompting, meaning one single question to the LLM [A] [@xiong2026sifting, p. 1].

### How they did it
They tested three open-source agent frameworks (Aider, OpenHands, SWE-agent), each with three LLMs: Claude Sonnet 4, DeepSeek Chat and GPT-5 [V] [@xiong2026sifting, p. 7]. Each agent received the SAST warning, access to the code and the instruction to decide whether the finding is real or a false positive [V] [@xiong2026sifting, p. 7].

The SAST tools were CodeQL, Semgrep, SonarQube and Joern, run with default rules [V] [@xiong2026sifting, p. 6]. On a recent C/C++ set, the authors also ran stronger single-prompt baselines and ablations, meaning versions with one agent ability switched off [V] [@xiong2026sifting, p. 10]. No deep-learning filter was tested [I].

### Data and setup
Three datasets were used:

1. OWASP Benchmark v1.2: 2,740 synthetic Java test programs with planted flaws, 1,415 vulnerable and 1,325 safe, across 11 weakness types [V] [@xiong2026sifting, p. 6]. Synthetic means written for testing, not taken from real projects.
2. Vul4J: 50 randomly sampled CodeQL warnings from real Java projects, labelled 31 false and 19 true, mostly by the first author [V] [@xiong2026sifting, p. 8; @xiong2026sifting, p. 9].
3. OSS-Fuzz: 50 CodeQL warnings from 5 C/C++ projects whose fixes came 10–12 months after Claude Sonnet 4's training cutoff (the date after which a model has seen no data) [V] [@xiong2026sifting, p. 9]. Two raters labelled them, with Cohen's kappa 0.725, a measure of agreement beyond chance where 1 is perfect [V] [@xiong2026sifting, p. 10].

Temperature was 0 (the most repeatable setting) [V] [@xiong2026sifting, p. 19]. The false-positive rate (FPR) is the share of safe cases that are still flagged. Scripts and data are stated to be public [V] [@xiong2026sifting, p. 21].

### Key findings
- [V] SAST alone on OWASP: CodeQL had precision 60.3% and recall 97.0%, with an FPR of 68.2%; SonarQube's FPR was 94.6% [@xiong2026sifting, p. 11].
- [V] All four tools together flagged 98.3% of safe cases. After filtering by SWE-agent with Claude, the remaining FPR was 6.3%, vs 23.0% with vanilla Claude [@xiong2026sifting, p. 12].
- [V] Agents do not always help. With DeepSeek, vanilla prompting (11.2%) beat all three agents (13.1–15.8%) [@xiong2026sifting, p. 12].
- [V] The best setup wrongly dismissed 314 real vulnerabilities, a miss rate of 22.25% [@xiong2026sifting, p. 18].
- [V] Misses depend on weakness type: at most 2.38% for injection types such as SQL injection and cross-site scripting, but 77.17% for weak cryptography and 84.50% for weak hashing [@xiong2026sifting, p. 18].
- [V] On real Java warnings, the best F1 (a score combining precision and recall) was 83.3% [@xiong2026sifting, p. 13].
- [V] On the post-cutoff C/C++ set, SWE-agent reached F1 95.5% vs 51.6% for vanilla prompting. Giving the vanilla model the same files did not help (51.6%) [@xiong2026sifting, p. 15].
- [V] Cost per warning ranged from $0.0028 to $0.1867 depending on agent and model [@xiong2026sifting, p. 17].

### Limitations and weaknesses
The authors note LLM randomness, small real-world samples (50 warnings each), mostly single-author labels for Vul4J, and real-world tests based mainly on CodeQL [A] [@xiong2026sifting, p. 19; @xiong2026sifting, p. 20]. They warn that agents are "unsuitable for unconditional, automatic suppression of SAST warnings" [A] [@xiong2026sifting, p. 19].

Our own concerns [I]:

- The headline numbers are inconsistent: the abstract says an initial false-positive rate of "over 92%", the results say 98.3%.
- The main comparison uses synthetic code. The real-vulnerability loss was measured for one configuration only.
- With 50 warnings per real-world set, one or two cases change percentages a lot, and no confidence intervals are given. Some runs that did not finish seem to be silently dropped.
- From the real Java table we estimate that the GPT-5 settings dismissed roughly half to two-thirds of the true vulnerabilities in that small sample; the authors do not report this share.
- No significance tests are reported, although the abstract says agents "significantly" outperform vanilla prompting.

### Gaps and future work this paper leaves open
- Gap G3 (true-positive loss per weakness type): this paper is the main evidence for this gap. The authors plan "CWE-aware, cost-adaptive agent strategies" and human-in-the-loop review [A] [@xiong2026sifting, p. 20]. No study yet tests a filter that is only applied to weakness types with low miss rates, on real security alerts.
- Gap G5 (other languages and SAST tools): listed as future work [A] [@xiong2026sifting, p. 20].
- Gap G2 (recent, contamination-free comparisons): this is one of only three papers in our corpus that test on code newer than the models' training data, but it runs no deep-learning detector [I].

### Why it matters for your research
It gives the clearest numbers in our corpus on the main trade-off of SAST-plus-LLM pipelines (RQ3): far fewer false alarms in exchange for lost real vulnerabilities. Its per-weakness results feed RQ4, and its SAST-only figures give a clean RQ1 baseline [I].

### Connections to other papers
- du2026reducing finds the same trade-off in industry on non-security bugs. Together they form agreement G7 in the evidence matrix [@du2026reducing, p. 8; @xiong2026sifting, p. 18].
- CodeQL's OWASP numbers here closely match khare2025understanding (precision 0.58, recall 0.96), a rare cross-group replication (agreement G5) [@khare2025understanding, p. 9; @xiong2026sifting, p. 11].
- Its finding that injection-type warnings are easy fits khare2025understanding, where LLM detectors do best on self-contained weakness types such as command injection and SQL injection [@khare2025understanding, p. 7].
- The authors argue that agents gain by gathering evidence step by step rather than from more context [A] [@xiong2026sifting, p. 15]. This fits agreement G6 in the evidence matrix, that missing context is a shared cause of failure; for example, 14.60% of false positives in li2026llm come from truncated context across functions [@li2026llm, p. 15] [I].

