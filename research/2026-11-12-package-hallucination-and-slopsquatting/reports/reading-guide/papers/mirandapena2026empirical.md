## An Empirical Analysis of Static Analysis Methods for Detection and Mitigation of Code Library Hallucinations
> **Takeaway:** Free code-checking tools such as Pyright catch some, but far from all, cases where AI-written Python uses library features that do not exist, and the authors put the realistic ceiling at about 77% [@mirandapena2026empirical, p. 8; @mirandapena2026empirical, p. 12]. The tools check against installed packages, not PyPI, so they cannot spot a squatted package.

| Item | Detail |
|---|---|
| Authors | Clarissa Miranda-Pena, Andrew Reeson, Cécile Paris, Josiah Poon, Jonathan K. Kummerfeld |
| Year · Venue | 2026 · arXiv |
| Status | Preprint; the PDF states acceptance in Transactions on Machine Learning Research (TMLR), which we have not verified |
| Identifier | arXiv 2604.07755 (DOI 10.48550/arxiv.2604.07755) |
| Paper type | Comparative evaluation of detection, repair and constrained decoding, with manual annotation |
| Relevance to us | Medium — RQ3, RQ4, RQ5 (main); RQ1 (partial) |

### In plain words
Static analysis means checking code without running it, a bit like a spell-checker for programs. Mypy and Pyright are free static checkers for Python. Here a library hallucination is code that would only work if imagined functions or arguments of a library existed [@mirandapena2026empirical, p. 1]. The paper asks three things: how many of these errors such tools catch, whether an AI can repair them using the tools' messages, and whether a grammar can stop the model from writing them in the first place [@mirandapena2026empirical, p. 2].

### How they did it
1. Six models wrote code for three Python benchmarks: DS-1000, ODEX and BigCodeBench [@mirandapena2026empirical, p. 5].
2. Four detectors were compared: Mypy, Pyright, a grammar built automatically from library documentation, and o3-mini as an AI judge [@mirandapena2026empirical, p. 4].
3. The authors hand-annotated 600 failure cases to see what the tools could catch in principle [@mirandapena2026empirical, p. 6]. Annotators agreed well, with Cohen's kappa (agreement corrected for chance) of 0.79 [@mirandapena2026empirical, p. 7].
4. Repair: o3-mini fixed the code given the error alone or the error plus Mypy or Pyright output [@mirandapena2026empirical, p. 9; @mirandapena2026empirical, p. 10].
5. Constrained decoding: the grammar limits which tokens the model may write, run in llama.cpp, a tool for running models locally [@mirandapena2026empirical, p. 4; @mirandapena2026empirical, p. 11].

### Data and setup
- Benchmarks: DS-1000 (1,000 problems), ODEX (550 of 945 used) and BigCodeBench (1,140) [@mirandapena2026empirical, p. 5].
- Models: Claude-3, GPT-4 and GPT-3.5 through APIs, and Gemma2 2B, Granite 3B and Qwen3 8B as open models [@mirandapena2026empirical, p. 5]. Exact API versions are not reported.
- The whole study ran on an M2 laptop-class computer with 24 GB of memory [@mirandapena2026empirical, p. 17].
- Detection takes about 1 s with Mypy, 2.5 s with Pyright and 4 s with o3-mini per sample [@mirandapena2026empirical, p. 19].
- A code release is not reported.

### Key findings
- [V] Pyright's recall on library hallucinations (the share it flags) ranges from 0.14 to 0.85 by model and benchmark [@mirandapena2026empirical, p. 20].
- [V] In the hand-checked sample, the static tools flagged hallucinations for the right reason in only 37.6% (DS-1000), 4.0% (ODEX) and 10.0% (BigCodeBench) of cases [@mirandapena2026empirical, p. 8].
- [V] The share the tools could catch in principle is 77.0%, 70.5% and 48.5% [@mirandapena2026empirical, p. 8].
- [V] Benchmark noise is large: ambiguous inputs or outputs explain 36.9% of sampled hallucinations in ODEX and 34.1% in BigCodeBench, but 1.1% in DS-1000 [@mirandapena2026empirical, p. 9].
- [V] Repair makes more code run, for example Gemma2 2B on DS-1000 from 47.2% to 77.9% [@mirandapena2026empirical, p. 9].
- [V] Its effect on hallucinations depends on the benchmark. Their share of remaining errors falls on DS-1000 for every model (claude-3 9.1 to 2.7) but rises on ODEX for small models (Qwen3 8B 31.3 up to 55.6) [@mirandapena2026empirical, p. 10].
- [A] The authors summarise repair as "no improvement" in most cases [@mirandapena2026empirical, p. 10]. [I] Their own table shows clear gains on DS-1000, so this overstates.
- [V] Constrained decoding gives small, mixed changes and adds about 12 seconds per response [@mirandapena2026empirical, p. 11].

### Limitations and weaknesses
- [A] Python only; the grammar cannot handle unusual import aliases, and incomplete documentation causes grammar errors [@mirandapena2026empirical, p. 16; @mirandapena2026empirical, p. 8].
- [A] After the agreement check, one annotator labelled the rest [@mirandapena2026empirical, p. 7].
- [I] A missing module is judged against the benchmark environment, not a registry [@mirandapena2026empirical, p. 18]. Uninstalled real packages and invented ones are merged.
- [I] Package-level cases are not reported separately; library causes are only 6.0–14.7% of the sample [@mirandapena2026empirical, p. 8].
- [I] Two abstract ranges (8.1–40% and 16–70%) could not be matched to any table [@mirandapena2026empirical, p. 1].
- [I] The repair measure is relative, so it can change when other errors change. No confidence intervals and mixed temperatures.

### Gaps and future work this paper leaves open
- [V] G2: this is the only study in our set run on a laptop-class machine [@mirandapena2026empirical, p. 17]. [I] It shows a client-side check is feasible, but a registry layer is still needed to catch squatted names.
- [I] G3: its environment-based rule for missing modules is another of the inconsistent definitions the gap report describes [@mirandapena2026empirical, p. 18].
- [A] The authors suggest tracking data and control flow in static tools and building benchmarks that accept several valid solutions [@mirandapena2026empirical, p. 7; @mirandapena2026empirical, p. 9].

### Why it matters for your research
It proves that a defence study can run on an ordinary laptop. Mypy or Pyright can be a cheap first screen before running AI code. Its limits are clear, though: a squatted package installs fine and passes these checks, so a PyPI or npm lookup must sit on top. Two reporting lessons: count hallucinations in absolute numbers, not only as a share, and hand-check a sample for benchmark noise. Constrained decoding does not look worth its cost here.

### Connections to other papers
- [V] White-box defences that edit the model or its outputs need model weights and GPU servers [@liu2026packmonitor, p. 12; @liu2026mitigating, p. 6; @spracklen2026llm, p. 8]; this paper's tools do not.
- [V] zhang2025llm also defines a missing package by the environment rather than PyPI [@zhang2025llm, p. 6].
- [V] twist2026library uses the same BigCodeBench tasks but checks names against PyPI [@twist2026library, p. 4].
- [I] Its checks run before code executes, in line with ohm2020backstabbers' finding that most malicious packages act at install time [@ohm2020backstabbers, p. 11].
