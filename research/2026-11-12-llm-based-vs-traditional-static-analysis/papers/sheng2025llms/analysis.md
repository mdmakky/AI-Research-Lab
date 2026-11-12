---
key: sheng2025llms
status: complete
evidence_basis: full-text
design: Narrative (non-systematic) survey with keyword-driven, iterative venue search; no quality assessment; descriptive counts, no meta-analysis
dataset: Top security/SE venues (S&P, USENIX Sec, CCS, TSE, ...) + keyword searches; databases not reported; 2019-2024
sample_size: 58 highly relevant studies (from ~500-600 screened; >80 papers discussed)
metrics: Counts/shares of models, languages, techniques across studies; catalogue of 42 datasets (Table 4); per-study F1 listing (Table 5)
main_finding: LLM vulnerability detection research is mostly function-level C/C++ snippet classification; dataset quality/leakage, cross-file context, robustness and explainability are the key open challenges.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# LLMs in Software Security: A Survey of Vulnerability Detection Techniques and Insights

- Authors: Sheng, Ze; Chen, Zhicheng; Gu, Shuning; Huang, Heqing; Gu, Guofei; Huang, Jeff
- Year / venue: 2025, ACM Computing Surveys (published)
- DOI: 10.1145/3769082 · URL: https://doi.org/10.1145/3769082
- Source text: `fulltext.txt` (page refs = PDF page index)
- **Version analysed:** arXiv:2502.07049v2 (12 Feb 2025) (p. 1). This is the preprint of the ACM Computing Surveys article, not the typeset CSUR version. `kaniewski2026systematic` lists the published version as Sep 2025 with a 2017–2025 time frame (p. 4 of that paper), so the published content may differ from what is analysed here.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

Convention for this survey: counts about the survey's own corpus that appear in its own tables, figures or "Finding" boxes are marked [V]. They are the survey's own data, although we cannot re-check the underlying extraction. Anything reported about results of individual primary studies (F1 scores, accuracies) is second-hand and marked [A], never [V].

## 1. Research objective
- [A] Survey the use of LLMs for software vulnerability detection: problem formulation, model selection, techniques, datasets, metrics, challenges and research directions (p. 1).
- [A] Claims to be "the first comprehensive survey" on strengths and weaknesses of LLMs in vulnerability detection (p. 2). It nevertheless acknowledges `zhou2025large` as prior work and differentiates itself by newer models (GPT-4o, o1, Claude 3.5 Sonnet), benchmark/metric analysis and detection-specific detail (p. 5).
- [A] Motivation: traditional static and dynamic analysis tools suffer from high false-positive rates, low efficiency and heavy effort across many vulnerability types (p. 1–2).

## 2. Research questions / hypotheses
- RQ1: What LLMs have been applied to vulnerability detection? (p. 2)
- RQ2: What benchmarks, datasets and metrics have been designed to evaluate vulnerability detection? (p. 3)
- RQ3: What techniques have been used in LLMs for vulnerability detection? (p. 3)
- RQ4: What challenges do LLMs face in detecting vulnerabilities, and what are potential directions? (p. 3)
- No hypotheses.

## 3. Methodology
- Research design: narrative survey with a keyword-driven, iterative selection. It is **not** a protocol-based systematic review: no SLR guideline is cited, there is no search string or database list, no formal inclusion/exclusion table and no quality assessment (p. 3–4). `kaniewski2026systematic` also classifies it as non-SLR (✗) (p. 4 of that paper).
- Approach: started from top-tier security venues (S&P, USENIX Security, CCS) and journals such as IEEE TSE. Then searched with key terms ("vulnerability detection", "LLM", "large language model", "AI"), repeated every three weeks over two months (p. 3–4).
- Inclusion/exclusion [A]: in scope are LLM-based vulnerability detection studies, primarily on C/C++, Java and Solidity. Excluded are studies using traditional ML (CNN, RNN, LSTM) and studies unrelated to vulnerability detection, such as malware analysis or network intrusion detection (p. 3–4).
- Quality assessment: not reported (none described).
- Baselines or comparison conditions: not applicable. The survey does not compare LLMs with SAST or DL detectors, and it explicitly excludes traditional ML/DL approaches (p. 3).
- Number of reviewers, screening procedure, agreement: not reported.

