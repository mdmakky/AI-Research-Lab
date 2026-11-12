# Methodology comparison: AI-assisted reverse engineering and vibe coding (functional fidelity, code quality, maintainability)

Project: 2026-11-11-ai-reverse-engineering-vibe-coding · Date: 2026-11-12 · Basis: 23 complete, full-text, critically reviewed analyses (`papers/*/analysis.md`) and `evidence-matrix.md`.

Labels: **[V]** verified in the paper, **[A]** author claim, **[I]** our interpretation. Seven papers are preprints (not peer-reviewed): bai2026recreationworld, chen2025iwr, kim2026programdistill, mota2026comparing, pan2026functional, yang2026programbench, zhao2025vibe. They are marked † below and carry less weight.

Terms used:
- An *oracle* is the reference that decides whether an output is correct, such as a test suite or a human judge.
- *Functional fidelity* means how closely a rebuilt app behaves like the original.
- An *LLM judge* is a language model used to score outputs in place of humans.

## 1. Overview table

All cells are [V] from the analyses unless marked otherwise. "n.r." = not reported.

| Paper | Design | Data / sample (N) | Setup | Metrics | Baselines | Statistical testing | Reproducibility |
|---|---|---|---|---|---|---|---|
| asdaque2026novice [@asdaque2026novice, p. 2] | MSR repository mining (5-page paper) | 22,953 agentic PRs from 1,719 users, AIDev, repos >100 stars | Low- vs high-experience split by commits / account age | Commits and files per PR, acceptance, time to merge, review comments | High-experience users; no non-AI PRs | Mann-Whitney, Chi-square, Benjamini-Hochberg; no effect sizes or CIs; test unit unclear [@asdaque2026novice, p. 4] | Public dataset + replication package [@asdaque2026novice, p. 5] |
| bai2026recreationworld† [@bai2026recreationworld, p. 7] | Benchmark + SFT transfer | 250 apps (50 per platform: Ubuntu, macOS, Windows, Android, Web) x 10 models; rollouts n.r. (probably 1) | Isolated VMs; Codex or Claude Code scaffolds (model and scaffold confounded) [@bai2026recreationworld, p. 28] | Programmatic accessibility/DOM tests + VLM assertions; LOC, files, largest-file share | Model vs model | No CIs or tests on main scores; bootstrap CIs on secondary analyses [@bai2026recreationworld, p. 12] | Release claimed [A] [@bai2026recreationworld, p. 27]; proprietary models; COI not declared [I] |
| borg2026echoes [@borg2026echoes, p. 24] | Preregistered 2-phase experiment; Phase 2 RCT | 151 professionals; Phase 1 n=76, Phase 2 n=75 (128 planned); 2 KLoC Java app | Second developer evolves AI-assisted or non-AI code without AI | Completion time, CodeScene CodeHealth (customised), JaCoCo coverage, perceived productivity | Non-AI code (control) | Wilcoxon/Welch, Cliff's δ / Cohen's d, bootstrap, Bayesian; no multiple-testing correction [@borg2026echoes, p. 19] | Zenodo + GitHub [@borg2026echoes, p. 74]; COI declared [@borg2026echoes, p. 75] |
| chen2025iwr† [@chen2025iwr, p. 6] | Benchmark | 113 video tasks from 100 websites x 28 LVLMs; runs n.r. | Video (≤64 frames) + assets → one HTML file; agent judge (Gemini-2.5-Pro) | IFS (action replay + assertions), VFS (OCR+DINO+MLLM), Final = 0.7 IFS + 0.3 VFS | Model vs model | None; weights tuned in-sample on 60 human-rated cases (ρ 0.57/0.65) [@chen2025iwr, p. 17] | Release promised [A] [@chen2025iwr, p. 1] |
| ehsani2026faster [@ehsani2026faster, p. 1] | Multivocal literature review | 31 peer-reviewed + 73 grey sources (to Jan 2026) | Dual extraction; κ 0.93 formal [@ehsani2026faster, p. 13] | Mention counts per debt type, tool, metric | Grey vs formal | None (descriptive) | figshare supplement [@ehsani2026faster, p. 4] |
| fawzy2026vibe [@fawzy2026vibe, p. 5] | Grey-literature review, thematic analysis | 101 sources, 518 coded units | Mainly single coder; subset cross-check [@fawzy2026vibe, p. 4] | Theme frequencies (quotes, not people) | None | None; no agreement statistic | Zenodo package [@fawzy2026vibe, p. 10] |
| he2026speed [@he2026speed, p. 4] | Staggered DiD + dynamic-panel GMM | 806 Cursor-adopting repos + 1,172–1,380 matched controls; 21,699 repo-months | Monthly panel Jan 2024–Aug 2025 | Commits, lines added; SonarQube warnings, cognitive complexity, duplication | Matched non-adopters (may use other AI) | ATT + SEs, pre-trend tests, Sargan/AR; estimator-sensitive [@he2026speed, p. 16] | Zenodo [@he2026speed, p. 11]; SonarQube version n.r. |
| kim2026programdistill† [@kim2026programdistill, p. 8] | Benchmark (LLM-built) | 300 partial tasks x 9 models; full rebuild 12 apps x 3 models = 36 runs | Browser CLI to a live reference; text observations only | Trace-replay binary and chain scores; atomic and cumulative recovery | Model vs model; no human baseline | None (means only) | Not yet released [A] [@kim2026programdistill, p. 1] |
| liu2026benchmarking [@liu2026benchmarking, p. 3] | Benchmark from existing apps | 46 web apps, 244 requirements, 703 BDD tests; 6 frameworks x 6 LLMs x 3 runs | Requirements + `data-testid` anchors in prompt [@liu2026benchmarking, p. 16] | Req.Acc, Test.Acc, cost, time | Vanilla LLM | Mean ± SD; no tests [@liu2026benchmarking, p. 6] | Code + data released [A] [@liu2026benchmarking, p. 9] |
| lu2025webgen [@lu2025webgen, p. 5] | Benchmark + SFT | 101 instructions, 647 test cases x 16 settings; single run | Bolt.diy / OpenHands / Aider | UI-agent accuracy (half credit for PARTIAL), appearance 1–5 | Frameworks and models; no human baseline | None ("No" to error bars) [@lu2025webgen, p. 40] | Code, data, weights [A] [@lu2025webgen, p. 1] |
| mock2026vibe [@mock2026vibe, p. 16] | Static-group comparison + exploratory agent runs | 9 solo + 7 collaborative professionals; 3 fully-automated + 12 agentic runs; 2 small Python tasks | GPT-3.5 for humans vs GPT-5/Claude Sonnet 4 for agentic [@mock2026vibe, p. 17] | Baseline-test pass rate, McCabe, coverage, time | Solo human coding | KW, one-tailed MWU, Cliff's δ, Holm [@mock2026vibe, p. 10] | GitHub package [@mock2026vibe, p. 43] |
| molison2025llm [@molison2025llm, p. 4] | Comparative static analysis | APPS; GPT-4o zero/few/fine-tuned vs humans; N per group n.r.; Pass@1 on 15 per approach | SonarQube default profile [@molison2025llm, p. 5] | Bugs, smells, severity, fix effort, Pass@1 | APPS human solutions | ORs, MWU + Cliff's δ; no CIs or correction [@molison2025llm, p. 8] | Zenodo [@molison2025llm, p. 11] |
| mota2026comparing† [@mota2026comparing, p. 2] | Exploratory static analysis | 9 apps (Lovable, v0, Replit x 3), one prompt | Free tiers, May 2026 | SonarQube issues, severity, effort, duplication, per KLOC | Tools vs each other; no human or functional check | None (descriptive) [@mota2026comparing, p. 6] | Code + reports shared [@mota2026comparing, p. 6] |
| pan2026functional† [@pan2026functional, p. 2] | Benchmark | 38 Python repos x 16 LLMs x 3 runs; ~11 functional tests per task [@pan2026functional, p. 5] | Zero-shot single-pass repository generation | Functional pass rate; reference-normalised MI, security, robustness, efficiency, resource | Model vs model; reference as normalisation anchor | None; reruns + rank robustness [@pan2026functional, p. 10] | GitHub [A] [@pan2026functional, p. 11] |
| si2025benchmarking [@si2025benchmarking, p. 3] | Benchmark | 484 webpages (+80 HARD); human eval on 100 pages x 5 annotators | Screenshot → single HTML; greedy decoding | Block-Match, Text, Position, Color, CLIP; human win/tie/lose | MLLMs and prompts | Logistic regression validation (79.9%); no model tests [@si2025benchmarking, p. 7] | Release claimed, no URL [@si2025benchmarking, p. 10] |
| tran2026vibe [@tran2026vibe, p. 3] | Benchmark | 50 test apps (964 workflows total) x 16 models; 1 generation each [I] | OpenHands-based harness, React/Vite + Supabase | Workflow pass (≥90% substeps) by LLM browser agent; cost; latency | Model vs model | Mean ± SE across apps; variance panel; human alignment [@tran2026vibe, p. 8] | Harness + trajectories released [A] [@tran2026vibe, p. 11] |
| wu2026looks [@wu2026looks, p. 3] | Benchmark | 29 apps, 309 screens, 701 nav specs x 6 models = 174 single runs | Screenshots + page-relationship description → React/TS | Build, NavPass, Borda VLM visual, LoC/reuse/dead-component proxies | Model vs model | Wilson CIs for failure sample only [@wu2026looks, p. 8] | Repo + one-command replay [A] [@wu2026looks, p. 10] |
| xiao2025benchmarking [@xiao2025benchmarking, p. 3] | Benchmark + user study | 127 pages / 374 interactions x 6 MLLMs x 3 prompts; user study 4 people | Before/after interaction screenshots → one HTML file | CLIP, SSIM, text, Implement Rate; human Usability Rate | Direct prompting | None; human–metric "consistency" claimed only [A] [@xiao2025benchmarking, p. 6] | GitHub [A] [@xiao2025benchmarking, p. 1] |
| xiong2026propgen [@xiong2026propgen, p. 7] | Tool + evaluation | 12 Android apps; 985 properties; single run | GPT-5.2 runtime exploration + property synthesis | Functionality / property validity, refinement, new bugs | DroidAgent, naive LLM, 4 bug detectors | Cohen's κ 0.81–0.91 only | Zenodo [A] [@xiong2026propgen, p. 13] |
| yang2026programbench† [@yang2026programbench, p. 4] | Benchmark | 200 programs x 9 models = 1,800 runs; 248,853 tests | Execute-only binary + docs, no internet, mini-SWE-agent [@yang2026programbench, p. 5] | % resolved, % almost, % tests passed, structure stats | Model vs model; native test suites for coverage | None; Fleiss' κ for cheating judges [@yang2026programbench, p. 17] | Open-sourced [A] [@yang2026programbench, p. 2] |
| zhao2025vibe† [@zhao2025vibe, p. 6] | Benchmark | 186 tasks from 100 Python repos x 12 agent settings; single pass@1 | Agents re-implement a masked feature | FuncPass, SecPass, CWE P/R/F1 | Settings vs each other | None [@zhao2025vibe, p. 8] | GitHub [A] [@zhao2025vibe, p. 1] |
| zhou2025declarui [@zhou2025declarui, p. 6] | Technique + comparison + user study | 50 apps (250 pages); ablation 13 apps; 5 developers x 12 apps | CV + MLLM page-transition graph + compile/navigation refinement; human graph correction [@zhou2025declarui, p. 4] | CLIP, SSIM, PCR, CSR, ACIC, AMCT; Likert readability and maintainability | Raw GPT-4o / Claude-3.5 | MWU on non-independent ratings only [@zhou2025declarui, p. 10] | No code or data link (n.r.) |
| zhu2026understanding [@zhu2026understanding, p. 4] | Exploratory static analysis (2 experiments) | Exp I: 90 problems x 5 LLMs x 2 prompts + 90 human; Exp II: ~20 MetaGPT apps [I] | PyExamine smell detection | Code / structural / architectural smell counts, LoC | Human solutions (Exp I) | Exp I none; Exp II Spearman / KW without correction [@zhu2026understanding, p. 9] | Zenodo [@zhu2026understanding, p. 10] |

