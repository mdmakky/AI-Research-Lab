---
key: mock2026vibe
status: complete
evidence_basis: full-text
design: pre-experimental static-group comparison (solo vs collaborative TDD with professionals) plus exploratory repeated runs of fully-automated and agentic workflows
dataset: 2 small Python TDD tasks (TextFormatter string centring); baseline test suite of 12 assertions derived by category-partition testing
sample_size: 16 professionals (9 solo, 7 collaborative); 3 fully-automated runs; 12 agentic runs (MetaGPT X, GPT-5 / Claude Sonnet 4)
metrics: test pass rate on baseline tests, McCabe complexity, statement/branch coverage, LCS/Levenshtein similarity, test methods/assertions, iterations, time
main_finding: Agentic runs passed most baseline tests (mean 94.6%) fastest but with higher complexity and lower coverage; collaborative vibe coding did not beat solo coding.
relevance: medium
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Vibe Coding: An experiment with test-driven development

- Authors: Mock, Moritz; Russo, Barbara
- Year / venue: 2026, Empirical Software Engineering (published)
- DOI: 10.1007/s10664-026-10950-z · URL: https://doi.org/10.1007/s10664-026-10950-z
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Note on the source: the PDF analysed is the published Springer open-access version of record (link.springer.com, DOI above; not the arXiv preprint 2607.22406) (Empirical Software Engineering (2027) 32:40, accepted 4 August 2026; 48 pages). Metadata gives year 2026 (online publication); the printed volume year is 2027 (p. 1).

## 1. Research objective
- [A] To investigate how humans and conversational LLMs (CLLMs) can collaborate "as peers through vibe coding", by comparing four interaction models (solo, collaborative, fully automated, agentic) within a Test-Driven Development (TDD) process (p. 1, p. 2).
- [V] Empirical goal (GQM): "Analyse code generation to compare human-CLLM interaction models with respect to code quality and development process efficiency, from the viewpoint of developers, in the context of TDD" (p. 11).
- [I] Important for our use: in this paper "vibe coding" means the collaborative model in which the human writes TDD tests and the CLLM writes production code through fixed, scripted prompts that participants could not modify (p. 7, p. 8, p. 15). This is narrower and more structured than the "minimal review" vibe coding of grey-literature definitions (e.g. fawzy2026vibe).

## 2. Research questions / hypotheses
- [V] RQ1: How does the quality of production code vary across interaction models? Sub-questions: RQ1.1 syntactic similarity, RQ1.2 functional correctness, RQ1.3 complexity (p. 11, p. 12).
- [V] RQ2: How does the quality of the tests vary? RQ2.1 structural complexity of tests, RQ2.2 coverage (p. 13).
- [V] RQ3: How does TDD process efficiency vary? (p. 13)
- [V] Statistical null hypotheses per pairwise comparison are one-tailed (H0: A <= B, per Tables 9-13) (p. 25, p. 27); no substantive directional hypotheses stated up front. [I] The reported test directions are not reliable row by row; see §9.

## 3. Methodology
- Research design: [V] Two complementary settings: (i) a "controlled pre-experimental study" using a Static-Group Comparison design with a control group (solo-coding, CG) and an experimental group (collaborative, EG) of professionals; (ii) "repeated exploratory executions" of fully-automated and agentic workflows on the same tasks (p. 1, p. 14, p. 15). A *pre-experimental design* is a weak experimental design (Campbell & Stanley) without pre-tests and, in the classical form, without random assignment.
- Approach / model / intervention: [V] Four interaction models operationalised as workflows (p. 7, p. 8): solo-coding (human only); collaborative (human writes tests, CLLM generates production code; this is what the paper calls vibe coding); fully-automated (scripts drive a single CLLM to write both tests and code); agentic (MetaGPT X platform, Engineer mode) (p. 7, p. 8, p. 17). Prompts built from White et al.'s prompt-pattern catalogue (Game Play, Persona, Template, Context Manager, Question Refinement) (p. 8); prompts tell the CLLM "Built-in functions are not allowed" (Table 7, p. 20). A failing test triggers up to five automatic re-prompts before control returns to the human (p. 19). Each iteration is a new session (p. 22).
- Baselines or comparison conditions: [V] Solo-coding (human-only TDD) is the control condition (p. 15). A baseline test suite derived from the specification by category-partition testing is the correctness oracle (p. 11, p. 12).

