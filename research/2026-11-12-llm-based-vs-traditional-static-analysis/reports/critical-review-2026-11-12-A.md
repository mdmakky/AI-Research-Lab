# Critical review — batch A (10 analyses) — 2026-11-12

Reviewer: critical-reviewer agent. Scope: `papers/<key>/analysis.md` for zhou2024comparison, gnieciak2025large, khare2025understanding, dubniczky2025castle, li2026llm, guo2025repoaudit, yildiz2025benchmarking, tan2026think, ahmed2026secvuleval, shu2026evaluating. Analyses were not edited.

Method: ran `rlab validate` and `rlab cite-check` on each analysis (all 10 cite-checks OK). For each paper, checked at least 5 [V]/[A] items against `fulltext.txt` with grep, covering all the Key-findings numbers, sample size and dataset. For zhou2024comparison, also rendered PDF page 6 to check Table 3. Recomputed every [I] arithmetic claim that was flagged for checking.

**Summary: 3 pass, 7 fix needed.** Most findings are minor or moderate. None invalidates an analysis. The most important ones are G1, G2 and L1 (the RepoAudit contradiction), K2, and S2.

| Key | Verdict | Provenance |
|---|---|---|
| zhou2024comparison | fix needed | verified; arXiv v1 preprint, flagged |
| gnieciak2025large | pass | verified; arXiv v1 of IEEE Access paper, recorded |
| khare2025understanding | fix needed | **MISMATCH** (arXiv year 2023 vs ICST 2025); not recorded |
| dubniczky2025castle | fix needed | verified; arXiv v2 of LNCS chapter, recorded |
| li2026llm | fix needed | verified; arXiv v2 of TSE paper, recorded |
| guo2025repoaudit | fix needed | verified; arXiv v3 (ICML camera-ready text), preprint tier flagged |
| yildiz2025benchmarking | pass | verified; identity "probable", confirmed by title and authors on p. 1 |
| tan2026think | fix needed | verified; publisher PDF, DOI match |
| ahmed2026secvuleval | pass | verified; identity UNCONFIRMED by rlab. **Manually confirmed**: the 5 authors on PDF p. 1 (Ahmed, Shiri Harzevili, Shin, Pham, Wang; York University) match metadata. Title differs: arXiv 2505.19828v1. Recorded |
| shu2026evaluating | fix needed | verified; arXiv v2 of EMSE paper, recorded |

All RQ links (RQ1–RQ5) exist in `RESEARCH-QUESTIONS.md`. None of the papers is retracted.

---

## zhou2024comparison — fix needed

1. **§7 item 3 ("10.6 / 9.1 points more").** Problem: the paper's 10.6% and 9.1% are *relative* gains, not percentage points. Evidence: Table 3 (p. 6) gives these Java means. Fine-tuned lightweight S1 is (87.5+75+87.5+75)/4 = 81.25 and PEFT is 587.5/8 = 73.44. That is +7.8 points, or +10.6% relative. For S2 it is 56.25 vs 51.56: +4.7 points, or +9.1% relative. "43.2% more functions" is also relative (27.8 vs 19.4). Required fix: say "10.6% / 9.1% higher (relative; ≈ +7.8 / +4.7 points)".
2. **§9 bullet 2 and Analyst notes, "Internal inconsistencies between Table 3 and the text".** Problem: the analyst is right that the rendered PDF shows 7.5, 4.4 / 3.3 and 0.0 / 0.0 (I confirmed on rendered p. 6). So this is not a pdftotext artefact. But the pattern shows a typesetting defect, not conflicting results: the leading digit is dropped in some highlighted cells. Evidence:
   - 37.5→7.5, 44.4→4.4, 33.3→3.3, 30.0→0.0, 20.0→0.0.
   - The PEFT CodeLlama Java "Marked" cell prints ".3". It must be 8.3: the text gives the Java range as "8.3% to 77.4%" (p. 7), and the PEFT mean of 19.4% implies ≈ 8.2.
   - The PEFT Llama3 C cell prints ".5". It must be 3.5, the lower bound of "3.5% to 70.1% in C" (p. 7).
   - Horusec 7.5 is not a multiple of the 12.5-point step, which also points to a dropped digit.

   Required fix: reword it as "a typesetting defect in Table 3 (dropped leading digits). The text values are consistent with the table's other cells." Remove it as evidence of an internal inconsistency in §9 and §12.

