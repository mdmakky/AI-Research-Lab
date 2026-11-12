## LLM Hallucinations in Practical Code Generation: Phenomena, Mechanism, and Mitigation
> **Takeaway:** In realistic Python tasks set inside real projects, most AI coding mistakes come from misunderstanding the task, and problems with missing packages make up under 1% of hallucinations [@zhang2025llm, p. 4; @zhang2025llm, p. 6]. Read it as background: it maps the kinds of code hallucination, but it does not measure invented PyPI packages.

| Item | Detail |
|---|---|
| Authors | Ziyao Zhang, Chong Wang, Yanlin Wang, Ensheng Shi, Yuchi Ma, Wanjun Zhong, Jiachi Chen, Mingzhi Mao, Zibin Zheng (published version; our arXiv copy lists five authors) |
| Year · Venue | 2025 · Proceedings of the ACM on Software Engineering (PACMSE), ISSTA 2025 issue |
| Status | Peer-reviewed (PACMSE / ISSTA 2025); our copy is the arXiv version |
| Identifier | DOI 10.1145/3728894 (arXiv 2409.20550) |
| Paper type | Empirical study: hand-built taxonomy of errors plus a small mitigation pilot |
| Relevance to us | Low — RQ1 (marginal), RQ3 and RQ4 (background) |

### In plain words
Many studies test AI coding on small, self-contained functions. This paper uses repository-level tasks instead: the model must write a function that fits into a real project with its own files and dependencies [@zhang2025llm, p. 1]. The authors read thousands of generated snippets and sorted the mistakes into a taxonomy (a structured list of error types) [@zhang2025llm, p. 3; @zhang2025llm, p. 4]. Package hallucination is only one small corner of that map. The paper is useful to us mainly for context and for a warning about definitions.

### How they did it
1. They used CoderEval Python, a benchmark of 230 tasks taken from real projects, each with tests and a working project environment [@zhang2025llm, p. 3].
2. Six models produced 10 answers per task with nucleus sampling at temperature 0.6, a moderately random setting [@zhang2025llm, p. 3].
3. Two authors open-coded (read examples and created labels from what they saw) 1,380 snippets from 23 tasks to build the first version of the taxonomy [@zhang2025llm, p. 3].
4. Three volunteers labelled the remaining snippets, and one author reviewed all labels [@zhang2025llm, p. 3; @zhang2025llm, p. 10].
5. They compared models and proposed root causes [@zhang2025llm, p. 8].
6. A pilot fix used RAG (retrieval-augmented generation): it added the 10 most similar code snippets from the same project to the prompt. Success was measured by Pass@1, the share of tasks where the first answer passes the tests [@zhang2025llm, p. 9].

### Data and setup
- Models: GPT-3.5-Turbo, CodeGen-350M, PanGu-alpha-2.6B, DeepSeekCoder-6.7B, CodeLlama-7B-Python and StarCoder2-7B [@zhang2025llm, p. 3].
- [I] 230 tasks × 6 models × 10 answers gives 13,800 snippets by our arithmetic; the paper does not state the total number of hallucinations.
- A "non-existent package" means one that is not available in the task's environment [@zhang2025llm, p. 6]. There is no check against PyPI.
- Code, data and results are on GitHub [@zhang2025llm, p. 1]. Hardware and exact prompts are not reported.

### Key findings
- [V] Three categories: task requirement conflicts 43.53%, factual knowledge conflicts 31.91% and project context conflicts 24.56% of hallucinations [@zhang2025llm, p. 4; @zhang2025llm, p. 5; @zhang2025llm, p. 6].
- [V] Environment conflicts, which include importing a package missing from the environment, are only 0.94%. The example is a package called _lfu_cache [@zhang2025llm, p. 6].
- [I] _lfu_cache is not a valid PyPI distribution name, so it is probably a missing internal module. The 0.94% is therefore an upper bound on invented-package cases.
- [V] API knowledge conflicts are much more common (20.41%), for example a parameter that a real function does not have, as in timedelta(year=1) [@zhang2025llm, p. 6].
- [V] Library knowledge conflicts make up 2.68% [@zhang2025llm, p. 5].
- [V] One security-relevant example: generated code used yaml.load instead of the safer safe_load [@zhang2025llm, p. 5].
- [V] Task requirement conflicts are the most frequent category for all six models [@zhang2025llm, p. 8].
- [V] RAG raised Pass@1 for every model, for example ChatGPT from 10.40% to 12.61% and CodeLlama from 2.17% to 5.22%. [A] The authors call the gain modest [@zhang2025llm, p. 9].

### Limitations and weaknesses
- [A] Python only and only 230 tasks [@zhang2025llm, p. 10].
- [A] No formal inter-rater reliability measure (a statistic for how far independent labellers agree) [@zhang2025llm, p. 10].
- [I] The fix was judged by Pass@1, not by counting hallucinations, so it does not show that RAG reduces hallucinations.
- [I] Without a registry check, invented PyPI names cannot be separated from real packages that simply are not installed.
- [I] Shares are given without totals, so per-answer rates cannot be worked out.
- [I] The models are old and small; some Pass@1 values are as low as 0.04% [@zhang2025llm, p. 9].
- [I] Our arXiv copy lists five authors against nine in the published version, so the content may differ [@zhang2025llm, p. 1].

### Gaps and future work this paper leaves open
- [I] Our gap report does not use this paper as evidence for any gap (G1–G5).
- [I] G3: its definition ("not in the environment") is one more example of the unshared rules for deciding what counts as a hallucinated package [@zhang2025llm, p. 6].
- [A] The authors suggest better ways to find and locate hallucinations, richer retrieval sources and multi-agent systems with tools [@zhang2025llm, p. 9; @zhang2025llm, p. 10].

### Why it matters for your research
Cite it as related work only. It shows that package hallucination is a narrow slice of code hallucination when the model writes code inside an existing project. It also gives a definitional warning: "does not exist in the environment" is not the same as "does not exist on PyPI". If you build a measurement, record these as separate outcomes.

### Connections to other papers
- [V] mirandapena2026empirical also judges missing modules against the installed environment rather than a registry [@mirandapena2026empirical, p. 18].
- [V] Studies that ask models to write whole programs from a prompt find package hallucination in every model tested [@spracklen2024we, p. 7; @churilov2026range, p. 6]. [I] The different task type likely explains why it is so rare here.
- [I] Its API knowledge conflicts resemble the library member hallucinations (calls to functions a real library lacks) studied by twist2026library [@twist2026library, p. 1].