## 4. Dataset and sample
- Data source(s): [V] Two development tasks of a Python `TextFormatter` class: centre one word in a line (task 1) and centre two words (task 2), plus a `setLineWidth` setter (Fig. 4, p. 12). Baseline suite: two test methods with 5 and 7 assertions (p. 12, p. 28).
- Sample size (N) and unit: [V] 16 professional developers: 9 solo-coding (P1-P9), 7 collaborative (P10-P16) (p. 16). 5 came from a preliminary experiment (Mock et al. 2025), extended with 11 more (p. 13). Fully-automated: 3 runs (FA1-FA3) (p. 42). Agentic: 12 runs = 2 models (ChatGPT 5, Claude Sonnet 4) x 2 prompt scenarios x 3 runs (p. 42).
- Sampling / selection method: [V] IT professionals from Italy, Denmark and Brazil with TDD and Python experience (p. 15). Recruitment method: not reported beyond this. The authors justify N by the "typical" 15-25 range for studies with professionals (p. 13, p. 15). Participants "randomly assigned" to groups (p. 15). Experience was uneven: many participants had <1 year TDD and/or <1 year Python (Table 5, p. 16). No power analysis reported.
- Data availability (public? link?): [V] Toolbox, participant data and questionnaire responses in a GitHub replication package, https://github.com/moritzmock/AI4TDD_journal (p. 43, p. 45). We did not open it.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Google Colab environment; sessions remote (screen sharing) or in person; 40-minute limit; internet search allowed but not full solutions or independent CLLM use, monitored by observation (p. 15). Collaborative participants could not modify prompts (p. 15). Collaborative and fully-automated workflows used OpenAI GPT-3.5 Turbo via API (p. 14, p. 17). Agentic workflow used MetaGPT X web interface with ChatGPT 5 or Claude Sonnet 4 (p. 17). Agentic runs pooled across models and prompts after observing "little difference" (p. 17). Time self-reported by humans, measured by runtime (`time` command) for automated workflows (p. 13, p. 17). Iterations not collectable for agentic runs (p. 17). Temperature or other model parameters: not reported. Model version dates/snapshots: not reported.
- Code availability: [V] Toolbox and data in the GitHub replication package (p. 43).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] (Table 4, p. 14)
  - TPR (Test Pass Rate): share of baseline tests passing on the production code — functional correctness, ISO 25010 sub-attribute (p. 11, p. 12, p. 14).
  - MCC (McCabe complexity), SCB/BCB (statement/branch coverage of the production code by the baseline tests) — structural complexity as a maintainability-related attribute (p. 12, p. 14).
  - LCS (longest common subsequence) and LED (Levenshtein edit distance) — syntactic similarity between workflows' code (p. 11, p. 14).
  - TM (test methods), TAM (assertions per method), SC/BC (coverage of own code by own tests) — test quality (p. 13, p. 14).
  - Number of iterations and Time — process efficiency (p. 13, p. 14). CLOC/TLOC reported for size (p. 13).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [V] Kruskal-Wallis H with epsilon-squared effect size as a screen; one-tailed Mann-Whitney U pairwise with Cliff's delta; alpha = 0.05; Holm-Bonferroni correction over six pairwise comparisons per metric (p. 10, p. 11). Confidence intervals: not reported. Means and SDs per group in Table 16 (p. 41, p. 42).

