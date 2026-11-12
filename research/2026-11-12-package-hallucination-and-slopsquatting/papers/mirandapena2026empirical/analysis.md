---
key: mirandapena2026empirical
status: complete
evidence_basis: full-text
design: Empirical comparison of static-analysis, grammar, LLM-judge detection plus LLM repair and grammar-constrained decoding, with manual annotation of failures
dataset: DS-1000 (1,000), ODEX (550 library-requiring questions of 945), BigCodeBench-instruct (1,140); outputs of 6 LLMs
sample_size: 6 LLMs x 3 benchmarks; 600 manually annotated failure cases; repair on 5,502 erroneous samples
metrics: precision/recall on all errors; Imaginary Feature Recall (IFR); RIF; Pass@1; Execution Rate; IF%; Cohen's kappa; Spearman; latency
main_finding: Pyright detects 14-85% of library hallucinations (recall); manual ceiling 48.5-77%; LLM repair lowers hallucination share on DS-1000, not Odex/BigCode.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# An Empirical Analysis of Static Analysis Methods for Detection and Mitigation of Code Library Hallucinations

- Authors: Miranda-Pena, Clarissa; Reeson, Andrew; Paris, Cécile; Poon, Josiah; Kummerfeld, Jonathan K.
- Year / venue: 2026, arXiv (preprint)
- DOI: 10.48550/arxiv.2604.07755 · URL: https://arxiv.org/abs/2604.07755
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

**Source tier:** **Preprint (tier 3), not confirmed as peer-reviewed.**
- [A] The PDF header reads "Published in Transactions on Machine Learning Research (10/2026)". Page 1 gives "Reviewed on OpenReview" with a forum link, and the arXiv stamp is v3, 6 Nov 2026 (p. 1).
- `metadata.json` records `venue_kind: preprint`, and no TMLR DOI or OpenReview record has been verified.
- Orchestrator decision (2026-11-12): keep at preprint tier. TMLR acceptance is treated as an author claim.

## 1. Research objective
- [A] Quantify what static analysis can and cannot do to detect and mitigate *library hallucinations* in NL-to-code generation. A library hallucination is code that would only work if imagined libraries, functions, parameters or types existed (pp. 1, 3).
- [A] Establish an upper bound for static methods through manual analysis (pp. 1–2).

## 2. Research questions / hypotheses
- No formal RQs. The stated contributions are (p. 2):
  1. an analysis of static tools for detection and mitigation;
  2. manual hallucination annotations on three benchmarks;
  3. a docstring-to-grammar framework for constrained decoding.
- Implicit questions (pp. 5–11):
  - detection precision and recall (§5.1);
  - the upper bound, and the causes of misses (§5.1.1–5.1.2);
  - whether LLM repair guided by tool output fixes hallucinations (§5.2);
  - whether constrained decoding prevents them (§5.3).

## 3. Methodology
- Research design: [V] A comparative empirical evaluation with four parts (pp. 4–11):
  - three detectors plus a baseline;
  - repair with and without tool output;
  - constrained vs unconstrained decoding;
  - manual annotation of a sample of failures.

  It runs on three execution-based benchmarks with six generation models.
- Approach / model / intervention:
  - [V] **(1) Grammar.** A GBNF grammar auto-extracted from library docstrings via `inspect` and combined with the Python grammar. It is used for post-hoc checks and for constrained decoding in llama.cpp/Ollama. Its import rule validates packages "in the environment of the benchmark and Python built-in modules" (pp. 3–4).
  - [V] **(2) Off-the-shelf analysers.** Mypy and Pyright, with auto-generated type stubs (p. 4).
  - [V] **(3) Baseline judge.** o3-mini as an LLM judge, asked whether the code will execute (p. 4).
  - [V] **Repair.** o3-mini is given the code and the error, either alone ("o3+Self") or with Mypy/Pyright output (pp. 9–10).
- Baselines or comparison conditions (pp. 6, 9, 11): [V]
  - detection: the o3-mini judge;
  - repair: "No repair" and o3+Self;
  - mitigation: unconstrained decoding.

