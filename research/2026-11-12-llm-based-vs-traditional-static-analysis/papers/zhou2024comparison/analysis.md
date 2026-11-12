---
key: zhou2024comparison
status: complete
evidence_basis: full-text
design: Empirical comparison, 15 SAST tools vs 12 open-source LLMs (fine-tuned + prompted) on repo-level detection; preprint
dataset: Real-world CVE repos: Java (Li et al.), C (Lipp et al.), new Python dataset from NVD
sample_size: 270 CVEs in 134 repos (87 Java, 85 C, 98 Python); ~5.5M functions; random 8:1:1 split, test set roughly 8-10 CVEs per language
metrics: Vulnerability detection ratio (S1 any function, S2 all functions); marked function ratio as FPR proxy; no precision/F1
main_finding: SAST tools detect few vulnerabilities (up to 44.4%) but mark few functions; LLMs detect up to 100% but mark up to 77.4%.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Comparison of Static Application Security Testing Tools and Large Language Models for Repo-level Vulnerability Detection

- Authors: Zhou, Xin; Tran, Duc-Manh; Le-Cong, Thanh; Zhang, Ting; Irsan, Ivana Clairine; Sumarlin, Joshua
- Year / venue: 2024, arXiv (preprint) — **not peer-reviewed**
- DOI: 10.48550/arxiv.2407.16235 · URL: https://arxiv.org/abs/2407.16235
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] To compare SAST tools with LLMs for detecting vulnerabilities in whole repositories, understand the pros and cons of each family, and explore combining them (p. 1).
- [A] Introduces a "repo-level" detection task: find the vulnerable functions among all functions of a repository rather than only among functions in files touched by a fix commit (p. 2–3).

## 2. Research questions / hypotheses
- [V] RQ1: How effective are SAST tools and LLMs? RQ2: Which is more effective, SAST tools or LLMs? RQ3: To what extent can combining multiple SAST tools or LLMs improve detection? (p. 7).
- No formal hypotheses (p. 7).

## 3. Methodology
- Research design: [V] Empirical benchmark study; 15 SAST tools and 12 open-source LLMs evaluated on the same held-out test sets for Java, C and Python (p. 5, p. 7).
- Approach / model / intervention: [V] LLMs: 4 lightweight (<1B) models — CodeBERT, GraphCodeBERT, CodeT5, UniXcoder — with full fine-tuning; 8 large (3.8B–8B) decoder models — CodeLlama-7B, Llama3-8B, CodeQwen-7B, DeepSeek-Coder-6.7B, Mistral-7B, Phi3-3.8B, StarCoder-7B, StarCoder2-7B — with LoRA fine-tuning (PEFT), zero-shot, chain-of-thought ("Let's think step by step") and few-shot (2 examples) prompting (p. 4–5). [V] Repositories are split into functions with Tree-sitter, each function classified separately, and predictions aggregated per repository (p. 3).
- Baselines or comparison conditions: [V] SAST, all free/open-source: Java — CodeQL, Contrast Codesec Scan, Horusec, Insider, SpotBugs, Semgrep, SonarQube CE; C — Flawfinder, Cppcheck, Infer, CodeChecker, CodeQL; Python — Bandit, Dlint, DevSkim, CodeQL, Graudit, Semgrep (p. 4). [V] Commercial LLMs excluded from the main study because of cost and non-reproducibility (p. 4); a small side experiment uses gpt-3.5-turbo-0125 (p. 9). [V] Ensembles: union of all SAST tools per language; voting over 12 fine-tuned LLMs at >50%, >2/3 and >80% thresholds (p. 8–9). [I] No ensemble combining SAST and LLM outputs is actually run, despite the abstract and conclusion wording (based on p. 8–9 vs p. 1, p. 11).

