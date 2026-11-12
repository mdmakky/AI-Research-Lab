---
key: djire2026evaluating
status: complete
evidence_basis: full-text
design: Comparative empirical evaluation (8 models x 4 languages x 8 strategies, 3 runs) + measurement-bias analysis + adversarial stress test
dataset: 4,000 GPT-4o-mini prompts seeded from top-1,000 Libraries.io packages per registry (PyPI, npm, RubyGems, crates.io); 4,000 adversarial prompts; registry snapshots of 2026-03-04 + stdlib manifests
sample_size: 8 open-weight 1-8B models; 4,000 standard + 4,000 adversarial prompts; 3 runs per configuration
metrics: micro/macro Package Hallucination Rate (PHR), Package Utility (precision/recall/F1 vs embedding-based reference set), Semgrep syntax-error rate and code-smell count
main_finding: No inference-time defence dominates; RAG gives lowest PHR in 19/32 settings but worsens JavaScript; ignoring stdlib inflates Python PHR by up to 9.4 pp.
relevance: high
analysed: 2026-11-12
---

# Evaluating Inference-Time Defenses against Package Hallucination in LLM-Generated Code

- Authors: Djire, Alberick Euraste; Olatunji, Iyiola E.; Tessa, Melissa; Barr, Earl T.; Klein, Jacques; Bissyandé, Tegawendé F.
- Year / venue: 2026, Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering (published)
- DOI: 10.1145/3832783.3837555 · URL: https://doi.org/10.1145/3832783.3837555
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified · **[A]** author claim · **[I]** our interpretation.

Source tier: peer-reviewed (ASE 2026) (p. 1). The text used is arXiv v1, which carries the ACM DOI (p. 1).

## 1. Research objective
- [A] Four contributions (p. 1–2):
  - Correct registry-based measurement, which misclassifies standard-library modules as hallucinations.
  - Evaluate seven inference-time defences.
  - Introduce a Package Utility (PU) metric.
  - Stress-test the defences with adversarial prompts.
- [A] The focus is small open models, because they hallucinate more and run on resource-constrained hardware (p. 2, p. 4).

## 2. Research questions / hypotheses
- [V] RQ1: How does baseline PHR vary across model families and languages once stdlib imports are accounted for?
- [V] RQ2: How effective is guided decoding compared with RAG and Self-Refine?
- [V] RQ3: What is the trade-off between mitigation and utility?
- [V] RQ4: How robust are the defences to prompts seeded with fabricated names? (p. 3)

## 3. Methodology
- Research design: [V] Factorial comparison: 8 models × 4 languages (Python, JavaScript, Ruby, Rust) × vanilla + 7 strategies. Each runs on the full D_eval with 3 independent runs (p. 3, p. 5).
- Approach / model / intervention (with **required access**):
  - [V] **Greedy:** T=0 (p. 5). The paper counts Greedy as one of its five guided decoding strategies (p. 2, p. 6). [I] Works with an API.
  - [V] **Contrastive Decoding (CD):** α=0.5, "amateur/expert layer pairing (model-specific)" (Table 1, p. 5). The text describes subtracting a smaller amateur model's log-probabilities (p. 4). [I] It needs logits from two models (or layers); the description is inconsistent.
  - [V] **DoLa:** contrasts the final layer with early layers {4, 8, 12, 16}; repetition penalty 1.2 (p. 5). [I] White-box: needs intermediate hidden states.
  - [V] **ALCD:** DoLa plus an entropy ≥1 activation policy (p. 5). [I] White-box.
  - [V] **Nudging:** the surrogate is the "largest in family"; top-probability threshold 0.4 (p. 5). [I] Needs token probabilities plus a second model. Given the model list (p. 3), the largest in family is the model itself for 5 of 8 models (gemma-4b, deepseek-6.7b, qwen-3b, mistral-7b, llama-8b). The paper does not explain what Nudging does in those cases (p. 5).
  - [V] **Self-Refine:** up to 5 iterations of self-critique (p. 4–5). [I] Black-box. Whether the critique sees registry data is not reported.
  - [V] **RAG:** retrieval k=5 over a per-language registry corpus, following Spracklen et al.'s top-k setup (p. 4–5). Retriever and embedder: not reported. [I] Black-box model plus an external index.
  - [A] CD and Nudging run two models at once, so model sizes were capped to fit one GPU (p. 4).
- Baselines or comparison conditions: [V] Vanilla decoding with T=1.0, top-k 50, top-p 1.0 (p. 4–5). One fixed configuration per strategy, based on Shi et al. (p. 4).

