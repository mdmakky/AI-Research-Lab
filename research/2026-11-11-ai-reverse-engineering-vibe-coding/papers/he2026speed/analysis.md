---
key: he2026speed
status: complete
evidence_basis: full-text
design: quasi-experimental causal study; staggered difference-in-differences (Borusyak imputation estimator) with propensity-score-matched controls, plus Arellano-Bond dynamic panel GMM
dataset: 806 GitHub repos (>=10 stars) that committed Cursor config files, Aug 2024-Mar 2025 adoptions; matched never-adopter controls; monthly panel Jan 2024-Aug 2025
sample_size: 806 treated repos (801 in final panel) + 1,172-1,380 matched control repos; 21,699 repo-months
metrics: commits, lines added; SonarQube static-analysis warnings, cognitive complexity, duplicated-line density (all log-transformed, monthly)
main_finding: Cursor adoption gives a transient velocity spike (+281% lines added month 1) but persistent +30% static-analysis warnings and +41.6% code complexity, which then slow velocity.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Speed at the Cost of Quality

- Authors: He, Hao; Miller, Courtney; Agarwal, Shyam; Kästner, Christian; Vasilescu, Bogdan
- Year / venue: 2026, Proceedings of the 23rd International Conference on Mining Software Repositories (published)
- DOI: 10.1145/3793302.3793349 · URL: https://doi.org/10.1145/3793302.3793349
- Source text: `fulltext.txt` (page refs = PDF page index). Our PDF is arXiv v3 (arXiv:2511.04427v3, 26 Jan 2026, stamp on p. 1) carrying the MSR '26 header, not the ACM Digital Library copy, so page refs use arXiv pagination. It includes Appendices A–D; the paper says the appendix is only in the arXiv version (p. 11).

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
Estimate the causal effect of adopting an LLM agent assistant (Cursor) on project-level development velocity and software quality in open-source GitHub projects, and test how velocity and quality interact over time [A] (p. 1, p. 2).

## 2. Research questions / hypotheses
- Single RQ: "How does the adoption of LLM agent assistants impact project-level development velocity and code quality?" [V] (p. 2).
- No formal hypotheses are stated. The panel-GMM part tests four causal paths: lines added → warnings, lines added → complexity, complexity → next-month lines added, warnings → next-month lines added (Equation 7) [V] (p. 6).

## 3. Methodology
- Research design: observational, quasi-experimental difference-in-differences (DiD) with staggered adoption. *DiD* compares how an outcome changes over time in adopters versus non-adopters, so that trends affecting both groups cancel out. Cursor adopters are compared with never-adopters matched by propensity score (1:3 nearest neighbour, same primary language) [V] (p. 4, p. 5). Main estimator: Borusyak et al. imputation estimator, chosen because two-way fixed effects (TWFE) can be biased under staggered adoption with heterogeneous effects [V] (p. 6). Pre-trend (placebo) tests use heteroscedasticity- and cluster-robust Wald tests on h = −6..−2; h = −1 is dropped for anticipation [V] (p. 6). Velocity–quality interactions are tested with Arellano-Bond dynamic panel GMM (two-step, first-difference, repository + month fixed effects, lags 2–3 as instruments) [V] (p. 6, p. 8).
- Approach / model / intervention: "treatment" = first commit touching `.cursorrules` or `.cursor` files, used as a proxy for adopting the modern (Composer/agentic) Cursor client [V] (p. 2, p. 4). Treatment is intent-to-treat: actual usage intensity, LLM backend and Cursor version are unknown [V] (p. 7).
- Baselines or comparison conditions: matched never-adopter repositories plus not-yet-treated adopters. The comparison is against "state-of-the-practice" (controls may use Copilot or ChatGPT without visible traces), not against no AI use [V] (p. 7). Robustness: TWFE and Callaway & Sant'Anna estimators (Appendix B) and subsets by usage intensity, activity level, other AI tools, language and adoption cohort (Section 4.3, Appendix C) [V] (p. 9, p. 15, p. 16, p. 17).