## 4. Dataset and sample
- Data source(s): top security/SE venues plus keyword searches (p. 3–4). The databases used are not reported.
- Sample size (N) and unit: 58 "highly related" studies, within "more than 80 papers" selected from "over 500" screened (p. 3), or "approximately 500-600" screened (p. 4) [A]. The language statistics are based on "56 selected papers" (p. 10), not 58.
- Time window: 2019–2024 (p. 3). NVD CVE statistics were collected until 3 November 2024 (Table 3, p. 10).
- Sampling / selection method: iterative keyword search, see section 3. Preprints are included: the authors estimate that about 60% of research in the area appears as arXiv preprints (p. 26). The share of preprints in their own corpus is not reported.
- Data availability: a GitHub list of papers is maintained (p. 1). An extraction sheet is not reported.

## 5. Experimental setup
- Procedure, settings, tools: data extraction fields are not reported. The analysis is organised by RQ, with "Finding" boxes I–IX (p. 11–25).
- Code availability: not applicable; a paper list is on GitHub (p. 1).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: the survey uses counts and shares of models, languages and techniques. It also catalogues the metrics used by primary studies: accuracy, precision, recall, F1 and MCC for imbalanced data; BLEU and ROUGE for generated descriptions; execution time for efficiency (p. 14). Table 5 lists one F1 score per fine-tuning study, each on a different dataset (p. 18).
- Statistical testing: none; not reported.

## 7. Key findings
1. Language focus of studies: C/C++ 50%, Java 21.1%, Solidity 11.8%, other (Python, PHP, Go) 16.6% — [V] (Finding I, p. 11)
2. Model usage: 33 distinct LLMs across 58 studies; GPT-4 is the most used (29 instances), then GPT-3.5 (25). By architecture: encoder-only 24.2%, encoder-decoder 8.7%, decoder-only 67.1% of usage — [V] (p. 8–9)
3. Datasets: 42 datasets are catalogued, mostly function- or file-level and C/C++. C/C++ accounts for about 60% of dataset coverage, and repository-level datasets are scarce. Only MAGMA and CWE-Bench-Java are repository-level (Table 4, p. 13; Finding II, p. 13) — [V]
4. About 40 studies (stated as 83%) analyse isolated code snippets. The authors argue that LLM performance on snippets exceeds what is seen in real-world detection ([37]) — [A] (p. 20)
5. LLMs and static analysis: for full-codebase analysis, "LLMs typically assist static analysis tools or support fuzzing tasks" rather than performing standalone analysis. Commit-level methods combine commits with static analysis results — [A] (p. 20)
6. Neuro-symbolic approaches (e.g. CodeQL or Bear combined with LLMs) "have shown promise on large-scale projects", but they still need better taint propagation modelling, more efficient LLM reasoning and cross-language adaptation — [A] (p. 3)
7. 41.3% of studies use code-processing techniques (AST/CFG/DFG, RAG, slicing). Gains over direct prompting are "modest" and shrink for complex cross-file vulnerabilities. Larger models' own gains "tend to outweigh" these preprocessing gains — [V] for the share / [A] for the interpretation (Finding III, p. 16)
8. Benchmark sensitivity, second-hand: Ding et al. (our `ding2025vulnerability`) report F1 of only 0.21 on PrimeVul. Guo et al. report CodeBERT at 0.099 F1 on PrimeVul but 0.66 on Choi2017. Table 5 reports F1 of 0.21–0.99 across different datasets — [A] (p. 18–19)
9. Vulnerability-type imbalance: memory-related vulnerabilities reach higher detection accuracy, while logic vulnerabilities are under-explored. One cited study reports high accuracy on CWE-787 but poor accuracy on CWE-862 — [A] (p. 3, p. 22)
10. LLMs detect vulnerabilities well in simple synthetic single functions, even zero-shot, but need much more context for larger projects. Callee functions may rely on their callers for protection, which causes wrong conclusions when they are analysed in isolation — [A] (p. 22)
11. LLMs lack robustness to perturbations and give inconsistent, run-to-run variable explanations, even when the detection itself is correct — [A] (p. 23)
12. Key challenges listed for LLM detection: data leakage that inflates metrics, understanding complex context, positional bias in long contexts, and high false-positive rates with poor zero-day performance — [A] (p. 14)