## 7. Key findings
1. [V] Kruskal-Wallis significant for CLOC, TPR, MCC, BCB, SC, BC and Time; large effects for CLOC (0.34), TPR (0.52), MCC (0.5), Time (0.63) (Table 8, p. 23).
2. [V] Functional correctness (TPR): agentic mean 94.58% vs solo 62.0%, collaborative 60.8%, fully-automated 83.3% (Table 16, p. 41, p. 42). Agentic beats every other workflow after Holm-Bonferroni (e.g. agentic > solo: U = 106.5, Cliff's delta 0.97, p = 7.81e-05) (Table 9, p. 25).
3. [V] Collaborative (the paper's vibe coding) vs solo-coding: no significant difference in TPR (U = 36.5, delta -0.16, p = 0.314) or MCC (p = 0.479) (Table 9, p. 25; Table 10, p. 27). TPR within humans ranged widely: 8.3% (P7) to 100% (P13); SD 27.3 (solo) and 36.8 (collaborative) (p. 26, p. 41).
4. [V] Agentic code is more complex: MCC mean 11.67 vs 6.44 (solo), 6.57 (collaborative), 6.0 (fully-automated) (p. 41, p. 42); significant after correction vs all three (Table 10, p. 27). Baseline branch coverage lower for agentic (mean 65.33%) than solo (83.89%) and collaborative (79.00%) (p. 41, p. 42; Table 10, p. 27).
5. [A] The authors interpret the uncovered branches as agent "implementation decisions that are not explicitly defined by the functional specifications", making agentic solutions "architecturally more complex and potentially more difficult to maintain" (p. 35). Not directly measured.
6. [V] Agentic code "preserves the main implementation but adds helper methods, logging, and validation"; agentic code shares long common subsequences with other workflows but has larger local edit distance (p. 24).
7. [V] Test quality: fully-automated tests always one assertion per method, three methods (p. 28); agentic tests had lower statement and branch coverage than solo tests (SC: U = 88.5, delta -0.64, p = 6.42e-03; BC: p = 7.31e-03), significant after correction (Table 12, p. 30; p. 31). Collaborative test organisation closest to the baseline suite (qualitative) (p. 28).
8. [V] Efficiency: agentic fastest (mean 75 s) vs fully-automated 800 s, collaborative 2,057 s, solo 2,266 s (p. 41, p. 42); collaborative participants averaged 12.1 iterations, 5.6 of them needing assertion rework (Table 14, p. 33).
9. [A] Choice of interaction model should depend on the objective: agentic for speed and production-code correctness, human-involved workflows for test quality and control (p. 40).

## 8. Limitations stated by the authors
- [A] Human and autonomous workflows were evaluated in different settings (controlled experiment vs repeated executions); comparisons across them need care (p. 36).
- [A] Results may be affected by participants' TDD and Python experience (p. 36).
- [A] Limited number of professionals reduces statistical power; increasing N was not feasible (p. 13, p. 36).
- [A] Instrumentation, baseline test suite, model configuration, TDD process and environment may have influenced the data; not addressed exhaustively (p. 37).
- [A] Tasks are simple (p. 37). A single CLLM (ChatGPT via API) for the human-involved workflows (p. 37).
- [A] Participants could have used an AI tool on a second screen; cannot be fully ruled out (p. 15).
- [A] The agentic part "should be considered exploratory" (p. 17).

## 9. Limitations we identified
- [I] Model confound: collaborative and fully-automated workflows used GPT-3.5 Turbo (p. 14, p. 17), while agentic runs used ChatGPT 5 and Claude Sonnet 4 (p. 17). The agentic advantage in TPR and time cannot be separated from the large model-generation gap. The authors call ChatGPT 5 "the most similar" model (p. 17), which we find hard to accept. This undermines the cross-workflow comparison that drives the main conclusions.
- [I] Very small groups: 9 vs 7 humans (p. 16), 3 fully-automated runs (p. 42). Repeated runs of the same configuration are not independent participants, yet they enter the same Mann-Whitney tests as people. With n = 3 (fully-automated) the minimum attainable one-tailed p-value is limited, so non-significance there is uninformative.
- [I] Design inconsistency: a Static-Group Comparison is, by definition, a design without randomisation, yet participants are said to be "randomly assigned" (p. 14, p. 15); 5 of the 16 came from an earlier preliminary session (p. 13), so session is a possible confound. No pre-test of skill; groups differ in experience (Table 5, p. 16).
- [I] Time is self-reported by humans (rounded to minutes, values like 2,400 s) but machine-measured for automated runs (p. 13, p. 41). Differences in Time mix measurement methods.
- [I] Two tiny string-formatting tasks with a 12-assertion oracle (p. 12) say little about application-level generation. TPR is assertion-level (e.g. 8.3% = 1/12).
- [I] The paper's "vibe coding" condition forbids prompt modification (p. 15) and uses scripted prompts, so it does not represent free-form vibe coding. Conclusions about "vibe coding" should be read as conclusions about this structured TDD workflow.
- [I] Some claims go beyond the data: the claim that humans "can reach the same level of correctness in collaborative settings" (p. 26) rests on single participants (P13: 100%) while the collaborative mean is 60.8% (p. 41). The Related Work states "the agentic workflow statistically produces higher-quality code" (p. 40), which conflicts with the higher complexity and lower coverage reported (p. 27, p. 35).
- [I] MCC is the only maintainability proxy; no code smells, readability or static-analysis measures.
- [I] Test direction is reported inconsistently. Under H0: A <= B, a negative Cliff's δ should give a large one-tailed p-value, yet several such rows carry small p-values:
  - "collaborative > agentic": δ −0.65, p = 8.55e-03 (Table 9, p. 25);
  - "fully-automated > agentic": δ −1.00, p = 3.79e-03 (Table 9, p. 25);
  - "collaborative > agentic": δ −0.77, p = 3.13e-03 (Table 10, p. 27).

  "collaborative > solo-coding" (δ −0.16, p = 0.314, p. 25) is also below 0.5. Other rows are consistent, e.g. "fully-automated > solo-coding" δ −0.15, p = 0.685 (p. 27). This suggests that, for some rows, the reverse alternative was tested and the labels were not updated. The substantive conclusions (agentic has higher TPR and higher MCC) agree with the group means (p. 41, p. 42). Individual p-values should not be quoted without this caveat.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Model generation confounded with workflow (see section 9); session (preliminary vs main) and experience imbalance; self-reported vs measured time. [A] Possible hidden AI use (p. 15).
- External (generalisability of sample/context): [A] Simple tasks, single CLLM for human workflows (p. 37). [I] Python-only, function-level tasks, one agentic platform; results do not transfer to multi-file applications or UI work.
- Construct (do metrics measure the concept?): [I] TPR against a 12-assertion spec-derived suite is a reasonable small-scale functional-correctness oracle; MCC alone is a thin proxy for maintainability; lower baseline coverage of agentic code partly reflects added validation/logging rather than lower quality.
- Statistical conclusion (power, multiple comparisons, variance): [V] Holm-Bonferroni correction and effect sizes reported (p. 10, p. 11). [A] Low power acknowledged (p. 36). [I] Non-independent repeated runs pooled as samples; no confidence intervals; one-tailed tests chosen for every direction; reported test directions are inconsistent with the sign of Cliff's δ in several rows (see §9, p. 25, p. 27).
- Reproducibility (data/code/setup reported?): [V] Prompts (Table 7, p. 20), metrics definitions (p. 14), per-participant data (p. 41, p. 42) and GitHub package (p. 43). [I] Agentic runs via a web interface of a commercial platform are hard to reproduce; model parameters not reported.

## 11. Future research directions
- Stated by authors [A]: extend to other development practices, CLLMs and agentic platforms (p. 40); investigate whether phase-based and iterative process models remain appropriate when AI can generate complete solutions (p. 40); apply the fully-automated evaluation suite to MBPP and HumanEval (p. 40); study agentic performance under different prompting settings (p. 17); more integrated experimental platforms than Colab (p. 34).
- Suggested by us [I]: hold the model constant across workflows; use larger, application-level tasks; measure maintainability with more than MCC (e.g. static-analysis smells, change effort); for our project, reuse the idea of a specification-derived oracle test suite (category-partition) as a functional-fidelity measure for a reconstructed app.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (contrasts structured vibe coding with agentic generation), RQ2 (functional correctness measured by a spec-derived baseline test suite), RQ3 (complexity and coverage of AI-generated vs human code), RQ4 (design weaknesses: tiny N, model confound, mixed measurement), RQ5 (no application-level or maintainability-focused evaluation).
- How it informs our work [I]: one of the few peer-reviewed controlled experiments that labels its condition "vibe coding" and compares it with human-only and agentic generation. Its evaluation framework (oracle tests for correctness + complexity/coverage for internal quality + time/iterations for effort) is a template our study design could scale up. Its findings are function-level and confounded, so they should not be used as evidence about application reconstruction. Relevance medium for RQ4/RQ5 design lessons, low for direct outcome evidence.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | "Vibe coding" operationalised as human-written TDD tests plus CLLM-generated code via fixed scripted prompts; agentic coding via MetaGPT X as the autonomous contrast | p. 7, p. 8, p. 15, p. 17 | V | moderate |
| RQ2 | Agentic runs passed more spec-derived baseline tests (mean TPR 94.58%) than solo (62.0%), collaborative (60.8%) and fully-automated (83.3%) workflows; significant after Holm-Bonferroni, but agentic used newer models (GPT-5/Claude Sonnet 4 vs GPT-3.5 Turbo) | p. 25, p. 41, p. 42 | V | weak |
| RQ2 | Collaborative vibe coding did not differ significantly from solo human coding in functional correctness (TPR p = 0.314); human results varied from 8.3% to 100% | p. 25, p. 41 | V | weak |
| RQ3 | Agentic code had higher McCabe complexity (mean 11.67 vs about 6-6.6 for other workflows) and lower baseline branch coverage (65.3% vs 79-84% for human workflows), adding helpers, logging and validation | p. 24, p. 27, p. 41, p. 42 | V | weak |
| RQ3 | Authors argue agentic solutions are architecturally more complex and "potentially more difficult to maintain"; maintainability not directly measured | p. 35 | A | weak |
| RQ4 | Evaluation used spec-derived category-partition oracle tests, MCC, coverage, LCS/LED similarity, iterations and time, with Kruskal-Wallis, one-tailed Mann-Whitney, Cliff's delta and Holm-Bonferroni | p. 10, p. 11, p. 14 | V | moderate |
| RQ4 | Sample: 9 solo vs 7 collaborative professionals, 3 fully-automated and 12 agentic runs; 2 small Python tasks; time self-reported for humans but measured for automated runs | p. 12, p. 13, p. 16, p. 42 | V | moderate |

## 14. Key quotes
> "The solutions produced by the agentic workflow show the highest functional correctness, although human developers can reach the same level of correctness in collaborative settings." (p. 26)

> "autonomous agentic platforms can effectively solve development tasks while generating solutions that are architecturally more complex and potentially more difficult to maintain" (p. 35)

> "Nonetheless, the limited number of professional participants reduces the statistical power of our analyses." (p. 36)

## Analyst notes
- Reading coverage: whole paper read (pp. 1-43), including appendix Table 16 (pp. 41-42) and declarations (p. 43). Fig. 4 (task specification, p. 12) and Table 7 (prompts, p. 20) read from the PDF images because the text layer omits them. Figures 1-3, 5-11 (diagrams/boxplots) not inspected beyond captions and text. Reference list (pp. 43-48) only checked for the replication package. Replication package not opened.
- Uncertainties: whether "randomly assigned" (p. 15) applied to all 16 or only to the 11 new participants is not stated. Agentic TPR values in Table 16 (83.0, 92.0) do not exactly equal multiples of 1/12 (83.3, 91.7), suggesting rounding or a different baseline count for agentic runs; not explained. Funding: EU NextGenerationEU / PRIN2022; authors declare no conflict of interest (p. 43).