## 2. Approach families

**F1. Visual UI-to-code (screenshot or design → code):** si2025benchmarking, xiao2025benchmarking, zhou2025declarui, wu2026looks.
- Strengths [I]: real webpages and apps as references [@si2025benchmarking, p. 2; @wu2026looks, p. 3]. Each paper also adds some reliability check:
  - visual metrics partly validated against humans [@si2025benchmarking, p. 7];
  - a human-calibrated VLM judge with an anchor [@wu2026looks, p. 13];
  - navigation measured with app exploration [@zhou2025declarui, p. 7].
- Weaknesses [I]:
  - Fidelity is mostly visual. si2025benchmarking strips JavaScript [@si2025benchmarking, p. 13].
  - Interaction coverage is shallow: navigation edges only [@wu2026looks, p. 5], or element presence as "Implement Rate" [@xiao2025benchmarking, p. 4].
  - Structural priors are given as input: a page-relationship description [@wu2026looks, p. 3] or a human-corrected page-transition graph [@zhou2025declarui, p. 4].
  - Code quality is unmeasured or measured by proxies or Likert ratings.

**F2. Behaviour-observed reconstruction (video, live reference or executable → app):** chen2025iwr†, bai2026recreationworld†, kim2026programdistill†, yang2026programbench†.
- This family is the closest match to "AI-assisted reverse engineering" [I].
- Strengths [I]: implementation-agnostic behavioural oracles [@bai2026recreationworld, p. 4; @yang2026programbench, p. 5; @kim2026programdistill, p. 4]. The papers also use:
  - leakage and isolation controls [@yang2026programbench, p. 18; @kim2026programdistill, p. 10; @bai2026recreationworld, p. 9];
  - oracle-quality audits: coverage [@yang2026programbench, p. 7] and interaction-outcome share [@bai2026recreationworld, p. 9].
