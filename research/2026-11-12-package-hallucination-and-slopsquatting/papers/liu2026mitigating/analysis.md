---
key: liu2026mitigating
status: complete
evidence_basis: full-text
design: Technique proposal + controlled experiment (localized LoRA model editing vs Full-FT, Self-Refinement, ROME, MEMIT, DINM) with 4 edit folds, ablation, cost and HumanEval checks
dataset: Per-model high-risk Python prompts (Sample-HR > 0.5 over 5 generations) from the Spracklen et al. LLM-generated prompt set; PyPI metadata with release-date cutoff
sample_size: 3 open LLMs (6.7-8B); 609-1,134 high-risk prompts per model (4 x 50 edit, 409-934 unseen); 5 samples per prompt; 100-prompt subsets for transfer and ablation
metrics: Sample-HR, Package-HR, Valid-Rate, HumanEval pass@1/pass@10, localization/edit/test time, adapter size
main_finding: Localized LoRA editing cuts high-risk-prompt Package-HR 79.9% (edit) and 65.4% (unseen) relative; Valid-Rate rises on average but falls for Qwen3; HumanEval within ±2%.
relevance: medium
analysed: 2026-11-12
---

# Mitigating Package Hallucinations in Large Language Models via Model Editing

- Authors: Liu, Shuhan; Zhao, Yukai; Hu, Xing; Liu, Kui; Yang, Xiaohu; Xia, Xin
- Year / venue: 2026, arXiv (preprint)
- DOI: 10.48550/arxiv.2607.02052 · URL: https://arxiv.org/abs/2607.02052
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified · **[A]** author claim · **[I]** our interpretation.

Source tier: preprint (arXiv v1, July 2026), **not peer-reviewed** (p. 1). Three of the authors (Zhao, Hu, Xia) also wrote HFuzzer (zhao2025hfuzzer).

## 1. Research objective
- [A] Propose BOUND, a lightweight localized model-editing framework. It treats package hallucination as a "package-validity boundary" problem: the model's ability to tell valid from hallucinated names in a given task context. The goal is to suppress hallucinated names while keeping valid ones (p. 1–2).

## 2. Research questions / hypotheses
- [V] RQ1: How effective is BOUND compared with package-hallucination mitigation and model-editing methods?
- [V] RQ2: Does it generalise to other package-related tasks?
- [V] RQ3: Ablation of its components (p. 6).

## 3. Methodology
- Research design: [V] Technique proposal with controlled comparison on 4 edit folds of 50 prompts each, plus ablation, cost and HumanEval checks (p. 5–9).
- Approach / model / intervention:
  - [V] **Localization:** one forward pass per high-risk prompt. A boundary risk score is computed at the first answer token as LSE(logits of hallucinated-name tokens) − λa·LSE(logits of valid-name tokens), then back-propagated through the frozen model. Saliency is mean |∇W R ⊙ W| per projection matrix (q, k, v, o, gate, up, down) over all layers. The top 5 modules are selected (p. 3–4, p. 6).
  - [V] **Editing:** LoRA with r=8, α=16, dropout 0.05, lr 2×10⁻⁴, 3 epochs, batch 1 (p. 6).
  - [V] **Loss:** valid-package NLL + unlikelihood on hallucinated names + locality KL, weighted 1.0 / 0.15 / 0.03 (p. 4–6).
  - [V] **Edit cases come from the model's own errors.** Each case uses the model's own valid and hallucinated names from its five generations (p. 5).
  - [V] **Required access:** full white-box access (weights, logits and gradients), plus a GPU training run per model. PyPI metadata is needed to label valid and hallucinated names when building edit cases (p. 3–5). [I] At inference only the LoRA adapter is needed, with no registry access.
