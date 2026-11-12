---
key: liu2026packmonitor
status: complete
evidence_basis: full-text
design: Technique proposal + controlled experiment (decoding-time constrained decoding vs RAG/SR/RAG+SR/SFT baselines)
dataset: HFuzzer fuzzing rounds (DeepSeek-V3 tester) + subset of Package4U (Spracklen et al.); PyPI list of 706,618 names
sample_size: 5 open-weight 7-8B LLMs; 1 HFuzzer round (1,000 iterations) per model x configuration; 231-2,288 recommended packages per run
metrics: Package Hallucination Rate (PHR), Response Hallucination Rate (RHR), unique hallucinated packages, avg generation time, HumanEval Pass@1
main_finding: Logit masking against a cached DFA of the PyPI name list drives PHR to 0% on five 7-8B models with x1.07-x1.28 latency and unchanged HumanEval.
relevance: high
analysed: 2026-11-12
---

# PackMonitor: Towards Zero Package Hallucinations via Decoding-Time Monitoring

- Authors: Liu, Xiting; Liu, Yuetong; Zhang, Yitong; Li, Jia; Hu, Shi-Min
- Year / venue: 2026, Proceedings of the ACM on Software Engineering (published)
- DOI: 10.1145/3832118 · URL: https://doi.org/10.1145/3832118
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.

Source tier: peer-reviewed (PACMSE, ISSTA 2026 issue, article ISSTA027) (p. 1). The text used is arXiv v2, whose first page carries the ACM DOI and publication data (p. 1).

## 1. Research objective
- [A] Eliminate package hallucinations in LLM dependency recommendations, not merely reduce them. The argument: package-name validity can be decided against a finite, enumerable authoritative package list, so hallucinated names can be made unreachable during decoding (p. 1, p. 2).
- [A] Achieve this without training, as a plug-in, with low latency and no loss of model utility (p. 1, p. 3).

## 2. Research questions / hypotheses
- [V] RQ1: How effective is PackMonitor at eliminating package hallucinations compared with baselines? (p. 10)
- [V] RQ2: How much efficiency overhead does it add? (p. 10)
- [V] RQ3: Does it degrade general code-generation capability? (p. 10)
- [V] RQ4: How much does DFA caching improve inference efficiency and scalability? (p. 10)