## 4. Dataset and sample
- Data source(s) (p. 5): [V]
  - DS-1000: 1,000 problems, 7 libraries;
  - ODEX: 945 problems, 79 libraries, 4 natural languages;
  - BigCodeBench-instruct: 1,140 problems, 139 libraries.
- Sample size (N) and unit:
  - [V] All questions of DS-1000 and BigCodeBench, plus "550 questions from RIG"; questions not needing imports were skipped (p. 5). [I] "RIG" is never defined and is probably ODEX.
  - [V] Six generation models (p. 5).
  - [V] Manual analysis: 200 failure cases per benchmark, 600 in total, sampled equally across claude-3, gpt-3.5, gpt-4 and Granite 3B (p. 6).
  - [V] Repair: erroneous samples numbered 2,210 for DS-1000, 2,001 for BigCode and 1,291 for Odex (p. 10).
- Sampling / selection method:
  - [V] The benchmarks were chosen because they combine an NL prompt that demands library use with test cases (p. 5).
  - How the manual sample was drawn within the strata is not reported.
- Data availability:
  - [V] Benchmarks are used under Apache-2.0 / CC-BY-SA-4.0 (p. 17).
  - [A] The annotation guideline is supplemental material (pp. 7, 17).
  - Release of the generated outputs or annotations: not reported.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] **Models.** Claude-3, GPT-4 and GPT-3.5 via API; Gemma2 2B, IBM-Granite 3B and Qwen3 8B open-weight (p. 5).
    - Temperature is 1 for the API models and 0.4 for the open models, "as reported in prior work" (p. 5).
    - Exact API model versions: not reported.
  - [V] **Granite responses.** The BigCodeBench responses came from the leaderboard and were re-run for the constrained comparison (p. 10).
  - [V] **Hardware.** "a local computer with an M2 processor, 8-core CPU, 10-core GPU, and 24GB RAM" (p. 17).
  - [V] **Decoding.** llama.cpp's parser, with an added state cache for the parser's pushdown automata. llama.cpp samples first and applies the grammar mask only when the sample is rejected (p. 4).
  - [V] **Grammar construction.** Converting the Python grammar to GBNF took about 4 h by hand. Each library-grammar step takes under a second (pp. 4, 16).
  - [V] **Detection time.** Mypy about 1 s; Pyright and the grammar about 2.5 s; o3-mini about 4 s (p. 19).
  - [V] **Constrained-decoding cost.** Unconstrained responses average 22.3 s, constrained 34.76 s (p. 11).
- Code availability: not reported (no repository link found).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] **Precision and recall on all errors.**
  - [V] **Imaginary Feature Recall (IFR):** recall on the examples containing Attribute, Import, Type or ModuleNotFound errors (p. 5).
  - [V] **RIF:** imaginary features as a share of the errors left after repair (p. 5).
  - [V] **Pass@1, Execution Rate (ER) and IF%.** IF% is the share of samples with one of the four error types (p. 5).
  - [V] **Manual-analysis measures:** Caught, TP (correctly identified for the right reason), Overlap, Capable (p. 7).
  - [I] RIF is a relative measure. It can rise when repair removes *other* errors while hallucinations stay the same, and fall when other errors remain. Changes in RIF are not changes in the absolute number of hallucinations.
- Statistical testing:
  - [V] Cohen's kappa for annotation agreement, average 0.79 (pp. 7, 18).
  - [V] Spearman correlation between the full and the validated benchmark: 0.98 for detection, 0.99 for constrained decoding, 0.88 for repair (p. 12).
  - No CIs, significance tests or multi-run variance.

## 7. Key findings
1. **Abstract figures.**
   - [A] LLMs use non-existent library features in "8.1-40% of responses" (p. 1).
   - [A] Static tools detect "16-70% of all errors, and 14-85% of library hallucinations" (p. 1).
   - [I] "14-85%" matches Pyright's IFR range in Table 10 (0.14–0.85, p. 20).
   - [I] "8.1-40%" and "16-70%" could not be matched to any table. Pyright's all-error recall is 0.16–0.82 (p. 6). The no-repair RIF is 8.1–44.9 (p. 10), but that is a share of errors, not of responses. Table 6 gives IF% of 4.4–22.2 for the open models (p. 11).