## gnieciak2025large — pass

- Pooled-count [I] verified. Summed Tables 4–5 (p. 8) give reported/TP: SonarQube 15/13, CodeQL 26/21, Snyk 57/42, GPT-4.1 74/55, Mistral 61/48, DeepSeek 70/52, with 63 vulnerabilities in total. My recomputed P/R/F1 match the analysis to two decimals (e.g. SonarQube 0.867/0.206/0.333; GPT-4.1 0.743/0.873/0.803). The FP counts (GPT-4.1 19; Snyk 15/57) are also correct. Table 13 (p. 10), Table 6 runtimes (p. 9) and Table 14 (p. 12) checked.
- Optional: the paper also says the projects are "between 3500 and 5500 characters" (p. 5), while Table 3 shows 3,145–5,317 (p. 6). This is a minor in-paper inconsistency the analysis could add to §9.

## khare2025understanding — fix needed

1. **Provenance not recorded.** `rlab validate` returns **MISMATCH** (arXiv cross-check year_match = false: arXiv v1 is 2023, ICST is 2025). The Analyst notes do not mention this. It is benign, but the standards require provenance problems to be recorded. Required fix: add a line explaining the MISMATCH (preprint year vs proceedings year; same title and first author).
2. **§7 item 9, §13 RQ1 row 3, frontmatter main_finding: the LLM-vs-DL comparison is selective and omits the trivial baseline.** Evidence: Table IX (p. 10).
   - The analysis contrasts Qwen-2.5-32B F1 0.65 only with the in-distribution DL rows (DeepDFA 0.23, LineVul 0.61). The other rows are DeepDFA BigVul→CVEFixes F1 0.62 and LineVul Juliet→CVEFixes F1 0.64.
   - On accuracy, in-distribution LineVul (0.59) beats Qwen (0.56).
   - Qwen's F1 of 0.65 (P 0.54, R 0.81) is *below* the always-vulnerable F1 of 0.667 that §9 itself invokes.
   - The same caveat applies to CodeQL on OWASP (A 0.63, P 0.58, R 0.96, F1 0.72; Table VIII, p. 9).

   Required fix: report the full DL range (F1 0.02–0.64), note LineVul's higher in-distribution accuracy, and attach the trivial-baseline caveat to the RQ1 rows.
3. **Analyst notes, "mean F1 0.71 not directly traceable".** This can be resolved. The 0.71 is the mean of the best F1 per dataset in Table XII (p. 16): (0.70 + 0.79 + 0.67 + 0.73 + 0.67)/5 = 0.712. Two of the five bests (CVEFixes Java and CVEFixes C/C++, 0.67) are "always vulnerable" rows (P 0.50, R 1.00). Required fix: replace the uncertainty with this derivation and use it to strengthen the §9 trivial-baseline [I]. (§9 bullet 1 is otherwise verified: CodeLlama-7B/13B/34B CWE-DF and DSCoder-15B CWE/CWE-DF rows.)

## dubniczky2025castle — fix needed

1. **§9 bullet 1 and §13 RQ2 row: "TP + FN exceeds 150 for most LLMs".** Problem: it is **all 10 LLMs**, with TP + FN from 154 to 179 (o3-mini 162, o1 163, R1 165, 4o 179, 4o-mini 177, Qwen 163, Falcon 154, Mistral 154, Gemma 158, Llama 163). It also applies to 4 tools: CodeQL 157, Semgrep 156, GitLab 156, Jit 155. The other 11 tools sum to exactly 150 (Table 3, p. 11). §7 item 3 also repeats "29% (45/150)" as [V], but 45/150 = 30%; 29% = 45/157. The paper's own sentence (p. 12) therefore confirms the denominator problem. Required fix: change "most" to "all"; add the 45/150 ≠ 29% observation; flag §7 item 3 accordingly.
2. **§7 item 4 [A] vs §13 RQ3 row [V], "reasoning models produce fewer FPs".** Problems:
   - The label is inconsistent between §7 and §13.
   - The claim only holds for the OpenAI o-series (o3-mini 73 FP, o1 90 FP vs GPT-4o 116, 4o-mini 263). DeepSeek R1, also a reasoning model, has 166 FP, more than GPT-4o (Table 3, p. 11). Yet the authors say reasoning models "consistently produced fewer false positives" (p. 14).

   Required fix: label it [A] in both places and add the R1 counter-example as [I].