## 4. Dataset and sample
- Data source(s):
  - [V] Step 1: the top 1,000 most popular packages per registry via the Libraries.io API, as (name, description) pairs (p. 3).
  - [V] Step 2: full registry name lists "as of March 4, 2026", plus standard-library module lists. The ground truth P_ℓ is registry ∪ stdlib (p. 3).
  - [V] Step 3: GPT-4o-mini writes one coding instruction per pair. The system prompt asks for a bracketed package list (p. 3).
- Sample size (N) and unit:
  - [V] D_eval has 4,000 instructions, 1,000 per language (p. 3).
  - [V] Eight models: gemma-1b/4b, deepseek-coder-1.3b/6.7b, qwen2.5-1.5b/3b, mistral-7b-Instruct-v0.3, llama-3.1-8b (p. 3).
  - [V] Generated packages range from 1,470 to 32,337 per model–language cell under vanilla decoding (Table 3, p. 6).
- Sampling / selection method:
  - [V] Adversarial set: 1,000 non-existent names each for Python and JavaScript, produced by Meta-Llama, Alibaba and OpenAI GPT models, verified absent from npm/PyPI by direct lookup. The same names are reused as seeds for Ruby and Rust and placed into "install and use" templates, giving 4,000 prompts (p. 9).
  - [V] Code-generation extension: the same instructions, asking for runnable code; imports are validated against the same snapshots (p. 6).
- Data availability (public? link?): [V] Code, datasets and instructions on Zenodo record 21786704 (p. 11).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] **Hallucination decision:** a name is "classified as hallucinated if and only if it is absent from P_ℓ" (p. 4).
  - Not reported: name normalisation and output-parser details.
  - [V] **Code generation:** "All imported packages are validated against the same registry snapshots" (p. 6). No import-to-distribution mapping is described.
    - [I] Import names that are not registered under the same name (e.g. `cv2` for `opencv-python`) probably count as hallucinations. That would inflate the hallucinated counts in Fig. 1.
  - [V] **Stdlib:** manifests were collected for "the two applicable languages" (Python, Ruby) (p. 5), although Step 2 says every snapshot is augmented (p. 3). [I] Treatment of JavaScript and Rust built-ins is unclear.
  - [V] **Hardware:** "within the memory budget of a single GPU" (p. 4). GPU type, inference library and runtimes: not reported.
  - **Overhead/latency of the strategies:** not reported.
  - [V] **Code quality:** Semgrep syntax-error rate and code-smell count (p. 7).
  - [V] Mean ± SD over 3 runs; per-run values are in the artifact (p. 5).
- Code availability: [V] Zenodo (p. 11).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] Micro-PHR pools all generated names. Macro-PHR averages per prompt, and a prompt with no output counts as 0 (p. 4). [I] Macro-PHR therefore rewards silence.
  - [V] PU is the F1 of precision and recall against R_i: the seed package plus the k−1 packages with most similar descriptions (text-embedding-3-small, cosine), k ∈ {1, 2, 5, 10}, plus a reference set derived from generated code. PU is 0 for empty outputs (p. 4, p. 7). [A] PU "remains a semantic proxy" (p. 4).
  - [V] Syntax-error rate and mean smell count (p. 7–8).
- Statistical testing: [V] Mean ± SD over 3 runs. No significance tests or confidence intervals. Counts like "19 of 32" are not corrected for multiple comparisons (p. 5–10).

## 7. Key findings
1. [V] **Stdlib correction:** pooled Python vanilla PHR is 24.7% with stdlib vs 32.3% without (+7.6 pp). The maximum is +9.4 pp (Self-Refine); Ruby ranges +1.6 to +2.5 pp (Table 2, p. 5). [V] Table 3's Python counts sum to N_gen 79,965 and N_hall 19,776, which gives 24.7% (p. 6).
2. [V] **Baseline:** corrected vanilla micro-PHR ranges from 16.1% (Mistral-7b) to 47.9% (Qwen-1.5b) overall, peaks at 63.1% (Qwen-1.5b, Rust) and is lowest at 7.6% (Mistral, JavaScript). Larger in-family models cut PHR by 18.3–20.3 pp (p. 5–6).
3. [V] **Defences:**
   - RAG has the lowest PHR in 19 of 32 configurations and lowers the cross-model average from 29.7% to 18.1%. But it raises JavaScript PHR for 7 of 8 models, by 12.7 pp on average (p. 6).
   - By our count from Table 4, RAG is below Vanilla in 24 of 32 cells (p. 7).
   - Greedy matches Self-Refine at 25.6% average PHR (p. 6).
   - DoLa is the worst guided method at 38.0% overall, and 83.5–91.2% on DeepSeek-1.3b (p. 6).
   - CD never achieves the lowest PHR (p. 6), although by our count it is below Vanilla in 19 of 32 cells (Table 4, p. 7). ALCD mostly underperforms vanilla (p. 6–7).
