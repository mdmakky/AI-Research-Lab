## Toward Functional and Non-Functional Evaluation of Application-Level Code Generation

> **Takeaway:** When 16 AI models rewrite 38 real Python projects from a short description, none passes more than 45% of the tests, and code quality measured against the original is middling. It is one of the very few studies that scores working behaviour and code quality on the same generated apps, using the original project as the yardstick.

| Item | Detail |
|---|---|
| Authors | Ruwei Pan, Yakun Zhang, Qingyuan Liang, Yueheng Zhu, Chao Liu, Lu Zhang, Hongyu Zhang |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (not peer-reviewed) |
| Identifier | DOI 10.48550/arxiv.2602.03462 · arXiv 2602.03462 |
| Paper type | Benchmark (RAL-Bench) plus controlled empirical comparison of 16 models |
| Relevance to us | High — RQ2, RQ3, RQ4, RQ5 (RQ1 secondary) |

### In plain words
Most code benchmarks test single functions or small fixes. The authors ask whether AI models can write a whole working application, with many files and dependencies, and whether that code is also good on qualities beyond "it works" [@pan2026functional, p. 1]. These other qualities are called non-functional: how maintainable, secure, robust, fast and resource-hungry the code is. They take real open-source projects as references, describe each in a short text, ask the AI to write the project, and test the result against the original [@pan2026functional, p. 2]. For us this is close to a joint "fidelity plus quality" study, although the AI never sees or runs the original app.

### How they did it
1. Pick projects: 38 maintained Python projects on GitHub (for example click, requests, celery), each frozen at a fixed version, in seven scenario groups [@pan2026functional, p. 2].
2. Write requirements: a short natural-language description built from the project's README, API, examples and code, then edited to remove implementation details and project names [@pan2026functional, p. 2].
3. Add an interface specification: the list of modules and packages the result should expose [@pan2026functional, p. 4].
4. Generate: each model writes the whole repository in one go, "zero-shot" (no examples and no second attempt). Each model runs 3 times and scores are averaged [@pan2026functional, p. 5].
5. Test behaviour: black-box tests (tests that only check inputs and outputs, not the code inside) are kept only if they pass on the original. The functional score is the share of tests passed [@pan2026functional, p. 4].
6. Test quality: five dimensions, each compared with the original and capped at 1 [@pan2026functional, p. 3]. Maintainability uses the Maintainability Index (MI), a formula that turns code complexity and size into one number. Security counts high-risk findings from static analysis (automatic code scanning without running it). Robustness, efficiency and resource use (memory and CPU) come from extra test runs [@pan2026functional, p. 4].
7. Combine: the five dimensions are weighted (maintainability 0.36, security 0.24, robustness 0.16, efficiency 0.12, resource 0.12) into one non-functional score (NF) [@pan2026functional, p. 4].
8. Extra studies: a failure analysis, costs, three improvement strategies on GPT-5.2, prompt wording, and different weightings [@pan2026functional, p. 5].

### Data and setup
- 38 projects of 1 to 242 files and 0.3k to 109.5k lines of code [@pan2026functional, p. 2].
- About 11 functional tests per task on average (minimum 10, maximum 19) [@pan2026functional, p. 5].
- 16 models: 11 "standard" and 5 "thinking" (reasoning) models, 3 runs each [@pan2026functional, p. 5].
- 76 deliberately injected bugs (2 per task) to check that the tests catch errors [@pan2026functional, p. 5].
- The pipeline was rerun 5 times for three models to check stability [@pan2026functional, p. 7].
- Greedy decoding is stated only in the abstract [@pan2026functional, p. 1]. Scripts and data are released (author claim) [@pan2026functional, p. 11].