## 8. Limitations stated by the authors
- [A] Comprehensiveness: about 60% of the research appears only as arXiv preprints, and terminology variation may cause missed papers. Mitigation: keywords were extracted from published papers, and selection was refined over two months (p. 26).
- [A] Future versions will add localisation, assessment and patching tasks (p. 26).

## 9. Limitations we identified
- [I] Weak review methodology. There is no search string, no database list, no formal criteria, no quality appraisal and no PRISMA-style counts (p. 3–4). Its corpus-level statistics are therefore less reliable than those of a protocol-based SLR such as `kaniewski2026systematic`, and the survey should be weighted lower for "state of the field" claims.
- [I] Internal numeric inconsistencies, all from the text:
  - 58 studies (p. 8) vs 56 papers used for the language statistics (p. 10).
  - "approximately 40 studies (83%)" (p. 20) implies a denominator of about 48, not 58.
  - Minimum fine-tuning dataset size is "at least 10K samples" (p. 19) vs "at least 100,000 examples" (p. 24).
  - Encoder models are said to "dominate non-fine-tuning studies (72.4%)" (p. 10), while decoder-only models are 67.1% of overall usage and GPT-4/GPT-3.5 top the usage table (p. 9). With only about 30% of studies fine-tuning (p. 19), these figures are hard to reconcile.
- [I] Metric definition error: precision is described as the "true positive rate" (p. 14). True positive rate is recall. This is minor but signals limited editorial checking.
- [I] Possible citation mismatch: the CWE-787 vs CWE-862 performance contrast is attributed to [36] (p. 22). In the reference list, [36] is a 2021 repair paper ("Beyond Tests: Program Vulnerability Repair via Crash Constraint Extraction", p. 28). The intended source is probably [37] (Gao et al. 2023, "How far have we gone in vulnerability detection using large language models"), but this is unverified. Do not reuse this claim without checking the primary source.
- [I] Table 5 puts F1 scores from different datasets and tasks side by side (0.21 on PrimeVul to 0.99 on a custom Solidity set) (p. 18). These numbers are not comparable, and the "F1 near 0.9" conclusion (Finding V, p. 19) leans on custom or easier datasets.
- [I] No LLM-vs-SAST or LLM-vs-DL synthesis, despite the motivation in the abstract that traditional tools have high false-positive rates (p. 1). The claim that LLMs "typically assist static analysis tools" (p. 20) is a characterisation, not a quantified comparison.
- [I] Includes smart-contract (Solidity) studies (p. 4), which our project and `kaniewski2026systematic` treat as a separate domain. Corpus shares are therefore not directly comparable with Kaniewski's.

## 10. Threats to validity
- Internal (confounds, leakage, selection): selection is unsystematic and venue-anchored, and no quality filter is applied (p. 3–4). Preprint share not reported. The survey itself warns that primary studies suffer from data leakage that inflates their metrics (p. 14, p. 25).
- External (generalisability of sample/context): the corpus covers 2019–2024 and is C/C++-heavy (50%) (p. 11). It includes Solidity (p. 4).
- Construct (do metrics measure the concept?): percentages such as ">95% of studies report that code complexity…" (p. 22) and "100% of recent studies" adopting CoT for models above 10B (p. 18) are given without denominators or a coding scheme.
- Statistical conclusion: not applicable; F1 values are listed, not pooled.
- Reproducibility: the paper list is on GitHub (p. 1). The search protocol and extraction data are not reported.

## 11. Future research directions
- Stated by authors [A]:
  - Move beyond snippet classification to real-world problems (p. 20–22):
    - full-scale and incremental (commit-level) detection
    - vulnerability reproduction via fuzzers/PoCs, to reduce false positives
    - repair validated by tests
    - CWE-specific detection
    - classification and severity assessment
  - Represent vulnerability semantics better (p. 22–23):
    - let LLMs explore repository code dynamically
    - optimised AST/CFG/DFG representations
    - specialised agents
    - external tools and RAG
  - Address intrinsic LLM limits (p. 24):
    - fine-tune frontier LLMs
    - vulnerability-specific and repository-adaptive fine-tuning
    - ensembles to reduce false positives
    - domain-adaptive pre-training
    - adaptive/continual learning
  - Datasets (p. 25):
    - accurate labels, minimal leakage (obfuscation, synthesis, updated datasets) and rich repository-level annotations
    - small, verified, community-maintained test sets
    - augmentation for long-tail vulnerability types
  - Improve neuro-symbolic (static analysis + LLM) approaches: taint propagation modelling, efficient reasoning, cross-language adaptation (p. 3).