## li2026llm — fix needed

1. **§13 RQ3 row: "Hybrid LLM+SAST tools (IRIS+CodeQL, KNighter+CSA) do not beat plain SAST on real-world SFDR".** This is wrong for KNighter (o3-mini). Its overall SFDR is 81.25%, lower (better) than CSA 85.51% and CodeQL 86.01% (Table VII, p. 11). That figure comes from only 48 warnings on one module (linux/drivers/net). The GPT-5.4 variant is 95.56% (Table VIII, p. 11). Required fix: restrict the claim to IRIS (97.80% vs CodeQL 77.00% Java, Table IX, p. 12) and KNighter-GPT-5.4. State that KNighter-o3-mini's lower SFDR rests on one project.
2. **§7 item 1: RepoAudit with its original backbone is missing.** RepoAudit Sonnet 3.5 detects **0** of 110 C/C++ controlled vulnerabilities (Table IV, p. 7); only the GPT-5.4 variant finds 2. Table XII (p. 16) also shows a RepoAudit minimum of 0.00 input tokens and $0.00. On at least one project no LLM call was made at all, which is consistent with the authors' "incomplete API modelling" explanation (108/108 misses, p. 7). Required fix: add both facts. They matter for the guo2025repoaudit contradiction.
3. Minor: several items carry a combined "[V]/[A]" label (§7 items 5, 7). The standards require one label per statement. Split them.

Verified: the 59.55% (131/220), 63.87%/81.94%, SFDR, cost and per-warning figures; the Codex warning totals of 22 C/C++ and 22 Java used in the §9 [I]; and the version stamp arXiv 2601.19239v2 (25 Sep 2026).

## guo2025repoaudit — fix needed

1. **§9 bullet 6, "Contradicts later independent evaluation".** The bullet conflates two li2026llm datasets and omits the setup differences.
   - The overlapping projects (linux/mm, linux/sound, linux/drivers/net, linux/drivers/peci, ImageMagick) are in li's *real-world* set at current commits (6093a68 / 3bf1076; li Table III, p. 6), where recall is not measured.
   - On those projects RepoAudit (Sonnet 3.5) emitted 0 warnings (linux/sound, linux/mm, ImageMagick), 1 warning (linux/drivers/net, FP) and 3 warnings (peci, all FP) (li Table VII, p. 11). The 92.77% is the 9-project average.
   - The "0 detections on known CWE-401/416" come from li's *controlled* ReposVul set (li Table IV, p. 7), whose repositories li does not name ("three repositories with the most cases", li p. 5).
   - Setup differences: guo's 21 "Old" bugs are the prior tools' bug reports on older commits (guo p. 7, Table 2, p. 8). The 4 Linux cases are all intra-procedural, as li notes (li p. 7). The metrics also differ: precision on the tool's own reports vs recall on CVEs and SFDR.

   Required fix: rewrite it as a documented tension, with both sides' page refs and these differences, labelled [I].
2. **Missing cross-paper cost contradiction.** guo reports an average of $2.54 and 0.44 h per project, maximum $18.15 (p. 7–8). li measures RepoAudit (Sonnet 3.5) at an average of $172.77, maximum $1,247.66, and >800 min per project (li Table XII and text, p. 16). Required fix: add this to §9 and the RQ3 evidence row as an [I] contradiction (different projects and sizes; li includes multi-million-LOC Linux modules, gpac and bitlbee).

Verified: Table 2 sums (Old 21, New 19 of which 14 fixed, FP 11, Inter 21); Infer 13 built / 8 analysed / 7 TP / 2 FP; CodeGuru 0/18. The Table 4 MLK TP column sums to 75 against a printed total of 76, and 185 TP at 85.71% fits 186/217 better than 185/216 (85.65%). The analysis is correct on both points.

## yildiz2025benchmarking — pass

