# Critical review, batch A (2026-11-11)

Project: 2026-11-11-ai-reverse-engineering-vibe-coding. Reviewer: critical-review subagent. Rules: `docs/research-standards.md`.
Scope: `papers/<key>/analysis.md` for 10 keys, checked against `fulltext.txt` (page markers), `metadata.json` and, for asdaque2026novice, the page objects of `paper.pdf`. No analysis files were edited.

## Process and provenance checks

- `rlab cite-check` passes for all 10 analyses: asdaque 56 citations, borg 98, ehsani 124, fawzy 56, he 80, kim 86, liu 84, lu 77, mock 93, molison 97.
- `rlab validate` **could not run** for any key: every call stopped with `error: pdftotext not found`. Because of this, PDF identity was not re-checked by the tool. From `metadata.json`, all 10 have `verification.status: verified` and `is_retracted: false`. PDF identity is `match` for 9 keys. For liu2026benchmarking it is `probable`, but the ACL footer on PDF p. 1 confirms it ("Proceedings of the 64th Annual Meeting ... pages 35032–35068", fulltext lines 70–71). **Action for the lead:** install poppler (pdftotext/pdfinfo) and re-run `rlab validate` for this batch before marking any analysis `complete`.
- asdaque2026novice: `paper.pdf` has **5** page objects (counted with pypdf). The ACM reference line agrees ("ACM, New York, NY, USA, 5 pages", p. 1). `metadata.json` `fulltext.pages: 7` is wrong. The analysis's mapping is correct: markers 4–6 are real page 4, and marker 7 is real page 5. I checked every asdaque page ref against the real 5-page text.
- Six of the ten analyses cite arXiv PDFs of papers that are recorded as published: asdaque, ehsani, fawzy, he, lu, molison. Page refs therefore use arXiv pagination. Three of these PDFs are pre-acceptance versions, so their content may differ from the published papers:
  - fawzy: header placeholder "Conference'17".
  - ehsani: footer "Manuscript submitted to ACM".
  - lu: "Preprint. Under review."

  Each of these analyses notes the version. The synthesis should repeat the caveat.
- Every RQ link (RQ1–RQ5) exists in `RESEARCH-QUESTIONS.md`. Every cross-reference to another project key (fawzy2026vibe, tran2026vibe, yang2026programbench, he2026speed, borg2026echoes, molison2025llm) exists under `papers/`.

## Summary

| Key | Verdict | Fixes |
|---|---|---|
| asdaque2026novice | pass-with-minor-fixes | 3 (+1 recommendation) |
| borg2026echoes | pass-with-minor-fixes | 4 |
| ehsani2026faster | pass-with-minor-fixes | 4 |
| fawzy2026vibe | pass-with-minor-fixes | 3 |
| he2026speed | pass-with-minor-fixes | 2 |
| kim2026programdistill | pass-with-minor-fixes | 3 |
| liu2026benchmarking | **needs-fixes** | 2 (1 factual [V] error) |
| lu2025webgen | pass-with-minor-fixes | 3 (1 metadata escalation) |
| mock2026vibe | pass-with-minor-fixes | 1 |
| molison2025llm | pass-with-minor-fixes | 2 |

Overall the batch is of high quality. I sampled at least 10 [V] numbers per paper (all headline numbers, the sample size and the dataset) by searching `fulltext.txt`. Apart from the items below, they matched the cited page. Appraisal sections are paper-specific rather than generic. The analyses correctly identified the most important weaknesses: few-shot leakage (molison), the model-generation confound (mock), estimator sensitivity (he), self-preference of the construction model (kim) and DOM-anchor coupling (liu).

---

## asdaque2026novice — pass-with-minor-fixes

Verified correct (real PDF pages):
- 22,953 PRs / 1,719 users and 33,596 / 1,796 (p. 1, p. 2).
- 859/860 quartile split (p. 2).
- 2.15x, 10/11 categories, 1.58 vs 4.20 (p. 2–3).
- 1.47x, 9/11, 5/11, 24.29 vs 70.35 (p. 3).
- 31%, 93.06 vs 75.39 (p. 3).
- 5.16x, 0.61 vs 2.83 (p. 3).
- 4.52x, 6/11, 0.13 vs 0.86 (p. 3).
- Benjamini-Hochberg "for all tests" (p. 4).
- Limitations (p. 4).
- Replication package (p. 2, ref [9] p. 5).

The "creation-to-merge vs 'remain open before resolution'" critique in §9 is a good catch.