## 3. Methodology
- Research design: [V] A technique proposal tested by controlled comparison against training-free baselines (RAG, Self-Refinement, RAG+SR) on HFuzzer and against SFT on Package4U. It also includes an ablation (with vs without cache) and a scaling test of DFA construction and loading time (p. 10, p. 12–17).
- Approach / model / intervention:
  - [V] A *Context-Aware Parser*, modelled on a context-free grammar, tracks whether the output is natural language, an ordinary code line, or the package names of an installation command. It recognises code blocks by delimiters such as ```bash and switches intervention on only after `pip install` (grammar `INSTALL_CMD_LINE → pip install PACKAGE_NAMES \n`) (p. 8).
  - [V] A *Package-Name Intervenor* compiles the authoritative list into a deterministic finite automaton (DFA, a state machine that accepts exactly the listed names). A token trie is built from the tokenizer vocabulary. At each step, every token that cannot extend the current prefix towards some allowlisted name gets logit −∞. A terminator is allowed only once the prefix is a complete allowlisted name (p. 6, p. 8–9).
  - [V] A *DFA-Caching Mechanism* builds the DFA once offline, stores it as a checkpoint and loads it at inference time (p. 10).
  - [V] **Required access:** the method masks the model's logits at every decoding step, so it needs next-token logits from a locally decoded model plus that model's tokenizer vocabulary (p. 9). No training and no weight changes (p. 3).
  - [I] It therefore cannot be added to a closed chat API (ChatGPT, Claude, Copilot) that does not expose per-step logits or accept an arbitrary token-level constraint. The paper does not discuss black-box APIs.
- Baselines or comparison conditions:
  - [V] Vanilla; RAG (retrieved valid package names injected into the prompt); Self-Refinement (SR); RAG+SR; and SFT, using the fine-tuned checkpoints released by Spracklen et al. (p. 11, p. 13–14).
  - [V] "Following prior work on mitigating package hallucinations [41], we include three representative baselines" (p. 11). The RAG retriever, corpus and k are not reported.
  - [I] No baseline is a simple post-generation registry lookup that blocks invalid names.

## 4. Dataset and sample
- Data source(s):
  - [V] HFuzzer (Zhao et al., ASE 2025) is the primary evaluation framework. It is a fuzzer in which a tester model (DeepSeek-V3, temperature 0) iteratively writes test cases for the target model (temperature 0.7) (p. 10–12).
  - [V] Package4U, the ~40,000-task dataset of Spracklen et al. (about half Python), is used "in a subset of our experiments", namely the SFT comparison (p. 11, p. 14).
  - [V] HumanEval is used for utility (p. 16).
  - [V] Authoritative list: the PyPI index, 706,618 names "at the time of our experiments", obtained via PyPI's official API (p. 12, p. 19). The snapshot date is not reported.
- Sample size (N) and unit:
  - [V] Five open-weight models: DeepSeek-Coder-Instruct-6.7B, CodeLlama-7b-Instruct, Qwen2.5-Coder-7B-Instruct, Meta-Llama-3-8B-Instruct and Meta-Llama-3.1-8B-Instruct (p. 11).
  - [V] One HFuzzer round of 1,000 iterations per model × configuration (p. 12).
  - [V] Units are recommended packages (P_total from 231 to 2,288 per run) and responses (Table 2, p. 13).
  - The Package4U subset size is not reported.
- Sampling / selection method: [V] Models follow HFuzzer's selection "to ensure a fair comparison" (p. 11). HFuzzer generates prompts adaptively (p. 10). [I] So each configuration sees a different, self-generated prompt stream.
- Data availability (public? link?): [V] Code is at https://github.com/THU-Agent/PackMonitor (p. 20). Settings are in the supplementary material (p. 19). Release of HFuzzer transcripts: not reported.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Tester temperature 0 and target temperature 0.7 on HFuzzer; temperature 0 for HumanEval (p. 12, p. 16).
  - [V] **Hallucination decision:**
    - The definition covers non-existent packages and packages from the wrong ecosystem (p. 2, p. 4).
    - Validity is membership of "a finite and enumerable list of valid package names … either from an official registry snapshot or a curated allowlist" (p. 6). In the experiments that list is the PyPI index (p. 12).
    - The metrics (PHR, RHR, unique count) are adopted from Spracklen et al. and HFuzzer (p. 12).
    - [I] Whether HFuzzer's own oracle uses the same 706,618-name list is not stated. If it does, the 0% result holds by construction.
  - [I] **Import path vs install name.** The paper's own motivating example is import-path vs install-name confusion: `google.protobuf` is a legitimate import path, but `google-protobuf` is not in the list (p. 6). The mask guarantees only that *some* listed name is produced, not the intended package.
  - **Stdlib handling:** not reported. [I] This matters little here, because only `pip install` arguments are constrained and scored.
  - **Name normalisation** (case, `-`/`_`): not reported.
  - Handling of version pins, flags (`-U`, `-r`), `python -m pip` and `conda`/`npm`: not reported for the experiments. Other ecosystems are discussed only "in principle" (p. 19).
  - [V] **Hardware:** a server with 8× NVIDIA A100 80 GB, 2× AMD EPYC 7543 (64 cores) and 1 TB RAM, running Ubuntu 22.04 (p. 12). GPUs used per run, inference framework and DFA memory footprint: not reported.
  - [V] **Overhead, with cache:** time per response rises ×1.07–×1.28, i.e. +0.06 s to +0.58 s (Table 4, p. 14). The text says "around 0.2s in the worst case" (p. 15), but CodeLlama goes from 2.4296 s to 3.0130 s (+0.58 s) (p. 14).
  - [V] **Overhead, without cache:** ×2.81–×6.24 (Table 6, p. 17).
  - [V] **DFA build vs load:** building takes 0.021 s (7k names), 4.407 s (700k) and 21.121 s (3,000k); loading takes 0.002–0.247 s (Table 7, p. 17).
- Code availability: [V] Public GitHub repository (p. 20).

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] PHR is hallucinated packages divided by recommended packages. RHR is the share of responses with at least one hallucinated package. P_hall-unique counts distinct hallucinated names, as a measure of diversity. All three are adopted from prior work (p. 12).
  - [V] P_total checks that the method does not work by suppressing recommendations (p. 13).
  - [V] Mean generation time measures overhead (p. 15). HumanEval Pass@1 measures utility (p. 16).
  - [I] There is no metric of whether the forced package is correct or relevant for the task (cf. Package Utility in djire2026evaluating).
- Statistical testing: [V] None. Single runs. Only Fig. 3 shows a standard deviation of latency (p. 15).

## 7. Key findings
1. [V] PHR and RHR are 0% on all five models on HFuzzer. For example, DeepSeek-Coder goes from 8.39% / 11.60% (vanilla) to 0% / 0% (Table 2, p. 13). The lowest baseline is RAG+SR on CodeLlama at 1.30% PHR, but that run produced only 231 recommended packages vs 1,004 for vanilla (p. 13).
2. [V] RAG can increase hallucination. Qwen2.5-Coder PHR goes from 3.25% to 3.33%, and Llama-3 RHR from 6.40% to 7.10% (p. 12–13). SR never reaches zero; DeepSeek-Coder ends at 7.55% PHR (p. 13).
3. [V] On Package4U, SFT lowers PHR from 16.14% to 2.66% (DeepSeek-Coder) and from 26.28% to 10.27% (CodeLlama); PackMonitor gives 0% (Table 3, p. 14). The SFT checkpoints could not run through HFuzzer because their instruction-following was degraded (p. 14).
4. [V] Overhead with cache is ×1.07–×1.28, against RAG up to ×1.70, SR up to ×1.94 and RAG+SR up to ×2.65 (Table 4, p. 14–15).
5. [V] HumanEval Pass@1 is unchanged on all five models (e.g. 72.6% vs 72.6%). The SFT drops of −26.9 and −14.0 pp are quoted from [41], not re-measured (Table 5, p. 16).
6. [V] P_total is described as "comparable", e.g. DeepSeek-Coder 1,847 vs 1,648. But CodeLlama goes from 1,004 to 1,514 (p. 13).

## 8. Limitations stated by the authors
- [A] The guarantee is conditional on the correctness and completeness of the list. A stale snapshot or omissions undermine it, so the list must be refreshed periodically (p. 18–19).
- [A] Timing results may vary with deployment hardware. Effectiveness does not (p. 19).
- [A] Scope is chat-based PyPI recommendations after `pip install` only. It does not cover `requirements.txt`, Dockerfiles, CI configurations or coding-agent workflows (p. 19).
- [A] It targets name validity, not executability, API compatibility or version compatibility (p. 19).
- [A] Generalisability across models is argued from five LLMs plus adversarial HFuzzer prompts (p. 19).

## 9. Limitations we identified
- [I] **0% is largely by construction.** If PHR is scored against the enforced list, the informative results are only overhead, P_total and utility.
- [I] **"Valid" ≠ safe.** Any name on PyPI passes, including hallucinated names already squatted by attackers, typosquats and malware that has not yet been removed. This is the core slopsquatting case (RQ2). Custom allowlists are mentioned (p. 6, p. 19) but not evaluated.
- [I] **Forced substitutions are unmeasured.** When the model would emit a non-existent name, the mask forces it onto some existing name sharing a prefix. That name may be wrong, or itself a squatted look-alike. There is no relevance metric. The paper's own `google-protobuf` example (p. 6) is exactly this import-name vs install-name case.
- [I] **Cross-ecosystem confusion is only partly covered.** The definition counts wrong-ecosystem packages as hallucinations (p. 2, p. 4), but the mask checks only PyPI membership. An npm name that also exists on PyPI (e.g. the paper's `jsonwebtoken` example, p. 2) would pass if registered there; whether it is registered is not reported.
- [I] **Prompt streams differ.** Adaptive fuzzing gives each configuration different prompts: CodeLlama P_total differs by 51% (1,004 vanilla vs 1,514 PackMonitor), and CodeLlama RAG+SR yields only 231 packages, so its 1.30% PHR rests on far fewer recommendations (p. 13). There is one round per configuration and no variance.
- [I] **The HumanEval test cannot reveal harm.** HumanEval contains almost no `pip install`, and decoding is greedy (p. 16), so the intervenor never fires.
- [I] **Narrow trigger surface.** `import` lines, requirements files, version pins and flags are not covered, so an agent writing `requirements.txt` bypasses the monitor.
- [I] **Some baseline numbers appear borrowed.** The Package4U vanilla figures (16.14%, 26.28%) equal those quoted from [41] (p. 4). It is unclear whether they were re-measured; cite spracklen2024we for them.
- [I] **No CPU measurement.** Overhead was measured on A100s only; the CPU cost of the trie/DFA intersection is unknown.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Adaptive prompt streams differ per configuration. The tester reacts to target outputs.
- External (generalisability of sample/context): [V] Five open 7–8B models, PyPI only, chat setting only (p. 11, p. 19). No API models, agents or npm.
- Construct (do metrics measure the concept?): [I] PHR is measured against the enforcement list itself. "Valid" means listed, not safe, intended or correct.
- Statistical conclusion (power, multiple comparisons, variance): [V] One round per configuration, no tests or confidence intervals (p. 12–13).
- Reproducibility (data/code/setup reported?): [V] Code, hardware and temperatures are given (p. 12, p. 20). Missing: snapshot date, normalisation, RAG configuration, Package4U subset.

## 11. Future research directions
- Stated by authors [A]:
  - Extend to `conda`/`npm` and to private allowlists (p. 19).
  - Cover requirements files, Dockerfiles, CI and agents (p. 19).
  - Address executability and version compatibility (p. 19–20).
  - Refresh the list periodically (p. 19).
- Suggested by us [I]:
  - Test a vetted allowlist (minimum package age or downloads).
  - Measure the relevance of forced substitutions.
  - Use a fixed prompt set across configurations.
  - Compare with a plain registry filter.
  - Measure CPU-only overhead.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ3, RQ4, RQ5.
- How it informs our work [I]:
  - **Laptop feasibility:** it needs a locally decoded open-weight model exposing logits and tokenizer, and CPU-only operation is untested. All timings come from 8×A100 (p. 12, p. 19). DFA loading takes ≤0.25 s (p. 17), but that is host-side and does not show that 7–8B decoding is laptop-feasible. Not usable with closed APIs.
  - **What it leaves open:**
    - Names that already exist on the registry because an attacker registered them.
    - Correctness of forced substitutions.
    - Surfaces other than `pip install`.
    - npm and other ecosystems.
    - Black-box models.
  - **The cheap competitor:** a client-side registry or allowlist check gives the same "no non-existent name is installed" property without logit access. It is the natural low-compute comparison and was not tested.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Decoding-time DFA logit masking against a PyPI list (706,618 names) yields 0% PHR/RHR on 5 open 7–8B models on HFuzzer, vs residual 1.30–7.55% PHR for RAG/SR/RAG+SR (1.30% on only 231 packages) | p. 12–13 | V | moderate |
| RQ3 | RAG can raise hallucination (Qwen2.5-Coder PHR 3.25%→3.33%; Llama-3 RHR 6.40%→7.10%) | p. 12–13 | V | weak |
| RQ3 | Overhead with cached DFA ×1.07–×1.28 per response (A100 server); ×2.81–×6.24 without cache | p. 14, p. 17 | V | moderate |
| RQ3 | HumanEval Pass@1 unchanged with PackMonitor on all 5 models (temperature 0) | p. 16 | V | weak |
| RQ3 | Requires per-step logits and tokenizer of a locally decoded model; training-free | p. 3, p. 9 | V | strong |
| RQ3 | SFT checkpoints still leave 2.66% / 10.27% PHR on Package4U (vanilla values as in spracklen2024we) | p. 14 | V | moderate |
| RQ4 | Guarantee conditional on correctness/completeness of the authoritative list; list must be refreshed | p. 18–19 | A | moderate |
| RQ4 | Mask guarantees some listed name, not the intended one (import path `google.protobuf` vs install name) | p. 6 | I | moderate |
| RQ2 | Any registry-present name passes the mask, so already-squatted names are not blocked (vetted allowlists not evaluated) | p. 6, p. 19 | I | moderate |
| RQ5 | Not evaluated: requirements.txt, Dockerfiles, CI configs, coding-agent workflows, non-PyPI ecosystems | p. 19 | A | strong |

## 14. Key quotes
> "this guarantee is conditional on the correctness and completeness of the given authoritative package list" (p. 18)

> "do not yet cover broader dependency specifications such as requirements.txt, Dockerfiles, CI configurations, or end-to-end coding-agent workflows" (p. 19)

> "This list comprises 706,618 valid package names at the time of our experiments" (p. 12)

## Analyst notes
- Reading coverage: all 23 PDF pages (pp. 20–23 are references). Tables 2–7 extracted cleanly. Fig. 3 is known only from the text.
- Metadata: `rlab validate` reports MISMATCH only because the arXiv listing title differs (similarity 0.854). Crossref and OpenAlex are verified (similarity 1.0), and the DOI is printed in the PDF (p. 1).
- Uncertainties:
  - Whether HFuzzer's oracle is the same list.
  - Whether the Package4U numbers were re-measured.
  - The Package4U subset size.
  - The worst-case overhead: the text says ~0.2 s, but Table 4 gives +0.58 s (p. 14–15).
- Funding: Chinese MoE, Tsinghua–Tencent lab, Tsinghua–Keystone centre, Beijing NSF (p. 20). No conflict of interest apparent.
- Review fixes (critical review 2026-11-12) applied while `ready`:
  - Verbatim baseline quote.
  - Hallucination-definition pages.
  - Import-name caveat.
  - Laptop-feasibility wording.
  - RAG+SR package count.
  - Validate note.