4. [V] **Utility:** Greedy gives the best trade-off, with the highest PU under all five reference sets. PU recall falls from 23.4 (Top-1) to 2.7 (Top-10). DeepSeek models have near-zero PU (p. 7–8).
5. [V] **Code quality:** vanilla and greedy decoding keep near-perfect syntax, while guided strategies add syntax errors, e.g. a 29% rate for DeepSeek-6.7b on Rust under Nudging (p. 7). In code generation, Self-Refine increases both valid and hallucinated references (p. 6).
6. [V] **Adversarial prompts:**
   - Vanilla PHR spans 46.6–92.5%; Mistral-7b rises by 47.8 pp on average. Ruby is the most vulnerable and Rust the most resistant language for every model (p. 9).
   - RAG or Self-Refine gives the lowest PHR in 29 of 32 settings, RAG alone in 16. The lowest value is 11.4% (Gemma-4b, Python, RAG) (p. 10).
   - DoLa is worse than Greedy in 24 of 32 (p. 10).

## 8. Limitations stated by the authors
- [A] Prompts are synthetic (GPT-4o-mini), with no human validation or comparison to real developer queries (p. 10).
- [A] Only 8 small open models and 4 ecosystems. Results may not generalise to larger models, other languages or private registries (p. 10).
- [A] One fixed hyperparameter configuration per strategy, so rankings are not upper bounds (p. 10).

## 9. Limitations we identified
- [I] **Internal inconsistencies:**
  - The abstract's "18 of 32" for RAG (p. 1) matches neither the 24/32 reductions vs Vanilla nor the 19/32 "lowest" count derivable from Table 4 (p. 7). The 19/32 count is the one stated on p. 6.
  - The abstract says PHR rises "up to 45 pp"; the conclusion says "up to 58.1 pp" (p. 1 vs p. 11). Mistral's +47.8 pp average (p. 9) already exceeds 45.
  - The conclusion calls Nudging the best trade-off "among the guided decoding strategies" (p. 11). But the paper counts Greedy as guided (p. 2, p. 6), and Greedy has the best trade-off (p. 8).
  - Table 1 describes CD as a layer pairing; the text describes two models (p. 4–5).
  - Stdlib augmentation is said to apply to every snapshot vs only "two applicable languages" (p. 3 vs p. 5).
  - p. 6 says RAG lowers PHR "without increasing PHR for any model" in Python, Ruby and Rust. But Table 4 shows mistral-7b on Rust rising from 18.6 to 20.8 under RAG (p. 7).
- [I] **Suspicious table values:** Table 4 shows Greedy identical to Vanilla in all 4 languages for deepseek-6.7b and llama-8b (p. 7), although Vanilla is sampled at T=1.0 over 3 runs. This looks like a copy error.
- [I] **Nudging may be a no-op.** For 5 of 8 models, the surrogate ("largest in family") is the model itself (p. 3, p. 5). Nudging may then reduce to self-nudging, and its results for those models are hard to interpret.
- [I] **Popularity-seeded prompts:** prompts are built from the 1,000 most popular packages, so the right answer is usually a well-known name. RAG retrieves descriptions from the same registry and may simply retrieve the seed package, which flatters RAG and may understate hallucination on niche tasks.
- [I] **No release-date cutoff:** the ground truth is the current snapshot (2026-03-04). Names registered after model training, including squatted hallucinations, count as valid.
- [I] **Code-generation imports are checked without mapping (p. 6).** Unregistered import names such as `cv2` probably inflate the hallucinated counts.
- [I] **No cost data:** no latency or memory figures, although the defences are presented as practical. CD and Nudging double the model count.
- [I] **Missing defences:** neither PackMonitor-style constrained decoding nor a plain registry filter is evaluated.
- [I] **Adversarial seeds:** seeds for Ruby and Rust were only checked as absent from npm/PyPI (p. 9). Scoring is still snapshot-based, so this affects prompt design, not scoring.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Synthetic prompts; possible retrieval of the seed package by RAG; inconsistent reporting.
- External (generalisability of sample/context): [V] Small open 1–8B models only (p. 10). No API models or agents.
- Construct (do metrics measure the concept?): [V] PU is a semantic proxy based on embedding similarity (p. 4). [I] Macro-PHR counts empty outputs as 0. Import names are checked as package names in code generation.
- Statistical conclusion (power, multiple comparisons, variance): [V] 3 runs with SD reported; no tests (p. 5).
- Reproducibility (data/code/setup reported?): [V] Zenodo artifact and Table 1 hyperparameters (p. 5, p. 11). Hardware and parser are unspecified.