- Random-baseline [I] verified. Independent coin-flip labelling of a pair gives pAcc 0.5 × 0.5 = 25%, which is also the maximum q(1−q) for any random guesser. The best GPT pAcc is 20.17 (4o-mini ReAct FS) and 19.13 (4o) (Table 2, p. 6). Table 2, Table 3 (5.41–12.21; it is on p. 7, not p. 6) and Table 4 (p. 15: 82.09 / 69.24; ReAct ≤21.39) checked. The 1/119 granularity note checks out (3.36 = 4/119, 20.17 = 24/119, 14.29 = 17/119).
- Optional additions:
  - All GPT F1 values (48.23–66.05) are at or below the always-vulnerable F1 of 66.7 on the balanced pairs.
  - The paper's own random reference is 22.70% (from Ding et al., p. 7) vs our 25%; state why both are below.

## tan2026think — fix needed

1. **§9 bullet 2, "All P-C values are ≤26.9%, close to the 25% expected from random independent labelling".** Problem: "close to" misstates the DA results. DA P-C is 0.7–18.8 per setting, with a mean of 6.2 (Table 3, p. 7), and 0.5–13.0 in Table 9 (p. 11). That is far *below* the random ceiling. Required fix: "≤26.9%, i.e. at or below the 25% random-labelling ceiling; DA is far below it."

Verified:
- The always-vulnerable [I]: F1 = 0.667. The maximum reported F1 is 0.665 in Table 3 (p. 7; DA rows Qwen-4B Inst Zero and Qwen-30B Inst Zero) and 0.666 in Table 9 (p. 11). No F1 value in the text exceeds 0.667 (all larger decimals are recalls).
- The NA accuracy order 0.518 (instruct) → 0.523 (thinking), recomputed from Table 2 (p. 6).
- P-C improved in 6 of 8 settings (1 tie, 1 decrease).
- Costs (p. 10) and the "largely" vs "not wholly" wording conflict (p. 9 vs p. 11).

## ahmed2026secvuleval — pass

- Identity: the authors on PDF p. 1 match `metadata.json` exactly. The version note correctly records arXiv 2505.19828v1 and the title change.
- **Statement-level recall [I] verified exactly for all five models.** I reconstructed the counts from Table 3 (p. 8) and the flag counts on p. 13:

  | Model | Flagged | Func TP | Positives | Stat TP |
  |---|---|---|---|---|
  | Claude | 215 | 90 | 119 | 33 |
  | GPT-4.1 | 214 | 87 | 119 | 31 |
  | Codestral | 116 | 55 | 120 | 15 |
  | Qwen | 124 | 44 | 126 | 15 |
  | Deepseek | 124 | 56 | 121 | 7 |

  Every reported statement-level recall equals TP_stat / (TP_stat + function-level FN): 33/62 = 53.23, 31/63 = 49.21, 15/80 = 18.75, 15/97 = 15.46, 7/72 = 9.72. Under the stated definition (p. 7), recall = TP_stat / positives. For Claude that is 33/119 = 27.7%, with F1 = 19.8%; for GPT-4.1 it is 31/119 = 26.1%. The 214/215 flag counts rule out integer multiples. The Qwen precision requires 124 flagged, not the 121 printed on p. 13 (43/121 = 35.54 ≠ 35.48).
- The claim is correctly labelled [I] and hedged ("appears"). Optional: soften "That means … were not counted as FN" to "This is consistent with … not being counted as FN".

## shu2026evaluating — fix needed

1. **Header author list omits Yasutaka Kamei.** He is the 7th author in `metadata.json` and on PDF p. 1. Required fix: add him (frontmatter/body consistency).
2. **§9 leakage [I], last sentence ("The time-split check tests memorisation of pre-training data, not this split-level overlap").** Problem: this is incomplete. BM25 few-shot examples are retrieved from the **REEF training dataset** (p. 12). If the 2024–2025 time-split run used the same pool, twins of time-split test functions cannot be in it. The time-split function-level result (Acc 0.7874 ≥ 0.7196, Table 10, p. 39) is then evidence *against* twin/BM25 leakage driving the function-level advantage. The line-level drop (0.6641 → 0.3450) remains compatible with the hypothesis. The paper does not state the retrieval pool for the time-split run (p. 38). Required fix: add this counter-evidence and the unknown retrieval pool to the [I], and keep the strength "weak".

