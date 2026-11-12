---
key: dubniczky2025castle
status: complete
evidence_basis: full-text
design: Benchmark paper; 13 static analyzers + 2 formal verification tools vs 10 prompted LLMs on new hand-written C micro-benchmarks
dataset: CASTLE: 250 compilable C programs (7-164 lines), 25 CWEs, 6 vulnerable + 4 clean per CWE, line-level labels
sample_size: 250 programs (150 vulnerable, 100 non-vulnerable), 10,392 lines total; 25 tools/models
metrics: TP/TN/FP/FN, precision, recall, accuracy, new CASTLE Score (severity-weighted, FP-penalised), combination score
main_finding: On small C programs, top LLMs (GPT-o3-mini 977, o1, R1, GPT-4o) outscore all SAST and formal tools; best non-LLM ESBMC 661, CodeQL 634.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# CASTLE: Benchmarking Dataset for Static Code Analyzers and LLMs Towards CWE Detection

- Authors: Dubniczky, Richard A.; Horvát, Krisztofer Zoltan; Bisztray, Tamás; Ferrag, Mohamed Amine; Cordeiro, Lucas C.; Tihanyi, Norbert
- Year / venue: 2025, Lecture Notes in Computer Science (book)
- DOI: 10.1007/978-3-031-98208-8_15 · URL: https://doi.org/10.1007/978-3-031-98208-8_15
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] To introduce CASTLE (CWE Automated Security Testing and Low-Level Evaluation), a compilable, balanced, line-labelled C micro-benchmark, and use it to compare static analyzers, formal verification (FV) tools and LLMs for CWE detection, together with a new metric, the CASTLE Score (p. 1–2).

## 2. Research questions / hypotheses
- [V] RQ1: How do state-of-the-art static analysis tools, FV methods and LLM-based approaches compare in detecting C vulnerabilities? RQ2: Are combinations of tools more effective than a single tool? RQ3: What metrics can reliably show these differences? (p. 2).

## 3. Methodology
- Research design: [V] Benchmark construction plus single-benchmark comparative evaluation of 25 tools/models (p. 6, p. 11).
- Approach / model / intervention: [V] 10 LLMs prompted via OpenAI-style APIs with one system prompt ("professional security analyst"), returning JSON with severity, line, CWE, message and line content; the prompt states "You get 5 points for each vulnerability you find, but get -1 for all false positives" (p. 8–9). [V] LLMs: GPT-o3-Mini, GPT-o1, DeepSeek R1, GPT-4o, GPT-4o-Mini, Qwen 2.5 Coder Instruct 32B, Falcon 3 7B, Mistral Instruct 7B, Gemma 2 9B, Llama 3.1 8B (Table 3, p. 11). No fine-tuning; zero-shot only.
- Baselines or comparison conditions: [V] Static analyzers with versions: CodeQL 2.20.1, GCC -fanalyzer 13.3.0, Snyk 1.1295.4, Semgrep Code 1.110.0, SonarQube 25.3.0, Coverity 2024.6.1, Cppcheck 2.13.0, Clang Analyzer 18.1.3, GitLab SAST 15.2.1, Splint 3.1.2, plus API-only Aikido, Jit, CodeThreat; FV tools ESBMC 7.8.1 and CBMC 5.95.1 (Table 3, p. 11). [V] ESBMC run with --overflow --no-unwinding-assertions --memory-leak-check --timeout 60 --multi-property (p. 12). [V] Tool combinations evaluated with a combination score (p. 10, p. 13). [I] No LLM + SAST/FV combination is evaluated (based on p. 11–13).

