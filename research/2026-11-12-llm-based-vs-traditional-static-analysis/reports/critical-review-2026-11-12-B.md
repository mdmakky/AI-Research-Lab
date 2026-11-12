# Critical review B — 2026-11-12

Scope: 10 analyses (all `status: ready`, `evidence_basis: full-text`). Reviewer did not edit any analysis.

Checks run for every key: `rlab validate` (all: metadata verified, PDF identity match, not retracted), `rlab cite-check` on `analysis.md` (all OK), RQ links (RQ1–RQ5 all exist in `RESEARCH-QUESTIONS.md`), and spot-checks of ≥5 [V]/[A] items per paper against `fulltext.txt` (all Key-findings numbers, sample size, dataset).

**Summary: 2 pass, 8 fix needed.** Most fixes are small: labels, attribution, RQ mapping, or wording. None changes a paper's headline result.

| Key | Verdict |
|---|---|
| li2024iris | pass (2 advisory notes) |
| xiong2026sifting | fix needed |
| du2026reducing | fix needed |
| ding2025vulnerability | fix needed |
| chakraborty2024revisiting | fix needed |
| risse2025top | fix needed |
| fu2023chatgpt | fix needed |
| kaniewski2026systematic | fix needed |
| zhou2025large | pass |
| sheng2025llms | fix needed |

---

## li2024iris — pass

Verified: Table 1 (55/120, 45.83%, AvgFDR 84.82 vs 90.03, F1 0.177 vs 0.076, p. 8); Table 2 per-CWE and Infer 0 / SpotBugs 4 / Snyk 23 (p. 8); 27/50 → 46% (p. 7); funnel 1065→120 (p. 19); Table 3 ablation 27/36/24/55 (p. 10); runtimes 43 s–4 h (p. 22–24); settings (p. 20–21). Version note is correct: v3 header reads "Published as a conference paper at ICLR 2025" (p. 1). The note and Analyst notes explain why the metadata says preprint while the text is the ICLR camera-ready. Nothing is wrong silently.

Advisory (no fix required):
1. §9/§10 confound bullet. It says IRIS runs on patched CodeQL "while the baseline uses stock 2.15.3 queries". The paper says the queries are the built-in 2.15.3 ones (p. 20, C.2). It does not say whether the baseline ran on the patched or the unpatched engine. Suggested wording: "unclear whether the baseline used the patched engine".
2. §6 and §9 say "one run per configuration". The paper does not report the number of runs; it gives only temperature 0 and a fixed seed (p. 21). Suggested wording: "number of runs not reported (deterministic settings)".

## xiong2026sifting — fix needed

Verified: Table 3 FPRs (p. 12); 1,303/1,325 = 98.3% (p. 12); abstract "over 92%" (p. 1) vs 98.3% (p. 12), and "↓92.1%" is a percentage-point drop described as "eliminating more than 92% of FPs" (p. 19). The inconsistency claim is correct. Also verified: 314/1,411 = 22.25% (p. 18); Table 4 values (p. 13); Table 5 (p. 14–15); Table 8 costs and tokens (p. 17); 15,636 trajectories and 145 scope-drift cases (p. 18). The version note (arXiv v3 = PACMSE ISSTA009) is fine.

[I] derivation check (Table 4, p. 13). True vulnerabilities filtered = Mis-id FP / (Mis-id FP + Corr. Ret.):
- GPT-5 Aider 19.5/34.1 = 57%
- OpenHands 25.0/37.5 = 67%
- SWE-agent 19.1/40.4 = 47%
- Vanilla 19.0/33.3 = 57%

The arithmetic holds (≈47–67%). The cross-check precision = Iden/(Iden+Mis-id), e.g. 61.0/80.5 = 75.8%, confirms that Mis-id FP means true vulnerabilities wrongly filtered.

