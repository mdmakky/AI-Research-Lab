# Critical review D — pass 2 (2026-11-12)

Scope: tashenova2026real, deininger2026open. Reviewer: critical-reviewer agent; report saved by orchestrator.
Result: 0 pass, 2 fix-needed. Checks: rlab validate (verified, DOI in PDF, not retracted), cite-check OK (127 / 136), ~40 numbers per paper spot-checked OK. Analyst arithmetic verified: tashenova prevalence 74.53% (A) / 46.24% (B), always-vulnerable macro-F1 0.316 (B) / 0.427 (A); deininger F1 at 1:44 always-flag 0.043, DeepSeek 0.072, CodeBERT-PrimeVul 0.147, Flawfinder r≥1 0.101 (r≥2 0.113, r≥4 0.078; Semgrep INFO 0.055); USD/TP reproduces for all 8 models.
Metadata: both metadata.json share a wrong batch added_reason (as lu2025lab); correct reasons in search/screening.md; not hand-edited.

## tashenova2026real — fix-needed
1. Frontmatter main_finding: scope "misses ~98%" to an unnamed in-house intra-procedural lexical taint analyser, not a standard SAST (p. 5, p. 13); add [I] scope note under §14 quotes.
2. §4 + RQ2 row: 50.4% / 19.3% is total reduction (conflict removal + dedup + collapse); collapse alone removed 11,123 / 3,714 records (Table 2, p. 5).
3. §7 #7 + RQ2 row: "1086 / 676 exact test copies" is [A] (p. 10); [V] = records in duplicate groups spanning folds (Table 1, p. 4), test-side share not reported.
4. §3 SAST bullet: split — [V] unnamed, no version (p. 5); [I] does not match an established PHP SAST tool.
5. §7 #11: margins vs majority baselines 0.136 (A) / 0.251 (B), 0.285 vs always-vulnerable (B); MCC ≤ 0.203 is Variant B only; Variant A MCC not reported; fold-mean vs pooled caveat.
6. §6: fold-level test unnamed, no p-value; with n = 5 a two-sided Wilcoxon cannot reach p < 0.05; only plugin-level Wilcoxon p = 0.295, d = 0.057 quantified (p. 6, p. 9).
7. COI: [V] no external funding, no COI declared (p. 14); [I] self-re-evaluation of authors' SentinelCMS (p. 2), bias runs against own earlier claims.
8. §7 #4: paper calls Bi-LSTM best neural; uni-LSTM 0.578 is (Table 5); Table 4 vs Table 5 Bi-LSTM 0.572 vs 0.573.
9. §12 G5: likely competitor Neef et al. 2026 arXiv:2606.21397 (LLMs on WordPress-plugin web vuln detection, cited by deininger p. 3) — G5 open pending check.
10. RQ1 row 1 strength → weak–moderate (single seed, ≤48.8% label precision, overlapping CIs).
Minor: §4 negatives come only from vulnerable plugins (A: patched twins), not per CVE; §9 "CodeQL does not support PHP" = outside knowledge, mark [I].

## deininger2026open — fix-needed
1. §7 #11 + RQ3 row: Table 5 kJ/TP for Qwen (4.0) and Llama (44.8) use FLOP estimates (40 J, 944 J; Table 8 p. 14), not measured Table 4 values (88 J, 738 J) → measured ≈ 8.8 / 34.9 kJ/TP [I]; Gemma 3.7 uses 64 J estimate, measured c=1 84.4 J → ≈ 4.9.
2. §4 truncation: [A] non-LLM baselines untruncated (p. 4) vs CodeBERT 512-token truncation (p. 6); [I] applies to SAST only; CodeBERT disadvantaged, strengthens its win.
3. Precision "2.3–3.8%" is first epoch (Table 5); budget-matched epoch 2.8–4.6% (Table 11, p. 17) — fix everywhere (main_finding, §7 #8, §12, RQ1 row).
4. RQ1 SAST row: only Flawfinder (6.2–13.4%) and Semgrep (26.0% [5.7–66.9]) beat every LLM on precision; Cppcheck 2.46–3.77% in LLM range (Table 7 p. 10); Semgrep vs CodeBERT CIs overlap.
5. §9 reasoning multiplier: p. 24's 2.5–7.6× refers to Section 4.9 earlier epoch, no cost table (unverifiable); cite Table 12 4.5–12.1× (p. 18).
6. §9 AI-assistance: quote p. 27 accurately (DeepL + ChatGPT GPT-5.5 for translation; Claude Opus 5 / Sonnet 5 for drafting/revising text and Python code; no AI-generated figures/data); two evaluated vendors; code covered by 82 tests (p. 6); [I] our pipeline is Claude-based.
7. Funding/COI: [V] State of Styria PRISMA ABT12-270413/2024 (p. 26); TU Graz OA fund; no COI declared (p. 27).
8. §4: 24,788 / 549 (1:44) differs from PrimeVul test split 695 / 25,216 recorded in ding2025vulnerability; unexplained ("after loading").
9. §7 #11: "human triage not included" → [I] (p. 8 only says "No triage workflow absorbs that").
10. §9: contamination (p. 24) and in-distribution vs zero-shot asymmetry (p. 11) are author-stated → §8 [A].
11. §1: non-verbatim quote → "We make no claim to be first on any single one of these axes" (p. 3).
12. §9 inconsistencies: add p. 2 "roughly twenty-six false alarms" (Table 5: 25.6–41.9) and p. 23 "dominate … on both quality and efficiency" vs p. 21 / Family C p = 0.081 (p. 17).

## Cross-paper (for evidence matrix)
- deininger evaluates unpaired functions; don't pool with pair-wise results (ding P-C, tan2026think). RQ1 "near/below chance on PrimeVul" must keep "pairs".
- C1 extension: fine-tuned CodeBERT beats all 8 LLMs (deininger) vs ding's GPT-4 CoT > fine-tuned on pairs; [I] argmax-collapse (p. 11) consistent with ding's P-B 84–88%.
- G1/C5 agreement at ~2% prevalence: deininger, lu2025lab, yildiz2025benchmarking — LLMs barely above flag-all. Tension [I]: deininger CodeBERT-PrimeVul (chronological split) holds bal. acc. 0.765 vs lu temporal DL collapse.
- G1: trivial baselines competitive in tashenova (length baseline), shu2026evaluating, deininger.
- Label quality: tashenova 48.8%, risse2025top 39–65%, ding 24–36% older datasets; PrimeVul 86–92% outlier.
- C3: deininger fits "LLMs higher recall, SAST higher precision but finds little".
- C4: deininger DeepSeek reasoning lowers specificity 0.52 → 0.37 (p. 17, p. 20) — model-dependent.
- Gap report: G2/G6 "No SAST" wrong; G5 + threats "abstract only" stale; G5 novelty check missing Neef et al. 2026 (arXiv:2606.21397); G2 check maybe Dahiya et al. 2026 (arXiv:2605.23243).