2. [V] **Detection recall on all errors** (Table 1, p. 6).
   - Pyright has the highest recall overall, e.g. 0.70 for claude-3 on DS-1000 and 0.82 for gpt-4 on Odex.
   - Grammar recall is 0.04–0.22.
   - o3-mini has high precision and low recall.
3. [V] **Detection recall on hallucinations (IFR)** (pp. 7, 20).
   - By method: Pyright 0.14–0.85; Mypy 0.03–0.70; grammar 0.06–0.20; o3-mini 0.02–0.78. o3-mini does better on the small models.
   - Automatic precision on hallucinations was 1, except one cell at 0.98.
   - [A] Mypy and the grammar do best on ImportError/ModuleNotFound; Pyright does better on Type/AttributeError (p. 6).
   - [V] **These are recall figures from automatic error matching.** In the manual sample, the share of hallucinations flagged for the right reason (TP) by the static tools is only 37.6% (DS-1000), 4.0% (Odex) and 10.0% (BigCode). The share flagged at all (Caught) is 56.7%, 19.0% and 23.0% (Table 2, p. 8).
4. [V] **Manual upper bound** (Table 2, p. 8).
   - Share of hallucinations each method could catch ("Capable"): static tools 77.0% (DS-1000), 70.5% (Odex), 48.5% (BigCode); grammar 18.0%, 10.5%, 7.0%.
   - [A] "after manual inspection we found that false positives mean the true upper bound is 77%" (p. 12).
5. [V] **Benchmark noise.**
   - Ambiguous input plus ambiguous output make up 36.9% of the sampled hallucinations in Odex, 34.1% in BigCode and 1.1% in DS-1000 (p. 9). In Table 3 these are input 6.6/7.5% plus output 30.3/26.6% (p. 8).
   - This supports the authors' "over 30%" claim for Odex and BigCode (p. 9).
   - Removing noisy items (3% / 7.7% / 6.1%) preserves model rankings (p. 12).
6. [V] **Repair raises execution rate and Pass@1** (Table 4, p. 9), e.g. Gemma2 2B on DS-1000: ER 47.2 → 77.9 with o3+Self.

   Its effect on the hallucination share (RIF, Table 5, p. 10) depends on the benchmark:
   - **DS-1000: RIF falls for every model and every repair method.** Examples: claude-3 9.1 → 2.7; Gemma2 2B 22.3 → 5.8–8.1; Qwen3 8B 25.4 → 6.1–13.4; Granite 3B 17.2 → 11.9–13.9.
   - **BigCode: roughly flat for the large models (within ±2 points); falls modestly in most small-model cells.** Gemma2 44.9 → 35.7–42.7; Granite 43.9 → 38.2–39.0; Qwen3 31.8 → 23.1 with Mypy, but 36.4 with Pyright.
   - **Odex: flat or slightly up for the large models; rises sharply for the small models.** claude-3 20.4 → 16.2–16.6; gpt-4 13.7 → 15.6–16.0; Gemma2 23.8 → 27.8–51.0; Granite 24.0 → 46.6–48.9; Qwen3 31.3 → 47.8–55.6.

   [A] The authors summarise this as "In most cases, there is no improvement in fixing hallucinations" (p. 10) and say the hallucination rate "remained unchanged across all benchmarks" (p. 12). Both overstate Table 5, which shows clear improvement on DS-1000. [I] Because RIF is relative (§6), none of these changes can be read as absolute reductions in hallucinations.
7. [V] **Constrained decoding** (Table 6, p. 11) changes IF% by small, mixed amounts:
   - Odex: Gemma 5.4 → 4.8; Granite 8.9 → 8.2; Qwen 6 → 4.4.
   - DS-1000: Granite 10.4 → 6.7, but Gemma 10.4 → 12.6.
   - Pass@1 sometimes drops.
   - It adds about 12 s per request.