- Baselines or comparison conditions:
  - [V] Full-FT (Spracklen et al.) and Self-Refinement (up to 5 rounds; the model's packages are checked for validity, and invalid ones go into an avoidance list).
  - [V] ROME, MEMIT and DINM, adapted with defaults. All trainable baselines use the same edit cases (p. 5–6).
  - [I] Self-Refinement here gets registry-oracle feedback.

## 4. Dataset and sample
- Data source(s): [V] The "recent Python subset" of the LLM-generated prompt dataset of Spracklen et al., built from descriptions of popular Python packages (p. 5).
- Sample size (N) and unit (Table I, p. 5):

| Model | High-risk prompts | Edit prompts | Unseen evaluation |
|---|---|---|---|
| DeepSeekCoder | 741 | 4×50 | 541 |
| Qwen3 | 609 | 4×50 | 409 |
| Llama-3.1 | 1,134 | 4×50 | 934 |

  - [V] Transfer and ablation use 100 random prompts from the unseen set (p. 7–8).
- Sampling / selection method: [V] Each prompt is queried 5 times and kept as "high-risk" if Sample-HR > 0.5 (p. 5). The size of the pool before filtering is not reported.
- Data availability (public? link?): not reported.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Models: deepseek-coder-6.7b-instruct, Qwen3-8B, Llama-3.1-8B-Instruct. PyTorch + HuggingFace Transformers, bf16 (p. 6).
  - [V] Generation: 5 samples per prompt, T=0.7, top_p 0.9. Maximum 128 tokens for recommendation and `pip install` tasks, 2,048 for code generation (p. 6).
  - [V] **Hallucination decision:** a package is valid only if it exists on PyPI *and* has at least one release before the model's knowledge cutoff; otherwise it is hallucinated (p. 5).
  - Not reported: the PyPI query date (the reference lists "accessed: 2026-06-14", p. 11), per-model cutoff dates, stdlib handling and normalisation.
  - [V] Extraction uses regular expressions, with one-shot prompting to fix the output format (p. 9).
  - [V] Code generation: imports are extracted, and the **unedited base model** maps them to PyPI names (p. 7).
  - [V] **Hardware:** Ubuntu 22.04, 2× Xeon Platinum 8358P (64 cores), 1 TB RAM, 8× A100-SXM4 80 GB (p. 6). GPUs per run: not reported.
  - [V] **Cost (Table V, "average cost … across models"; the unit of each time, per edit run or per case, is not defined, p. 9):**

| Method | Localization | Edit | Test time | Artifact |
|---|---|---|---|---|
| BOUND | 23.81 s | 83.09 s | 11.30 s | 731.03 KB |
| ROME | 10.19 s | 384.45 s | 10.86 s | 98.01 MB |
| MEMIT | – | 193.06 s | 13.17 s | 588.01 MB |
| DINM | 0.92 s | 11.97 s | 12.63 s | 126.68 MB |
| Full-FT | – | 124.16 s | 15.31 s | 14.27 GB |
| Self-Refinement | – | – | 25.12 s | – |

  - [A] The authors state that BOUND's edit time is "lower than ROME, MEMIT, and Full-FT" (p. 9). [I] That holds only because DINM (11.97 s edit, 0.92 s localization) is left out. ROME's test time (10.86 s) is also below BOUND's (11.30 s).
- Code availability: not reported.

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] Sample-HR is the share of answers with at least one hallucinated name. Package-HR is the share of hallucinated names among extracted names. Valid-Rate is the share of answers with at least one valid name, which says nothing about semantic correctness (p. 6).
  - [V] Changes are reported as **relative** percentages (p. 6).
  - [V] HumanEval pass@1 and pass@10 (p. 9).
- Statistical testing: [V] None. Averages over 4 folds × 5 samples; no variance (p. 6, p. 9).