1. **§13 Evidence table, RQ4 row**
   - Current: "Experience operationalised as commits per GitHub account age, which authors admit conflates activity with skill; PRs treated as independent, no effect sizes reported | p. 2, p. 4 | V | moderate".
   - Problem: one row labelled [V] mixes three things:
     - a verified design fact (p. 2);
     - an author admission ([A], p. 4);
     - our inference ("PRs treated as independent" is [I], and see fix 2).
   - Correct: split into three rows:
     - [V] "Experience = total commits / GitHub account age; quartile split Q1–2 vs Q3–4; group differences reported as ratios of means without effect sizes or CIs (p. 2, p. 3)".
     - [A] "Authors state the commit-based proxy 'conflates activity with skill' (p. 4)".
     - [I] "Unit of analysis for the tests is unclear; if PR-level, observations are clustered by user".
2. **§9 bullet 2 (Non-independence) and §10 Statistical conclusion**
   - Current: "22,953 PRs from 1,719 users ... are tested as independent observations".
   - Problem: stated as fact, but the paper only says "we conduct group-wise statistical test comparisons on mean values of each metric across PR categories" (p. 2). That wording could mean PR-level tests or tests on category means; the unit of the Mann-Whitney/Chi-square tests is not stated.
   - Correct: "[I] The unit of the statistical tests is not stated clearly ('on mean values of each metric across PR categories', p. 2). If PR-level values were tested, about 13 PRs per user are treated as independent and prolific users can dominate; if category means were tested, n = 11 per group and power is very low."
3. **Source note (line 28)**
   - Current: "The PDF has **5 pages** (`pdfinfo`)".
   - Problem: `pdfinfo` and `pdftotext` are not installed on this machine (`rlab validate` fails with "pdftotext not found"), so the stated check cannot have been run here. The page count itself is correct.
   - Correct: "The PDF has 5 pages (PDF page tree; the ACM reference line says '5 pages', p. 1)". Keep the request to the lead to fix `metadata.json` `fulltext.pages` via `rlab` (no hand-editing).
4. *Recommendation (not blocking):* in §12 or the Analyst notes, state the MSR track once it can be checked on the DOI landing page. A 5-page paper on a public dataset is likely a short or challenge-track paper, which is a lower evidence tier than a technical-track paper. Do not assert the track without checking.

## borg2026echoes — pass-with-minor-fixes

Verified correct:
- Pre-screening and allocation: 449 / 92.2% / 118 / 106 / 225 (p. 24); 151 participants (33.6%, p. 19); G*Power 128 (p. 19); achieved power 0.57 / 0.17 (p. 19).
- Time handling: 73/151, 67 estimates, 11 values >16 h removed (p. 18); 72 Task 2 times (p. 32).
- Phase 2 outcomes:
  - completion time: 136 vs 173 min, δ −0.079, p = 0.56, 76%, −12.59% (p. 33);
  - interruptions: 173.66% (p. 34);
  - perceived productivity: 3.95 vs 4.06, d −0.21, 84%, −1.26 SD (p. 35–36);
  - CodeHealth: 8.49 vs 8.44, d 0.28, +0.10, 98% (p. 38–39); developer skill +0.16 (p. 40);
  - coverage: 0.70, δ 0.09, 91% (p. 42–43).
- Phase 1: 30.7% median time reduction (p. 43); Bayesian estimate ~60% faster, CrI [−77.11, −30.64] (p. 33); smell shares 55/31, 18/3, 26/8 (p. 38).
- Inconsistencies flagged by the analysis: 55.9 vs 59.6 speedup (p. 1/2/62 vs p. 54); α 0.82 vs >0.85 (p. 18 vs p. 61).
- Conflict of interest (p. 75); data collection closed 18 Jan 2025 (p. 17).

1. **§9 bullet 2 (inconsistencies)**
   - Current: "the 'habitual AI user' threshold is 'Strongly agree' (=5) on p. 15 but '4 or 5' in the pilot assignment on p. 17".
   - Problem: "4 or 5" on Q1-7a is the criterion for assignment to the AI-dev group. It was used in the pilot and then in the main phase ("using the same assignment criteria", p. 17). "Habitual AI users" on p. 15 is the analysis variable, defined as "Strongly agree" only. These are two thresholds for two purposes, not a pilot-only discrepancy. The paper does use the word "habitual" loosely for both.
   - Correct: "The word 'habitual' covers two thresholds: AI-dev group assignment required 4 or 5 on Q1-7a plus a preference median >3 (pilot and main phase, p. 17), whereas the analysis variable 'habitual AI users' means 'Strongly agree' only (p. 15)."
