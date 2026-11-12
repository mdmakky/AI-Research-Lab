## E2EDev: Benchmarking Large Language Models in End-to-End Software Development Task

> **Takeaway:** E2EDev starts from real, existing web apps, writes tests that pass on the originals, and asks AI systems to rebuild each app from its requirements. The best setup fully satisfies only 53.75% of requirements, and multi-agent frameworks do not consistently beat a plainly prompted model.

| Item | Detail |
|---|---|
| Authors | Jingyao Liu, Chen Huang, Zhizhao Guan, Wenqiang Lei, Yang Deng |
| Year · Venue | 2026 · Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026, Long Papers) |
| Status | Peer-reviewed. We read the published ACL Anthology version |
| Identifier | DOI 10.18653/v1/2026.acl-long.1618 · arXiv 2510.14509 |
| Paper type | Benchmark plus comparative evaluation (6 frameworks × 6 models, 3 runs) plus human failure analysis |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5; the closest design to reverse engineering among the spec-to-app benchmarks |

### In plain words
Most earlier tests of AI software builders used vague task descriptions and scored the results by human opinion or rough rules [@liu2026benchmarking, p. 1]. The authors wanted something stricter. They took 46 small, popular web apps from GitHub, wrote down exactly what each app should do, and wrote automatic tests that pass on the original app [@liu2026benchmarking, p. 5]. Then they asked AI systems to rebuild each app from that written description and ran the same tests on the rebuild. This is very close to our idea of reconstruction: the original app is the yardstick for the copy.

### How they did it
1. Choose apps: GitHub web projects with more than 500 stars that run in about five minutes without a database or API key [@liu2026benchmarking, p. 12].
2. Add anchors: GPT-4o agents inserted data-testid labels into the original source. A data-testid is a fixed name attached to a button or field so that a test can find it [@liu2026benchmarking, p. 3].
3. Extract requirements: AI agents read the code and wrote user-facing requirements; human supervisors checked them against the running app [@liu2026benchmarking, p. 4].
4. Write tests: an agent wrote BDD tests. BDD (behaviour-driven development) means tests written as plain "Given … When … Then …" scenarios. Five software-testing experts reviewed and extended them [@liu2026benchmarking, p. 4].
5. Automate tests: an agent turned each scenario into Python code that drives a real Chrome browser through Selenium, with self-correction and human fallback [@liu2026benchmarking, p. 5].
6. Check the tests: every test passes on the original projects [@liu2026benchmarking, p. 5].
7. Rebuild: each AI setup received the project summary, the requirements and the data-testid names [@liu2026benchmarking, p. 16].
8. Score: the tests give a plain pass or fail; no AI judge is involved [@liu2026benchmarking, p. 5]. Req.Acc is the share of requirements whose tests all pass; Test.Acc is the share of single tests that pass. Results are averaged over three runs, and cost and time are also recorded [@liu2026benchmarking, p. 5].

### Data and setup
- 46 projects, 244 requirements and 703 tests (about 15 tests per project) [@liu2026benchmarking, p. 3].
- Project types include calculators, form apps and mini games [@liu2026benchmarking, p. 18].
- Six frameworks: a plain prompted model ("Vanilla"), GPT-Engineer (single agent), and four multi-agent systems (Self-Collaboration, MapCoder, ChatDev, MetaGPT). A multi-agent framework splits the work among several AI "roles" that talk to each other [@liu2026benchmarking, p. 5].
- Six backbone models: Claude-Haiku 4.5, GPT-4o, GPT-4o-mini, Qwen2.5-7B, Qwen2.5-72B and Qwen2.5-Max [@liu2026benchmarking, p. 5]. OpenHands and SWE-Agent ran on two of them only [@liu2026benchmarking, p. 20].
- Test quality audit: 10 experts reviewed 100 sampled tests with Fleiss' kappa 0.81 [@liu2026benchmarking, p. 14]. Kappa is an agreement score corrected for chance; 1 means perfect agreement.
- A human failure analysis covered 360 generated projects [@liu2026benchmarking, p. 7].

