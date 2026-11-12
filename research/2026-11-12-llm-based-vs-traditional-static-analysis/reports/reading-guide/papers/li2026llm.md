## LLM-based Vulnerability Detection at Project Scale: An Empirical Study

> **Takeaway:** When whole projects are scanned, general coding agents (Codex, Claude Code) find far more known vulnerabilities than SAST tools (59.55% average recall on C/C++ against 0–34.29%). Specialised LLM detectors often find almost nothing, most tools' warnings on real projects are 77–100% false, and LLM runs can cost up to USD 1,247.66 per project.

| Item | Detail |
|---|---|
| Authors | Fengjie Li, Jiajun Jiang, Dongchi Chen, Yingfei Xiong |
| Year | 2026 |
| Venue | IEEE Transactions on Software Engineering (journal) |
| Status | Peer-reviewed. Our copy is the arXiv version (2601.19239, v2, September 2026), not the IEEE version of record; page numbers and some numbers may differ. |
| Identifier | DOI 10.1109/tse.2026.3742453 |
| Paper type | Comparative empirical study |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
Most studies test detectors on single functions. This one tests them where developers actually use them: on whole projects, some with millions of lines of code. It compares three groups of tools. Specialised LLM detectors are research tools built around an LLM for one job, such as RepoAudit, KNighter, IRIS, LLMDFA and INFERROI. General coding agents are AI assistants that can open files and search code on their own; here Codex and Claude Code. SAST tools are rule-based scanners: CodeQL, Semgrep, SpotBugs and the Clang Static Analyzer (CSA).

The general agents clearly find the most known flaws. But on real, current projects nearly every tool, LLM or SAST, raises mostly false alarms, and some LLM tools are slow and costly.

### How they did it
The study has two parts. First, a controlled benchmark of known vulnerabilities measures recall (share of known flaws found) and precision (share of warnings that are right) [@li2026llm, p. 5]. Second, the tools scan 24 real projects where the true flaws are unknown. There the main measure is SFDR, the sampled false discovery rate: the share of a random sample of a tool's warnings that turn out to be false [@li2026llm, p. 6].

Each specialised tool ran with its original model and again with GPT-5.4, to separate the effect of the workflow from the effect of the model [@li2026llm, p. 4]. SAST rule sets were picked by hand to match the eight CWEs studied; a CWE is a standard catalogue number for a type of weakness [@li2026llm, p. 7]. Codex labelled the sampled real-world warnings as true or false, and humans checked a stratified sample [@li2026llm, p. 11]. The authors also hand-coded why tools raise false alarms [@li2026llm, p. 13].

### Data and setup
- Controlled set: 265 known vulnerabilities, 110 in C/C++ and 155 in Java, across 8 CWEs [@li2026llm, p. 6].
- Real-world set: 24 actively maintained projects or modules, from 1,715 to 6,033,855 lines of code [@li2026llm, p. 6]. 21 of the 24 code versions are newer than the August 2025 knowledge cutoff of the agents' models [@li2026llm, p. 5]. The knowledge cutoff is the date after which a model has seen no training data.
- 6,442 warnings were sampled and 5,896 false positives classified by cause [@li2026llm, p. 11].
- No deep-learning detectors were included [@li2026llm, p. 4]. Each setup ran once [@li2026llm, p. 18].
- Scripts, prompts and labels are public [@li2026llm, p. 2].

