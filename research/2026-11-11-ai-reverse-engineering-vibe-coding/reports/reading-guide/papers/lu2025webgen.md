## WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scratch

> **Takeaway:** When AI coding agents build whole websites from a plain-language request, even the best early-2025 setup passes only 27.8% of the test cases, and visual or design requirements are met far more often than functional ones. A site can look right while its features do not work.

| Item | Detail |
|---|---|
| Authors | Zimu Lu, Yunqiao Yang, Houxing Ren, Haotian Hou, Han Xiao, Ke Wang, et al. (10 authors in our metadata; the arXiv PDF author line differs slightly) |
| Year · Venue | 2025 · Advances in Neural Information Processing Systems 38 (NeurIPS 2025) |
| Status | Peer-reviewed. We read the arXiv v2 version, which is marked "Under review"; the published version may differ in details |
| Identifier | DOI 10.52202/085713-2419 · arXiv 2505.03733 |
| Paper type | Benchmark plus comparative evaluation, with a fine-tuning experiment |
| Relevance to us | High — RQ1, RQ2, RQ4; RQ5 by what it leaves out (no code quality) |

### In plain words
The authors ask a simple question: can an AI agent build a complete, working website on its own if you only describe what you want in everyday words? To answer it they built a benchmark, which is a fixed set of tasks plus an automatic way of scoring them, so that different AI systems can be compared fairly [@lu2025webgen, p. 3]. The tasks are 101 website requests, such as small business or data-management sites, and each comes with a list of things a user should be able to do [@lu2025webgen, p. 5]. A second AI then clicks through each generated site like a tester and reports whether each feature works [@lu2025webgen, p. 6]. This matters for us because it was one of the first studies to score whole AI-built apps by their behaviour, not just by how the code looks.

### How they did it
1. They collected 20 categories of web applications from freelance job platforms. Forty computer-science PhD students brainstormed 10,152 project ideas, and GPT-4o turned them into instructions [@lu2025webgen, p. 5].
2. They picked 101 instructions as the test set [@lu2025webgen, p. 5].
3. For each instruction, GPT-4o drafted 5–10 test cases. A test case is one small action plus the expected result (for example "click Add, a new row appears"). Two PhD students checked and corrected them, giving 647 test cases [@lu2025webgen, p. 6].
4. Three agent frameworks built the sites: Bolt.diy, OpenHands and Aider. An agent framework is the software around a language model that lets it write files and run commands on its own [@lu2025webgen, p. 7].
5. A "UI agent" (WebVoyager, driven by the Qwen2.5-VL-32B model) opened each site, tried each test case in at most 15 interactions, and answered YES, PARTIAL or NO [@lu2025webgen, p. 6].
6. Accuracy is (YES + 0.5 × PARTIAL) divided by all test cases. A site that does not start counts as a failure [@lu2025webgen, p. 8].
7. GPT-4o also gave each site an appearance grade from 1 to 5 [@lu2025webgen, p. 6].
8. To check the automatic tester, three humans tested three settings by hand and their labels were compared with the UI agent's [@lu2025webgen, p. 8].
9. Finally they fine-tuned (further trained) open Qwen2.5-Coder models on 600 recorded agent runs to see whether training helps [@lu2025webgen, p. 7].

### Data and setup
- 101 test instructions: 28 content presentation, 49 user interaction, 24 data management [@lu2025webgen, p. 6].
- 647 test cases: 339 functional, 186 data display, 122 design validation [@lu2025webgen, p. 23]. That table prints "Total 667", which is a typo; the categories add up to 647.
- Models included Claude-3.5-Sonnet, DeepSeek-R1, DeepSeek-V3, GPT-4o, o3-mini and Qwen2.5 models, mostly inside Bolt.diy [@lu2025webgen, p. 7].
- One run per setting. Temperature and time budgets are not reported [@lu2025webgen, p. 40].
- Testing all 647 cases by hand would take about 10.8 hours and $377.8 per setting, which is why they automated it [@lu2025webgen, p. 6].
- Data, code and models are released under an MIT licence (author claim; we did not check the link) [@lu2025webgen, p. 1].