- Weaknesses [I]:
  - All four are preprints, and all use single runs.
  - Same-family builders appear in yang2026programbench and kim2026programdistill (see Contradiction C10 in the evidence matrix).
  - Code quality is measured only through size and structure proxies [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9] or not at all [@kim2026programdistill, p. 6].
  - Oracles are coupled to the original's selectors in kim2026programdistill [@kim2026programdistill, p. 35].

**F3. Specification-to-app benchmarks with executable oracles:** liu2026benchmarking, lu2025webgen, tran2026vibe, pan2026functional†, zhao2025vibe†.
- Strengths [I]: requirement-level executable tests. Several papers check their oracles:
  - expert test audits [@liu2026benchmarking, p. 14];
  - judge–human alignment [@tran2026vibe, p. 9; @lu2025webgen, p. 9];
  - reference-validated tests [@pan2026functional, p. 2];
  - upstream human tests with no LLM judge [@zhao2025vibe, p. 5].
- Two papers start from existing apps, which brings them close to reconstruction: liu2026benchmarking and pan2026functional [I].
- Weaknesses [I]:
  - The input is a written specification, not observed behaviour.
  - LLM judges and LLM-drafted tests are used (tran2026vibe, lu2025webgen).
  - Oracles are thin: about 11 tests per task [@pan2026functional, p. 5].
  - Only pan2026functional measures maintainability, through one MI proxy [@pan2026functional, p. 3].