## 4. Dataset and sample
- Data source(s): [V] Java from Li et al. (SAST study for Java), C from Lipp et al. (static C analyzers study), both real-world CVEs whose repositories were re-downloaded; new Python dataset built from NVD 2002–2023 entries linked to GitHub fix commits (p. 3).
- Sample size (N) and unit: [V] Java 50 projects / 87 CVEs / 3,986,848 functions (vulnerable ratio 0.008%); C 6 projects / 85 CVEs / 1,181,556 functions (0.009%); Python 78 projects / 98 CVEs / 312,045 functions (0.18%) (p. 3). Unit of detection = CVE within a repository; unit of marking = function.
- Sampling / selection method: [V] Repositories kept only if downloadable via the GitHub API (Java) or per the original authors' instructions (C); Python projects that errored during SAST scanning were omitted (p. 3). [V] Vulnerable functions = pre-fix versions of functions changed by the fix commit; all other functions labelled non-vulnerable (p. 3–4). [V] Random 8:1:1 train/validation/test split; SAST and LLMs evaluated on the same test sets (p. 5). Test-set sizes: not reported. [I] Detection ratios move in steps of 12.5 (Java), 11.1 (C) and 10.0 (Python) points in Table 3 (p. 6), implying test sets of about 8, 9 and 10 vulnerabilities.
- Data availability (public? link?): [A] Code and data are "publicly accessible" (p. 10); no link given in the text.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Fine-tuning on a balanced training set (all vulnerable functions + equal number of random non-vulnerable functions), 20 epochs, batch size 8, best snapshot on a balanced validation set; LoRA r = 8, α = 16; Hugging Face; Ubuntu 22.04 with an NVIDIA RTX A5000 GPU; models capped at 8B parameters due to compute (p. 4–5, p. 7). [V] Prompt: "If the following code snippet has any vulnerabilities, output Yes; otherwise, output No" with code markers (p. 4). [V] ChatGPT side experiment: 1:100 vulnerable:clean sample, temperature 0 (p. 9). SAST tool versions and rule configurations: not reported. Runtime and monetary cost: not reported.
- Code availability: [A] stated public, no URL (p. 10).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] Vulnerability detection ratio = detected vulns / all vulns; Scenario 1 (S1): at least one vulnerable function of the CVE flagged; Scenario 2 (S2): all vulnerable functions flagged (p. 5). [V] Marked function ratio = flagged functions / all functions, used as an approximation of the false-positive rate because only 0.008–0.18% of functions are vulnerable (p. 5). [V] Precision and F1 deliberately not computed because unknown vulnerabilities may exist (p. 5).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): not reported; single runs, no variance or CIs. [V] A rank-sum heuristic (rank by S2 + rank by marked ratio) picks the "best" approach (p. 8).

## 7. Key findings
1. [V] SAST detection is low: many tools detect 0% (CodeQL, Contrast, Insider, SpotBugs, SonarQube for Java; Flawfinder, Cppcheck, CodeChecker for C; CodeQL, Graudit for Python) and SAST tools mark only 0.2%–5.2% of functions (p. 6–7). Best per text: Horusec Java S1 37.5%; CodeQL C 44.4% S1 / 33.3% S2; DevSkim Python 30.0% / 20.0% (p. 7). Infer (C) 11.1% / 11.1% with 0.9% marked; Semgrep Python 10.0% / 10.0% with 0.6% marked (p. 6).
2. [V] LLMs detect much more but flag many functions: up to 100% S1 / 87.5% S2 in Java (fine-tuned Llama3, 21.8% marked), 100% / 88.9% in C (fine-tuned CodeBERT, GraphCodeBERT, UniXcoder; 25.6–44.6% marked), 90% / 90% in Python (fine-tuned CodeT5, 50.5% marked) (p. 6). LLMs mark 8.3–77.4% of functions in Java, 3.5–70.1% in C, 14.9–73.4% in Python (p. 7).
3. [V] Fine-tuning beats prompting for large LLMs: in Java, PEFT models average 73.4% (S1) / 51.6% (S2) detection with 19.4% marked vs 52.1–55.0% marked for prompting (p. 7). Fine-tuned lightweight models detect 10.6% / 9.1% more (S1 / S2) than fine-tuned large ones in Java but mark 43.2% more functions (p. 7). [I] All three figures are relative gains, not percentage points: Table 3 Java means are 81.25 vs 73.44 (S1, ≈ +7.8 points), 56.25 vs 51.56 (S2, ≈ +4.7 points) and 27.8 vs 19.4 marked (p. 6; PEFT CodeLlama marked read as 8.3, see section 9).
4. [A] By the rank-sum metric, best approaches are fine-tuned DeepSeek-Coder (Java), UniXcoder (C) and Llama3 (Python); the best choice depends on language and tolerated marked ratio (p. 8).
5. [V] Union of SAST tools raises detection: Java S1 37.5% → 50.0% (marked 1.7% → 4.3%); C 44.4% → 55.6% S1 and 33.3% → 44.4% S2 (marked 5.2% → 7.2%); Python 30.0% → 50.0% S1 and 20.0% → 40.0% S2 (marked 4.5% → 7.7%) (p. 8).
6. [V] Voting over 12 fine-tuned LLMs (>2/3) cuts the marked ratio by 61.7% (Java), 74.6% (C), 40.9% (Python) relative to the LLM average while keeping detection near the best single LLM; >80% voting gives marked ratios 0.8–9.2% but S2 detection only 0–37.5% (p. 9).
7. [A] Combined LLMs are best for Java; combined SAST tools are best for C and Python (p. 9).
8. [V] CWE view (languages merged, SAST union vs union of the 2 best LLMs): CWE-119 best detected (LLM group 100%), CWE-476 second; CWE-835 and CWE-89 detected by neither group (p. 8).
9. [V] ChatGPT (gpt-3.5-turbo-0125, 1:100 sample, averaged over languages): S1 3.7% zero-shot, 3.7% CoT, 23.2% few-shot, marked 1.3–10.8%; fine-tuned CodeBERT 89.2% S1 / 35.7% marked and fine-tuned Llama3 67.4% / 20.1% in the same setting (p. 10).

