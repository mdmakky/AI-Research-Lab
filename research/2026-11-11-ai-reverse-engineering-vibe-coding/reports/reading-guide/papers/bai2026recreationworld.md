## RecreationWorld: Scalable and Verifiable Environments for Hybrid Computer-Use Agents
> **Takeaway:** When AI agents rebuild real apps by using a running original, even the best agent averages only 58.06% and passes every functional test on just 2.8% of apps [@bai2026recreationworld, p. 11]. The rebuilds are also much smaller and more concentrated in a few files than the originals [@bai2026recreationworld, p. 15]. This is the closest study to our topic, but it does not measure code quality.

| Item | Detail |
|---|---|
| Authors | Shuai Bai, Jiayong Deng, Sicheng Fan, Yikun Fu, Chang Gao, Xuhao Hu, et al. (33 authors, Alibaba Group) |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (not peer-reviewed); industry paper |
| Identifier | DOI 10.48550/arxiv.2609.22000 (arXiv 2609.22000) |
| Paper type | Benchmark and environment framework, with a model comparison and a training (transfer) experiment |
| Relevance to us | High — RQ1, RQ2, RQ3 (partly), RQ4, RQ5 |

### In plain words
Imagine giving an AI a working app, but not its source code, and asking it to build a copy that behaves the same way. That is "application recreation", which is very close to AI-assisted reverse engineering. The authors built a large test set for it on five platforms: Ubuntu, macOS, Windows, Android and the Web [@bai2026recreationworld, p. 7]. They tested ten of the newest AI models and studied how the agents worked and what code they produced. They also checked whether practising this task helps on other coding tasks [@bai2026recreationworld, p. 3].

### How they did it
1. They collected 250 reference apps. Desktop and Android apps came from open-source projects. The Web set has 44 sites the authors made themselves and 6 real, openly licensed sites [@bai2026recreationworld, p. 7].
2. Each agent got a task prompt, live access to the running original, and a computer with GUI control (the ability to look at and click an interface) and developer tools. It had to hand back source code that builds and launches [@bai2026recreationworld, p. 7]. On desktop and Android the agent could not see the original's source code. On the Web, the page code sent to the browser is necessarily visible [@bai2026recreationworld, p. 7]. Each attempt had up to 20 hours [@bai2026recreationworld, p. 4].
3. Hidden tests were written by AI agents, replayed on a clean copy of the original, cleaned of unstable cases, and reviewed by humans before being frozen [@bai2026recreationworld, p. 8].
4. Two scores were computed [@bai2026recreationworld, p. 9]. The Programmatic score is the share of tests passed; the tests read text, buttons and values through the accessibility interface (the system layer that screen readers use). The VLM score uses a vision-language model (an AI that reads images) as a judge, which checks screenshots against statements about the original. An app that does not build scores zero.
5. They then analysed agent behaviour and code size for four of the models [@bai2026recreationworld, p. 12].

### Data and setup
- 250 tasks, 50 per platform [@bai2026recreationworld, p. 7].
- Median original size: 49.3k lines of code on Ubuntu, 13.5k on macOS, 6.7k on Windows, 15.0k on Android [@bai2026recreationworld, p. 8].
- 10 models. GPT models ran in the Codex tool and all others in Claude Code [@bai2026recreationworld, p. 28].
- Network access was blocked by default, and reference and test files were protected [@bai2026recreationworld, p. 9].
- Runs per task are not reported. [I] Our reviewers think it was probably one run, because one single-run comparison reproduces a main-table score exactly [@bai2026recreationworld, p. 11].