**F4. Code-quality studies of LLM or vibe-coded code (static analysis):** molison2025llm, mota2026comparing†, zhu2026understanding, he2026speed (plus the non-functional arm of pan2026functional).
- Strengths [I]: established tools (SonarQube, PyExamine), and one quasi-causal design at scale [@he2026speed, p. 7].
- Weaknesses [I]:
  - The instruments disagree with each other (C3).
  - Counts are often not normalised by size [@zhu2026understanding, p. 8].
  - Functional correctness is not checked [@mota2026comparing, p. 2], or checked only on 15 samples [@molison2025llm, p. 8].
  - Human baselines are weak (competitive-programming submissions) [@molison2025llm, p. 9].
  - Tasks are algorithmic snippets, not applications (molison2025llm, zhu2026understanding Exp I).

**F5. Human-centred and workflow studies:** borg2026echoes (RCT), mock2026vibe (experiment), asdaque2026novice (mining), fawzy2026vibe (grey review), ehsani2026faster (multivocal review).
- Strengths [I]:
  - The only randomised maintainability evidence, a hand-off evolution design [@borg2026echoes, p. 13].
  - Real developers [@mock2026vibe, p. 16].
  - Practitioner definitions of vibe coding [@fawzy2026vibe, p. 1].
  - A technical-debt taxonomy [@ehsani2026faster, p. 16].
- Weaknesses [I]:
  - Small or underpowered samples [@borg2026echoes, p. 19; @mock2026vibe, p. 13].
  - Model-generation confound [@mock2026vibe, p. 17].
  - Perception or proxy outcomes [@fawzy2026vibe, p. 8; @asdaque2026novice, p. 2].
  - Reviews rely heavily on grey sources [@ehsani2026faster, p. 16].
  - None studies reconstruction.

