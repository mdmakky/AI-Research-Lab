---
key: liu2026benchmarking
status: ready
evidence_basis: full-text
design: benchmark construction (requirements and BDD tests derived from existing open-source web apps) + comparative evaluation of 6 frameworks x 6 LLMs, 3 runs each; human failure analysis
dataset: E2EDev, 46 small front-end web apps from GitHub (>500 stars) with 244 fine-grained requirements and 703 executable Gherkin/Behave (Selenium) tests
sample_size: 46 projects x 36 framework-backbone settings x 3 runs; human failure analysis on 360 generated projects; test-quality audit on 100 tests by 10 experts
metrics: Req.Acc (share of requirements with all tests passing), Test.Acc, Balanced score (0.6/0.4), Soft Req.Acc, cost, CO2, duration
main_finding: Best setting (GPT-Engineer + Claude-Haiku 4.5) fully satisfies 53.75% of requirements; multi-agent frameworks rarely beat a plain prompted LLM and cost more.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# E2EDev: Benchmarking Large Language Models in End-to-End Software Development Task

- Authors: Liu, Jingyao; Huang, Chen; Guan, Zhizhao; Lei, Wenqiang; Deng, Yang
- Year / venue: 2026, Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (published)
- DOI: 10.18653/v1/2026.acl-long.1618 · URL: https://doi.org/10.18653/v1/2026.acl-long.1618
- Source text: `fulltext.txt` (page refs = PDF page index)
- Identity note: `metadata.json` lists identity as "probable"; PDF page 1 shows the exact title, the five authors and the ACL 2026 proceedings footer (pages 35032–35068), so identity is confirmed (p. 1). The PDF is the ACL Anthology version.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] To provide an end-to-end software development (E2ESD) benchmark with fine-grained user requirements and executable behaviour-driven (BDD) tests, replacing the vague specifications and human or heuristic scoring of earlier benchmarks (SoftwareDev, SRDD), and to use it to assess LLM-based development frameworks (p. 1–2).

## 2. Research questions / hypotheses
No formal RQs or hypotheses. The work addresses two stated problems of prior benchmarks: coarse-grained requirement specifications and unreliable evaluation protocols (p. 1). [A] Analyses ask how effective and efficient existing frameworks are, whether agentic frameworks improve on plain LLMs, and why they fail (p. 5–8). [V]

## 3. Methodology
- Research design: benchmark construction from existing open-source web apps with a human-in-the-loop multi-agent annotation pipeline (HITL-MAA); comparative evaluation of 6 framework types across 6 LLM backbones with 3 runs per task; human failure-mode analysis (p. 3–8). [V]
- Approach / model / intervention: generation side — Vanilla LLM, GPT-Engineer (single agent), Self-Collaboration, MapCoder, ChatDev, MetaGPT (multi-agent); OpenHands and SWE-Agent as reference systems (p. 5, p. 19–20). [V] Python-oriented frameworks were adapted to HTML/CSS/JS by changing system prompts (p. 19–20). [V]
- Benchmark construction (reverse-engineering direction): (1) GPT-4o agents insert `data-testid` attributes into the original source as stable DOM anchors (p. 3, p. 13); (2) a Code Analyzer Agent and Requirement Extractor Agent derive user-facing requirements from the source code, reviewed by human supervisors who check them against the running app (p. 4, p. 14); (3) a Test Case Generation Agent writes Gherkin Given–When–Then scenarios, reviewed and extended by five software-testing experts (p. 4); (4) a Test Automation Engineer Agent writes Python/Selenium step implementations, self-corrected by a dry-run verifier (max 3 iterations) and a test runner (max 6 iterations), with human fallback (p. 4–5, p. 13). [V] All tests pass on the original projects: "Validation on the generated dataset achieved a 100% pass rate across all executable tests" (p. 5). [V]
- How functional correctness is tested: the generated project is run in Chrome via Selenium and the Behave framework executes the Gherkin scenarios, giving deterministic pass/fail per test (p. 5, p. 29–30). [V] No LLM judge is used in scoring. [V] (p. 5) Generated apps must expose the same `data-testid` names, which are given in the prompt (p. 16–17). [V]
- Baselines or comparison conditions: Vanilla LLM is the reference baseline in all tables (p. 6). [V] HumanEval / HumanEval-ET runs of the same frameworks are used as a function-level contrast (p. 27). [V]