## 7. Key findings
1. [V] **Edit prompts (average):** Sample-HR 0.8500 → 0.2050 (−75.9%), Package-HR 0.4463 → 0.0897 (−79.9%), Valid-Rate 0.8013 → 0.8527 (+6.4%) (p. 6). [V] Per model, Qwen3 Valid-Rate falls on edit prompts (0.7620 → 0.7410) and on unseen prompts (0.7990 → 0.7434, about −7%) (Table II, p. 7).
2. [V] **Unseen prompts:** Sample-HR 0.8573 → 0.3113 (−63.7%), Package-HR 0.4421 → 0.1529 (−65.4%), against −37.8% for Full-FT (p. 6–7). [V] Residual Package-HR on unseen prompts is 0.0927–0.1955 (Table II, p. 7).
3. [V] **Full-FT beats BOUND in one case.** On DeepSeekCoder Edit50, Full-FT is better on Package-HR (0.0188 vs 0.0745), Sample-HR (0.0580 vs 0.1980) and Valid-Rate (0.9500 vs 0.9480) (Table II, p. 7). [A] The authors' "best overall balance" claim (p. 7) rests mainly on unseen-prompt and cross-model results.
4. [V] **Collapse in baselines:** ROME and DINM lower hallucination by collapsing output. Llama ROME has Valid-Rate 0.0110 (p. 7). In the `pip install` task, ROME and Full-FT on Llama reach 0 HR together with 0 Valid-Rate (p. 8).
5. [V] **Transfer:** Package-HR −12.8% in code generation and −34.0% in `pip install` recommendation (p. 7–8).
6. [V] **HumanEval:** changes stay within ±2%, e.g. DeepSeekCoder pass@1 68.96% → 67.58% (Table VI, p. 9).
7. [V] **Ablation:** without hallucinated-name unlikelihood, Package-HR rises from 0.1508 to 0.5646. Without valid-package NLL, Valid-Rate falls from 0.8248 to 0.1512 (p. 9).

## 8. Limitations stated by the authors
- [A] Regex extraction may miss packages; randomness is handled by 5 samples and 4 folds; localization may be noisy (p. 9).
- [A] Only three open models; commercial models were excluded for reproducibility (p. 10).
- [A] PyPI only (p. 10).
- [A] Three tasks only, not configuration files, build scripts or repository workflows (p. 10).

## 9. Limitations we identified
- [I] **Extreme subset only.** Prompts were kept only if Sample-HR > 0.5, so base rates are ~0.85. Relative reductions on this subset do not translate to population-level rates.
- [I] **Small, same-distribution edit sets.** Each fold has 50 prompts. The "unseen" set comes from the same model-specific filtered pool, so it is not out-of-distribution.
- [I] **"Unseen" gains may be memorised-name suppression.** Edit cases suppress the model's own hallucinated names (p. 5), and unseen prompts come from the same pool. If the same fabricated names recur across prompts, part of the gain is suppression of memorised names, not a learned boundary. Name overlap between the edit and unseen sets is not reported.
- [I] **Residual risk remains.** About 9–20% of names stay hallucinated on unseen high-risk prompts, which are still squattable.
- [I] **Valid-Rate is not uniformly preserved.** Qwen3 loses about 7% on unseen prompts (p. 7).
- [I] **LLM inside the measurement.** In code generation, imports are mapped to PyPI names by an LLM. Stdlib handling is unspecified, so `import os` may be mis-scored.
- [I] **Questionable utility baseline.** Qwen3-8B HumanEval pass@1 of 23.29% (p. 9) is unexpectedly low for that model, and the setup is not explained. This weakens the utility check for Qwen3.
- [I] **Uneven baseline.** Self-Refinement uses registry feedback and is evaluated only on Edit50 (p. 7).
- [I] **Selective cost comparison.** The edit-time claim omits DINM (p. 9).
- [I] **Good cutoff design, missing detail.** The release-date cutoff for validity is a sound choice: it excludes post-cutoff registrations, including squatted names. But the cutoff dates are not reported.
- [I] No code or data release is stated, and no variance is reported.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] High-risk selection; same-pool unseen set with possible name overlap; an LLM-based mapping step.
- External (generalisability of sample/context): [V] 3 open 6.7–8B models, PyPI only (p. 10).
- Construct (do metrics measure the concept?): [V] Valid-Rate does not measure task correctness (p. 6). [I] Relative-percentage reporting magnifies effects at high base rates.
- Statistical conclusion (power, multiple comparisons, variance): [V] No variance or tests (p. 6–9).
- Reproducibility (data/code/setup reported?): [V] Hyperparameters and hardware are given (p. 6). Code, data, snapshot date and cutoffs are not.

