# Critical review — defences, tool-side and background analyses (batch 2)

- Date: 2026-11-12 · Reviewer: critical-reviewer agent (returned as text; saved by orchestrator)
- Scope: liu2026packmonitor, djire2026evaluating, liu2026mitigating, spracklen2026llm, raj2026names, mirandapena2026empirical, twist2026library, ohm2020backstabbers
- Result: 0 pass · 7 pass-with-minor-fixes · 1 fail (mirandapena2026empirical). cite-check OK; validate MISMATCH for liu2026packmonitor, raj2026names (explained below).

## Fixes per key

### liu2026packmonitor (minor)
1. Analyst notes: record "rlab validate: MISMATCH only because arXiv listing title differs (similarity 0.854); Crossref + OpenAlex verified; DOI printed in PDF (p. 1)".
2. §3 baselines: use verbatim p. 11 wording "Following prior work on mitigating package hallucinations [41], we include three representative baselines" or drop quote marks.
3. §5 hallucination decision: definition is on p. 2 ("non-existent packages") and p. 6 (official registry snapshot / curated allowlist), not p. 12. Add [I]: the paper's own example is import-path vs install-name confusion (google.protobuf vs google-protobuf, p. 6); the mask only guarantees some listed name.
4. §12: "needs logits but no GPU" is unsupported. Replace: "[I] Needs a locally decoded open-weight model exposing logits and tokenizer; CPU-only operation untested; timings from 8×A100 (p. 12, p. 19); DFA loading ≤0.25 s (p. 17) is host-side and does not show 7–8B decoding is laptop-feasible."
5. §7 finding 1: RAG+SR on CodeLlama 1.30% PHR comes with only 231 recommended packages vs 1,004 vanilla (p. 13) — add here and in §9.

### djire2026evaluating (minor)
1. §9 third bullet: remove the CD accusation — CD is below Vanilla in 19/32 cells (Table 4, p. 7) and lowest in none (p. 6); both true. Replace Nudging point with: "[I] The conclusion calls Nudging the best trade-off 'among the guided decoding strategies' (p. 11), though the paper counts Greedy as guided (p. 2) and Greedy has the best trade-off (p. 8)."
2. §9 first bullet: "Abstract '18 of 32' (p. 1) matches neither the 24/32 reductions nor the 19/32 'lowest' count derivable from Table 4 (p. 7)."
3. New §9 [I]: p. 6 says RAG does not increase PHR for any model in Python/Ruby/Rust, but Table 4 shows mistral-7b Rust 18.6 → 20.8 (p. 7).
4. §3 Nudging: add [I] that for 5 of 8 models the surrogate (largest in family) is the model itself (p. 3); unexplained (p. 5).
5. §4: Table 3 counts (1,470–32,337) are "per model–language cell under vanilla decoding".
6. §13: split the guided-decoding RQ3 row into [V] (DoLa 38.0% avg; syntax errors) and [I] (white-box access needed); relabel the RQ5 "latency not reported" row as [I].
7. §5: add [I] code-gen imports are "validated against the same registry snapshots" (p. 6); unregistered import names like cv2 probably count as hallucinations, inflating Fig. 1.

### liu2026mitigating (minor)
1. Frontmatter main_finding: "Valid-Rate rises on average (+6.4% edit) but falls 7% for Qwen3 on unseen prompts (0.7990 → 0.7434; Table II, p. 7); HumanEval within ±2% (Table VI, p. 9)."
2. §13 cost row: "per edit run (unit undefined), averaged across models" (Table V, p. 9).
3. §5 cost: add DINM (edit 11.97 s, localization 0.92 s) and ROME test time 10.86 s (Table V, p. 9); "lower than ROME, MEMIT, Full-FT" holds only because DINM is omitted.
4. §7: Full-FT beats BOUND on DeepSeekCoder Edit50 (Package-HR 0.0188 vs 0.0745; Valid-Rate 0.9500 vs 0.9480; Table II, p. 7) — qualifies "best overall balance".
5. §9 [I]: edit cases use the model's own hallucinated names (p. 5); unseen prompts come from the same pool; "unseen" generalisation may partly be suppression of memorised names; overlap not reported.

