# Research gap report — Evaluating AI-Assisted Reverse Engineering for Software Application Reconstruction through Vibe Coding: Functional Fidelity, Code Quality, and Maintainability

A gap is only listed when it is backed by evidence from the analysed papers AND a novelty check found no paper already filling it.

- Date: 2026-11-12. Basis: 23 complete full-text analyses, `evidence-matrix.md` (204 rows, contradictions C1–C10), `reports/methodology-comparison.md` §5–§6 (8 candidate gaps), `RESEARCH-QUESTIONS.md`.
- Labels: **[V]** verified in the paper, **[A]** author claim, **[I]** our interpretation. Papers in the project are cited in pandoc style with project key and page.
- Papers found during the novelty checks are **not analysed**. They are named in plain text with identifiers copied from `rlab search` output, and statements about them come from their abstracts (or the arXiv HTML page where noted). They are therefore [A] and must not be used as evidence until added and analysed. See "Papers recommended for inclusion".
- Novelty-check procedure (docs/research-standards.md §7): per gap ≥3 `rlab search` queries across ≥2 sources with `--from` 2023–2026, plus one WebSearch for very recent work; closest hits read at abstract level. All queries run on 2026-11-12 are listed in `search/search-log.md` (rows dated 2026-11-12). Semantic Scholar and Google Scholar were not queried, and web results are US-indexed only, so every "we found no study" statement is limited to these sources.
- Related work: the security-fidelity question (are the original's security controls preserved in a rebuild?) was checked separately in `reports/novelty-check-security-fidelity.md`. It is not repeated here. Its verdict ("partially novel, novel core: differential, reference-anchored security evaluation of behaviour-only rebuilds") fits as an extra outcome dimension in the G1 study design.

## Ranking

Score = evidence strength (1–3) × novelty (1–3) × beginner feasibility (1–3). Ties are broken by feasibility. All scores are our judgement [I].

| Rank | Gap (short) | Candidate # in comparison §6 | Evidence | Novelty verdict | Feasibility | Score | Confidence |
|---|---|---|---|---|---|---|---|
| G1 | Joint behavioural fidelity + validated maintainability of reconstructed apps, measured against their originals | 1 | 3 (strong) | novel (narrow claim) | moderate (2) | 18 | medium-high |
| G2 | Same-family builder/judge/test-author bias, untested in app-generation and reconstruction benchmarks | 4 | 2 | partially novel | easy (3) | 12 | medium |
| G3 | Do maintainability instruments agree, and do they predict maintenance effort, for AI-built *applications*? | 6 | 2 | partially novel (narrowed) | easy–moderate (3) | 12 | medium |
| G4 | Does feedback (self-testing, repair, static-analysis loops) improve fidelity *and* code quality together in reconstruction? | 5 | 2 | partially novel | moderate (2) | 8 | medium |
| G5 | Effect of training-data contamination on reconstruction fidelity (public vs post-cutoff/private originals) | 3 | 2 | partially novel | moderate (2) | 8 | medium-low |
| G6 | Human-steered (vibe-coding) reconstruction vs autonomous agents | 2 | 2 | partially novel | moderate–hard (2) | 8 | medium |
| G7 | Size of the bias from identifier-coupled oracles in reconstruction fidelity scores | 7 | 2 | mostly addressed as a method; narrow residual gap | easy (3) | 6 | low-medium |
| G8 | Native-mobile reconstruction including hidden back-end behaviour | 8 | 2 | partially addressed | hard (1) | 2 | low |

[I] G6 ranks low only because human-participant studies are harder for a beginner. It is the gap closest to the project title ("through vibe coding"), and it can be added to the G1 study as an optional arm.

---

## G1: No study jointly measures behavioural fidelity and validated maintainability of AI-reconstructed applications against their originals

- Gap type: methodological / evidence.
- Evidence that the gap exists:
  - [V] Reconstruction benchmarks with behavioural oracles measure code only through size and structure proxies (89.4% smaller rebuilds, fewer files, larger largest-file share) [@bai2026recreationworld, p. 15]. [A] The authors call the framework data "architectural substitution rather than implementation quality" [@bai2026recreationworld, p. 16].
  - [V] Rebuilt programs are shorter, shallower and use fewer files than the human originals, but no quality or maintainability measure is applied [@yang2026programbench, p. 9].
  - [V] Code quality of rebuilds is not measured in kim2026programdistill (authors' future work covers visual fidelity and other platforms) [@kim2026programdistill, p. 14]. chen2025iwr scores behaviour and appearance only, with single-file output [@chen2025iwr, p. 7].
  - [V] The visual-UI family uses unvalidated proxies (LoC, reuse, dead components) [@wu2026looks, p. 4] or Likert ratings by 5 developers [@zhou2025declarui, p. 10]. si2025benchmarking and xiao2025benchmarking measure no code quality [@si2025benchmarking, pp. 3–4; @xiao2025benchmarking, p. 5].
  - [V] The only reference-anchored maintainability score in the corpus is a single Maintainability Index proxy on Python repositories rebuilt from requirements, not from observed behaviour [@pan2026functional, p. 3; @pan2026functional, p. 6].
  - [A] "Passing functional tests does not imply maintainable, secure or documented code" [@tran2026vibe, p. 9]. [A] No standardised benchmark exists for the technical debt or maintainability of LLM code; benchmarks focus on binary correctness [@ehsani2026faster, pp. 23–24].
  - [V] Functional correctness and other quality dimensions diverge whenever both are measured [@molison2025llm, p. 8; @zhao2025vibe, p. 6; @wu2026looks, p. 7] (evidence matrix G-A4). So fidelity alone cannot stand in for quality.
  - [V] The one validated maintainability design in the corpus, a second developer evolving the code, has never been applied to reconstructions [@borg2026echoes, p. 13].
  - Independent support: ≥6 independent papers (evidence matrix G-A6, rated strong as a description of the field).
- Novelty check (2026-11-12):
  - `rlab search` queries:
    1. "maintainability of reconstructed application compared to original functional equivalence LLM" (openalex, arxiv; from 2024)
    2. "application reconstruction benchmark code quality maintainability functional fidelity" (openalex, arxiv; 2025)
    3. "rebuilding software from reference application LLM agent code quality" (crossref, arxiv; 2024)
    4. "app clone generation LLM maintainability static analysis functional tests" (openalex, crossref; 2024)
    5. "recreate existing web application coding agent functional fidelity maintainability" (arxiv; 2025; 0 hits)
    6. "functional fidelity and code quality joint evaluation generated web application benchmark" (openalex, crossref; 2025)
    7. "code quality maintainability of programs rebuilt by coding agents compared with original source" (arxiv, openalex; 2026)
    8. "MirrorCode AI can rebuild entire programs from behavior alone" (arxiv, openalex; 2026; identifier check)
  - WebSearch: "benchmark AI agents rebuild existing app functional fidelity and maintainability code quality of reconstruction 2026".
  - Closest prior work (abstract level, [A]):
    - *MirrorCode: AI can rebuild entire programs from behavior alone* (arXiv 2606.30182, preprint). Agents reimplement 25 CLI programs without source access, scored by exact output match. No code-quality measure in the abstract.
    - *UI2App* (arXiv 2607.06306, preprint). Multi-route web apps from static screenshots, scored on executability, visual fidelity and interaction inference. No code-quality measure in the abstract.
    - *VISTA* (arXiv 2605.26144, preprint). Full-stack Web and Android apps from design handoffs, with component-level behaviour probes. The abstract mentions no static-analysis or maintainability measure and no original implementation.
    - *WebCoderBench* (ACL 2026, DOI 10.18653/v1/2026.acl-long.535). Spec-to-web-app with 24 metrics. From the arXiv HTML: its "maintainability" perspective is comment rate only, plus linting and code redundancy. There are no reference implementations.
    - *Is Agent Code Less Maintainable Than Human Code?* (CodeThread; EMNLP 2026, DOI 10.18653/2026.emnlp-main.2528). Agents resolve fewer follow-up tasks when building on agent code than on human code (up to −13.1%). Issue-level repository tasks, not application reconstruction.
    - *Trajectory-Level Security Debt in LLM Coding Agents* (DOI 10.1609/aaaiss.v10i1.43533). SAST on ProgramBench rebuilds. Security only, with no comparison to the originals (see `reports/novelty-check-security-fidelity.md` §3).
    - *Software Aging in LLM-Generated Applications* (arXiv 2608.26391, preprint). Runtime aging of spec-generated BaxBench back-ends. Not reconstruction.
    - *SWE-CI* (arXiv 2603.03823, preprint). Maintainability as the change in functional correctness over long CI histories. Not reconstruction.
  - Verdict: **novel** for the narrow claim. We found no study that rebuilds existing applications from observable artefacts (UI, screenshots, behaviour) and then measures, on the same rebuilds, (a) behavioural fidelity against the original and (b) maintainability with more than one size-normalised instrument plus a maintenance task, using the original as the baseline (searches on 2026-11-12). Measuring each part separately is not new.
- Confidence: **medium-high**. The evidence is strong and consistent across the corpus. Novelty rests on abstract-level reading of eight close 2026 papers, mostly preprints, and the field publishes monthly. Re-run the check before submission.
- Potential contribution: the first reference-anchored "fidelity × maintainability" profile of AI reconstruction. It would show whether rebuilds that behave like the original are also as easy to change as the original. It would also test whether the size reduction [@bai2026recreationworld, p. 15] means simpler code or missing functionality, which C8 in the evidence matrix leaves open.
- Suggested study / experiment:
  - Design: a within-app factorial benchmark study, apps × tools × repeated runs.
  - Data and sample:
    - 8–10 small web apps (about 1–5 KLoC, React or plain JS, with a back-end of at most simple CRUD).
    - Stratum A (5 apps): public apps from the released E2EDev set, which come with validated BDD tests [@liu2026benchmarking, p. 5; @liu2026benchmarking, p. 9].
    - Stratum B (3–5 apps): apps first published after the evaluated models' training cutoffs, or apps the researcher writes. This also gives a contamination contrast (G5).
  - Builder input: the running original (URL) plus screenshots only. No source code, no `data-testid` hints.
  - Arms: 2–3 builders (e.g. one terminal coding agent and one commercial vibe-coding platform). Record tool versions and dates. Run each builder 3 times per app, which gives about 60–90 rebuilds.
  - Fidelity metrics:
    1. Pass rate of Playwright/BDD tests written against the original with role- and text-based locators. Each test must pass on the original (100%) before use.
    2. A secondary visual score.
  - Maintainability metrics, each also computed on the original, with the rebuild/original ratio as the outcome:
    1. SonarQube issues per KLoC and cognitive complexity per function.
    2. Duplication % (SonarQube) plus a second analyser (ESLint complexity rules or a Maintainability Index tool).
    3. A standard change task: 2 small feature changes, each with its own acceptance tests. The task is done by a fixed "maintainer" agent (3 runs) on the original and on each rebuild; outcomes are success and tokens/time, following the CodeThread idea. An optional pilot with 4–6 student developers follows the hand-off design of borg2026echoes [@borg2026echoes, p. 13].
  - Baseline: the original app on every measure.
  - Analysis:
    - Preregister the hypotheses.
    - Mixed-effects models with app as a random effect.
    - Report mean ± SD over runs with bootstrap CIs.
    - Report the Spearman correlation between fidelity and the maintainability ratio across rebuilds.
    - Normalise all counts by size; this matters because of C8 and [@he2026speed, p. 8].
  - Expected threats to validity:
    - Small app sample (external validity).
    - Tool drift between runs (record versions; run all arms in the same week).
    - Finite test suites give only a lower bound on fidelity [@yang2026programbench, p. 12; @bai2026recreationworld, p. 22].
    - Static instruments are not validated for AI code (G3).
    - The agent-as-maintainer confounds AI capability with code maintainability.
    - Contamination in Stratum A.
- Feasibility for a beginner: **moderate**. All tools are free or have free tiers, and E2EDev provides apps and tests. The main effort is writing locator-independent tests for Stratum B and managing about 60–90 rebuilds. API cost is moderate. This needs supervision on the statistics.

## G2: Same-family bias between benchmark builder, test author and judge is untested in app-generation and reconstruction benchmarks

- Gap type: methodological / contradiction (C10).
- Evidence that the gap exists:
  - [V] Overlap where the same family also wins:
    - Claude wrote the tests and Claude models lead [@yang2026programbench, p. 3; @yang2026programbench, p. 31].
    - GPT-5 drafted the specs and GPT-5.3-Codex ranks first [@tran2026vibe, p. 3; @tran2026vibe, p. 6].
    - GPT-5.6 Sol built the tasks, GPT-6 Astra ranks first and also classifies the failures [@kim2026programdistill, p. 2; @kim2026programdistill, p. 8; @kim2026programdistill, p. 12].
    - Claude 4 Sonnet built the environments and wins [@zhao2025vibe, p. 17; @zhao2025vibe, p. 7].
  - [V] Overlap without a visible advantage in other papers [@lu2025webgen, p. 8; @bai2026recreationworld, p. 11; @wu2026looks, p. 13].
  - [V] Judge–human agreement ranges from 36.1% to 86.4% depending on the judge model, reported as raw agreement with no κ [@tran2026vibe, p. 9]. Judges are calibrated in-sample [@chen2025iwr, p. 17; @si2025benchmarking, p. 17].
  - [I] No paper in the corpus tests construction-model or judge-model self-preference (evidence matrix C10).
- Novelty check (2026-11-12):
  - `rlab search` queries:
    1. "self-preference bias LLM judge code evaluation" (openalex, arxiv; 2024)
    2. "LLM-as-a-judge self-enhancement bias software engineering benchmark" (crossref, arxiv; 2024)
    3. "benchmark tests generated by LLM bias toward same model family evaluation" (openalex, arxiv; 2024)
    4. "WebDevJudge evaluating LLMs as critiques for web development quality" (arxiv, openalex; 2025)
  - WebSearch: "self-preference bias LLM judge web app generation benchmark same model family test generator coding agents".
  - Closest prior work ([A], abstracts):
    - *Silencer: From Discovery to Mitigation of Self-Bias in LLM-as-Benchmark-Generator* (NeurIPS 2025, DOI 10.52202/085713-4317; arXiv 2505.20738). Models score higher on benchmarks they generated; a mitigation is proposed. The tasks are not app generation (abstract and search snippet).
    - *Preference Leakage: A Contamination Problem in LLM-as-a-judge* (arXiv 2502.01534, preprint). Bias of judges toward same-model, inherited and same-family generators.
    - *Play Favorites: A Statistical Method to Measure Self-Bias in LLM-as-a-Judge* (arXiv 2508.06709, preprint) and *Quantifying and Mitigating Self-Preference Bias of LLM Judges* (arXiv 2604.22891, preprint). Measurement methods.
    - *WebDevJudge* (arXiv 2510.18560, preprint). LLM judges fall well short of human experts on web-development quality.
  - Verdict: **partially novel**. Self-preference and generator self-bias are established phenomena with ready-made measurement methods. We found no study that measures them in app-generation or reconstruction benchmarks, where the LLM writes the specs or tests and also judges the browser workflows (searches on 2026-11-12).
- Confidence: **medium**. The pattern is consistent in 4 papers, but it may be explained by real capability, which is exactly what the study must separate.
- Potential contribution: an estimate of how much benchmark rankings in this field move when the judge or test-author family changes, with a recommendation for cross-family judging and chance-corrected agreement.
- Suggested study / experiment:
  - Design: a re-evaluation study with no new generation.
  - Data: the released Vibe Code Bench trajectories and generated apps [@tran2026vibe, p. 11]. Optionally add WebGen-Bench outputs [@lu2025webgen, p. 1].
  - Sample: 20 apps × the 4–6 released models from different families.
  - Method:
    1. Re-judge every workflow with browser-agent judges from three families (e.g. Claude, GPT and an open-weights model), with fixed prompts.
    2. Two human raters label a stratified subsample of about 300 substeps as the gold standard.
    3. Estimate self-preference as the judge's score for same-family apps minus its score for other-family apps, conditional on the human gold (the Play Favorites idea).
  - Baseline: the human labels, and the original canonical judge.
  - Metrics: Cohen's/Fleiss' κ, ranking changes (Kendall τ), and the self-bias estimate with CIs.
  - Analysis: logistic mixed model (pass ~ judge family × builder family + app).
  - Threats to validity:
    - The human subsample may be too small to detect small biases.
    - Proprietary judges change over time.
    - Released trajectories may not be enough to replay every app; check this before starting.
- Feasibility for a beginner: **easy**. No generation is needed, only judge API calls and about 15–20 hours of human labelling.

## G3: It is unknown whether maintainability instruments agree with each other, and whether they predict maintenance effort, for AI-built applications

- Gap type: methodological / contradiction (C3, partly C1–C2).
- Evidence that the gap exists:
  - [A] PyExamine was chosen over SonarQube's "superficial linting" [@zhu2026understanding, p. 2]. [A] Technical-debt tools disagree on what counts as debt [@ehsani2026faster, p. 5]. [A] SonarQube and general linters are not designed for LLM-specific debt [@ehsani2026faster, p. 22], and LLM-aware quality tools are rarely independently evaluated [@ehsani2026faster, p. 28].
  - [A] SonarQube is called an "auxiliary indicator" only [@mota2026comparing, p. 6]. [V] borg2026echoes' outcome metric is a proprietary CodeHealth customised for the study, from the first author's employer [@borg2026echoes, p. 13; @borg2026echoes, p. 75].
  - [V] The direction of "LLM vs human" changes with the instrument and unit: fewer SonarQube bugs [@molison2025llm, p. 8], more repository warnings [@he2026speed, p. 7] that run mainly through code size [@he2026speed, p. 8], and smell counts that track LoC (ρ = 0.94) [@zhu2026understanding, p. 8].
  - [V] The only randomised maintenance outcome (second-developer time) showed no difference, while static measures in Phase 1 did show some [@borg2026echoes, p. 33; @borg2026echoes, p. 30]. The two kinds of measure were not related to each other.
- Novelty check (2026-11-12):
  - `rlab search` queries:
    1. "agreement between static analysis tools maintainability LLM-generated code" (openalex, arxiv; 2024)
    2. "SonarQube validity maintainability measurement developer perception AI-generated code" (crossref, openalex; 2023)
    3. "code smell detectors disagreement LLM generated code comparison of tools" (arxiv, openalex; 2024)
    4. "code quality maintainability of programs rebuilt by coding agents compared with original source" (arxiv, openalex; 2026)
  - WebSearch: "validity of SonarQube CodeHealth maintainability metrics for LLM-generated code agreement between tools human maintainability ratings 2026".
  - Closest prior work ([A], abstracts):
    - *Is Agent Code Less Maintainable Than Human Code?* (CodeThread; EMNLP 2026, DOI 10.18653/2026.emnlp-main.2528). Regression shows that "many traditional software engineering maintainability metrics do not explain" why agents do worse when building on agent code. The setting is issue-level repository patches with agents as maintainers. **This partly fills the original candidate**, so the gap is narrowed.
    - *Beyond Functional Correctness: Static Code Quality Profiling of LLM-Generated Code* (arXiv 2610.19167, preprint). Pylint, Radon and SonarQube on 65,663 LiveCodeBench programs. Single programs; the abstract mentions no tool-agreement or human validation.
    - *Comparing Open Source with Software Code Generated by AI Tools from Software Maintainability Quality Factor Perspective* (DOI 10.37394/232018.2025.13.58). MI, CC and Halstead on 3 tasks; no validation.
    - The WebSearch found no study that validates SonarQube or CodeHealth against human ratings or maintenance effort for LLM code.
  - Verdict: **partially novel (narrowed)**. Issue-level evidence that classic metrics fail to explain agent maintenance outcomes now exists (CodeThread). We found no study that, for whole AI-generated *applications*, (a) measures agreement among ≥3 maintainability instruments after size normalisation and (b) relates them to measured maintenance effort by humans or agents (searches on 2026-11-12).
- Confidence: **medium**. CodeThread and related 2026 work show the area is moving. Our claim is limited to application-level code and to inter-instrument agreement.
- Potential contribution: guidance on which (if any) static instruments a reconstruction study such as G1 should trust, and a test of the explanation offered for C1–C3.
- Suggested study / experiment:
  - Design: a measurement-validity (convergent and predictive validity) study.
  - Data: released generated full-stack apps from Vibe Code Bench [@tran2026vibe, p. 11]. Possibly also E2EDev outputs [@liu2026benchmarking, p. 9]. Sample about 60 apps across 4+ models.
  - Instruments: SonarQube (issues/KLoC, cognitive complexity), ESLint complexity rules, a Maintainability Index tool, jscpd duplication, and optionally CodeScene's free tier. All are normalised per KLoC or per function.
  - Criterion measures:
    1. Agent-maintainer success and cost on 2 scripted change requests per app (3 runs).
    2. Expert ranking by 3 raters of a 20-app subsample.
  - Analysis:
    - Kendall's W and pairwise Spearman correlations between instruments.
    - Mixed models predicting maintenance success from each instrument, controlling for size and functional pass rate.
    - Compare explained variance between instruments.
  - Threats to validity:
    - Agent-maintainer success depends on the maintainer model.
    - Apps from different models differ in features, not only in quality (control with functional pass rate).
    - Rater expertise.
- Feasibility for a beginner: **easy–moderate**. Existing released apps, free tools and scripted change tasks. The statistics are standard.

## G4: No study tests whether feedback loops improve both behavioural fidelity and code quality in reconstruction

- Gap type: contradiction (C4) / evidence.
- Evidence that the gap exists:
  - [V] On GPT-5.2, self-repair, environment repair and planning each lowered the non-functional score (46.1–49.9% vs 57.1%) without raising functional correctness [@pan2026functional, p. 8]. This is one model and one-shot strategies.
  - [V] Browser self-testing correlates with accuracy (r = 0.72), but the evidence is observational and the system prompt demands testing [@tran2026vibe, p. 7; @tran2026vibe, p. 16].
  - [V] Targeted loops improve exactly what they check: compile success and navigation [@zhou2025declarui, p. 9; @zhou2025declarui, p. 10], and build success, which then saturates [@wu2026looks, p. 6; @wu2026looks, p. 12]. zhou2025declarui's navigation score is partly circular [@zhou2025declarui, p. 7].
  - [A] Agents' own validation missed behavioural mismatches with the reference [@kim2026programdistill, p. 12].
  - [A] The authors of pan2026functional propose quality-aware generation and multi-turn evaluation as next steps [@pan2026functional, p. 10].
- Novelty check (2026-11-12):
  - `rlab search` queries:
    1. "self-repair iterative feedback code quality maintainability LLM agents" (openalex, arxiv; 2024)
    2. "iterative refinement degrades code quality security LLM generated code" (crossref, arxiv; 2024)
    3. "multi-turn feedback web application generation functional correctness and code quality" (openalex, arxiv; 2025)
    4. "Static Analysis as a Feedback Loop: Enhancing LLM-Generated Code Beyond Correctness" (arxiv, openalex; 2025; identifier check)
    5. "Generation of Web Apps with Agentic IDEs: An Empirical Assessment" (arxiv, openalex; 2026; identifier check)
  - WebSearch: "iterative self-repair feedback loop effect on both functional correctness and maintainability of generated web applications study".
  - Closest prior work ([A], abstracts):
    - *From Runnable Code to Shippable Applications: Test-Driven Development for Full-Stack Web Application Generation* (TDDev; DOI 10.1145/3832783.3834388). TDD loops raise functional accuracy by 15.5–23.7 pp on 20 spec-built web apps. The abstract mentions no code-quality outcome.
    - *Static Analysis as a Feedback Loop* (DOI 10.1109/scam67354.2025.00017; arXiv 2508.14419). Bandit and Pylint feedback improves security, readability and reliability on snippets (GPT-4o).
    - *Comparative Analysis of Iterative Prompt Refinement and Quality of LLM-Generated Code* (SSRN, DOI 10.2139/ssrn.7435043, preprint). 30 JavaScript tasks; correctness, maintainability and security under iteration.
    - *Security Weaknesses in LLM-Generated Source Code: … Iterative AI-Assisted Development* (SSRN, DOI 10.2139/ssrn.6958668, preprint). Security degradation across 1,250 versions.
    - *Generation of Web Apps with Agentic IDEs* (Zenodo DOI 10.5281/zenodo.19208142; arXiv 2608.20903). Five full-stack apps; iteration "rarely introduces regressions".
    - MACBench (DOI 10.18653/2026.emnlp-main.2172) and FronTalk (arXiv 2601.04203). Multi-turn front-end generation.
  - Verdict: **partially novel**. Feedback-loop effects on code quality are studied for snippets and spec-built apps, and on functionality for full-stack apps. We found no controlled study of reconstruction from an original that compares feedback types (behavioural diff against the original, generic self-repair, static-analysis feedback) on fidelity and maintainability together (searches on 2026-11-12).
- Confidence: **medium**. The contradiction in our corpus is real, but nearby work is dense. The novelty lies only in the combination (reconstruction setting × two outcome families × feedback types).
- Potential contribution: resolves C4. It would show whether feedback in reconstruction trades code quality for fidelity, as pan2026functional's single-model result suggests, or improves both.
- Suggested study / experiment:
  - Design: a 4-arm within-app experiment. It can reuse the G1 pipeline.
    1. No feedback.
    2. Generic self-repair.
    3. Behavioural-diff feedback: failing locator-independent tests run on the original vs the rebuild, with the test messages shown to the agent.
    4. Static-analysis feedback: SonarQube/ESLint findings.
  - Sample: 6 apps × 1 open agent harness × 2 models × 4 arms × 3 runs = 144 rebuilds. The iteration budget is the same in every arm.
  - Metrics: the G1 fidelity and maintainability measures, plus code size.
  - Analysis: mixed model (outcome ~ arm × model + app), with planned contrasts against arm 1.
  - Threats to validity:
    - Arm 3 leaks the test oracle; use a held-out test split for scoring.
    - Equal budgets may still differ in tokens.
    - Two models limit generality.
- Feasibility for a beginner: **moderate**. The harness scripting is straightforward but the run count is large. Start with 3 apps.

## G5: The effect of training-data contamination on reconstruction fidelity has not been measured

- Gap type: methodological.
- Evidence that the gap exists:
  - [V] Reference apps are mostly popular public projects. Explicit controls appear in only a few papers: an overlap audit [@bai2026recreationworld, p. 18], no internet access plus an ablation [@yang2026programbench, p. 6], BLEU against the original [@xiao2025benchmarking, p. 5], post-cutoff builds [@xiong2026propgen, p. 11], and keeping task code out of public repositories [@borg2026echoes, p. 66].
  - [A] pan2026functional cannot rule out pretraining exposure [@pan2026functional, p. 2]. [V] Its example prompt names the original project [@pan2026functional, p. 3]. [V] Interface hints raised one task from 0.17 to 0.67 [@pan2026functional, p. 4].
  - [V] With internet access, 20–36% of the stronger models' tasks were flagged as cheating, mostly source lookup [@yang2026programbench, p. 6; @yang2026programbench, p. 17].
  - [I] For chen2025iwr, kim2026programdistill, liu2026benchmarking, si2025benchmarking and wu2026looks, no contamination discussion was found (methodology comparison §5.3).
- Novelty check (2026-11-12):
  - `rlab search` queries:
    1. "data contamination benchmark web application generation LLM" (openalex, arxiv; 2024)
    2. "contamination-free benchmark repository-level code generation post-cutoff" (arxiv, crossref; 2024)
    3. "obfuscated private reference application benchmark coding agents leakage" (openalex, arxiv; 2025)
  - WebSearch: "contamination-free app generation benchmark unseen private reference applications coding agents 2026".
  - Closest prior work ([A]):
    - *The Next Challenge for Agentic Cybersecurity: A Realistic, Contamination-Free Reverse Engineering Benchmark* (SRE-Bench; arXiv 2608.11469, preprint). 19 private, expert-built programs for binary reverse engineering in a security analysis setting, not app reconstruction.
    - RAL-Bench, which is our pan2026functional, excludes repositories already used in public benchmarks (web-search snippet). Vibe Code Bench, our tran2026vibe, keeps a held-out test split.
    - The web search reports private-repository coding benchmarks for issue fixing (secondary sources only, not verified).
    - Contamination surveys and limited-contamination benchmarks exist in general NLP, e.g. *LiveBench* (arXiv 2406.19314) and *Benchmark Data Contamination of Large Language Models: A Survey* (arXiv 2406.04244).
  - Verdict: **partially novel**. Contamination-limited benchmark construction is known, including private programs for binary RE. We found no study that measures the *size of the contamination effect* on reconstruction fidelity by comparing public, well-known originals with matched post-cutoff or private originals under the same black-box protocol (searches on 2026-11-12).
- Confidence: **medium-low**. Matching public and private apps on difficulty is hard, so a null result would be hard to interpret. Several benchmarks already apply partial controls.
- Potential contribution: an estimate of how far published reconstruction scores may be inflated by memorisation, which is needed to interpret RQ2 figures.
- Suggested study / experiment:
  - Design: a matched-pair comparison, embeddable in G1 as the Stratum A vs B factor.
  - Data and sample:
    - 5 public apps with many GitHub stars.
    - 5 matched apps of similar size and features, written by the researcher or first released after the model cutoffs.
    - Optional "renamed clone" control: the same public app with renamed identifiers and text.
  - Method: identical black-box inputs, 2 models, 3 runs each.
  - Metrics:
    1. Fidelity (G1 tests).
    2. Verbatim or near-verbatim overlap with the original source (token n-gram or BLEU, as in xiao2025benchmarking [@xiao2025benchmarking, p. 5]).
    3. Whether the agent names the original project unprompted.
  - Analysis: paired differences with bootstrap CIs; overlap–fidelity correlation.
  - Threats to validity: imperfect matching of difficulty; researcher-written apps may be easier; small n.
- Feasibility for a beginner: **moderate**. Writing 5 matched apps is the main cost; small CRUD apps are enough.

## G6: Human-steered (vibe-coding) reconstruction has not been compared with autonomous agents

- Gap type: population/context / practical.
- Evidence that the gap exists:
  - [A] Human-guided and multi-agent reconstruction is named as future work in yang2026programbench [@yang2026programbench, p. 12]. kim2026programdistill evaluates a single text-only harness [@kim2026programdistill, p. 14].
  - [V] Reconstruction and generation benchmarks have no human-developer baseline [@yang2026programbench, p. 20; @tran2026vibe, p. 5; @lu2025webgen, p. 7].
  - [V] Practitioner vibe coding is NL prompting plus re-prompting with minimal review [@fawzy2026vibe, p. 1]. 36% of QA units report skipped QA [@fawzy2026vibe, p. 8].
  - [V] The only human vs agentic comparison in the corpus uses 2 tiny tasks, scripted prompts that participants could not change, and different model generations (GPT-3.5 vs GPT-5/Claude) [@mock2026vibe, p. 15; @mock2026vibe, p. 17].
  - [V] The definitions of vibe coding differ across papers, so results cannot be pooled (C9) [@asdaque2026novice, p. 1; @he2026speed, p. 4].
- Novelty check (2026-11-12):
  - `rlab search` queries:
    1. "human-in-the-loop versus autonomous coding agent application development controlled experiment" (openalex, arxiv; 2024)
    2. "vibe coding participants build application user study versus agent" (openalex, crossref, arxiv; 2025)
    3. "developer steering coding agent recreate existing application" (arxiv, openalex; 2025)
    4. "human developer versus AI agent rebuild application same specification comparison" (arxiv, crossref; 2025)
    5. "Why Human Guidance Matters in Collaborative Vibe Coding" (arxiv, openalex; 2026; identifier check)
  - WebSearch: "human-steered vibe coding versus autonomous agent rebuild application study 2026 arXiv".
  - Closest prior work ([A], abstracts):
    - *Why Human Guidance Matters in Collaborative Vibe Coding* (arXiv 2602.10473, preprint; data at OSF DOI 10.17605/osf.io/bzdrv). 20 experiments, 737 participants. Human-led, AI-led and hybrid vibe coding; human instructions outperform AI instructions. Per the web-search summary, the task is reproducing reference images as SVG code. That is reference reproduction, but not of software applications, and code quality is not measured.
    - *CentaurEval* (arXiv 2512.04111, preprint). 45 participants vs 5 LLMs at 4 levels of human intervention on "collaboration-necessary" coding templates. Not reconstruction.
    - *SWE-Together* (arXiv 2606.29957, preprint). Simulated users in repository tasks.
    - *Professional Software Developers Don't Vibe, They Control* (arXiv 2512.14012, preprint). Qualitative study.
    - mock2026vibe is already in the project.
  - Verdict: **partially novel**. The value of human guidance in vibe coding has been shown on non-software reference reproduction (SVG) and on coding puzzles. We found no study that compares human-steered vibe-coding reconstruction of an existing application with autonomous agents using the same model, scored on behavioural fidelity and maintainability (searches on 2026-11-12).
- Confidence: **medium**. The closest work (2602.10473) is strong and recent and could be extended by its authors.
- Potential contribution: evidence on whether the practitioner workflow named in the project title adds fidelity or quality beyond an autonomous agent with the same model, and at what cost in time.
- Suggested study / experiment:
  - Design: a within-subject, counterbalanced lab study plus an autonomous-agent arm.
  - Sample: 12–16 participants (students or junior developers).
  - Apps: 2 small apps of comparable size from G1 Stratum B.
  - Conditions:
    1. Human-steered: the participant may only prompt a vibe-coding tool, has 90 minutes, and sees the running original.
    2. Autonomous: the same tool and model, given the same initial prompt, 3 runs.
  - Model: fixed and identical in both conditions, which avoids mock2026vibe's model confound [@mock2026vibe, p. 17].
  - Metrics: G1 fidelity tests and maintainability measures, time, number of prompts, and the participant's prompting strategy (coded from logs).
  - Analysis: paired Wilcoxon tests or mixed models with effect sizes. Preregister.
  - Threats to validity:
    - Small sample.
    - Learning effects (counterbalance the order).
    - Participant skill (measure with a pre-test).
    - The time limit may favour the agent.
- Feasibility for a beginner: **moderate–hard**. It needs ethics approval and participant recruitment. Running it as a pilot with about 8 participants is realistic.

## G7: The bias from oracles tied to the original's identifiers has not been quantified

- Gap type: methodological. The original candidate is narrowed after the novelty check.
- Evidence that the gap exists:
  - [V] E2EDev tests depend on `data-testid` anchors from the original, and the anchors are given in the prompt [@liu2026benchmarking, p. 16]. kim2026programdistill's oracles use the original's selectors [@kim2026programdistill, p. 35].
  - [V] 6.5% of zhao2025vibe's security tests were coupled to the reference implementation and had to be rewritten [@zhao2025vibe, p. 19].
  - [V] Interface hints change measured fidelity a lot (0.17 → 0.67) [@pan2026functional, p. 4]. Structural priors are given as input [@wu2026looks, p. 3; @zhou2025declarui, p. 4], and zhou2025declarui's navigation metric is scored against its own input graph [@zhou2025declarui, p. 7].
- Novelty check (2026-11-12):
  - `rlab search` queries:
    1. "implementation-agnostic GUI test oracle locator-independent behavioural tests reimplementation" (openalex, arxiv; 2023)
    2. "semantic test migration across web applications LLM locator" (openalex, crossref, arxiv; 2023)
    3. "behavioral equivalence testing web application reimplementation black-box" (openalex, arxiv; 2024)
  - WebSearch: "implementation-agnostic black-box test oracle for evaluating reconstructed web apps without element identifiers selectors 2026".
  - Closest prior work ([A]):
    - *Do LLM-Generated Web Apps Behave Correctly? A Contract-Grounded Benchmark for Behavioral Conformance* (ConformWeb; EMNLP 2026, DOI 10.18653/2026.emnlp-main.2018). Hidden interaction scenarios from public behavioural contracts, without reference implementations.
    - *VISTA* (arXiv 2605.26144). Locates annotated components in the running app and probes them.
    - *UI2App* (arXiv 2607.06306). Its interaction metric "credits any valid implementation".
    - *BackendForge* (DOI 10.18653/2026.findings-emnlp.2236). Black-box HTTP tests against an OpenAPI contract.
    - In the project: implementation-agnostic CLI oracles [@yang2026programbench, p. 5] and accessibility/DOM tests [@bai2026recreationworld, p. 9].
  - Verdict: **mostly addressed as a method**. Identifier-free oracles now exist in several forms. The narrow residual gap: we found no study that re-scores the *same* rebuilds with identifier-coupled and identifier-free oracles to measure how much coupling changes fidelity scores and rankings (searches on 2026-11-12).
- Confidence: **low-medium**. The residual question is small and may be answered as a side analysis in any of the papers above.
- Potential contribution: a correction factor or caution for interpreting E2EDev-style and ProgramDistill-style fidelity figures (RQ2).
- Suggested study / experiment:
  - Data: released E2EDev projects and tests [@liu2026benchmarking, p. 9].
  - Method:
    1. Generate rebuilds of 10 apps without `data-testid` hints (2 models × 3 runs).
    2. Score them with (a) the original tests and (b) the same scenarios rewritten with role- and text-based Playwright locators, validated at 100% on the originals.
  - Metrics: the pass-rate difference and the change in model ranking (Kendall τ).
  - Threats to validity: the rewritten tests may be less strict, so check them on deliberately broken mutants.
- Feasibility for a beginner: **easy**. It mostly requires test rewriting.

## G8: Reconstruction of native mobile apps including their hidden back-end behaviour is barely studied

- Gap type: population/context.
- Evidence that the gap exists:
  - [V] Only bai2026recreationworld covers native desktop and Android [@bai2026recreationworld, p. 7]. Mobile work uses a React web proxy [@wu2026looks, p. 9] or UI-only code with no back-end or business logic [@zhou2025declarui, p. 2; @zhou2025declarui, p. 12].
  - [A] Back-end-dependent interactions are left as future work [@xiao2025benchmarking, p. 11], as are desktop and mobile apps [@kim2026programdistill, p. 14].
  - [V] Functional success drops with external services (34.2% vs 13.5%) [@tran2026vibe, p. 6].
- Novelty check (2026-11-12):
  - `rlab search` queries:
    1. "native Android app generation from screenshots LLM benchmark functional" (openalex, arxiv; 2024)
    2. "full-stack application reconstruction backend inference from frontend LLM" (openalex, arxiv; 2024)
    3. "mobile app generation LLM agent Kotlin Swift benchmark" (crossref, arxiv; 2024)
    4. "full-stack web application generation benchmark backend database functional tests" (openalex, arxiv; 2025)
    5. "Android app reverse engineering regenerate source code LLM UI behaviour" (arxiv, openalex; 2024)
    6. "From Assistant to Independent Developer Are GPTs Ready for Software Development Android" (openalex, arxiv; 2025; identifier check)
  - WebSearch: "LLM agents reconstruct native Android iOS app with backend from running app screenshots benchmark 2026".
  - Closest prior work ([A]):
    - *VISTA* (arXiv 2605.26144). Full-stack Web and Android apps from design handoffs.
    - *AppForge* (arXiv 2510.07740; listed as ICLR 2026 in the web result, not verified). 101 Android apps from NL specs.
    - *BackendForge* (DOI 10.18653/2026.findings-emnlp.2236). Back-ends from OpenAPI contracts.
    - *FullStack-Agent* (arXiv 2602.03798).
    - In the project: bai2026recreationworld (Android from a running reference).
  - Verdict: **partially addressed**. Native-Android generation from specs and designs, and Android reconstruction from a running app, exist. We found no study in which the back-end of a native mobile app must be inferred from black-box observation of the running app and scored for fidelity (searches on 2026-11-12).
- Confidence: **low**. The residual gap is narrow, and VISTA and bai2026recreationworld are close.
- Potential contribution: tests whether the "interaction lags structure" finding (G-A2) is worse when state lives on a hidden server.
- Suggested study / experiment:
  - Data: 3–5 small open-source Android apps with a simple REST back-end.
  - Method: the agent gets the emulator plus network-traffic observation, but no source. Two models, 3 runs each.
  - Metrics: UI-test pass rate, back-end API conformance (replayed requests), and G1 maintainability measures.
  - Threats to validity: emulator setup cost, few apps, and limited traffic visibility.
- Feasibility for a beginner: **hard**. It needs Android tooling, back-end hosting and traffic capture. Better as later work.

---

## Dropped or merged candidates

- **Single runs, no variance, no significance tests** (RQ4's strongest weakness [@lu2025webgen, p. 40; @tran2026vibe, p. 8]). This is not reported as a separate gap. It is a reporting-practice problem rather than an open research question, and no novelty check was run, so it cannot be claimed (§7). It is built into every design above (≥3 runs, CIs).
- **No human-developer baseline** [@yang2026programbench, p. 20]. Merged into G6.
- **Security fidelity of reconstructions**. Covered by `reports/novelty-check-security-fidelity.md` (separate check, not duplicated). It fits as an extra outcome in G1.
- **"Visual fidelity exceeds functional fidelity"** (C5). Dropped as a gap: the evidence matrix shows the claim rests partly on how the metrics are built [@chen2025iwr, p. 7], so it is a measurement artefact, not an untested question.

## Papers recommended for inclusion (found in novelty checks; not analysed, not cited as evidence)

Identifiers are copied from `rlab search` output on 2026-11-12. Priority is our judgement [I].

| Priority | Paper | Identifier | Why |
|---|---|---|---|
| high | Is Agent Code Less Maintainable Than Human Code? (CodeThread) | DOI 10.18653/2026.emnlp-main.2528; arXiv 2606.21804 | Peer-reviewed maintainability-by-downstream-task method; narrows G3; template for G1's maintainer task |
| high | VISTA: An End-to-End Benchmark for Visual Spec-to-Web-App Coding Agents | arXiv 2605.26144 | Design → full-stack Web + Android, component-level behaviour probes (G1, G7, G8) |
| high | UI2App: Benchmarking Visual Interaction Inference in Executable Web Application Generation | arXiv 2607.06306 | Screenshot-only multi-route app generation; implementation-agnostic interaction metric (G1, G7) |
| high | MirrorCode: AI can rebuild entire programs from behavior alone | arXiv 2606.30182 | Behaviour-only reimplementation benchmark (F2 family; G1) |
| high | Why Human Guidance Matters in Collaborative Vibe Coding | arXiv 2602.10473 | Human-led vs AI-led vibe coding, 737 participants (G6) |
| medium | Do LLM-Generated Web Apps Behave Correctly? (ConformWeb) | DOI 10.18653/2026.emnlp-main.2018 | Contract-grounded black-box oracle (G7) |
| medium | WebCoderBench | DOI 10.18653/v1/2026.acl-long.535; arXiv 2601.02430 | Multi-perspective web-app metrics including lint/comment-rate proxies (G1, G3) |
| medium | From Runnable Code to Shippable Applications (TDDev) | DOI 10.1145/3832783.3834388; arXiv 2605.17242 | Controlled TDD-loop study for full-stack apps (G4) |
| medium | Silencer: Self-Bias in LLM-as-Benchmark-Generator | DOI 10.52202/085713-4317; arXiv 2505.20738 | Generator self-bias method (G2) |
| medium | Preference Leakage: A Contamination Problem in LLM-as-a-judge | arXiv 2502.01534 | Same-family judge bias (G2) |
| medium | WebDevJudge | arXiv 2510.18560 | LLM-judge reliability for web development (G2) |
| medium | Trajectory-Level Security Debt in LLM Coding Agents | DOI 10.1609/aaaiss.v10i1.43533 | Static scans of ProgramBench rebuilds (G1; also in the security check) |
| medium | SWE-CI | arXiv 2603.03823 | Maintainability as functional stability over evolution (G1, G3) |
| low | AppForge | arXiv 2510.07740 | Native Android generation from spec (G8) |
| low | CentaurEval | arXiv 2512.04111 | Human-in-the-loop value benchmark (G6) |
| low | Beyond Functional Correctness: Static Code Quality Profiling of LLM-Generated Code | arXiv 2610.19167 | Multi-tool static profiling at scale (G3) |
| low | The Next Challenge for Agentic Cybersecurity (SRE-Bench) | arXiv 2608.11469 | Contamination-free private-program construction (G5) |
| low | BackendForge | DOI 10.18653/2026.findings-emnlp.2236; arXiv 2607.11042 | Black-box back-end oracle (G7, G8) |
| low | Comparative Analysis of Iterative Prompt Refinement and Quality of LLM-Generated Code | DOI 10.2139/ssrn.7435043 (SSRN preprint) | Iteration × maintainability on JS tasks (G4) |

## Implications for RQ5 (suggested text; RESEARCH-QUESTIONS.md not edited by this report)

See the caller's summary. In short: the top-ranked gap (G1) passed the novelty check for its narrow form. Two easy follow-ups (G2 judge-family bias, G3 instrument validity) are partially novel. All other candidates are partially novel or mostly addressed.
