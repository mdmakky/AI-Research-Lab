## Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks

> **Takeaway:** Code that passes its functional tests is often not secure. Even the best AI coding agent produced working code for 57.0% of tasks, but only 11.8% of tasks were solved both correctly and securely, so "it works" and "it is good code" must be measured separately [@zhao2025vibe, p. 7].

| Item | Detail |
|---|---|
| Authors | Songwen Zhao, Danqing Wang, Kexun Zhang, Jiaxuan Luo, Zhuo Li, Lei Li |
| Year · Venue | 2025 · Published at ICML 2026 (our copy: arXiv v4) |
| Status | Peer-reviewed (ICML 2026, PMLR 306, per the PDF footer; our metadata still lists it as an arXiv preprint) |
| Identifier | arXiv 2512.03262 (DOI 10.48550/arxiv.2512.03262) |
| Paper type | Benchmark plus comparative evaluation of AI coding agents |
| Relevance to us | Medium — RQ2, RQ3, RQ4, RQ5 |

### In plain words
"Vibe coding" means asking an AI agent in plain language to build a feature, and then using the result with little human checking. This paper asks a simple question: is the code that such agents write safe to put into real software? The authors built a test set of 186 real programming tasks where human programmers had once written code with a security hole. They then asked 12 different AI agent setups to write the same features and checked two things: does the code work, and is it secure? The answer is worrying: most working solutions still contain the old security hole. This matters for us because it shows that checking whether software "behaves correctly" says little about other qualities of the code.

