---
key: spracklen2026llm
status: complete
evidence_basis: full-text
design: Technique proposal + controlled experiment (adaptive unlearning vs gradient ascent, NPO, PMC) with loss, inner-epoch and mutation ablations
dataset: 20 hallucination-eliciting Python prompts from the Spracklen et al. benchmark (training) + 40 ChatGPT-paraphrased variants (test); static PyPI snapshot; EvalPlus
sample_size: 2 DeepSeek-Coder models (7B dense, 16B MoE); 20 training prompts; 40 test prompts; samples/identifiers per prompt not reported; single runs
metrics: Hallucination rate over Mode 1 (required) + Mode 2 (useful) package queries; KL divergence from base on code, instruction and package prompts; EvalPlus pass@1 (HumanEval(+), MBPP(+))
main_finding: Full-parameter adaptive unlearning cut package hallucination 21.23%→2.56% (7B) and 27.75%→6.13% (16B) on paraphrased held-out prompts; coding average +1.6 / −4.2 pp.
relevance: medium
analysed: 2026-11-12
---

# LLM Ghostbusters: Surgical Package Hallucination Suppression via Adaptive Unlearning

- Authors: Spracklen, Joseph; Aghazadeh, Pedram; Koushanfar, Farinaz; Jadliwala, Murtuza
- Year / venue: 2026, arXiv (preprint)
- DOI: 10.48550/arxiv.2605.01047 · URL: https://arxiv.org/abs/2605.01047
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified · **[A]** author claim · **[I]** our interpretation.

Source tier: preprint (arXiv v2, cs.CR, Sep 2026), **not peer-reviewed** (p. 1). It refers to the USENIX Open Science policy (p. 17). Authors overlap with spracklen2024we (Spracklen, Jadliwala). The paper discloses use of an AI writing and coding aid (p. 13).

## 1. Research objective
- [A] A post-deployment framework, Adaptive Unlearning (AU), that "surgically" suppresses package hallucinations while preserving general utility. It uses only model-generated data and no human annotation (p. 1–2).
- [A] Target properties: precision, generalisation, data efficiency and scalability (p. 2).

## 2. Research questions / hypotheses
- [V] No formal RQs. The implicit claims are:
  - AU beats gradient ascent (GA), NPO and PMC on the joint hallucination–utility–drift trade-off.
  - The hybrid loss, inner epochs and prompt mutation are each necessary (p. 3, p. 9–12).

## 3. Methodology
- Research design: [V] Technique proposal with controlled comparison against unlearning baselines, plus ablations (p. 8–12).
- Approach / model / intervention:
  - [V] **Closed loop:** sample completions; detect hallucinations with a registry oracle; build a per-token mask with three values (p. 5–7):
    - 0 = context tokens, anchored by a scaled CE term.
    - 1 = valid package names, reinforced with CE.
    - 2 = hallucinated names, suppressed with NPO against a frozen base model.
  - [V] **Nested epochs:** outer epochs resample completions; inner epochs train on the cached samples (p. 5–7).
  - [V] **Prompt mutation:** a prompt is "exhausted" when N samples contain no hallucination or after 5 outer epochs. The model then rewrites the original seed prompt (p. 5–7).
  - [V] **Required access:** **full-parameter fine-tuning** of the weights, explicitly not LoRA (p. 8, p. 19). NPO needs logits and a frozen reference copy (p. 5). The registry oracle is needed during training only, not at inference (p. 12).
- Baselines or comparison conditions: [V] Base, Gradient Ascent, NPO, PMC. Ablations: CE-only, NPO-only, inner-epoch sweep, mutation-count sweep (p. 8). All methods share the same generation, parsing and detection pipeline (p. 8).

## 4. Dataset and sample
- Data source(s):
  - [V] 20 code-generation prompts from the Spracklen et al. benchmark. Each was chosen so the base model's completion contains at least one valid and one hallucinated package, with diverse topics. They were deliberately hallucination-heavy, hence the high base rates (p. 8). The prompts are listed in Appendix F (p. 19–20).
  - [V] Utility is measured on EvalPlus (HumanEval, HumanEval+, MBPP, MBPP+) (p. 9).