## 8. Limitations stated by the authors
- [A] Python only. Other languages need a hand-converted grammar and an adapted script (pp. 4, 12).
- [A] The grammar cannot handle atypical aliases, because llama.cpp grammars cannot track state (p. 16). It also cannot link attributes imported via `from ... import` (p. 8).
- [A] Docstrings are incomplete (e.g. namespaces, dtype). This causes grammar errors and lowers Pass@1 (pp. 8, 10).
- [A] Static tools miss data-flow and control-flow cases, such as lambda/map/apply and changing types (pp. 7–8).
- [A] After agreement was checked, a single annotator labelled the remaining two-thirds (p. 7).
- [A] Memoisation gave no speed gain; latency needs further analysis (p. 19).

## 9. Limitations we identified
- [I] **Package existence is judged against the benchmark environment, not a registry.**
  - ModuleNotFoundError is defined as "does not exist in the environment and/or in real life" (p. 18), and the grammar validates imports against the benchmark environment (p. 4).
  - Real packages that are simply not installed are therefore merged with invented ones.
  - The paper says nothing about whether names exist on PyPI, or about squatting.
- [I] **Package-level results are a small, unseparated part.**
  - In the manual sample, the "Library" cause category (functions, parameters and constants defined in a library; Table 9, p. 19) is only 14.7% (DS-1000), 6.6% (Odex) and 6.0% (BigCode) (Table 3, p. 8).
  - Detection metrics are not broken down by cause, and ModuleNotFound (package-level) cases are not reported separately.
- [I] **Detection ranges overstate what the tools achieve.** IFR counts matched error types, but correct-for-the-right-reason detection by the static tools is 4.0–37.6% in the manual sample (p. 8).
- [I] **Authors' summary of repair is too negative.** As shown in §7 finding 6, the repair text (pp. 10, 12) contradicts Table 5 on DS-1000.
- [I] **Abstract ranges partly untraceable.** "8.1-40%" and "16-70%" could not be matched to any table; "14-85%" matches Pyright IFR (p. 20).
- [I] **Unspecified model versions and mixed temperatures.** API model versions are not given, and temperatures differ between closed (1.0) and open (0.4) models. This confounds model comparisons.
- [I] **Inconsistent annotation share.** The double-annotated share is "One third" on p. 7 but "25%" in the Table 8 caption (p. 18).
- [I] **Thin reproducibility and statistics.** No CIs, a single Pass@1 sample, and no reported code release.

## 10. Threats to validity
- Internal:
  - o3-mini is both a detector baseline and the repair model.
  - Granite outputs come from different sources across experiments (p. 10).
  - RIF is a relative metric, so its direction can reflect changes in other error types.
- External:
  - Python only, three benchmarks.
  - Older closed models (Claude-3, GPT-3.5/4) and small open models.
  - No agentic setting.
- Construct:
  - "Hallucination" is defined by runtime error types against an installed environment.
  - Benchmark underspecification inflates counts; the authors partly correct for this (pp. 9, 12).
  - Automatic detection credit exceeds correct-reason detection (p. 8).
- Statistical conclusion: no tests or CIs. Annotation agreement is substantial (kappa 0.79) (p. 7).
- Reproducibility: hardware and benchmarks are reported; model versions, code and outputs are not.

## 11. Future research directions
- Stated by authors [A]:
  - use the model's internal states for detection (p. 12);
  - extend static tools with data-flow and control-flow tracking (pp. 7–8);
  - build benchmarks that accept multiple valid solutions and specify input/output types (p. 9);
  - study where hallucinations originate (p. 12);
  - extend to other languages (p. 4).
- Suggested by us [I]:
  - add a registry-existence layer (PyPI/npm) to the static pipeline, so "not installed", "does not exist" and "exists but is a squat" are kept apart;
  - report package-level (ModuleNotFound) results and absolute hallucination counts after repair separately.

## 12. Relevance to our research
- Research questions addressed (RQ ids):
  - RQ3: static analysis and constrained decoding as cheap defences, with their cost and effectiveness.
  - RQ4: ground truth taken from the installed environment, benchmark-noise pitfalls, annotation reliability.
  - RQ1: hallucination shares across small and large models (partial).
  - RQ5: laptop feasibility.