**F6. Behavioural-specification recovery from running apps:** xiong2026propgen.
- Strengths [I]: runtime-grounded property inference with independent annotators (κ 0.81–0.91) [@xiong2026propgen, p. 7]. It is a candidate oracle generator for fidelity testing.
- Weaknesses [I]: 12 apps, single run, author-tool overlap in the baselines, and it generates no code.

## 3. Comparable results

**Rule:** numbers are compared only between papers that share the dataset, the metric and the setup. **No pair of papers in this corpus meets all three.** So all cross-paper statements below are directional, not quantitative.

| Pair (closest candidates) | What they share | Why the numbers are not comparable |
|---|---|---|
| si2025benchmarking vs xiao2025benchmarking | C4 validation-set pages, CLIP [@si2025benchmarking, p. 2; @xiao2025benchmarking, p. 2] | Static pages vs interaction regions; different subsets and models; different extra metrics |
| zhou2025declarui vs wu2026looks | Multi-screen mobile apps rebuilt from screenshots | PCR (graph edges, scored manually) vs NavPass (Playwright tests); native frameworks vs a React web proxy; different structural inputs |
| bai2026recreationworld vs chen2025iwr | A functional channel plus a visual channel | Accessibility tests + VLM assertions vs action replay + OCR/DINO/MLLM; VFS only over reached checkpoints [@chen2025iwr, p. 7] |
| lu2025webgen vs tran2026vibe | NL spec → web app; LLM browser judge | Atomic test cases with half credit vs workflows passing at ≥90% of substeps; different model generations |
| liu2026benchmarking vs pan2026functional | Rebuild of existing open-source apps against reference-validated tests | Web BDD via Selenium with `data-testid` anchors vs Python pytest on public APIs; different models |
| molison2025llm vs zhu2026understanding (Exp I) | Competitive-programming problems vs human solutions | APPS + SonarQube vs CodeContests + PyExamine; different models |
| he2026speed vs mota2026comparing | SonarQube issue measures | Change in repository-month totals vs per-KLOC issues in 9 generated apps |
| pan2026functional vs zhao2025vibe | Python repositories, test-based correctness, a "security" score | Whole-repo generation + static findings vs feature patch + targeted security tests (C7) |

Headline functional-fidelity figures, listed for orientation only. They are **not comparable** because each has a different oracle, input and app type [I]:

| Paper | Input → output | Oracle | Best reported |
|---|---|---|---|
| yang2026programbench† | Executable + docs → CLI program | ~770 behavioural tests per task (median) | 0% resolved; ≥95% of tests on 3% of tasks [@yang2026programbench, p. 6] |
| bai2026recreationworld† | Running app → app (5 platforms) | Accessibility/DOM tests + VLM | 58.06% average; 2.8% full programmatic pass [@bai2026recreationworld, p. 11] |
| kim2026programdistill† | Live web app → web app | Browser-trace replay | 49.15% cumulative workflows (3 models, 12 apps) [@kim2026programdistill, p. 11] |
| chen2025iwr† | Interaction video → single HTML | Agent replay + MLLM assertions | Final 36.35, IFS 24.39 [@chen2025iwr, p. 8] |
| liu2026benchmarking | Requirements from existing apps → web app | BDD/Selenium tests | 53.75% Req.Acc [@liu2026benchmarking, p. 6] |
| tran2026vibe | NL spec → full-stack web app | LLM browser workflows | 61.77% workflows [@tran2026vibe, p. 6] |
| lu2025webgen | NL instruction → website | UI-agent test cases | 27.8% accuracy [@lu2025webgen, p. 8] |
| pan2026functional† | Requirements → Python repo | pytest suites | <45% pass rate [@pan2026functional, p. 5] |
| zhao2025vibe† | Feature description → patch | Upstream functional tests | 57.0% FuncPass [@zhao2025vibe, p. 7] |
| wu2026looks | Screenshots + navigation map → React app | Playwright navigation | 92% NavPass [@wu2026looks, p. 7] |
| zhou2025declarui | Screenshots/designs → mobile UI | Manual graph-edge coverage | 96.8% PCR [@zhou2025declarui, p. 9] |

Within-paper model rankings are comparable, but single runs make near-ties uninterpretable:
- [V] tran2026vibe shows that generation variance dominates evaluator variance (73.5–92.5%) [@tran2026vibe, p. 8].
- [I] Rank gaps of a few points in yang2026programbench, wu2026looks, lu2025webgen and zhao2025vibe cannot be separated from noise.