- Sample size (N) and unit:
  - [V] The test set is 40 prompts: 2 ChatGPT-generated variants of each training prompt, held out from training (p. 8).
  - Not reported: samples per test prompt, total identifiers (N_total), and the size and source of the KL prompt sets.
- Sampling / selection method: [V] Prompts were selected for being hallucination-eliciting (p. 8).
- Data availability (public? link?): [V] An anonymous repository with code, prompts, harnesses and configs (p. 2, p. 13, p. 17).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Models: DeepSeek-Coder-7b-instruct-v1.5 (dense) and DeepSeek-Coder-V2-Lite-Instruct (MoE, 16B total, ~2.4B active) (p. 8).
  - [V] Configuration: batch 8, max length 1,024, 6 mutations per prompt, 5 cached samples per outer epoch. Loss weights (1.00, 1.25, 1.00) were chosen from a small grid (p. 8, p. 18).
  - [V] **Per-run settings (Table 3, p. 19):**

| Method | LR (7B) | LR (16B) | Checkpoint reported |
|---|---|---|---|
| AU | 5×10⁻⁵ | 2×10⁻⁵ | selected (7B: 60; 16B: "50 restarted") |
| GA | 1×10⁻⁵ | 1×10⁻⁵ | final (1 outer epoch) |
| NPO | 1×10⁻⁵ | 1×10⁻⁵ | final (1 outer epoch) |
| PMC | 1×10⁻⁵ | 2×10⁻⁵ | selected (25 / 20) |
| CE-only | 1×10⁻⁵ | 1×10⁻⁵ | selected |
| NPO-only | 1×10⁻⁵ | 5×10⁻⁵ | selected |

  - [V] **Hallucination decision:** parse `pip install` lines; ask the model (Mode 1) which packages are required to run the code and (Mode 2) which would be useful; parse and de-duplicate; resolve against a static PyPI snapshot collected before all experiments. An unresolved name is a hallucination (p. 8, p. 20–21).
  - Not reported: snapshot date, stdlib handling, name normalisation.
  - [A] Packages distributed outside PyPI may be mislabelled (p. 12).
  - [V] **Hardware:** AMD MI210 and MI300 GPUs (p. 8); Appendix D says "MI200 / MI300" (p. 18). Runs were capped at 24 h wall-clock (7B) and 12 h (16B) (p. 19). Number of GPUs: not reported.
  - [V] **The 16B AU restart is described inconsistently.** Appendix D says it restarted "at checkpoint 60 for another 12 hours" (p. 18), but Table 3 lists "50 restarted" (p. 19).
  - [A] **Inference overhead:** none, since the change lives in the weights (p. 12).
- Code availability: [V] Anonymous repository, to be made permanent on acceptance (p. 13).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] HR = N_halluc / N_total over all identifiers from both modes (p. 9).
  - [V] KL divergence from the base model on code, instruction-following and package prompts, to bound collateral change (p. 9).
  - [V] EvalPlus pass@1 (p. 9).
- Statistical testing: [V] None. Single reported runs and no variance. The loss-weight choice mentions "repeated runs" (p. 18).

## 7. Key findings
1. [V] **DeepSeek-7B:** HR 21.23% → 2.56% (−88% relative), against GA 7.2%, NPO 14.17% and PMC 11.84% (Table 1, p. 10).
2. [V] **DeepSeek-16B:** HR 27.75% → 6.13% (−78%); GA reaches 13.75% (p. 10, p. 13).
3. [V] **Utility:**
   - On 7B, the EvalPlus average goes from 66.98 to 68.57 (p. 9–10).
   - On 16B it goes from 77.4 to 73.17, with HumanEval falling from 81.1 to 73.2. GA keeps HumanEval at 79.9 and the average at 77.35 (Table 1, p. 10).
   - PMC drops the 7B average to 51.65 (p. 9–10).
4. [V] **Drift on 7B:** AU's KL is 0.0796 on code, 0.9905 on instruction-following and 1.4211 on package prompts. These are the highest code and instruction KL values of any method on 7B. GA's code KL is 0.0031 (Table 1, p. 10).
5. [V] **Ablations (7B):** CE-only reaches 12.06% and NPO-only 12.42%. With 1 inner epoch HR stays at 13.8%; the minimum is 4.0% at 14 inner epochs. Without mutation HR is 10.7%, falling to 3.9% at 6 mutations and rebounding to 6.3% at 10 (p. 11–12).