2. **§4 Sample size / §9 inconsistencies (missing item)**
   - Problem: the Task 1 counts are inconsistent and this is not flagged:
     - p. 24 gives "39 valid AI-dev solutions and 37 !AI-dev solutions", i.e. 76;
     - the same page says "AI-devs submitted 38 valid solutions (38 of 118, 32.2%)";
     - p. 28 says "Of the 75 Task 1 solutions, 24 were not evolved further".
   - Correct: add "Task 1 valid solutions are given as 39 + 37 = 76 (p. 24), as 38 AI-dev (p. 24) and as 75 in total (p. 28); the reclassification of one participant (p. 18) explains 38 vs 39 but not 75 vs 76."
3. **§4 Data availability**
   - Current: "The study code base was deliberately not hosted publicly to avoid leakage into LLM training data; it is shared as PDF documents [V] (p. 66)."
   - Problem: p. 74 states "A GitHub repository containing the full code base, scripts for data cleaning and analysis, and notebooks ... is available". This is in tension with p. 66, and the analysis does not mention it.
   - Correct: add "(p. 74 describes a GitHub repository 'containing the full code base'; it is unclear whether this means the RecipeFinder system or the analysis code)".
4. **§13 row "Task 1 developer Java skill had a larger effect on downstream CodeHealth (+0.16) than AI use | 40, 55 | V"**
   - Problem: the comparison "larger than AI use" is the authors' conclusion ("stronger influence on Task 2 outcomes than AI-usage", p. 55). The +0.16 (skill contrast, p. 40) and +0.10 (habitual-AI subgroup, p. 39) come from different contrasts.
   - Correct: one [V] row "Higher Task 1 Java skill: +0.16 CH in Task 2, P > 99%, CrI [+0.07, +0.26] (p. 40)" and one [A] row "Authors conclude skill mattered more than AI use (p. 55)".
   - Also add funding to §10 Reproducibility: WASP (Knut and Alice Wallenberg Foundation) and Swedish Foundation for Strategic Research grant FFL18-0231 (p. 74).

## ehsani2026faster — pass-with-minor-fixes

Verified correct:
- Search and screening: January 2026 search (p. 8); 375,000 hits and 132 grey sources (p. 9); mean 14.4 / SD 2.52 (p. 10); 551 → 49 → 27 + 4 = 31 formal sources, 1,737 snowballed (p. 11–12).
- Agreement: κ 0.93 (p. 13); the agreement of "1.0 ... reflects consensus after reconciliation" quote (p. 9).
- Table 8 counts (p. 16); 58/73 and 11/73 grey sources on strategies (p. 20); 8 / 7 / 10 / 6-of-31 formal sources (p. 21).
- Primary results reported by the review: 87.1% (p. 21); 28,125 prompts (p. 18).
- Review-level findings: "binary correctness" (p. 23); 52% company blogs (p. 30).
- The "small but growing" vs Table 1 "No" tension (p. 7, p. 18).
- References: Della Porta [157] listed under EASE (Table 6, p. 13) but cited as arXiv-only (p. 36); molison2025llm absent from the references (confirmed).

1. **§7 finding 2**
   - Current: "40 grey sources discuss the emerging debt forms (p. 17)".
   - Problem: the paper says "40 sources discuss five emerging forms" (p. 17). The sixth new type, data debt, has 0 grey mentions (Table 8, p. 16).
   - Correct: "40 grey sources discuss five of the six new forms (all except data debt, which is formal-only) (p. 16, p. 17)."
2. **§7 finding 4 (He et al.) and §13 RQ3 row "Cursor adoption ... +30% ... +41%"**
   - Problem: the primary study is in our corpus as he2026speed (ref [90], p. 34). The review reports "a statistically significant large increase ... substantial and persistent increase in complexity and code debt" (p. 18). It omits the primary study's own caveats:
     - the quality effects disappear under the Callaway–Sant'Anna estimator (he2026speed, p. 16);
     - once codebase size is controlled, the increase in warnings runs through code volume (he2026speed, p. 8).

     Keeping this row would double-count one study in the evidence matrix.
   - Correct: keep the [A] label and add "duplicate of he2026speed (ref [90]); cite the primary study, not the review, for this effect". Remove this row from the ehsani evidence table, or mark it "do not count separately".
3. **Version note (line 23) / §12**
   - Current: "The PDF is the arXiv version (arXiv:2606.14796v1, 38 pages)" and, in the Analyst notes, "The TOSEM version may differ from this arXiv v1."
   - Problem: understated. The PDF is a submitted manuscript: every page footer reads "Manuscript submitted to ACM", and the p. 1 citation is a template ("ACM Trans. Softw. Eng. Methodol. 1, 1 (January 2026)"). Its counts are pre-review numbers.
   - Correct: "Our PDF is the pre-acceptance manuscript ('Manuscript submitted to ACM', p. 1 onward); counts may have changed in the published TOSEM article (DOI 10.1145/3820165). Re-check headline counts if the published version becomes accessible."
