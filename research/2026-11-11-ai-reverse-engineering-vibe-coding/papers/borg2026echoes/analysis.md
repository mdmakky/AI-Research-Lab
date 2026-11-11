---
key: borg2026echoes
status: ready
evidence_basis: full-text
design: preregistered two-phase controlled experiment; Phase 1 observational (AI vs no-AI, assigned by preference), Phase 2 RCT (manual evolution of AI vs non-AI code); frequentist + Bayesian causal analysis
dataset: 2 KLoC Java/Spring Boot web app (RecipeFinder) with two feature tasks; 449 pre-screened volunteers, 92% professional developers
sample_size: 151 valid solutions; Phase 1 n=76 (39 AI / 37 no-AI); Phase 2 RCT n=75 (40 treatment / 35 control)
metrics: completion time; CodeScene CodeHealth (customised); JaCoCo line coverage; SPACE-based perceived productivity; plus PMD, RefactoringMiner, smell deltas (Phase 1)
main_finding: Evolving AI-assisted code showed no significant difference in time, CodeHealth, coverage or perceived productivity; at most a small, uncertain CodeHealth gain for habitual AI users.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Echoes of AI: Investigating the downstream effects of AI assistants on software maintainability

- Authors: Borg, Markus; Hewett, Dave; Hagatulah, Nadim; Couderc, Noric; Söderberg, Emma; Graham, Donald
- Year / venue: 2026, Empirical Software Engineering (published)
- DOI: 10.1007/s10664-026-10889-1 · URL: https://doi.org/10.1007/s10664-026-10889-1
- Further authors (from metadata.json): Kini, Uttam; Farley, Dave
- Source text: `fulltext.txt` (page refs = PDF page index). Our PDF is the Springer open-access version (78 pages); PDF page N = printed "Page N of 78".

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
Investigate whether co-developing code with AI assistants affects software maintainability, defined as how easily *another* developer can later evolve that code [A] (p. 1, p. 2).

## 2. Research questions / hypotheses
- RQ1: Do developers manually evolve code that has been co-developed with AI assistants more efficiently? RQ2: Does code co-developed with AI assistants result in higher quality upon manual evolution? [V] (p. 9).
- Four preregistered null hypotheses (non-directional alternatives): no difference in completion time (H0 1), CodeHealth (H0 2), test coverage (H0 3), perceived productivity (H0 4) between developers evolving AI-assisted vs non-assisted code [V] (p. 14).
- Note the "RQ1/RQ2" above are the paper's own RQs, not our project RQs.