## 4. Dataset and sample
- Data source(s): GitHub code search API (Cursor config files), GHArchive monthly event data (matching covariates), GitHub API (primary language), local SonarQube Community server (outcomes and lines of code) [V] (p. 4, p. 5).
- Sample size (N) and unit: unit = repository-month. 23,308 Cursor files in 3,306 non-fork repos were found; the ≥10-star filter leaves 806 adopting repos [V] (p. 4). The text states 1,380 matched controls [V] (p. 2); Table 7 "Original" setting lists 801 treatment repos, 1,172 control repos, 21,699 observations and 4,481 post-treatment observations [V] (p. 17). GMM models use 14,755 observations [V] (p. 8). Primary languages: TypeScript 366, Python 118, JavaScript 60, Go 36, Rust 24 repos [V] (p. 4).
- Sampling / selection method: all discoverable repos with Cursor config files and ≥10 stars (threshold cited as 97% precision for engineered projects); adoption dates Jan 2024–Mar 2025; still available Aug 2025 [V] (p. 4). Matching pool: all GitHub repos with ≥10 stars, ~760k–820k candidates per monthly cohort, at most 10,000 sampled per cohort; logistic propensity models with 6 monthly lags plus cumulative history; AUC 0.83–0.91, McFadden pseudo-R² 0.14–0.27 [V] (p. 4, p. 14). Balance: all normalised differences |ND| < 0.25 ("acceptable"), but raw mean gaps remain large (e.g. pull requests 1,075.58 vs 266.03; age 496 vs 681 days, ND −0.207) [V] (p. 14). No power analysis reported.
- Data availability (public? link?): replication package at https://doi.org/10.5281/zenodo.18368661 [V] (p. 11).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: monthly outcomes and covariates Jan 2024–Aug 2025, giving ≥6 months pre/post for treated repos; unbalanced panel [V] (p. 5). Time-varying covariates: lines of code, age, contributors, stars, issues opened (issue comments dropped for collinearity, ρ > 0.7) [V] (p. 5). All outcomes log-transformed; ATT read as 100(e^ATT − 1)% [V] (p. 7). SonarQube version and quality profile (rule set): not reported.
- Code availability: replication package on Zenodo (p. 11); its contents are not described in the paper.

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - Commits per month; lines added per month — development velocity; common productivity proxies with moderate-to-strong correlation with perceived productivity [V] (p. 5).
  - Static analysis warnings — total count of SonarQube reliability, maintainability and security issues; framed as an estimate of review effort because static analysis has false positives [V] (p. 5).
  - Duplicated line density — % duplicated lines (SonarQube; usually ≥10 consecutive statements or 100 tokens) [V] (p. 5).
  - Code complexity — total SonarQube cognitive complexity of the codebase; chosen as better aligned with understandability than cyclomatic complexity [V] (p. 5).
  - The three quality metrics were chosen from a technical-debt perspective because they can be computed at scale from version control [A] (p. 5).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): ATT with standard errors and ± ranges on the % change; significance at 0.05/0.01/0.001; robust Wald pre-trend tests; GMM with Sargan (instrument validity) and AR(1)/AR(2) tests [V] (p. 7, p. 8). No correction for multiple comparisons across 5 outcomes × many subsets is reported.

## 7. Key findings
1. Main DiD (Borusyak): lines added +28.58% (±13.7%, p < 0.05); commits +2.63% (n.s.); static analysis warnings +30.26% (±6.66%, p < 0.001); duplicated line density +7.03% (n.s.); code complexity +41.64% (±7.62%, p < 0.001) — [V] (p. 7). Significance stars were read from the PDF image; the text extraction attaches *** to every cell.
2. The velocity gain is transient: only months 1–2 are significant; commits +55.4% / +14.5% and lines added +281.3% / +48.4% in months 1 / 2 — [V] (p. 8, Figure 3).
3. Quality effects persist to month 6 for warnings and complexity; all outcomes pass the pre-trend tests — [V] (p. 8, Figure 3).
4. Panel GMM: velocity does not significantly raise warnings or complexity; Cursor has no significant direct effect on warnings (−0.011) once codebase size is controlled; Cursor still raises complexity (0.086, p < 0.01, reported as a "9% baseline increase") — [V] (p. 8, Table 3).
5. Panel GMM: a 100% increase in complexity or warnings goes with a 64.5% / 50.3% decrease in next-month lines added; Cursor gives a 1.84x baseline increase in lines added; ~3x complexity or ~5x warnings would cancel the gain — [V] (p. 8).
6. Robustness: quality effects are stronger in high-usage subsets (contributors who touched Cursor files made ≥80% of commits; months with config edits); they persist in very active repos and with/without traces of other AI tools (382 treated repos show other tools, 345 of them Copilot) — [V] (p. 9, p. 10, Figure 4).
7. Estimator sensitivity: TWFE agrees (warnings +18.48%, complexity +26.04%, both p < 0.001), but Callaway & Sant'Anna gives negative, non-significant quality estimates (warnings −10.49%, complexity −3.80%); the authors conclude the quality findings need caution — [V] (p. 16, Table 6).
8. Descriptive warning analysis (convenience sample, 195,010 warnings from 933 rules, 20-category taxonomy): 16/20 categories rise post-adoption; largest Naming Conventions +21.32, Code Hygiene +16.15, Code Complexity +15.34, Code Style +14.76 new warnings per repo per month; Logic Error +2.09, Security +1.98; API Usage −4.35 — [V] (p. 18, Table 8).
9. The authors interpret that much of the warning increase runs through velocity → codebase size → technical debt, so Cursor "may not necessarily introduce more code quality issues than non-adopting projects moving with the same velocity", whereas complexity is inherently higher in Cursor code — [A] (p. 10).