4. **§9 bullet 2 (Fig. 4)**
   - Current: "grey-source counts for 2025 (84 + 25 = 109) exceed the 73 grey sources (p. 19)".
   - Problem: these values are not in the text layer; they come from the figure image. That is acceptable, but the claim cannot be traced in `fulltext.txt`.
   - Correct: append "(values read from the Fig. 4 image; not in the text layer)".

## fawzy2026vibe — pass-with-minor-fixes

Verified correct:
- Corpus: 154 / 101 / 53 = 40 + 13 sources (p. 5); 518 units split 140/132/114/132 (p. 5–6).
- Tables 2–5: 87/62%, 20/14%, 15/11% (p. 6); 85/64%, 17/13%, 14/11% (p. 8); 78/68%, 22/19%, 5/4%, 5/4%, 3/3% (p. 8); 48/36%, 38/29%, 24/18%, 13/10%, 6/5% (p. 8).
- Method: quality threshold ≥10/15 (p. 4); the exclusion criterion "Experienced developers applying critical oversight without skipping QA" (p. 4, a sub-item of "No firsthand behavior"); mainly the first author coding, with "a subset" cross-validated (p. 4–5).
- Zenodo package (p. 11).

1. **§5**
   - Current: "Exact search date: not reported (reference access dates fall in May-July 2025, p. 11)".
   - Problem: access dates run from 01/05/2025 to 11/08/2025. One reference was accessed 11/08/2025, i.e. 11 August 2025 in the DD/MM format the paper uses.
   - Correct: "Exact search date: not reported (reference access dates range from 1 May to 11 August 2025, p. 11–12)."
2. **§9 bullet 1 (units read as people)**
   - Problem: a third instance is missing. On p. 9 the paper writes "About 14% of vibe coders are motivated ...". That 14% is the Accessibility & Empowerment share of motivation *units* (20/140, p. 6), not a share of people.
   - Correct: add "... and 'About 14% of vibe coders are motivated' (p. 9), which is 20/140 motivation units (p. 6)".
3. **§9 bullet 2 (selection bias)**
   - Problem: the bias is stronger than the analysis states. The *inclusion* criteria also require behavioural evidence such as "AI-generated code used as-is or with light edits ... minimal or no testing, review" (p. 4), in addition to the exclusion criterion already cited.
   - Correct: add "Inclusion additionally required evidence of 'minimal or no testing, review' (p. 4), so low-QA behaviour is partly a selection criterion rather than only a finding."

## he2026speed — pass-with-minor-fixes

Verified correct:
- Table 2: +28.58 / +30.26 / +7.03 / +41.64 (p. 7).
- Month-level velocity effects: 55.4 / 14.5 / 281.3 / 48.4 (p. 8).
- GMM: −0.011 and 0.086 (Table 3, p. 8); 64.5 / 50.3 / 1.84x (p. 8); 14,755 observations (p. 8).
- Sample: 806 / 3,306 / 23,308 (p. 4); 1,380 (p. 2); Table 7 801 / 1,172 / 21,699 / 4,481 (p. 17).
- Robustness: 382 / 345 repos with other AI tools (p. 10); TWFE +18.48 / +26.04 and CS −10.49 / −3.80 (p. 16).
- Warning analysis: 195,010 warnings, taxonomy with Claude Opus 4.5 (p. 18).
- 25.1% / 25% complexity statements (p. 10, p. 11); ITT quote (p. 7); "appropriate caution" quote (p. 16); Zenodo package (p. 11).
- The analysis correctly read significance from the image: the text layer attaches stars to every cell, including the n.s. CS row.

1. **Frontmatter `main_finding`**
   - Current: "persistent +30% static-analysis warnings and +42% cognitive complexity".
   - Problem: the paper reports +41.64% (Table 2, p. 7), "41.6%" (p. 8) and "41%" (abstract, p. 2); "42%" is our rounding and appears nowhere in the paper. This value feeds the literature matrix.
   - Correct: "+30% static-analysis warnings and +41.6% code complexity".
2. **§9 bullet 2 (sample counts)**
   - Problem: the analysis lists 806/1,380 vs 801/1,172 but misses that 1:3 nearest-neighbour matching (p. 5) of 806 treated repos would give up to 2,418 controls, not 1,380. Controls must have been reused across treated units or cohorts, which matters for independence and is not explained.
   - Correct: add "With 1:3 matching (p. 5), 1,380 distinct controls for 806 treated repos (p. 2) implies controls were reused across treated units or cohorts; the paper does not explain this."

## kim2026programdistill — pass-with-minor-fixes

Preprint correctly flagged ("preprint, not peer-reviewed", arXiv v1, 16 Sep 2026).

