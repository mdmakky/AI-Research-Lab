---
key: deininger2026open
status: complete
evidence_basis: full-text
design: empirical benchmark; zero-shot prompting of 8 LLMs (3 frontier, 5 open-weight) vs 3 SAST tools and 2 CodeBERT detectors on identical functions; cost/energy measured or estimated
dataset: PrimeVul test split (C/C++; 24,788 functions, 549 vulnerable, 1:44); stratified sample of all 549 vulnerable + 1000 safe functions
sample_size: 1549 functions (549 vulnerable, 35.4%); 8 LLMs x several configurations; 3 prompts; 3 safe-pool draws
metrics: balanced accuracy (primary), MCC, F1, recall, specificity, precision at 1:44 prevalence, FP/TP, USD/task, J/task, USD and kJ per true positive, latency
main_finding: Open LLMs dominate frontier on cost/energy; fine-tuned CodeBERT beats all LLMs (BA 0.765 vs ≤0.711); LLM precision at 1:44 prevalence 2.3–4.6% across two epochs.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Open or Frontier? A Cost- and Energy-Aware Benchmark of Large Language Models for Software Vulnerability Detection

- Authors: Deininger, Patrick; Slany, Wolfgang
- Year / venue: 2026, Computers (published)
- DOI: 10.3390/computers15090623 · URL: https://doi.org/10.3390/computers15090623
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] To benchmark open-weight against frontier LLMs on function-level vulnerability detection, treating monetary cost and energy as "first-class axes alongside detection quality" (p. 1). The study also calibrates the LLM results against non-LLM reference points (static analysers and learned detectors) "to gauge absolute difficulty" (p. 2). [A] The authors claim the conjunction is new (a security task, a five-model open roster, and cost and energy as per-task axes), stating "We make no claim to be first on any single one of these axes" (p. 3).

## 2. Research questions / hypotheses
- [V] No numbered RQs. Contributions are framed as (p. 2):
  - a cost- and energy-aware open-vs-frontier benchmark on label-clean PrimeVul with non-LLM reference points;
  - evidence on the quality–efficiency Pareto frontier;
  - an account of what can and cannot be measured for closed API models.
- [I] Implicit questions:
  1. Are open-weight LLMs competitive with frontier LLMs in quality?
  2. Are they more cost- and energy-efficient?
  3. How do LLMs compare with SAST and fine-tuned detectors at realistic prevalence?

## 3. Methodology
- Research design: [V] Empirical benchmark of binary function-level detection ("does this C/C++ function contain a vulnerability?") on a fixed stratified PrimeVul sample (p. 4). Additional analyses (pp. 9–20):
  - re-scoring at the natural 1:44 prevalence;
  - configuration-matched families A/B/C;
  - prompt, sample-draw and run-to-run robustness;
  - a reasoning-vs-direct replication across two measurement epochs.
- Approach / model / intervention: [V] Eight LLMs prompted zero-shot through a unified OpenAI-compatible API gateway (p. 4, Table 2). [V] The gateway is **not named** (pp. 4, 29).
  - **Frontier:** Claude Sonnet 5, GPT-5.1, Gemini 3.1 Pro (`gemini-3.1-pro-preview`); active parameters assumed ~100B for the energy estimate.
  - **Open-weight:** DeepSeek-V3.2 (~37B active), GLM-5 (~32B active), Llama-3.3-70B, Qwen3-Coder-30B (3B active MoE), Gemma-3-4B.
  - [V] Pinned providers and precision: DeepSeek-V3.2 and GLM-5 at GMICloud FP8; Llama-3.3-70B at DeepInfra FP8; Qwen3-Coder-30B at SiliconFlow FP8; Gemma-3-4B at DeepInfra bf16 (p. 29, Table A2).
  - [V] Main configuration: direct answer, reasoning disabled where permitted. Gemini cannot disable reasoning (HTTP 400) (p. 4, p. 29).
  - [V] Prompt: a security-reviewer persona; answer YES/NO first, then an optional explanation (p. 28). A lenient parser counts unparseable outputs as parse failures, not "safe" (p. 4, p. 29).
- Baselines or comparison conditions:
  - [V] **Trivial baselines:** always-safe and always-vulnerable (p. 7, Table 4); always-flag at 1:44 prevalence (p. 8, Table 5).
  - [V] **SAST arm** (p. 6, p. 10, Table 7): Flawfinder 2.0.20 (lexical), Cppcheck 2.21 (flow-sensitive), Semgrep 1.175 with community C and security-audit rulesets (pattern plus intraprocedural taint). A function is flagged if any finding reaches a swept severity threshold.
  - [V] **DL arm:**
    - CodeBERT fine-tuned on Devign (off the shelf, cross-dataset, argmax, 512 tokens) (p. 6);
    - CodeBERT (125M) fine-tuned on PrimeVul's training split, with the threshold selected on the validation split (p. 10–11).
  - [V] **CodeQL was not run.** PrimeVul functions are isolated snippets with no build, so no CodeQL database can be built (p. 10–11).

