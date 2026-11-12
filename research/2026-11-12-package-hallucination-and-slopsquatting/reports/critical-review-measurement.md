# Critical review — measurement analyses (batch 1)

- Date: 2026-11-12 · Reviewer: critical-reviewer agent (returned as text; saved by orchestrator)
- Scope: spracklen2024we, churilov2026range, okwor2026hallucination, krishna2025importing, zhao2025hfuzzer, haque2025secure, zheng2026when, dasu2026refusing, zhang2025llm
- Result: 0 pass · 8 pass-with-minor-fixes · 1 fail (okwor2026hallucination, provenance only). cite-check OK for all 9; `rlab validate` verified 8, okwor MISMATCH.

## Verdicts and fixes (summary; full fix text was sent to the analysts)

| key | verdict | fixes |
|---|---|---|
| spracklen2024we | minor | 3.59%/13.63% "overall" are Python-only (Table 7, p. 20; JS 4.00%/27.45%); 5.2/21.7/15.8/21.3% are unweighted means of per-test rates, only 19.7% pooled; RQ2–4 sampling statement is [A], some analyses use all 16 models (pp. 8, 10); fine-tuning H1/H2 labels = H2/H3 by own definitions; data release is a promise (p. 14), confirmed by churilov; top-k/min-p only DeepSeek and CodeLlama (p. 8); funding UTSA FDL + NSF 2231002 (p. 14); venue: tier 1 USENIX Security '25 (supported by churilov p. 1, 16; okwor p. 9), analysed from arXiv v3 |
| churilov2026range | minor | "level with Spracklen's best" compares pooled Py+JS with Python-only 3.59%; Gemini/DeepSeek/GPT-5.4-mini non-significant only at mention level (Table 4, p. 8); prompt-source ordering reverses Spracklen on the same corpus; funding/COI (p. 15); released corpus 39,969 prompts (p. 4) vs Spracklen's stated counts |
| okwor2026hallucination | fail → fixable | provenance: printed DOI …427 is the version DOI, metadata …426 the concept DOI of the same Zenodo deposit (resolved 2026-11-12); Crossref has no record (DataCite). npm-mirror claim is [A] (p. 3) partly supported (p. 7); single-operator attribution is [A] (evidence withheld, p. 6); 11-name scope (p. 7); add secondary [A] claims huggingface-cli / npm example (p. 2); code is promised (p. 8); justify tier choice |
| krishna2025importing | minor | not the only Rust study (zheng2026when, dasu2026refusing); N = 455 per cell inferable from Table 3 multiples; size correlation depends on guessed 200B GPT-4o (Table 1, p. 3); lowest Python Dracarys 2.42% |
| zhao2025hfuzzer | minor | PyPI "last accessed Mar. 2025" ref [13] (p. 12) as registry-date proxy; split [V]/[A] in RQ4 row; move proposal out of RQ3 row; temperature is tester-model temperature (p. 10) |
| haque2025secure | minor | "mostly URL" is [A] (p. 6); in the one table, 51% URL vs 49% file paths/free text (Table 2, p. 8); PHR overstates squattable names [I]; label inferred single pass [I] |
| zheng2026when | minor | Internetware acceptance unsourced → Analyst notes; `-`/`_` normalisation not reported; edit-distance units not comparable with Spracklen; quantization caveat applies to all open models |
| dasu2026refusing | minor | planted names are not evidence of spontaneous repetition; 18% "factual" not a slopsquatting risk; misspelled names fabricated 14% (p. 8); per-group model counts (Table V, p. 6) |
| zhang2025llm | minor | venue is PACMSE 2(ISSTA): 481–503 (cited by zheng p. 11, dasu p. 11); published OA version exists but not analysed (replacing paper.pdf needs user permission); `_lfu_cache` not a valid PyPI name |
| (all B-group) | format | use bracketed [V]/[A]/[I] everywhere; label §2 RQ lines [A] and §6 metric lines [V] |

## Cross-paper notes for the evidence matrix

**A. Rate units — never pool or rank across papers.** spracklen2024we: mention-level (pools install commands with model-queried lists; only 19.7% pooled). churilov2026range: mention- and generation-level, live registry, time-of-generation rule. krishna2025importing: per prompt, N = 455 per cell, regex imports, no mapping/stdlib filter, date-aware definition. zhao2025hfuzzer: per response on fuzzer-optimised tasks (not a base rate). haque2025secure: per Go package string (~half file paths/free text). zheng2026when: per source-level crate reference, 45.47% std/module confusions. dasu2026refusing: acceptance of a planted name (different construct). okwor2026hallucination: no rate. zhang2025llm: category shares only.

**B. Extraction method.** Model-queried: Spracklen H2/H3, Zhao. Install-command parsing: Spracklen H1, Churilov, Haque. Import parsing: Churilov (pipreqs ~1,157 names), Okwor (mapping source unreported), Krishna (none), Zheng (`-`/`_` unreported). Spracklen rejects import parsing yet Churilov claims to follow it (p. 5) → 2024→2026 comparison not like-for-like.

**C. Contradictions.** (1) Language: Spracklen JS > Py; Krishna and Churilov Py > JS — [I] likely extraction (import names). (2) Prompt source on the same corpus: Spracklen SO > LLM-generated; Churilov LLM-generated > SO — cleanest contradiction. (3) Model size: Krishna larger better (pseudo-replicated n = 33); Zheng no effect; Dasu small effect; Churilov Haiku < Sonnet; Zhao Llama-3.1 > Llama-3. (4) Temperature: Spracklen rises above 1; Zheng no effect 0–2 (Rust). (5) Edit distance: different units (unique vs occurrence-weighted). (6) Cross-model overlap: mostly model-specific with a persistent shared core (Spracklen 81% single-model; Churilov 104 universal names, Jaccard 0.219; Okwor 450/455 single-model). (7) RAG effect: Python large (Spracklen) vs Rust negligible (Zheng).

**D. Real-world registration (RQ2).** Churilov 25/2,282 registered in ~6 months, 1 with malware, 23 names with malware history; Okwor 0/1,641 after 4 days, 22/149 public names registered, 0 malicious, 19 defensive placeholders. Compatible, not contradictory.

**E.** Do not reuse Okwor's secondary numbers (misreports Spracklen units, quotes superseded Churilov v1–3).

**F. Hidden quantization confound:** Spracklen GPTQ for all open models; Dasu 4-bit ≤32B; Zheng unreported; Haque explicit.

**G. Independence/venues:** Churilov reuses Spracklen's prompts. Peer-reviewed: spracklen2024we, zhao2025hfuzzer, zhang2025llm. No paper in this batch measures agentic tools that install dependencies automatically (novelty check needed).