## 4. Dataset and sample
- Data source(s): GitHub repositories found with keywords such as "mini project", "web application", "H5", over 500 stars (p. 12). [V]
- Sample size (N) and unit: 46 projects, 244 requirements (2–11 per project, mean 5.3), 703 BDD tests (mean 2.9 per requirement, 15.3 per project) (p. 3, Table 2). [V] Project types include calculators, CRUD/form apps and mini games; about one-quarter use local storage and another quarter external APIs (p. 18). [V]
- Sampling / selection method: five annotators screened candidates for executability, functionality and suitability (testable in about five minutes, no database or API-key setup); pilot Fleiss' kappa 0.47 → 0.83 after guideline refinement, 0.79 on an overlap subset; 46 of "over 158" shortlisted projects kept (p. 12–13). [V] The text describes the overlap subset as "10% of the full dataset (158 projects)" (p. 12) and then "over 158 initially shortlisted" (p. 13); the counts are inconsistent.
- Data availability (public? link?): code on GitHub and data on Hugging Face, CC-BY 4.0 data / MIT code (p. 9–10). [A] (links not checked by us)

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: backbones Claude-Haiku 4.5, GPT-4o, GPT-4o-mini, Qwen2.5-7B-Instruct, Qwen2.5-72B-Instruct ("Qwen-70B"), Qwen2.5-Max (p. 5, p. 19). [V] Six frameworks evaluated on all six backbones; OpenHands and SWE-Agent only on Claude-Haiku 4.5 and GPT-4o, OpenHands restricted to one execution without human interaction (p. 20, p. 22). [V] Effectiveness averaged over three runs; efficiency from a single run (p. 5, p. 20). [V] Decoding settings (temperature, seeds), maximum budgets per framework: not reported (ChatDev's 20-turn cap is mentioned, p. 24). The prompt contains the project summary, external resources and the refined requirements with `data-testid` names (p. 13, p. 16). [V]
- Code availability: released (p. 9). [A]
- Evaluator-reliability evidence:
  - Test-quality audit: 10 experts (5 original + 5 external) blind-reviewed a stratified random sample of 100 tests; Fleiss' kappa 0.81 (p. 14). [V]
  - Gold-checker protocol: four annotators validate each requirement/test, a senior "Gold Checker" consolidates only when Fleiss' kappa on equivalence, completeness and correctness exceeds 0.7 (p. 14). [V]
  - Human vs automatic: in the failure-analysis study "Cohen's Kappa" was 0.86 among human annotators and 0.74 between human and automatic evaluation (p. 22). [V] Which units were compared (requirements of the 360 projects?) and how many items were double-annotated are not reported.
  - Manual-only annotation pilot (no pipeline) gave Fleiss' kappa 0.23 on 14 test cases and ~80% executable tests (p. 15, p. 17, Table 5). [V]

## 6. Evaluation metrics
- Req.Acc — fraction of requirements whose associated tests all pass (p. 5, p. 20). [V]
- Test.Acc — fraction of all tests passing (p. 5, p. 20). [V]
- Balanced score — 0.6 × Req.Acc + 0.4 × Test.Acc; weights chosen by the authors' "intuition" (p. 20). [V]/[A]
- Soft Req.Acc — allows partial requirement fulfilment (p. 5, p. 25); its exact definition is not given in the text we read. [V]
- Cost (USD from token prices), carbon footprint (estimated with A100 assumptions), duration (p. 5, p. 21). [V]
- Statistical testing (tests used, significance, effect sizes, confidence intervals): mean ± standard deviation over three runs (p. 6, p. 20). No significance tests or confidence intervals. [V]

## 7. Key findings
1. Best effectiveness: GPT-Engineer + Claude-Haiku 4.5, Req.Acc 53.75 ± 0.43, Test.Acc 69.41 ± 1.07 (p. 6, Table 3). [V] Excluding MetaGPT, all Claude-Haiku 4.5, GPT-4o and Qwen-Max settings fall between 42.30 and 53.75 Req.Acc (p. 6). [V] The authors summarise: "achieving only 30%–50% Req. Acc." and no model exceeds 60% (p. 5). [A]
2. Soft Req.Acc exceeds Req.Acc by about 25–33 points in most settings (e.g. GPT-Engineer + Claude-Haiku 4.5: 0.5402 vs 0.7991), meaning partially working requirements are common (p. 25, Table 10). [V] The authors attribute this to failing edge cases and fine details (p. 6). [A]
3. Agentic frameworks do not reliably beat a plain prompted LLM: e.g. GPT-4o-mini Vanilla 44.82 Req.Acc vs ChatDev 33.16 and MapCoder 41.30; GPT-4o Vanilla 45.95 vs ChatDev 42.71 (p. 6, Table 3). [V] Multi-agent frameworks cost up to ~12x more and take longer (e.g. GPT-4o ChatDev $0.1947 vs Vanilla $0.0160) (p. 6). [V]
4. MetaGPT almost completely fails (0.00–5.39 Req.Acc), attributed to inter-agent communication breakdowns: 44% of its failures are code inconsistency (missing files, syntax errors) (p. 6, p. 8). [V]/[A]
5. The same frameworks reach 71–91% Pass@1 on HumanEval (except MetaGPT), far above their E2EDev scores (p. 27, Table 12). [V]
6. OpenHands and SWE-Agent underperform the Vanilla baseline (Claude-Haiku 4.5: 43.45 and 44.73 vs 48.69 Req.Acc) (p. 23, Table 8). [V] The authors explain this by task mismatch with their original design (p. 22). [A]
7. Human failure analysis of 360 projects: four failure types (code inconsistency, requirement missing, requirement misaligned, detail mismatch); Vanilla LLM and ChatDev show the most missing requirements; Vanilla shows the fewest detail mismatches (p. 7–8, p. 23). [V]/[A]
8. The semi-automated pipeline needed human refinement for ~20% of requirements, ~50% of test cases and <20% of test scripts, at ~3.5 hours and ~$0.48 GPT-4o cost per project (p. 15–17). [V]

## 8. Limitations stated by the authors
- [A] Small scale: 46 projects, because building repository-level executable tests is costly (p. 9, p. 30).
- [A] Web applications only; CI/CD workflows and deep backend inspection excluded for reproducibility (p. 9).
- [A] Pre-defined test scripts cannot be reused easily across methods because generated code structures vary (p. 30) — addressed by the `data-testid` anchors (p. 3).
- [A] OpenHands and SWE-Agent target different task settings, so direct comparison is "not conceptually equivalent" (p. 22).

## 9. Limitations we identified
- [I] Tests are coupled to `data-testid` DOM anchors from the original app, and the prompt tells the model these IDs (p. 3, p. 16–17). A functionally correct app that names elements differently fails. Scores therefore mix behavioural correctness with instruction-following of naming conventions; how many failures are anchor mismatches is not reported.
- [I] The "human vs automatic" Cohen's kappa of 0.74 (p. 22) is the only direct validation of the automated oracle against human judgement, but its sample, unit and procedure are not described; Cohen's kappa is used although five annotators are involved, and 295 instances were "evenly distributed" (single-labelled) with only 5 shared calibration examples (p. 21). The kappa 0.86 among humans may therefore rest on very few items.
- [I] Inconsistent reporting: "four domain experts" in the main text (p. 7) vs "5 professional annotators" in the appendix (p. 21); "30 different models (6 backbones × 6 frameworks)" (p. 21) where 6 × 6 = 36; "10% of the full dataset (158 projects)" (p. 12) vs 158 shortlisted (p. 13).
- [I] Possible contamination: source projects are popular public GitHub repositories (> 500 stars) whose reference implementation is linked (p. 12, p. 17); models may have seen them. Not discussed.
- [I] Backbones are small or older models (Claude-Haiku 4.5, GPT-4o, Qwen2.5); no frontier coding models, so absolute ceilings are uncertain.
- [I] Projects are small, front-end-only apps that run from a local file without setup (p. 12, p. 17); backend, persistence beyond local storage, auth and deployment are out of scope.
- [I] Three runs give standard deviations, but some settings report ±0.00 (e.g. Qwen-70B and Qwen-7B Vanilla, p. 6), suggesting deterministic decoding for some backbones; decoding settings are not reported.
- [I] Requirements are detailed and implementation-near (e.g. exact class names and 150 ms timing, p. 16–17), unlike vague vibe-coding prompts; results speak to specification-following, not intent inference.
- [I] No code-quality or maintainability measures; "code inconsistency" in the failure analysis is a functional-defect category, not a quality metric (p. 23).

## 10. Threats to validity
- Internal (confounds, leakage, selection): framework adaptations via system-prompt edits (p. 19–20) may disadvantage Python-oriented frameworks [I]; GPT-4o built the annotations and is also evaluated (p. 13, p. 16) [V]; anchor naming in prompts couples test outcome to instruction following [I].
- External (generalisability of sample/context): 46 small HTML/CSS/JS apps from GitHub (p. 3, p. 12) [V]; authors argue web is a "lower bound" for harder domains (p. 9) [A].
- Construct (do metrics measure the concept?): BDD tests validated on the original implementation (100% pass, p. 5) and audited by experts (κ = 0.81, p. 14) [V]; Req.Acc is strict (all tests must pass) and Balanced-score weights are arbitrary (p. 20) [V/I].
- Statistical conclusion (power, multiple comparisons, variance): 3 runs with SD; no significance tests; many framework/backbone comparisons uncorrected (p. 6) [V/I].
- Reproducibility (data/code/setup reported?): code, data, prompts (Appendix G) and metric formulas released/printed (p. 9, p. 20–21, p. 31–37) [V]; decoding parameters not reported [V].

## 11. Future research directions
- Stated by authors [A]: design "effective, reliable, and cost-efficient E2ESD solutions" (p. 9); expand E2EDev and maintain a public leaderboard (p. 9); reduce frameworks' reliance on strong backbones (p. 7); more robust stopping/exit strategies for multi-agent frameworks (p. 24).
- Suggested by us [I]: replace source-derived DOM anchors with anchor-free behavioural checks (e.g. browser-agent or accessibility-tree matching) so reconstructions are not penalised for naming; report human–oracle agreement per requirement with sample sizes; add code-quality metrics; test frontier coding agents.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (single- vs multi-agent generation frameworks for whole apps), RQ2 (functional fidelity measured by executable BDD tests derived from the original apps), RQ4 (test-oracle construction, kappa-based annotation quality, human–automatic agreement), RQ5 (no quality/maintainability; anchor-coupling issue).
- How it informs our work [I]: E2EDev is the closest benchmark design to reverse engineering in our set: it starts from existing applications, extracts requirements from their code and observed behaviour, writes behavioural tests that pass on the original, and asks models to rebuild the app from those requirements. This gives a concrete template for measuring functional fidelity of a rebuild against an original. Its weak point for our purpose is that tests depend on DOM IDs copied from the original source, which a true black-box reconstruction would not have. It also shows that agent orchestration adds cost without reliably adding fidelity.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | Best setting (GPT-Engineer + Claude-Haiku 4.5) fully satisfies 53.75% of requirements (Test.Acc 69.41%) when rebuilding 46 small web apps from fine-grained requirements | 6 | V | moderate |
| RQ2 | Partial fulfilment is common: Soft Req.Acc exceeds strict Req.Acc by ~25–33 points across settings | 25 | V | moderate |
| RQ1 | Multi-agent frameworks do not reliably beat a plain prompted LLM and cost up to ~12x more; MetaGPT nearly always fails (0–5.4% Req.Acc) | 6 | V | moderate |
| RQ1 | Same frameworks score 71–91% Pass@1 on HumanEval but ~10–54% Req.Acc on E2EDev | 27 | V | moderate |
| RQ4 | Functional oracle = Gherkin/Behave tests with Selenium, derived from the original app's code via LLM agents plus human review, passing 100% on the original projects; no LLM judge | 5 | V | moderate |
| RQ4 | Test-quality audit by 10 experts on 100 sampled tests gives Fleiss' kappa 0.81; a manual-only annotation pilot gave kappa 0.23 | 14 | V | moderate |
| RQ4 | Human vs automatic evaluation agreement Cohen's kappa 0.74 (human–human 0.86), but sample and unit not described | 22 | V | weak |
| RQ5 | Tests depend on `data-testid` anchors taken from the original source and supplied in the prompt, so a black-box rebuild could fail on naming rather than behaviour | 16 | I | weak |

## 14. Key quotes
> "Validation on the generated dataset achieved a 100% pass rate across all executable tests" (p. 5)
> "We report a strong agreement score of 0.86 among human annotators and 0.74 between human and automatic evaluation" (p. 22)
> "Agentic frameworks do not consistently improve the effectiveness of base LLMs." (p. 6)

## Analyst notes
- Reading coverage: main text p. 1–9, references p. 10–12 skimmed, appendices A–F p. 12–30 read; Appendix G prompts (p. 31–37) skimmed. Figures 1–9 are images; Figure 4–6 values not extracted, only text statements used. Soft Req.Acc definition not found in the text layer.
- Uncertainties: count inconsistencies listed in §9; the unit of the human–automatic kappa; whether OpenHands numbers (no SD) come from one run; decoding settings. Table 2 "Prompt Len." unit not stated (p. 3).