## 4. Contradictions

The full entries with both sides, differences and [I] explanations are in `evidence-matrix.md` → "Contradictions". Summary:

1. **C1 Maintainability harm.** Project-level warnings and complexity rise after Cursor adoption [@he2026speed, p. 7], but a second developer's effort and CodeHealth show no significant difference [@borg2026echoes, p. 33; @borg2026echoes, p. 38]. Tools, units, scale and time differ, and the he2026speed effect depends on the estimator [@he2026speed, p. 16].
2. **C2 Static issues.** LLM code has fewer SonarQube bugs than APPS humans [@molison2025llm, p. 8], vs +30% repository warnings [@he2026speed, p. 7]. The units and baselines differ, so the results are not comparable.
3. **C3 Instrument choice.** PyExamine is chosen over SonarQube's "superficial linting" [@zhu2026understanding, p. 2]. Technical-debt tools disagree [@ehsani2026faster, p. 5].
4. **C4 Iterative feedback.**
   - It hurts non-functional quality without functional gain [@pan2026functional, p. 8].
   - It correlates with or enables better outcomes elsewhere [@tran2026vibe, p. 7; @zhou2025declarui, p. 10; @wu2026looks, p. 12].
   - The studies differ in feedback type, outcome and design (intervention vs correlation).
5. **C5 Looks vs behaves.** chen2025iwr and bai2026recreationworld are only directionally consistent. VFS > IFS is partly built into chen2025iwr's metrics [@chen2025iwr, p. 7]. In bai2026recreationworld the visual channel is below the programmatic one for 9 of 10 models [@bai2026recreationworld, p. 11].
6. **C6 MetaGPT.** It nearly always fails in liu2026benchmarking [@liu2026benchmarking, p. 6] but leads on tiny tasks with newer models in mock2026vibe [@mock2026vibe, p. 41].
7. **C7 Security.** 87.40% static security [@pan2026functional, p. 6] vs 79.3% of correct solutions failing targeted tests [@zhao2025vibe, p. 6].
8. **C8 Code volume.** Rebuilds are smaller than the originals [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9], while assisted development adds code [@he2026speed, p. 8; @borg2026echoes, p. 30].
9. **C9 Construct differences.** "Vibe coding" is defined differently in [@fawzy2026vibe, p. 1; @asdaque2026novice, p. 1; @mock2026vibe, p. 15; @he2026speed, p. 4; @ehsani2026faster, p. 17], so these results must not be pooled. The fidelity scores of kim2026programdistill, liu2026benchmarking, lu2025webgen, bai2026recreationworld and chen2025iwr use different oracles and are not comparable.
10. **C10 Same-family construction or judging.** The same model family builds or judges the benchmark and then wins in yang2026programbench, tran2026vibe, kim2026programdistill and zhao2025vibe. There is overlap without a visible advantage in liu2026benchmarking, lu2025webgen, bai2026recreationworld, chen2025iwr and wu2026looks. This is untested everywhere [I].

## 5. Methodological weaknesses across the field

Counts are our tally over the analyses [I]. Each pattern is verified in the cited papers.

1. **Single runs, no variance, no significance tests.**
   - Main results come from one run or generation per cell, or the number of runs is not reported. Examples: [@bai2026recreationworld, p. 11; @chen2025iwr, p. 8; @kim2026programdistill, p. 12; @lu2025webgen, p. 40; @wu2026looks, p. 9; @yang2026programbench, p. 10; @zhao2025vibe, p. 6; @xiong2026propgen, p. 8].
   - Studies that repeat runs: liu2026benchmarking (3 runs) [@liu2026benchmarking, p. 5], pan2026functional (3 runs + 5 reruns) [@pan2026functional, p. 5], and tran2026vibe's 6-app variance panel [@tran2026vibe, p. 8].
   - No benchmark paper tests model differences for significance. Where measured, run-to-run variance is large: generation SE up to 5 pp [@tran2026vibe, p. 8].