## 11. Future research directions
- Stated by authors [A]: more ecosystems and languages (e.g. Java); configuration files, build scripts and repository-level workflows (p. 10–11).
- Suggested by us [I]:
  - Evaluate on representative, not only high-risk, prompts.
  - Report name overlap between edit and unseen sets.
  - Combine with a registry check.
  - Test the adapter in quantized CPU inference.
  - Test robustness over time as the registry changes.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ3, RQ4.
- How it informs our work [I]:
  - **Laptop feasibility:** not feasible on a laptop without a GPU. Editing needs gradients through 7–8B models in bf16; the authors used A100s. The 731 KB adapter could in principle be loaded by a local runtime for inference, but this was not tested. Not applicable to closed APIs.
  - **Methodology lesson:** the release-date cutoff in the validity rule is worth reusing.
  - **What it leaves open:**
    - Non-zero residual hallucination.
    - npm and other ecosystems.
    - Agents and requirements files.
    - Behaviour on ordinary prompts.
    - Names registered by attackers after editing.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Localized LoRA editing (5 modules, 731 KB adapter) lowers Package-HR 0.4463→0.0897 on edit prompts and 0.4421→0.1529 on unseen high-risk prompts (3 models) | p. 6–7 | V | weak |
| RQ3 | Residual Package-HR after editing stays 0.09–0.20 on unseen high-risk prompts | p. 7 | V | moderate |
| RQ3 | Valid-Rate rises on average (+6.4% edit) but falls for Qwen3 (unseen 0.7990→0.7434) | p. 6–7 | V | weak |
| RQ3 | Full-FT outperforms BOUND on DeepSeekCoder Edit50 (Package-HR 0.0188 vs 0.0745) but generalises worse to unseen prompts (−37.8% vs −65.4%) | p. 7 | V | weak |
| RQ3 | ROME/DINM/Full-FT can reach ~0 HR only by collapsing package output (Valid-Rate ≈ 0) | p. 7–8 | V | moderate |
| RQ3 | Transfer: −12.8% Package-HR in code generation, −34.0% in pip-install recommendation (relative) | p. 7–8 | V | weak |
| RQ3 | HumanEval pass@1 changes within ±2% after editing | p. 9 | V | weak |
| RQ3 | Requires white-box weights, gradients, LoRA training on GPU (8×A100 server) and registry labels; per edit run (unit undefined), averaged across models: edit 83.09 s, localization 23.81 s | p. 3–6, p. 9 | V | moderate |
| RQ4 | Validity = exists on PyPI with ≥1 release before the model's knowledge cutoff | p. 5 | V | strong |

## 14. Key quotes
> "A package is valid only if it exists on PyPI and has at least one release before the model's knowledge cutoff." (p. 5)

> "BOUND is lightweight in practice, requiring only 731 KB of LoRA parameters on average" (p. 2)

## Analyst notes
- Reading coverage: all 12 PDF pages. The two-column extraction was readable and Tables I–VI were extracted cleanly.
- Uncertainties:
  - PyPI query date and per-model cutoffs.
  - Stdlib handling.
  - Size of the pool before high-risk filtering.
  - Units of the Table V times.
  - Qwen3 HumanEval setup.
  - Overlap of hallucinated names between edit and unseen sets.
- Funding: not reported.
- Quote note: the first quote spans a line break in `fulltext.txt` (p. 5); the apostrophe in "model's" is a typographic ’ in the source.
- Review fixes (critical review 2026-11-12) applied while `ready`:
  - main_finding (Qwen3 Valid-Rate).
  - Cost-row unit.
  - Full Table V incl. DINM and ROME.
  - Full-FT DeepSeekCoder Edit50 result.
  - Memorised-name caveat.