Verified correct:
- Mining and tasks: 2,800 / 2,350 / 2,165 / 1,975 behaviours (p. 7); 4,063 tasks; depth max 17, mean 3.40 (p. 7); 572 merges (p. 6).
- Evaluation suite: 300-task quotas (p. 8).
- Partial-repair results: 84.3 / 68.7 / 60.7 and $33.99 / $28.86 / $16.01 (p. 8); depth 100→64.0, 96→32, 92→32 (p. 8–9); Table 9 92.9 / 76.9 and 76.4 / 46.9 (p. 38).
- Full reconstruction: 58.98 / 49.15, 42.03 / 28.81, 33.39 / 21.07 (p. 11); 81.8 MailHub / 5.9 Baserow (p. 11); 977 failures, 59.2 / 1.8 / 11.1 / 27.9% (p. 12); failure classification done by GPT-6 Astra (p. 12).
- Trajectory statistics: 9.3x / 10.7x / 34.60→8.46 / 11.1→24.6% (p. 9–10); 96.3 / 9.9 steps (p. 9).
- Context-length check: 40–80k band 82.6→24.2 (p. 39); Pearson −0.20 to −0.05, pooled +0.11 (p. 40).
- Shortcut attempts: 7.2 / 19.0 / 17.7 / 0.3% (p. 10).
- `handle(req, res, context)` (p. 37); selectors must match (p. 35); ExpenseFlow 2 to Reactive Resume 372 tasks (p. 19).

1. **§5 "Number of runs" and frontmatter `sample_size`**
   - Current: "[V] Number of runs: one per model and task (partial) and one per model and app (36 full-reconstruction runs, p. 12)" and frontmatter "300 tasks x 9 models (1 run each)".
   - Problem: the paper states 36 runs for full reconstruction (12 apps × 3 models, p. 11–12) but never states the number of runs per task for partial reconstruction. "One run" is an inference from the absence of variance reporting, so the [V] label is not supported.
   - Correct: "[V] Full reconstruction: 36 runs = 12 apps × 3 models (p. 11–12). [I] Partial reconstruction: runs per task not stated; no variance reported, so presumably one." Frontmatter: "300 tasks x 9 models (runs per task not stated)".
2. **§9 (missing reporting issue)**
   - Problem: the abstract says "Across nine frontier coding agents, GPT-6 Astra and Claude Opus 5 achieve 49.2% and 28.8% success on cumulative workflows in full-application reconstruction" (p. 1). Only three models were run in full reconstruction (p. 11). Read naively, the abstract implies "best of nine" for the headline full-rebuild number.
   - Correct: add "[I] The abstract places the full-reconstruction results under 'nine frontier coding agents' (p. 1), but only 3 models were evaluated in that setting (p. 11); synthesis should not describe 49.2% as best-of-nine."
3. **§9 bullet 1**
   - Current: "a single Node `handle()` entry with in-memory `context.state` (p. 37)".
   - Problem: the paper says state is kept in `context.state` "so the verifier can reset it" (p. 37). "In-memory" is our inference.
   - Correct: "with application state kept in `context.state` so the verifier can reset it (p. 37)". If "in-memory" is kept, mark it [I].

## liu2026benchmarking — needs-fixes

Identity confirmed from the ACL footer (p. 1).

Verified correct:
- Benchmark size: 46 / 244 / 703 (p. 3).
- Table 3 values:
  - best setting 53.75 ± 0.43 and 69.41 ± 1.07 (p. 6);
  - the 42.30–53.75 band (p. 6);
  - GPT-4o-mini Vanilla 44.82 vs ChatDev 33.16 and MapCoder 41.30;
  - GPT-4o Vanilla 45.95 vs ChatDev 42.71;
  - MetaGPT 0.00–5.39;
  - ±0.00 rows for Qwen.
- Annotation agreement: Fleiss κ 0.47 → 0.83 → 0.79 (p. 12–13); 0.81 (p. 14); 0.23 (p. 15, p. 17).
- Human vs automatic evaluation: Cohen κ 0.86 / 0.74 (p. 22); 295 instances (p. 21).
- Costs: 3.5 h and $0.48 per project (p. 15–17).
- OpenHands / SWE-Agent 43.45 / 44.73 vs 48.69 (p. 23).
- 44% of MetaGPT failures are code inconsistency (p. 8).
- Reporting inconsistencies "four domain experts" vs "5 professional annotators" and "30 different models" (p. 7, p. 21).
- Data-testid anchors supplied in the prompt (p. 16–17).