### Key findings
- [V] GPT-6 Astra leads with an average of 58.06 (Programmatic 58.19, VLM 57.92). Next are Claude Opus 5 (44.16) and GPT-5.6 Sol (42.06); Qwen3.7-Plus is lowest (9.15) [@bai2026recreationworld, p. 11].
- [V] Full fidelity is rare. The best model passes at least 90% of tests on 17.6% of apps and all tests on 2.8%; every other model reaches at most 5.53% and 0.8% [@bai2026recreationworld, p. 11].
- [V] Agents copy what an interface contains better than what it does. Structure tests had the highest pass rate in 15 of 16 native comparisons, and the weakest category trailed by 9.1 to 34.4 points [@bai2026recreationworld, p. 16].
- [V] Rebuilds are smaller: 89.4% have less code than the original (median 16.9% of its size), and 92.3% use fewer files [@bai2026recreationworld, p. 15].
- [V] More code did not mean better fidelity. Among the four analysed models, Claude Opus 5 wrote the most code, while the top model GPT-6 Astra wrote the least on four of five platforms [@bai2026recreationworld, p. 15].
- [V] Agents often switched to a different UI framework, for example rebuilding 75% of Electron, Tauri or Wails desktop apps natively. [A] The authors call this "architectural substitution rather than implementation quality" [@bai2026recreationworld, p. 16].
- [V] Training two models on recreation runs left both above their starting checkpoint on five other benchmarks, by up to 17.9 points [@bai2026recreationworld, p. 3]. [A] The authors call this "exploratory" evidence [@bai2026recreationworld, p. 29].
- [V] Agents rarely checked their final work: the full "edit, relaunch, inspect" loop appears in only 23.6% to 47.5% of runs [@bai2026recreationworld, p. 12].

### Limitations and weaknesses
- [A] A finite test suite "cannot establish equivalence across all states and interaction paths" [@bai2026recreationworld, p. 22].
- [A] Public originals may be in the models' training data [@bai2026recreationworld, p. 22].
- [A] The behaviour and code analyses are descriptive and do not show cause and effect [@bai2026recreationworld, p. 3].
- [I] No confidence intervals and probably one run per task, so small gaps between models may not be stable [@bai2026recreationworld, p. 11]. Model and tool are also mixed up: GPT ran in Codex, the rest in Claude Code [@bai2026recreationworld, p. 28].
- [I] All authors are from Alibaba, and Qwen models serve as judge and as training-data generator. No conflict-of-interest statement is given [@bai2026recreationworld, p. 5]. The Qwen judge model scored lowest, so no favourable self-scoring is visible [@bai2026recreationworld, p. 11].
- [I] One Web site that replayed copied content escaped the cheating detector and kept a 54.82% Programmatic score [@bai2026recreationworld, p. 47].

### Gaps and future work this paper leaves open
- G1: code is described only by size and structure, never by maintainability [@bai2026recreationworld, p. 15].
- G2: the VLM judge is never checked against human ratings, and self-preference is not tested [@bai2026recreationworld, p. 9].
- G4: agents' weak self-checking [@bai2026recreationworld, p. 12] raises the question of whether better feedback loops would help.
- G5: copying looks rare (median exact-line overlap 0.014% to 0.088%) [@bai2026recreationworld, p. 18], but the authors still suggest newly built originals to reduce training-data risk [@bai2026recreationworld, p. 22].
- G6: [I] there is no human-developer or human-steered condition.
- G8: it is the only project paper with native Android rebuilds [@bai2026recreationworld, p. 7], but apps needing login or remote services were excluded [@bai2026recreationworld, p. 8].

### Why it matters for your research
[I] This is the strongest evidence that rebuilding apps from observation works only partly. Reuse its design ideas: tests checked against the original, two scoring channels and network isolation. Its main gap is your opportunity: rebuilds are smaller and more monolithic, but nobody knows whether they are harder to maintain. Avoid its weak points: run each task several times, validate any AI judge against humans, and keep model and tool separate.

### Connections to other papers
- Agrees with yang2026programbench: rebuilds are shorter and use fewer files than the originals [@yang2026programbench, p. 9], and full equivalence is rare there too (0 of 200 programs) [@yang2026programbench, p. 6].
- Builds on ProgramBench: it is one of the benchmarks used to test training transfer [@bai2026recreationworld, p. 6].
- Agrees with kim2026programdistill: agents rebuilding web apps from a live original recover only 49.15% of workflows [@kim2026programdistill, p. 11], and their self-checks miss errors [@kim2026programdistill, p. 12].
- Only partly agrees with chen2025iwr. Both find interaction harder than static structure [@chen2025iwr, p. 16]. But here the visual score is below the programmatic score for 9 of 10 models [@bai2026recreationworld, p. 11], so "looks right but behaves wrong" is not supported in general.
