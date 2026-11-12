---
key: yildiz2025benchmarking
status: complete
evidence_basis: full-text
design: benchmark paper + comparative evaluation of plain LLM, dependency-augmented LLM and ReAct agent across 4 prompting strategies and 4 foundation models
dataset: JITVul, 879 CVEs from PrimeVul (91 CWEs, C/C++), each target function paired with vulnerability-introducing and vulnerability-fixing commit
sample_size: 1,758 paired samples (879 vulnerable, 879 benign) from 879 CVEs; extra non-paired PrimeVul test set 695 vul / 25,216 benign
metrics: F1, pairwise accuracy (pAcc); share of pairwise error types; tool-invocation counts
main_finding: ReAct agents get best pairwise accuracy but all GPT-4o/4o-mini methods stay at pAcc <=20.17% despite F1 48-66%; F1 is misleading on balanced data.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Benchmarking LLMs and LLM-based Agents in Practical Vulnerability Detection for Code Repositories

- Authors: Yildiz, Alperen; Teo, Sin G; Lou, Yiling; Feng, Yebo; Wang, Chong; Divakaran, Dinil Mon
- Year / venue: 2025, Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (published)
- DOI: 10.18653/v1/2025.acl-long.1490 · URL: https://doi.org/10.18653/v1/2025.acl-long.1490
- Source text: `fulltext.txt` (page refs = PDF page index; printed pages 30848–30865). Identity confirmed: title and authors on p. 1 match metadata.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
Provide a practical benchmark for just-in-time (JIT, i.e. commit-triggered) repository-level vulnerability detection with interprocedural context and pairwise (vulnerable vs patched) evaluation, and use it to compare LLMs with LLM-based ReAct agents [A] (p. 1, p. 2).

## 2. Research questions / hypotheses
- No numbered RQs. Four comparisons: detection method (p. 7), prompting strategy (p. 8), foundation model (p. 8), pairwise error analysis (p. 8) [V].
- Three stated requirements for practical benchmarks: interprocedural context, scalability, pairwise comparison [V] (p. 3, p. 4).

## 3. Methodology
- Research design: benchmark construction plus comparative evaluation [V] (p. 4, p. 5).
- Approach / model / intervention: (1) Plain LLM — target function only; (2) Dep-Aug LLM — adds Top-5 lexically similar callers/callees (Jaccard), reproducing VulEval; (3) ReAct agent with tools get_callers, get_callees, get_definition (CFlow + CTags, LangChain) [V] (p. 5, p. 6). Each in four variants: vanilla, CoT ("Solve this problem step by step..."), few-shot (10 hand-made vulnerable/benign pairs from CWE Top-25 web pages), CoT+FS [V] (p. 5, p. 6).
- Baselines or comparison conditions: the three LLM settings against each other; no SAST tools, no fine-tuned deep-learning detectors [V] (p. 5). A random-guessing reference (22.70%) is cited from Ding et al. (p. 7).

## 4. Dataset and sample
- Data source(s): PrimeVul (CVE fixed in a single commit modifying a single function); vul-intro commit approximated by tracing the target function's history back to its last modification into the vulnerable version [V] (p. 4, p. 5).
- Sample size (N) and unit: 879 CVEs, 91 CWEs (max 10 CVEs per CWE), 1,758 samples (879 vul, 879 ben) [V] (p. 4, p. 5). Repositories: mean 2,955.9 files, 91% C / 9% C++, mean 988.8 KLoC (median 297.6, SD 1,991.2); target function mean 696.4 LOC [V] (p. 5).
- Sampling / selection method: random selection of 879 PrimeVul CVEs ensuring CWE coverage [V] (p. 4).
- Data availability (public? link?): "We release all code and data at this repository" (p. 2); the URL is a hyperlink not present in the extracted text.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: GPT-4o-mini and GPT-4o at temperature 0; Transformers v4.52.0, LangChain v0.3.14 [V] (p. 6). Llama-3.1-8B and DeepSeek-Coder-V2-16B in Appendix B [V] (p. 8, p. 15). Number of runs: not reported (one implied by temperature 0). Number of pairs evaluated per setting: not reported (see Analyst notes). Token use, cost and runtime: not reported.
- Code availability: yes, per p. 2.