## 4. Dataset and sample
- Data source(s): [V] 250 small C programs "crafted manually by cybersecurity experts"; each compiles (warnings allowed), single file, exactly one or zero vulnerabilities; vulnerable lines marked with `// {!LINE}` (p. 6–7).
- Sample size (N) and unit: [V] 25 CWEs × 10 tests (6 vulnerable, 4 non-vulnerable) = 250 programs (150 vulnerable, 100 clean); 7–164 lines (mean 42, total 10,392); 1–8 functions; cyclomatic complexity 1–29 (mean 6.3); ~115,620 input tokens in total with the system prompt (p. 6).
- Sampling / selection method: [V] CWEs chosen mostly from the MITRE Top-25 of 2023–2024; 7 of the 25 CWEs are not in the 2024 Top-25 (e.g., CWE-253, -327, -362, -401, -617, -628, -843) (Table 2, p. 7). [V] Iterative expert validation; ambiguous cases mapped to higher-level CWE (p. 6–7). Number and selection of experts: not reported.
- Data availability (public? link?): [V] https://github.com/CASTLE-Benchmark (p. 1); wrappers public; intermediate vendor reports not shared (p. 9).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Free tools containerised in Docker with Python wrappers; closed-source tools (CodeThreat, Aikido) run via uploads to vendor dashboards/APIs with manual consistency checks (p. 8). [V] API-only tools and LLMs evaluated in February 2025 (p. 11). [V] LLM metadata and side-channel information removed before analysis (p. 7). [V] LLMs also return the code line content so that small line-number offsets could be adjusted during evaluation (p. 8). LLM temperature/sampling and model snapshot versions: not reported. Cost and runtime: not reported (only total token count, p. 6).
- Code availability: [V] Wrappers in the main repository (p. 9).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] TP, TN, FP, FN, precision, recall, accuracy (Table 3, p. 11). [V] CASTLE Score: per vulnerable test, correct detection scores 5 + Top-25 rank bonus (max 5) minus 1 per extra finding; per clean test with no report, 2 points; otherwise −(number of findings); missing a vulnerability with no report scores 0 (p. 9–10). Tools reporting nothing score 200; theoretical maximum 1,250 (p. 12). [V] Combination score: union of findings, TPs/TNs counted once, FP penalties summed (p. 10).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): not reported. [A] Repeated evaluations deviate by less than 3% (p. 14); number of repeats not reported.

## 7. Key findings
1. [V] Static/FV tools (TP/TN/FP/FN, P/R/A, CASTLE): ESBMC 53/91/32/97, 62%/35%/53%, 661; CodeQL 45/79/49/112, 48%/29%/44%, 634; GCC Fanalyzer 41/76/93/109, 31%/27%/37%, 559; Snyk 26/82/42/124, 38%/17%/39%, 552; Semgrep Code 36/73/70/120, 34%/23%/36%, 541; CBMC 18/100/0/132, 100%/12%/47%, 536; SonarQube 43/68/135/107, 24%/29%/31%, 511; Aikido 481; Jit 478; Coverity 31/86/62/119, 33%/21%/39%, 425; Cppcheck 19/100/9/131, 68%/13%/46%, 406; Clang Analyzer 13/99/2/137, 87%/9%/45%, 381; GitLab SAST 36/67/240/120, 13%/23%/22%, 374; Splint −598 (1,027 FP); CodeThreat −692 (1,101 FP) (Table 3, p. 11).
2. [V] LLMs: GPT-o3-Mini 126/60/73/36, 63%/78%/63%, 977; GPT-o1 128/56/90/35, 59%/78%/60%, 962; DeepSeek R1 148/41/166/17, 47%/90%/51%, 956; GPT-4o 136/45/116/43, 54%/76%/53%, 954; GPT-4o-Mini 134/27/263/43, 34%/76%/34%, 761; Qwen 2.5 Coder 32B 114/31/224/49, 34%/70%/35%, 708; Falcon 3 7B 521; Mistral 7B 446; Gemma 2 9B 436; Llama 3.1 8B 83/22/337/80, 20%/51%/20%, 417 (Table 3, p. 11).
3. [A] CodeQL is the best SAST tool, finding "29% of the weaknesses in the code (45/150)" vs a 23% average among SAST tools; SonarQube also 29% but with 2.7× CodeQL's false positives (p. 12). [I] Labelled [A], not [V]: 45/150 = 30%, while 29% = 45/157 (CodeQL TP + FN in Table 3, p. 11); the same happens for GPT-o3-Mini, "126 out of the 150" (p. 14) but recall 78% = 126/162 (p. 11). The text therefore confirms the denominator problem in section 9.
4. [A] Reasoning models (o1, o3-mini) "consistently produced fewer false positives" than GPT-4o/4o-mini, which find more true positives (p. 14). [I] This holds for the OpenAI o-series only (o3-mini 73 FP, o1 90 FP vs GPT-4o 116, 4o-mini 263); DeepSeek R1, generally regarded as a reasoning model though the paper does not classify it, has 166 FP, more than GPT-4o (Table 3, p. 11). [A] LLMs "rival—and often surpass" classical static analyzers on compact code (p. 14).
5. [V] Best two-tool combination ESBMC + CodeQL scores 814, +153 over ESBMC alone (661), i.e., +23% vs ESBMC and +28% vs CodeQL (p. 13). [A] Combinations help when tools have complementary CWE coverage; overlapping tools lose score through added FPs (p. 13).
6. [A] FV tools have very few FPs (CBMC 0) but cannot detect non-formal issues such as SQL injection, path traversal or hard-coded credentials (p. 12).
7. [A] Smaller models (<6B parameters) often failed to produce well-formed JSON; models often found the right vulnerability with an offset line number (p. 8).
8. [A] In a preliminary test on a 400+ line program built by merging clean tests, LLMs reported more false positives and most failed to find one hidden injected vulnerability (p. 14). No numbers given.