## 8. Limitations stated by the authors
- [A] Undiscovered vulnerabilities may exist in the benchmarks; the study only measures detection of known vulnerabilities (p. 10).
- [A] Possible data leakage from LLM pre-training; argued to be minor because prompting performs worse than fine-tuning (p. 10).
- [A] Commercial LLMs excluded from the main study due to cost (p. 4, p. 9); models limited to ≤8B parameters by compute (p. 4).
- [A] Only generic LLM techniques used, no specialised designs (p. 10).

## 9. Limitations we identified
- [I] Very small test sets: detection ratios are multiples of ~10–12.5 points (Table 3, p. 6), so each language result rests on about 8–10 CVEs; one CVE moves a ratio by 10+ points. No variance, repeated splits or CIs. Most cross-tool differences are therefore statistically unreliable.
- [I] Typesetting defect in Table 3 (dropped leading digits), not conflicting results. Table 3 prints Horusec Java S1 = 7.5, CodeQL C = 4.4 / 3.3, DevSkim Python = 0.0 / 0.0 and truncated cells ".0", ".3", ".5" (p. 6; present in the rendered PDF), while the text gives 37.5, 44.4 / 33.3 and 30.0 / 20.0 (p. 7). The text values are consistent with the table's other cells: ".3" (PEFT CodeLlama, Java marked) must be 8.3, the lower bound of the stated Java range "8.3% to 77.4%" (p. 7), and it reproduces the stated PEFT mean of 19.4% (p. 6–7); ".5" (PEFT Llama3, C marked) matches the lower bound 3.5 of "3.5% to 70.1% in C" (p. 7); 7.5 is not a multiple of the 12.5-point Java step. Two more cells fall below the stated ranges and are probably affected too: C Starcoder2 PEFT marked 0.3 (< 3.5) and Python DeepSeek-Coder few-shot marked 4.9 (< 14.9) (p. 6–7). We quote best-SAST numbers from the text.
- [I] Abstract and conclusion say that ensembling "the SAST tools and LLMs" mitigates both families' drawbacks (p. 1, p. 11), but experiments only combine SAST with SAST and LLM with LLM (p. 8–9). This paper gives no direct evidence on SAST+LLM hybrids.
- [I] Asymmetric comparison: LLMs were fine-tuned on 80% of the same CVE distribution (random CVE-level split, so the same project can appear in train and test), while SAST tools run untuned. Project-level leakage is not discussed.
- [I] The marked function ratio is a proxy for false positives, not an FPR; with no precision/F1, numbers cannot be pooled with precision/recall-based studies.
- [I] SAST versions, rule sets and configurations not reported; 0% results (e.g., CodeQL on Java and Python) may reflect configuration or build issues rather than tool capability.
- [I] Fine-tuned models train on balanced data but are tested on extremely imbalanced repositories, which plausibly explains the high marked ratios.
- [I] The PDF running header uses an "ESEC/FSE'23" template although this is a 2024 preprint (p. 2); it is not evidence of peer review.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Random CVE-level split without project grouping; label noise from the fix-commit heuristic (all other functions labelled clean, p. 3–4); pre-training leakage acknowledged by the authors (p. 10).
- External (generalisability of sample/context): [I] Only ≤8B open models and free SAST tools; the C dataset has only 6 projects (p. 3); no commercial SAST and no frontier LLMs beyond a small GPT-3.5 test.
- Construct (do metrics measure the concept?): [I] S1 counts a CVE as detected if any one of its functions is flagged, which favours tools that flag many functions; the marked ratio only approximates FPR.
- Statistical conclusion (power, multiple comparisons, variance): [I] ~8–10 test CVEs per language, single run, no tests; many comparisons across 15 tools × 12 LLMs × 4 adaptations.
- Reproducibility (data/code/setup reported?): [I] Hyper-parameters reported (p. 5, p. 7); code/data claimed public without a link (p. 10); SAST configuration missing.

