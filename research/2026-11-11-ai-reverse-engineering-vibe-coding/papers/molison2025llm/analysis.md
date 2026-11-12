---
key: molison2025llm
status: complete
evidence_basis: full-text
design: Quantitative comparative study; one LLM (GPT-4o) under 3 configurations vs human solutions; SonarQube static analysis + small Pass@1 sample
dataset: APPS (Python coding problems: introductory/interview/competition; human solutions from Codeforces, AtCoder, Kattis, Codewars)
sample_size: Fine-tuned model: 240 train / 480 test questions (160 per level); total solutions analysed per dataset not reported; Pass@1 on 15 solutions per approach
metrics: SonarQube bugs, code smells, vulnerabilities, severity (blocker-minor), remediation effort (min); odds ratios; Mann-Whitney U + Cliff's delta; Pass@1
main_finding: GPT-4o solutions show far fewer SonarQube bugs and less fix effort than APPS human solutions, but lower Pass@1; advantage shrinks on competition tasks.
relevance: medium
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Is LLM-Generated Code More Maintainable & Reliable Than Human-Written Code?

- Authors: Molison, Alfred Santa; Moraes, Marcia; Melo, Glaucia; Santos, Fabio; Assunção, Wesley K. G.
- Year / venue: 2025, 2025 ACM/IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM) (published)
- DOI: 10.1109/esem64174.2025.00036 · URL: https://doi.org/10.1109/esem64174.2025.00036
- Source text: `fulltext.txt` (page refs = PDF page index). The PDF analysed is the arXiv version, "arXiv:2508.00700v1 [cs.SE] 1 Aug 2025" (p. 1), from arxiv.org/pdf/2508.00700; page numbers refer to our PDF, not the ESEM proceedings pagination.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] Compare internal quality attributes (maintainability and reliability) of LLM-generated and human-written Python code, including the SonarQube-estimated effort to fix issues, across three task difficulty levels and three LLM configurations (zero-shot, few-shot, fine-tuning) (p. 1).
- [A] Secondary aim: provide a reusable experimentation infrastructure (LLM + PostgreSQL + SonarQube) for replications and automated quality analysis (p. 1).

## 2. Research questions / hypotheses
- [V] Single RQ: "Is LLM-Generated Code More Maintainable and Reliable than Human-Written Code?" (p. 1).
- [V] The only explicit null hypothesis is H0 of equal effort-in-minutes distributions between groups (p. 7, p. 9). No hypotheses are stated for bugs or code smells; these are compared with odds ratios (p. 6).

## 3. Methodology
- Research design: [V] Quantitative comparative study (static analysis of four solution sets) plus a small manual functional-correctness check (Pass@1) and qualitative inspection of failures (p. 3, p. 5, p. 8).
- Approach / model / intervention: [V] GPT-4o-2024-08-06 via the OpenAI API, used in three configurations: zero-shot prompt, few-shot prompt, and a fine-tuned GPT-4o (p. 4). The authors call all three "prompt engineering techniques" (p. 4).
- Baselines or comparison conditions: [V] Human solutions from the APPS dataset serve as the baseline ("the human dataset") (p. 4). Pairwise comparisons: each LLM configuration vs human, few-shot vs zero-shot, fine-tuned vs zero-shot (p. 6, p. 8). Few-shot vs fine-tuned is not reported.

## 4. Dataset and sample
- Data source(s): [V] APPS dataset (Hendrycks et al., NeurIPS 2021): 10,000 Python coding questions with multiple human solutions per question, labelled introductory, interview or competition (p. 3, p. 11). Human solutions were collected from Codeforces, AtCoder, Kattis and Codewars and curated by students over six months (p. 3–4).
- Sample size (N) and unit:
  - [V] Fine-tuning: 80 random questions per level for training (240 total); 160 questions per level for testing (480 total) (p. 4).
  - Number of questions submitted for zero-shot and few-shot generation: not reported (the text says "each coding question" was submitted, p. 4, but does not say whether this means all 10,000 or the 480 test questions).
  - Number of human solutions analysed by SonarQube: not reported. APPS has several human solutions per question (p. 3); whether all, one, or a sample were used is not stated.
  - [V] Twelve SonarQube result files (4 datasets × 3 difficulty levels) (p. 5).
  - [V] Pass@1 evaluated on 15 solutions per approach, 5 per difficulty level (p. 7–8).