2. **Unvalidated or same-family oracles and judges.**
   - Many papers use LLM-drafted tests, LLM-built tasks or LLM judges, often from the evaluated families (C10).
   - Judge validation uses raw percent agreement without chance correction [@tran2026vibe, p. 9; @lu2025webgen, p. 9], small or author-labelled panels [@wu2026looks, p. 13], or in-sample calibration [@chen2025iwr, p. 17; @si2025benchmarking, p. 17].
   - Some automatic metrics are only declared "consistent" with humans [@xiao2025benchmarking, p. 6].
3. **Contamination handling is uneven.**
   - Reference apps and programs are popular public projects in most benchmarks.
   - Explicit controls appear in only a few: an overlap audit [@bai2026recreationworld, p. 18], no internet plus a language ablation [@yang2026programbench, p. 6], BLEU against the original [@xiao2025benchmarking, p. 5], post-cutoff builds [@xiong2026propgen, p. 11], and keeping task code out of public repositories [@borg2026echoes, p. 66].
   - pan2026functional acknowledges exposure [@pan2026functional, p. 2], and its example prompt names the original project [@pan2026functional, p. 3].
   - No contamination discussion was found for chen2025iwr, kim2026programdistill, liu2026benchmarking, si2025benchmarking, wu2026looks, zhao2025vibe, molison2025llm or zhu2026understanding (per their analyses) [I].
4. **Code quality and maintainability are absent or measured by unvalidated proxies.**
   - The proxies used are size and structure [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9], LoC/reuse/dead-component counts [@wu2026looks, p. 4], a single MI index [@pan2026functional, p. 3], Likert ratings [@zhou2025declarui, p. 7], and raw smell counts not normalised by size [@zhu2026understanding, p. 8].
   - No reconstruction benchmark combines a behavioural oracle with a validated maintainability measure or a hand-off maintenance task like the one in borg2026echoes [@borg2026echoes, p. 13] [I].
5. **Oracle coupling and incompleteness make fidelity scores incomparable.**
   - Tests are tied to the original's identifiers: `data-testid` anchors [@liu2026benchmarking, p. 16] and selectors [@kim2026programdistill, p. 35].
   - Structural priors are given as input [@wu2026looks, p. 3; @zhou2025declarui, p. 4].
   - Suites are thin: about 11 tests per task [@pan2026functional, p. 5].
   - Finite suites can only give a lower bound [@yang2026programbench, p. 12; @bai2026recreationworld, p. 22].
   - Metrics are partly circular: navigation is scored against the method's own input graph [@zhou2025declarui, p. 7], and VFS uses a different denominator [@chen2025iwr, p. 7].