## 11. Future research directions
- Stated by authors [A]: shift from function-level to repo-level detection (p. 10); reduce LLM marked ratios via filtering untrustworthy predictions, adding repository structure context, better prompting or ensembles (p. 10); combine LLMs and SAST tools more effectively (p. 10–11).
- Suggested by us [I]: re-run with project-grouped splits, multiple seeds and larger test sets; measure precision on manually triaged samples; actually test SAST+LLM hybrids (e.g., LLM triage of SAST alerts). Based on the limitations in section 9.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]: One of the few studies comparing many SAST tools with many fine-tuned and prompted LLMs on the same real-world, multi-language data. It supports the recurring pattern "SAST = low recall, few alarms; LLM = high recall, many alarms", but its small test sets, a typesetting defect in Table 3 and preprint status make it moderate-to-weak evidence.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Best single SAST tools detect 37.5% (Java, Horusec), 44.4% (C, CodeQL), 30.0% (Python, DevSkim) of test CVEs (S1), marking 0.2–5.2% of functions; many SAST tools detect 0% | 6–7 | V | weak |
| RQ1 | LLMs reach up to 100% (Java, C) and 90% (Python) S1 detection but mark 3.5–77.4% of functions | 6–7 | V | weak |
| RQ1 | LoRA-fine-tuned large LLMs beat zero-shot/CoT/few-shot prompting: Java 73.4% S1 with 19.4% marked vs 52.1–55.0% marked for prompting | 7 | V | weak |
| RQ1 | GPT-3.5 prompting detects only 3.7–23.2% (S1) on a 1:100 sample, far below fine-tuned CodeBERT (89.2%) and Llama3 (67.4%) | 10 | V | weak |
| RQ2 | Repo-level task with 0.008–0.18% vulnerable functions vs 4.5–9.2% in function-level datasets; precision/F1 not computed, marked-function ratio used as FPR proxy | 3, 5 | V | moderate |
| RQ2 | Test sets of roughly 8–10 CVEs per language (inferred from 12.5/11.1/10-point steps in Table 3); no variance reported | 6 | I | weak |
| RQ3 | Union of SAST tools raises detection by 25.2–100% relative (e.g., Python S1 30.0% → 50.0%) at small marked-ratio cost (4.5% → 7.7%) | 8 | V | weak |
| RQ3 | Voting over 12 fine-tuned LLMs cuts the marked ratio by 40.9–74.6%; >80% voting gives 0.8–9.2% marked but 0–37.5% S2 detection | 9 | V | weak |
| RQ3 | No SAST+LLM hybrid is evaluated, although abstract/conclusion claim that ensembling SAST tools and LLMs mitigates drawbacks | 1, 8–9, 11 | I | moderate |
| RQ4 | Best approach differs by language: combined LLMs best for Java, combined SAST best for C and Python | 9 | A | weak |
| RQ4 | CWE-119 best detected (LLM group 100%), CWE-476 second; CWE-835 and CWE-89 missed by both SAST and LLM groups | 8 | V | weak |
| RQ5 | High LLM marked-function ratios need filtering, repository context, better prompts or ensembles; repo-level evaluation recommended over function-level | 10 | A | moderate |

## 14. Key quotes
> "SAST tools obtained low vulnerability detection ratios (up to 44.4%) and many failed to detect any vulnerabilities." (p. 2)

> "LLMs mark 8.3% to 77.4% of functions in Java, 3.5% to 70.1% in C, and 14.9% to 73.4% in Python." (p. 7)

> "We also cannot compute the F1 score, as it is based on Precision." (p. 5)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–11), references skimmed (pp. 11–13); Table 3 and Figs. 3–7 checked on the rendered PDF (pp. 6, 8, 9).
- Source version: arXiv v1 (2407.16235, 23 Jul 2024). Preprint, not peer-reviewed; the "ESEC/FSE'23" running header is a template artefact. Check whether a peer-reviewed version exists and prefer it if so.
- Uncertainties: several Table 3 cells lost their leading digit in typesetting (section 9); the text values are consistent with the rest of the table and are quoted for best SAST tools. Test-set sizes are inferred, not reported. The "SAST+LLM ensembling" claim in abstract/conclusion is not backed by an experiment.