Findings:
1. **§7 KF6, last sentence.** The analysis says "This TP-suppression risk on real code is not discussed by the authors." That is false. On p. 14 the authors write that for GPT-5 "the primary differentiator shifts to how effectively the framework avoids mis-identifying true vulnerabilities". For DeepSeek they say a high FP rate "is insufficient if it is achieved by incorrectly discarding actual security flaws". Fix: change it to "the authors discuss mis-identification qualitatively (p. 14) but do not report it as a share of true vulnerabilities lost".
2. **§13 row "GPT-5 configs filter ≈47–67%".** The range includes the vanilla GPT-5 baseline, not only agent configurations. It also rests on very small denominators: about 14–19 true-positive alerts are scored per configuration (our inference from row percentages). Fix: say "all four GPT-5 settings incl. vanilla" and add "(≈14–19 TPs per configuration)" so the weak strength is visibly justified.

## du2026reducing — fix needed

Verified: Table 1 (433 = 328 FP / 105 TP; per-type split, p. 4). Table 2 LLM4PFA rows: accuracy 0.93–0.94, P 0.83–0.93, R 0.75–0.88, FPR_R 0.94–0.98; LLM4SA and prompting ranges (p. 8). Table 4 costs: LLM4PFA 12.6–58.3 s and $0.0025–$0.12; overall 2.1–109.5 s and $0.0011–$0.12 (p. 8). Three runs with majority vote (p. 6). "Conference'17" placeholder header (p. 2), so the text is the v1 preprint, as stated. Model/reference mismatch is confirmed: [8] = Claude 3.5 Sonnet, [13] = DeepSeek-Coder-V2-Instruct, [21] = GPT-4 Turbo, [45] = Qwen2.5-Coder-32B-Instruct (p. 11–12). LLM4PFA [15] shares first author (Du) and last author (Lou) (p. 11). Scope: the note on NPD/OOB/DBZ as general bugs and the paper's own "memory safety bugs" (p. 10) is correct, and relevance `medium` is justified.

Findings:
1. **§9 conflict-of-interest bullet is incomplete.** It mentions only the author overlap with LLM4PFA. Four of the nine authors (Wei Xu, Jie Ma, Wei Zhang, Sisi Liu) are Tencent employees, Tencent email addresses are listed on p. 1, and the study evaluates Tencent's own analyser and data. Fix: add the industry-affiliation COI. Funding is not reported (no acknowledgements section found).
2. **Header "Authors" line lists 6 of 9 authors** with no "et al." (missing Liu, Peng, Lou). Lou is the author who links the paper to LLM4PFA, which is the subject of the COI claim. Fix: list all nine authors or add "et al.".

## ding2025vulnerability — fix needed

Verified: Table V (p. 7). BigVul F1 62.88–68.26. Cross-dataset BV→PV F1 1.91–5.82 (CT5 5.82, CB 4.49, UC 1.94, SC2 3.09, CG2.5 1.91). Within-PrimeVul F1 18.05–21.43. VD-S 88.78–91.51. P-C 1.06–3.01. P-B 84.22–88.30. Table VIII (p. 9): GPT-4 CoT P-C 12.94, two-shot 5.14 / P-V 71.63, GPT-3.5 FT 1.24, random 22.70. Tables VI–VII (p. 8–9). Key findings §7 and the frontmatter keep the cross-dataset and within-PrimeVul F1 separate correctly. The CodeBERT "96.86%" text/table inconsistency (p. 8 vs p. 7) is confirmed.

Findings:
1. **§12, conflation.** The analysis says "shows a ~50–65 pp F1 collapse under realistic evaluation". This mixes the two settings. From Table V (p. 7), the within-PrimeVul drop is 42–50 pp (e.g. SC2 68.26→18.05, CB 62.88→20.86). The cross-dataset drop is 58–65 pp. Fix: give both ranges with their settings.
2. **§7 KF1 and §13 row 1, label.** The BigVul 25.0%, CrossVul 47.8%, CVEFixes 51.7% and DiverseVul 60.0% label accuracies are marked "∗ Refers to label accuracy numbers in Chen et al." (Table I, p. 4). They are not this paper's data, but they are labelled [V]. Fix: label them [A] (citing Chen et al. via Ding) or split the row. Only SVEN, CodeXGLUE, VulnPatchPairs and PrimeVul are Ding's own audit, and even SVEN was not majority-voted (p. 3).
3. **§13 row "RQ3 — class weights and contrastive learning".** In our project, RQ3 is about hybrid LLM + static analysis. Training tricks for a single model are not hybrids. Fix: re-map the row to RQ1 or RQ2.
4. **Header lists 6 of 9 authors** (Wagner, Ray and Yizheng Chen are missing) with no "et al.". Fix as for du2026reducing.
5. Minor: §6 says "single-run point estimates", but §5 correctly says runs/seeds are "not reported". Align §6 to "not reported".

