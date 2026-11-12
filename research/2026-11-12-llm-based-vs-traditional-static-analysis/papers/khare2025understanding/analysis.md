---
key: khare2025understanding
status: complete
evidence_basis: full-text
design: Empirical study, 16 prompted LLMs x 3 prompts vs CodeQL (synthetic only) and DeepDFA/LineVul (CVEFixes C/C++)
dataset: OWASP Benchmark, Juliet Java, Juliet C/C++ (synthetic); CVEFixes Java and C/C++ (real-world); MITRE Top-25 CWEs
sample_size: 5,000 function-level snippets (1,000 per dataset, 500 vulnerable / 500 non-vulnerable), 25 CWEs, single run at temperature 0
metrics: Accuracy, precision, recall, F1; balanced accuracy per CWE
main_finding: LLMs are modest (best accuracy 62.8% avg); CodeQL beats LLMs on synthetic data; LLMs win some CWEs; LLM vs DL F1 near trivial baseline.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Understanding the Effectiveness of Large Language Models in Detecting Security Vulnerabilities

- Authors: Khare, Avishree; Dutta, Saikat; Li, Ziyang; Solko-Breslin, Alaia; Alur, Rajeev; Naik, Mayur
- Year / venue: 2025, 2025 IEEE Conference on Software Testing, Verification and Validation (ICST) (published)
- DOI: 10.1109/icst62969.2025.10988968 · URL: https://doi.org/10.1109/icst62969.2025.10988968
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] To systematically evaluate how well pre-trained LLMs detect known security vulnerabilities across more datasets, languages, models, prompts and vulnerability classes than prior work, and to compare them with a static analyser (CodeQL) and deep-learning detectors (DeepDFA, LineVul) (p. 1–3).

## 2. Research questions / hypotheses
- [V] RQ1: LLM performance across languages and datasets; RQ2: effect of prompting strategies; RQ3: variation across vulnerability classes (CWEs); RQ4: LLMs vs state-of-the-art static analysis; RQ5: LLMs vs state-of-the-art DL tools (Table I, p. 2). No formal hypotheses.

## 3. Methodology
- Research design: [V] Function/snippet-level binary classification benchmark on balanced samples, plus manual qualitative inspection of 20-sample subsets (p. 3–6).
- Approach / model / intervention: [V] 16 pre-trained LLMs, "Instruct" variants where available: Qwen-2.5-Coder 1.5B/7B, CodeLlama 7B/13B/34B, DeepSeekCoder 7B/15B(v2)/33B, Llama-3.1 8B/70B, Qwen-2.5 14B/32B, Codestral-22B, Gemini-1.5-Flash, GPT-3.5 (gpt-3.5-turbo-0613), GPT-4 (gpt-4-0613) (Table V, p. 4). [V] Three prompts with a "security researcher" persona: Basic (any vulnerability), CWE-specific (target CWE named), CWE-DF (simulate source–sink–sanitizer dataflow analysis before the verdict) (p. 4, p. 14). [V] Few-shot and chain-of-thought were tried with GPT-4 on 100 samples and dropped as not better than CWE-DF (p. 4, p. 14–15). No fine-tuning of LLMs.
- Baselines or comparison conditions: [V] CodeQL with official queries for the Top-25 CWEs, on synthetic datasets only (OWASP, Juliet Java, Juliet C/C++) because real-world projects need building (p. 7–8). [V] DeepDFA (GNN over CFG + dataflow facts) and LineVul (transformer) from DeepDFA's artifact, trained on Juliet C/C++, CVEFixes C/C++ (test samples excluded) or BigVul, 80/20 train/validation, tested on the 1,000 CVEFixes C/C++ samples, averaged over three runs (p. 9). CodeQL version: not reported.