## 8. Limitations stated by the authors
- [A] Treatment covers only repos that commit Cursor config files; possible selection bias in either direction (p. 7).
- [A] Usage intensity and persistence unknown; estimates are intent-to-treat (p. 7).
- [A] Cursor version and LLM backend unknown (argued to raise external validity) (p. 7).
- [A] Matching is imperfect; unobserved confounders (expertise, team practices, culture) are untestable (p. 7, p. 14).
- [A] Contamination by other AI tools in both groups; the effect is relative to current practice, not to no AI (p. 7).
- [A] External validity: other agents, proprietary projects, languages beyond JS/TS/Python; fast-changing tools (p. 7); Java, C/C++, Rust insufficiently covered (p. 16).
- [A] Quality metrics may not capture the multi-dimensional nature of quality; complexity metrics were designed for human-written code (p. 11).
- [A] Estimators disagree for quality outcomes; many cohorts have fewer than 100 repos (p. 16).
- [A] Composer use and agentic use cannot be separated (p. 2, p. 17).
- [A] The warning-category analysis is a convenience sample and descriptive only (p. 18).

## 9. Limitations we identified
- [I] Internal inconsistencies in reported numbers: the discussion cites a "25.1%" complexity increase attributed to Table 2 (p. 10) and a "25%" increase attributed to Table 3 (p. 11), while Table 2 reports +41.64% and Table 3 a 0.086 coefficient (~9%) (p. 7, p. 8). Probably left over from an earlier version; use the table values.
- [I] Sample counts differ between text and tables: 806 treated and 1,380 controls (p. 2, p. 4) versus 801 treated and 1,172 controls in Table 7 (p. 17). The paper does not explain the difference. Also, with 1:3 nearest-neighbour matching (p. 5), 806 treated repos would need up to 2,418 controls, yet only 1,380 distinct controls are reported (p. 2), so controls were shared across treated units or cohorts. The paper hints at matching with replacement ("many adopters matched the same control during 1:1 matching", p. 5) but does not state it, and does not say how reused controls are weighted or how this affects the independence of observations.
- [I] Warnings and complexity are repository totals, so they scale with codebase size; in the GMM, lines of code absorbs most variance and removes the direct Cursor effect on warnings (p. 8). "+30% warnings" is therefore mainly "more code", not a higher warning density. For RQ3 the per-code quality signal is complexity, not warnings. Based on Table 3 (p. 8).
- [I] The headline quality result depends on the estimator (Borusyak/TWFE positive; Callaway–Sant'Anna negative and n.s.) (p. 16); the abstract does not mention this.
- [I] Cursor-generated code is not identified at file or line level; quality changes are attributed to whole repositories, including human-written code.
- [I] The warning taxonomy was produced by the first author together with Claude Opus 4.5 (p. 18); no inter-rater or validation check is reported.
- [I] No functional-correctness or test outcome is measured; quality is static analysis only.

## 10. Threats to validity
- Internal (confounds, leakage, selection): selection into treatment by committing config files; ITT dilution; unobserved confounders despite matching and fixed effects; anticipation handled by dropping h = −1 (p. 6, p. 7). Pre-trend tests pass for the main estimator (p. 8). Balance acceptable but imperfect (p. 14).
- External (generalisability of sample/context): open-source, ≥10-star GitHub repos, mostly TypeScript/Python/JavaScript; one tool (Cursor); mid-2024 to mid-2025 (p. 4, p. 7, p. 11). [I] No enterprise or reconstruction setting.
- Construct (do metrics measure the concept?): lines added and commits are rough velocity proxies; SonarQube warnings include false positives and are framed as review effort; cognitive complexity is a whole-codebase sum (p. 5, p. 11). [I] Maintainability is not measured directly (e.g. change effort by later developers).
- Statistical conclusion (power, multiple comparisons, variance): no power analysis; many outcome × subset comparisons without correction; standard errors and ± ranges reported; estimator sensitivity for quality outcomes (p. 7, p. 16).
- Reproducibility (data/code/setup reported?): Zenodo replication package (p. 11); estimators and model specifications given as equations (p. 4, p. 6, p. 14, p. 15); SonarQube version/rule set not reported.

## 11. Future research directions
- Stated by authors [A]: replicate with other and newer LLM coding tools (p. 7); test whether transient gains and proportional debt generalise to enterprise settings (p. 11); study why LLMs produce overly complex code and develop readability-aware fine-tuning or simplification passes (p. 11); study duplication under heavy AI use (p. 10); study other programming languages (p. 16); find the causes of warning-category increases (p. 18); design tools with quality assurance as a first-class feature, e.g. self-throttling (p. 11).
- Suggested by us [I]: measure quality per line or per file for AI-attributed changes instead of repository totals; pair static-analysis metrics with a downstream maintainability task (as borg2026echoes does) to test whether higher cognitive complexity actually slows later evolution.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ3 (main), RQ4, RQ5.
- How it informs our work [I]: the strongest real-world causal evidence in our set that agentic, vibe-coding-style development raises code complexity and static-analysis warnings at project level. It does not study reconstruction from UI/behaviour, so it informs RQ3 by analogy only. Methodologically it shows the metric choices (SonarQube warnings, cognitive complexity, duplication) and why size normalisation and estimator robustness matter, which a reconstruction study should copy (RQ4/RQ5).

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Cursor adoption raises SonarQube static-analysis warnings by +30.26% (p<0.001) relative to matched controls (Borusyak DiD) | 7 | V | moderate |
| RQ3 | Cursor adoption raises total cognitive complexity by +41.64% (p<0.001), persisting 6 months; still significant (0.086, p<0.01) after controlling for codebase size in GMM | 7, 8 | V | moderate |
| RQ3 | Duplicated line density shows no significant change after adoption (+7.03%, n.s.) | 7 | V | moderate |
| RQ3 | With codebase size controlled, Cursor has no significant direct effect on warnings (GMM); the warning rise runs mainly through more code | 8 | V | moderate |
| RQ3 | Higher complexity and warnings predict lower next-month lines added (−64.5% / −50.3% per 100% increase) | 8 | V | moderate |
| RQ3 | Velocity gain is transient: lines added +281.3% month 1, +48.4% month 2, then n.s. | 8 | V | moderate |
| RQ4 | Quality results are estimator-sensitive: Callaway–Sant'Anna gives negative, n.s. estimates for warnings (−10.49%) and complexity (−3.80%) | 16 | V | moderate |
| RQ4 | Project-level quality measured with SonarQube warnings, cognitive complexity and duplicated-line density; treatment proxied by committed .cursorrules files (intent-to-treat) | 5, 7 | V | moderate |
| RQ5 | Authors call for enterprise replications, other tools/languages, and research on why LLMs generate overly complex code | 11, 16 | A | moderate |

## 14. Key quotes
> "our main estimates represent intent-to-treat (ITT) effects" (p. 7)

> "Cursor adoption still leads to significant increases in code complexity, even when models control for project velocity dynamics" (p. 2)

> "the findings around code quality outcomes should be interpreted with appropriate caution" (p. 16)

## Analyst notes
- Reading coverage: all 19 PDF pages read; references skimmed; Appendices A (matching), B (alternative estimators), C (robustness), D (SonarQube warning taxonomy) read in full. Tables 2, 3 and 6 were checked on the PDF image because pdftotext attaches *** to every cell.
- Uncertainties: which N is final (806/1,380 vs 801/1,172); the 25%/25.1% complexity figures in the discussion conflict with the tables; SonarQube version and quality profile not reported. Venue MSR 2026 (peer-reviewed); our PDF is arXiv v3 with appendices, so appendix page refs have no counterpart in the proceedings. Funding: NSF, Google research awards, Google Cloud credits, Digital Infrastructure Fund (p. 11); no conflict bearing on Cursor apparent.
- Review fixes applied 2026-11-12 (critical-review-batch-a): `main_finding` now uses the paper's 41.6% (was rounded to 42%); added the 1:3-matching vs 1,380-controls point (modified: the paper hints at shared controls on p. 5, so we say "not stated" rather than "not explained at all"). Note for synthesis: ehsani2026faster reports this study's +30%/+41% second-hand (its ref [90]); count the effect once, from this paper.
