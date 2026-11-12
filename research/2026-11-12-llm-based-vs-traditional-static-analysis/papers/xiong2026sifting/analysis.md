---
key: xiong2026sifting
status: complete
evidence_basis: full-text
design: Comparative empirical study: 3 LLM agent frameworks x 3 backbones vs vanilla prompting for filtering SAST false positives; ablations + post-cutoff check
dataset: OWASP Benchmark v1.2 (Java, synthetic) with 4 SAST tools; Vul4J real-world Java CodeQL alerts; post-cutoff OSS-Fuzz C/C++ CodeQL alerts
sample_size: OWASP 2,740 cases (1,325 negatives / 1,415 positives); Vul4J 50 sampled alerts (31 FP/19 TP); OSS-Fuzz 50 alerts (22 FP/28 TP)
metrics: residual FPR; FP identification rate (recall), precision, F1, accuracy; TP retention / miss rate; tokens, rounds, USD per task
main_finding: Best agent (SWE-agent+Claude Sonnet 4) cuts OWASP FPR 98.3%->6.3% but suppresses 22.25% of true vulns; gains depend on backbone and CWE.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Sifting the Noise: A Comparative Study of LLM Agents in Vulnerability False Positive Filtering

- Authors: Xiong, Yunpeng; Zhang, Ting
- Year / venue: 2026, Proceedings of the ACM on Software Engineering (published)
- DOI: 10.1145/3832100 · URL: https://doi.org/10.1145/3832100
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

**Version note:** our text is arXiv 2601.22952 **v3 (23 Jul 2026)**, formatted as the PACMSE ISSTA 2026 article (ISSTA009) with "Received 2026-01-30; accepted 2026-06-25" (p. 1, p. 24). It matches the DOI in metadata.

## 1. Research objective
- [A] Compare LLM-based agent frameworks (Aider, OpenHands, SWE-agent) for filtering false positives (FPs) produced by SAST tools, and find out whether agentic reasoning beats vanilla one-shot LLM prompting and at what cost (p. 1–2).

## 2. Research questions / hypotheses
- [V] RQ1: effectiveness of agent frameworks in filtering SAST FPs (OWASP Benchmark); RQ2: effectiveness on real-world Java (Vul4J/CodeQL); RQ3: which agentic capabilities drive performance and whether gains generalise to a contamination-free C/C++ setting; RQ4: success drivers and failure modes (p. 6).