## 4. Dataset and sample
- Data source(s): [V] OWASP Benchmark (Java, synthetic), SARD Juliet Java and Juliet C/C++ (synthetic), CVEFixes Java and C/C++ (real-world, method-level from NVD fix commits) (Table III, p. 3). [V] CVEFixes chosen because it has CVE/CWE metadata, is two-sided and multi-language (p. 3).
- Sample size (N) and unit: [V] 5,000 code snippets: 1,000 per dataset, 500 vulnerable + 500 non-vulnerable; 25 CWEs (p. 1, p. 5; Table VI, p. 4). Unit = single method/snippet.
- Sampling / selection method: [V] Filtering: Top-25 CWE only, snippets ≤2,048 tokens, multi-file Juliet cases skipped, then random sampling (Table VI, p. 4; p. 5; p. 14). [V] Hints removed: comments stripped, identifying names (e.g., "CWE80_XSS…", "owasp") anonymised (p. 5, p. 14). [V] CVEFixes labels: pre-fix vs post-fix versions of methods changed in fix commits (p. 14).
- Data availability (public? link?): source datasets public (p. 3); the authors' sampled subsets and evaluation code: not reported (no link in this version).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] OpenAI ChatCompletions API (GPT-3.5/4), Gemini API, Hugging Face for open models on a cluster with A100, A6000 and RTX 2080 GPUs; temperature 0, max 1,024 output tokens, top-1 prediction, default other parameters (p. 5). [V] Single run per benchmark (p. 10). [A] CWE-DF "is costlier since it generates more tokens" (p. 4). Token counts, monetary cost, runtime: not reported.
- Code availability: not reported in this version.

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] Accuracy, precision, recall, F1 as standard classification metrics (p. 3–4). [V] Balanced accuracy per CWE for RQ3/RQ4, only CWEs with ≥10 samples, best prompt per model and dataset (p. 6–7). [V] RQ1 reports the best accuracy/F1 per model per dataset across prompts (p. 5).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): not reported; [A] "significantly" is used descriptively (p. 1); standard-deviation bars across models in Fig. 2 (p. 5).

