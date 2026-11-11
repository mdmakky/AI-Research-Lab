---
key: fawzy2026vibe
status: ready
evidence_basis: full-text
design: systematic grey literature review with thematic analysis (Garousi guidelines)
dataset: 101 practitioner grey-literature sources (blogs, forums, media) found via Google + snowballing, 2022-2025
sample_size: 101 sources; 518 coded behavioural units
metrics: theme frequencies and percentages of behavioural units per RQ (no code measured)
main_finding: Practitioners vibe code for speed (62% of motivation units) but mostly perceive the code as fast but flawed (68%); QA is often skipped (36%).
relevance: medium
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Vibe Coding in Practice: Motivations, Challenges, and a Future Outlook – a Grey Literature Review

- Authors: Fawzy, Ahmed; Tahir, Amjed; Blincoe, Kelly
- Year / venue: 2026, Proceedings of the IEEE/ACM 48th International Conference on Software Engineering: Software Engineering in Practice (published)
- DOI: 10.1145/3786583.3786866 · URL: https://doi.org/10.1145/3786583.3786866
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Note on the source: our PDF is the arXiv v1 (arXiv:2510.00328, 30 Sep 2025) with an ACM template placeholder header ("Conference'17"); the published ICSE-SEIP 2026 version may differ in wording and pagination. Page refs are to our 12-page PDF.

## 1. Research objective
- [A] To systematically investigate why users engage in vibe coding, what they experience while doing so, how they perceive the quality of AI-generated code, and which quality assurance (QA) practices they apply, using firsthand accounts in grey literature (p. 1, p. 2).
- [A] The authors define vibe coding as "using AI code generation tools to produce software primarily by describing goals in natural language and iteratively prompting, while relying on minimal review of the generated code" (p. 1).

## 2. Research questions / hypotheses
- [V] RQ1: What are the motivations behind vibe coding? (p. 2)
- [V] RQ2: What is the user experience while vibe coding? (p. 2)
- [V] RQ3: What is the perception of the AI-generated code quality with vibe coding? (p. 2)
- [V] RQ4: What quality assurance (QA) practices are applied when vibe coding? (p. 2)
- No hypotheses; exploratory qualitative design (p. 2).

## 3. Methodology
- Research design: [V] Systematic grey literature review (GLR) following Garousi et al.'s guidelines, with a quality-assessment step and Braun & Clarke thematic analysis of extracted "behavioural units" (p. 3, p. 4, p. 5). A *grey literature review* is a systematic review of non-peer-reviewed sources such as blogs and forum posts.
- Approach / model / intervention: [V] Google search with an iteratively developed search string (six stages, including a pivot to practitioner language and a quasi-gold-standard check), plus backward snowballing (p. 3, p. 4). Each source scored 0-3 on five quality criteria (Authority, Evidence, Objectivity, Currency, Purpose; max 15); sources scoring >= 10 retained (p. 4, p. 5). Quotes extracted at the behavioural-unit level and coded into themes per RQ (p. 5).
- Baselines or comparison conditions: not applicable (descriptive review; no comparison groups). No comparison against non-vibe-coding or human-written code.

## 4. Dataset and sample
- Data source(s): [V] Grey literature: blog posts, online articles, forums, media articles, technical reports, found via Google (p. 3, p. 5).
- Sample size (N) and unit: [V] 154 sources retrieved; 101 included; 518 behavioural units (140 motivation, 132 experience, 114 code-quality perception, 132 QA practice) (p. 5).
- Sampling / selection method: [V] First 100 results of the final string screened, then screening continued until thematic saturation; snowballing applied to the first 100 results (p. 4). Inclusion: English, 2022-2025, identifiable author, public full text, behavioural evidence of vibe coding (p. 4). 53 excluded: 40 below the quality threshold, 13 by inclusion/exclusion criteria (p. 5). Sources showing "Experienced developers applying critical oversight without skipping QA" were an explicit exclusion criterion (p. 4).
- Data availability (public? link?): [V] Replication package on Zenodo, doi 10.5281/zenodo.17188020 (p. 10, p. 11). We did not open it.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Search with Google; the quasi-gold-standard set comprised posts by Karpathy, Willison, Najim and Shields (p. 4). Quality assessment and unit extraction "mainly conducted by the first author", with "a subset" cross-validated by another co-author (p. 4, p. 5). Exact search date: not reported (reference access dates fall in May-July 2025, p. 11). Size of the cross-validated subset: not reported. Inter-rater agreement statistic: not reported. Breakdown of included sources by type: not reported in the text.
- Code availability: not applicable (no software); data and analysis in the replication package (p. 10).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] Frequency and percentage of behavioural units per theme within each RQ (Tables 2-5) (p. 6, p. 8). These count coded quotes, not sources or people. No code-level measures (correctness, quality, maintainability) are taken.
- Statistical testing (tests used, significance, effect sizes, confidence intervals): not reported (descriptive counts only).