- Suggested by us [I]: none of the directions asks for controlled head-to-head comparisons of LLMs with SAST or DL detectors on the same leakage-controlled benchmark. That absence is directly relevant to our RQ1/RQ5 gap analysis (pending a novelty check).

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2 (dataset catalogue, granularity, leakage, metric usage), RQ3 (LLM-assisted static analysis and neuro-symbolic directions, qualitative only), RQ4 (language focus, memory vs logic vulnerabilities, CWE variation), RQ5 (challenges and directions).
- How it informs our work [I]: a peer-reviewed (CSUR) but methodologically light survey. Its main value is three things:
  - the dataset catalogue (Table 4);
  - the explicit challenge list (leakage, cross-file context, false positives, robustness, explainability);
  - the qualitative statement that, in practice, LLMs mostly assist static analysis rather than replace it.

  Cite its numbers cautiously, given the internal inconsistencies above, and cite primary studies for any performance figure.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | The survey offers no quantified LLM-vs-SAST/DL comparison; it states that for full-codebase analysis LLMs typically assist static analysis tools or fuzzing rather than performing standalone analysis | 20 | A | weak |
| RQ2 | About 40 studies (83% as stated) evaluate isolated code snippets, where LLM performance exceeds real-world detection performance | 20 | A | weak |
| RQ2 | Existing datasets are narrowly scoped, mislabelled and affected by data leakage that inflates metrics; repository-level datasets are scarce (2 of 42 catalogued) | 3, 13, 25 | A | moderate |
| RQ2 | The same model family scores very differently by benchmark (e.g. CodeBERT 0.099 F1 on PrimeVul vs 0.66 on Choi2017, second-hand) | 19 | A | weak |
| RQ3 | Code-processing techniques (AST/CFG/DFG, RAG, slicing) are used in 41.3% of studies with only modest gains that shrink for cross-file vulnerabilities | 16 | V | weak |
| RQ3 | Neuro-symbolic approaches (CodeQL/Bear + LLM) show promise on large projects but need better taint modelling and efficiency | 3 | A | weak |
| RQ4 | 50% of studies target C/C++, 21.1% Java, 11.8% Solidity | 11 | V | weak |
| RQ4 | Memory-related vulnerabilities are detected more accurately than logic vulnerabilities (second-hand claim; the CWE-787 vs CWE-862 example is cited to a mismatched reference [36]) | 3, 22 | A | weak |
| RQ5 | Main open challenges: limited problem scope, complex vulnerability semantics and context, LLM robustness and explanation consistency, lack of high-quality datasets | 20–25 | A | moderate |

## 14. Key quotes
> "LLMs typically assist static analysis tools or support fuzzing tasks" (p. 20)

> "Existing datasets are narrowly scoped and have a data leakage problem." (p. 3)

> "Our analysis reveals that 41.3% of studies employed code processing techniques" (p. 16)

## Analyst notes
- Reading coverage: all 26 body pages read (abstract to conclusion, Tables 1–6, Findings I–IX). The reference list (p. 26–33) was consulted for refs [24], [36], [37], [53], [66] and [121]. Figures 1–12 are images and do not appear in the text layer; their content was taken from the running text.
- Version: arXiv v2 (Feb 2025). The ACM CSUR version (DOI 10.1145/3769082) was not compared and may differ in corpus and time window.
- Overlaps with our corpus: the survey cites IRIS ([66], our `li2024iris`) and Ding et al. ([24], our `ding2025vulnerability`).
- Funding / conflict of interest: not reported.
- Uncertainties: see the inconsistencies in section 9. The 83% denominator and the 72.4% vs 67.1% architecture figures could not be resolved from the text.