## 7. Key findings
1. [V] Best model+prompt per dataset averages 62.8% accuracy; bests are Llama-3.1-70B (CWE) 76% on Juliet Java, Qwen-2.5-14B 65% on Juliet C/C++, CodeLlama-13B 60% on OWASP, Gemini-1.5-Flash 57% on CVEFixes Java, Qwen-2.5-32B 56% on CVEFixes C/C++ (p. 5). [A] Mean F1 0.71 (p. 1–2). [I] Both headline means are averages of the best value per dataset in Table XII (p. 16): accuracy (0.60+0.76+0.57+0.65+0.56)/5 = 0.628; F1 (0.70+0.79+0.67+0.73+0.67)/5 = 0.712. Two of the five best F1s (CVEFixes Java and CVEFixes C/C++, 0.67) come from "always vulnerable"-type rows (P 0.50, R 0.99–1.00).
2. [V] Best accuracies on synthetic datasets are 10.5% higher on average than on real-world datasets (p. 5).
3. [A] Performance does not improve with scale: Qwen-2.5-14B/32B beat GPT-x on real-world data; only GPT-x and Llama-3.1-x improve with size on ≥3 datasets (p. 5).
4. [V] CWE-DF raises average F1 over CWE and Basic prompts on real-world datasets by up to 0.18 (CVEFixes C/C++) and 0.14 (CVEFixes Java), with lowest variance across models (p. 5). [V] Basic prompt names an incorrect CWE in >60% (Java) and >53% (C/C++) of samples (p. 6; Table VII).
5. [V] Manual inspection (20-sample subsets): CWE-DF identifies correct sources/sinks in 18/20 and sanitizers in 16/20 real-world Java samples; on wrongly predicted Juliet C/C++ samples, sources/sinks/sanitizers are correct in 17/20 but unsanitized flows wrong in 12/20 (p. 6).
6. [V] CWE-wise: best on self-contained vulnerabilities — CWE-78 (Llama-3.1-70B 64% CVEFixes Java, 78% CVEFixes C/C++), CWE-787/125 in Java (Llama-3.1-8B/GPT-4 up to 89%/84%), CWE-476 (DSCoder-7B 63–88%), CWE-89 (GPT-3.5 70% on CVEFixes Java), CWE-79 (Qwen-2.5-32B 66–67%); poor on CWE-862 and on C/C++ out-of-bounds (<53% for GPT-4/Llama-3.1-8B; no LLM >60%) (p. 7).
7. [V] CodeQL vs best LLM per synthetic dataset (A/P/R/F1): OWASP 0.63/0.58/0.96/0.72 vs CodeLlama-13B 0.60/0.58/0.74/0.65; Juliet Java 0.94/0.92/0.95/0.94 vs Llama-3.1-70B 0.76/0.71/0.89/0.79; Juliet C/C++ 0.72/0.99/0.44/0.61 vs Qwen-2.5-14B 0.65/0.60/0.89/0.72 (Table VIII, p. 9). CodeQL has higher accuracy on all three; the LLM has higher F1 only on Juliet C/C++ (p. 8). [I] On OWASP both CodeQL (A 0.63, R 0.96, F1 0.72) and the best LLM (A 0.60, F1 0.65) are close to the always-vulnerable baseline (A 0.50, F1 0.667); the LLM's F1 is below it (Table VIII, p. 9).
8. [V] LLMs beat CodeQL on CWE-22, CWE-78, CWE-476, CWE-416 on ≥2 of 3 datasets (e.g., DSCoder-7B +24% on CWE-416 Juliet C/C++; +12% on CWE-476 Juliet Java); CodeQL beats LLMs on CWE-190 by 11% (Juliet Java) and 21% (Juliet C/C++) (p. 8). [A] CodeQL misses some cases because its queries are narrow (e.g., CWE-78 query handles execl but not _execvp) (p. 8).
9. [V] DL tools on CVEFixes C/C++ (A/P/R/F1), Table IX (p. 10): DeepDFA trained in-distribution 0.51/0.55/0.17/0.23, on Juliet 0.53/0.53/0.65/0.58, on BigVul 0.52/0.52/0.76/0.62; LineVul in-distribution 0.59/0.58/0.65/0.61, on Juliet 0.50/0.50/0.91/0.64, on BigVul 0.50/0.63/0.01/0.02; Qwen-2.5-32B (CWE-DF, no training) 0.56/0.54/0.81/0.65. DL F1 on CVEFixes therefore ranges 0.02–0.64, and in-distribution LineVul has higher accuracy than Qwen (0.59 vs 0.56) (p. 9–10). Trained on BigVul, both reach ≥0.98 accuracy on BigVul (p. 10). [A] DL tools do not generalise across datasets; LLMs preferable for low inference overhead and explanations (p. 9–10). [I] Qwen's F1 of 0.65 is below the 0.667 F1 of always answering "vulnerable" on this 50/50 set, as are all DL F1s, so the F1 comparison does not show that any of these tools beats the trivial baseline (based on Table IX, p. 10).

## 8. Limitations stated by the authors
- [A] Choice of LLMs and datasets may bias results; may not generalise to other languages or datasets (p. 10).
- [A] Single runs; GPT-3.5/GPT-4 may be non-deterministic even at temperature 0 (p. 10).
- [A] Possible bugs in evaluation code and errors in manual analysis, mitigated by multiple co-authors' review (p. 10).
- [A] Multi-file samples and snippets >2,048 tokens excluded due to prompt size (p. 5, p. 14).

