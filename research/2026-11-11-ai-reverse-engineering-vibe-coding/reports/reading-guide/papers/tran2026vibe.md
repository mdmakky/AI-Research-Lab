## Vibe Code Bench: Evaluating AI Models on End-to-End Web Application Development

> **Takeaway:** When 16 AI models each build a full, deployed web app from a plain-text description, the best passes 61.77% of user-style browser workflows. The choice of AI "judge" model changes the measured result a lot, and code quality is not measured at all.

| Item | Detail |
|---|---|
| Authors | Hung Tran, Langston Nashold, Rayan Krishnan, Antoine Bigeard, Alex Gu |
| Year · Venue | 2026 · Proceedings of the ACM Conference on AI and Agentic Systems |
| Status | Peer-reviewed. We read the arXiv v3 version (May 2026); the ACM version was not compared |
| Identifier | DOI 10.1145/3786335.3813180 · arXiv 2603.04601 |
| Paper type | Benchmark plus comparative evaluation of 16 models, with a judge-reliability and variance study |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5; RQ3 as negative evidence (quality not measured) |

### In plain words
The authors test the "zero-to-one" job: going from a short, non-technical description of an app to a working, deployed web application, with no human help [@tran2026vibe, p. 3]. Instead of reading the code, they judge the app the way a user would: an AI agent opens it in a browser and follows pre-written user workflows step by step [@tran2026vibe, p. 4]. They also ask how far that AI judge can be trusted, by comparing it with human testers [@tran2026vibe, p. 9]. This matters for us because it is the closest benchmark to an autonomous vibe-coding build, and its browser-based scoring could be reused to compare a rebuild with its original.

### How they did it
1. Write tasks: a GPT-5 pipeline drafted 100 app specifications and their test workflows. Two product-manager reviewers accepted, changed or rejected each test, and an AI audit looked for mismatches [@tran2026vibe, p. 3].
2. Split: 50 apps for validation and 50 for the test set used in the main results [@tran2026vibe, p. 4].
3. Build: each model worked inside a modified OpenHands container. This "harness" is the fixed environment around the model: a terminal, a browser and ready-made services for database (Supabase), email (MailHog) and payments (Stripe). Each app had up to 5 hours [@tran2026vibe, p. 4].
4. Fix the technology: the system prompt required React + Vite, Tailwind, Supabase and Docker Compose, so that apps could be tested in the same way [@tran2026vibe, p. 4].
5. Test: a Browser Use agent with Claude Sonnet 4.5 as the judge followed pre-written workflows and marked each small substep pass or fail. A workflow passes when at least 90% of its substeps pass; accuracy is the share of workflows that pass. If the app cannot be deployed, all its workflows fail [@tran2026vibe, p. 5].
6. Keep tests independent: each workflow starts in a fresh browser session with new account data [@tran2026vibe, p. 5].
7. Check variance: 6 specs × 3 models × 5 separate builds, plus 5 re-judgings of the same apps [@tran2026vibe, p. 8].
8. Check the judge: 18 apps (1,401 substeps) were tested by two of three humans who were blind to the model, and by four judge models [@tran2026vibe, p. 8].

### Data and setup
- 100 specifications, 964 workflows and 10,131 substeps; the test split has 50 apps, 473 workflows and 5,136 substeps [@tran2026vibe, p. 4].
- 28 of the 100 apps need payments and/or email [@tran2026vibe, p. 3].
- 16 models from 9 providers; no human developer or commercial tool baseline [@tran2026vibe, p. 5].
- Three models ran without browser vision because of provider settings [@tran2026vibe, p. 5].
- [I] The paper does not state how many builds per app were used in the main table; it appears to be one.
- The harness, all trajectories (step-by-step logs of the agent) and generated apps are released (author claim) [@tran2026vibe, p. 11].