## 3. Methodology
- Research design: [V] Comparative empirical study: 3 agents × 3 backbone LLMs plus vanilla zero-shot prompting, on a synthetic benchmark and real-world alerts, followed by ablations, stronger baselines and qualitative trajectory analysis (p. 2–3, p. 6–10).
- Approach / model / intervention: [V] Each agent gets the SAST warning(s) for the target file, code access, and a prompt to "verify if this static analysis finding represents a real vulnerability or an FP"; browser/web tools disabled where possible (p. 7). Backbones: Claude Sonnet 4 (claude-sonnet-4-20250514), DeepSeek Chat (deepseek-chat), GPT-5 (gpt-5-2025-08-07) (p. 7).
- Baselines or comparison conditions: [V] SAST tools alone (CodeQL v2.23.7, Semgrep v1.145.0, SonarQube Community v9.9.8, Joern v4.0.454, default rules) (p. 6); vanilla zero-shot LLM with repo structure + flagged file + findings (p. 7). [V] On OSS-Fuzz also: LLM4SA-style prompt (without LLM4SA's program-dependence context extraction), context-augmented vanilla LLM, oracle-context vanilla LLM (same files the agent opened), and four ablations (no multi-turn, no cross-file navigation, no tool-based verification, no config-file access) (p. 10). No deep-learning FP classifier baseline.

## 4. Dataset and sample
- Data source(s): [V] OWASP Benchmark for Java v1.2 (synthetic servlets with injected vulnerabilities, labelled) (p. 6); Vul4J (79 reproducible Java vulnerabilities from Project KB, 25 CWEs) (p. 8); OSS-Fuzz/OSV records for 5 C/C++ projects (mpv, libhevc, libical, gpsd, quickjs) with fixing commits 10–12 months after Claude Sonnet 4's training cutoff (p. 9).
- Sample size (N) and unit: [V] OWASP: 2,740 test cases, 1,415 vulnerable / 1,325 non-vulnerable, 11 CWEs (Table 1, p. 6). [V] Vul4J: 79 versions, 6,786,406 SLOC, 3,426 CodeQL alerts, of which 50 alerts were sampled (26 projects, 16 CodeQL rules), labelled 31 FP / 19 TP (p. 8–9). [V] OSS-Fuzz: 804 eligible CodeQL alerts, 50 sampled (seed 42), 11 rule IDs, labelled 22 FP / 28 TP (p. 9–10). [V] RQ4: 256 success and 103 failure trajectories inspected (p. 10).
- Sampling / selection method: [V] OWASP: candidate set = union of instances flagged by ≥1 SAST tool (p. 7). Vul4J and OSS-Fuzz: random sampling with fixed seed (p. 8, p. 9).
- Data availability (public? link?): [V] Scripts and data stated to be public at https://doi.org/10.5281/zenodo.18420284 (p. 21). [I] The reference list gives a different Zenodo DOI for the same artifact (10.5281/zenodo.21282004, ref [6], p. 21); which is current is unclear.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Aider v0.86.1, OpenHands Agent SDK v1.5.2, SWE-agent commit 1d3cfb (p. 7). [V] Temperature 0 (p. 19). [V] Browser-access check on 50 OWASP cases with OpenHands+Claude: 86.0% FP identification with browser disabled vs 82.0% enabled (p. 7). [V] Vul4J ground truth: method-level patch matching (2 TPs) plus manual labelling of 48 alerts by the first author (6 years' experience), about 20 person-hours (p. 8–9). [V] OSS-Fuzz ground truth: two independent raters, 86.0% raw agreement, Cohen's κ = 0.725, disagreements resolved by discussion (p. 10). Number of runs per case: not reported (appears to be one).
- Code availability: [V] Zenodo artifact (p. 21).

## 6. Evaluation metrics
- [V] RQ1 FPR: share of non-vulnerable instances flagged positive; after filtering, the remaining FPR (p. 7, p. 12).
- [V] RQ2/RQ3: alert-level binary classification with SAST FPs as the positive class: Identified FP, Missed FP, Mis-identified FP (true vulnerability wrongly filtered, a "safety violation"), Correct Retention; recall = FP identification rate, precision = share of alerts called FP that truly are FP, F1, accuracy (p. 9, p. 10).
- [V] TP retention / miss rate on OWASP positives (p. 18). Cost: average rounds, tokens and USD per task (p. 17).
- Statistical testing: not reported. [I] The abstract says agents "significantly outperform" vanilla prompting (p. 1), but no significance test is reported; Cohen's κ is the only statistic.

## 7. Key findings
1. [V] SAST alone on OWASP: CodeQL precision 60.3%, recall 97.0%, F1 74.4%, FPR 68.2% (904 FPs); Semgrep precision 56.3%, recall 90.4%, FPR 74.8%; SonarQube precision 51.9%, recall 95.6%, FPR 94.6% (1,254 FPs); Joern precision 54.7%, recall 8.2%, FPR 7.2% (Table 2, p. 10–11).
2. [V] FPs are largely shared across tools: 36 FP instances flagged by all four tools; CodeQL, Semgrep and SonarQube jointly flag 710 (p. 11).
3. [V] The union of tools flags 1,303 of 1,325 non-vulnerable cases (98.3% FPR); after agent filtering the remaining FPR is 6.3% (SWE-agent+Claude), 14.3% (Aider+Claude), 14.9% (OpenHands+Claude), vs 23.0% for vanilla Claude; DeepSeek: vanilla 11.2% is best, agents 13.1–15.8%; GPT-5: vanilla 20.4%, agents 14.1–20.3% (Table 3, p. 12).
4. [V] TP retention (SWE-agent+Claude, OWASP positives): 314 of 1,411 completed runs wrongly labelled FP; retention 77.7%, miss rate 22.25%. Miss rate is ≤2.38% for CWE-78/89/79/90/643 but 77.17% CWE-327, 84.50% CWE-328, 77.11% CWE-501, 50.00% CWE-614 (p. 18).
5. [V] Vul4J (50 CodeQL alerts, 62% FP): best F1 83.3% (GPT-5+Aider: recall 92.6%, precision 75.8%); highest FP recall 93.3% (GPT-5+OpenHands, precision 70.0%); OpenHands+DeepSeek precision 100%, recall 38.7%; Claude agents beat vanilla Claude (F1 80.7% Aider vs 69.1%) (Table 4, p. 13–14).
6. [I] Derived from Table 4 (p. 13): row percentages imply some runs did not complete (e.g., GPT-5+Aider ≈ 41 scored alerts). For all four GPT-5 settings (incl. vanilla), Mis-identified FP (19.0–25.0% of alerts) against Correct Retention (12.5–21.3%) means about half to two-thirds (≈47–67%) of the true vulnerabilities in the scored sample were filtered out. The authors discuss mis-identification qualitatively (p. 14: for GPT-5 "the primary differentiator shifts to how effectively the framework avoids mis-identifying true vulnerabilities") but do not report it as a share of true vulnerabilities lost.
7. [V] OSS-Fuzz C/C++ (post-cutoff, Claude Sonnet 4): full SWE-agent accuracy 96.0%, precision 95.5%, recall 95.5%, F1 95.5%; vanilla recall 36.4%, F1 51.6%; LLM4SA-style F1 70.8%; context-augmented F1 66.7%; oracle-context F1 51.6%. Ablations: without cross-file navigation F1 62.5%, without multi-turn 56.3%, without tool verification 88.9%, without config read 97.7% (Table 5, p. 15).
8. [A] The agentic gain comes from iterative evidence gathering, not context volume, because the oracle-context baseline equals vanilla (p. 15).
9. [V] Cost per task (OWASP): from $0.0028 (Aider+DeepSeek, 11,036 tokens) to $0.1867 (OpenHands+Claude, 20.5 rounds, 219,299 tokens); SWE-agent+Claude $0.1501, 130,846 tokens (Table 8, p. 17).
10. [V] Contamination checks: filename-only probe stays at chance (49.8–51.6% accuracy); no trajectory among 15,636 claims prior exposure (p. 18).
11. [V] Weaker-backbone "scope drift": in 145 cases DeepSeek+SWE-agent turned a correct vanilla FP verdict into TP, reporting other issues (stack traces, cookies, CRLF) instead of the alerted CWE (p. 18–19).
12. [V] Failure modes: incorrect CWE attribution, overly conservative threat modelling, surface-level pattern matching; concentrated in CWE-327 (85 trajectories) and CWE-614 (24) (Table 7, p. 15–17).

## 8. Limitations stated by the authors
- [A] LLM non-determinism; temperature 0 helps but does not guarantee determinism (p. 19).
- [A] Vul4J uses only 50 alerts, mostly labelled by the first author; the sample may not represent the full alert distribution or rule mix (p. 20).
- [A] OSS-Fuzz is a focused 50-alert validation set, not a full C/C++ benchmark, and does not rank all agents/models (p. 20).
- [A] Alert-specific labels count an agent wrong when it rejects the alert's rationale but finds a different real issue (p. 20).
- [A] Real-world evaluation mainly uses CodeQL alerts (p. 20).
- [A] Agents should not be used for automatic suppression; they suit decision support (p. 19).

## 9. Limitations we identified
- [I] Numbers are inconsistent: the abstract says an initial FP rate of "over 92%" (p. 1), while the results give 98.3% (p. 12). The "↓" values in Table 3 (e.g., 92.1%) look like percentage-point drops, while Lesson 1 calls them "eliminating more than 92% of FPs" (p. 19); relative reduction would be about 93.6% [our arithmetic from 98.3% → 6.3%].
- [I] OWASP is synthetic (single-file servlets with injected flaws, p. 6), and RQ1 filters only negatives, with TP retention measured for one configuration only (p. 18). Without a full confusion matrix per configuration, precision/recall of the hybrid pipeline on OWASP cannot be compared across agents.
- [I] Real-world Java (N=50) and C/C++ (N=50) samples are small; per-cell differences of a few alerts change the percentages a lot, and no confidence intervals are given.
- [I] Incomplete runs are dropped silently in Table 4 (denominators below 50), which can bias comparisons between configurations.
- [I] No deep-learning or classical ML FP-classifier baseline, so LLM vs DL cannot be compared here (RQ1).
- [I] The OWASP filename-only probe tests label memorisation, not whether the models know OWASP code patterns; the post-cutoff C/C++ check addresses this better, but only for one configuration.
- [I] Ablation "w/o config read" scores higher than the full agent (F1 97.7% vs 95.5%, p. 15), which shows noise of about one alert at N=50.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Single annotator for most Vul4J labels (p. 20); dropped runs; possible prior exposure of models to OWASP and Vul4J (partly probed, p. 18).
- External (generalisability of sample/context): [I] Mostly Java; synthetic benchmark for the main comparison; C/C++ only for the best configuration and 5 projects (p. 20).
- Construct (do metrics measure the concept?): [I] RQ1 "remaining FPR" ignores true-vulnerability loss unless read with Section 5.2; alert-specific labels (acknowledged, p. 20).
- Statistical conclusion (power, multiple comparisons, variance): [I] No tests, many configurations compared, small real-world N, apparently single runs.
- Reproducibility (data/code/setup reported?): [V] Tool versions, model IDs and artifact are given (p. 6–7, p. 21). [I] Two different Zenodo DOIs are listed.

## 11. Future research directions
- Stated by authors [A]: CWE-aware, cost-adaptive agent strategies; human-in-the-loop auditing to keep TPs; more languages and SAST tools (p. 20). Lightweight execution-based checks (p. 16).
- Suggested by us [I]: full confusion-matrix reporting per configuration on real-world code; larger, multi-rater real-world alert sets; comparison with DL FP classifiers.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]: Strong evidence for RQ3 (SAST + LLM-agent post-filtering), with explicit cost per alert and a measured TP-suppression risk. Per-CWE results (injection filtered well; crypto/policy CWEs poorly) feed RQ4. SAST-alone figures on OWASP give a clean baseline for RQ1. The post-cutoff C/C++ set is a rare contamination control for RQ2.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | SAST alone on OWASP v1.2: CodeQL P 60.3% R 97.0% FPR 68.2%; Semgrep FPR 74.8%; SonarQube FPR 94.6%; Joern R 8.2% | p. 11 | V | moderate |
| RQ3 | Agent post-filtering cuts union-of-SAST FPR 98.3% → 6.3% (SWE-agent+Claude Sonnet 4) vs 23.0% vanilla Claude | p. 12 | V | moderate |
| RQ3 | Same best config wrongly filters 22.25% of true vulnerabilities (314/1,411) | p. 18 | V | moderate |
| RQ3 | Agent benefit is backbone-dependent: DeepSeek vanilla (11.2%) beats its agents (13.1–15.8%) | p. 12 | V | moderate |
| RQ3 | Cost per alert $0.0028–$0.1867, 11k–269k tokens depending on agent/model | p. 17 | V | moderate |
| RQ1/RQ3 | Real-world Java (50 CodeQL alerts): up to 93.3% FP recall, best F1 83.3% | p. 13 | V | weak |
| RQ3/RQ5 | On real-world Java, all four GPT-5 settings (incl. vanilla) filter out ≈47–67% of the true vulnerabilities (≈14–19 TPs per configuration; derived from Table 4 percentages) | p. 13 | I | weak |
| RQ2/RQ3 | Post-cutoff C/C++ (50 alerts): SWE-agent F1 95.5% vs vanilla 51.6%, LLM4SA-style 70.8% | p. 15 | V | weak |
| RQ4 | Injection CWEs filtered reliably (miss ≤2.38%); crypto/policy CWEs poorly (miss 50–84.5%) | p. 18 | V | moderate |
| RQ5 | Agents unsuitable for automatic suppression; human-in-the-loop needed | p. 19 | A | moderate |
| RQ2 | Abstract "over 92%" vs results 98.3% initial FPR; reduction reported as pp, described as % | p. 1, p. 12, p. 19 | I | weak |

## 14. Key quotes
> "reducing an initial FP detection rate of over 92% on the OWASP Benchmark to as low as 6.3% in the best configuration" (p. 1)
> "The agent incorrectly labeled 314 true vulnerabilities as FPs, resulting in a TP retention of 77.7% and a miss rate of 22.25%." (p. 18)
> "LLM-based agents are unsuitable for unconditional, automatic suppression of SAST warnings" (p. 19)

## Analyst notes
- Reading coverage: whole paper read (pp. 1–21 text; pp. 21–24 references only). Heatmaps (Fig. 5, Fig. 7) read from the text layer; values match the prose.
- Venue: peer-reviewed PACMSE (ISSTA 2026) article; the full text we hold is the arXiv v3 copy of it.
- Uncertainties: exact denominator for "remaining FPR" (1,325 vs 1,303) not stated; number of runs per case not stated; the Table 4 denominators (<50) are our inference from the percentages.