1. **§7 finding 3 and §13 RQ1 row (factual error, labelled [V])**
   - Current: "Multi-agent frameworks cost up to ~12x more and take longer (e.g. GPT-4o ChatDev $0.1947 vs Vanilla $0.0160) (p. 6). [V]" and, in the evidence table, "cost up to ~12x more".
   - Problem: the paper states no "12x". The ratio is our calculation, and "up to" is wrong. From Table 3 (p. 6):
     - Qwen-7B ChatDev $0.0075 vs Vanilla $0.0003 (≈25x);
     - Qwen-7B MetaGPT $0.0207 vs $0.0003 (≈69x);
     - Claude-Haiku ChatDev $0.174 vs $0.015 (≈11.6x).

     Also, the multi-agent Self-Collaboration costs about the same as Vanilla (Claude-Haiku $0.014 vs $0.015; GPT-4o $0.0155 vs $0.0160), so "multi-agent costs more" is not universal.
   - Correct: "[V] Most multi-agent frameworks (MapCoder, ChatDev, MetaGPT) cost several times more than Vanilla, e.g. ≈12x for GPT-4o ChatDev ($0.1947 vs $0.0160) and up to ≈25x (ChatDev) and ≈69x (MetaGPT) on Qwen-7B, on small absolute costs; Self-Collaboration costs about the same as Vanilla (p. 6, Table 3)." Update the evidence-table row in the same way.
2. **§9 bullet 3 (inconsistent reporting, missing item)**
   - Problem: the strict Req.Acc values in Table 10 (p. 25) do not match Table 3 (p. 6). Examples: GPT-Engineer + Claude-Haiku 0.5402 vs 53.75; GPT-Engineer + GPT-4o 0.5037 vs 50.83. §7 finding 2 quotes 0.5402 next to the Table 3 figure without noting the difference.
   - Correct: add "Strict Req.Acc in Table 10 (p. 25) differs from Table 3 (p. 6) by 0.2–0.5 points (e.g. 0.5402 vs 53.75); possibly a single run vs the three-run mean; not explained."

## lu2025webgen — pass-with-minor-fixes

Verified correct:
- Test set: 101 instructions / 647 test cases (p. 5–6); 6,667 training instructions (p. 5); 10,152 descriptions and forty PhD students (p. 2, p. 5).
- Table 3 (p. 8): 27.8 / 26.4 / 20.8 / 9.0 / 14.1, start failures 38.6 / 32.1, 9.5 → 38.2.
- Training size: Table 6 25.1 / 31.9 / 38.2 (p. 10).
- Table 4 (p. 9): 21.1 vs 44.3, 17.1 vs 52.0.
- Table 5 (p. 9): 90.3 / 86.1 / 94.4.
- Human testing cost: 10.8 h / $377.8 (p. 6).
- UI agent limited to at most 15 interactions (p. 19).
- No error bars (p. 40).

1. **§4 Sample size, §9 bullet 4, §13 last row (647 vs 667)**
   - Current: "total 667 in Table 8 (p. 23), which does not match the 647 stated elsewhere" and the evidence row "Test-case total inconsistent (647 in text vs 667 in Table 8), illustrating weak reporting of benchmark composition".
   - Problem: the three main categories in Table 8 sum to 339 + 186 + 122 = 647 (p. 23). The printed "Total 667" is an arithmetic or typographical error in that row, not evidence of a different test set.
   - Correct: "Table 8's main categories sum to 647 (339 + 186 + 122), matching the text; its printed total of 667 is a typo (p. 23)." Downgrade or delete the RQ4 evidence row.
2. **§9 bullet 2**
   - Current: "with 59–74% NO labels (p. 9, Table 5)".
   - Problem: Table 5 NO rates are 64.1 / 64.3 / 73.9 for the UI agent and 59.0 / 58.1 / 70.3 for manual testing.
   - Correct: "with 58–74% NO labels (p. 9, Table 5)".
3. **Metadata (escalation to the lead; the analysis already notes it)**
   - Problem: `metadata.json` lists 10 authors, including "Hou, Haotian" as 4th. The PDF (p. 1) lists 9 authors: Lu, Yang, Ren, Xiao, Wang, Shi, Zhou, Zhan, Li.
   - Required: the lead should re-resolve DOI 10.52202/085713-2419 with `rlab`, without hand-editing. If the published NeurIPS version differs, record which version page refs refer to. Check `references.bib` before any document cites this key.

## mock2026vibe — pass-with-minor-fixes