## chakraborty2024revisiting — fix needed (minor)

All three numeric-inconsistency claims are verified:
- (a) IVDetect P 39 / R 63 / F1 24 (Table 2, p. 6). The harmonic mean is 48.2.
- (b) The Table 1 project sizes sum exactly to 270,919 (p. 4), and p. 13 repeats "270,919 samples". Section 3 gives 1,682,713 uncertain functions (p. 4). Further support the analysis does not use: p. 9 gives Chrome and Linux *test* samples of 81,351 and 47,181, which is also incompatible with 913,249 test uncertain functions.
- (c) Balanced LineVul: accuracy 99, P 11, R 99, AUC 51.4 (Table 5, p. 9). With 1,110 positives in a test set of about 914k, R 0.99 at about 1% FPR implies an AUC well above 0.5.

LLM accuracy vs imbalance is also verified. With P 0.34, R 0.54 and accuracy 0.80 (Table 8, p. 12), the positive share must be about 13%, versus 0.12% in the Real-Vul test set. So the LLM test set must differ, as the analysis says. Mixtral "7 B parameter" is quoted correctly (p. 12). Augmented LineVul P 37 / R 65 / F1 46 / AUC 81.8 (p. 10) and Mixtral F1 46 / P 38 are verified, as are the AUC gaps of 14.8 and 10.8.

Findings:
1. **Label inconsistency.** "15% of ReVeal vulnerable samples also uncertain" is [V] in §4 but [A] in §13 (p. 3). Fix: pick one. It is the authors' own measurement reported in their text, so [V] is consistent with the other rows.
2. **§9, Big-Vul label-accuracy attribution.** "Ding et al. estimate only ~25% of Big-Vul vulnerable labels are correct [@ding2025vulnerability, p. 4]". Ding copies that figure from Chen et al. (Table I footnote ∗, p. 4). Fix: "Chen et al., as reported by [@ding2025vulnerability, p. 4]". Optionally add Risse's own audit of 39% [@risse2025top, p. 8].
3. **§13 row "RQ3 — dead-code augmentation".** This is not a hybrid LLM + SAST result. Fix: re-map to RQ1 or RQ2.

## risse2025top — fix needed

Verified: 88% / 81 papers, 36/36/22 and 53/81 (p. 5); 39/47/65% (p. 7–8); 151 context-dependent functions (p. 9); 82/90 (p. 10); κ 0.64 / 0.96, more than 150 h, 15-minute cap (p. 6); Table III 0.86/0.96, 0.62/0.68, 0.11/0.48, accuracy 0.63/0.68 (p. 11); SOTA sources (p. 7).

Findings:
1. **§9 bullet 3 has a factual error.** "On DiverseVul (the least leaky/noisy of the three per Ding et al.)". In Ding's Table II (p. 4) exact-copy leakage is CodeXGLUE/Devign 0.6% < DiverseVul 3.3% < BigVul 12.7%, so DiverseVul is not the least leaky. It is the least noisy, but only via Chen et al.'s figures in Ding's Table I. The reference also lacks a citation key. Fix: "least noisy by label accuracy (60%, Chen et al. via [@ding2025vulnerability, p. 4]); not least leaky (3.3% vs Devign 0.6%)". Alternatively, use Risse's own 65% (p. 8).
2. **The same bullet is labelled [I] but restates an author caveat.** On p. 11 the authors write that DiverseVul "may contain fewer exploitable spurious features. However, this is not definitive proof". Fix: attribute it as [A] (p. 11) and keep only the "not universal" inference as [I].

## fu2023chatgpt — fix needed (minor)

