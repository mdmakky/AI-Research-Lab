# Critical review, batch C (2026-11-12)

Project: 2026-11-11-ai-reverse-engineering-vibe-coding
Keys reviewed: bai2026recreationworld, xiong2026propgen, chen2025iwr
Reviewer: critical-review subagent. No `analysis.md` was edited.

## Checks run

| Check | bai2026recreationworld | xiong2026propgen | chen2025iwr |
|---|---|---|---|
| `rlab validate` | could not run: `pdftotext not found` (poppler missing on this machine) | same | same |
| metadata.json verification | verified (OpenAlex), identity "arXiv id printed in PDF", not retracted | verified (OpenAlex), identity "DOI printed in PDF", not retracted | verified (arXiv), identity "arXiv id printed in PDF", not retracted |
| Preprint flag | preprint, flagged in the analysis | published (ASE '26). PDF is arXiv v2 with the camera-ready header. Correctly described | preprint, flagged in the analysis |
| Published version | Crossref search 2026-11-12: none found | n/a | Crossref search 2026-11-12: none found |
| `rlab cite-check` | OK (101 citations) | OK (77 citations) | OK (69 citations) |
| RQ ids exist in RESEARCH-QUESTIONS.md | yes (RQ1-RQ5) | yes | yes |

Because `rlab validate` failed for a tooling reason, PDF identity could not be re-confirmed in this review. It rests on the recorded `fulltext.identity` field. Install poppler and re-run `rlab validate` before these analyses are marked `complete`.

Items spot-checked against `fulltext.txt`: bai, 31 numbers (Tables 2, 3, 4, 11, 12; pp. 9, 11-18, 28-31, 38-39, 46-47). xiong, 26 (Tables 1-5, kappas, costs, RQ4 counts). chen, 30 (Tables 1, 3-6, Appendix C, prompts).

Answers to the analyst's flagged points:
- **chen per-category counts**: the arithmetic is right (7.96% x 113 = 9.0; 10.62% x 113 = 12.0) and it is labelled [I]. Fine as is. See C1 for a bigger problem with the same tables.
- **bai 13.64% implies 44 tasks**: labelled [I], which is correct. 6/44 is not the only possible fraction (3/22 also gives 13.64%). Add the supporting evidence the paper does give (B4).
- **bai scrape penalty on case scores**: this can be resolved further than the analysis says. Ablira was *detected* (p. 47), yet its reported channel scores (72.73/40.79) are far above the 0.10 cap, so the case table shows pre-penalty channel scores (B3).
- **xiong kappas**: 0.91 / 0.82 / 0.81 match p. 7 exactly. The column interleaving did not garble them.
- **83.8%**: this figure is in **bai**, not xiong (p. 15-16, "83.8% place a larger share of source in the single largest file"). It is correct. The xiong analysis contains no 83.8% figure.

---

## bai2026recreationworld — verdict: **needs-fixes** (10 fixes)

**B1 (serious, factual error). §7 Key finding 1.**
- Current: "Grok 4.6 is lowest (9.15) — [V] (p. 11)".
- Problem: the column headers of Table 3 are scrambled in the text layer. The column with 9.18 / 9.12 / 9.15 is **Qwen3.7-Plus**, not Grok 4.6. Evidence:
  - Figure 1 (p. 1) lists the models in descending five-platform mean: GPT-6 Astra, Claude Opus 5, GPT-5.6 Sol, **Grok 4.6**, Qwen3.8-Max-0902, Kimi K3, Claude Opus 4.8, GLM-5.3, Gemini 3.7 Flash, **Qwen3.7-Plus**.
  - The scaffold labels in Figure 1 match Table 8 (p. 28): Grok xhigh, Qwen3.7-Plus "enabled".
  - Read in that order, the Table 3 averages are strictly descending: 58.06, 44.16, 42.06, 36.73, 34.80, 31.41, 31.10, 24.38, 21.12, 9.15.
- Correct text: "...then Claude Opus 5 (44.16) and GPT-5.6 Sol (42.06); Grok 4.6 is fourth (36.73) and Qwen3.7-Plus is lowest (9.15) — [V] (p. 1, p. 11)."
- Knock-on edit to §9 COI: "[I] Qwen3.7-Plus, which is also the VLM judge (p. 9), is the lowest-scoring evaluated model (VLM 9.12, average 9.15, p. 11). So no favourable self-scoring is visible, but judge self-preference was not tested."

**B2 (serious, scope). §7 findings 4, 5, 7; §12; §13 RQ3 rows.**
- Current: "Rebuilt apps are much smaller... 89.4%...", "Claude Opus 5 has the highest median recreation LOC on all five platforms, while GPT-6 Astra has the lowest on four of five", "final edit -> relaunch -> inspect ... 23.6-47.5% of trajectories". All are presented as general findings.
- Problem: the trajectory and artifact analyses cover only **4 of the 10 models**: Claude Opus 5, GPT-6 Astra, GLM-5.3 and Qwen3.8-Max-0902 (Figure 10 legend p. 12; "for the four models analyzed above", p. 15).
  - The reference-size comparisons cover native platforms only (p. 15).
  - "Coverage varies across model–platform cells" (p. 15), and the denominators are not given.
  - "Highest/lowest LOC" therefore means highest/lowest among four models.
- Correct text: add to findings 4, 5 and 7, and to the RQ3 evidence rows: "(four models analysed: Claude Opus 5, GPT-6 Astra, GLM-5.3, Qwen3.8-Max-0902; desktop and Android only for reference comparisons; per-cell coverage not reported) (p. 12, p. 15)". In finding 5: "...the highest median recreation LOC **among the four analysed models**...".

**B3 (serious, misreported integrity evidence). §7 finding 8; §9 "Score integrity gap"; §13 RQ4 row "scraped-content replay can earn substantial scores"; Analyst notes uncertainty (4).**
- Current: "Two Web cases replayed scraped reference content yet scored 72.73% and 54.82% Prog, one escaping the detector"; "whether the 0.10 scrape cap (p. 38) was applied to those reported case scores ... is not reported".
- Problem: the paper says the detector **caught** Ablira ("source-level class-provenance and scrape-mechanism checks catch Ablira's bulk replay", p. 47). A SCRAPE verdict replaces the task aggregate with min(s, 0.10) (p. 9, p. 38).
  - Ablira's reported 72.73 Prog / 40.79 VLM (p. 39, p. 46) are therefore pre-penalty channel scores. Its penalised aggregate would be at most 0.10. This is [I], but it follows directly from the stated rule.
  - Only Kartova (54.82 Prog / 14.63 VLM / 34.72 average, p. 47), which escaped the detector, shows a replay that kept a real score.
  - As written, the RQ4 row overstates the integrity gap.
- Correct text, finding 8: "Two Web case studies replayed reference content. Ablira (72.73% Prog / 40.79% VLM, p. 46) was caught by the scrape detector, so the 0.10 aggregate cap applies (p. 38, p. 47); the table shows its pre-penalty channel scores [I]. Kartova escaped detection and kept 54.82% Prog / 14.63% VLM (34.72% average) (p. 47) — [V]."
- RQ4 row: "A transformed replay evaded the scrape detector and scored 54.82% Prog (p. 47); detected replay is capped at 0.10 (p. 38) | 38, 46, 47 | V | weak". Update analyst note (4) to match.

**B4 (moderate, unsupported inference needs its evidence). §9 "Unexplained denominators"; Analyst notes (3).**
- Current: "13.64% (p. 30), consistent with 6 of 44 rather than 50 tasks, suggesting some runs were excluded as invalid".
- Problem: the [I] label is right, but the inference skips an alternative and leaves out the support the paper gives.
  - 13.64% equals 6/44 and also 3/22. With 50 tasks, every value would be a multiple of 2.00, as all other cells in Table 11 are (p. 30).
  - The paper states that a failed isolation check "invalidates the run rather than lowering the model's score" (p. 9). Quality metrics use "evaluator-valid" pairs (p. 11, p. 38), and the paired Bash comparison covers "249 application–platform pairs" (p. 20). So exclusions exist, but their number is never reported.
- Correct text: "[I] Claude Opus 5's Web Prog >= 90% of 13.64% (p. 30) cannot come from 50 tasks; it fits 6/44 (or 3/22). The paper invalidates runs that fail isolation checks (p. 9) and reports evaluator-valid subsets elsewhere (p. 11, p. 20), so some runs were probably excluded. The number of excluded runs per model and platform is not reported."

**B5 (moderate, missed evidence on run count). §5 "Rollouts per task per model in the main benchmark: not reported"; §9 "No variance"; frontmatter `sample_size`.**
- Problem: the statement is literally true, but the paper gives indirect evidence. The direct-MCP arm of the Windows / Claude Opus 4.8 comparison is "one rollout per task" (p. 11, p. 38). Its scores (Prog 35.05, VLM 31.00, Figure 9, p. 11) are identical to the Table 11 Windows / Claude Opus 4.8 entries (35.05 / 31.00, p. 30).
- Correct text (add to §5 and §9): "[I] The main benchmark is probably a single rollout per task. The one-rollout direct-MCP arm (p. 11) reproduces the Table 11 Windows / Claude Opus 4.8 scores exactly (p. 30). This is not stated explicitly."

**B6 (moderate, missing appraisal of the transfer experiment). §7 finding 9; §9; §12.**
- Problem: the analysis records the authors' "exploratory" caveat but does not appraise the design.
  - Gains are measured against "each run's first evaluated checkpoint", not the untrained initialisation (p. 3, p. 6).
  - There is no control arm, such as SFT on equally long non-recreation agent trajectories, so the effect of recreation data cannot be separated from any SFT on agentic trajectories.
  - Each OOD benchmark is run once per task per checkpoint (p. 6, p. 28).
  - Curves are non-monotonic (p. 6), and the gain reported is the last-vs-first difference, with no uncertainty.
- Correct text, new §9 bullet: "[I] **Transfer design is uncontrolled.** Improvements are measured from the first evaluated checkpoint (p. 6), with one trial per task (p. 28) and no control SFT mixture. Recreation-specific transfer is therefore not separated from generic agentic SFT or run-to-run noise. 'Gains up to 17.9 points' (p. 3) is a single best-case difference."

**B7 (labels). §13 evidence table.**
- Rows labelled V that are our appraisal of absences or confounds:
  - "RQ4 | No CIs or repeated runs for main scores; judge accuracy and reviewer agreement not reported; model and scaffold confounded"
  - "RQ5 | ... maintainability ... assessed only through size and structure proxies"
- Required: label both **I**, with the basis (p. 11, p. 28; p. 15-16). The paper does not state the RQ5 proposition. The authors' own framing ("architectural substitution rather than implementation quality", p. 16) can be cited as [A].

**B8 (hedging of the cross-paper claim). §12 "The interaction-vs-appearance pattern agrees with [@chen2025iwr]".**
- Problem: in bai the aggregate VLM (visual) channel is *not* higher than Prog. GPT-6 Astra has VLM 57.92 vs Prog 58.19, and several models have VLM below Prog (Claude Opus 5 42.34 vs 45.99) (p. 11). The bai support comes from category pass rates *within* the programmatic channel (structure vs action-conditioned, p. 16-17), not from a visual-vs-functional channel gap like chen's VFS vs IFS.
- Correct text: "[I] Directionally consistent with [@chen2025iwr]. Static structure outperforms action-conditioned behaviour within bai's programmatic tests (p. 16-17), but bai's visual channel does not exceed its programmatic channel in aggregate (p. 11). The two papers measure the gap differently."

**B9 (minor, missing reliability caveat). §9 "Web scores are panel-relative".**
- Fine as [I]. Add that the panel's composition is not reported, and that the gate runs on "rebuilds from a panel of models" (p. 34). If those models overlap with the evaluated ones, Web scores are partly defined by the evaluated models themselves.

**B10 (minor, paper-internal inconsistency worth recording). Analyst notes.**
- Table 12 (p. 39) lists a case "GLM-5.2 / Ubuntu", but GLM-5.2 is not among the evaluated models in Table 8 (p. 28), which lists glm-5.3. Note it as a paper inconsistency that is not resolvable from the text.

Checked and correct: findings 2, 3, 6, 7 (numbers), 8 (overlap table), 10. Also the 20-hour budget, 35,000 trajectories, 81 tasks / 393 fixtures, the 0.10 cap rule, the coverage audit (77% / 24% / 94.2% / 40.7%), the judge model and temperature, the licence breakdown, and all three key quotes (verbatim). The limitations in §8 are all stated by the authors on the cited pages.

---

## xiong2026propgen — verdict: **pass-with-minor-fixes** (5 fixes)

**X1 (moderate, understated bias). §9 "Possible author-tool bias".**
- Current: "Kea and PBFDroid come from overlapping author groups (refs [52], [71], p. 12-13) ... consulting the original tool authors partly mitigates this."
- Problem: the overlap is wider than stated, and the mitigation is weaker.
  - PropGen co-author Ting Su is an author of Genie [51], Odin [63], PBFDroid [52], Kea [71] and Kea2 [29].
  - Yiheng Xiong co-authored Genie [51] and Kea [71], and Bo Ma co-authored Kea2 [29] (p. 12-13).
  - Three of the four RQ4 baselines (Genie, Odin, PBFDroid; p. 7) therefore come from the PropGen authors' own group. "We further consulted the authors of Genie, Odin, and PBFDroid" (p. 8) partly means consulting a co-author of this paper.
- Correct text: "[I] **Author-tool overlap.** Ting Su (PropGen co-author) co-authored Genie, Odin, PBFDroid and Kea; Xiong co-authored Genie and Kea (refs [29], [51], [52], [63], [71], p. 12-13). The scope analysis is manual (p. 8), its 'validation' by the baseline authors involves the same group, and the PBFDroid properties were written by the PropGen authors (p. 8). Only VisionDroid (p. 7) is independent. This is not necessarily bias in PropGen's favour, since the group knows these tools well, but the scope analysis is not independently validated."

**X2 (moderate, framing that matters for our RQs). §12 "it recovers behavioural specifications from a running black-box app (no source, no spec)"; also the RQ2 evidence row "...from a running Android app without specs".**
- Problem: PropGen is not purely observational.
  - It feeds the MLLM "the list of activity names extracted from the AndroidManifest.xml file" (p. 4).
  - It filters widget text against "a whitelist extracted via static analysis" (p. 5).
  - "Black-box" is the authors' description (p. 11) and should be labelled [A].
  - For a reverse-engineering study, this is observation plus static analysis of the APK (grey-box).
- Correct text: "...recovers behavioural specifications from a running app without source code or written specifications, using runtime observation plus light static analysis of the APK (manifest activity names, a string whitelist; p. 4-5). The authors call this 'exploring a black-box app' [A] (p. 11)."

**X3 (moderate, one-sided evidence row). §13 RQ2 row "Generated properties found 25 previously unknown functional bugs in 12 apps; prior tools rediscovered only 3".**
- Problem: this leaves out the opposite direction, which the paper reports alongside it: the four prior tools together found 13 unknown bugs, 10 of which PropGen missed (p. 10).
- Correct text: "...prior tools rediscovered 3 of them, but themselves found 13 unknown bugs, 10 of which PropGen missed; authors call the approaches complementary [A] (p. 10)."

**X4 (minor, missing appraisal). §9.**
- Add "[I] Whether the annotators were blind to which tool (PropGen or DroidAgent) produced each functionality is not reported (p. 7). The set of items over which Cohen's kappa was computed (PropGen only, or both tools) is not stated (p. 7)."

**X5 (minor, label). Frontmatter `sample_size` "single run each"; §6 "single run per tool and app (p. 8-10)"; §13 RQ4 row "Single run per tool and app ... | 7, 8 | V".**
- Problem: the paper says "This single run" only for the RQ4 prior techniques (p. 8). For PropGen's RQ1-RQ3 no repetition is reported, but "single run" is not stated either.
- Correct text: "No repeated runs are reported (single run stated for RQ4 baselines, p. 8)". Label the evidence row **I**.

Checked and correct:
- Every number in §7 against Tables 2-5 (pp. 8-10) and the text: 1,282 / 1,210 / 977; 575 / 491 / 187; 985 / 912 (78.7-98.8% per app); 240 / 0; 127 / 118 with 53 / 1 / 64; 9 = 5 + 4; 25 bugs = 12 + 6 + 4 + 3; 7 (28%) / 3 (12%); 13 and 10.
- Costs; kappas 0.91 / 0.82 / 0.81; GPT-5.2 snapshot and temperature; budgets of 3 h + 6 h and 9 h; Zenodo DOI; funding; received/accepted dates; all three quotes.
- Two-column interleaving did not corrupt any number used. §8 limitations are all author-stated (p. 9-11).

---

## chen2025iwr — verdict: **needs-fixes** (9 fixes)

**C1 (serious, misread metric). §7 finding 5; §13 RQ2 row "Functional fidelity falls from static to algorithmic tasks (GPT-5 Final 61.85 on L1 vs 25.26 on L4)".**
- Problem: Tables 4-6 report **Final Score only** ("For each task category, the Final Score is reported", p. 16). They are not IFS, and Table 5 is not a visual score.
  - "Functional fidelity falls" and "Data-dense layouts (V4) are hardest visually" misdescribe what was measured.
  - The pattern is also not monotonic. For GPT-5, L2 and L3 are nearly equal (35.43 vs 35.12). Several models score L3 above L2: Claude-Sonnet-4 32.86 vs 31.04, Claude-Opus-4 (thinking) 32.57 vs 31.52, GPT-4.1 31.98 vs 30.32 (p. 17). For GPT-5, V3 is well above V2 (43.77 vs 30.73, p. 18). The robust contrast is L1 vs the rest.
  - L1 ("Static Content Consumption", mainly scrolling, p. 16) has about 9 tasks [I].
- Correct text, finding 5: "Final Score drops sharply from static L1 tasks to interactive ones (GPT-5 61.85 on L1 vs 35.43 / 35.12 / 25.26 on L2 / L3 / L4); L2 and L3 are similar and their order varies by model (p. 17). By visual category, Final Score is lowest on data-dense layouts (GPT-5 26.05 vs 44.77 on V1), with V3 above V2 (p. 18). Category tables report Final Score only (p. 16)."
- RQ2 row: "Final Score falls from static (L1) to interactive tasks (GPT-5 61.85 vs 25.26 on L4); strata are about 9-12 tasks | 16, 17 | V | weak".

**C2 (serious, missing construct appraisal of the headline finding). §7 findings 1-2; §9; §10 Construct; §13 RQ2 row rated moderate; §12.**
- Problem: VFS is "computed exclusively over checkpoints that were successfully reached" (p. 7), while IFS counts every action (p. 7). VFS is therefore conditional on success. A page that fails early loses IFS but cannot lose VFS for the unreached states.
- The headline "IFS lags VFS for every model" is partly built into the metric definitions, and the two scores are not on a common denominator. The authors acknowledge the unreachable-state issue only as the reason for α = 0.7 (p. 7). The analysis does not discuss this.
- Correct text, new §9 bullet: "[I] **IFS and VFS are not comparable in scale.** VFS averages only over reached checkpoints (p. 7) and so cannot be lowered by functional failures that block later states; IFS counts all 1,001 actions. Part of the IFS < VFS gap is therefore a property of the metrics, not only of the models." Add a matching sentence to §10 Construct.
- Keep the RQ2 "moderate" rating only with this caveat, or downgrade it to weak.

**C3 (moderate, incomplete counter-evidence and label). §7 finding 4.**
- Current: notes only that Gemini-2.5-Pro (thinking) has a lower VFS.
- Problem: all three thinking/non-thinking pairs have **lower VFS** with thinking (p. 8):
  - Claude-Sonnet-4: 60.20 vs 61.34
  - Claude-Opus-4: 58.67 vs 60.18
  - Gemini-2.5-Pro: 50.67 vs 53.18
- The authors' heading "Reasoning Enhancement Provides Consistent but Moderate Gains" (p. 9) is a conclusion beyond the data and should be [A].
- Correct text: "...thinking variants raise IFS and Final slightly in all three pairs but lower VFS in all three (60.20 vs 61.34; 58.67 vs 60.18; 50.67 vs 53.18) — [V] (p. 8, p. 9). [A] Authors describe the gains as 'consistent but moderate' (p. 9). The Gemini Final difference is 0.05 points."

**C4 (moderate, §8 contains items that are not author-stated limitations).**
- Current: "[A] An LLM was used for grammar correction and language refinement of the paper (p. 21)". The alternative-weighting remark (p. 7) is also listed as self-critical.
- Problem: the LLM-use note is a disclosure (Appendix G), not a limitation. The weighting remark is a design rationale. The standard bars limitations in §8 that the authors never stated.
- Correct text: "Not reported: the paper has no limitations or threats-to-validity section. Design notes and disclosures (alternative weighting rejected, p. 7; agent-evaluation errors fixed, p. 9; LLM-assisted editing, p. 21) are recorded in Analyst notes." Move those items there.

**C5 (moderate, missing appraisal of the evaluator). §5; §9.**
- Problem: the paper calls the executor "deterministic ... built upon the browser-use library" (p. 6). Yet actions target elements by natural-language description (p. 17), and browser-use resolves descriptions with a model.
  - Which model resolves element descriptions, and whether replays are repeatable, is not reported.
  - "Deterministic" is an author claim [A].
  - It is also not reported whether the full benchmark was re-scored after the 3/100 evaluator failures were "rectified" (p. 9).
- Correct text, add to §5: "[A] Executor described as deterministic (p. 6); the model that resolves natural-language element descriptions (p. 17) and replay repeatability are not reported." Add to §9: "[I] Whether all 28 x 113 evaluations were re-run after the evaluator fixes (p. 9) is not reported."

**C6 (minor, missing "not reported"). §6 metric-weights bullet; §9 "Moderate human alignment".**
- Add: "Agreement among the five human raters is not reported; their judgements were aggregated (p. 17)." Likewise, nothing is reported about agreement among the three PhD students observing the agent (p. 9).

**C7 (hedging of the cross-paper claim). §12 last sentence; §13 strength note.**
- Current: "The same 'looks right, behaves wrong' pattern is reported across five platforms by [@bai2026recreationworld], which strengthens the finding."
- Problem: same as B8. bai's support is within-programmatic category gaps (p. 16-17 of bai). bai's visual channel is not higher than its programmatic channel in aggregate (bai p. 11).
- Correct text: "[I] Directionally consistent with [@bai2026recreationworld], which finds static structure reproduced better than action-conditioned behaviour within its programmatic tests; the two papers measure the gap differently, and here the gap is partly metric-induced (see §9)."

**C8 (labels). §13.**
- Rows "RQ4 | No repeated runs, confidence intervals or significance tests..." and "RQ5 | ...single-file output means code quality/maintainability is not assessed" are our appraisal of what is absent. The paper states neither. Label both **I**, with basis (p. 8-9; p. 7, 20).

**C9 (minor). §3 and §7 finding 3.**
- "28 models" counts three thinking variants separately, so there are 25 distinct base models (p. 8). Add as [I].
- "Proprietary models lead (Final 16.50-36.35)" overstates the separation: the best open-source model, Qwen3-VL (thinking) at 31.15, beats 11 of the 17 proprietary models (p. 8). Rephrase as "the top six are proprietary".

Checked and correct:
- 113 tasks / 100 sites; 200 -> 161 -> 113; 1,001 actions, 620 visual, 403 assertions; 35.4 s / 172.9 s; 19 resolutions; 10.62% mobile; L1-L4 and V1-V4 shares.
- Model group counts 17 / 9 / 2; GPT-5 36.35 / 24.39 / 64.25; the Final formula (0.7 x 24.39 + 0.3 x 64.25 = 36.35).
- 1 fps / 64 frames; HVS rubric 10 / 15 / 40 / 15 / 20; grid search, ρ = 0.57 / 0.65; 3 / 100 agent failures; case studies; Gemini-2.5-Pro as judge and evaluated model. All three quotes are verbatim.
- The derived per-category counts (§9) are correctly labelled [I].

---

## Cross-paper observations

1. **"Looks right, behaves wrong" is claimed as convergent evidence in both §12s, but the two papers measure different things** (see B8, C2, C7).
   - chen: VFS vs IFS, where VFS is conditional on reached states [@chen2025iwr, p. 7].
   - bai: structure vs action-conditioned categories within one programmatic channel [@bai2026recreationworld, p. 16-17], while its visual and programmatic channel aggregates are close [@bai2026recreationworld, p. 11].
   - The convergence is real at the level of "static structure is easier than interaction logic". It is *not* evidence that visual fidelity systematically exceeds functional fidelity. The evidence matrix should phrase it that way.
2. **Both benchmarks use an evaluated model family as judge, and neither tests self-preference.** chen uses Gemini-2.5-Pro, which is also evaluated (mid-table). bai uses Qwen3.7-Plus, which is also evaluated (lowest, after the B1 correction). Record this as a shared RQ4 weakness, not two separate ones.
3. **No repeated runs or CIs on headline scores in either benchmark**, and bai probably uses a single rollout (B5). This is a consistent limitation across the F2/F5 benchmark cluster and supports a gap claim about variance reporting, subject to the novelty-check rules.
4. **Difficulty gradient is consistent.** Algorithmic or game logic is hardest in chen (L4) and computation/interaction is weakest in bai. Neither paper controls for the size of each stratum: chen's L1 and L4 have about 9-12 tasks, and bai's category subsets differ (bai p. 17).
5. **Oracle construction from a running reference appears in two forms.** bai validates generated tests on the reference and adds human review [@bai2026recreationworld, p. 8-9]. PropGen shows that LLM-derived behavioural properties are imprecise at a non-trivial rate (127/985 caused false positives) and need refinement plus human confirmation [@xiong2026propgen, p. 9]. Together they argue that auto-generated fidelity oracles need validation, which is relevant to the RQ5 study design.
6. **No duplicated or conflicting data across the three keys.** The other "Grok 4.6" mention in the project (kim2026programdistill) concerns a different benchmark, so it does not conflict. Once B1 is fixed, check that no downstream document (evidence matrix, gap report) has copied "Grok 4.6 lowest". As of this review, neither cites bai yet.

## Cross-cutting labelling note
In all three analyses, statements that something is absent ("no CIs", "not assessed", "confounded") are labelled [V] in the evidence tables. They are our appraisal of a missing item and should be [I], with the pages that were checked as the basis.