Verified correct:
- Table 16 (p. 41–42): TPR 94.58 / 62.0 / 60.8 / 83.3; MCC 11.67 / 6.44 / 6.57 / 6.0; BCB 65.33 / 83.89 / 79.00; time 75 / 800 / 2,057 / 2,266 s.
- Table 9 (p. 25): agentic > solo U = 106.5, δ 0.97, p = 7.81e-05; collaborative vs solo U = 36.5, p = 0.314.
- Table 10 (p. 27): MCC collaborative vs solo p = 0.479.
- Table 12 (p. 30): 88.5 / 6.42e-03 / 7.31e-03.
- Iterations: 12.1 / 5.6 (p. 31, p. 33).
- Models: GPT-3.5 Turbo (p. 14, p. 17); ChatGPT 5 "most similar" (p. 17).
- Design statements: Static-Group Comparison (p. 14) and "randomly assigned" (p. 15); 15–25 participants as the typical range (p. 13).
- Quote that the agentic workflow "statistically produces higher-quality code" (p. 40, end of §8 Related Work); P7 8.3% and P13 100% (p. 26).
- Volume and year: (2027) 32:40.

1. **§2 hypotheses, §9 and §10 Statistical conclusion (missing statistical-reporting problem)**
   - Problem: the one-tailed tests in Tables 9 and 10 are internally inconsistent in direction. Examples:
     - TPR "collaborative > agentic: U = 69.5, effect size −0.65, p = 8.55e-03**" and "fully-automated > agentic: δ −1.00, p = 3.79e-03**" (Table 9, p. 25);
     - MCC "collaborative > agentic: δ −0.77, p = 3.13e-03**" (Table 10, p. 27).

     Under the stated H0 (A ≤ B), a negative δ should give a large one-tailed p. The small p-values evidently test the reverse direction. Meanwhile "collaborative > solo-coding: δ −0.16, p = 0.314" is also below 0.5. The substantive reading in the analysis (agentic higher TPR and MCC) agrees with the group means (p. 41–42). However, the analysis repeats "H0: A <= B, per Tables 9-13" without noting that the reported test directions cannot be trusted.
   - Correct: add to §9: "[I] Test direction is reported inconsistently: several rows with negative Cliff's δ carry small one-tailed p-values (e.g. collaborative > agentic, δ −0.65, p = 0.0086, Table 9, p. 25; δ −0.77, p = 0.0031, Table 10, p. 27). This suggests the reverse alternative was tested and labels were not updated. Conclusions are consistent with the means (p. 41–42), but individual p-values should not be quoted without this caveat." Add a pointer to this in §10.

## molison2025llm — pass-with-minor-fixes

Verified correct:
- Setup: GPT-4o-2024-08-06, temperature 1.00, top-p 1.00, 2048 tokens (p. 4); 80 / 240 / 160 / 480 questions, loss 0.21, 496,176 tokens (p. 4); the few-shot prompt contains all human solutions to the same question (p. 4).
- Table I blocker shares 87.50 / 71.27 / 86.30 (p. 8).
- Table II, Table III (3.57 / 0.52 / 0.00) and Table IV (0.54 / 0.21 / 0.1, 0.24, −0.50) (p. 8).
- Effort minutes 7.20 / 3.75 / 4.72 / 5.00 / 7.06 / 5.48 / 6.13 / 4.67 / 6.95 / 6.14 / 7.33 / 7.60 (p. 7).
- Table V Pass@1 1.0 / 0.53 / 0.87 / 0.47 and partial shares 47% / 13% (p. 8).
- Severity share: 94.1% minor for fine-tuning (p. 6).
- Inconsistencies flagged by the analysis: "≤ 0.19%" (p. 9), "half as likely" (p. 7), "GPT-4" (p. 10), 0.86 vs 0.87 (p. 1 vs p. 8).
- Zenodo package (p. 11).

The few-shot leakage critique is the most important point in the analysis and is correct.

1. **§13 first row**
   - Current: "(OR 0.0005–0.019, p<0.001)".
   - Problem: Table II fine-tuned vs human, introductory, is "0.00***" (p. 8), so the range starts at 0.00. Because an OR of 0.00 implies a zero cell, the minimum is not a real estimate.
   - Correct: "(OR 0.00–0.019, all p<0.001; the 0.00 implies a zero cell)".
2. **§9 inconsistency bullet 2**
   - Current: "Finding 7 says odds of bugs are '≤ 0.19%' (p. 9), but Table II includes 0.019, i.e. 1.9% (p. 8)."
   - Problem: an odds ratio is not a percentage. The inconsistency is only valid under the paper's own convention of writing ORs as percentages ("0.05% of the odds ... 0.8% ... 0.6%", p. 6).
   - Correct: "Under the paper's own convention of expressing ORs as percentages (OR 0.0005 written as '0.05% of the odds', p. 6), the largest bug OR in Table II (0.019, p. 8) is 1.9%, not '≤ 0.19%' as stated in Finding 7 (p. 9)."

---

## Cross-paper observations