### Key findings
- [V] On 110 known C/C++ vulnerabilities, the general agents average 59.55% recall and 32.19% precision. CodeQL's recall is 6.00–34.29% across the three CWEs, while Semgrep and CSA find none. KNighter finds none, and RepoAudit finds 0 of 110 with its original model [@li2026llm, p. 7].
- [V] On 155 known Java vulnerabilities, Claude Code's recall is 81.94% and Codex's 63.87%, against CodeQL 14.19%, Semgrep 6.67% and SpotBugs 14.84% [@li2026llm, p. 9].
- [V] On real C/C++ projects, SFDR is 92.77% for RepoAudit, 86.01% for CodeQL, 85.51% for CSA and 100% for Semgrep. Codex is lowest at 9.09%, but on about two warnings per project [@li2026llm, p. 11].
- [V] On real Java projects, IRIS (an LLM plus CodeQL hybrid) has 97.80% SFDR, worse than plain CodeQL at 77.00% [@li2026llm, p. 12].
- [V] Weak API modelling explains all 108 RepoAudit misses with GPT-5.4 [@li2026llm, p. 7]. API modelling means knowing which library functions allocate memory, read input and so on. Given perfect API lists for memory leaks (CWE-401), recall rises sharply: CodeQL from 6% to 56%, RepoAudit from 0% to 48% [@li2026llm, p. 8].
- [V] Across tools, 63.33% of false alarms come from misjudging what a program point does, and 14.60% from missing context in other functions [@li2026llm, p. 15].
- [V] Cost per project: RepoAudit averages USD 172.77 with a maximum of USD 1,247.66; Codex averages USD 5.38 and 14.80 minutes; SAST tools run in minutes with no token cost [@li2026llm, p. 16].
- [A] The authors conclude that the tool's workflow, not the model, limits recall [@li2026llm, p. 9].

### Limitations and weaknesses
- [V] Codex, which is also evaluated, labelled the real-world warnings; humans found its labels 94.36% accurate on 621 checked warnings [@li2026llm, p. 11]. [I] A judge that favours its own reports is only partly ruled out, and Codex scores best on SFDR.
- [I] Codex's low SFDR rests on roughly 22 warnings per language, so it is imprecise.
- [I] Controlled-set precision counts false alarms only inside known vulnerable files, so it is not comparable with precision in other papers [@li2026llm, p. 6].
- [I] The known vulnerabilities likely predate model training, so agent recall may partly reflect memory. Recall on the newer real-world code is not measured.
- [I] SAST rules were chosen by the authors; other rules could change SAST results.
- [A] Two languages, 8 CWEs, single runs, and several modules from one Linux version [@li2026llm, p. 18].

### Gaps and future work this paper leaves open
- [A] The authors call for combining agents with program analysis, better API specifications, cost-aware designs, and more languages and CWEs [@li2026llm, p. 17; @li2026llm, p. 18].
- [I] Gap G4: this is the only independent re-test of the hybrids RepoAudit and IRIS in our set, and its labeller is an evaluated tool, so target, metric and labeller effects are still mixed.
- [I] Gap G2: it uses code newer than the training cutoff with repository context, but has no deep-learning arm and no recall on that newer code.
- [I] Gap G6: it reports cost per project, not cost per confirmed vulnerability including human checking time.
- [I] Gap G1: SFDR is yet another headline metric that cannot be pooled with others. Gap G5: no PHP or Go.

### Why it matters for your research
This is the most realistic LLM-vs-SAST comparison in our set: real projects, current code, full tools rather than single functions. It shows that "LLM vs SAST" depends heavily on the LLM workflow. Flexible agents beat SAST on recall, while several published specialised hybrids do not. It also gives concrete cost data for RQ3 and a shared list of false-alarm causes for RQ5.

### Connections to other papers
- Contradiction C2: RepoAudit's own paper reports 78.43% precision and USD 2.54 per project [@guo2025repoaudit, p. 7], against 0 of 110 here. Targets, code versions, metrics and labellers differ, so neither paper refutes the other.
- Contradiction C6: IRIS beat CodeQL on 120 known Java vulnerabilities in its own paper [@li2024iris, p. 8], but is noisier than CodeQL on new Java projects here.
- Contradiction C3: the agents' recall lead echoes the small-code LLM wins [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11], and the high false alarm rates echo the repository-level preprint zhou2024comparison [@zhou2024comparison, p. 7].
- Agreement G4 (low SAST recall), agreement G6 (missing context causes failures) and agreement G9 (LLM cost far exceeds SAST) all draw on this paper.