## 8. Limitations stated by the authors
- [A] **Oracle dependence:** AU applies only to domains with deterministic ground truth. The oracle checks existence, not correct use, and mislabels non-PyPI packages (p. 12).
- [A] AU complements rather than replaces inference-time verification. Filtering at inference time needs registry access and adds latency per query (p. 12).
- [A] **Oracle poisoning:** names pre-registered by an attacker move from the forget set to the retain set, so AU "reinforces what it was deployed to suppress". The snapshot must be audited (p. 12).
- [A] **Token-disjointness assumption:** the case where a hallucinated name collides with a real identifier is not measured (p. 6, p. 12).
- [A] Two DeepSeek models and Python only. Frontier-scale full fine-tuning exceeded the compute budget. npm, vcpkg and Conan are future work (p. 12).
- [A] The explanation for the 16B MoE result is an untested hypothesis (p. 9).

## 9. Limitations we identified
- [I] **Near-in-distribution test.** The 40 test prompts are paraphrases of the 20 training seeds, and AU trains on model paraphrases of those same seeds. Generalisation to new tasks is untested. N_total is unreported, so 2.56% may rest on few identifiers.
- [I] **Checkpoint selection.** Table 3 reports "the checkpoint that yielded best results" with no stated validation set (p. 19). If it was chosen on test HR, results are optimistic.
- [I] **Tuning and checkpoint selection favour AU.**
  - AU uses a higher learning rate (5×10⁻⁵ for 7B, 2×10⁻⁵ for 16B) than GA and NPO (1×10⁻⁵).
  - GA and NPO report their final checkpoint after one outer epoch, while AU (and PMC, CE-only, NPO-only) report a selected checkpoint (Table 3, p. 19).
  - So the comparison is not tuning-matched.
- [I] **Internal inconsistencies:**
  - Fig. 4 shows 25.0% → 4.8% (81%), while Table 1 shows 21.23% → 2.56% (88%) (p. 10).
  - No-mutation HR is 10.7% in the text (p. 12) but 12.7% on p. 7 and in Fig. 7 (p. 13).
  - Appendix G says per-mode rates are reported "in our main results", but Table 1 gives only the total (p. 20).
  - MI210 vs MI200 (p. 8 vs p. 18).
  - The 16B AU restart is at checkpoint 60 per Appendix D (p. 18) but "50 restarted" per Table 3 (p. 19).
- [I] **"Surgical" is overstated; this is a trade-off, not dominance.**
  - On DeepSeek-7B, GA already reaches 7.2% HR with unchanged utility (average 66.95 vs 66.98) and far less code drift (KL 0.0031 vs 0.0796 for AU).
  - On 16B, GA keeps the average at 77.35 vs 73.17 for AU (Table 1, p. 10).
  - AU buys lower HR at the cost of more drift (7B) or lower coding scores (16B). The +6.7 pp HumanEval gain on 7B after unlearning is surprising for a single run.
- [I] **Stdlib not handled.** Mode 1 ("required packages") answers can include `os`, `json` and similar. If those count as hallucinations, the base rate is inflated (cf. +7.6–9.4 pp in djire2026evaluating) and training would suppress legitimate names.
- [I] **No release-date cutoff.** Names registered after model release count as valid, which is the poisoning issue the authors raise.
- [I] **Heavy compute.** Full-parameter runs of up to 24 h on data-centre GPUs, repeated per model. This is "lightweight" only relative to retraining.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Paraphrase leakage between training and test; checkpoint selection; unequal tuning across methods; hallucination-heavy prompt selection.
- External (generalisability of sample/context): [V] 2 DeepSeek models, Python only (p. 12).
- Construct (do metrics measure the concept?): [V] The oracle checks existence only (p. 12). [I] Stdlib treatment is unknown, and Mode 2 ("useful") inflates the opportunities to hallucinate.
- Statistical conclusion (power, multiple comparisons, variance): [V] Single runs, no variance (p. 10–11).
- Reproducibility (data/code/setup reported?): [V] Artifacts and per-run configurations are given (p. 17–19). Snapshot date, sample counts and GPU counts are missing, and the restart checkpoint is inconsistent.