1. **Double counting of he2026speed.** ehsani2026faster cites he2026speed as ref [90] and repeats "+30% warnings, +41% complexity" (ehsani p. 18). The evidence matrix should cite [@he2026speed, p. 7] once and treat the ehsani mention as second-hand. Ehsani omits the primary study's estimator sensitivity (Callaway–Sant'Anna estimates are negative and n.s., he2026speed p. 16) and the GMM result that warnings rise mainly through codebase size (he2026speed p. 8).
2. **Apparent contradiction for the evidence matrix "Contradictions" section (RQ3).**
   - What conflicts: molison2025llm finds GPT-4o code has far lower odds of SonarQube bugs than human code (Table II, p. 8). he2026speed finds Cursor adoption raises SonarQube warnings by 30.26% (p. 7).
   - Possible explanations, to be recorded as [I] only:
     - unit: per-solution odds vs repository totals;
     - baseline: APPS competitive-programming submissions vs matched OSS repos;
     - generation mode: one-shot GPT-4o vs agentic Cursor in evolving projects;
     - size: he's warnings effect disappears once lines of code are controlled (p. 8).
3. **Maintainability signals at different scales (RQ3/RQ4).** The four studies use different metrics at different granularities, so they must not be aggregated into one "AI code is more or less maintainable" claim:
   - borg2026echoes: no hand-off maintainability difference, with +0.10 CodeHealth for habitual users (file-level, LoC-weighted CodeHealth; 2 KLoC system; 2024 chat/completion tools; p. 38–39);
   - he2026speed: +41.64% total cognitive complexity (repository-level; agentic Cursor; p. 7);
   - mock2026vibe: agentic McCabe 11.67 vs ~6.5 (single function; MetaGPT X; p. 41–42);
   - molison2025llm: mixed code-smell odds ratios (single algorithmic solutions; p. 8).

   The borg analysis already makes this point against he2026speed. Extend it to mock and molison.
4. **Functional-fidelity headline numbers are not comparable (RQ2).** The three benchmarks differ in input, oracle and model generation:

   | Study | Headline | Input | Oracle | Models |
   |---|---|---|---|---|
   | kim2026programdistill | 49.15% cumulative workflows (p. 11) | live reference app | trace replay; selectors must match | 2026 |
   | liu2026benchmarking | 53.75% Req.Acc (p. 6) | detailed requirements with supplied `data-testid` | BDD tests | 2025 |
   | lu2025webgen | 27.8% (p. 8) | NL instruction only | UI agent; half credit for PARTIAL | early 2025 |

   Do not rank approaches across these papers.
5. **Shared construct threat: DOM identity.** kim (selectors and accessible names must match, p. 35) and liu (`data-testid` anchors from the original, p. 16–17) both mix behavioural fidelity with naming identity. lu avoids anchors but uses an LLM judge. This shared weakness supports a gap: an anchor-free, non-LLM fidelity oracle. Any gap claim still needs a novelty check.
6. **Shared threat: self-preference.** In three benchmarks the model that builds the benchmark is also evaluated:
   - kim: GPT-5.6 Sol builds traces, masks and statements and is evaluated; GPT-6 Astra classifies the failures;
   - liu: GPT-4o annotates and is evaluated;
   - lu: GPT-4o writes the instructions and test cases and is evaluated.

   Record this as a cross-study weakness under RQ4.
7. **"Vibe coding" is operationalised in five incompatible ways:**
   - fawzy: minimal-review prompting (p. 1);
   - asdaque: supervise-and-validate, proxied by "opened agentic PRs" (p. 1–2);
   - mock: human-written TDD tests plus scripted, unmodifiable prompts (p. 15);
   - he: adoption of Cursor configuration files (p. 4);
   - ehsani: fast-integration debt (p. 17).

   The evidence matrix must not pool these under one "vibe coding" label.
8. **Consistent finding: developer skill.** asdaque (low-experience users' agentic PRs carry more review overhead, p. 3) and borg (the original developer's Java skill had a larger effect on CodeHealth, p. 40, p. 55) both point to operator skill as a factor that a reconstruction study must measure or control. This is consistent, but the two constructs differ: a GitHub activity rate vs self-reported Java proficiency.
9. **Consistent finding: quality and correctness diverge.** molison (fine-tuned model has the best static quality but the lowest Pass@1, p. 8) and mock (agentic code is most correct but most complex, p. 41–42) both support measuring fidelity and quality jointly in RQ5.
10. **Version and pagination risk.** Six analyses cite arXiv pagination for published papers. Three of those PDFs are explicitly pre-acceptance (fawzy, ehsani, lu). Any quote reused in a review or report should keep the arXiv page ref and name the version.
