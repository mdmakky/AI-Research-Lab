## Vibe Coding: An experiment with test-driven development
> **Takeaway:** On two tiny Python tasks, an AI agent produced the most correct code fastest, but its code was more complex. Humans working with an AI were not better than humans alone. The agent also used much newer AI models, so the comparison is not fair.

| Item | Detail |
|---|---|
| Authors | Moritz Mock, Barbara Russo |
| Year · Venue | 2026 · Empirical Software Engineering (journal; printed volume dated 2027) |
| Status | Peer-reviewed |
| Identifier | DOI 10.1007/s10664-026-10950-z |
| Paper type | Small controlled experiment with professionals, plus exploratory repeated runs of automated and agentic workflows |
| Relevance to us | Medium — RQ1, RQ2, RQ3, RQ4, RQ5 (mainly design lessons) |

### In plain words
The authors ask how humans and AI chatbots can work together as peers when writing code [@mock2026vibe, p. 1; @mock2026vibe, p. 2]. They use test-driven development (TDD: you write tests first, then the code that makes them pass). They compared four ways of working on the same small tasks: a human alone, a human writing tests while the AI writes code, a script letting one AI do everything, and an AI agent platform [@mock2026vibe, p. 7; @mock2026vibe, p. 8]. Here "vibe coding" means the human-plus-AI version, with fixed prompts the human could not change [@mock2026vibe, p. 15]. This matters because it is one of the few experiments that labels a condition "vibe coding" and compares it with humans and agents.

### How they did it
1. Define four workflows: solo (human only), collaborative (human writes tests, AI writes code; the paper's "vibe coding"), fully automated (scripts drive one AI to write both tests and code), and agentic (the MetaGPT X platform) [@mock2026vibe, p. 7; @mock2026vibe, p. 8; @mock2026vibe, p. 17].
2. Give everyone the same two small tasks: centre one word, then two words, in a line of text [@mock2026vibe, p. 12].
3. Build an answer key: 12 checks (assertions) derived from the specification by category-partition testing (a systematic way to cover each type of input) [@mock2026vibe, p. 11; @mock2026vibe, p. 12].
4. Run the human sessions. 16 professionals were split into solo and collaborative groups, with a 40-minute limit [@mock2026vibe, p. 15; @mock2026vibe, p. 16].
5. Run the automated workflows several times each [@mock2026vibe, p. 42].
6. Measure correctness (share of the 12 checks passed), McCabe complexity (a count of decision paths in code), test coverage, code similarity, iterations and time [@mock2026vibe, p. 14].
7. Compare groups with rank-based tests (Kruskal-Wallis, then one-sided Mann-Whitney), with Cliff's delta effect sizes and Holm-Bonferroni correction for multiple tests [@mock2026vibe, p. 10; @mock2026vibe, p. 11].

### Data and setup
- 16 professional developers from Italy, Denmark and Brazil: 9 solo, 7 collaborative [@mock2026vibe, p. 15; @mock2026vibe, p. 16].
- Many had less than 1 year of TDD or Python experience [@mock2026vibe, p. 16].
- Collaborative and fully automated workflows used GPT-3.5 Turbo; agentic runs used ChatGPT 5 or Claude Sonnet 4 [@mock2026vibe, p. 14; @mock2026vibe, p. 17].
- 3 fully automated runs and 12 agentic runs (2 models x 2 prompt versions x 3 runs) [@mock2026vibe, p. 42].
- Prompts told the AI not to use built-in functions; a failing test triggered up to five automatic re-prompts [@mock2026vibe, p. 19; @mock2026vibe, p. 20].
- Human time was self-reported; automated time was machine-measured [@mock2026vibe, p. 13; @mock2026vibe, p. 17].
- Replication package on GitHub [@mock2026vibe, p. 43].

### Key findings
- [V] Correctness: agentic 94.58% of checks passed on average, versus fully automated 83.3%, solo 62.0% and collaborative 60.8% [@mock2026vibe, p. 41; @mock2026vibe, p. 42].
- [V] Collaborative vibe coding was not significantly different from solo coding in correctness [@mock2026vibe, p. 25]. Human results ranged from 8.3% to 100% [@mock2026vibe, p. 26].
- [V] Agentic code was more complex: mean McCabe 11.67 vs about 6.0–6.6 for the other workflows [@mock2026vibe, p. 41; @mock2026vibe, p. 42].
- [V] Agentic code had lower branch coverage by the answer-key tests (65.33%) than solo (83.89%) and collaborative (79.00%) code [@mock2026vibe, p. 41; @mock2026vibe, p. 42].
- [V] Agentic code kept the main solution but added helper methods, logging and validation [@mock2026vibe, p. 24].
- [V] Agentic runs were fastest: 75 s on average vs 800 s (fully automated), 2,057 s (collaborative) and 2,266 s (solo) [@mock2026vibe, p. 41; @mock2026vibe, p. 42].
- [A] The authors call agentic solutions "potentially more difficult to maintain", but maintainability was not measured directly [@mock2026vibe, p. 35].
- [I] Caution on statistics: for some comparisons the reported one-sided p-values point the wrong way relative to the effect sizes (for example Table 9 [@mock2026vibe, p. 25] and Table 10 [@mock2026vibe, p. 27]). The main conclusions match the group averages, but do not quote single p-values from this paper without this caveat.

### Limitations and weaknesses
- [A] Human and automated workflows were tested in different settings, so cross-comparisons need care [@mock2026vibe, p. 36].
- [A] Few participants, so low statistical power; tasks are simple [@mock2026vibe, p. 36; @mock2026vibe, p. 37].
- [A] The agentic part is exploratory [@mock2026vibe, p. 17].
- [I] Model confound: agents used GPT-5 and Claude Sonnet 4, humans' AI used GPT-3.5 Turbo. The agent's advantage cannot be separated from the newer model [@mock2026vibe, p. 17].
- [I] The "vibe coding" condition used scripted prompts participants could not modify [@mock2026vibe, p. 15], so it is not free-form vibe coding.
- [I] Repeated runs of one setup were treated like independent people in the tests.
- [I] McCabe complexity is the only maintainability measure.

### Gaps and future work this paper leaves open
- [A] Try other practices, AI models and agent platforms; test agents under different prompts [@mock2026vibe, p. 17; @mock2026vibe, p. 40].
- [I] G6: a fair human-steered vs autonomous comparison with the same model is still missing [@mock2026vibe, p. 17].
- [I] G1: larger, application-level tasks with richer maintainability measures are needed.

### Why it matters for your research
Reuse its evaluation framework: an answer-key test suite derived from the specification for correctness, complexity and coverage for internal quality, and time and iterations for effort. That maps well onto measuring fidelity in a rebuilt app. Avoid its flaws: hold the AI model constant across conditions, use more than one maintainability measure, and use larger tasks. Do not cite its results as evidence about app reconstruction.

### Connections to other papers
- [V] Disagrees with liu2026benchmarking, where MetaGPT nearly always failed on larger web apps [@liu2026benchmarking, p. 6]. Task size and model generation differ (evidence matrix C6).
- [V] Its higher agentic complexity echoes he2026speed's rise in complexity after adopting an agentic tool [@he2026speed, p. 7], though at a tiny scale.
- [V] Its "vibe coding" is narrower than fawzy2026vibe's minimal-review prompting [@fawzy2026vibe, p. 1]; do not pool (C9).
- [V] Like borg2026echoes, human results varied widely, and individual skill mattered [@borg2026echoes, p. 40].
