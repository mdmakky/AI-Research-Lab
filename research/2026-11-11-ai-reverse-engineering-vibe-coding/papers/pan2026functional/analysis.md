---
key: pan2026functional
status: ready
evidence_basis: full-text
design: benchmark construction + controlled empirical evaluation of 16 LLMs (zero-shot, single-pass repository generation)
dataset: RAL-Bench, 38 pinned Python GitHub projects in 7 scenarios with reference-validated black-box system tests
sample_size: 38 tasks x 16 LLMs x 3 runs; 446 repositories in failure analysis; 76 injected defects
metrics: functional test pass rate; reference-normalised maintainability (MI), security (high-risk static findings), robustness, efficiency, resource; AHP-weighted non-functional score; USD cost
main_finding: No LLM exceeds 45% functional pass rate on application-level repository generation; non-functional scores ~50%; repair/planning strategies did not help and lowered quality.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Toward Functional and Non-Functional Evaluation of Application-Level Code Generation

- Authors: Pan, Ruwei; Zhang, Yakun; Liang, Qingyuan; Zhu, Yueheng; Liu, Chao; Zhang, Lu; Zhang, Hongyu
- Year / venue: 2026, arXiv (preprint, not peer-reviewed; the PDF carries an unfilled ACM "Conference'17" template header)
- DOI: 10.48550/arxiv.2602.03462 · URL: https://arxiv.org/abs/2602.03462
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] Test whether current LLMs can generate *application-level* repositories (runnable, multi-file, with dependencies, executable end to end) that satisfy both functional correctness and non-functional quality attributes. The authors argue that function-, contest-, repo-completion- and feature-level benchmarks do not test this (p. 1).
- [A] Introduce RAL-Bench (Real-World Application-Level Code Generation Bench): a benchmark and evaluation framework that derives a natural-language requirement from a real reference project and tests generated repositories with reference-validated black-box system tests (p. 1).

## 2. Research questions / hypotheses
- [V] RQ1: how well current LLMs perform at application-level generation; RQ2: where they fail; RQ3: what it costs; RQ4: whether mainstream generation strategies help (p. 5).
- No formal hypotheses stated.

## 3. Methodology
- Research design: [V] Benchmark construction, then a controlled, single-turn, zero-shot comparison of 16 LLMs, plus a manual failure taxonomy, a cost analysis, a single-model strategy ablation, and prompt-sensitivity and metric-robustness checks (p. 4; p. 5; p. 9).
- Approach / model / intervention: [V] Each LLM receives (a) a short NL requirement drafted from the reference project's README, public API, usage examples and source code, then manually edited to remove implementation details, file-layout hints and project-specific names, and (b) the reference repository's expected module/package surface (an "interface specification"). It outputs the whole repository in one pass (p. 2; p. 4; p. 5). [V] For GPT-5.2 on Stegano, adding the interface specification raised the functional score from 0.1667 to 0.6667, attributed to fewer entry-point/module-path mismatches (p. 4).
- Baselines or comparison conditions: [V] 11 "standard" and 5 "thinking" LLMs are compared with each other. There is no non-LLM or human baseline; the reference repository is used only as a normalisation anchor for non-functional scores (p. 4; p. 5). [V] RQ4 compares the GPT-5.2 baseline with three one-shot strategies: S1 feedback-driven self-repair, S2 automated environment repair, S3 planning-driven generation (p. 8).
- [I] Relation to our topic: the "reference" is a real application, and generated code is judged on tests that pass on that reference. This is close to rebuilding an existing app from its specification. However, the model never sees or runs the reference. It gets a distilled text requirement plus the API surface, so this is spec-to-app generation, not black-box behavioural reverse engineering.