### Key findings
- [V] Top scores on the test split: GPT-5.3-Codex 61.77 ± 4.71%, Claude Opus 4.6 57.57%, GPT-5.2 53.50%; the lowest is Grok 4.1 Fast Reasoning at 1.20%. Open-weight models reach about 5–23% [@tran2026vibe, p. 6].
- [V] Harder apps and external services lower the score: 44.29% for easy vs 6.03% for hard apps, and 34.18% with no integrations vs 13.49% with email plus Stripe (averages over all models) [@tran2026vibe, p. 6]. These subgroups contain only a few apps each.
- [V] Models that used the browser more during building scored higher (r = 0.72 across 16 models), while editing volume did not (r = 0.09) [@tran2026vibe, p. 7]. [A] The authors read this as self-testing being linked to better results [@tran2026vibe, p. 7].
- [V] Failure is often total: 73.2% of apps from the five weakest models score zero vs 12.8% for the five strongest, and only 8.8% of top-five apps score 100% [@tran2026vibe, p. 7].
- [V] Among apps that started, failed workflows were mostly missing features (46.7%) or authorization problems (20.4%) [@tran2026vibe, p. 8].
- [V] Build-to-build variation is the main source of noise: 73.5–92.5% of observed variance comes from generation, not from the judge [@tran2026vibe, p. 8].
- [V] Humans agree with each other on 88.6–93.6% of substeps. The official judge (Claude Sonnet 4.5) agrees with humans on 86.4%, but GPT-5.2 as judge agrees on only 36.1% [@tran2026vibe, p. 9]. [A] "Evaluator selection can materially change reported outcomes" [@tran2026vibe, p. 9].

### Limitations and weaknesses
- [A] Code readability, visual design and security are not measured: "Passing functional tests does not imply maintainable, secure, or well-documented code" [@tran2026vibe, p. 9].
- [A] One harness, one technology stack and web apps only [@tran2026vibe, p. 9].
- [I] The official judge is a Claude model, and several evaluated models are Claude models. Self-preference was not tested; the human check used apps from only three models [@tran2026vibe, p. 8].
- [I] GPT-5 drafted the specs and an OpenAI model ranks first [@tran2026vibe, p. 3]; this possible advantage is not examined.
- [I] Agreement is raw percent, with no chance correction such as kappa [@tran2026vibe, p. 9]. The very low GPT-5.2 agreement is unexplained.
- [I] The browser-use correlation is observational and based on 16 models, and the system prompt itself demands browser testing [@tran2026vibe, p. 16].
- [I] Difficulty tiers are defined from the models' own pass rates, so tier results are partly circular [@tran2026vibe, p. 6].
- [I] The validation split is called "private" in the text but "public" in a table [@tran2026vibe, p. 4]. Funding and conflicts are not reported.

### Gaps and future work this paper leaves open
- [A] The authors suggest extending to CLI, desktop and mobile apps, other harnesses and stacks, and treating judge choice as "a first-class reporting concern" [@tran2026vibe, p. 9].
- [I] G1: code quality and maintainability of the apps remain unmeasured.
- [I] G2: spec-writer, judge and evaluated models overlap in family. The released apps make a re-judging study possible [@tran2026vibe, p. 11].
- [I] G3: the released apps could also test whether maintainability tools agree with each other.
- [I] G4: whether self-testing truly causes better results needs a controlled experiment.
- [I] G6: no human or human-steered baseline [@tran2026vibe, p. 5]. G8: success drops with hidden external services [@tran2026vibe, p. 6].

### Why it matters for your research
[I] This is your best ready-made template for scoring behavioural fidelity: write user workflows in plain language, run them in a browser on the original and on the rebuild, and compare. Its released apps are free data for small first studies on judge bias or code quality. It also warns you to validate any AI judge yourself, report run-to-run variation, and not treat a high pass rate as proof of good code. Note that "vibe coding" here means an autonomous agent, not a human prompting a tool.

### Connections to other papers
- [V] Builds on lu2025webgen, which used single-action test cases with half credit and reported 86–94% judge–human agreement [@lu2025webgen, p. 9]. [I] Vibe Code Bench adds multi-step workflows and shows that agreement depends strongly on the judge model.
- [V] Its top score sits in the same 49–62% band as E2EDev and ProgramDistill [@liu2026benchmarking, p. 6; @kim2026programdistill, p. 11]. [I] The oracles differ, so the numbers must not be ranked against each other.
- [V] Contrasts with pan2026functional, where self-repair and planning lowered code quality without raising correctness on GPT-5.2 [@pan2026functional, p. 8]. [I] Different designs; this conflict is unresolved (gap G4).
- [V] Unlike E2EDev, which uses deterministic browser tests and no AI judge [@liu2026benchmarking, p. 5], scoring here relies on an AI judge.
- [V] Practitioner vibe coding is described elsewhere as human prompting with minimal review [@fawzy2026vibe, p. 1]. [I] Results from autonomous agents should not be pooled with human-steered studies.