## 6. Evaluation metrics
- Metric — what it measures — why chosen: F1 (common metric) and pairwise accuracy pAcc = share of pairs where both versions are labelled correctly, inspired by PrimeVul, to test whether methods capture the vulnerability rather than surface patterns [V] (p. 6). Error types: pairwise vulnerable, pairwise benign, pairwise reversed [V] (p. 8).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): none reported.

## 7. Key findings
1. GPT-4o-mini F1/pAcc — Plain: 56.00/3.36 (vanilla), 65.10/3.36 (CoT), 48.74/7.56 (FS), 64.65/11.76 (CoT+FS); Dep-Aug: 52.68/2.05, 66.05/4.86, 48.23/7.27, 65.01/4.68; ReAct: 56.63/12.61, 56.93/16.81, 56.81/20.17, 51.06/14.29 — [V] (p. 6, Table 2).
2. GPT-4o F1/pAcc — Plain: 65.96/1.02, 62.22/15.02, 62.77/4.44, 64.44/17.63; Dep-Aug: 63.30/1.03, 62.60/18.66, 62.03/2.39, 61.12/18.79; ReAct: 57.77/17.63, 58.07/19.13, 56.42/18.91, 52.61/18.89 — [V] (p. 6, Table 2).
3. ReAct agents have higher pAcc than other methods for every prompting strategy (gains 0.1 to 16.61 points); Plain/Dep-Aug have higher F1 in most settings (4.15–13.95 points) — [V] (p. 7). Average ReAct pAcc gain over Dep-Aug: 9.46 (4o-mini) and 8.42 (4o) — [V] (p. 7).
4. LLM methods label >90% of samples vulnerable in some settings; precision is around 50% for all methods on the balanced benchmark, so F1 rewards over-prediction — [V]/[A] (p. 7).
5. On the original non-paired PrimeVul test set (695 vul / 25,216 ben), GPT-4o-mini F1 falls to 5.41–12.21 — [V] (p. 7, Table 3).
6. Dep-Aug does not consistently beat Plain and sometimes lowers pAcc, possibly due to noisy retrieved context — [V]/[A] (p. 7).
7. The most common pairwise error is "both vulnerable": ~40–95% for LLMs, ~35–50% for ReAct — [V] (p. 8).
8. ReAct calls tools far more on the vulnerable than the benign version (5.85 vs 1.79, GPT-4o-mini vanilla) — inconsistent analysis — [V] (p. 9).
9. Llama-3.1-8B ReAct agents often fail output formatting and default to "benign" (F1 3.28–14.67); DeepSeek-Coder-V2 Dep-Aug with CoT+FS reaches F1 82.09 and pAcc 69.24, the best result in the paper, while its ReAct agent stays at pAcc ≤21.39 — [V] (p. 8, p. 15, Table 4).

## 8. Limitations stated by the authors
- [A] Vul-intro commits may be traced imperfectly; some instances manually inspected (p. 9).
- [A] Label-balanced dataset may bias F1 comparisons (p. 9).
- [A] Missing statistics such as the share of interprocedural vulnerabilities; annotation hard to scale (p. 9).

## 9. Limitations we identified
- [I] No SAST or deep-learning baselines and no cost data, so the paper cannot answer LLM-vs-SAST/DL questions directly. Based on p. 5–6.
- [I] All GPT-4o/4o-mini settings have pAcc ≤20.17%, below the 25% expected from independent random labelling of each pair member; "ReAct is better" means "less bad". Based on Table 2 (p. 6).
- [I] The headline "ReAct agents better at pairwise" is not robust across models: with DeepSeek-Coder-V2, Dep-Aug LLM is far better (pAcc 69.24 vs ≤21.39). Based on Table 4 (p. 15).
- [I] Data leakage is not discussed: PrimeVul CVEs and fixes are public and likely in GPT-4o training data. Based on p. 4 (no contamination analysis found in the text).
- [I] No repeated runs, variance or significance tests; differences of a few points (e.g. 0.1-point pAcc gain) are not interpretable. Based on p. 6–7.
- [I] Few-shot examples are single-function CWE web-page snippets, which may not suit interprocedural agents (authors note this too, p. 8).