## 4. Dataset and sample
- Data source(s): [V] 38 actively maintained Python GitHub projects (e.g. tabulate, click, requests, celery, mitmproxy, sqlmap), each pinned to a commit SHA and grouped into seven scenarios (Tooling, Data, Web, Security, Automation, Observability, Content). Sizes range from 1 to 242 files and 0.3k to 109.5k LoC (p. 2).
- Sample size (N) and unit: [V] 38 tasks with "more than 450 evaluation points" (p. 2). [V] Functional tests per task: mean 11.03, median 11.5, min 10, max 19. Executable suites per task: mean 17.66 (p. 5). [V] 16 LLMs, 3 runs each (p. 5). [V] The failure analysis covers 446 generated repositories and more than 4,500 test execution logs (p. 7).
- Sampling / selection method: [V] Three criteria: clearly documented functionality, stable public interfaces suitable for end-to-end tests, and active real-world use. Average popularity is above 1,000 stars, and repositories already used in public code-generation benchmarks are excluded (p. 2). How the 38 were picked from the candidate pool: not reported.
- Data availability (public? link?): [A] All scripts and data are released at github.com/Wwstarry/RAL-Bench (p. 11). The AHP derivation is said to be in an "anonymous repository" (p. 4).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Zero-shot, each model's default prompt template, the whole repository generated in one pass within context limits, three repeats averaged (p. 5). [A] The abstract says "greedy decoding" (p. 1). The setup section does not restate temperature or decoding parameters (not reported in Section 3.1). [V] Tests are pytest suites run against the generated repository; the functional score is the pass ratio (p. 3; p. 4). [V] Non-functional pipeline (p. 3; p. 4):
  - maintainability: lower-bound Maintainability Index (MI) from static analysis;
  - security: number of high-risk static-analysis findings;
  - robustness: pass rate on an invalid/boundary-input suite;
  - efficiency: runtime of an efficiency suite;
  - resource: average RSS memory and CPU during a resource suite.
  
  Each is normalised against the reference repository and capped at 1. The static-analysis tools are not named in the text; Fig. 3 shows only "mi_min" and "high_risk_count" (p. 4). [V] Aggregate NF = 0.36 M + 0.24 S + 0.16 Rb + 0.12 E + 0.12 Ru. The weights come from AHP (analytic hierarchy process, a method that turns pairwise importance judgements into weights) applied to an ordering taken from Botchway et al.; consistency ratio 0.030 (p. 4).
- [V] Rerun stability: the full pipeline was rerun 5 times for GPT-5.2, Gemini-3-Pro-Preview and Claude-4.5-Sonnet (p. 6; p. 7).
- [V] Cost: provider token pricing, generation only, excluding test execution (p. 8).
- Code availability: [A] public GitHub repository (p. 11).

## 6. Evaluation metrics
- Functional score: pass rate of reference-validated black-box functional tests. Chosen because it "directly measures whether the generated application behavior matches the reference implementation's intended functionality" (p. 4).
- Maintainability M = (g/b)/(1+g/b), where g and b are the MI lower bounds of the generated and reference code. Called a "low-cost and reproducible signal of structural complexity"; the authors note that it misses naming quality and architectural clarity (p. 3).
- Security S = min(1, (b+1)/(g+1)) over high-risk static findings, described as a "conservative risk signal" (p. 3).
- Robustness Rb is the pass ratio of the robustness suite. Efficiency E = min(1, Tref/Tgen), set to 0 if the suite fails. Resource Ru is the mean of the capped memory and CPU ratios, set to 0 if the suite fails (p. 3; p. 4).
- Non-functional score NF: AHP-weighted sum of the five dimensions (p. 4).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V] No significance tests, confidence intervals or effect sizes. The paper reports only means over 3 runs and Std/CV over 5 reruns (p. 5; p. 7). [V] Metric robustness is checked with Spearman rank correlation of model rankings under alternative aggregations (p. 10).

## 7. Key findings
1. [V] Functional correctness is low. The average functional score is 33.98% for standard and 30.23% for thinking LLMs, and no model exceeds 45%. Best: Gemini-3-Pro-Preview 43.86% and Gemini-2.5-Pro-Thinking 43.44%; lowest: DeepSeek-R1 16.23% (p. 5; p. 6).
2. [V] Non-functional averages are higher: 52.25% for standard and 49.57% for thinking LLMs. For standard LLMs, average maintainability is 33.45% and security 87.40% (p. 5; p. 6).
3. [V] NF separates models that functional scores do not: Gemini-2.5-Pro and GPT-4o have almost equal functional scores (27.63% vs 27.48%) but NF of 35.15% vs 57.59% (p. 5).
4. [V] Thinking models are not consistently better and on average score slightly below standard LLMs (p. 6).
5. [V] Failure taxonomy: requirement–implementation mismatches plus non-functional quality failures make up 82.8% of failures; executability/dependency failures make up 17.2% (p. 7).
6. [V] Cost per run ranges from $0.15 (DeepSeek-V3.2) to $16.63 (Claude-3.7-Sonnet-Thinking), averaging $4.10 for standard and $11.00 for thinking models. Higher cost does not reliably buy a higher functional score (p. 8).
7. [V] On GPT-5.2, none of the three one-shot strategies beat the baseline (41.80% functional, 57.10% NF). S1 scored 37.70/46.10, S2 40.20/49.90 and S3 41.20/49.60; all three lowered NF (p. 8; p. 9).
8. [V] Prompt variants moved GPT-5.2's mean functional score from 0.4181 (baseline) to 0.4972 (clarified) and 0.4919 (paraphrased). The authors call the differences small (p. 9).
9. [V] Functional scores had Std = 0 and CV = 0 across 5 reruns for all three models and all 38 projects; the median NF CV was 0.0007 (p. 6; p. 7).
10. [V] The NF model ranking is stable under equal weights, uncapped normalisation and leave-one-out variants (Spearman 0.90–0.99), but not under a rank-based aggregate (0.6441) (p. 10).
11. [V] Defect-injection sanity check: the functional suites detected all 76 injected defects (2 per task); the robustness suites detected 0.375 of them (p. 5).

