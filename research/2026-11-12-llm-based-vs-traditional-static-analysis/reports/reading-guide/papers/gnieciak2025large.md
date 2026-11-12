## Large Language Models Versus Static Code Analysis Tools: A Systematic Benchmark for Vulnerability Detection

> **Takeaway:** On ten small C# projects with planted security flaws, three chatbot-style LLMs found far more flaws than three standard code scanners (mean F1 0.75–0.80 against 0.26–0.55). The test set is tiny and the scoring was more lenient for the LLMs, so treat this as weak evidence.

| Item | Detail |
|---|---|
| Authors | Damian Gnieciak, Tomasz Szandala |
| Year | 2025 |
| Venue | IEEE Access (journal) |
| Status | Peer-reviewed. Our copy is the arXiv version (2508.04448, v1), so numbers may differ slightly from the published article. |
| Identifier | DOI 10.1109/access.2025.3635168 |
| Paper type | Empirical benchmark (head-to-head comparison) |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4 |

### In plain words
A security vulnerability is a mistake in code that an attacker can exploit. One classic way to find such mistakes is static application security testing (SAST). SAST tools read the source code without running it and apply fixed rules, such as "user input must not flow into a database query". A newer way is to ask a large language model (LLM), a chatbot-style AI trained on huge amounts of text and code, to review the code.

This paper puts three well-known SAST tools (SonarQube, CodeQL and Snyk Code) against three LLMs (GPT-4.1, Mistral Large and DeepSeek V3). All six look at the same ten small C# projects. The LLMs win clearly on the authors' headline numbers. But the paper also shows two practical problems: the LLMs never gave the right line number, and they sometimes reported problems that did not exist.

### How they did it
The authors built a tool called ProjectAnalyzer. It pastes every file of a project into one prompt and asks the LLM to act as "a static code analysis engine" [@gnieciak2025large, p. 7]. The prompt lists ten vulnerability types and asks for a structured answer. This was zero-shot: the models got no examples and no extra training. The SAST tools ran with their default settings [@gnieciak2025large, p. 8]. Each tool or model ran once per project. The authors then checked every reported finding by hand against a list of the known flaws [@gnieciak2025large, p. 6].

The main measures are precision, recall and F1. Precision is the share of a tool's warnings that are real flaws. Recall is the share of real flaws the tool finds. F1 combines the two into one score between 0 and 1. The authors computed these per project and then took the plain average over the ten projects, which is called a macro average [@gnieciak2025large, p. 10].

### Data and setup
- The test set is 10 C# projects with 3–10 files each, 3,145–5,317 characters each, and 63 vulnerabilities in total [@gnieciak2025large, p. 6].
- The flaws come from six categories: SQL injection, cross-site scripting, hard-coded secrets, command injection, weak encryption and outdated libraries [@gnieciak2025large, p. 5].
- The paper says the projects were "prepared" with "a random number of vulnerabilities" [@gnieciak2025large, p. 5], but the abstract calls them "real-world" projects [@gnieciak2025large, p. 1]. [I] The sizes suggest small purpose-built examples, not real software.
- Temperature (a setting that controls how random the LLM's answers are), model versions and actual run costs are not reported. List prices per million tokens are given [@gnieciak2025large, p. 5].
- The harness code is public [@gnieciak2025large, p. 1].

### Key findings
- [V] Mean F1: GPT-4.1 0.797, Mistral Large 0.753, DeepSeek V3 0.750, against Snyk Code 0.546, CodeQL 0.386 and SonarQube 0.260 [@gnieciak2025large, p. 10].
- [V] The gap comes mainly from recall. The LLMs reach mean recall 0.783–0.877, the SAST tools 0.187–0.523. Mean precision is closer: 0.723–0.783 for LLMs, 0.567–0.686 for SAST [@gnieciak2025large, p. 10].
- [I] Pooling the raw counts instead of averaging per project gives SAST precision of about 0.74–0.87 against 0.74–0.79 for the LLMs, and Snyk's F1 rises to about 0.70 (our arithmetic from the raw tables [@gnieciak2025large, p. 8]). The averaging method widens the gap.
- [V] LLMs were fast. CodeQL took 185.9–213.1 seconds per project and GPT-4.1 took 3.5–17.8 seconds [@gnieciak2025large, p. 9].
- [A] All LLMs named the right file but always gave the wrong line and column [@gnieciak2025large, p. 11].
- [V] LLMs invented findings. For example, GPT-4.1 flagged a current version of a library (Newtonsoft.Json 13.0.3) as outdated [@gnieciak2025large, p. 12].
- [A] The authors recommend LLMs for early, broad checks during development and SAST for high-assurance audits [@gnieciak2025large, p. 12].

### Limitations and weaknesses
- [I] The benchmark is tiny: 63 flaws in projects small enough to fit easily in one prompt [@gnieciak2025large, p. 6]. This suits LLMs and says little about real repositories.
- [V] Wrong line locations were not counted against the LLMs [@gnieciak2025large, p. 6]. [I] SAST tools got no such leniency, so the comparison is tilted towards the LLMs.
- [V] When a tool reported nothing on a project, its precision was recorded as 0.000 and averaged in [@gnieciak2025large, p. 9]. [I] This lowers SAST precision.
- [I] Each model ran once, with no repeat runs, no statistical tests and no confidence intervals. LLM answers can vary between runs.
- [I] Default SAST settings were used, and "outdated libraries" is normally the job of a different tool type. Both may disadvantage the SAST tools.
- [I] There are no results per vulnerability type, and no actual cost, although prices are listed.

### Gaps and future work this paper leaves open
- [A] The authors call for studying prompt design and building a hybrid in which classic tools and LLMs prioritise and verify findings [@gnieciak2025large, p. 11].
- [I] The lenient location rule for LLMs is one of the scoring differences behind gap G1 (no shared evaluation protocol across studies).
- [I] The study uses small, synthetic-looking projects in one language, so it does not touch gap G2 (a fair three-way test on real, recent code with repository context).
- [I] It lists prices but reports no cost per real flaw found, which is the subject of gap G6.

### Why it matters for your research
This is one of the few head-to-head tests of commercial-grade SAST against frontier LLMs, and the only one in our set on C#. It supports the claim that LLMs beat SAST on small, self-contained code. But it is weak evidence. Use it as one data point in the "LLMs win on small code" group, and always pair it with the larger real-code studies that point the other way. It is also a good teaching example of how a scoring choice, such as averaging per project, can change a headline result.

### Connections to other papers
- It is one side of contradiction C3 in the evidence matrix (LLM vs SAST rankings reverse between settings). CASTLE also finds LLMs ahead on small C programs [@dubniczky2025castle, p. 11]. CodeQL beats LLMs on accuracy on synthetic test suites [@khare2025understanding, p. 9].
- At repository scale, LLM tools flag up to 77.4% of functions (preprint) [@zhou2024comparison, p. 7], and most LLM detectors and SAST tools produce mostly false warnings [@li2026llm, p. 11].
- [I] The "LLMs find more but are noisier" pattern also appears in deininger2026open, where SAST tools are more precise than every LLM at a realistic vulnerability rate [@deininger2026open, p. 8].
