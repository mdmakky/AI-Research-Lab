# Research questions — LLM-based vs Traditional Static Analysis and Deep Learning Approaches for Source Code Vulnerability Detection: A Comparative Review

<!-- 3-5 questions. Each must be answerable from literature evidence. -->

## RQ1: How do LLM-based approaches compare with SAST tools and DL detectors in detection effectiveness (precision, recall, F1, false-positive rate) in head-to-head evaluations?
- Type: comparative
- Why it matters: the core practical question — which approach finds more real vulnerabilities with fewer false alarms.
- Linked objective: 1
- Status: answered (synthesis 2026-11-12; updated pass 2, 2026-11-12)
- Current answer (updated pass 2, 2026-11-12): No family wins across settings. Frontier LLMs beat SAST on small, self-contained code [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11], but CodeQL beats LLMs on synthetic function-level suites [@khare2025understanding, p. 9]. At project scale general coding agents reach far higher recall than SAST (59.55% vs 0–34.29% on C/C++), while most LLM detectors and SAST tools produce mostly false warnings [@li2026llm, p. 7; @li2026llm, p. 11]. On the same 1549 unpaired PrimeVul functions, seven of eight zero-shot LLMs beat lightweight SAST on balanced accuracy [@deininger2026open, p. 7; @deininger2026open, p. 10]. At the natural 1:44 prevalence, however, Flawfinder and Semgrep are more precise than every LLM, whose precision (2.3–4.6%) is barely above flag-all (2.21%) [@deininger2026open, p. 8; @deininger2026open, p. 17]. Versus fine-tuned DL, the ranking depends on dataset, class balance and decision threshold [@fu2023chatgpt, p. 4; @shu2026evaluating, p. 40; @deininger2026open, p. 11]. A fine-tuned CodeBERT beats all eight LLMs on those unpaired functions (balanced accuracy 0.765 vs ≤ 0.711) [@deininger2026open, p. 11; @deininger2026open, p. 17], and all families are near or below chance on PrimeVul pairs [@ding2025vulnerability, p. 9; @tan2026think, p. 6]. On 2025 CVEs at 1.97% prevalence, trained DL (F1 3.47–8.65) and four open LLMs ≤ 32B (0.79–5.36) both sit near the all-positive F1 of about 3.87% [I] [@lu2025lab, p. 13; @lu2025lab, p. 14]. For PHP, no LLM has been tested; a bespoke lexical taint analyser detects 1.7–1.8% of vulnerabilities [@tashenova2026real, p. 9]. **Strength: weak–moderate.** Most results come from single-run studies with incompatible metrics, and only one study compares all three families on identical real functions, with lightweight SAST. Most robust pattern [I]: LLMs have higher recall and lower precision, and at realistic prevalence their margin over trivial baselines is small.

## RQ2: How do evaluation setups (benchmarks, languages, CWE coverage, synthetic vs. real-world code, data-leakage control) differ across studies, and how do they explain disagreements in reported results?
- Type: methodological
- Why it matters: results that look contradictory may come from different benchmarks; this decides how much any number can be trusted.
- Linked objective: 2
- Status: answered (synthesis 2026-11-12; updated pass 2, 2026-11-12)
- Current answer (updated pass 2, 2026-11-12): Evaluation setup explains much of the disagreement. Sources of variation include:
  - label noise: 39–65% of positive labels correct [@risse2025top, p. 8], and 48.8% in a PHP benchmark [@tashenova2026real, p. 11];
  - leakage: exact-copy leakage up to 18.9% [@ding2025vulnerability, p. 4], and duplicate and contradictory-label groups even across plugin-grouped folds [@tashenova2026real, p. 4];
  - balanced vs realistic class ratios that flip rankings [@shu2026evaluating, p. 40; @yildiz2025benchmarking, p. 7; @deininger2026open, p. 8];
  - trivial baselines that are rarely reported but often competitive [@tashenova2026real, p. 8; @deininger2026open, p. 7; @lu2025lab, p. 14];
  - temporal and cross-dataset shift [@lu2025lab, p. 12; @lu2025lab, p. 13];
  - prompt wording and decision threshold, either of which can change the winner [@deininger2026open, p. 11; @deininger2026open, p. 20];
  - synthetic vs real code [@khare2025understanding, p. 5];
  - function vs statement granularity [@ahmed2026secvuleval, p. 8];
  - custom datasets with inconsistent splits [@kaniewski2026systematic, p. 35]. The same model on the same named dataset can differ by 28 F1 points between papers [@lu2025lab, p. 12; @ding2025vulnerability, p. 7].

  **Strength: strong** for label noise and the collapse under realistic evaluation, which are consistent across independent primary studies and two SLRs. **Moderate** for prompt and threshold sensitivity and for trivial baselines, which rest on fewer studies.