## 8. Limitations stated by the authors
- [A] The repositories are public, so pretraining exposure cannot be ruled out. Results are interpreted as reflecting "realistic public-repository exposure conditions" (p. 2).
- [A] Validating tests on the reference repository supports oracle validity but does not guarantee full behavioural coverage (p. 3).
- [A] MI does not capture naming quality or architectural clarity. Static security analysis can give false positives and false negatives. Runtime measures depend on the environment. The metrics are operational proxies, not an expert audit (p. 3; p. 4).
- [A] The single-turn zero-shot protocol does not represent iterative or agentic workflows; a multi-turn/agentic study is future work (p. 4; p. 5).
- [A] The strategy study (RQ4) uses a single model and is not a ranking of strategy families (p. 8).
- [A] The AHP weights are not claimed to be universal across domains (p. 4).

## 9. Limitations we identified
- [I] The oracles are small. About 11 functional tests per task (p. 5) is a thin behavioural specification for projects of up to 109.5k LoC (p. 2). The 100% defect-detection rate rests on only 2 injected defects per task, and their type and injection method are not described (p. 5). It does not show that the suites would catch subtle divergences.
- [I] Contamination is likely, not just possible. The example requirement in Fig. 2/3 asks for code that "is API-compatible with the core parts of the Stegano project" (p. 3; p. 4), naming the original even though project-specific names were supposedly removed (p. 2). In the Celery failure case, the generated code references `celery.utils.threads`, "consistent with upstream Celery internals" (p. 9), which suggests recall of the original code. Together with the supplied module/package surface (p. 4), the task partly tests memory of well-known Python libraries.
- [I] The non-functional metrics can reward incomplete code. Maintainability and security are static and are computed whatever the functional result. A small or partial repository naturally has fewer high-risk findings and simpler structure. GPT-3.5-Turbo's 97.37% security score next to its 29.76% functional score (p. 6) fits this reading. NF therefore mixes "quality" with "less code". Only efficiency and resource are set to 0 when their suites fail (p. 3).
- [I] The maintainability score M = (g/b)/(1+g/b) equals 0.5 when the generated MI equals the reference MI and approaches 1 only when the generated MI is much higher (p. 3). M is therefore on a different scale from the other four dimensions, yet it carries the largest weight (0.36) (p. 4). An average M of about 33% (p. 6) suggests that the typical generated repository has a lower MI lower bound than the reference, but the paper reports no raw MI values to confirm this.
- [I] Zero variance in functional scores across 5 full reruns (p. 7) is surprising for API-served LLMs generating whole repositories, even with greedy decoding. Either the reruns re-evaluated cached generations, or the models were unusually deterministic. The paper does not say which, so the stability claim may describe the test harness rather than generation.
- [I] The 446 repositories in the failure analysis (p. 7) do not match 16 models x 38 tasks (608 per run), and how they were selected is not reported. Who assigned the failure categories, and whether agreement was measured, is also not reported.
- [I] The prompt-sensitivity result (0.4181 to 0.4972, about +8 points or +19% relative) (p. 9) is not "small" compared with the roughly 16-point spread across most models (p. 6). Requirement wording may matter as much as model choice.
- [I] All projects are Python libraries or CLI-style tools (p. 2), with no GUI, web front end or interactive application, so the findings transfer only partly to UI-level reconstruction.
- [I] "Maintainability" is reduced to one complexity index. Code smells, duplication, modularity and human judgement of the generated code are not measured.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Requirements were drafted with access to the source code (p. 2), tests were built from the reference's documented behaviour (p. 2), and the interface specification reveals the module layout (p. 4). Contamination with the original public code is plausible (see section 9). Who drafted and reviewed the requirements and tests, and with what tool support, is not reported.
- External (generalisability of sample/context): [I] 38 Python projects, mostly libraries and CLI tools. Generation is single-turn and zero-shot without agents (p. 4; p. 5), unlike vibe-coding practice where developers iterate with agents.
- Construct (do metrics measure the concept?): [I] The functional score is a pass rate on about 11 tests (p. 5), maintainability is the MI lower bound only (p. 3), and security is a count of high-risk static findings. These are weak proxies for "functional fidelity" and "maintainability" as our project defines them, which the authors acknowledge (p. 4).
- Statistical conclusion (power, multiple comparisons, variance): [I] No tests or intervals. Model differences of a few points (e.g. 27.63 vs 27.48) are discussed only descriptively (p. 5). Results are means of three runs (p. 5).
- Reproducibility (data/code/setup reported?): [A] Code and data are public (p. 11), and commits are pinned (p. 2). [I] Decoding parameters appear only in the abstract, and the static-analysis tools are not named in the text.