Verified: F1 94/87/35/29/10, top-10 accuracy 99/99/87/65/25 (text p. 3, Fig. 5 p. 4); the internal consistency of the figure-read P/R values (gpt-4 P 25 / R 33 gives F1 28.4; GraphCodeBERT P 50 / R 27 gives 35); the 1:20 ratio and 80/10/10 split (p. 3); 70/10/20 for repair (p. 3); "pilot study" (p. 2); the repair quote (p. 5); self-authored baselines [8]–[11] (Fu/Tantithamthavorn, p. 5); no limitations section.

Findings:
1. **§9 bullet 2, attribution.** "Ding et al. report ... ~25% label accuracy for Big-Vul". The 25% is Chen et al.'s figure, reproduced by Ding (Table I ∗, p. 4). Fix as in chakraborty F2.
2. **§12, contradiction framing.** "the ordering reverses" is accurate only on a different metric and test set. Fu uses F1 on a 1:20 random-split Big-Vul. Ding uses P-C on 564 PrimeVul pairs. Ding's own BigVul rows (F1 62.88–68.26%, p. 7) agree with Fu's direction. Fix: state the metric and dataset difference in the same sentence.

## kaniewski2026systematic — fix needed (minor)

Verified: 263 studies (p. 1, 7), 78 (29.7%) preprints (p. 8), 514/865/2776 hits (p. 8), "as of December 13th 2025" (p. 8), 195 / 139 (p. 11, 13), LoRA 27, RAG 25, agentic 10 (4 on PrimeVul), GNN 20 (p. 36–37), 87 custom datasets / nine reused >10 times (p. 35), 555 CWEs (p. 34), Table 4 usage counts (p. 26), Table 5 shares (p. 28). The internal inconsistencies are confirmed: Fig. 11 caption "Mar 2025" (p. 34) and SecurityEval 75 vs 69 CWEs (p. 29 vs p. 28). Survey-about-others numbers are correctly [A].

Findings:
1. **§12 and §13 RQ2 row, range.** "vulnerable shares from 0.7% to 50%" / "0.7–50% vulnerable" is wrong for Table 5 (p. 28), which includes FormAI 80.2% and SecurityEval 100.0%. Fix: "0.7–100% (0.7–48% among the function-level C/C++ benchmarks)" or name the subset.
2. **§13 RQ5 row** ("Seven open limitation themes", label A) is rated **strong**. It is the authors' own synthesis and opinion. Under standards §5, "strong" requires replication or consistency across studies. Fix: downgrade it to moderate, or justify "strong" by citing the other surveys that agree (zhou2025large, sheng2025llms).

## zhou2025large — pass

Verified: the selection flow 1,535 → 1,387 → 1,332 → 212 → 82 → 42 (37 + 5) → 58 (Fig. 2, p. 4; p. 6–7); the abstract's 43 + 15 (p. 1); 26.1% (24/92), 47.8% (44/92) (p. 7); ≈73/17/10% (p. 9, 14); repair ≈63/37% with "three techniques" listing two (p. 17); 7 line-level studies and 1 repo-level study ([130]) (p. 17–18); 42 and 12 samples (p. 18); 67.6% and 20% (p. 21); the "For vulnerability repair" sentence inside a detection-label paragraph (p. 19); [130] Zhou … Lo (references). Second-hand claims are [A]. Self-citation of the only LLM-vs-SAST study is flagged correctly.

## sheng2025llms — fix needed (minor)

All claimed inconsistencies are verified:
- 58 studies (p. 8) vs "56 selected papers" (p. 10)
- "approximately 40 studies (83%)" (p. 20)
- "at least 10K samples" (p. 19) vs "at least 100,000 examples" (p. 24)
- "encoder models still dominate non-fine-tuning studies (72.4%)" (p. 10) vs decoder-only 67.1% overall (p. 9)
- precision described as "true positive rate" (p. 14)
- [36] is Gao et al. 2021 *Beyond Tests* (repair) but is cited for CWE-787 vs CWE-862 (p. 22 vs reference list)