### spracklen2026llm (minor)
1. §9 [I]: "surgical" overstated — GA on DeepSeek-7B reaches 7.2% HR with unchanged utility (Avg 66.95 vs 66.98) and code KL 0.0031 vs AU 0.0796 (Table 1, p. 10); on 16B GA keeps Avg 77.35 vs AU 73.17. Trade-off, not dominance.
2. New §9 [I]: tuning/checkpoint selection favours AU — AU LR 5e-5 (7B), 2e-5 (16B) vs GA/NPO 1e-5; GA/NPO report final checkpoint, AU/CE-only/NPO-only a selected one (Table 3, p. 19).
3. §9 inconsistency: Appendix D says 16B AU is a restart at checkpoint 60 (p. 18); Table 3 says "50 restarted" (p. 19). §5 must not state "checkpoint 60" as fact.
4. §7 finding 3: HumanEval 16B drops 81.1 → 73.2 under AU while GA keeps 79.9 (p. 10).

### raj2026names (minor)
1. Source tier/notes: "rlab validate: MISMATCH (arXiv and OpenAlex agree; Zenodo DOI not in Crossref); PDF identity probable (only 'Version: v1, arXiv, August 2026', p. 1)."
2. §5/§9: stdlib handling not reported (extractor keeps all top-level imports, p. 5; any 404 = fake, p. 5). [I] directly affects give-up rates.
3. §7 finding 4: add paper evidence — reconciler maps pil → Pillow (p. 7) but pil returns 200 so the reconciler cannot fire (p. 5); flagged 36 times as squat (Table 3, p. 8); pkg-resources listed as invention (p. 8); faiss counted as hallucinatory variant in bait test (p. 11).
4. §13 RQ4 row "give-up 79% → ~29%": strength weak; different overlapping prompt sets (70, 58, 60, 300; Table 1, p. 7).
5. Optional §9 [I]: paper attributes the term "slopsquatting" to Spracklen et al. (p. 2) without support; 3-item reference list (p. 15).

### mirandapena2026empirical (FAIL)
1. §7 finding 6, §13 RQ3 row, main_finding, §12: wrong RIF claim. Table 5 (p. 10): RIF falls on DS-1000 for all models and repair methods (claude-3 9.1 → 2.7, Gemma2 22.3 → 8.1, Qwen3 25.4 → 6.1), roughly flat on BigCode, rises on Odex for small models (Qwen3 31.3 → 55.6). Correct to "[V] … (p. 10). [A] The authors summarise this as 'no improvement in most cases' (p. 10), which overstates the table."
2. §9/§7 finding 1: abstract "14–85%" = Pyright IFR range (Table 10, p. 20). "16–70%" and "8.1–40%" could not be matched (Pyright all-error recall 0.16–0.82, p. 6; no-repair RIF 8.1–44.9, p. 10).
3. §13 RQ4: "≈27–30% (Odex 30.3%, BigCode 26.6%) of sampled hallucinations; authors say 'over 30%' (p. 9)" (Table 3, p. 8).
4. §7 findings 2/3 and §13 row 1: detection range is recall; correct-for-the-right-reason (TP) only 37.6% DS-1000, 4.0% Odex, 10.0% BigCode (Table 2, p. 8).
5. §9: "Package-level causes are a small share (Library category 14.7/6.6/6.0%, p. 8); detection metrics not broken down by it."
6. Tier: orchestrator decision 2026-11-12 — keep preprint tier (TMLR acceptance is an arXiv-comment author claim; no DOI/OpenReview record verified).

### twist2026library (minor)
1. §3/§12: PyPA normalisation only folds case and -_. ; cannot map dateutil → python-dateutil or cv2 → opencv-python; dateutil corrected manually (p. 15); false positive pywintypes (p. 15). Add [I]: check effectively tests whether the import name exists on PyPI; third-party-registered import names count as valid. Replace "Adopt the PyPI name normalisation" with "adopt normalisation plus an explicit import→distribution map".
2. §4: "one response per task" unsupported — p. 7 "same experimental setup used previously" implies three; remove or mark "not stated".
3. §5: JS validated against all-the-package-names (jsDelivr, 2026), Rust against Cargo registry (p. 20), snapshots undated; "January 2026 snapshot" only for the rarity top-PyPI list (p. 19).
4. main_finding: "one-char typos up to 26%, multi-char up to 79% (79.44%, p. 6), fake names up to 99%".

