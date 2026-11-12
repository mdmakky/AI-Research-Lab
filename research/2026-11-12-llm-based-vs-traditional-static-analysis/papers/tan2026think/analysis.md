---
key: tan2026think
status: complete
evidence_basis: full-text
design: controlled factorial empirical study; 4 open LLMs x instruct/thinking mode x zero/few-shot x NA/SA/DA/MA orchestration (64 configs), call-matched baselines, blinded human + calibrated LLM-judge explanation study
dataset: PrimeVul Pair (C/C++ functions; 870 instances = 435 vulnerable + 435 benign paired functions); 193-pair subset for call-matched runs
sample_size: 870 functions (435 pairs) x 64 configurations; 120 human-rated and 480 judge-rated explanations
metrics: accuracy, precision, recall, F1, pair-wise correct prediction (P-C), FPR, predicted-positive rate, F1 SD/CV; explanation Likert scores; GPU-hours, kWh, tokens, USD
main_finding: Thinking raises non-agent F1 0.31->0.41 (p=0.023) via recall at 2.7-4.4x energy; dual-agent tops F1 by flagging 88.2%; self-revision matches multi-agent pairwise accuracy.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# To Think or Not to Think: Evaluating LLM Reasoning and Agents in Vulnerability Detection

- Authors: Tan, Hua Beng; Widyasari, Ratnadira; Astekin, Merve; Goknil, Arda; Sözer, Hasan; Tun, Yan Naing; Husom, Erik Johannes; Shar, Lwin Khin; Jiang, Lingxiao
- Year / venue: 2026, Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering (published)
- DOI: 10.1145/3832783.3837521 · URL: https://doi.org/10.1145/3832783.3837521
- Source text: `fulltext.txt` from the user-supplied publisher PDF (ACM version of record, ASE '26, 13 pages, printed pp. 2856–2868; page refs = PDF page index).

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
Separate the effects of reasoning-enabled ("thinking") inference, agentic orchestration and explanation quality on LLM vulnerability detection, which prior work examined separately or under heterogeneous settings [A] (p. 1, p. 2).

## 2. Research questions / hypotheses
- RQ1: Do reasoning-enabled LLMs outperform non-reasoning LLMs in software vulnerability detection? [V] (p. 2)
- RQ2: How do multi-agent configurations compare with single-agent setups in performance, cross-setting stability and improvement consistency? [V] (p. 2)
- RQ3: How does explanation quality differ between thinking and non-thinking LLMs? [V] (p. 2)
- No formal hypotheses.

## 3. Methodology
- Research design: controlled, factor-separated (factorial) experiment. RQ1: 4 models × 2 modes × 2 prompting strategies, non-agent = 16 configurations; RQ2: same × 3 agent designs = 48 configurations; RQ3 on the generated outputs [V] (p. 3, Table 1). Additional call-matched and role-sensitivity experiments (p. 10, p. 11).
- Approach / model / intervention: Nemotron-Nano-8B, Nemotron-Super-49B, Qwen3-4B, Qwen3-30B-A3B, each in instruct and thinking mode [V] (p. 3, p. 4). Designs: NA (direct call, no state); SA (one agent); DA (Code Author proposes, Security Analyst reviews and decides); MA (Security Researcher, Code Author, Moderator, Review Board) [V] (p. 4). Zero-shot and few-shot prompts with identical structure and examples across models/modes [V] (p. 4).
- Baselines or comparison conditions: instruct mode vs thinking mode; SA as the agentic baseline; call-matched self-revision with 2 and 4 calls, best-of-4 at T = 0.7, and VulAgent-lite (a specialist hypothesis–validation workflow without Joern CFG/DFG) [V] (p. 10, p. 11). No SAST tools, no fine-tuned deep-learning detectors, no proprietary LLMs as detectors.

## 4. Dataset and sample
- Data source(s): PrimeVul Pair; each vulnerable function paired with a benign counterpart sharing ≥80% of its string content; the counterpart is not shown at inference [V] (p. 3, p. 5).
- Sample size (N) and unit: 870 functions (435 vulnerable, 435 benign) per configuration [V] (p. 3); call-matched experiments on a pair-preserving 193-pair subset, 2 largest models, zero-shot [V] (p. 11). RQ3: 120 explanations (60 snippets × 2 modes, 15 per TP/TN/FP/FN) rated by 2 blinded humans; paired tests on 59 pairs; LLM judge on a 480-explanation frame (2 models × 2 modes × 4 strata × 30) [V] (p. 5, p. 9).
- Sampling / selection method: full PrimeVul Pair set for RQ1/RQ2; how the 193-pair subset was chosen is not reported beyond "pair-preserving" (p. 11). No power analysis.
- Data availability (public? link?): replication package with code, prompts and dataset on Zenodo, https://doi.org/10.5281/zenodo.21401826 [V] (p. 5, p. 12).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: vLLM v0.17–v0.18, 64K context window, NVIDIA H100 80GB on RunPod; temperature 0; pilot repetitions showed no variation, so one run per configuration [V] (p. 4). Agents built with the AG2 framework [V] (p. 4). Outputs auto-parsed to binary labels; non-conforming outputs "handled conservatively" (exact rule not reported) [V] (p. 5). LLM judge: Claude Sonnet 4.6 with 24 few-shot exemplars from held-out human ratings, validated by 5-fold cross-validation against the inter-human agreement level; Claude Opus 4.8 tried as an alternative [V] (p. 5, p. 9). Cost assumes RunPod H100 SXM at $2.69/GPU-hour [V] (p. 10).
- Code availability: yes, Zenodo package (p. 12).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: accuracy, precision, recall, F1 (directly interpretable because the data are balanced); P-C, the share of pairs where both functions are classified correctly, to measure discrimination between near-identical code (following Ding et al.) [V] (p. 5). Alert burden: false-positive rate and predicted-positive rate [V] (p. 7). Stability: mean F1, SD and coefficient of variation across settings; improvement consistency = share of matched settings beating SA [V] (p. 5). Explanations: completeness, informativeness, clarity, actionability on 1–5 Likert scales [V] (p. 5). Cost: GPU-hours, kWh, input/output tokens, USD [V] (p. 10).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): Wilcoxon signed-rank with Cohen's d for RQ1/RQ2 [V] (p. 6, p. 7); Wilcoxon signed-rank with Bonferroni for paired explanation scores, Mann–Whitney for correct vs incorrect, Spearman and partial Spearman for length effects [V] (p. 5, p. 8, p. 9). No confidence intervals reported; the reasoning × orchestration interaction is not significance-tested [A] (p. 8).