## 8. Limitations stated by the authors
- [A] Micro-benchmark scope: single, isolated vulnerabilities; real software has cross-file flaws over many files (p. 14).
- [A] Lack of large code samples: LLM accuracy declines and false positives rise with code length; FV suffers state explosion; SAST scales better but has many FPs (p. 14).
- [A] Potential overfitting: fixed public tests could be targeted by vendors; dataset should be refreshed (p. 14).
- [A] LLM stochasticity, though repeated evaluations deviated less than 3% (p. 14).

## 9. Limitations we identified
- [I] Count inconsistencies in Table 3 (p. 11): there are 150 vulnerable programs, but TP + FN exceeds 150 for all 10 LLMs (154–179: o3-mini 162, o1 163, R1 165, GPT-4o 179, 4o-mini 177, Qwen 163, Falcon 154, Mistral 154, Gemma 158, Llama 163) and for 4 tools (CodeQL 45 + 112 = 157, Semgrep 156, GitLab SAST 156, Jit 155); the other 11 tools sum to exactly 150. The paper's own sentence "29% … (45/150)" (p. 12) shows it: 45/150 = 30%, 29% = 45/157. Recall therefore uses a denominator that is not the number of vulnerabilities (R1 recall 90% = 148/165, not 148/150), and accuracy is computed over finding counts rather than 250 programs. The counting rule for multiple findings per test is not explained. Exact recall/accuracy numbers should be quoted with this caveat.
- [I] The paper's own text is inconsistent on tool counts: "11 static code analyzers and 11 LLMs" (p. 3) vs 13 static + 2 FV + 10 LLMs (p. 1, p. 11).
- [I] Lenient LLM scoring: LLM line offsets were corrected using the returned line content (p. 8), a help not described for SAST tools; the prompt also mirrors the CASTLE scoring incentive (p. 9).
- [I] Synthetic, tiny, single-file programs (mean 42 lines) are ideal for LLM context windows and hard for tools tuned to real projects; the authors' own 400-line test suggests the ranking may flip on larger code (p. 14). This is the key external-validity caveat for RQ1.
- [I] The CASTLE Score is a new, author-defined weighting (bonus from Top-25 rank, 2 points per clean test, no penalty for silent misses) (p. 9–10). Its claim to be more reliable than precision/recall (p. 15) is not validated against any external criterion.
- [I] No per-CWE results table, so CWE-level strengths (RQ4) cannot be extracted beyond qualitative statements.
- [I] No LLM + static/FV hybrid is tested, though combination scoring would allow it.
- [I] LLM versions, temperature and costs not reported; closed models may change over time.
- [I] Funding partly from ZEISS Digital Innovation (p. 15); no conflict evident, noted for completeness. The authors filed ESBMC bug reports (p. 12) and co-authors' earlier FormAI dataset was labelled with ESBMC (p. 3); ESBMC ranks best among non-LLM tools here. Possible familiarity bias in configuring ESBMC (relaxed 60 s timeout, p. 12) is not discussed.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Author-built tests and author-defined metric; line-offset correction for LLMs only; possible bias toward ESBMC-friendly memory-safety CWEs. Newly written tests reduce pre-training contamination, but tests are now public (p. 1).
- External (generalisability of sample/context): [I] C only; single-file micro-programs; 25 CWEs with 10 tests each; no real-world code.
- Construct (do metrics measure the concept?): [I] CASTLE Score weights are arbitrary; TP/FN accounting inconsistent with the 150-vulnerability ground truth.
- Statistical conclusion (power, multiple comparisons, variance): [I] 6 vulnerable tests per CWE; differences of a few TPs between tools are within noise; no CIs; LLM run-to-run variance only summarised (<3%).
- Reproducibility (data/code/setup reported?): [I] Dataset and wrappers public with tool versions (p. 1, p. 9, p. 11); LLM settings and API-tool versions missing.