## 11. Future research directions
- Stated by authors [A] (p. 10; p. 11):
  - requirement analysis that turns short NL requests into explicit specifications with behaviours and edge cases;
  - cross-module repair using application-level feedback;
  - quality-aware generation that treats robustness, efficiency, resources, maintainability and security as explicit constraints;
  - extending RAL-Bench to more projects and to multi-turn/agentic settings (p. 5).
- Suggested by us [I]:
  1. Run the same reference-validated test design in an agentic, iterative (vibe-coding-like) setting.
  2. Report raw MI and add richer maintainability measures that do not depend on code size (smells, duplication, modularity, change-effort experiments).
  3. Test with obfuscated project names and without the interface specification to estimate contamination.
  4. Extend the design to applications with UIs.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2, RQ3, RQ4, RQ5 (secondary RQ1).
- How it informs our work [I]: This is one of the few studies that measures both functional correctness and maintainability of the same generated applications against the original project, using the original as test oracle and as normalisation anchor. That is the joint fidelity-plus-quality design that RQ5 asks about. Its weaknesses (thin oracles, MI-only maintainability, single-turn generation, contamination) are exactly what a new study should improve. Its finding that one-shot repair and planning lowered non-functional quality (p. 8) is a direct warning for vibe-coding workflows that iterate on failures.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | In single-pass generation of 38 real Python applications, no LLM exceeds 45% functional test pass rate (averages 33.98% standard, 30.23% thinking). | p. 5 | V | weak (preprint, single study, ~11 tests/task) |
| RQ2 | Most failures (82.8%) occur after the code runs (requirement–implementation mismatch or runtime instability); only 17.2% are executability/dependency failures. | p. 7 | V | weak (coding procedure not reported) |
| RQ3 | Reference-normalised maintainability (MI lower bound) averages ~31–33%, the weakest non-functional dimension, while security averages 85–87%. | p. 6 | V | weak (single MI proxy; parity with reference scores only 0.5) |
| RQ3 | On GPT-5.2, self-repair, environment repair and planning each lowered the aggregate non-functional score (46.1–49.9% vs 57.1% baseline) without raising functional correctness. | p. 8 | V | weak (one model, one-shot strategies) |
| RQ4 | Tests are kept only if they pass on the pinned reference repository; functional suites caught 76/76 injected defects. | p. 2; p. 5 | V | weak (only 2 defects/task, method not described) |
| RQ4 | Functional scores had zero variance across 5 reruns; the NF ranking is robust to weighting choices (Spearman ≥0.90) except rank-based aggregation (0.64). | p. 7; p. 10 | V | weak |
| RQ4 | Authors cannot rule out pretraining exposure to the public reference repositories. | p. 2 | A | weak |
| RQ4 | Giving the reference's module/package surface raised one task's functional score from 0.17 to 0.67, so interface hints strongly affect measured fidelity. | p. 4 | V | weak (single example) |
| RQ5 | Authors propose quality-aware generation and multi-turn/agentic evaluation under the same benchmark as next steps. | p. 5; p. 10 | A | weak |

## 14. Key quotes
> "no model exceeds a 45% functional score" (p. 1)

> "we do not claim that pretraining exposure can be fully ruled out" (p. 2)

> "MI does not capture all aspects of maintainability, such as naming quality or architectural clarity" (p. 3)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–12), including all tables and the reference list. Figure 4 (failure shares per category) is garbled in the text layer, so only the combined 82.8%/17.2% split stated in the text is used. Figure 6 (strategy workflows) was only skimmed.
- Uncertainties:
  - whether a "rerun" means regenerating the code or re-evaluating existing generations;
  - how the 446 repositories were selected;
  - which static-analysis tools were used;
  - decoding settings (greedy decoding is stated only in the abstract).
  
  Model names such as GPT-5.2 and Gemini-3-Pro-Preview are taken as reported.
- Strength ratings follow research-standards §5: a preprint without replication is rated weak, although the design (pinned references, reference-validated tests, repeated runs) would support "moderate" if published.