## 7. Key findings
1. Non-agent: thinking beats instruct F1 in 7 of 8 model–prompt settings; mean F1 0.31 → 0.41 (Wilcoxon p = 0.023, Cohen's d = 1.37); accuracy barely changes (0.518 vs 0.523, p = 0.46), so the gain is a recall shift — [V] (p. 6).
2. Best non-agent F1: Nemotron-Super-49B thinking zero-shot F1 0.620 (recall 0.749, precision 0.529); best non-agent P-C: Qwen3-30B-A3B instruct zero-shot 22.5% — [V] (p. 6, Table 2). Nemotron-Nano-8B stays weak (zero-shot recall 0.005–0.048) — [V] (p. 6).
3. Thinking improves P-C in 6 of 8 non-agent settings — [V] (p. 6).
4. Agent designs (means over 16 settings): SA F1 0.368 / recall 0.326 / P-C 13.7; DA F1 0.634 / recall 0.885 / precision 0.502 / P-C 6.2; MA F1 0.497 / recall 0.559 / P-C 15.8 — [V] (p. 7, Table 3).
5. DA flags 88.2% of functions (PPR 0.882, FPR 0.880) vs SA 30.3% (FPR 0.280) and MA 55.4% (FPR 0.549); DA vs SA F1 p < 0.0001, d = 1.40; MA vs SA p = 0.0013, d = 0.92 — [V] (p. 7).
6. DA beats SA on F1 in all 16 settings and is the most stable (CV 9% vs MA 32%, SA 46%); MA has the best P-C in 11 of 16 settings, DA in none — [V] (p. 7, p. 8).
7. Thinking's F1 benefit reverses with orchestration: ΔF1 +0.104 (NA), +0.100 (SA), −0.054 (DA), −0.066 (MA); ΔP-C stays positive (+1.9, +1.5, +8.1, +5.4) — [V] (p. 8, Table 5).
8. Call-matched (193 pairs, zero-shot, 2 models): 4-call self-revision has the highest mean P-C (24.7) vs SA and MA (21.9) and DA (4.7), with FPR 0.47 vs DA 0.93; the authors conclude much of the multi-agent benefit is extra inference budget — [V]/[A] (p. 11, Table 9).
9. Cost: thinking uses 2.7–4.4× more energy and 2.5–3.6× more output tokens; MA-thinking averages 25,533 tokens per sample vs 3,703 for NA; per configuration SA $27.5 / 8.0 h, DA $37.1 / 11.5 h, MA $52.7 / 14.4 h; all 64 configurations cost about $2,448, 481 kWh and 423.0M tokens — [V] (p. 10, Table 8).
10. Explanations (Nemotron-Super-49B, 59 pairs): the LLM judge rates thinking higher on completeness (+0.49), clarity (+0.51) and informativeness (+0.64); humans corroborate only informativeness (+0.30, p = 0.006) — [V] (p. 8).
11. Thinking explanations are 4.6× longer (13,579 vs 2,935 chars); controlling for length shrinks the judge's mode effect by about 40–60% but does not remove it; for Qwen3-30B no thinking advantage — [V] (p. 9, p. 10).
12. Blinded explanation quality does not differ between correct and incorrect predictions (e.g. completeness 3.58 vs 3.61, all Mann–Whitney p > 0.3); an unblinded judge creates a spurious gap (3.51 vs 2.22) — [V] (p. 9, p. 10).

## 8. Limitations stated by the authors
- [A] Deterministic decoding (T = 0) and a single run per configuration: results limited to deterministic decoding, no repeated-run variability (p. 11).
- [A] Prompt sensitivity and agent-design choices; configurations are representative, not task-optimal (p. 11).
- [A] Metrics may not fully capture the constructs; the rubric measures developer-facing quality, not faithfulness; a single external Claude judge may have stylistic and length preferences (p. 11).
- [A] Function-level PrimeVul Pair only; no project context, interprocedural reasoning or repository-level vulnerabilities; only four open Nemotron/Qwen models, larger models (DeepSeek-V3.1, Kimi-K2) not run due to hardware budget (p. 3, p. 11).
- [A] RQ3 manual evaluation uses a sample, which adds sampling uncertainty (p. 11).
- [A] The call-matched results are single runs and reported descriptively (p. 11).

## 9. Limitations we identified
- [I] An "always vulnerable" classifier scores F1 = 0.667 on this balanced set (precision 0.5, recall 1.0). No reported configuration exceeds it (Table 3 max 0.665, Table 9 max 0.666), so DA's "highest F1" is near the trivial flag-everything point. Based on Table 3 (p. 7) and Table 9 (p. 11).
- [I] All P-C values are ≤26.9%, i.e. at or below the 25% that a random guesser labelling each pair member independently can reach at most (q(1−q) ≤ 0.25 for flag rate q); only self-revision slightly exceeds it (25.9–26.9%, Table 9). DA is far below that ceiling: 0.7–18.8% per setting, mean 6.2% (Table 3, p. 7), and 0.5–13.0% in Table 9 (p. 11). Absolute discrimination is therefore weak in every design. Based on Tables 2, 3, 4 and 9 (p. 6, p. 7, p. 11).
- [I] No SAST or deep-learning baselines, so the paper says nothing about LLMs vs traditional tools. Based on Table 1 (p. 3).
- [I] Training-data contamination is not discussed; PrimeVul is public and the open models may have seen it. Based on a search of the full text for contamination or memorisation (none found).
- [I] Statistical tests on 8 or 16 paired configuration-level means have little power and no correction across RQ1/RQ2 tests; differences between individual cells should not be over-read (the authors say this too, p. 6).
- [I] Wording conflict: the abstract and conclusion say explanation gains are "largely" length-mediated (p. 11), while Section 4.3 says "substantially but not wholly" (40–60%) (p. 9).
- [I] Selection of the 193-pair subset and the handling of non-conforming outputs are not described, which limits checks on Table 9. Based on p. 5, p. 11.

## 10. Threats to validity
- Internal (confounds, leakage, selection): agent designs differ in number of calls and context, partly controlled by call-matched baselines (p. 7, p. 11); possible pretraining contamination not addressed; parsing rule for non-conforming outputs unspecified (p. 5).
- External (generalisability of sample/context): function-level C/C++, one benchmark, four mid-size open models (p. 11).
- Construct (do metrics measure the concept?): F1 on balanced data rewards over-flagging (authors pair it with P-C, p. 7); explanation rubric measures perceived quality, not faithfulness (p. 11).
- Statistical conclusion (power, multiple comparisons, variance): single runs; small numbers of paired configuration means; Bonferroni applied only in RQ3 (p. 8, p. 9).
- Reproducibility (data/code/setup reported?): good — open models, vLLM versions, hardware, prompts and replication package on Zenodo (p. 4, p. 12).

## 11. Future research directions
- Stated by authors [A]: more reasoning-oriented families (distilled DeepSeek-R1, Gemma) and larger models; costlier repository-level settings with dependency resolution, retrieval and tool support (p. 11); deeper per-model analysis and significance testing of the reasoning × orchestration interaction (p. 8).
- Suggested by us [I]: report the trivial flag-all and random baselines alongside F1/P-C; add SAST and fine-tuned DL baselines on the same pairs; repeat runs with non-zero temperature for variance.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (LLM-only variants), RQ2, RQ3, RQ5.
- How it informs our work [I]: controlled evidence that reasoning modes and multi-agent designs mainly shift the recall/false-positive trade-off rather than improving discrimination, with detailed energy, token and USD costs. Useful for RQ3 (cost vs benefit of agentic LLM designs) and RQ2 (F1 vs pairwise metrics), and consistent with yildiz2025benchmarking's finding that F1 hides near-random pairwise accuracy. No traditional or DL baseline, so it does not inform LLM-vs-SAST directly.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Thinking mode raises non-agent mean F1 from 0.31 to 0.41 across 4 open models (Wilcoxon p = 0.023, d = 1.37), mainly via recall; accuracy unchanged (0.518 vs 0.523) | p. 6 | V | moderate |
| RQ1 | Best function-level F1 on PrimeVul Pair is 0.620 (Nemotron-Super-49B thinking) and best non-agent P-C 22.5%, i.e. weak discrimination of vulnerable vs patched functions | p. 6 | V | moderate |
| RQ2 | Dual-agent design reaches the highest F1 (0.634) by flagging 88.2% of functions (FPR 0.880) and has the worst pairwise accuracy (P-C 6.2) | p. 7 | V | moderate |
| RQ2 | F1 on balanced data and pairwise correctness rank designs differently: MA best on P-C in 11/16 settings, DA in 0/16 despite best F1 | p. 7, p. 8 | V | moderate |
| RQ3 | Four-call self-revision matches or beats the multi-agent pipeline on P-C (24.7 vs 21.9) on 193 pairs: much of the agent gain is extra inference budget | p. 11 | V | weak |
| RQ3 | Thinking uses 2.7–4.4× more energy and 2.5–3.6× more output tokens; MA-thinking uses ~25.5K tokens per function; per-configuration cost SA $27.5, DA $37.1, MA $52.7 | p. 10 | V | moderate |
| RQ3 | Thinking's F1 benefit turns negative under DA (−0.054) and MA (−0.066) | p. 8 | V | weak |
| RQ5 | Blinded explanation quality is indistinguishable between correct and incorrect predictions (all p > 0.3); fluent explanations do not signal correctness | p. 9 | V | moderate |
| RQ5 | Authors call for repository-level evaluation with dependency resolution, retrieval and tools | p. 11 | A | weak |

## 14. Key quotes
> "thinking improves mean F1 from 0.31 to 0.41 (Wilcoxon p = 0.023, Cohen's d = 1.37)" (p. 6)

> "DA flags 88.2% of functions (PPR = 0.882, FPR = 0.880)" (p. 7)

> "much of the apparent collaboration benefit reflects additional inference budget rather than multi-agent structure itself" (p. 11)

> "the explanation does not reveal its own incorrectness" (p. 9)

## Analyst notes
- Source: publisher version of record (ACM, ASE 2026; Creative Commons Attribution 4.0 licence; DOI printed on p. 1), supplied by the user and attached with `rlab attach`; identity check "match (DOI printed in PDF)". This replaces the earlier abstract-only analysis.
- Reading coverage: all 13 PDF pages read (pp. 1–11 body, pp. 12–13 acknowledgements, data availability, references). Figures 1–4 (heatmaps and bar charts) are images; their values were taken from Tables 2–9 and the text.
- Uncertainties: the 𝑝 symbol in quotes is rendered as "p" (extraction shows "𝑝"); quote 3 is joined across a hyphenated line break ("col-laboration"). Table 8 prints "36.4,kWh" (typo) (p. 10). Funding: EU Horizon Europe and Research Council of Norway (p. 12); no conflicts of interest declared. Claude Sonnet 4.6 as judge is from a different family from the evaluated models (p. 5).