## 4. Dataset and sample
- Data source(s): [V] PrimeVul test split (C/C++): 24,788 functions after loading, 549 vulnerable — "a realistic 1:44 class ratio" (p. 4).
  - [I] This differs from the PrimeVul test split recorded in ding2025vulnerability (695 vulnerable / 25,216 benign) [@ding2025vulnerability, p. 6]. The paper does not explain the difference beyond "after loading" (p. 4); filtering or de-duplication on load is plausible but not reported.
- Sample size (N) and unit: [V] N = 1549 functions: all 549 vulnerable plus 1000 seeded-random safe functions (p. 4). [I] Prevalence in the evaluated sample is 35.4% (549/1549). This is **not** 50/50, although the text once calls it "balanced by construction" (p. 8). [V] The effective N per model is 1526–1549 because parse failures are excluded (p. 6).
- Sampling / selection method:
  - [V] Label-stratified sample fixed by seed (p. 4).
  - [V] Two further near-disjoint safe pools (<6% overlap) were drawn for robustness (p. 19).
  - [V] LLM inputs were truncated to 8000 characters. This affects 105/1549 functions and 87/549 (15.8%) of the vulnerable ones (p. 4).
  - [A] "The two non-LLM baselines" see the untruncated function and are therefore "if anything, advantaged" on long inputs (p. 4). [V] But the CodeBERT-Devign baseline uses "inputs truncated to 512 tokens" (p. 6); the input length of CodeBERT-PrimeVul is not reported (pp. 10–11).
  - [I] The untruncated claim can hold only for the SAST tools. CodeBERT's 512-token window is shorter than the LLMs' 8000-character budget, so on long functions CodeBERT is, if anything, disadvantaged — which strengthens rather than weakens its win over the LLMs (basis: p. 4, p. 6; CodeBERT-PrimeVul's limit inferred from the architecture, not reported).
  - [V] All CVEs date from 2008–2022 and predate the models' training cutoffs (p. 24). [V] The PrimeVul training split contains no evaluated function or function body (up to whitespace) (p. 10, p. 25).
- Data availability (public? link?): [V] Released on Zenodo (doi 10.5281/zenodo.21391073): harness, configurations, sampled function IDs, price snapshot, energy sweep, baseline scores and aggregated results (p. 26). [V] PrimeVul is fetched from its original authors by script; the fine-tuned checkpoint is regenerable by script (p. 26).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Harness and decoding: a test-driven harness with 82 automated tests; temperature 0, seed 12345, one generation per item; output budget 64 tokens in the matched configuration (256 for two frontier models in the first epoch) (p. 6, p. 29).
  - [V] Cost: computed from logged input/output tokens × list price at a pinned provider, with gateway fallbacks disabled (p. 5).
  - [V] Provider price dispersion: up to 14.4× for DeepSeek-V3.2 (USD 0.209–3.000 per million input tokens) (p. 5, Table 3).
  - [V] Energy (p. 5):
    - FLOP estimate E ≈ 2·N_active·T·ε for API-served models;
    - measured with the NVML energy counter on a dedicated NVIDIA H200 for locally servable open models (concurrency 1, idle-subtracted "active" energy);
    - plus a concurrency sweep c = 1/8/32/64 (p. 14, Table 9).
  - [V] Latency: client-side under concurrency 10, so it conflates queueing (p. 30).
  - [V] Statistics: stratified paired bootstrap of balanced-accuracy differences (20,000 resamples, seed 12,345) with Holm correction over a 9-comparison primary family and a 15-comparison strict family (p. 6, p. 28).
- Code availability: [V] The harness and configurations are released (p. 6, p. 26).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] **Balanced accuracy** is the primary metric, because accuracy is dominated by the always-safe classifier (0.646 accuracy, above every LLM) and both trivial classifiers score exactly 0.5 on it (p. 6).
  - [V] MCC and F1 are also reported (p. 6).
  - [V] Deployment metrics at 1:44 prevalence are derived from the prevalence-invariant TPR/FPR (p. 8, Table 5):
    - precision; false positives per true positive (FP/TP);
    - alerts and found vulnerabilities per 1000 functions;
    - **USD per true positive** and **kJ per true positive**.
  - [V] Elicited 0–100 confidence gives ROC-AUC where usable. VD-Score is declined because the coarse score grids cannot reach its 0.5% FPR point (p. 9–10).