Verified:
- **"All seven languages" contradiction.** In JavaScript, CodeT5P (0.7062) and CodeT5 (0.6898) beat GPT-4o ITFSP (0.6642) (p. 21). Yet the RQ1 summary claims GPT-4o "outperformed all other PLMs and LLMs across all seven studied languages" (p. 22). The same page also claims GPT-4o "surpasses CodeT5P in high-level languages" (p. 21).
- **Padding [I] arithmetic.** The line-level DummyClf_vul precision is 0.0267 (p. 23), against 25,161 / 175,768 = 14.3% vulnerable lines (Table 2, p. 8). 810 × 113 = 91,530 slots, and 2.67% of that ≈ 2,444, close to the ≈ 2,505 expected (3.09 per function).
- Table 3/4/11 values; the "0.1264" text value is actually the FPR of the ITFSP row (p. 40); costs and the break-even point (p. 41–42).

---

## Cross-paper observations

1. **RepoAudit: confirmed contradiction (guo2025repoaudit vs li2026llm).**
   - guo: 40 TP / 11 FP, precision 78.43%, all 21 known bugs reproduced on 15 C/C++ projects [@guo2025repoaudit, p. 7–8]; cost $2.54 per project [@guo2025repoaudit, p. 7].
   - li: RepoAudit-Sonnet 3.5 detects 0/110 known C/C++ vulnerabilities and RepoAudit-GPT-5.4 detects 2/110 [@li2026llm, p. 7]; real-world SFDR is 92.77% [@li2026llm, p. 11]; average cost $172.77, maximum $1,247.66 [@li2026llm, p. 16].
   - Both sides are confirmed in the texts. They differ in target selection (prior tools' reports vs ReposVul CVEs), code version (old vs HEAD), metric (precision vs recall/SFDR), labeller (authors vs Codex) and project scale. li's zero-token runs and its API-modelling analysis point to source/sink coverage as one mechanism. Record this in the evidence-matrix "Contradictions" section with these differences, as [I].
2. **F1 on balanced data is at or near the trivial "flag everything" baseline in four studies:**
   - khare: best-per-dataset F1 includes 0.67 always-vulnerable rows [@khare2025understanding, p. 16].
   - tan: maximum 0.665/0.666 vs 0.667 [@tan2026think, p. 7, p. 11].
   - yildiz: GPT F1 48–66 [@yildiz2025benchmarking, p. 6].
   - shu: DummyClf_vul F1 0.6693 vs best 0.7075/0.7069 [@shu2026evaluating, p. 17].

   The synthesis should never compare F1 values across balanced and imbalanced studies and should report trivial baselines next to F1 values. Pairwise accuracy is at or below the 25% random ceiling in yildiz and tan. Both use PrimeVul-derived pairs, so this is one dataset family, not independent replication.
3. **"Reasoning reduces false positives" is contested.** CASTLE's claim [@dubniczky2025castle, p. 14] holds for o1/o3-mini but not for DeepSeek R1 (166 FP) [@dubniczky2025castle, p. 11]. tan finds that thinking mode mainly raises recall and flagging [@tan2026think, p. 6]. shu finds reasoning LLMs near chance [@shu2026evaluating, p. 37–38]. Treat this as a contradiction, not a finding.
4. **SAST effectiveness depends on the setting rather than conflicting across papers.** CodeQL ranges from 0% (Java/Python repo-level) [@zhou2024comparison, p. 6–7] through 6–34% recall (C/C++) and 14% (Java) [@li2026llm, p. 7, p. 9] and 29% on CASTLE [@dubniczky2025castle, p. 12] to accuracy 0.94 on Juliet Java [@khare2025understanding, p. 9]. This pattern supports the RQ2 explanation: synthetic suites favour SAST rules, real repositories do not. CodeQL configuration is unreported in zhou.
5. **Overlapping targets, not duplicated data.** guo and li share five C/C++ projects/modules at different commits, so their RepoAudit results are not independent of project choice. ahmed (SecVulEval) and khare (CVEFixes) both draw on NVD fix commits for C/C++. yildiz and tan both use PrimeVul. Weight these as related evidence in the evidence matrix.
6. **Version provenance.** 6 of the 10 analyses use arXiv text of published papers: gnieciak, khare, dubniczky, li, shu, and ahmed (whose title differs). guo is camera-ready text but registered as a preprint. All record this; numbers should be re-checked against the versions of record before the final report. zhou is the only true preprint without a known published version.