## 7. Key findings
1. [V] Motivation: Speed & Efficiency is the most frequent theme, 87/140 units (62%); Accessibility & Empowerment 20 (14%); Learning & Experimentation 15 (11%) (p. 6).
2. [V] Experience: Instant Success & Flow 85/132 (64%); Prompt Struggle & Iteration 17 (13%); Code Breakdown or Abandonment 14 (11%) (p. 8).
3. [V] Perceived code quality: Fast but Flawed 78/114 (68%); Fragile or Error-Prone 22 (19%); Sloppy or Low Maintainability 5 (4%); Prototype-Ready Only 5 (4%); High Quality & Clean 3 (3%) (p. 8).
4. [V] QA practices: Skipped QA 48/132 (36%); Manual Testing or Edits 38 (29%); Uncritical Trust 24 (18%); Delegated QA to AI 13 (10%); Reprompting Instead of Debugging 6 (5%) (p. 8).
5. [A] A "speed-quality trade-off paradox": vibe coders knowingly accept flawed code for rapid progress; only experienced users can fix problems when they arise (p. 9).
6. [A] A "QA crisis": most QA practices depart from code verification; vibe-coded apps "may look fine but hide serious flaws" (p. 9).
7. [A] A "new class of vulnerable developers" who can build but not debug; practitioners documented vibe-coded apps lacking authentication/authorization or containing hardcoded secrets (p. 9).
8. [A] Vibe coding "lowers barriers and accelerates prototyping, but at the cost of reliability and maintainability" (p. 1). This conclusion rests on practitioner perceptions, not on measured code.

## 8. Limitations stated by the authors
- [A] Cannot claim to have captured all relevant grey literature, given its diffuse and evolving nature (p. 10).
- [A] Residual quality bias despite the 10/15 threshold (p. 10).
- [A] Thematic coding involves subjective judgement; findings are "patterns drawn from the data rather than precise measurements" (p. 10).
- [A] Self-selection bias: only practitioners who chose to share stories online; findings not generalisable to all vibe coders (p. 10).
- [A] Coding mainly by the first author with subset cross-validation; this "reduced, but did not eliminate" subjective bias (p. 10).

## 9. Limitations we identified
- [I] Percentages are shares of coded quotes, not of sources or people, yet the Discussion reads them as people: "29% reported that they usually make some manual adjustments" and "19% admitting their code is 'fragile or error-prone'" (p. 9). One source can contribute several units, so prolific sources may dominate. Based on the unit definition (p. 5) vs the Discussion wording (p. 9).
- [I] Excluding "Experienced developers applying critical oversight without skipping QA" (p. 4) removes careful-practice accounts by design, which likely inflates the share of skipped/uncritical QA themes. The 36% Skipped QA figure is partly a product of the definition and selection.
- [I] No code was inspected: all quality and maintainability statements are practitioner perceptions. "Sloppy or Low Maintainability" is only 5 units (4%) (p. 8), so the paper gives little direct evidence on maintainability despite its headline claim (p. 1).
- [I] No inter-rater reliability statistic and unknown size of the cross-checked subset (p. 4, p. 5) limit confidence in theme assignment.
- [I] Grey-literature authors (bloggers, journalists, vendor staff) may over-report dramatic successes or failures; the source-type mix is not reported in the text.
- [I] Inclusion window is 2022-2025 although the term was coined in 2025 (p. 1, p. 4); how pre-2025 "vibe coding" behaviour was identified is not explained.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Selection shaped by Google ranking, a single search engine, and an exclusion criterion that removes careful QA behaviour (p. 3, p. 4). Mainly single coder (p. 5).
- External (generalisability of sample/context): [A] Self-selected online accounts; not representative of all vibe coders (p. 10). [I] English-only, 2025-era tools; tool mix not reported.
- Construct (do metrics measure the concept?): [I] Unit frequency measures how often a theme is mentioned, not how prevalent a behaviour is among vibe coders, nor actual code quality.
- Statistical conclusion (power, multiple comparisons, variance): not applicable (no inferential statistics); [I] themes with 1-5 units are too thin to interpret.
- Reproducibility (data/code/setup reported?): [V] Search string, criteria, quality rubric and a replication package are reported (p. 4, p. 5, p. 10). [I] Google results are not reproducible over time; exact search dates not reported.