- Statistical testing (tests used, significance, effect sizes, confidence intervals):
  - [V] Paired bootstrap 95% CIs and Holm-adjusted p for open-vs-frontier gaps (p. 27, Table A1).
  - [V] Wilson-based 95% CIs on precision at deployment prevalence for the non-LLM baselines (p. 10, Table 7).
  - [V] Robustness: Spearman rank correlation across prompts and draws (p. 19, Table 13).
  - [V] Output-budget effects are tested with a paired bootstrap (p. 16, Table 10).

## 7. Key findings
1. **Detection quality, first epoch** — [V] Balanced accuracy / F1 per model, direct mode, N = 1549 (p. 7, Table 4). [V] F1 range across LLMs is 0.405–0.615 vs always-vulnerable F1 0.523 (p. 7, Table 4).

   | Model | Bal. acc. (95% CI) | F1 |
   |---|---|---|
   | DeepSeek-V3.2 | 0.676 (0.654–0.697) | 0.615 |
   | Gemma-3-4B | 0.653 | 0.590 |
   | GLM-5 | 0.637 | 0.596 |
   | Gemini-3.1-Pro | 0.623 | 0.591 |
   | GPT-5.1 | 0.617 | 0.560 |
   | Claude-Sonnet-5 | 0.616 | 0.582 |
   | Llama-3.3-70B | 0.604 | 0.578 |
   | Qwen3-Coder-30B | 0.511 | 0.405 |

2. **Open vs frontier significance** — [V] DeepSeek-V3.2 significantly beats all three frontier models: +0.054 to +0.060 balanced accuracy, Holm p < 5×10⁻⁴ (p. 6, p. 27, Table A1).
   - [V] Gemma-3-4B beats Claude-Sonnet-5 (+0.037, Holm p = 0.032); the other top-open gaps are not significant (p. 7, p. 27).
   - [V] Qwen3-Coder-30B is indistinguishable from chance (MCC 0.022, CI −0.03 to 0.07) (p. 7).
3. **Budget-matched second epoch (Family A)** — [V] Balanced accuracy / MCC: DeepSeek-V3.2 0.711 / 0.403; GLM-5 0.669 / 0.352; Gemma-3-4B 0.653 / 0.297; Claude-Sonnet-5 0.653 / 0.321; GPT-5.1 0.615 / 0.225; Llama 0.609 / 0.267; Qwen 0.568 / 0.136; Gemini 0.606 / 0.252, on only the 54.2% of tasks it answered (p. 17, Table 11).
   - [V] Claude equals Gemma (+0.0003, p = 0.98) (p. 17).
   - [V] Absolute numbers shifted by up to 0.06 between epochs seven weeks apart ("service drift") (p. 7–8, p. 20).
4. **Reasoning mode** — [V] Reasoning helps every frontier model (Claude +0.032, GPT-5.1 +0.044, Gemini +0.096) but hurts DeepSeek-V3.2 (−0.133, p < 10⁻⁴) and does not help GLM-5 (−0.019, n.s.); it costs 4.5–12.1× more per task (p. 17–18, Table 12).
   - [V] Best observed: DeepSeek 0.711 (direct) vs Claude 0.685 and Gemini 0.680 (reasoning); DeepSeek vs Claude p = 0.081 (p. 17).
   - [V] Reasoning lowers DeepSeek's specificity from 0.52 to 0.37 (p. 20).
5. **Prompt sensitivity dominates** — [V] Two paraphrases move balanced accuracy by up to 0.088 and produce three different winners (DeepSeek 0.711, Claude 0.741, GLM-5 0.700); Spearman ρ vs anchor = 0.381 and 0.810 (p. 19–20, Table 13).
   - [V] Safe-pool redraws move scores ≤0.015 (ρ = 1.000) (p. 19).
   - [V] Temperature-0 verdict agreement is 88.3–100%; only Gemma is exactly reproducible (p. 19).
6. **SAST baselines on the same functions** (p. 7, p. 10, Table 4, Table 7) — balanced accuracy / recall / specificity / precision at 1:44:
   - [V] Flawfinder risk≥1: 0.589 / 0.271 / 0.907 / 6.20%; risk≥4: 0.523 / 0.055 / 0.992 / 13.40%.
   - [V] Cppcheck: 0.548–0.592 balanced accuracy; precision 2.46–3.77%.
   - [V] Semgrep severity≥INFO: 0.514 / 0.031 / 0.998 / 25.96% (CI 5.7–66.9%). It flags 19 of 1549 functions with 17 TP and 2 FP (p. 11).
   - [V] Flawfinder is "ahead of every LLM at every threshold" on deployment precision but finds almost nothing (p. 9, p. 23).