### Key findings
- [V] Functional correctness is low: on average 33.98% for standard and 30.23% for thinking models, and no model exceeds 45%. The best is Gemini-3-Pro-Preview at 43.86%; the lowest is DeepSeek-R1 at 16.23% [@pan2026functional, p. 6].
- [V] Non-functional scores average 52.25% (standard) and 49.57% (thinking). Security is the strongest dimension (87.40% / 85.32%). Resource usage is the weakest (31.25% / 28.92%), with maintainability close behind (33.45% / 31.38%) [@pan2026functional, p. 6].
- [V] Quality separates models that function equally well: Gemini-2.5-Pro and GPT-4o score almost the same functionally (27.63% vs 27.48%), but 35.15% vs 57.59% on NF [@pan2026functional, p. 5].
- [V] Thinking models are not consistently better [@pan2026functional, p. 6].
- [V] 82.8% of failures happen after the code runs (wrong behaviour or poor quality); 17.2% are install or start-up failures [@pan2026functional, p. 7].
- [V] Cost per run ranges from $0.15 to $16.63, and paying more does not reliably buy correctness [@pan2026functional, p. 8].
- [V] On GPT-5.2, self-repair, environment repair and planning all failed to beat the baseline (41.80% functional, 57.10% NF) and all lowered NF, to 46.10–49.90% [@pan2026functional, p. 8].
- [V] Giving the module list raised one task's functional score from 0.1667 to 0.6667 [@pan2026functional, p. 4]. Rewording the prompt moved GPT-5.2 from 0.4181 to 0.4972 [@pan2026functional, p. 9].

### Limitations and weaknesses
- [A] The projects are public, so the authors "do not claim that pretraining exposure can be fully ruled out" [@pan2026functional, p. 2].
- [A] MI misses naming quality and architecture; static security scans give false alarms and misses; all metrics are proxies, not expert audits [@pan2026functional, p. 3].
- [A] One-shot generation does not represent iterative, agent-based work; the strategy study uses one model [@pan2026functional, p. 8].
- [I] About 11 tests is a thin check for projects of up to 109.5k lines, and 2 injected bugs per task is a weak test of the tests.
- [I] Memorisation looks likely: the example requirement names the original "Stegano project" [@pan2026functional, p. 3], and one output used internals of the real Celery library [@pan2026functional, p. 9].
- [I] The quality score can reward incomplete code. GPT-3.5-Turbo scores 97.37% on security but 29.76% on function [@pan2026functional, p. 6]; less code means fewer findings.
- [I] The maintainability score equals 0.5, not 1, when the rebuild matches the original [@pan2026functional, p. 3], yet it has the largest weight.
- [I] Zero variance across 5 reruns [@pan2026functional, p. 7] is surprising and may mean cached outputs were re-tested. The authors call the prompt effect small, but it is about 30–40% of the spread between models.
- [I] Python libraries only; no user interfaces are tested.

### Gaps and future work this paper leaves open
- [A] The authors propose quality-aware generation, repair across modules, and multi-turn, agent-based evaluation [@pan2026functional, p. 10].
- [I] G1: this is the only reference-anchored maintainability score in our corpus, but it is a single MI proxy, from text requirements rather than observed behaviour [@pan2026functional, p. 3].
- [I] G4: does feedback improve function and quality together? Here it harmed quality, for one model and one-shot strategies.
- [I] G5 and G7: memorisation and interface hints may inflate scores; neither effect is measured.
- [I] G3: whether MI agrees with other quality tools is untested.

### Why it matters for your research
[I] This paper shows the design you want, in rough form: measure behaviour and quality on the same rebuild and use the original as the baseline. Reuse the idea of tests kept only if they pass on the original, and of quality scores relative to the original. Improve on it: use richer, size-normalised quality measures, more tests, an iterative workflow, and controls for memorisation. Its result that repair strategies lowered quality is a warning for vibe-coding loops, but it is weak evidence (preprint, one model).

### Connections to other papers
- [V] Disagrees on security with zhao2025vibe, where 79.3% of functionally correct solutions fail targeted security tests [@zhao2025vibe, p. 6]. [I] Static counts and attack-style tests measure different things.
- [V] Conflicts on feedback with tran2026vibe (browser self-testing correlates with accuracy, r = 0.72) [@tran2026vibe, p. 7] and zhou2025declarui (refinement loop lifts navigation) [@zhou2025declarui, p. 10]. [I] Those loops check the very thing they score; this one measures quality after repair.
- [V] Agrees that function and quality diverge: in wu2026looks the visual leader is not the maintainability leader [@wu2026looks, p. 7].
- [V] Rebuilds elsewhere are much smaller than their originals [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9]. [I] That is why size-sensitive quality scores like this one need care.
- [V] borg2026echoes offers a stronger maintainability test: a second developer evolves the code [@borg2026echoes, p. 13].