### How they did it
1. They started from real security fixes in open-source Python projects. Each fix has a "before" version (with the vulnerability) and an "after" version (fixed) [V] [@zhao2025vibe, p. 3].
2. In the "before" version, an AI agent removed (masked) the code of one feature. A second agent wrote a feature request in the style of a GitHub issue (a short task description). The description had to explain what the feature does, without any hint about security [V] [@zhao2025vibe, p. 4; @zhao2025vibe, p. 16].
3. The masks were built on the vulnerable version, not the fixed one, so that no information from the fix leaks into the task [A] [@zhao2025vibe, p. 4].
4. Each AI agent then had to re-implement the missing feature inside the full repository. It could run code and use the results, for up to 200 steps [V] [@zhao2025vibe, p. 6].
5. Two kinds of tests were run on the result. Functional tests (the project's existing tests) check whether the feature works. Security tests (tests added by the historical fix) check whether the old vulnerability is back [V] [@zhao2025vibe, p. 4; @zhao2025vibe, p. 5].
6. Scoring used pass@1 (the share of tasks solved on the first and only try). FuncPass counts tasks that pass the functional tests; SecPass counts tasks that pass both functional and security tests [V] [@zhao2025vibe, p. 6]. No AI judge was used for scoring [V] [@zhao2025vibe, p. 6].
7. Five software-engineering experts checked the security tests and rewrote those that were too tied to one specific implementation [V] [@zhao2025vibe, p. 19].

### Data and setup
- 186 tasks from 100 Python repositories, covering 10 application domains and 79 CWE types (CWE = a standard catalogue of software weakness types) [V] [@zhao2025vibe, p. 2; @zhao2025vibe, p. 13].
- Tasks are large: on average 236K lines of context, a 175.0-line target change, 66.9 functional tests and 3.5 security tests per task [V] [@zhao2025vibe, p. 5].
- 12 agent settings: 3 agent frameworks (SWE-agent, OpenHands, Claude Code) times 4 models (Claude 4 Sonnet, Kimi K2, Gemini 2.5 Pro, Gemini 3 Pro) [V] [@zhao2025vibe, p. 6].
- One run per task. Temperature, exact model versions and cost are not reported [V] [@zhao2025vibe, p. 6].
- The main runs already include a short generic security reminder in the prompt [V] [@zhao2025vibe, p. 7].

### Key findings
- [V] The best setting, SWE-agent with Claude 4 Sonnet, reached FuncPass 57.0% but SecPass only 11.8% [@zhao2025vibe, p. 7]. 79.3% of its working solutions were insecure [@zhao2025vibe, p. 6].
- [V] Across all 12 settings, FuncPass ranged from 12.9% to 57.0% and SecPass from 3.8% to 12.9% [@zhao2025vibe, p. 7].
- [V] Success drops when the change spans more files. For Claude 4 Sonnet, FuncPass fell from 66.9% (one file) to 30.3% (more than two files), and SecPass from 15.4% to 3.0% [@zhao2025vibe, p. 14].
- [V] Simple security prompting helped little. Giving the agent the exact weakness type raised SecPass from 11.8% to 15.1%, while FuncPass fell from 57.0% to 55.4%; letting the agent pick weakness types itself gave 50.0% / 14.5% [@zhao2025vibe, p. 8].
- [V] When asked to choose weakness types, agents picked 7.2 types per task against 1.1 true types, with precision of only 0.086 to 0.114 [@zhao2025vibe, p. 9].
- [V] On tasks that all models solved, Gemini 2.5 Pro had the highest secure share (30.4% vs 18.3% for Claude 4 Sonnet), although it was functionally the weakest [@zhao2025vibe, p. 6]. [I] Treat this ranking as weak: the size of this shared subset is never reported and can be at most about 24 to 37 tasks per framework, based on the FuncPass numbers [@zhao2025vibe, p. 7].

### Limitations and weaknesses
- [A] Python only; tests are a practical stand-in for security, and the tests may not cover all weaknesses [@zhao2025vibe, p. 24].
- [A] Security tests from historical fixes can reject secure alternative solutions; 6.5% were tied to the original implementation and were rewritten [@zhao2025vibe, p. 19].
- [I] Only one run per task and no confidence intervals. With 186 tasks, one task is about 0.54 percentage points, so small differences such as 11.8% vs 12.9% may be noise [@zhao2025vibe, p. 7].
- [I] No agreement score between the five experts is reported [@zhao2025vibe, p. 19].
- [I] The tasks rebuild public historical code from popular projects, so models may have seen the fixed versions in training; the paper does not discuss this [@zhao2025vibe, p. 13].
- [I] Claude 4 Sonnet built the test environments [@zhao2025vibe, p. 17] and SWE-agent built the tasks [@zhao2025vibe, p. 4], and SWE-agent with Claude 4 Sonnet scored best. A "home advantage" is possible but untested.
- [I] Only the known historical vulnerability is tested (3.5 tests per task), so other new holes go unseen; SecPass is an upper bound on "secure" [@zhao2025vibe, p. 5].

### Gaps and future work this paper leaves open
- [A] The authors call for more languages, property-based and adversarial tests, static analysis and security-aware training [@zhao2025vibe, p. 24].
- [I] It measures security, not maintainability, and patches, not whole applications. This is part of G1 (fidelity and maintainability of rebuilt apps are never measured together).
- [I] The possible builder–winner overlap is one of the cases behind G2 (same-family bias between benchmark builder and evaluated model).
- [I] Its coupled security tests are an example for G7 (tests tied to the original's code can unfairly fail valid rebuilds).
- [I] Training-data exposure of public repositories is not addressed, which links to G5.

### Why it matters for your research
This paper is your clearest evidence that "it passes the tests" and "it is good code" are different things [I]. Its task design is worth reusing: hide an existing implementation, describe it in words, let an AI rebuild it, then test it against the original's own tests. That is close to a reconstruction study. Reuse the idea of two separate scores (one for behaviour, one for a quality dimension). Avoid its weak points: run each setting several times, report the size of every subset, and check whether your tests are tied to the original's code.

### Connections to other papers
- [V] Agrees with molison2025llm that correctness and another quality dimension diverge: there, the fine-tuned model had the best static quality but the lowest Pass@1 [@molison2025llm, p. 8].
- [V] Seems to disagree with pan2026functional, where reference-normalised security averages 87.40% [@pan2026functional, p. 6]. [I] The instruments differ (static findings vs targeted security tests), so the numbers cannot be compared.
- [V] Agrees with tran2026vibe that success falls as tasks get more complex [@tran2026vibe, p. 6].
- [V] Like yang2026programbench, where Claude wrote the tests and Claude models lead, it shows the builder–winner overlap behind G2 [@yang2026programbench, p. 3; @yang2026programbench, p. 31].
