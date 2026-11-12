---
key: asdaque2026novice
status: complete
evidence_basis: full-text
design: repository mining study comparing agentic pull requests of low- vs high-experience GitHub users (MSR 2026, 5-page paper; track not stated)
dataset: AIDev dataset subset (repos >100 stars) of AI-agent pull requests (Copilot, Codex, Claude Code, Cursor, Devin) on GitHub OSS
sample_size: 22,953 PRs from 1,719 users (860 low-experience, 859 high-experience by commits/account-age quartiles)
metrics: commits and files changed per PR, PR acceptance rate, PR resolution time (days to merge), review comments per PR
main_finding: Low-experience users' agentic PRs were larger (2.15x commits), accepted 31% less often, took 5.16x longer and drew 4.52x more review comments.
relevance: low
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Novice Developers Produce Larger Review Overhead for Project Maintainers while Vibe Coding

- Authors: Asdaque, Syed Ammar; Haider, Imran; Malik, Muhammad Umar; Ghafoor, Maryam Abdul; Bangash, Abdul Ali
- Year / venue: 2026, Proceedings of the 23rd International Conference on Mining Software Repositories (published)
- DOI: 10.1145/3793302.3793597 · URL: https://doi.org/10.1145/3793302.3793597
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Note on the source and page numbers: our PDF is the arXiv v1 (arXiv:2602.23905v1, 27 Feb 2026, stamp on p. 1) carrying the MSR '26 ACM header and DOI; it is not the ACM Digital Library copy, so page refs use arXiv pagination. The PDF has **5 pages**: the PDF page tree has 5 page objects (re-checked with `pdfinfo` on 2026-11-12, after poppler was installed), and the ACM reference line says "5 pages" (p. 1). But `fulltext.txt` has 7 page markers because the text extraction of Figure 2 inserted spurious breaks. Page refs below use the real PDF page index checked against `paper.pdf`: `fulltext.txt` markers "page 4", "page 5" and "page 6" are all PDF page 4, and marker "page 7" is PDF page 5 (references). `metadata.json` (`fulltext.pages: 7`) is also wrong on this point; the lead should repair it through `rlab`, not by hand-editing.

## 1. Research objective
- [A] To test whether developer experience still matters in AI-assisted development, i.e. whether "vibe coders with less development experience [can] substitute for expert developers", by comparing agentic pull requests (PRs) of low- and high-experience GitHub users (p. 1).
- [V] The paper adopts the definition of vibe coding as "a workflow in which a human developer directs and supervises an AI agent through natural-language prompts and validates the generated code" (p. 1). Operationally, a "vibe coder" is any non-bot user in AIDev who created agentic PRs (p. 2).

## 2. Research questions / hypotheses
- [V] RQ1: What is the frequency and magnitude of contributions submitted by high-experience (ExpHigh) and low-experience (ExpLow) vibe coders in OSS? (p. 2)
- [V] RQ2: Is the PR merge effort similar between ExpHigh and ExpLow vibe coders? (p. 2)
- No formal hypotheses stated.

## 3. Methodology
- Research design: [V] Retrospective mining study of an existing public dataset of AI-agent PRs, with group comparison and a small manual inspection (p. 2, p. 3). A *mining study* analyses existing repository data rather than running an experiment.
- Approach / model / intervention: [V] Three steps: select vibe coders and PRs; split them by experience; extract metrics for statistical comparison (p. 2). Experience score = total commits by the user / GitHub account age, retrieved via the GitHub GraphQL API, following Malik et al. (p. 1, p. 2). Users split into quartiles: Q3+Q4 = ExpHigh (859), Q1+Q2 = ExpLow (860) (p. 2). Manual inspection of the top 15 highest-review-volume ExpLow feature PRs to explain friction (p. 3).
- Baselines or comparison conditions: [V] ExpHigh vibe coders are the comparison group for ExpLow (p. 2). No comparison with non-AI (human-only) PRs.