### Key findings
- [V] The best general-model setting, Bolt.diy with DeepSeek-R1, reaches only 27.8% accuracy; Bolt.diy with Claude-3.5-Sonnet reaches 26.4% [@lu2025webgen, p. 8].
- [V] The framework matters a lot. With the same model (DeepSeek-V3), accuracy is 20.8% in Bolt.diy, 14.1% in Aider and 9.0% in OpenHands [@lu2025webgen, p. 8].
- [V] Many sites never start: start failures reach 38.6% for Bolt.diy with o3-mini [@lu2025webgen, p. 8].
- [V] Functional tests are much harder than design tests: 21.1% vs 44.3% for Bolt.diy with DeepSeek-R1, and 17.1% vs 52.0% with Claude-3.5-Sonnet [@lu2025webgen, p. 9].
- [A] The authors conclude that "superficial aspects, such as color themes, are easier to implement than deeper internal functionalities" [@lu2025webgen, p. 8].
- [V] The UI agent agrees with the human label on 86.1–94.4% of test cases in the three checked settings [@lu2025webgen, p. 9].
- [V] Fine-tuning Qwen2.5-Coder-32B on 600 runs lifts accuracy from 9.5% to 38.2%, and more training data helps (25.1% with 150, 31.9% with 300, 38.2% with 600) [@lu2025webgen, p. 10].

### Limitations and weaknesses
- [A] Only TypeScript, JavaScript, CSS and HTML sites; only supervised fine-tuning was tried [@lu2025webgen, p. 14].
- [A] No error bars "because it would be too computationally expensive" [@lu2025webgen, p. 40].
- [I] The human check covers only 3 of 16 settings, all in Bolt.diy. Agreement is raw percent with no chance correction, and agreement between the humans themselves is not reported [@lu2025webgen, p. 9].
- [I] Most labels are NO (58–74%), so a tester that often says NO gets high agreement almost by default [@lu2025webgen, p. 9].
- [I] Each test checks one small visible feature, and PARTIAL earns half credit [@lu2025webgen, p. 8]. Deeper behaviour such as saved data or multi-step workflows is not tested.
- [I] With a single run, differences of 1–2 points (27.8 vs 26.4) cannot be told apart from noise.
- [I] The fine-tuning data was filtered by appearance score, not by functional tests [@lu2025webgen, p. 7].
- [I] No code quality, security or maintainability is measured.

### Gaps and future work this paper leaves open
- [A] The authors want more languages and tools, and other training methods (RL, DPO) [@lu2025webgen, p. 14].
- [I] G1: the generated code is never checked for quality or maintainability.
- [I] G2: GPT-4o wrote the test cases and is also evaluated. It scored low, so no advantage is visible [@lu2025webgen, p. 8], but bias was not tested. The released outputs could be re-judged in a G2 study [@lu2025webgen, p. 1].
- [I] G6: there is no human-developer baseline [@lu2025webgen, p. 7].
- [I] For reconstruction, tests would need to come from an existing site's observed behaviour, not from an instruction.

### Why it matters for your research
[I] WebGen-Bench set the pattern that many later benchmarks copy: AI-drafted, human-checked test cases run by a visual browser agent, plus a check against human testers. You can reuse this idea to score a rebuilt app against its original. Its main lesson for you is the gap between design and function: a rebuild that looks like the original may still fail on behaviour. Avoid two of its weak points in your own study: single runs, and judge checks on only a few settings without chance-corrected agreement.

### Connections to other papers
- Agrees with chen2025iwr, where interactive functionality scores below visual fidelity for all models (GPT-5: 24.39 vs 64.25) [@chen2025iwr, p. 8], and with xiao2025benchmarking, where interactive regions score lower than full pages [@xiao2025benchmarking, p. 6].
- Partly disagrees with bai2026recreationworld, where the visual channel scores below the programmatic channel for 9 of 10 models [@bai2026recreationworld, p. 11]. [I] The visual and functional scales differ across papers, so "looks right, works wrong" is only directionally supported.
- tran2026vibe builds on the same idea with multi-step browser workflows [@tran2026vibe, p. 4] and shows that judge agreement with humans ranges from 36.1% to 86.4% depending on the judge model [@tran2026vibe, p. 9]. [I] So the 86–94% here holds only for this judge.
- [I] Do not compare its 27.8% with E2EDev's 53.75% [@liu2026benchmarking, p. 6] or Vibe Code Bench's 61.77% [@tran2026vibe, p. 6]; each uses a different test method and scoring rule.