### Key findings
- [V] The best setting, GPT-Engineer with Claude-Haiku 4.5, reaches Req.Acc 53.75 ± 0.43 and Test.Acc 69.41 ± 1.07 [@liu2026benchmarking, p. 6]. [A] The authors summarise most settings as "only 30%–50%" [@liu2026benchmarking, p. 5].
- [V] Partial success is common: a softer score that gives credit for partly met requirements is about 25–33 points higher in most settings [@liu2026benchmarking, p. 25].
- [A] "Agentic frameworks do not consistently improve the effectiveness of base LLMs" [@liu2026benchmarking, p. 6]. [V] Example: with GPT-4o-mini, Vanilla scores 44.82 vs ChatDev 33.16 and MapCoder 41.30 [@liu2026benchmarking, p. 6]. [I] By our count, only 9 of 24 multi-agent cells beat Vanilla, mostly by small margins.
- [V] Most multi-agent frameworks cost more but the sums are small: GPT-4o ChatDev costs $0.1947 per task vs $0.0160 for Vanilla, while Self-Collaboration costs about the same as Vanilla. All four multi-agent frameworks are slower, e.g. 28 s for Vanilla vs 114 s for ChatDev on GPT-4o [@liu2026benchmarking, p. 6].
- [V] MetaGPT almost always fails (0.00–5.39 Req.Acc) [@liu2026benchmarking, p. 6]; 44% of its failures are code inconsistency such as missing files [@liu2026benchmarking, p. 8].
- [V] The same frameworks score 71–91% on the small-function benchmark HumanEval, far above their E2EDev scores [@liu2026benchmarking, p. 27].
- [V] OpenHands and SWE-Agent score below Vanilla on Claude-Haiku 4.5 (43.45 and 44.73 vs 48.69) [@liu2026benchmarking, p. 23].
- [V] Building the benchmark still needed humans: about 50% of test cases were refined by hand, at about 3.5 hours per project [@liu2026benchmarking, p. 15].

### Limitations and weaknesses
- [A] Only 46 projects, because executable tests are costly to build [@liu2026benchmarking, p. 9].
- [A] Web apps only; CI/CD and deep back-end checks are excluded [@liu2026benchmarking, p. 9].
- [I] Tests depend on data-testid names copied from the original and given in the prompt [@liu2026benchmarking, p. 16]. A correct rebuild that names elements differently would fail. A true black-box rebuild would not have these names.
- [I] The only check of automatic vs human scoring (Cohen's kappa 0.74) does not describe its sample or unit [@liu2026benchmarking, p. 22].
- [I] Reporting is inconsistent in places: four vs five annotators [@liu2026benchmarking, p. 7; @liu2026benchmarking, p. 21], and strict scores in one table differ from the main table [@liu2026benchmarking, p. 25].
- [I] Popular public projects may be in the models' training data; this is not discussed [@liu2026benchmarking, p. 12].
- [I] Requirements are very detailed, unlike vague vibe-coding prompts [@liu2026benchmarking, p. 16]. The models are small or older ones, apps are front-end only, decoding settings are not reported, and there are no significance tests.
- [I] No code quality or maintainability measure.

### Gaps and future work this paper leaves open
- [A] The authors call for reliable, cost-efficient end-to-end methods and a larger, maintained benchmark [@liu2026benchmarking, p. 9].
- [I] G7: how much the identifier-tied tests distort fidelity scores is unmeasured. Our G7 study would rewrite E2EDev tests with locators based on visible text and roles and compare [@liu2026benchmarking, p. 9].
- [I] G1: E2EDev apps with validated tests could form "Stratum A" of the G1 study [@liu2026benchmarking, p. 5].
- [I] G5: contamination is not discussed. G3: E2EDev outputs could test whether quality tools agree.

### Why it matters for your research
[I] E2EDev gives you a concrete template for measuring fidelity: start from an existing app, write behaviour tests that pass 100% on the original, then run them on the rebuild. Its released apps and tests are reusable. Two things to avoid: tying tests to the original's internal names, and assuming that more elaborate agent setups give better rebuilds. Note that its 53.75% is not comparable with scores from other benchmarks.

### Connections to other papers
- [V] Converges with kim2026programdistill and tran2026vibe: the best requirement- or workflow-level pass rates in this field sit around 49–62% [@kim2026programdistill, p. 11; @tran2026vibe, p. 6].
- [V] Shares the identifier problem with kim2026programdistill, whose tests also use the original's selectors [@kim2026programdistill, p. 35]. yang2026programbench and bai2026recreationworld avoid it with implementation-agnostic tests [@yang2026programbench, p. 5; @bai2026recreationworld, p. 9].
- [V] Contrasts with mock2026vibe, where agentic MetaGPT X had the highest test pass rate (mean 94.58%) [@mock2026vibe, p. 25], but on a tiny two-function task with newer models [@mock2026vibe, p. 12]. [I] Framework value likely depends on the model and task size.
- [V] Differs from tran2026vibe, which scores with an AI browser judge rather than deterministic tests [@tran2026vibe, p. 4].
- [V] GPT-4o built the annotations and was evaluated, but the best backbone was Claude-Haiku [@liu2026benchmarking, p. 13]; no self-advantage is visible.