## RQ3: Do hybrid LLM + static-analysis approaches outperform either family alone, and what are the trade-offs in cost, speed and explainability?
- Type: comparative
- Why it matters: industry is moving to combined tools; evidence for their benefit is scattered.
- Linked objective: 3
- Status: answered (synthesis 2026-11-12; updated pass 2, 2026-11-12)
- Current answer (updated pass 2, 2026-11-12): LLM filtering of SAST alarms removes most false alarms at < $0.20 per alarm but loses 12–25% of real bugs [@du2026reducing, p. 8; @xiong2026sifting, p. 18] (**moderate**). Hybrid detection (IRIS, RepoAudit) beats SAST in the authors' own evaluations [@li2024iris, p. 8; @guo2025repoaudit, p. 8] but not in an independent project-scale study [@li2026llm, p. 7; @li2026llm, p. 12], and it needs a strong LLM [@li2024iris, p. 10] (**weak/contested**). LLM costs range from cents per alarm to $1,247.66 per project, against minutes and no token cost for SAST [@li2026llm, p. 16]. The only cost per true positive comes from a non-hybrid study: USD 0.003–0.212 and 3.7–119.6 kJ per true positive at 1:44 prevalence [@deininger2026open, p. 8]. These are compute costs only. Human triage of the 25.6–41.9 false positives per true one is excluded [@deininger2026open, p. 8], and part of the energy values are FLOP estimates [@deininger2026open, p. 14]. The same study finds that small open models can match a frontier model at 1/66 of the cost [@deininger2026open, p. 17] (**moderate, single study**). Explainability is limited: LLMs mislocate findings [@gnieciak2025large, p. 11], and fluent explanations do not signal correctness [@tan2026think, p. 9].

## RQ4: Which vulnerability types (CWEs), languages and code scales does each family handle well or poorly?
- Type: comparative
- Why it matters: guides tool choice for a given codebase and points to where research is missing.
- Linked objective: 1, 4
- Status: answered (synthesis 2026-11-12; updated pass 2, 2026-11-12)
- Current answer (updated pass 2, 2026-11-12): LLMs do best on self-contained injection-style CWEs and worst on context-dependent and crypto/policy CWEs and on localising memory-safety bugs [@khare2025understanding, p. 7; @xiong2026sifting, p. 18; @shu2026evaluating, p. 30]. CodeQL is better on CWE-190 [@khare2025understanding, p. 8]. LLM performance falls with function/file length [@ahmed2026secvuleval, p. 13; @li2026llm, p. 9]. Results also vary by project: LineVul (BigVul) finds 76% of Chromium CVEs but none in Linux, while all LLMs cover Linux better [@lu2025lab, p. 13]. Evidence is concentrated on C/C++ and Java [@kaniewski2026systematic, p. 28]. The only PHP evidence (tashenova2026real) tests no LLM and uses a bespoke lexical taint analyser that detects 1.7–1.8% of vulnerabilities. In that study, learned models detect XSS (F1 up to 0.500) far better than SQLi (≤ 0.146) or RCE (≤ 0.085) [@tashenova2026real, p. 9]. **Strength: weak** (small per-CWE cells, divergent results, a single PHP study).

## RQ5: What gaps and open problems remain for reliable, deployable LLM-based vulnerability detection?
- Type: descriptive
- Why it matters: basis for the gap section and future work of the paper.
- Linked objective: 4
- Status: answered (synthesis 2026-11-12; updated pass 2, 2026-11-12)
- Current answer (updated pass 2, 2026-11-12): Recurring open problems:
  - verified, realistic, repository-level benchmarks with context [@zhou2025large, p. 19; @sheng2025llms, p. 25];
  - trivial baselines and realistic prevalence in every evaluation [@tashenova2026real, p. 13; @deininger2026open, p. 8];
  - label quality and contamination control [@tashenova2026real, p. 12; @lu2025lab, p. 17];
  - same-benchmark LLM vs SAST vs DL comparisons. Two studies run all three: khare, with SAST on synthetic data only [@khare2025understanding, p. 7], and deininger, with lightweight function-level SAST on pre-2023 CVEs [@deininger2026open, p. 10; @deininger2026open, p. 24];
  - independent labelling and statistical testing, including prompt sensitivity [@li2026llm, p. 11; @deininger2026open, p. 20];
  - cost reporting that includes human triage and states where energy figures come from [@deininger2026open, p. 8];
  - true-positive loss in filtering [@xiong2026sifting, p. 19];
  - workflow integration [@zhou2025large, p. 19].

  deininger's authors judge that no tested method is ready for independent function-level triage [@deininger2026open, p. 26]. **Strength: moderate** [I]. These are candidate gaps only. Gap specifics and novelty checks are in gap-report.md.
