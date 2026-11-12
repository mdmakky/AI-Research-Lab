# Critical review C — pass 2 (2026-11-12)

Scope: qin2026review, lu2025lab. Reviewer: critical-reviewer agent; report saved by orchestrator.
Result: 0 pass, 2 fix-needed. Checks: rlab validate (both identity match), cite-check OK, all key-finding numbers grepped against fulltext.txt, qin Figs 1–2 rendered, qin PrimeVul ranges checked against ding2025vulnerability Table V (p. 7) — all six match.

Orchestrator verification (2026-11-12): Crossref confirms lu2025lab published as "From lab to reality…", Lu & Lagaisse, Journal of Systems and Software, Nov 2026, doi 10.1016/j.jss.2026.113185 (Elsevier licence, not OA). Decision: keep arXiv v4 (accepted manuscript, footnote p. 1) as page source and record the JSS DOI in the analysis; no second registry entry (would duplicate the paper).

## qin2026review — fix-needed
1. §5 l.49: PrimeVul Table V re-report labelled [V] and "re-analysis" → [A] re-report; [I] all six ranges match [@ding2025vulnerability, p. 7]; cite ding directly.
2. §13 row 2: strength moderate → weak (secondary; cite ding p. 7).
3. §4 l.44: Table 1 lists 12 methods (8 LLM-based), not 11 (pp. 6–7); ~16 of 32 refs are LLM detection/evaluation studies.
4. §7 f.5 l.61: ref [1] is on p. 14; [1] is SAST-only; the sole LLM-vs-SAST source [15] = gnieciak2025large reports LLMs above SAST on F1 (0.75–0.80 vs 0.26–0.55) — qin omits this; cite gnieciak directly.
5. §12 l.92: "corroborate independently" wrong — qin cites ding [14], gnieciak [15], sheng [21]; not independent.
6. §7 f.4 l.60: Table 2 is a normative risk matrix → [A] (pp. 10–11).
7. §2 l.35 / §9 l.77: "internally inconsistent" overstated → framing Qs (p. 2) vs formal RQs (p. 4) not reconciled; "C2" (p. 12) undefined.
8. Header l.21: flag venue (Zeus Press; peer review not documented; low-visibility).
9. §10: add source-dependence threat (quantitative claims rest on ding and gnieciak, both in our corpus).

## lu2025lab — fix-needed
1. Venue (l.21, §9 l.83, notes l.122): published JSS 2026 (doi above); page refs = arXiv v4; status peer-reviewed.
2. §9 l.77: chance baseline — p = 263/13,326 = 1.97% → all-positive F1 = 3.87%; DL F1 3.47–8.65 (Table 7 p. 13) ≤4.8 pts above; 7 of 12 LLM conservative F1 (Table 8 p. 14) below it.
3. §4 l.46 / l.124: Table 7 A/P/R back-calculation: LineVul rows imply 1.97% (= 263/13,326, drop the "assume" caveat); ReVeal rows imply 1.79% on its processable subset → all-positive F1 ≈ 3.5%.
4. §7.5 l.63, §12 l.97–98, §13 row 5: name the metric; PACC (≤5.75%) far below random q(1−q) (up to 25%) — models label vulnerable and patched versions alike [I].
5. §7.5 / §13 row 4: "same data" → ReVeal on processable subset (p. 7), few-shot excludes demos, valid-only subsets (p. 8); add best DL 8.65 (~2.5× its chance) vs best LLM 5.36 (~1.4×) [I].
6. §13 strengths: justify moderate (now peer-reviewed; consistent with ding/chakraborty) or weak; rescope row 5 to "evaluated DL detectors and four open-weight LLMs ≤32B".
7. §7 f.1 l.59: unlabelled inference → [A] (p. 11).
8. §3 l.41: k = 4 given "for example" (p. 8); actual k not stated.
9. §5 l.56 / §9 l.80: DL runs/seeds not reported; LLMs one deterministic run (temp 0, seed 42, p. 8).
10. §10/notes: COI — ICVul is the authors' own dataset (p. 3; refs pp. 18–19); funding not reported.
11. §10 Internal: unchecked overlap of VentiVul unchanged functions with BigVul/ICVul Linux/Chromium code and LLM pretraining (pp. 3–4).
12. §9 l.81: "many" → up to 63 multi-function CVEs (263 pairs / 200 CVEs, p. 4); share needing cross-function reasoning not reported.
13. §10 Repro l.90: templates given (Table 4 p. 9); system prompt paraphrased; demonstrations not listed.
14. main_finding l.9 / §12 l.98: VulBERTa 94.14 not run on VentiVul → "LineVul F1 91–94.5 → 4.39–6.87 (all 8 configs 3.47–8.65)"; "direct evidence, consistent with ding2025vulnerability".
15. §7 f.8 / §13 row 7: add "(LLMs: zero-shot, valid-only, p. 13)".
16. §8: add authors' limitations (incomplete coverage, model coverage, Function-Pair less noise-exposed, p. 17).

## Cross-paper (for evidence matrix)
- New contradiction C7: CodeBERT/LineVul BigVul in-distribution F1 91.00 [@lu2025lab, p. 12] vs 62.88 [@ding2025vulnerability, p. 7]; [I] likely split/preprocessing differences.
- Agreement: BigVul-trained models collapse on newer/cleaner data (ding BV→PrimeVul F1 1.91–5.82 p. 7; lu LineVul(BigVul)→VentiVul 6.87 p. 13) — read against chance.
- Double counting: qin is not independent support for RQ1/RQ2.
- Qin vs gnieciak: qin omits that LLMs outscored SAST in its sole head-to-head source.