## 3. Methodology
- Research design: preregistered (registered report, Borg et al. 2024b) two-phase sequential controlled experiment, following the ACM SIGSOFT Empirical Standard for experiments [V] (p. 2, p. 9). Phase 1 (Task 1): participants add a feature to a Java web app with or without AI; assignment to AI-dev / !AI-dev was by stated preference and habitual AI use, not random, so Phase 1 is observational [V] (p. 10, p. 43). Phase 2 (Task 2) is a *randomised controlled trial (RCT)*, i.e. participants are assigned to groups by chance: new participants, all without AI, were randomly assigned to evolve a valid Task 1 solution from either the AI-dev (treatment) or !AI-dev (control) cohort [V] (p. 2, p. 12). Analysis: frequentist tests plus Bayesian causal models built from a DAGitty causal graph, adjusting for Task 1 developer Java skill and habitual AI use (and Task 2 interruptions for completion time) [V] (p. 14, p. 15, p. 16). Qualitative coding of free-text answers and code analysis (CodeScene, PMD, RefactoringMiner) [V] (p. 22, p. 23).
- Approach / model / intervention: independent variable = whether the evolved Task 1 code was co-developed with an AI assistant [V] (p. 13). Participants used their preferred tools; reported Task 1 tools: GitHub Copilot 21, ChatGPT 13, Cursor 9, JetBrains AI 5, Claude 4, others ≤2 [V] (p. 27). No fully autonomous agent was given the whole task; usage frequency: every statement 17, often 10, sometimes 12 [V] (p. 25, p. 26). Data collected Oct 2024 – 18 Jan 2025, i.e. before agentic tools became common [V] (p. 3, p. 17).
- Baselines or comparison conditions: control = evolving code written without AI in Task 1 [V] (p. 12). Bayesian sensitivity analysis with neutral, AI-sceptical and AI-enthusiastic priors (optimistic completion-time prior from Peng et al.'s 55% speedup) [V] (p. 21).

## 4. Dataset and sample
- Data source(s): RecipeFinder, a deliberately substandard Java/Spring Boot web app (2 KLoC, 47 files) co-designed with Equal Experts consultants; plus questionnaires and CI measurements [V] (p. 64, p. 65, p. 66).
- Sample size (N) and unit: 449 valid pre-screening sign-ups (92.2% professional developers, median age group 40–49) [V] (p. 24). 118 assigned to AI-dev, 106 randomly to !AI-dev, 225 reserved for Task 2 [V] (p. 24). Valid solutions: Task 1 = 39 AI-dev + 37 !AI-dev (one !AI-dev reclassified for AI use); Task 2 = 75 (40 treatment, 35 control) [V] (p. 24, p. 25, p. 28, p. 30). Total 151 participants (33.6% of sign-ups) [V] (p. 19). Completion-time analysis uses 72 Task 2 times after removing values >16 h [V] (p. 18, p. 32). Of 75 Task 1 solutions offered, 51 were evolved; 24 were not (similar CH, mean 8.32 vs 8.35) [V] (p. 28).
- Sampling / selection method: volunteers recruited via social media (YouTube, LinkedIn, X) and personal networks; incentive = signed book by the last author and a chance at an "Ask Me Anything" session [V] (p. 10). Stratified random sampling into tasks [V] (p. 10). A priori power analysis (G*Power): 128 Phase 2 participants needed for d = 0.5, α = 0.05, power 0.80; target not reached [V] (p. 19). Sample is 95% male, no participants from China, Japan, South Korea [V] (p. 61).
- Data availability (public? link?): Zenodo replication package (task instructions, anonymised data, causal graph; CC BY 4.0) and a GitHub repository with analysis scripts [V] (p. 74). The study code base was deliberately not hosted publicly to avoid leakage into LLM training data; it is shared as PDF documents [V] (p. 66).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: tasks administered via snapcode.review with per-participant GitHub repos; GitHub Actions ran 3 acceptance tests per task, CodeScene (CH) and JaCoCo (coverage), and recorded timestamps [V] (p. 16, p. 17, p. 65). Task 1: add total-time filter to search and fix an injected bug; Task 2: add a cost-per-serving filter on top of a Task 1 solution; quality requirement deliberately vague ("easy to read and maintain") [V] (p. 65). Each Task 1 submission was offered to three Task 2 participants [V] (p. 17). Only solutions passing acceptance tests were kept [V] (p. 17). 73 of 151 (48.3%) did not work in one sitting; 67 self-reported time estimates replaced recorded times; 11 values >16 h removed [V] (p. 18). Bayesian models implemented in Turing (Julia) [V] (p. 67). Phase 1 code analysis: CodeScene v6.19.15, PMD v7.13.0 (default/all Java rules), RefactoringMiner 2.0 [V] (p. 23, p. 66).
- Code availability: analysis scripts and notebooks on GitHub, mirrored to Zenodo [V] (p. 74).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - Completion time — time from repo access to final submission; proxy for maintainability because more maintainable code should take less effort to evolve [V] (p. 3, p. 13).
  - CodeHealth (CH) — CodeScene file-level score 1–10 penalising 25+ code smells, LoC-weighted average over all files; authors cite prior work showing it correlates with maintenance cost, defects and onboarding and outperforms SonarQube Maintainability Rating and Microsoft Maintainability Index on a benchmark [V] (p. 4, p. 13). Customised for small tasks: Complex Method triggers at cyclomatic complexity 4 (default 9), Nested Complexity at 3 levels (default 4) [V] (p. 13).
  - Test coverage (TC) — JaCoCo line coverage; indicator of attention to testing [V] (p. 13).
  - Perceived productivity (PP) — 10 five-point Likert items mapped to SPACE dimensions S, C, E [V] (p. 12, p. 14).
  - Phase 1 only (exploratory, not preregistered): code smell deltas (removed/improved/unchanged/degraded/introduced), PMD violations, refactoring operations, regex-detected tests/comments/functional style [V] (p. 23, p. 43, p. 45).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): Shapiro-Wilk normality; Wilcoxon rank-sum + Cliff's δ (time, TC); Welch's t-test + Cohen's d (CH, PP); bootstrap CIs (1,000,000 resamples); no multiple-testing correction [V] (p. 18, p. 19). Bayesian: probability of direction > 95% counted as "significant", 95% credible intervals, posterior predictive simulations [V] (p. 22). Achieved power with n = 75: 80% only for d ≈ 0.66; 0.57 for d = 0.5; 0.17 for d = 0.2 [V] (p. 19). PP internal consistency Cronbach's α = 0.82 [V] (p. 18).