## 4. Dataset and sample
- Data source(s): [V] AIDev dataset of AI-assisted PRs on GitHub OSS, covering agents such as Copilot, Codex, Claude Code, Cursor and Devin; the subset for repositories with >100 stars contains 33,596 PRs and 1,796 users (p. 2).
- Sample size (N) and unit: [V] After removing bot accounts: 22,953 PRs by 1,719 distinct users (p. 2). Unit of analysis is the PR, grouped by author experience; 11 PR categories (e.g. feature, fix, docs, chore) (p. 2, p. 3).
- Sampling / selection method: [V] All non-bot users in the AIDev >100-star subset; bot filter = username contains "bot" or matches known agent identifiers (e.g. Copilot) (p. 2). Selection of the 15 inspected PRs = top review volume in the feature category (p. 3).
- Data availability (public? link?): [V] AIDev is public (p. 2); replication package at github.com/AmmarAsdaque/msr-2026-replication-package (p. 2, p. 5). We did not open it.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Python (pandas, numpy, matplotlib, seaborn, scipy) (p. 2). Group-wise comparisons "on mean values of each metric across PR categories" (p. 2). Date of AIDev snapshot, agent mix per group, number of repositories, and PRs per user distribution: not reported. Who did the manual inspection and how it was coded: not reported.
- Code availability: [V] Replication package on GitHub (p. 5).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] Contribution magnitude = commits per PR and files changed per PR (RQ1); PR acceptance rate = merged PRs / submitted PRs; PR resolution time = days from PR creation to merge; PR review volume = total review comments per PR (RQ2) (p. 2). Rationale: "real-world outcomes" of contribution size and merge effort (p. 1, p. 2).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V] Mann-Whitney U for commits, files, resolution time and review volume; Chi-square for acceptance rate; overall and per category; significance at p < 0.05 (p. 2, p. 3). Benjamini-Hochberg correction "for all tests" (p. 4). Exact p-values, effect sizes and confidence intervals: not reported. Group differences are reported as ratios of means (e.g. 2.15x) (p. 2, p. 3).

## 7. Key findings
1. [V] ExpLow PRs contain 2.15x more commits per PR than ExpHigh (Mann-Whitney p < 0.05); more commits in 10/11 categories, significant in all 10; feature PRs: 1.58 vs 4.20 mean commits (p. 2, p. 3).
2. [V] ExpLow PRs change 1.47x more files (p < 0.05); more files in 9/11 categories, significant in 5/11; style PRs: 24.29 vs 70.35 mean files (p. 3).
3. [V] ExpLow PRs have a 31% lower acceptance rate (Chi-square p < 0.05); lower in 10/11 categories, significant in all 10; documentation: 93.06% (ExpHigh) vs 75.39% (ExpLow) (p. 3).
4. [V] ExpLow PRs take 5.16x longer from creation to merge (p < 0.05); significant in 10/11 categories; chore: 0.61 vs 2.83 days (p. 3).
5. [V] ExpLow PRs receive 4.52x more review comments (p < 0.05); significant in 6/11 categories; chore: 0.13 vs 0.86 comments per PR (p. 3). Figure 2c shows average review volume below 1 comment per PR in every category for both groups (p. 4), so the large ratios rest on small absolute numbers.
6. [A] Manual inspection of 15 PRs suggests two friction sources: "Infrastructure Mismatch" (AI code that is syntactically correct but ignores build/CI environment constraints) and "Integration Friction" (AI code lacking system context, e.g. privacy schemas), each illustrated by one PR (p. 3, p. 4).
7. [A] Low-experience vibe coders "focus on generating more code while shifting verification burden onto reviewers"; managers "may not be able to safely replace experienced developers with low-experience vibe coders without increasing review capacity" (p. 1).

## 8. Limitations stated by the authors
- [A] Findings may not apply under the broader definition of vibe coding as any AI assistance (p. 4).
- [A] Experience measured by commit count "conflates activity with skill"; developers with offline experience but few GitHub commits count as low-experienced (p. 4).
- [A] Project-specific factors (e.g. review policies) can influence acceptance and review volume; within-category comparison mitigates but residual effects may remain (p. 4).
- [A] Multiple comparisons raise Type I error risk; mitigated by Benjamini-Hochberg correction (p. 4).

## 9. Limitations we identified
- [I] Confounding by repository and agent: ExpLow and ExpHigh users may contribute to different projects (with different review norms) and use different agents (Copilot vs Devin etc.). Neither is controlled or reported (p. 2). Category-level comparison (p. 4) does not control for these.
- [I] Unit of analysis / non-independence: the unit of the statistical tests is not stated clearly ("group-wise statistical test comparisons on mean values of each metric across PR categories", p. 2). If PR-level values were tested, the 22,953 PRs from 1,719 users (about 13 PRs per user on average, p. 2) are treated as independent and prolific users or repositories can dominate; no mixed-effects or per-user aggregation is reported. If category means were tested, n = 11 per group and power is very low.
- [I] The experience score (commits per account-age, p. 2) is a rate of public activity, not skill; it can also be inflated by AI-agent commits themselves, which may make the split partly circular. Quartile split at the median discards information.
- [I] Effect reporting: ratios of means are reported for skewed count/time data while tests are rank-based (Mann-Whitney) (p. 2, p. 3); no effect sizes or CIs. "31% lower acceptance rate" is not stated as relative or absolute, and overall acceptance rates are not given (p. 3).
- [I] Resolution time is defined as creation-to-merge (p. 2), i.e. merged PRs only, yet the abstract says ExpLow PRs "remain open 5.16x longer before resolution" (p. 1). Unmerged PRs are not part of this measure.
- [I] No code-level quality measure: acceptance, review comments and time are proxies of review burden, not of correctness or maintainability. Calling users "vibe coders" because they opened agentic PRs assumes, but does not verify, the supervise-and-validate workflow of the adopted definition (p. 1, p. 2).
- [I] The friction categories rest on 15 PRs and two examples, without a coding protocol (p. 3, p. 4); treat as anecdotal.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Repository, agent and task-difficulty confounds; possibly non-independent PRs (test unit unclear, see §9); bot filtering by username heuristic may leave automated accounts (p. 2).
- External (generalisability of sample/context): [I] OSS repositories with >100 stars only (p. 2); one dataset; agents of 2025. Does not cover single-developer app building or reconstruction.
- Construct (do metrics measure the concept?): [A] Experience proxy conflates activity with skill (p. 4). [I] Review volume and acceptance are indirect measures of code quality.
- Statistical conclusion (power, multiple comparisons, variance): [V] Benjamini-Hochberg correction applied (p. 4). [I] The unit of the tests is unclear (p. 2, see §9): if PR-level, very large N makes small differences significant and clustering by user is ignored; if category means, n = 11 per group gives very low power. No effect sizes either way.
- Reproducibility (data/code/setup reported?): [V] Public dataset and replication package (p. 2, p. 5). [I] AIDev snapshot date and GitHub API retrieval date not reported; account statistics change over time.