6. **Further recurring problems:**
   - No human-developer baseline in any reconstruction or generation benchmark [@yang2026programbench, p. 20; @tran2026vibe, p. 5; @lu2025webgen, p. 7].
   - Small human samples [@mock2026vibe, p. 16; @zhou2025declarui, p. 10; @xiao2025benchmarking, p. 11].
   - Underpowered RCT [@borg2026echoes, p. 19].
   - Internal numeric inconsistencies, flagged in the analyses of borg2026echoes, he2026speed, liu2026benchmarking, molison2025llm, wu2026looks, xiao2025benchmarking, yang2026programbench and zhou2025declarui (see each paper's §9) [I].
   - Construct heterogeneity of "vibe coding" (C9).
   - Almost exclusively web, Python or CLI targets. Only bai2026recreationworld covers native desktop and Android [@bai2026recreationworld, p. 7]; mobile work uses a web proxy [@wu2026looks, p. 9] or UI-only code [@zhou2025declarui, p. 2].

## 6. What this means for our RQs

**RQ1 (approaches and their relation to vibe coding).**
- Six approach families exist (§2). Inputs range from screenshots, designs, interaction videos and before/after interaction screenshots to live running references, executables plus docs, and natural-language specs [@si2025benchmarking, p. 4; @chen2025iwr, p. 5; @bai2026recreationworld, p. 3; @kim2026programdistill, p. 3; @yang2026programbench, p. 2; @tran2026vibe, p. 3] [V].
- Almost all evaluations run autonomous agents or single prompts. Practitioner vibe coding is human-steered natural-language prompting with little review [@fawzy2026vibe, p. 1], and that is studied only in small human experiments [@mock2026vibe, p. 15] or as a field proxy [@he2026speed, p. 4] [I].
- Evidence strength: **moderate**. The descriptive picture is consistent, but 7 of 23 papers are preprints and the field moves monthly.

**RQ2 (measuring functional fidelity and how well it is achieved).**
- Fidelity is measured by four oracle types [I]:
  - behavioural test replay (bai2026recreationworld, kim2026programdistill, yang2026programbench, liu2026benchmarking, pan2026functional, zhao2025vibe);
  - LLM or agent judges running natural-language tests (lu2025webgen, tran2026vibe, chen2025iwr);
  - visual similarity (si2025benchmarking, xiao2025benchmarking, wu2026looks, zhou2025declarui);
  - navigation graphs (wu2026looks, zhou2025declarui).
- Achieved fidelity is partial everywhere:
  - full equivalence is rare [@bai2026recreationworld, p. 11; @yang2026programbench, p. 6];
  - the best workflow-level or requirement-level pass rates are about 49–62% [@kim2026programdistill, p. 11; @liu2026benchmarking, p. 6; @tran2026vibe, p. 6];
  - interaction logic lags static structure (G-A2).
- Evidence strength: **moderate** for "fidelity is far from complete and interaction is the bottleneck". **Weak** for any specific number or cross-benchmark ranking (C9, §3).

**RQ3 (code quality and maintainability vs human code).**
- The evidence is mixed and does not support a single answer.
  - Project-level warnings and complexity rise, but the result is estimator-sensitive and size-driven [@he2026speed, p. 7; @he2026speed, p. 16].
  - No short-term downstream maintainability harm was found in an RCT [@borg2026echoes, p. 38].
  - LLM code has fewer SonarQube bugs than a weak human baseline, with mixed smells [@molison2025llm, p. 8].
  - LLM code shows different smell types [@zhu2026understanding, p. 7].
  - Quality is platform-dependent [@mota2026comparing, p. 5].
  - Rebuilds are smaller and more monolithic than the originals [@bai2026recreationworld, p. 15; @yang2026programbench, p. 9].
  - Practitioners perceive the code as "fast but flawed" [@fawzy2026vibe, p. 8].
- No study measures validated maintainability of *reconstructed* applications against their originals [I].
- Evidence strength: **weak to moderate** (conflicting results, C1–C3).

**RQ4 (methodological strengths and weaknesses).**
- Strengths: implementation-agnostic behavioural oracles with leakage controls (F2), oracle audits (coverage, expert κ), judge–human alignment checks, and one preregistered RCT.
- Weaknesses: the six patterns in §5.
- Evidence strength: **strong** for missing variance and significance testing and for absent maintainability measurement (verified across 12+ papers). **Moderate** for judge, contamination and oracle-coupling problems.

**RQ5 (gaps and study design).**
- The convergent weak point is the missing joint evaluation of behavioural fidelity *and* validated maintainability for UI- or behaviour-based reconstruction [I]. The partial exceptions are pan2026functional (Python APIs, MI only), wu2026looks (proxies) and zhou2025declarui (Likert).
- Candidate gaps for the gap analyst are listed below. **None is claimed as a gap yet: each needs the novelty check in docs/research-standards.md §7.**
  1. Joint fidelity + maintainability evaluation of AI-reconstructed apps against their originals, using static quality with size normalisation and more than one tool, plus a hand-off maintenance task as in borg2026echoes.
  2. Human-steered vibe-coding reconstruction compared with autonomous agents. All benchmarks are autonomous; future-work statements: [@yang2026programbench, p. 12; @kim2026programdistill, p. 14].
  3. Contamination-controlled reconstruction targets, such as post-cutoff, obfuscated or private reference apps (uneven handling, §5.3).
  4. Judge and oracle independence: cross-family judges, chance-corrected agreement, and tests of builder- or judge-family self-preference (C10).
  5. Whether iterative feedback or self-testing improves fidelity *and* code quality together (C4).
  6. Validity of maintainability instruments for AI-generated code: SonarQube vs PyExamine vs CodeHealth vs MI (C3).
  7. Black-box oracles that are not coupled to the original's identifiers (§5.5).
  8. Native mobile and back-end-inclusive reconstruction.
- A design sketch [I]:
  - reference apps of known provenance (post-cutoff or private);
  - several vibe-coding tools and agents, plus a human-steered arm;
  - ≥3 runs per cell;
  - a behavioural oracle (trace replay or BDD, black-box selectors) plus a validated visual judge;
  - size-normalised static quality from two tools plus a second-developer change task;
  - cross-family judges with κ reporting and preregistered tests.
- Evidence strength: **weak** (pending novelty check).