- How it informs our work [I]:
  - **Proof of laptop feasibility.** The whole study ran on an M2 machine with 24 GB RAM, including constrained decoding of 2–8B models (p. 17). It is the only laptop-class run in this batch.
  - **Cheap import-level screening, with a catch.**
    - Mypy and Pyright with type stubs take about 1–2.5 s per sample (p. 19), a cheap check before running the code.
    - Their automatic detection credit overstates correct-reason detection (p. 8).
    - They check the *installed environment*, not the registry, so they cannot tell a slopsquatted package (which installs fine) from a legitimate one. A registry-aware check is still needed.
  - **Repair after detection is benchmark-dependent.** It lowered the hallucination share on DS-1000 but not on Odex for small models (p. 10). A defence study should report absolute hallucination counts, not just RIF.
  - **Constrained decoding is not worth it here:** about +12 s per request for small, inconsistent gains (p. 11).
  - **Measurement lesson:** separate benchmark noise from model hallucination, and hand-validate a subset.
  - **Evidence strength: moderate–weak.** It is a preprint (TMLR acceptance unverified) with a sound manual analysis, but its relevance at the package level is indirect.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Static tools' recall on library hallucinations (IFR) is 0.03–0.85 by model/benchmark (Pyright 0.14–0.85); but in a manual sample, correct-for-the-right-reason detection is only 37.6% (DS-1000), 4.0% (Odex), 10.0% (BigCode) | 8, 20 | V | moderate |
| RQ3 | Manual analysis caps static detection of hallucinations at 48.5–77% | 8, 12 | V | moderate |
| RQ3 | LLM repair raises execution rate; the hallucination share of remaining errors (RIF) falls on DS-1000 for all models (e.g. claude-3 9.1 → 2.7), is roughly flat for large models on BigCode, and rises on Odex for small models (Qwen3 8B 31.3 → 55.6); the authors' "no improvement in most cases" overstates this | 9, 10, 12 | V (table) / A (summary) | moderate |
| RQ3 | Grammar-constrained decoding gives small, mixed IF% changes at about +12 s per request | 11 | V | moderate |
| RQ4 | Ambiguous input/output in the benchmark accounts for 36.9% (Odex) and 34.1% (BigCode) of sampled hallucinations, vs 1.1% for DS-1000 | 8, 9 | V | moderate |
| RQ4 | ModuleNotFound "hallucinations" are judged against the installed environment, not a package registry; library-definition causes are only 6.0–14.7% of the sample | 4, 8, 18 | V | moderate |
| RQ5 | Full pipeline incl. constrained decoding of 2–8B models ran on an M2 laptop (24 GB RAM); detection takes 1–4 s per sample | 17, 19 | V | moderate |

## 14. Key quotes
> "While repair consistently improves executability, imaginary features prove resistant." (p. 10)

> "after manual inspection we found that false positives mean the true upper bound is 77%" (p. 12)

> "This module does not exist in the environment and/or in real life." (p. 18)

## Analyst notes
- Reading coverage: all 24 PDF pages, including appendices B–D. Figures 1, 3 and 6–12 are charts; we relied on the tables (Table 10 mirrors Figure 1) and the text.
- Uncertainties:
  - TMLR acceptance is an author claim; the paper is kept at preprint tier per the orchestrator decision.
  - "RIG" is undefined (p. 5).
  - "8.1-40%" and "16-70%" in the abstract are untraced.
- Critical-review fixes (2026-11-12):
  - **Applied:**
    - RIF/repair claim corrected against Table 5 in the main finding, §6, §7.6, §9, §10, §12 and §13;
    - abstract range traceability (14–85% = Pyright IFR);
    - TP alongside recall;
    - Library-cause shares;
    - preprint tier.
  - **Partly applied:** the review's "≈27–30%" for benchmark underspecification counts only ambiguous *output*. Page 9 gives 36.9% (Odex) and 34.1% (BigCode) for ambiguous input plus output, consistent with Table 3 (p. 8). That supports the authors' "over 30%", so the RQ4 row is now [V] with those figures.