## 11. Future research directions
- Stated by authors [A]: how practices shift with experience (non-developers, novices, professionals) (p. 10); whether vibe coding produces defect and vulnerability patterns different from conventional AI-assisted and human coding (p. 10); which code review practices (run-and-see, automated tests, AI-assisted review) work under vibe-coding conditions (p. 10); integrating vibe coding into training for non-software developers (p. 10).
- Suggested by us [I]: check the perceived-quality themes against actual code (static analysis, tests) for the same projects; count sources or people, not quotes; for our project, test whether a vibe-coded reconstruction of a known app shows the "fast but flawed" pattern on objective fidelity and maintainability measures. Based on the gap between perception data here and the code-level questions in RQ2/RQ3.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (characterises the vibe-coding workflow: prompt-iterate, run-and-see, delegate QA), RQ3 (practitioner perceptions of quality/maintainability, not measured), RQ5 (authors' call for empirical defect/vulnerability comparisons).
- How it informs our work [I]: gives a practitioner-grounded definition of vibe coding and a description of typical QA behaviour (run-and-see, reprompting) that a reconstruction study should model or control. It does not measure fidelity or code quality, so it can motivate but not support claims for RQ2/RQ3. Venue is peer-reviewed (ICSE-SEIP), but the underlying evidence is grey literature, so weight it as perception evidence only.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Vibe coding defined as natural-language goal prompting plus iterative re-prompting with minimal code review; speed is the dominant motivation (87/140 motivation units, 62%) | p. 1, p. 6 | V | moderate |
| RQ1 | Common vibe-coding QA behaviours: skipped QA (36%), uncritical trust (18%), delegating QA to the AI (10%), reprompting instead of debugging (5%) of 132 QA units | p. 8 | V | weak |
| RQ3 | Practitioners mostly perceive vibe-coded output as "fast but flawed" (78/114, 68%) or fragile/error-prone (22/114, 19%); only 3 units (3%) call it high quality | p. 8 | V | weak |
| RQ3 | Authors conclude vibe coding trades reliability and maintainability for speed; based on perceptions, no code measured | p. 1, p. 9 | A | weak |
| RQ4 | Evidence is counts of coded quotes from 101 self-selected grey-literature sources, coded mainly by one author, no agreement statistic reported | p. 5, p. 10 | V | moderate |
| RQ5 | Authors call for empirical evidence on whether vibe coding yields defect/vulnerability patterns distinct from AI-assisted and human coding, and on which review practices work | p. 10 | A | moderate |

## 14. Key quotes
> "we define vibe coding as the practice of using AI code generation tools to produce software primarily by describing goals in natural language and iteratively prompting, while relying on minimal review of the generated code" (p. 1)

> "Our analysis reveals a speed–quality trade-off paradox" (p. 1)

> "thematic coding inevitably contains subjective judgment, so our findings should be understood as patterns drawn from the data rather than precise measurements" (p. 10)

## Analyst notes
- Reading coverage: whole paper read (pp. 1-10); reference list (pp. 11-12) skimmed for the replication-package entry. Figures 1-3 are images not rendered in the text; their content is covered by text and tables. Replication package not opened.
- Uncertainties: the published ICSE-SEIP version may have revised numbers or wording; our PDF is arXiv v1. Strength "weak" for perception rows reflects grey-literature sources, quote-level counting and mainly single-coder design, not a judgement on the venue.
