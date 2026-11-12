## Library Hallucinations in LLM-Generated Code: A Risk Analysis Grounded in Developer Queries
> **Takeaway:** Ordinary coding requests almost never make AI models invent library names, but asking for a library "from 2025" or mistyping a library name makes many models invent or accept fake ones [@twist2026library, p. 5; @twist2026library, p. 6]. A tool that lets the model check PyPI helps only if the model actually calls it [@twist2026library, p. 8].

| Item | Detail |
|---|---|
| Authors | Lukas Twist, Mark Harman, Helen Yannakoudakis, Jie M. Zhang |
| Year · Venue | 2026 · Proceedings of EMNLP 2026 (main conference) |
| Status | Peer-reviewed; our copy is the published ACL Anthology version |
| Identifier | DOI 10.18653/2026.emnlp-main.78 (arXiv 2509.22202) |
| Paper type | Controlled prompt-variation experiments plus a released benchmark (LibHalluBench) |
| Relevance to us | High — RQ1, RQ3, RQ4 (main); RQ2 and RQ5 (indirect) |

### In plain words
Developers often describe the library they want in words ("a fast library", "a library from 2025"), or they misspell its name. This paper asks whether that everyday wording makes AI models invent libraries. It looks at two kinds of error: library name hallucinations (importing a library that does not exist) and library member hallucinations (calling a function that a real library does not have) [@twist2026library, p. 1]. The authors present it as the first systematic study of how user-level prompt wording affects these errors [@twist2026library, p. 2].

### How they did it
1. They started from BigCodeBench, a public coding benchmark, and kept 356 tasks that use 30 libraries without naming them [@twist2026library, p. 3].
2. Experiment 1 inserted descriptions mined from 3,917 library questions on the Software Recommendations StackExchange site, such as "fast" or "from 2025" [@twist2026library, p. 4].
3. Experiment 2 inserted mistakes: one-character typos, multi-character typos or fake library names, each checked to be unregistered [@twist2026library, p. 4].
4. Seven models answered each prompt three times through their providers' APIs, in a fresh session with no system prompt [@twist2026library, p. 3; @twist2026library, p. 4].
5. Python's own parser read the import lines, and names were compared with PyPI after standard name normalisation [@twist2026library, p. 4].
6. Two measures: RHR, the share of responses with a hallucination, and THR, the share of tasks where at least one of the three responses hallucinates [@twist2026library, p. 5].
7. Extra studies covered prompt techniques, a PyPI-existence tool and JavaScript and Rust [@twist2026library, p. 8; @twist2026library, p. 20].

### Data and setup
- Models with exact versions: GPT-4o-mini, GPT-5-mini, Ministral-8B, Qwen-2.5-Coder 32B, Llama-3.3 70B, DeepSeek-V3.1 and Claude-4.5-Haiku, each at its default temperature (0.3 to 1.0) [@twist2026library, p. 15].
- Model details are recorded as of January 2026 [@twist2026library, p. 15].
- The JavaScript and Rust study used 500 tasks and one response per task [@twist2026library, p. 20].
- LibHalluBench has 4,173 prompts and is released on Hugging Face (gated) and as a PyPI package [@twist2026library, p. 8].
- The detector was checked by hand on 200 responses [@twist2026library, p. 15].
- The date of the PyPI name list is not reported.

### Key findings
- [V] With normal or adjective prompts, library-name hallucination stays at or below 0.31% of responses for every model [@twist2026library, p. 5].
- [V] "From 2025" requests cause invented library names in 84.74% of tasks for GPT-4o-mini, 63.86% for GPT-5-mini and 61.68% for Qwen-2.5-Coder, but only 0.62% for Claude-4.5-Haiku [@twist2026library, p. 5].
- [V] Models go along with user mistakes: one-character typos in up to 25.86% of tasks, multi-character typos up to 79.44% and fake names up to 99.22% [@twist2026library, p. 6].
- [V] Asking for a "hidden gem" gives the highest rate among the adjective prompts, 5.35% [@twist2026library, p. 8].
- [V] Self-analysis and explicit-check prompts reduced hallucinations in 29 and 30 of 36 settings, while chain-of-thought was inconsistent [@twist2026library, p. 19].
- [V] With a PyPI tool, GPT-4o-mini called it on 98.65% of "from 2025" responses and hallucinated in 2.49%. GPT-5-mini called it on only 7.89% and gave no code 90.76% of the time [@twist2026library, p. 21].
- [V] Under user mistakes, invalid libraries were still accepted in up to 38.79% of cases even with the tool [@twist2026library, p. 21].
- [V] Fake names were also accepted in JavaScript (up to 88.8%) and Rust (up to 96.76%) [@twist2026library, p. 20].
- [V] 23 of 24 automatically flagged responses were true hallucinations (95.8% precision) [@twist2026library, p. 15].

### Limitations and weaknesses
- [A] A finite set of tasks, ecosystems and model versions [@twist2026library, p. 9]; the tool study is a "small case study" [@twist2026library, p. 8].
- [I] Experiment 2 measures acceptance of the user's mistake, not invention. The threat is typosquatting amplification, not classic slopsquatting.
- [I] Any name registered on PyPI counts as valid, so collisions with squatted names are invisible by design [@twist2026library, p. 4].
- [I] Normalisation cannot map import names to package names (dateutil to python-dateutil); such cases were fixed only by hand [@twist2026library, p. 15].
- [I] Whether invented names repeat across runs, which matters for slopsquatting, is not reported.
- [I] No statistical tests or confidence intervals, mixed temperatures, API models only, and undated registry lists.

### Gaps and future work this paper leaves open
- [A] G1: the authors name agentic coding workflows as future work [@twist2026library, p. 9]. [V] The optional tool was rarely called by GPT-5-mini [@twist2026library, p. 8].
- [I] G2: this supports testing a forced, client-side existence check against a tool the model may skip.
- [V] G3: it counts registered import names as valid [@twist2026library, p. 4], while raj2026names flags them as squats [@raj2026names, p. 8].
- [I] G4: no local or quantized models were tested; running LibHalluBench on Ollama models is a cheap extension.
- [I] Typo amplification was dropped as a gap because this paper already measures it [@twist2026library, p. 6].

### Why it matters for your research
This is one of the strongest papers in the set: peer-reviewed, seven models, repeated answers, ablations and everything released. It gives you a ready trigger set that runs on a laptop; year-based and typo prompts are the highest-yield conditions. Its tool study teaches a key design lesson: a check the model may choose to call is weak, so compare it with a check that always runs. Add an explicit import-to-package map and record "registered but suspicious" as its own result.

### Connections to other papers
- [V] dasu2026refusing finds the same acceptance pattern, with nonexistent npm packages fabricated on 94% of prompts [@dasu2026refusing, p. 8].
- [V] raj2026names treats registered import names such as pil and faiss as squats, the opposite rule (evidence matrix contradiction 5) [@raj2026names, p. 8].
- [V] churilov2026range found import names of real packages to be the largest false-positive class [@churilov2026range, p. 10].
- [V] mirandapena2026empirical also uses BigCodeBench but checks against the installed environment, not PyPI [@mirandapena2026empirical, p. 4].