7. **Fine-tuned DL baseline beats every LLM** — [V] CodeBERT-PrimeVul (125M, validation-tuned threshold) reaches balanced accuracy 0.765, MCC 0.526, recall 0.709, specificity 0.821, precision 8.23% at 1:44 (CI 6.9–9.7) and ROC-AUC 0.845 (p. 10, Table 7; p. 10–11). [V] CodeBERT-Devign (cross-dataset) collapses to 0.518, flagging 97% of functions (p. 7, p. 23). [V] At argmax 0.5 the PrimeVul detector predicts all-safe because no score exceeds 0.372. The authors "nearly reported" this artefact as evidence that trained detectors are no better than LLMs (p. 11).
8. **Deployment at 1:44 prevalence** — [V] First epoch: every LLM's precision is 2.3–3.8% vs 2.21% for always-flag; FP/TP ranges from 25.6 (DeepSeek) to 41.9 (Qwen); models alert on 43–75% of functions (p. 8, Table 5). [V] Budget-matched second epoch (Family A): LLM precision 2.8–4.6% (DeepSeek 4.62% highest; Gemini's 2.84% is on the 54.2% of tasks it answered) (p. 17, Table 11). [A] "Neither is ready for independent use" (p. 9).
9. **Cost per task** — [V] USD/task, first epoch (p. 7, Table 4); SAST and CodeBERT-Devign cost ≈0:

   | Model | USD/task |
   |---|---|
   | DeepSeek-V3.2 | 0.00017 |
   | Gemma-3-4B | 0.00004 |
   | GLM-5 | 0.00048 |
   | Gemini-3.1-Pro | 0.00448 |
   | GPT-5.1 | 0.00139 |
   | Claude-Sonnet-5 | 0.00441 |
   | Llama-3.3-70B | 0.00008 |
   | Qwen3-Coder-30B | 0.00006 |

   - [V] Family A cost (p. 17, Table 11): DeepSeek 0.00015, Claude 0.00265, Gemini 0.00219 USD/task.
   - [V] Gemma matches Claude's Family A quality at 1/66 of the cost; DeepSeek beats Claude at 1/18 (p. 17).
10. **Energy per task** — [V] J/task (p. 7, Table 4); frontier values are FLOP estimates at an assumed 100B active parameters, with the 25–400B sweep in brackets:

    | Model | J/task | Source |
    |---|---|---|
    | DeepSeek-V3.2 | 526 | estimated |
    | Gemma-3-4B | 64 | estimated |
    | GLM-5 | 424 | estimated |
    | Gemini-3.1-Pro | 1966 [492–7865] | estimated |
    | GPT-5.1 | 1332 [333–5329] | estimated |
    | Claude-Sonnet-5 | 2489 [622–9955] | estimated |
    | Llama-3.3-70B | 738 | measured |
    | Qwen3-Coder-30B | 88 | measured |

    - [V] Concurrency sweep on an H200 (c = 1 → 64), J/task: Gemma 84.4 → 3.8; Qwen 84.0 → 7.5; Llama 739.9 → 74.2. The FLOP estimator overstates batched energy by 5.4–16.9× (p. 14, Table 9).
    - [A] API-served energies are "most likely" overstated by about an order of magnitude (p. 14).
11. **Cost and energy per detected vulnerability (G6)** — [V] At 1:44 prevalence (p. 8, Table 5):

    | Model | USD per TP | kJ per TP |
    |---|---|---|
    | Gemma-3-4B | 0.003 | 3.7 |
    | Llama-3.3-70B | 0.004 | 44.8 |
    | Qwen3-Coder-30B | 0.006 | 4.0 |
    | DeepSeek-V3.2 | 0.009 | 28.4 |
    | GLM-5 | 0.023 | 20.3 |
    | GPT-5.1 | 0.082 | 78.3 |
    | Gemini-3.1-Pro | 0.210 | 92.4 |
    | Claude-Sonnet-5 | 0.212 | 119.6 |

    - [V] Flawfinder: ≈0 cost per TP (p. 8, Table 5).
    - [V] USD/TP is not reported for CodeBERT-PrimeVul ("negligible inference cost", p. 11) or for Cppcheck/Semgrep (pp. 8–11).
    - [V] **kJ/TP provenance is mixed.** The kJ/TP values for Qwen (4.0) and Llama (44.8) reproduce from the FLOP *estimates* of 40 J and 944 J (p. 14, Table 8), not from the *measured* 88 J and 738 J shown in Table 4 (p. 7), even though Table 5 says it inherits Table 4's provenance (p. 8). Gemma's 3.7 uses its 64 J estimate (p. 7).
    - [I] Our recalculation with measured concurrency-1 energy (J/task × 1000 / Found per 1000, Table 5 p. 8): Qwen ≈ 8.8 kJ/TP (88 J), Llama ≈ 34.9 kJ/TP (738 J), Gemma ≈ 4.9 kJ/TP (84.4 J, Table 9 p. 14). The ordering among the cheap open models changes (Gemma lowest), but the gap to frontier (78.3–119.6 kJ/TP, estimated) remains.
    - [I] **Human triage effort is not included**: these are compute costs per TP surfaced, with 25.6–41.9 false positives per TP (p. 8). The paper does not cost triage; it only remarks "No triage workflow absorbs that" (p. 8).