## 7. Key findings
1. Phase 2 completion time: median 136 min treatment vs 173 min control; Cliff's δ = −0.079 (negligible); Wilcoxon p = 0.56 — [V] (p. 33). Bayesian: P(Δ<0) = 76%, posterior mean −12.59%, CrI [−45.77%, +32.68%]; with a pessimistic prior the probability falls to ~38–39% — [V] (p. 33, p. 34).
2. Interruptions dominate Task 2 time: developers who took breaks finished 173.66% later (CrI [+37.69%, +416.88%]) — [V] (p. 34).
3. Phase 2 perceived productivity: mean 3.95 vs 4.06; Cohen's d = −0.21; Welch p = 0.37. Bayesian: P(Δ<0) = 84%, mean −1.26 SD, CrI [−2.46, +2.31] for code from habitual AI users — [V] (p. 35, p. 36).
4. Phase 2 CodeHealth: mean 8.49 vs 8.44; Cohen's d = 0.28; Welch p = 0.24 (n.s.). Bayesian: code originally AI-co-written by habitual AI users had +0.10 CH after evolution (P(Δ>0) = 98%, CrI [+0.02, +0.19]), stable across priors — [V] (p. 38, p. 39).
5. Developer skill mattered more: higher Task 1 Java skill gave +0.16 CH in Task 2 (P > 99%, CrI [+0.07, +0.26]) — [V] (p. 40); authors state Java proficiency had a stronger influence than AI use — [A] (p. 55).
6. Phase 2 test coverage: median 0.70 both groups; Cliff's δ = 0.09; Wilcoxon p = 0.49; Bayesian P(Δ>0) = 91%, logit +0.10 (CrI [−0.04, +0.26]) — [V] (p. 42, p. 43).
7. Phase 2 smell changes: treatment degraded Complex Method more often (55% vs 31%) and introduced Complex Conditional more often (18% vs 3%); control introduced Primitive Obsession more often (26% vs 8%); the paper calls these "significant" but does not name a test — [V] (p. 38).
8. Phase 1 (observational): AI-devs had 30.7% shorter median completion time (Wilcoxon p = 0.0029, Cliff's δ = −0.42); Bayesian estimate for habitual AI users ~60% faster (CrI [−77.11%, −30.64%]) — [V] (p. 33, p. 43). Phase 1 CH: no significant difference (p = 0.52, δ = 0.09) — [V] (p. 44).
9. Phase 1 code-level patterns: AI-devs added up to 10,788 lines (mean 642.74 vs 216.41 added lines); resolved the Bumpy Road smell more often (72% vs 46%); introduced more Code Duplication (23% vs 11%), Complex Conditionals (13% vs 5%), Nested Complexity (8% vs 0%); fewer PMD complexity violations but higher variance in Code Style violations (SD 154 vs 45) — [V] (p. 30, p. 45, p. 46, p. 47). Authors: AI use "may reduce complexity but add stylistic clutter" — [A] (p. 47).
10. Overall conclusion: no systematic maintainability advantage or disadvantage when others evolve AI-co-developed code; main risks are code bloat and "cognitive debt" — [A] (p. 1, p. 57, p. 58, p. 62).

## 8. Limitations stated by the authors
- [A] Only short-term maintainability is observed; long-term effects need longitudinal case studies (p. 58).
- [A] Individual developers only, no team dynamics; small system, so no architectural conclusions; security not studied (p. 58).
- [A] Many participants worked in several sittings; time partly self-estimated (p. 18, p. 59).
- [A] Possible confirmation bias in AI-devs' perceived productivity (p. 45, p. 59).
- [A] Participants' differing definitions of "good enough" quality; randomisation may not balance them at this N (p. 55, p. 59).
- [A] Remote setting; protocol adherence cannot be guaranteed; one participant submitted Task 1 twice (p. 17, p. 59, p. 60).
- [A] External validity: one small Java/Spring Boot system; Task 2 developers did not use AI; mature commercial assistants only; 95% male, uneven geography (p. 60, p. 61).
- [A] RCT underpowered: non-significant results rule out only large effects (p. 61).

## 9. Limitations we identified
- [I] Phase 1 assignment by preference means the "treatment" is "code from developers who like and habitually use AI, using AI" — not AI use alone. The Phase 2 randomisation protects the comparison of *which code* is evolved, but the treatment effect bundles developer type and tool use. Based on the assignment procedure (p. 10, p. 17).
- [I] Internal numeric inconsistencies: the habitual-user Task 1 speedup is 55.9% in the abstract, introduction and conclusion (p. 1, p. 2, p. 62) but ~60% / 59.6% in the results and discussion (p. 33, p. 54); Cronbach's α is 0.82 (p. 18) but ">0.85" (p. 61); the "habitual AI user" threshold is "Strongly agree" (=5) on p. 15 but "4 or 5" in the pilot assignment on p. 17.
- [I] Several Phase 1/Phase 2 smell and PMD differences are called "significant" without a named test or correction (p. 38, p. 47); treat them as descriptive.
- [I] The headline "+0.10 CodeHealth" is a Bayesian subgroup result for habitual AI users, at the 95% probability-of-direction threshold, on a scale where groups differ by hundredths; it is the only "significant" maintainability effect and it favours AI.
- [I] CodeHealth is a proprietary metric from the first author's employer, customised for this study (p. 13, p. 75); independent replication with an open tool (e.g. SonarQube) was not done for the RCT outcome.
- [I] The evolved base system is small (2 KLoC) and Task 2 changes are tiny (median 56.5 vs 80 added lines; some participants called it "simplistic") (p. 52), which limits sensitivity to maintainability differences.
- [I] Code volume — the risk the authors themselves highlight — is not an RCT outcome; Task 2 participants were randomised to code bases that varied greatly in size (Task 1 added lines up to 10,788) (p. 30).

## 10. Threats to validity
- Internal (confounds, leakage, selection): Phase 2 randomised; Phase 1 not (preference-based) (p. 10, p. 43). Covariate adjustment for Java skill and AI habituality via causal DAG (p. 15, p. 16). Protocol violations handled (p. 17, p. 18). Task code kept out of public repos to prevent LLM training-data leakage (p. 66). Differential dropout: 24 of 75 Task 1 solutions were never evolved (p. 28).
- External (generalisability of sample/context): senior professional volunteers, largely Western, male; one Java/Spring Boot app; first/second-generation assistants (Copilot, ChatGPT, Cursor), late 2024 (p. 3, p. 24, p. 60, p. 61).
- Construct (do metrics measure the concept?): completion time as maintainability proxy is noisy (setup friction, Java ramp-up, interruptions) (p. 53, p. 54); CodeHealth customised thresholds (p. 13); PP self-reported (p. 59).
- Statistical conclusion (power, multiple comparisons, variance): underpowered (75 vs 128 planned); no multiple-testing correction; failed sensitivity analysis for completion time under optimistic prior (p. 19, p. 54, p. 61). Independence of observations assumed though some Task 1 solutions were evolved by up to four Task 2 participants (p. 18, p. 28).
- Reproducibility (data/code/setup reported?): preregistered; Zenodo + GitHub replication package with data, scripts, CodeHealth configuration and task materials (p. 13, p. 74). Conflicts of interest declared: first author employed by CodeScene; three authors consultants at Equal Experts (AI-accelerated delivery); last author runs the YouTube channel used for recruitment (p. 61, p. 75).

## 11. Future research directions
- Stated by authors [A]: study evolution where the second developer also uses AI; evaluate third-generation coding agents (Claude Code, Amp); add security analysis (p. 63); longitudinal case studies and action research on maintainability dynamics (p. 63); examine code bloat from excessive generation and cognitive debt (p. 1, p. 57, p. 62); study when enthusiastic AI use leads to downstream maintainability backlash (p. 62); broaden demographic representation (p. 61).
- Suggested by us [I]: run the same two-phase hand-off design with agent-generated (vibe-coded) applications reconstructed from a UI/spec, measuring code volume and system-level structure as RCT outcomes, with an open static-analysis tool alongside CodeHealth.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ3 (main), RQ4, RQ5.
- How it informs our work [I]: the only randomised evidence in our set on downstream maintainability of AI-assisted code. Its design — a second developer evolves the generated code without AI, with time and quality measured — is directly reusable for evaluating maintainability of reconstructed apps (RQ5). Its null result (no degradation at file level) contrasts with he2026speed's project-level complexity increase; the difference in tool generation (completion/chat vs agentic), scale (2 KLoC task vs real repos) and metric (CodeHealth average vs total cognitive complexity) is a key point for RQ3/RQ4.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Developers evolving AI-co-developed code showed no significant difference in completion time (median 136 vs 173 min, p=0.56, Cliff's δ=−0.079) | 33 | V | moderate |
| RQ3 | No significant difference in CodeHealth after evolution (8.49 vs 8.44, p=0.24, d=0.28); Bayesian +0.10 CH for code from habitual AI users (P=98%) | 38, 39 | V | moderate |
| RQ3 | No significant difference in test coverage (median 0.70 both, p=0.49) or perceived productivity (d=−0.21, p=0.37) | 35, 42 | V | moderate |
| RQ3 | Task 1 developer Java skill had a larger effect on downstream CodeHealth (+0.16) than AI use | 40, 55 | V | moderate |
| RQ3 | AI-assisted Task 1 code (observational) introduced more Code Duplication (23% vs 11%) and Complex Conditionals (13% vs 5%), fewer PMD complexity violations, and much larger code volume in outliers (up to 10,788 lines) | 30, 46, 47 | V | weak |
| RQ3 | AI assistance cut Task 1 median completion time by 30.7% (p=0.0029, δ=−0.42; observational) | 43 | V | moderate |
| RQ4 | Maintainability operationalised as hand-off evolution by a second developer (time) plus customised CodeScene CodeHealth, JaCoCo coverage and SPACE-based perceived productivity | 13 | V | moderate |
| RQ4 | RCT underpowered (75 of 128 planned; 80% power only for d≈0.66); authors read null results as evidence against large effects only | 19, 61 | V | moderate |
| RQ5 | Authors call for studies of third-generation agents, AI-assisted second developers, security, code bloat and cognitive debt, and longitudinal designs | 62, 63 | A | moderate |

## 14. Key quotes
> "we did not detect systematic maintainability advantages or disadvantages when other developers evolved code co-developed with AI assistants" (p. 1)

> "We therefore interpret our frequentist findings as evidence against large effects, rather than as evidence for the absence of any effect." (p. 61)

> "Even if individual files become highly maintainable, the sheer code volume may undermine system-level maintainability." (p. 57)

## Analyst notes
- Reading coverage: main text pages 1–63 read in full; Appendix A (system and tasks, pp. 63–66) read in full; Appendix B (Bayesian model specifications, pp. 67–72) skimmed for model structure; Appendices C and D (CodeScene smell and PMD rule descriptions) skimmed; declarations (pp. 74–75) read; references skimmed.
- Uncertainties: the inconsistent speedup (55.9% vs 59.6%) and Cronbach's α values; the test behind "significantly" for smell-delta differences is not reported; whether the 72 completion times and 75 CH/TC values imply further exclusions beyond those stated. Peer-reviewed journal (EMSE 2026) and preregistered; conflicts of interest are declared and relevant because the main quality metric is the first author's employer's product.
