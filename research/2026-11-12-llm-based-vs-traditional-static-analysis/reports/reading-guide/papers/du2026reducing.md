## Reducing False Positives in Static Bug Detection with LLMs: An Empirical Study in Industry

> **Takeaway:** On 433 real alarms from Tencent's in-house static analyser, hybrid methods that combine static analysis with an LLM removed 94–98% of false alarms while keeping 75–88% of real bugs, at cents per alarm; plain prompting and off-the-shelf deep-learning detectors did far worse. The winning method is the authors' own, four authors work at Tencent, the data are private, and the bugs are general bugs rather than security vulnerabilities, so treat it as indirect, unreplicated evidence.

| Item | Detail |
|---|---|
| Authors | Xueying Du, Jiayi Feng, Yi Zou, Wei Xu, Jie Ma, Wei Zhang, Sisi Liu, Xin Peng, Yiling Lou |
| Year | 2026 |
| Venue | Proceedings of the IEEE/ACM 48th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP) |
| Status | Peer-reviewed (conference). Our copy is the arXiv version 1 preprint (26 January 2026), not the camera-ready, so final numbers may differ |
| Identifier | doi:10.1145/3786583.3786910 (arXiv 2601.18844) |
| Paper type | Industrial empirical study (interviews plus offline evaluation) |
| Relevance to us | Medium: RQ1, RQ3, RQ4, RQ5 |

### In plain words
A static analysis tool (SAT) reads code without running it and raises warnings, called alarms, about possible bugs. Many alarms are false positives: warnings about code that is actually fine. Developers must check each alarm by hand, which costs time.

This study asks whether large language models (LLMs, AI models trained on huge amounts of text and code) can sort the alarms, so that developers only look at the likely real ones [A] [@du2026reducing, p. 1]. It is set inside Tencent, a large Chinese IT company, using its own analyser, BkCheck [V] [@du2026reducing, p. 1].

Important scope note: the three bug types are null pointer dereference (using a pointer that points to nothing), out-of-bounds access (reading or writing outside an array) and divide-by-zero [V] [@du2026reducing, p. 4]. These are general reliability bugs, not classic security vulnerabilities. They overlap with some security weakness types, so the study is only indirect evidence for our topic [I].

### How they did it
First, the authors interviewed 5 developers and reviewers about how alarms are handled [V] [@du2026reducing, p. 4]. Then they tested several ways to sort alarms on historical data [V] [@du2026reducing, p. 5]:

1. Plain prompting of four LLMs (GPT-4o, Claude-Opus-4, Qwen-3-Coder, DeepSeek-R1), with basic, chain-of-thought (asking the model to reason step by step), few-shot (showing a few solved examples) and bug-type-specific prompts.
2. Two hybrid methods that feed static-analysis information to the LLM. LLM4SA gives the LLM the warning plus surrounding code. LLM4PFA adds path conditions from static analysis and lets an LLM agent (an LLM that works in several steps) reason about whether the bug path can really happen.
3. Four deep-learning (DL) detectors, Devign, ReGVD, LLMAO and LineVul, used as originally trained, without retraining [V] [@du2026reducing, p. 6].

Each LLM query was run three times and the majority answer was used [V] [@du2026reducing, p. 6].

### Data and setup
The data are 433 alarms from Tencent's advertising and marketing code, mostly C/C++, from September 2024 to June 2025 [V] [@du2026reducing, p. 4]. Of these, 328 were false alarms and 105 real bugs, as judged by Tencent's routine two-round code review [V] [@du2026reducing, p. 4]. The dataset is confidential; methods and results are in a public replication package [V] [@du2026reducing, p. 2].

Key measures: precision (share of alarms called real that are real), recall (share of real bugs kept), and the share of false alarms removed.

### Key findings
- [V] The analyser alone: 76% of alarms in the dataset were false (328 of 433) [@du2026reducing, p. 6].
- [A] Developers review every alarm, spending 10–20 minutes per alarm [@du2026reducing, p. 6].
- [V] The hybrid LLM4PFA removed 94–98% of false alarms and kept 75–88% of real bugs, with precision 0.83–0.93 across the four LLMs [@du2026reducing, p. 8].
- [V] The other hybrid, LLM4SA, removed 84–96% of false alarms with recall 0.65–0.86 [@du2026reducing, p. 8].
- [V] Plain prompting was much weaker: accuracy 0.40–0.55 with a basic prompt and precision 0.26–0.29 [@du2026reducing, p. 8].
- [V] Off-the-shelf DL detectors failed. LineVul reached accuracy 0.76 only by calling every alarm false [@du2026reducing, p. 7; @du2026reducing, p. 8].
- [V] LLM4PFA cost 12.6–58.3 seconds and $0.0025–$0.12 per alarm [@du2026reducing, p. 8].
- [V] Cases that every method got wrong had functions about 95.6 lines longer than average, with 21 more conditional statements [@du2026reducing, p. 9].

### Limitations and weaknesses
The authors say recall is below the 90% that the company expects, so manual review is still needed [A] [@du2026reducing, p. 9]. LLMs can only filter alarms; they cannot find bugs the analyser misses [A] [@du2026reducing, p. 10]. The data cover one company, 433 cases over 10 months, mostly C/C++ [A] [@du2026reducing, p. 10].

Our own concerns [I]:

- Conflict of interest. Four of the nine authors are Tencent employees, and the study evaluates Tencent's own analyser on Tencent data [@du2026reducing, p. 1]. LLM4PFA, the winning method, is the authors' own earlier work. Funding is not reported. With private data, nobody outside can check the result.
- The DL comparison is unfair. These detectors were built for a different task and were not retrained.
- Plain-prompting precision (0.26–0.29) is barely above the share of real bugs in the data (about 0.24, our arithmetic).
- Model names in the text do not match the cited references, so the exact models are unclear.
- Whether the few-shot examples came from the test data is not reported.
- Our copy is the preprint, not the peer-reviewed final version.

### Gaps and future work this paper leaves open
- Gap G3 (true-positive loss when LLMs filter alarms): this paper loses 12–25% of real bugs while filtering, on non-security bugs. The gap report notes that loss per security weakness type on real alerts is still not controlled.
- Gap G5 (other languages): the authors plan more languages and business lines [A] [@du2026reducing, p. 10].
- Gap G6 (full cost comparison): cost is given per alarm but not per project, and human checking time is not costed against it [I].

### Why it matters for your research
This is the only industrial, real-world study in our corpus of LLMs sorting static-analysis alarms (RQ3). It shows hybrids beating both plain prompting and off-the-shelf DL detectors on the same alarms, with cost per alarm [I]. Its weight is limited by the conflict of interest, the private data and the non-security bug types.

### Connections to other papers
- xiong2026sifting is the closest independent study, on real security alerts. Together they form agreement G7 in the evidence matrix: LLM filtering removes most false alarms but loses some real ones [@du2026reducing, p. 8; @xiong2026sifting, p. 18].
- Both papers report filtering costs below $0.20 per alarm, part of agreement G9 on LLM cost [@du2026reducing, p. 8; @xiong2026sifting, p. 17].
- The authors excluded IRIS (li2024iris) because it needs a compilable repository for CodeQL [V] [@du2026reducing, p. 5].
- The finding that long functions defeat all methods matches li2026llm, where LLM performance falls with file length [@li2026llm, p. 9].