### ohm2020backstabbers (minor)
1. Tier: "Tier 2 (LNCS proceedings chapter per metadata); used as background because it predates LLMs, not because of source quality."
2. §7 finding 5: data exfiltration 55% (pp. 16–18).
3. §12 RQ2: add [V] some typosquats have Levenshtein distance 0 by reusing a name from another repository (python-sqlite from apt, p. 12) — pre-LLM analogue of cross-ecosystem/import-name confusion.

## Cross-paper notes for the evidence matrix

**A. Hallucination decision (do not pool rates).**

| key | ground truth | snapshot | stdlib | names checked | registered-but-malicious |
|---|---|---|---|---|---|
| liu2026packmonitor | PyPI list 706,618 names (p. 12, 19) | not reported | n/a (pip install args) | pip install args | valid |
| djire2026evaluating | registry ∪ stdlib manifests (p. 3–4) | 2026-03-04 | Py/Ruby corrected; JS/Rust unclear (p. 5) | recommended names; code-gen imports, mapping unstated | valid |
| liu2026mitigating | on PyPI and ≥1 release before model cutoff (p. 5) | ~2026-06-14; cutoffs unreported | not reported | recommendations; code-gen imports mapped by base LLM (p. 7) | post-cutoff counts as hallucinated (only paper) |
| spracklen2026llm | static PyPI snapshot (p. 20) | not reported | not reported | pip install lines + model answers (p. 8) | valid; oracle poisoning flagged (p. 12) |
| raj2026names | live PyPI JSON; 404 fake, 200 → classifier (p. 5) | live, undated | not reported | AST imports + pip install | flagged if metadata suspicious |
| mirandapena2026empirical | installed env + builtins (p. 4, 18) | n/a | builtins allowed | imports/members at runtime | not addressed |
| twist2026library | PyPI + PyPA normalisation (p. 4); npm list; crates (p. 20) | not reported | not reported | AST import names | valid |

- Import vs install names: Twist counts registered import names valid; Raj flags registered import names (pil, faiss, skimage) as squats; Djire code-gen and Twist probably count unregistered import names (cv2) as hallucinations → method-driven contradiction (RQ4).
- Stdlib: only djire2026evaluating quantifies the inflation (+7.6 to +9.4 pp Python, p. 5).
- Release-date cutoff: only liu2026mitigating; all others score post-training registrations (incl. attacker squats) as correct → undercounts exploitable names (RQ2).

**B. Defence access and hardware (RQ3/RQ5).** PackMonitor: white-box logits, 8×A100 (p. 12), CPU untested. Greedy/RAG/Self-Refine (djire): black-box, "single GPU", no latency. CD/DoLa/ALCD/Nudging: logits/hidden states. BOUND: weights + LoRA training, 8×A100 (p. 6). Adaptive unlearning: full fine-tuning, MI210/MI300, 12–24 h (p. 8, 19). raj2026names: black-box, PyPI API + small RF; API models (Groq), no local inference. mirandapena2026empirical static tools + grammar: CPU; grammar decoding via local llama.cpp on M2 24 GB (p. 17), +12 s/request (p. 11) — the only laptop-class run. twist2026library prompting/PyPI tool: black-box, API. ohm2020backstabbers: user-side pinning, disable install scripts (p. 16).

**C. Dependencies and contradictions.** PackMonitor's Package4U SFT numbers are quoted from spracklen2024we — cite the original. liu2026mitigating shares authors with zhao2025hfuzzer; PackMonitor uses HFuzzer as benchmark — not independent groups. RAG unstable in both studies (PackMonitor p. 12–13; Djire JS +12.7 pp, p. 6). Self-refine with registry feedback (liu2026mitigating p. 5) vs unreported (djire) — not comparable. User-supplied fake names (djire 46.6–92.5%, p. 9; twist 20.7–99.2%, p. 6; raj bait 6/10 or 9/10) measure compliance, not spontaneous invention. Relative reductions (−65.4%, −88%) are on hallucination-heavy selected prompts; report absolute residuals. Utility evidence weak everywhere. Persistence evidence thin in this batch (only raj2026names, p. 10).