## 10. Threats to validity
- Internal (confounds, leakage, selection): possible pretraining contamination; vul-intro approximation (p. 9); unclear per-setting sample sizes.
- External (generalisability of sample/context): C/C++ only (91% C), PrimeVul single-function fixes, OpenAI models mainly (p. 5, p. 6).
- Construct (do metrics measure the concept?): pAcc captures discrimination of vulnerable vs patched code; F1 on a balanced set overstates usefulness (p. 7).
- Statistical conclusion (power, multiple comparisons, variance): no tests, no variance, many configurations compared.
- Reproducibility (data/code/setup reported?): code and data released (p. 2); prompts in Appendix A (p. 12, p. 13).

## 11. Future research directions
- Stated by authors [A]: evaluation guidelines for JIT benchmarking; agent-oriented prompting strategies; robust reasoning models for vulnerability analysis (p. 2, p. 8); more benign commits for F1 (p. 9); code-specific LLMs optimised for agents (p. 15); integrate constraint solving or program analysis (p. 9).
- Suggested by us [I]: add SAST (CodeQL/Semgrep) and fine-tuned DL baselines on JITVul pairs; report cost and contamination checks.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (LLM-only), RQ2, RQ5.
- How it informs our work [I]: mainly methodological evidence for RQ2 — F1 on balanced data looks moderate (~50–66%) while pairwise accuracy shows near-random discrimination, explaining why reported LLM effectiveness varies across studies. No direct LLM-vs-SAST comparison.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | GPT-4o/4o-mini plain, dependency-augmented and ReAct detectors reach F1 48–66% but pairwise accuracy only 1.02–20.17% on 879 CVE pairs | p. 6 | V | moderate |
| RQ1 | ReAct agents give the highest pAcc for every prompting strategy with GPT-4o/4o-mini (gains up to 16.61 points) | p. 7 | V | weak |
| RQ2 | F1 is distribution-sensitive: GPT-4o-mini F1 drops from ~49–65% (balanced pairs) to 5.41–12.21% on non-paired PrimeVul (695 vul / 25,216 ben) | p. 6, p. 7 | V | moderate |
| RQ2 | LLM methods label >90% of samples vulnerable in some settings, with precision ~50%, inflating F1 | p. 7 | V | moderate |
| RQ2 | With DeepSeek-Coder-V2, Dep-Aug LLM reaches F1 82.09 / pAcc 69.24, contradicting the agent advantage seen with GPT models | p. 15 | V | weak |
| RQ5 | Most frequent failure is labelling both vulnerable and patched versions vulnerable (40–95% of LLM failures); agents analyse pairs inconsistently | p. 8, p. 9 | V | moderate |

## 14. Key quotes
> "A higher F1 score does not necessarily indicate a detection method's superior ability to capture vulnerability characteristics." (p. 7)

> "precision remains similar across methods, around 50%, as observed on our label-balanced benchmark" (p. 7)

## Analyst notes
- Reading coverage: all 18 PDF pages read, including Appendices A–C (prompts, Llama/DeepSeek results, case studies CVE-2019-15164 and CVE-2019-3877).
- Uncertainties: the number of pairs per setting is not stated. Every Plain and ReAct pAcc for GPT-4o-mini and Llama-3.1 is an exact multiple of 1/119 (e.g. 3.36 = 4/119, 20.17 = 24/119, 0.84 = 1/119), while GPT-4o values match k/879. This suggests some settings were evaluated on ~119 pairs, or after excluding failed runs, but the paper does not say so; treat cross-setting comparisons cautiously ([I], arithmetic on Table 2 p. 6 and Table 4 p. 15). "Improvements ... 0.1% to 16.61%" are percentage points. The 22.70% random-guessing figure is cited from Ding et al., not computed here (p. 7). Quote 2 is joined across a hyphenated line break ("sim-ilar").