12. **Self-hosting economics** — [V] At concurrency 64 on one H200, self-hosting is cheaper than the API for Gemma and Qwen (0.15–0.36× API price) (p. 22, Table 14). For Llama-3.3-70B it is 0.63× on owned hardware but 1.50× on a rented card. These are GPU-time-only assumptions (USD 3.50/h rented; USD 1.46/h owned).
13. **Contamination gradient** — [V] Recall on pre-2020 CVEs is 7–15 points higher than on 2021–2022 CVEs for better-balanced models (e.g. GPT-5.1 0.88 vs 0.73; DeepSeek 0.90 vs 0.81) (p. 24). [A] This is "consistent with some memorization" (p. 24).
14. **Elicited confidence** — [V] Only Claude used the requested probability scale (ROC-AUC 0.814); three models reported verdict confidence instead (converted AUC 0.69–0.76); DeepSeek emitted −1 on 1409/1549 tasks; Gemini produced a parseable pair on 1.2% of tasks (p. 9, Table 6).
15. **Trivial-baseline comparison** — [I] Our reading of Table 4 (p. 7):
    - Sample (35.4% positive): best LLM F1 0.615 is only +0.092 above always-vulnerable F1 0.523; Qwen (0.405) is below it. The 0.667 balanced-data reference does not apply at this prevalence.
    - At 1:44 prevalence, our calculation from Table 5 TPR and precision (p. 8): always-flag F1 ≈ 0.043; best LLM (DeepSeek) F1 ≈ 0.072; CodeBERT-PrimeVul ≈ 0.147; Flawfinder risk≥1 ≈ 0.101. Flawfinder's F1 is above every LLM's at deployment prevalence.