## 11. Future research directions
- Stated by authors [A]:
  - Make per-language stdlib exclusion a baseline requirement (p. 11).
  - Test indirect prompt injection and multi-turn manipulation (p. 11).
  - Combine guided decoding with lightweight registry verification at inference time (p. 11).
- Suggested by us [I]:
  - Report latency on CPU.
  - Add a registry-filter baseline and constrained decoding.
  - Use release-date-aware ground truth.
  - Add an import-to-distribution map.
  - Use real developer prompts.
  - Test agentic install flows.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ3, RQ4, RQ5.
- How it informs our work [I]:
  - **Laptop feasibility:** Greedy (T=0), Self-Refine and RAG need no internal access and were tested on 1–8B models. The 1–4B models are plausible on a laptop CPU, but the paper gives no runtimes. DoLa, ALCD, CD and Nudging need white-box access and sometimes two models.
  - **Methodology lesson for our measurement:** use a dated snapshot, a stdlib manifest and an import-to-distribution map, and report micro and macro PHR.
  - **What it leaves open:**
    - Overhead and cost.
    - Registry-verification defences.
    - Constrained decoding.
    - Agents and indirect injection.
    - Larger or closed models.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ4 | Treating stdlib modules as hallucinations inflates Python PHR by +7.6 pp (vanilla) up to +9.4 pp; Ruby ≤ +2.5 pp | p. 5 | V | moderate |
| RQ4 | Hallucination = name absent from registry snapshot (2026-03-04) ∪ stdlib manifest | p. 3–4 | V | strong |
| RQ1 | Corrected vanilla micro-PHR 16.1% (Mistral-7b) to 47.9% (Qwen-1.5b); up to 63.1% (Qwen-1.5b Rust); larger in-family models −18 to −20 pp | p. 5–6 | V | moderate |
| RQ3 | RAG lowest PHR in 19/32 settings (below Vanilla in 24/32), average 29.7%→18.1%, but raises JavaScript PHR by 12.7 pp on 7/8 models | p. 6–7 | V | moderate |
| RQ3 | Greedy decoding (T=0, black-box) gives best average mitigation–utility trade-off (PHR 29.7%→25.6%, highest PU) | p. 6, p. 8 | V | moderate |
| RQ3 | DoLa is the worst guided strategy (38.0% average PHR; 83.5–91.2% on DeepSeek-1.3b); guided strategies add syntax errors (up to 29%) | p. 6–7 | V | moderate |
| RQ3 | DoLa/ALCD/CD/Nudging need logits or hidden states (CD/Nudging a second model), so they cannot run on closed APIs | p. 4–5 | I | moderate |
| RQ1 | Adversarial prompts seeded with fake names raise vanilla PHR to 46.6–92.5%; Ruby most vulnerable for all 8 models | p. 9 | V | moderate |
| RQ3 | Under adversarial prompts RAG or Self-Refine is best in 29/32 settings; decoding-only defences unreliable | p. 10 | V | moderate |
| RQ5 | No latency/overhead and no GPU model reported for any defence | p. 4 | I | moderate |
| RQ5 | Authors propose combining guided decoding with lightweight registry verification at inference time | p. 11 | A | moderate |

## 14. Key quotes
> "A recommended name is classified as hallucinated if and only if it is absent from Pℓ" (p. 4)

> "we collected the complete list of package names available in each registry as of March 4, 2026" (p. 3)

> "inference within the memory budget of a single GPU" (p. 4)

## Analyst notes
- Reading coverage: all 13 PDF pages. The Figure 3 heatmaps (PU) and Figure 2 are partly garbled in extraction, so I used the text's summary values only.
- Own counts from Table 4 (p. 7): RAG < Vanilla in 24/32 cells; RAG lowest in row in 19/32; CD < Vanilla in 19/32; CD lowest in 0/32.
- Uncertainties: Table 4 Greedy=Vanilla rows; stdlib handling for JavaScript and Rust; Nudging with self-surrogate; abstract–body–conclusion inconsistencies (§9).
- Funding: Luxembourg MFA (D4D/LuxWAyS), ERC NATURAL (p. 11).
- Review fixes (critical review 2026-11-12) applied while `ready`:
  - CD/Nudging inconsistency reworded.
  - "18 of 32" wording.
  - Mistral-7b Rust contradiction.
  - Nudging surrogate note.
  - Table 3 unit.
  - Evidence rows split and relabelled.
  - Code-gen import note.