- Sampling / selection method: [V] Fine-tuning training questions were drawn at random (p. 4). [A] The performance sample was "randomized" and "representative" (p. 10). Whether the 480 test questions were disjoint from the 240 training questions: not reported.
- Data availability (public? link?): [V] APPS is public; replication package on Zenodo (record 15283737) (p. 1, p. 11).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Model GPT-4o-2024-08-06, chosen as the latest model that allowed fine-tuning; temperature 1.00, max tokens 2048, top-p 1.00, frequency and presence penalties 0.00 (p. 4).
  - [V] Zero-shot prompt: "Generate a Python code (only one solution) to solve this question:" plus the problem text (p. 4).
  - [V] Few-shot prompt: the question followed by all human solutions for that same question from APPS ("Sample Solution {index}" entries) (p. 4).
  - [V] Fine-tuning: GPT base model trained on 240 question–answer pairs; training loss 0.21; 496,176 tokens (p. 4). Epochs and other fine-tuning hyper-parameters not reported.
  - Number of generations per question: not reported (one solution per prompt is implied by the zero-shot prompt wording, p. 4). Repeated runs or seeds: not reported.
  - [V] SonarQube Free Server edition, default Python quality profile and quality gate; a new SonarQube project is created before each scan so that all files count as new code; scans driven by Python scripts via SonarScanner CLI; results stored in PostgreSQL (p. 4–5).
  - SonarQube version: the docs link points to SonarQube Server 10.8 (p. 4); exact installed version not otherwise reported.
  - [V] Infrastructure: Ubuntu Linux VM in a VPC with SonarQube, Grafana, PostgreSQL and Python (p. 3).
  - [V] Pass@1: three authors ran sampled solutions with `python3 file.py`, fed inputs from the test cases in the problem description, and checked outputs (p. 5, p. 8).
- Code availability: [V] Scripts and replication package available on Zenodo (p. 3, p. 11).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] SonarQube Bugs (reliability: coding errors causing runtime failures or unexpected behaviour), Vulnerabilities (security), Code Smells (maintainability) (p. 5).
  - [V] Severity levels Blocker, Critical, Major, Minor (p. 5).
  - [V] Effort-in-minutes: SonarQube's estimated time to fix issues (p. 5).
  - [V] Normalised issue percentage per dataset ("proportion of rows") (p. 5–6).
  - [V] Pass@1 (Chen et al. formula), k = 1 (p. 5).
  - [A] Metrics were chosen because prior studies used reliability, maintainability and security, and SonarQube is a standard static-analysis tool (p. 2–3).
- Statistical testing (tests used, significance, effect sizes, confidence intervals):
  - [V] Effort: Mann-Whitney U test with Cliff's delta, Romano et al. thresholds (negligible < 0.147, small < 0.33, medium < 0.474, else large) (p. 5).
  - [V] Bugs and code smells: odds ratios from 2×2 contingency tables per comparison, with significance stars (p. 5–6, p. 8). The test that produced the p-values for the odds ratios is not named.
  - Confidence intervals: not reported. Correction for multiple comparisons: not reported (15 comparisons per table across Tables II–IV, p. 8). Power analysis: not reported.