## 8. Limitations stated by the authors
- [A] Energy is measured for only some open models; frontier energy rests on an untested active-parameter assumption and is reported as a sensitivity range (p. 23).
- [A] Configuration asymmetries: Gemini cannot run without reasoning; two frontier models needed larger output budgets in the main run (p. 24).
- [A] Latency is confounded by queueing (p. 24).
- [A] Training-data contamination: all CVEs are 2008–2022 and may appear in pre-training; a recall gradient by CVE year is "consistent with some memorization"; absolute scores "may be optimistic"; a post-cutoff restriction is planned (p. 24).
- [A] The fine-tuned CodeBERT-PrimeVul detector is in-distribution (trained on PrimeVul's own training split) while the LLMs are zero-shot; the authors call this "not an unfair comparison" but note the different prerequisites (several thousand labelled vulnerable functions vs none) (p. 11).
- [A] One prompt, one draw and one generation in the headline table; variation across datasets and task formulations remains unbounded (p. 24).
- [A] Serving-layer dependence (p. 24–25):
  - price spread up to 14×;
  - two silent serving faults: billed empty outputs, and a reasoning flag ignored with HTTP 200;
  - quality is robust to provider and precision for Llama (0.599–0.609).
- [A] CodeQL cannot be applied to unbuildable function snippets (p. 25).
- [A] Scope: one dataset, one task formulation, function level only; other languages and statement-level localisation are future work (p. 25).
- [A] "No result here should be read as evidence that function-level vulnerability triage is ready for independent use" (p. 26).

## 9. Limitations we identified
- [I] **Internal inconsistencies from revision** (the paper went through at least one major review round, p. 1, pp. 16–19):
  - Gemma-3-4B is said to be incompatible with the local vLLM/CUDA build, so its energy is FLOP-estimated (p. 6, p. 15). Yet Table 9 reports a measured concurrency sweep for Gemma (p. 14), and the abstract says three open models were measured (p. 1), while p. 5 says two.
  - The limitations list says a fine-tuned PrimeVul detector "is the remaining gap" (p. 25), but Section 4.4 reports exactly such a detector (p. 10–11).
  - The reasoning cost multiplier is "2.5 to 7.6 times" on p. 24, which refers to the earlier-epoch comparison of Section 4.9 (p. 20); Section 4.9 gives no cost table, so that range cannot be checked. Cite Table 12's 4.5–12.1× (p. 18) instead.
  - The sample is called "balanced by construction" (p. 8) although it is 35.4% positive (p. 4).
  - p. 2 says "every model we tested raises roughly twenty-six false alarms per true finding", but Table 5 gives 25.6–41.9 FP/TP; 25.6 is the best model only (p. 8). p. 21 attributes "roughly twenty-six" to "the best model".
  - p. 23 says the best open models "dominate the frontier on both the quality and the efficiency axes", whereas p. 21 says the data "do not support a general claim of quality dominance", and DeepSeek's lead over Claude in Family C is not significant (p = 0.081) (p. 17).
  - p. 4 speaks of "two non-LLM baselines (Section 3.4)", but Section 3.4 lists four non-LLM detectors (p. 6).
  - These are reporting slips, not evidence of wrong numbers, but readers should cite table values rather than prose.
- [I] **The SAST arm is weak by design for C/C++.** Flawfinder, Cppcheck and Semgrep community rules on isolated functions, with no CodeQL, Infer or commercial tools (p. 10–11). The comparison is LLM vs lightweight function-level SAST, not vs semantic whole-program SAST.
- [I] Contamination and the in-distribution vs zero-shot asymmetry are author-stated (§8, p. 11, p. 24). Our addition: both cut in different directions — contamination may inflate the LLM scores, while the asymmetry favours CodeBERT — so the size of CodeBERT's lead over zero-shot LLMs on genuinely unseen code is unknown.
- [I] **Cost per TP excludes triage.** With 25.6–41.9 FP per TP (p. 8), analyst time would dominate compute cost (cents per TP). The paper's USD/TP therefore understates the practical cost per confirmed vulnerability by a large factor.
- [I] **Unnamed gateway** and preview model identifiers (`gemini-3.1-pro-preview`, p. 29) limit long-term reproducibility. The service drift of up to 0.06 between epochs (p. 20) shows API results are time-stamped observations.
- [I] **Function-level, C/C++ only** — no repository context. The truncation at 8000 characters affects 15.8% of positives (p. 4).
- **AI-assisted writing and code.** [V] The authors used DeepL Translator and ChatGPT (GPT-5.5, OpenAI) "to translate words, phrases, and passages from German into English", and Claude (Opus 5 and Sonnet 5, Anthropic) "to assist with drafting and revising portions of the text and with writing Python code"; "no figures, data, or images were AI-generated or fabricated" (p. 27). [V] The harness is covered by 82 automated tests (p. 6).
  - [I] Both assisting vendors (OpenAI, Anthropic) also supply evaluated models (GPT-5.1, Claude-Sonnet-5; p. 4). The disclosure and the test suite reduce the concern; we note it for transparency, not as a conflict. Our own analysis pipeline is also Claude-based, which readers may wish to weigh when judging our reading of Claude results.

## 10. Threats to validity
- Internal (confounds, leakage, selection):
  - [V] Train/test separation for CodeBERT-PrimeVul is verified: no evaluated function or body is in training (p. 25).
  - [V] Thresholds are tuned on validation, not test (sweeping on test would give 0.777 vs the reported 0.765) (p. 11).
  - [V] Contamination is not controlled but is measured as a recall gradient by CVE year (p. 24).
  - [V] Epoch drift is handled by within-epoch comparisons (p. 16–18).
  - [V] Parse failures are excluded, not recoded (p. 27).
- External (generalisability of sample/context):
  - [V] One dataset (PrimeVul), C/C++, function level (p. 25).
  - [I] It is unclear whether results hold for repository-level detection or other languages.
  - [I] Model versions are a 2026 snapshot.
- Construct (do metrics measure the concept?):
  - [V] Balanced accuracy is chosen deliberately; the paper shows its ranking differs from the precision ranking at deployment prevalence (GPT-5.1 3rd on precision, 5th on balanced accuracy) (p. 8–9).
  - [I] PrimeVul labels are "near-human-accuracy" per its authors (p. 3), but no own label audit was done.
- Statistical conclusion (power, multiple comparisons, variance):
  - [V] Paired bootstrap with Holm correction; families are declared explicitly (p. 28).
  - [V] Prompt variance (≤0.088) exceeds most between-model gaps (p. 19–20). [A] "No single-prompt ranking of LLMs on this task should be read as a property of the models" (p. 20).
  - [V] Deployment precision CIs are reported for the non-LLM rows and the best/weakest LLM (p. 10, Table 7).
- Reproducibility (data/code/setup reported?):
  - [V] Strong: harness, configurations, prompts, parser rules, pinned providers and prices, function IDs and energy data are released (p. 26, pp. 28–30).
  - [V] API non-determinism remains: 0–12% of verdicts flip at temperature 0 (p. 19).
- Funding and conflicts of interest: [V] Funded in part by the State of Styria (Land Steiermark), PRISMA project, grant ABT12-270413/2024 (p. 26); open-access publication supported by the TU Graz Open Access Publishing Fund; the authors declare no conflicts of interest (p. 27).

## 11. Future research directions
- Stated by authors [A]:
  - calibrate the FLOP energy estimator against measured batched energy, per architecture (p. 26);
  - corroborate on a second dataset and task formulation (p. 26);
  - post-cutoff CVEs or paired PrimeVul variants to bound memorisation (p. 24);
  - controlled single-request latency (p. 24);
  - other languages, statement-level localisation, and VD-Score at realistic imbalance (p. 25).
- Suggested by us [I]:
  - Add triage time per alert to turn USD/TP into cost per confirmed vulnerability (G6).
  - Run a semantic SAST arm at repository level, where builds exist.
  - Repeat with post-cutoff functions so that the fine-tuned vs zero-shot comparison is contamination-free (G2).

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1 (primary: LLM vs SAST vs fine-tuned DL on identical functions), RQ2, RQ3 (cost/energy trade-offs; no hybrid), RQ5.
- How it informs our work [I]:
  - **RQ1:** one of very few same-benchmark three-family comparisons. The ranking depends on the metric:
    - on balanced accuracy: fine-tuned CodeBERT > best LLMs > Flawfinder/Cppcheck > Semgrep;
    - on precision at realistic prevalence: Semgrep (26.0%, 95% CI 5.7–66.9) and strict-threshold Flawfinder (13.4%) > CodeBERT (8.2%, CI 6.9–9.7) > lenient Flawfinder (6.2%) > all LLMs (2.3–3.8% first epoch, p. 8; 2.8–4.6% budget-matched, p. 17). Cppcheck (2.46–3.77%) sits in the LLM range (p. 10, Table 7). Only Flawfinder and Semgrep beat every LLM on precision, and the Semgrep and Flawfinder intervals overlap CodeBERT's, so their ordering against CodeBERT is not established (p. 10, Table 7);
    - all are far from deployable.
  - This fits our "LLMs higher recall, lower precision" pattern and C3/C5.
  - **Correction for our gap report.** The G2 and G6 novelty-check notes describe *Open or Frontier?* as "No SAST". That is **incorrect**: Flawfinder 2.0.20, Cppcheck 2.21 and Semgrep 1.175 are run on the identical 1549 functions (p. 6, p. 10). G2 is therefore narrowed further: a same-benchmark LLM + SAST + fine-tuned DL comparison now exists at function level on C/C++. What is still missing is post-cutoff code, repository level, and semantic SAST.
  - **G6 is narrowed further.** USD/TP and kJ/TP at 1:44 prevalence are reported for 8 LLMs (p. 8). The remaining gap is the triage-effort term and a costed SAST/DL arm (≈0 is not quantified per TP).
  - **G1:** a further study that reports trivial baselines and realistic-prevalence re-scoring. It shows LLM precision barely above always-flag (2.3–3.8% first epoch, 2.8–4.6% budget-matched, vs 2.21%; p. 8, p. 17).
  - **C1:** the argmax-collapse artefact (p. 11) suggests some reports of fine-tuned models being near chance on PrimeVul may reflect decision thresholds rather than ranking ability. This is a candidate explanation, not established for other papers.
  - **C4:** reasoning raises frontier balanced accuracy but lowers DeepSeek's specificity (more false positives) (p. 17, p. 20). This supports the "model-dependent" reading.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | On 1549 PrimeVul C/C++ functions (35.4% vulnerable), zero-shot LLM balanced accuracy 0.511–0.676 (first epoch) and 0.568–0.711 (budget-matched epoch); best DeepSeek-V3.2 | 7, 17 | V | moderate (single dataset, prompt-sensitive) |
| RQ1 | Fine-tuned CodeBERT-PrimeVul (125M, validation-tuned threshold) beats every LLM: bal. acc. 0.765, MCC 0.526, precision at 1:44 8.23% vs best LLM 0.711 / 0.403 / 4.62% (budget-matched epoch) | 10, 11, 17 | V | moderate (in-distribution vs zero-shot) |
| RQ1 | Same functions, SAST: Flawfinder bal. acc. 0.589 (risk≥1), Cppcheck 0.548–0.592, Semgrep 0.501–0.514 (recall 0.002–0.031). At 1:44 only Flawfinder (6.2–13.4%) and Semgrep (26.0% [5.7–66.9]) are more precise than every LLM (2.3–3.8% first epoch; 2.8–4.6% budget-matched); Cppcheck (2.46–3.77%) is in the LLM range; Semgrep's CI overlaps CodeBERT's (8.23% [6.9–9.7]) | 7, 8, 10, 11, 17 | V | moderate (lightweight SAST only; no CodeQL; Semgrep precision rests on 2 FP) |
| RQ1 | Trivial baselines: always-vulnerable F1 0.523 vs LLM F1 0.405–0.615; at 1:44 every LLM's precision 2.3–3.8% (first epoch; 2.8–4.6% budget-matched) vs always-flag 2.21%, 25.6–41.9 FP per TP (first epoch) | 7, 8, 17 | V | moderate |
| RQ2 | Prompt paraphrase moves bal. acc. up to 0.088 and changes the winner (ρ vs anchor 0.381); safe-pool redraw ≤0.015; temperature-0 verdict agreement 88.3–100% | 19, 20 | V | moderate |
| RQ2 | Recall on pre-2020 CVEs 7–15 points higher than 2021–2022 for better-balanced LLMs (memorisation signal) | 24 | V | weak–moderate (no significance test reported) |
| RQ2 | Argmax decision rule made the fine-tuned detector look like always-safe (bal. acc. 0.500) despite ROC-AUC 0.845; threshold choice can flip LLM-vs-DL conclusions | 11 | V | moderate |
| RQ3 | Cost per task: open USD 0.00004–0.00048 vs frontier 0.00139–0.00448; Gemma-3-4B matches Claude-Sonnet-5 quality at 1/66 cost; reasoning costs 4.5–12.1× more | 7, 17, 18 | V | moderate (list prices, provider-dependent up to 14×) |
| RQ3 | Cost and energy per true positive at 1:44: USD 0.003 (Gemma) to 0.212 (Claude); 3.7 to 119.6 kJ as reported, with Gemma, Qwen and Llama kJ/TP computed from FLOP estimates (64, 40, 944 J), not measured energy; human triage of 25.6–41.9 FP per TP not costed | 7, 8, 14 | V | moderate (compute only; mixed energy provenance) |
| RQ3 | Re-computed with measured concurrency-1 energy, kJ/TP ≈ 4.9 (Gemma), 8.8 (Qwen), 34.9 (Llama), still far below frontier 78.3–119.6 (estimated) | 8, 14 | I | moderate (our calculation from Table 5 Found and Tables 8–9) |
| RQ3 | Energy per task: measured 88 J (Qwen3-Coder-30B) and 738 J (Llama-3.3-70B); frontier FLOP-estimated 1332–2489 J (range 333–9955); batching cuts measured energy 10–22× | 7, 14 | V | weak–moderate (frontier estimated) |
| RQ5 | Authors: no method tested (LLM, SAST, fine-tuned DL) is ready for independent function-level triage | 26 | A | moderate |

## 14. Key quotes
> "at the natural 1:44 prevalence, precision is 2.3–8.2%" (p. 1)

> "The LLMs flag nearly everything and are almost never right; the static analyzer flags almost nothing and is right somewhat more often." (p. 9)

> "Three reasonable phrasings of the same question produce three different winners." (p. 20)

> "No single-prompt ranking of LLMs on this task should be read as a property of the models; it is a property of the pair (model, prompt)." (p. 20)

## Analyst notes
- Reading coverage: All 32 pages read from `fulltext.txt`, including appendices A–B and references. Figures 1–3 (pp. 12–13) are plots whose values are also given in Tables 4 and 9 and in the text; they were not re-read from the PDF.
- Uncertainties:
  - Revision inconsistencies about which models had energy measured (see §9). Table values were used where prose and tables disagree.
  - Which figures are "first epoch" and which are "second epoch" matters. Table 4/5 cost and energy are first epoch (p. 8); Family A quality (Table 11) is second epoch.
  - The F1 values at 1:44 prevalence are our calculation from reported TPR and precision, not reported by the paper.
  - The gap-report G2/G6 entries need correcting: this paper does include SAST baselines.