## 9. Limitations we identified
- [I] Headline F1 is close to a trivial baseline: on 50/50 balanced data, always answering "vulnerable" gives P = 0.50, R = 1.00, F1 = 0.67, and many configurations show exactly this pattern (e.g., CodeLlama-7B, CodeLlama-13B, CodeLlama-34B and DSCoder-15B with CWE-DF: A 0.50 / P 0.50 / R 1.00 / F1 0.67 on most datasets, Table XII, p. 16). The mean F1 of 0.71 therefore says little: it is the mean of the best F1 per dataset (0.70, 0.79, 0.67, 0.73, 0.67; Table XII, p. 16), and two of those five bests are always-vulnerable-type rows (CVEFixes Java 0.50/0.50/1.00/0.67; CVEFixes C/C++ CodeLlama-34B CWE-DF 0.50/0.50/0.99/0.67). On real-world CVEFixes data, no configuration's F1 exceeds 0.67, i.e. none clearly beats the trivial 0.667. Accuracy (~50–60%) is the more honest signal.
- [I] Best-of-48 selection: RQ1 and RQ4 report the best model+prompt per dataset chosen after seeing test results (p. 5, p. 8), which favours LLMs against a single CodeQL configuration.
- [I] CodeQL is compared only on synthetic Juliet/OWASP data, where CodeQL queries are well-tuned, and LLM–CodeQL comparison on real-world code is absent (p. 7–8). This limits RQ1/RQ4 conclusions for real code.
- [I] Balanced 50/50 evaluation does not reflect real-world prevalence of vulnerable code; precision would drop sharply at realistic ratios.
- [I] Data contamination: Juliet, OWASP and CVEFixes are public and predate the LLMs' training cut-offs; not discussed beyond identifier anonymisation (p. 5, p. 14).
- [I] CVEFixes method-level labels are known to be noisy (fix-commit heuristic); label quality is not assessed. The appendix sentence labelling methods "in the fix commit and the parent commit … as vulnerable and non-vulnerable, respectively" (p. 14) reads reversed relative to the usual convention; likely a wording error.
- [I] Table V lists "DSCoder-15B" as deepseekcoder-v2-15b with size "33B" (p. 4), an internal inconsistency.
- [I] The abstract's statement that LLMs report higher accuracies than CodeQL refers to specific CWEs only; overall CodeQL wins on accuracy on all three synthetic datasets (p. 1 vs p. 8).
- [I] No cost or runtime data, so trade-offs for RQ3 cannot be assessed.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Post-hoc best-configuration selection; possible pre-training contamination; DL tools trained with 80/20 split but tested on the same 1,000-sample set as LLMs (CVEFixes test samples excluded from training, p. 9).
- External (generalisability of sample/context): [I] Function-level snippets only, no inter-procedural/multi-file context; two languages; Top-25 CWEs; balanced sampling.
- Construct (do metrics measure the concept?): [I] Binary verdict ignores whether the predicted CWE or location is right (Basic prompt names wrong CWE >53–60% of the time, p. 6); F1 on balanced data inflated by "always yes" behaviour.
- Statistical conclusion (power, multiple comparisons, variance): [I] 1,000 samples per dataset is reasonable, but per-CWE analysis uses as few as 10 samples (p. 7); no significance tests or CIs; single runs.
- Reproducibility (data/code/setup reported?): [I] Prompts fully given (p. 14–15) and model versions listed (p. 4); sampled subsets and code not linked in this arXiv version.