## 7. Key findings
1. [V] SonarQube found no security vulnerabilities in any dataset (p. 5).
2. [V] Odds of a SonarQube bug in LLM solutions vs human solutions were very low in every configuration and level: zero-shot 0.008 / 0.006 / 0.0005, few-shot 0.003 / 0.006 / 0.001, fine-tuned 0.00 / 0.019 / 0.0005 (introductory / interview / competition), all p < 0.001 (Table II, p. 8).
3. [V] Code smells were mixed: zero-shot had 3.57× the odds of a smell vs human for introductory problems (p < 0.001); few-shot vs human was 0.52 for competition (p < 0.05); fine-tuned vs human was 0.00 for introductory and competition (p < 0.001); several other comparisons were not significant (Table III, p. 8).
4. [V] In the human dataset, bug-type issues were dominated by Blocker severity (87.50% introductory, 71.27% interview, 86.30% competition, Table I) (p. 8). [A] The authors interpret these as "bug rates" (p. 6).
5. [V] Average SonarQube effort to fix (min): introductory human 7.20, zero-shot 3.75, few-shot 4.72, fine-tuned 5.00; interview human 7.06, zero-shot 5.48, few-shot 6.13, fine-tuned 4.67; competition human 6.95, zero-shot 6.14, few-shot 7.33, fine-tuned 7.60 (Fig. 6, p. 7). [A] "LLMs reduced effort in simpler tasks, but this advantage diminished as the tasks became more complex" (p. 7).
6. [V] Cliff's delta for effort, zero-shot vs human: 0.54 large (introductory), 0.21 small (interview), 0.1 negligible (competition), all significant; fine-tuned vs human introductory 0.24 small and fine-tuned vs zero-shot introductory −0.50 large are not marked significant (Table IV, p. 8).
7. [V] Severity shift: for interview problems fine-tuning had 94.1% minor, 2.1% major, 1.2% critical, 2.6% blocker issues, vs human 10.7% blocker (p. 6). For competition problems the human dataset had the fewest critical issues relative to LLM outputs (p. 6). [A] LLMs "may introduce more critical issues compared to human-generated code" on competition tasks (Finding 3, p. 6).
8. [V] Pass@1 on 15 sampled solutions per approach: human 1.0, zero-shot 0.53, few-shot 0.87, fine-tuned 0.47 (Table V, p. 8). Partial (some test cases passed) solutions: 47% of zero-shot, 13% of few-shot and fine-tuned (p. 8). Failures included runtime errors, wrong outputs, hard-coded inputs, waiting for input indefinitely and syntax errors (p. 8).
9. [A] The fine-tuned model has "the best quality metrics" yet "struggled to generate code for complex solutions" (p. 8); the authors attribute its low performance to too few fine-tuning samples (p. 9).
10. [A] AI models "may better avoid functional bugs than address structural code quality concerns" (p. 9).

## 8. Limitations stated by the authors
- [A] Possible cross-contamination of coding patterns or prompts between instances, affecting comparisons across zero-shot, few-shot and fine-tuned conditions (p. 10).
- [A] Prompt sensitivity: different wording could give significantly different results (p. 10).
- [A] Python only and competitive-programming style problems; limited generalisability to other languages and real-world software development (p. 10).
- [A] Only GPT-4 (GPT-4o) and a fine-tuned version; may not represent other LLMs (p. 10).
- [A] APPS lacks contextual information about the human-written code (p. 10).
- [A] Performance sample may not represent the population (p. 10).
- [A] LLM parameter and token-limit variations were not tested (p. 10).
- [A] SonarQube metrics may not capture all aspects of quality; its effort estimates may not reflect real developer effort (p. 10).
- [A] Fine-tuning used a limited number of rows due to resource constraints (p. 10).