## 11. Future research directions
- Stated by authors [A]: refresh the dataset or use dynamic test generation to prevent overfitting (p. 14); study scalability to large codebases for LLMs and FV (p. 15); select and combine tools to fit project needs (p. 15); LLMs as real-time guidance in code-completion frameworks (p. 1).
- Suggested by us [I]: extend CASTLE to multi-file and larger programs with the same line-level labels; test LLM + FV/SAST hybrids with the combination score; publish per-CWE results and fix TP/FN accounting.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]: The broadest tool panel in our set (13 SAST incl. commercial Coverity, Snyk, SonarQube; 2 FV; 10 LLMs incl. reasoning models) on one controlled C benchmark with line-level ground truth. It supports "frontier LLMs beat SAST on small self-contained code", while its own preliminary large-file test and table inconsistencies limit how far this can be generalised. Useful for RQ2 as a contrast to real-world repo-level studies (e.g., zhou2024comparison).

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Top LLMs outscore all static and FV tools on CASTLE: GPT-o3-Mini 977, GPT-o1 962, DeepSeek R1 956, GPT-4o 954 vs ESBMC 661, CodeQL 634 | 11 | V | moderate |
| RQ1 | LLM precision/recall: GPT-o3-Mini 63%/78%, GPT-4o 54%/76%, DeepSeek R1 47%/90%; small open models 20–28% precision | 11 | V | weak |
| RQ1 | SAST recall is low: CodeQL 29% (45 TP; 45/150 would be 30%, see RQ2 denominator row), SAST average 23%; high-precision tools have very low recall (Clang 87%/9%, CBMC 100%/12%) | 11–12 | V | moderate |
| RQ1 | Some SAST tools are unusable from noise: Splint 1,027 FP and CodeThreat 1,101 FP, giving negative CASTLE scores | 11, 13 | V | moderate |
| RQ2 | Benchmark is 250 hand-written single-file C programs (mean 42 lines), balanced 150/100, line-labelled; differs strongly from real-world repo-level setups | 6 | V | strong |
| RQ2 | Table 3 TP+FN exceeds the 150 vulnerable programs for all 10 LLMs (154–179) and 4 SAST tools (155–157), so reported recall/accuracy use inconsistent denominators (e.g., CodeQL "29% (45/150)" = 45/157) | 11–12 | I | moderate |
| RQ3 | Combining ESBMC and CodeQL raises the CASTLE score to 814 (+23% vs ESBMC); overlapping tools lose score through extra FPs; no LLM+tool hybrid tested | 10, 13 | V | weak |
| RQ3 | Reasoning LLMs (o1, o3-mini) produce fewer FPs than GPT-4o/4o-mini; [I] not true for DeepSeek R1 (166 FP vs GPT-4o 116), so the claim holds for the OpenAI o-series only | 11, 14 | A | weak |
| RQ4 | FV tools miss non-formal CWEs (SQL injection, path traversal, hard-coded credentials) but have near-zero FPs; no per-CWE numbers reported | 12 | A | weak |
| RQ4 | LLM accuracy declines and FPs rise on a 400+ line merged program; most LLMs missed a single hidden vulnerability | 14 | A | weak |
| RQ5 | Open problems: LLM scalability to large codebases, line-level localisation, JSON reliability of small models, benchmark overfitting | 8, 14 | A | weak |

## 14. Key quotes
> "LLMs perform exceptionally well in the CASTLE dataset when identifying vulnerabilities in small code snippets. However, their accuracy declines, and hallucinations increase as the code size grows." (p. 1)

> "The best-performing SAST tool is CodeQL, which found 29% of the weaknesses in the code (45/150)" (p. 12)

> "most LLMs failed to detect it reliably, suggesting that these models’ effectiveness may taper off with increasing code length." (p. 14)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–18). Figures 1–3 are images; Fig. 2 combination labels are garbled in text extraction, so only the ESBMC + CodeQL combination (stated in text) is reported; other combination scores (697–758) are not attributed.
- Source version: arXiv v2 (2503.09433, 31 Mar 2025). Published version: book chapter in Lecture Notes in Computer Science, 2025 (DOI 10.1007/978-3-031-98208-8_15, from metadata; venue_kind "book", i.e., proceedings chapter). Metadata has no abstract; numbers could differ from the published chapter.
- Uncertainties: how multiple findings per test are counted in TP/FN (section 9); the exact LLM model snapshots; whether the published version corrected Table 3.