## 11. Future research directions
- Stated by authors [A]: neuro-symbolic techniques combining LLM reasoning with logical reasoning engines and static analyzers (p. 11); use LLMs to infer specifications (sources, sinks, sanitizers) that static analysis then reasons over (p. 6, p. 8–10).
- Suggested by us [I]: evaluate CodeQL and LLMs together on real-world code at realistic prevalence; report trivial baselines; test the proposed LLM-specification + static-analysis hybrid directly.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]: Peer-reviewed (ICST 2025), multi-dataset study that covers all three families (LLM, SAST via CodeQL, DL via DeepDFA/LineVul). It shows CodeQL still wins overall on synthetic suites while LLMs win particular CWEs, and that LLM F1 on balanced data can be near-trivial. It is a key source for RQ4 (CWE-specific strengths) and for the "LLM finds specs, static analysis reasons" hybrid idea in RQ3/RQ5.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Best LLM+prompt per dataset averages 62.8% accuracy on balanced function-level data; real-world accuracy 10.5% lower than synthetic | 5 | V | moderate |
| RQ1 | CodeQL beats the best LLM in accuracy on OWASP (0.63 vs 0.60), Juliet Java (0.94 vs 0.76) and Juliet C/C++ (0.72 vs 0.65); F1: CodeQL 0.72/0.94/0.61 vs LLM 0.65/0.79/0.72. Caveat [I]: on OWASP both are near the always-vulnerable baseline (A 0.50, F1 0.667) | 9 | V | moderate |
| RQ1 | On CVEFixes C/C++, Qwen-2.5-32B (prompted) A 0.56 / F1 0.65 vs DL tools F1 0.02–0.64 (in-distribution LineVul A 0.59 / F1 0.61, higher accuracy than Qwen); LineVul trained on BigVul collapses to F1 0.02. Caveat [I]: Qwen and all DL F1s are below the always-vulnerable F1 of 0.667 on this 50/50 set | 10 | V | moderate |
| RQ1 | Model scale does not reliably improve detection; Qwen-2.5-14B/32B beat GPT-4 on real-world data | 5 | A | moderate |
| RQ2 | Many LLM configurations behave as "always vulnerable" (P 0.50, R 1.00, F1 0.67) on 50/50 data, so F1 ≈ trivial baseline | 16 | I | moderate |
| RQ2 | CodeQL evaluated only on synthetic datasets; best LLM configuration chosen post hoc from 16 models × 3 prompts | 5, 7–8 | V | moderate |
| RQ3 | CWE-DF (dataflow-style) prompt raises real-world F1 by up to 0.18; LLMs correctly identify sources/sinks/sanitizers in 16–18 of 20 inspected samples even when the verdict is wrong | 5–6 | V | weak |
| RQ3 | Authors propose neuro-symbolic hybrids: LLMs infer specifications, static analysers reason over them | 8–11 | A | weak |
| RQ4 | LLMs beat CodeQL on CWE-22, CWE-78, CWE-476, CWE-416 (e.g., +24% on CWE-416); CodeQL better on CWE-190 (+11–21%) | 8 | V | moderate |
| RQ4 | LLMs do well on self-contained CWEs (78, 476, 89, 79, Java 125/787) and poorly on context-dependent ones (CWE-862, C/C++ out-of-bounds with structs/pointers) | 7 | V | moderate |
| RQ5 | Missing global/inter-procedural context is the main failure cause on real-world C/C++; multi-file samples excluded | 5, 7 | A | moderate |

## 14. Key quotes
> "LLMs report lower overall accuracies than CodeQL on all synthetic datasets." (p. 2)

> "the best accuracies on synthetic datasets are 10.5% higher on average than those on the real-world datasets" (p. 5)

> "Finding 3.2: Poor performance on real-world C/C++ is due to missing global context." (p. 7)

## Analyst notes
- Reading coverage: whole paper read including appendix (pp. 1–18) and the full metrics table (Table XII, p. 16). Figures 1–4 are images; their numbers were taken from the text, not read off the plots.
- Source version: arXiv v3 (2311.16169, 23 Oct 2024). Published version: ICST 2025 (DOI 10.1109/icst62969.2025.10988968, from metadata). Numbers may differ slightly from the camera-ready; recheck if the published PDF becomes available.
- Provenance: `rlab validate` reports MISMATCH because the arXiv cross-check year (v1 posted 2023) differs from the ICST proceedings year (2025). Title and first author match on all three sources, and Crossref and OpenAlex match fully; the PDF prints the arXiv id. This is a benign preprint-year vs proceedings-year difference, not an identity problem.
- Uncertainties: the abstract's mean F1 0.71 is resolved: it is the mean of the best F1 per dataset in Table XII (p. 16), and 62.8% is the matching mean of best accuracies (section 7, item 1). Whether code/data were released is not stated in this version.