## 11. Future research directions
- Stated by authors [A]:
  - Cross-language generalisation (npm, vcpkg, Conan) and other model families (p. 12–13).
  - Semantic-correctness oracles (p. 13).
  - Applying AU to general-purpose LLMs (p. 13).
  - Overlapping or soft-assigned spans (p. 12).
- Suggested by us [I]:
  - Use a larger, non-paraphrase held-out set and report N.
  - Match tuning effort across methods.
  - Make the oracle stdlib-aware and time-cutoff-aware.
  - Try a LoRA variant to cut cost.
  - Test robustness to poisoned registries.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ3 (defence effectiveness and cost), RQ4 (oracle design), RQ2 (oracle poisoning by squatted names).
- How it informs our work [I]:
  - **Laptop feasibility:** not feasible on a laptop. It needs full-parameter fine-tuning of 7B/16B models on MI210/MI300-class GPUs for 12–24 h. Not usable by end users of closed APIs, though the authors pitch it to vendors (p. 13).
  - **What it leaves open:**
    - Lightweight, client-side defences.
    - Other ecosystems.
    - Agents.
    - How to keep a training-based defence correct once hallucinated names have been registered by attackers. The authors' own poisoning analysis argues for pairing it with a vetted registry check.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Adaptive unlearning (full-parameter FT) lowers package HR 21.23%→2.56% (DeepSeek-7B) and 27.75%→6.13% (DeepSeek-16B) on 40 paraphrased held-out prompts | p. 10 | V | weak |
| RQ3 | Lowest HR of the compared methods, but gradient ascent reaches 7.2% (7B) with unchanged utility and lower code drift, and keeps 16B utility (77.35 vs 73.17); tuning not matched | p. 10, p. 19 | V | weak |
| RQ3 | Coding utility (EvalPlus avg) +1.6 pp on 7B, −4.2 pp on 16B (HumanEval 81.1→73.2); PMC loses 15 pp on 7B | p. 9–10 | V | weak |
| RQ3 | Requires full-parameter fine-tuning on AMD MI210/MI300 GPUs with 12–24 h runs; no inference-time cost | p. 8, p. 12, p. 19 | V | moderate |
| RQ2 | If attackers pre-register hallucinated names, the registry oracle labels them valid and unlearning reinforces them (oracle poisoning) | p. 12 | A | moderate |
| RQ4 | Hallucination detected by asking the model for required (Mode 1) and useful (Mode 2) packages and resolving names against a static PyPI snapshot | p. 8, p. 20–21 | V | strong |
| RQ3 | Both reinforcement (CE) and suppression (NPO) terms are needed; either alone leaves HR ≈12% on 7B | p. 11 | V | weak |

## 14. Key quotes
> "AU reinforces what it was deployed to suppress" (p. 12)

> "This 40 prompt test set is completely held-out of training and enables generalized testing on unseen prompts." (p. 8)

> "The PyPI ground-truth list is constructed from a static snapshot of the registry collected prior to all experiments" (p. 20)

## Analyst notes
- Reading coverage: all 21 PDF pages, including the appendices (prompts, hyperparameters, PMC formulation, detection pipeline). Figures 4–7 are known only through their text annotations.
- Uncertainties:
  - Samples and identifiers behind each HR.
  - Checkpoint-selection criterion.
  - 16B restart checkpoint (60 vs 50).
  - Snapshot date.
  - Stdlib handling.
  - Figure 4 vs Table 1 discrepancy.
- Funding: not reported.
- Quote note: the first and third quotes span line breaks or hyphenation in `fulltext.txt`.
- Review fixes (critical review 2026-11-12) applied while `ready`:
  - GA trade-off.
  - Tuning/checkpoint asymmetry (PMC also uses a selected checkpoint, Table 3, p. 19).
  - Checkpoint 60 vs 50 inconsistency.
  - 16B HumanEval drop vs GA.