## 9. Limitations we identified
- [I] Few-shot leakage: the few-shot prompt contains the human reference solutions to the same question (p. 4). Few-shot outputs can therefore copy or adapt the baseline itself, so few-shot vs human is not an independent comparison and the high few-shot Pass@1 (0.87, p. 8) may partly reflect this. Based on the prompt description, p. 4.
- [I] Quality and correctness are not linked: static-quality comparisons include LLM solutions that fail the tests (fine-tuned Pass@1 0.47, p. 8). "Fewer bugs" in SonarQube terms is not "more correct" code. The headline "LLM-generated code has fewer bugs" (p. 1) uses SonarQube's rule-based "bug" category, not functional failures. Based on p. 5 and p. 8.
- [I] Unit of analysis and denominators unclear: the number of human solutions and of zero-/few-shot solutions analysed is not reported (p. 3–4), and normalised percentages are described as "proportion of rows" (p. 5) without defining a row. Odds ratios therefore cannot be reconstructed from the paper.
- [I] Baseline quality: APPS human solutions are competitive-programming submissions written for correctness, not maintainability, as the authors themselves note (p. 9). They are a weak and possibly unfair baseline for maintainability claims.
- [I] Data contamination: APPS has been public since 2021 (p. 11), so GPT-4o may have seen its problems and solutions in training. The paper does not discuss this; its "cross-contamination" limitation (p. 10) concerns prompts, not training data.
- [I] Single sample per question at temperature 1.0 (p. 4), with no repeated runs, so run-to-run variance is unknown.
- [I] Pass@1 on 15 solutions per approach (p. 7–8) is too small to support the performance ranking (e.g. 0.87 vs 0.53).
- [I] Internal inconsistencies:
  - Few-shot Pass@1 is 0.86 in the introduction (p. 1) and 0.87 in Table V (p. 8).
  - An odds ratio is not a percentage, but the paper expresses ORs as percentages (OR 0.0005 written as "0.05% of the odds", p. 6). Under that convention, the largest bug OR in Table II (0.019, p. 8) is 1.9%, not "≤ 0.19%" as stated in Finding 7 (p. 9).
  - Several severity percentages in the text do not match Fig. 5. Examples: zero-shot introductory critical is 5.0% in the text (p. 5) but 6.6 in Fig. 5 (p. 7); few-shot introductory values (critical 9.8%, major 40.2%, p. 5) do not appear in Fig. 5, where that bar is empty (p. 7); fine-tuned competition minor is 30% in the text (p. 6) but Fig. 5 shows 40.0 (p. 7).
  - The code-smell paragraph says "a bug in a few-shot approach is half as likely as a bug in a human solution" (p. 7), mixing bugs with smells.
  - The limitations say "GPT-4" (p. 10) while the model is GPT-4o (p. 4).
- [I] Top-p = 1.0 is described as "ensuring the most probable token distributions were used" (p. 4); top-p = 1.0 in fact applies no nucleus truncation. Minor, but it shows imprecise reporting of the generation setup.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Few-shot prompts contain baseline solutions (p. 4). Possible training-data contamination with APPS (not discussed). Train/test disjointness for fine-tuning not reported (p. 4). The human baseline includes many solutions per question, while LLMs produce one, so issue counts per question are not comparable unless normalised. The normalisation is not fully specified (p. 5).
- External (generalisability of sample/context): [A] Python, algorithmic problems, one model family (p. 10). [I] Single-function stdin/stdout programs say little about multi-file applications, UIs or vibe-coded apps.
- Construct (do metrics measure the concept?): [A] SonarQube rules and effort estimates are proxies (p. 10). [I] Static "bugs" and "code smells" from the default profile are only a partial measure of maintainability. Effort-to-fix is SonarQube's rule-based remediation estimate, not a measured effort.
- Statistical conclusion (power, multiple comparisons, variance): [V] No CIs and no multiple-comparison correction (p. 8). [I] Odds ratios of 0.00 imply zero cells, where ORs are undefined without correction. A large Cliff's delta (−0.50) that is not significant suggests small or tied samples for the fine-tuned introductory set (p. 8).
- Reproducibility (data/code/setup reported?): [V] Replication package with scripts on Zenodo, public dataset, model version and decoding parameters reported (p. 4, p. 11). [I] Sample sizes per condition, fine-tuning hyper-parameters, the exact SonarQube version and the OR test are missing. Fine-tuned GPT-4o weights are proprietary, so exact regeneration may be impossible.

## 11. Future research directions
- Stated by authors [A]:
  - Explore parameter tuning (p. 10).
  - Use PEFT and data pruning instead of costly full fine-tuning (p. 9).
  - Study quality–performance–cost trade-offs in different domains (p. 10).
  - Try RAG and other LLMs; add more languages and quality metrics (p. 10).
  - Add a component that checks solution performance (p. 10).
  - Study links to educational outcomes (p. 10).