## 11. Future research directions
- Stated by authors [A]: extend the ExpHigh vs ExpLow lens to industrial settings and longitudinal studies to see how AI's role evolves with experience, informing adaptive AI tools, reviewer automation and task assignment (p. 4); training that emphasises verification skills (p. 4).
- Suggested by us [I]: control for repository and agent with mixed-effects models; add code-level quality measures (static analysis, defects after merge) to separate review friction from code quality; for our project, record and control the operator's experience level when evaluating vibe-coded reconstructions.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ3 (indirect: review burden and acceptance of AI-agent code as quality proxies), RQ4 (proxy metrics, clustering, experience operationalisation), RQ5 (operator experience as a variable a reconstruction study should control).
- How it informs our work [I]: shows that outcomes of AI-generated contributions differ with the human operator's experience, so a study of vibe-coded app reconstruction should fix or measure operator expertise. It does not evaluate application reconstruction, functional fidelity or code quality directly, hence relevance low. Peer-reviewed 5-page paper at MSR 2026 (track not stated in the PDF; a 5-page format suggests a short or challenge-track paper, which would be a lower tier than a technical-track paper, but this is unchecked) with large N but weak construct validity.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Agentic PRs from low-experience users were accepted less often (31% lower; e.g. docs 93.06% vs 75.39%) and drew 4.52x more review comments than those from high-experience users | p. 3 | V | moderate |
| RQ3 | Low-experience users' agentic PRs were larger (2.15x commits, 1.47x files per PR) and took 5.16x longer from creation to merge | p. 2, p. 3 | V | moderate |
| RQ3 | Authors attribute friction to AI code that ignores build/CI constraints and lacks system context (from 15 inspected PRs) | p. 3, p. 4 | A | weak |
| RQ4 | Experience = total commits / GitHub account age; quartile split Q1–2 vs Q3–4; group differences reported as ratios of means without effect sizes or CIs | p. 2, p. 3 | V | moderate |
| RQ4 | Authors state the commit-based experience proxy "conflates activity with skill" | p. 4 | A | moderate |
| RQ4 | Unit of analysis for the tests is unclear ("on mean values of each metric across PR categories", p. 2); if PR-level, observations are clustered by user (based on 22,953 PRs / 1,719 users, p. 2) | p. 2 | I | weak |
| RQ5 | Authors call for industrial and longitudinal studies of how AI's role changes with developer experience | p. 4 | A | weak |

## 14. Key quotes
> "a workflow in which a human developer directs and supervises an AI agent through natural-language prompts and validates the generated code" (p. 1)

> "Our results indicate that low-experienced vibe coders focus on generating more code while shifting verification burden onto reviewers." (p. 1)

> "we measure “experience” via commit count [15], which conflates activity with skill" (p. 4)

## Analyst notes
- Reading coverage: whole paper read (5 PDF pages including references). Figures 1 and 2 read from the PDF images (pages 3 and 4) because the text layer garbles them. Replication package not opened.
- Page-number caveat: `fulltext.txt` contains NUL bytes (use `grep -a`) and wrong page markers after page 4 (see note at top). Quotes on PDF page 4 appear in `fulltext.txt` under markers "page 4" to "page 6". Reported to the caller so the metadata/fulltext can be repaired by the lead.
- Uncertainties: whether "31% lower" is relative or absolute; whether AIDev "agentic PRs" include PRs opened autonomously under a human account; the track of the MSR paper (not stated in the PDF; check on the DOI landing page before asserting it, per critical review batch A, 2026-11-11).
- Review fixes applied 2026-11-12 (critical-review-batch-a): split the RQ4 evidence row into [V]/[A]/[I]; reworded the non-independence point as an unclear test unit; restated the page-count source; removed the unsourced "short paper" label.