Also verified: 33 LLMs, GPT-4 29 / GPT-3.5 25 (p. 8); language shares 50 / 21.1 / 11.8 / 16.6 (p. 11); 41.3% (p. 16); repository-level datasets are only MAGMA and CWE-Bench-Java (Table 4, p. 13); Kaniewski lists Sheng et al. as Sep 2025, 2017–2025, non-SLR (kaniewski p. 4). Numbers about other papers (Ding 0.21, Guo 0.099 / 0.66) are correctly [A].

Findings:
1. **§13 RQ4 row** combines a corpus count (50% C/C++ …, [V] by the survey convention) with "memory-related vulnerabilities are detected more accurately than logic vulnerabilities". The second part is a second-hand claim, and §7 KF9 itself labels it [A] (p. 3, 22). The row carries a single [V] label. Fix: split it into two rows, a V row for the count and an A row for the memory-vs-logic claim.

---

## Cross-paper observations

1. **fu2023chatgpt vs ding2025vulnerability: contradiction confirmed, but metrics differ.**
   - Fu: on random-split Big-Vul (1:20), fine-tuned AIBugHunter reaches F1 94% and CodeBERT 87%, vs gpt-4 at 29% and gpt-3.5 at 10% [@fu2023chatgpt, p. 3–4].
   - Ding: on 564 PrimeVul pairs, GPT-4 CoT gets P-C 12.94% vs ≤3.01% for fine-tuned 7B and smaller models; random is 22.70% [@ding2025vulnerability, p. 7, p. 9].
   - The two use different metrics (F1 vs pair-wise correctness), different datasets (noisy random split vs de-duplicated temporal split) and different GPT versions and dates. Ding's own Big-Vul rows (F1 62.88–68.26%, p. 7) agree with Fu's direction.
   - `evidence-matrix.md` "Contradictions" is currently empty and should record this pair with the explanation labelled [I] (standards §6).
2. **Conflicting numbers for the same model on the same dataset.** CodeBERT on Big-Vul: F1 87% [@fu2023chatgpt, p. 4] vs 62.88% [@ding2025vulnerability, p. 7]. The LineVul replication gives F1 90% [@chakraborty2024revisiting, p. 6]. The literature SOTA is DeepDFA at 96.46% [@risse2025top, p. 7]. A spread of about 25 pp for one model on "Big-Vul" is itself RQ2 evidence of split and preprocessing sensitivity, so cite these as a range, not as one number.
3. **Big-Vul label accuracy has two independent estimates:** 25% (Chen et al., reproduced in [@ding2025vulnerability, p. 4]) and 39% (Risse's own n=100 audit, [@risse2025top, p. 8]). Three analyses (ding, chakraborty, fu) cite the 25% as Ding's own finding. Fix the provenance consistently.
4. **Duplication figures (BigVul 12.7%, CVEFixes 18.9%, DiverseVul 3.3%) come from one source** (Ding, p. 4) and are reused by `ahmed2026secvuleval`. Do not count them as independent replication.
5. **The LLM-vs-SAST claim in zhou2025large (p. 22) is self-citation** of `zhou2024comparison`. Cite the primary study, and do not count the survey as independent support.
6. **Hybrid false-positive filtering shows the same pattern in two settings.** xiong2026sifting (OWASP / Vul4J / OSS-Fuzz) and du2026reducing (Tencent industrial) both report large false-positive reductions with a non-trivial loss of true positives: a 22.25% miss rate [@xiong2026sifting, p. 18] and recall of 0.75–0.88 [@du2026reducing, p. 8]. du covers non-security bug classes and includes the authors' own method plus a Tencent COI, so treat the agreement as moderate, not strong. kaniewski2026systematic excludes this study type by design (p. 7–8), so its corpus cannot be used against or for these results.
7. **Version drift.** du2026reducing is analysed from the v1 preprint (placeholder header), not the ICSE-SEIP camera-ready, so it has the highest risk that numbers changed. The other arXiv-text analyses carry correct version notes.
8. **Template artefact.** Header "Authors" lines are truncated at six names with no "et al." (du2026reducing 6/9, ding2025vulnerability 6/9). Check other analyses generated from the same template.