- Suggested by us [I]:
  - Report static quality only for solutions that pass the tests, so quality and correctness are evaluated jointly.
  - Use several samples per task with variance reporting.
  - Use a baseline of maintained, production-style human code.
  - Apply the same SonarQube pipeline to multi-file, application-level outputs (e.g. vibe-coded web apps) instead of single-function programs.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ3 (primary), RQ4, RQ2 (minor), RQ5.
- How it informs our work [I]:
  - It is a peer-reviewed (ESEM) direct comparison of LLM vs human code quality using SonarQube. It is a candidate template for the code-quality arm of a reconstruction study: default quality profile, bugs, smells, severity and remediation effort.
  - It shows that static quality and functional correctness can diverge sharply: the fine-tuned model has the best quality metrics but the lowest Pass@1. Any evaluation of reconstructed applications must therefore measure fidelity and quality jointly.
  - Its weaknesses are useful design lessons for RQ4/RQ5: baseline leakage, unreported N, tiny correctness sample, and no CIs or multiple-comparison correction.
  - Relevance is medium rather than high because the tasks are algorithmic snippets, not applications reconstructed from observable behaviour.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | GPT-4o solutions (zero-shot, few-shot, fine-tuned) had far lower odds of SonarQube-flagged bugs than APPS human solutions at all difficulty levels (OR 0.00–0.019, all p<0.001; the 0.00 implies a zero cell, so the minimum is not a real estimate) | 8 | V | weak (single model and study; N per group not reported; few-shot prompt contains baseline solutions) |
| RQ3 | Code-smell (maintainability) differences were mixed: zero-shot had 3.57× the odds of a smell vs human on introductory tasks, while fine-tuned had fewer smells; several comparisons were not significant | 8 | V | weak |
| RQ3 | SonarQube-estimated fix effort was lower for LLM code on introductory/interview tasks but not on competition tasks (human 6.95 min vs few-shot 7.33, fine-tuned 7.60) | 7 | V | weak |
| RQ3 | On competition-level problems LLM outputs carried more critical-severity issues than human code | 6 | A | weak |
| RQ2 | Functional correctness diverged from static quality: Pass@1 human 1.0, few-shot 0.87, zero-shot 0.53, fine-tuned 0.47 (fine-tuned had the best quality metrics) | 8 | V | weak (15 solutions per approach) |
| RQ4 | Comparison used SonarQube default profile, odds ratios, and Mann-Whitney U with Cliff's delta, without CIs or multiple-comparison correction | 5, 8 | V | moderate |
| RQ4 | The few-shot prompt included the human reference solutions of the same question, so few-shot vs human is not an independent comparison | 4 | I | moderate (directly from method description) |
| RQ5 | Authors call for other LLMs, more languages and metrics, RAG and cost–quality trade-off studies | 10 | A | weak |

## 14. Key quotes
> "LLM-generated code has fewer bugs and requires less effort to fix them overall." (p. 1)

> "the fine-tuned model solutions lost performance (0.47) compared to the few-shot model (0.86) in Pass@1" (p. 1)

> "current AI models may better avoid functional bugs than address structural code quality concerns." (p. 9)

> "Since the questions are not intended for use in a professional environment, the solutions may be prepared to be correct in the first place, leaving quality metrics as a low priority or even unobserved." (p. 9)

## Analyst notes
- Reading coverage: all 12 PDF pages read, including references. Figures 4–6 and Tables I–V were checked on the PDF images (pp. 6–8) because text extraction scrambled them. Figure 1 (architecture) was not inspected in detail; it is descriptive only.
- Uncertainties:
  - The exact number of solutions per dataset is not reported. This is the main obstacle to judging statistical strength.
  - Fig. 5 seems misaligned with its column labels, or the text reports different numbers; we report the text and table values and flag the mismatch.
  - We cite our arXiv PDF; the ESEM version may differ slightly.
