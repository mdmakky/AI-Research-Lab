---
key: wu2026looks
status: ready
evidence_basis: full-text
design: benchmark construction + five-axis empirical evaluation of six frontier MLLMs in a fixed single-agent harness; VLM-judge validation; failure taxonomy on labelled sample
dataset: MobileForge: 29 in-market consumer mobile apps, 309 human-reviewed screenshots, page-relationship annotations, 701 navigation test specifications
sample_size: 29 apps x 6 models = 174 runs (single trial each); 701 navigation specs; 55 human-ranked scenarios; 64 hand-labelled failures
metrics: Build success (tsc+vite), NavPassRate (state-isolated Playwright tests), list-wise Borda visual score (anchor-referenced VLM judge) + point-wise rubric, LoC, LoC/file, ReuseRate, DeadCompRate, ColorConsistency, tokens/cost
main_finding: All models build multi-screen React apps; navigation 58-92% pass; visual fidelity <=2.99/5; visual leader (Opus 4.6) is not maintainability leader (GPT-5).
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Looks Right, Works Right: A Project-Level Benchmark for Multi-Screen Mobile App Generation

- Authors: Wu, Fan; Gao, Cuiyun; Huang, Yiming; Xiao, Yang; Chen, Yujia; Liao, Qing
- Year / venue: 2026, Proceedings of the 2026 Conference on Empirical Methods in Natural Language Processing (published)
- DOI: 10.18653/2026.emnlp-main.2650 · URL: https://doi.org/10.18653/2026.emnlp-main.2650
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- Introduce MobileForge, a benchmark for project-level multi-screen mobile app generation from a folder of real app screenshots, with a five-axis evaluation (build, navigation, visual fidelity, code maintainability, efficiency), and use it to measure how far frontier multimodal LLMs are from producing a buildable, navigable, faithful and maintainable codebase [A] (pp. 1–2).

## 2. Research questions / hypotheses
- Opening question: "Can a multimodal LLM read a folder of mobile-app screenshots and generate the source code for that app?" [V] (p. 1). No formal hypotheses. The paper targets three gaps of existing benchmarks: single-page focus, no evaluation of interactive navigation, no project-wide maintainability measure [A] (p. 1).

## 3. Methodology
- Research design: benchmark construction (VLM-drafted, human-reviewed annotations) plus a full-factorial evaluation of 6 models × 29 apps with a fixed agentic harness, single trial per cell; method studies of the visual judge (human alignment, cross-judge, protocol comparison); hand-labelled failure taxonomy [V] (pp. 3–8, 12–13).
- Approach / model / intervention: one tool-augmented agent receives all screenshots of an app plus the human-reviewed page-relationship description and must produce a React + TypeScript + Tailwind project in a pre-scaffolded directory; eight tools (write_file, read_file, str_replace, batch_str_replace, list_files, delete_file, run_command, task_done), soft six-phase plan, up to 50 iterations; on task_done an automated tsc + vite build feeds errors back [V] (p. 6). Prompting is fixed across models, with no screenshot-specific instructions or chain-of-thought, to attribute differences to the model [A] (pp. 6, 14).
- Baselines or comparison conditions: six closed models available April 2026 — Claude Opus 4.6, Claude Haiku 4.5, GPT-5, GPT-5 Mini, Gemini 2.5 Pro, Gemini 2.5 Flash [V] (p. 6). No open-weight models and no non-agentic or prior-method baselines [I] (based on p. 6).

## 4. Dataset and sample
- Data source(s): 29 in-market consumer apps from official public distribution channels; screenshots captured manually from default-state or demo-mode screens without logging in [V] (pp. 3, 9).
- Sample size (N) and unit: 29 apps across 14 category buckets; 309 screens (mean 10.7, SD 3.8, range 5–21 per app); 701 navigation test specifications (mean 24.2, range 11–41 per app): 120 page-existence, 392 tab-navigation, 189 parent–child [V] (p. 3). Apps include Notion, Khan Academy, WhatsApp, Klook, Airbnb, Coinbase and others (Table 5) [V] (p. 12).
- Sampling / selection method: apps "prioritizing broad cultural recognition" [V] (p. 3) — a purposive, not random, selection. Annotation: a VLM drafts the page-relationship description and test specs; research-team annotators review every field; auto-drafts reach 96.8% recall / 94.3% precision (pages) and 74.1% / 83.9% (test cases); 64.7% of page and 76.5% of test drafts accepted unchanged [V] (pp. 3, 9, 15). The drafting VLM is not named — not reported. Inter-annotator agreement — not reported.
- Data availability (public? link?): https://github.com/anoa12159-hue/mobileforge_eval, research-only licence, with screenshots, annotations, harness, evaluator and all 174 run artifacts [A] (pp. 1, 9–10).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: single trial per (app, model) cell, 174 runs all completed [V] (p. 6). Build: clean Vite scaffold (React 19 + TypeScript + Tailwind), `npx tsc --noEmit` and `vite build` must both pass with zero errors [V] (p. 4). Navigation tests run in headless Playwright (375×812 viewport) [V] (p. 5). Visual judge: Gemini 2.5 Pro, list-wise with k-shuffle = 3 and reference anchor over 29 apps × 701 scenarios [V] (pp. 6, 13). Sampling temperature and other decoding settings — not reported.
- Code availability: repository above; "one-command replay reproduces the comparison table verbatim" [A] (p. 10). Full system prompt only in the repository [V] (p. 14).

## 6. Evaluation metrics
- Build Success — both type-check and build pass; also route count, page-file count, route coverage [V] (p. 4).
- Navigation Correctness — NavPassRate: share of the 701 specs passed under state-isolated execution: each test starts by loading the source page route directly, performs the action, and passes if the URL matches the expected page or, for overlays, the page content hash "changes meaningfully" [V] (pp. 4–5). Rationale: chained walkthroughs cascade failures and blur attribution [A] (p. 5).
- Visual Fidelity — primary: per-model Borda score in [0, 1] from list-wise ranking by a VLM judge, with the original screenshot hidden among candidates as an anchor; rankings where the anchor is not first are discarded and re-run [V] (pp. 4–6). Secondary: point-wise 1–5 rubric (Layout 30%, Style 25%, Content 25%, Consistency 20%) kept as an absolute reference [V] (p. 6).
- Code Maintainability — total LoC; mean LoC/file (conciseness); ReuseRate (mean import count per shared component); DeadCompRate (share of declared components never imported); ColorConsistency (share of Tailwind colour tokens from a small recurring palette) [V] (p. 4). The authors use "maintainability" rather than "code quality" because correctness is covered by Build [A] (p. 4). These indicators are not validated against human maintainability judgements or established maintainability models — not reported.
- Efficiency — input/output tokens, LLM call count, wall-clock LLM time, dollar cost from list prices [V] (p. 4).
- Validation against human judgement (visual judge): 55 scenarios labelled with a blinded ranking interface — list-wise vs human strict Kendall τ = 0.716, top-1 accuracy 83.6%, top-2 overlap 80.4%, unrankable-set IoU 0.968; τ = 0.699 for page-existence and 0.731 for parent–child scenarios [V] (p. 13). Number and expertise of human raters and their agreement — not reported. Cross-judge: Claude Sonnet 4.5 on 139 scenarios from 5 apps gives inter-judge τ = 0.867 on the per-model ranking; no self-preference observed [V] (p. 13). Protocol smoke test (3 scenarios × 5 models): list-wise shuffle stability τ = 0.822, pair-wise position bias 23.3%, point-wise "ties-in-the-middle" [V] (pp. 12–13). Judge eligibility: Gemini 2.5 Pro and Claude Sonnet 4.5 ~100% anchor pass on a 33-scenario screening set; GPT-5.1 ~35% [V] (pp. 5, 13).
- Navigation evaluator validity: Table 11 reports false positives of the automatic evaluator among flagged cases (6% page existence, 1% parent–child, 10% tab navigation) [V] (p. 16).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): Wilson 95% CIs for failure-mode proportions [V] (p. 8); ±1 SD error bars across apps in the cost plot [V] (p. 7). No significance tests for model differences; no run-to-run variance (single trial) [V] (pp. 6, 9).

## 7. Key findings
1. Build success is 100% for all six models; authors attribute this to the harness's verify-repair loop, not the model [V] (pp. 6–7, 12).
2. NavPassRate: Opus 4.6 92%, GPT-5 89%, Haiku 4.5 85%, Gemini 2.5 Pro 82%, Gemini 2.5 Flash 62%, GPT-5 Mini 58% [V] (p. 7).
3. Visual fidelity has not saturated: Borda 0.906 (Opus) to 0.130 (GPT-5 Mini); point-wise means 1.60–2.99/5, so even the best model stays below 3/5; Opus leads in 26 of 29 apps [V] (pp. 6–7). The gap is concentrated in cross-page Consistency: models re-implement navigation chrome inline per page instead of sharing a component [A] (p. 6).
4. Maintainability is dissociated from visual fidelity: Opus writes 1,441 LoC (82 LoC/file) vs GPT-5 668 (33 LoC/file); GPT-5 has higher reuse (4.23 vs 3.83) and fewer dead components (7.8% vs 19.9%); ColorConsistency saturates at 0.74–0.85 [V] (pp. 6–7). Authors: "maintainability is uncorrelated with visual fidelity" [A] (p. 8) — no correlation coefficient is computed.
5. Cost: $0.15 (GPT-5 Mini) to $2.90 (Opus) per app; GPT-5 ($0.50, Borda 0.542, NavPass 89%) dominates Haiku 4.5 and Gemini 2.5 Pro on cost and quality [V] (p. 7). Cheaper models fabricate content (Lorem ipsum, stock imagery) [A] (p. 7).
6. Navigation failure taxonomy (n = 64 stratified hand-labelled failures from 3,486 executions): C1 blank starting page 7.8% [3.0, 18.3]; C2 route mapping error 10.9% [5.4, 20.9]; C3 target unreachable/occluded 32.8% [22.6, 45.0]; C4 click has no effect 48.4% [36.6, 60.4] [V] (p. 8). C4 (missing or mis-wired onClick) dominates for Opus and GPT-5 (75% of their labelled failures); C3 for GPT-5 Mini (67%); C1 for Gemini 2.5 Flash (42%) [V] (pp. 8, 15). Build checks do not catch silent event-handler bugs [A] (p. 8).
7. Per-app difficulty varies widely: point-wise visual 3.62 (Notion) to 2.01 (Apple News); NavPass 0.45 (Medium) to 1.00 (Khan Academy) [V] (pp. 7, 12).

## 8. Limitations stated by the authors
- Single trial per cell; multi-trial replication left to future work [A] (p. 9).
- Visual scores come from Gemini 2.5 Pro, a competitor model class; mitigated by fixed judge, human calibration on 55 scenarios and a cross-judge check [A] (p. 9).
- Web-rendering proxy: output is React + Tailwind, not native iOS/Android; native APIs not exercised [A] (p. 9).
- Anchor-based judging depends on judges that follow the literal ranking instruction (GPT-5.1 fails) [A] (pp. 13–14).
- Per-model failure proportions (n = 8–12) are "descriptive signatures rather than precise point estimates" [A] (p. 8).
- Build success cannot discriminate models when a verify-repair loop is present [A] (p. 12).

## 9. Limitations we identified
- [I] Input is not screenshots alone: the agent also receives a human-reviewed page-relationship description (tab structure, parent–child triggers) (pp. 3, 6), although related work frames the benchmark as using "only screenshots" without "any structural prior" (p. 2). Results therefore describe reconstruction with an annotated navigation map, not pure black-box observation.
- [I] Maintainability indicators are structural proxies (LoC, reuse, dead components, colour tokens) with no validation against developer judgement or standard metrics (complexity, duplication, smells, tests). LoC partly reflects how much content is reproduced, so "more LoC" is not clearly worse (p. 4, 7).
- [I] "Uncorrelated"/"orthogonal" is asserted from six model means (p. 8); no correlation is computed at app or run level.
- [I] Internal inconsistency in failure analysis: overall C4 = 48.4% (Table 4, p. 8), but the per-scenario-type projection (Table 11, p. 16) gives C4 of only 33% (parent–child) and 3% (tab navigation), which cannot average to 48.4% over the 581 interactive specs. The projection method or labels may differ; this needs clarification.
- [I] Human validation of the visual judge: 55 scenarios with unreported number of raters, rater expertise and inter-rater agreement (p. 13); the protocol comparison uses only 3 scenarios × 5 models (p. 12).
- [I] NavPass counts a pass when the content hash "changes meaningfully" for overlays (p. 5) — a lenient criterion; Table 11 shows 1–10% false positives in flagged cases (p. 16), but overall evaluator precision/recall on passes is not reported.
- [I] Well-known apps chosen for "broad cultural recognition" (p. 3) are likely represented in model training data; contamination is not discussed.
- [I] Single run per cell with stochastic agents; differences of a few NavPass points (e.g. Opus 92% vs GPT-5 89%) may be within run-to-run noise.
- [I] Navigation evaluated only as page transitions; in-page behaviour, state, data and back-end logic are not tested.

## 10. Threats to validity
- Internal (confounds, leakage, selection): annotations drafted by an unnamed VLM, possibly from the same families evaluated; Gemini 2.5 Pro is both judge and candidate (self-preference check reported, p. 13); popular apps may be memorised [I].
- External (generalisability of sample/context): 29 apps, 5–21 screens each; web proxy instead of native; one harness design; closed models only [I].
- Construct (do metrics measure the concept?): NavPass measures routing, not full functional fidelity; Borda is relative (ordinal) and depends on the set of models compared; maintainability proxies unvalidated [I].
- Statistical conclusion (power, multiple comparisons, variance): single trial; no significance tests between models; Wilson CIs only for the failure sample (n = 64), per-model n = 8–12 [I].
- Reproducibility (data/code/setup reported?): strong — benchmark, harness, evaluator and run artifacts released, one-command replay (pp. 9–10); decoding settings and drafting VLM not reported; closed models may change [I].

## 11. Future research directions
- Stated by authors [A]: multi-trial replication (p. 9); cross-platform/native extension (p. 9); stricter build gates (no `any`, strict null checks, lint) if compilation is to discriminate models (p. 12).
- Suggested by us [I]: test pure screenshot-only input (without the page-relationship description) and interaction recordings as input; add in-page behavioural tests and data/state checks; validate maintainability proxies against developer ratings and standard static-analysis metrics; report run-to-run variance.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ3, RQ4, RQ5.
- How it informs our work [I]: MobileForge is the closest existing design to our target study: it rebuilds whole multi-screen apps from screenshots of real, in-market apps with an agentic (vibe-coding-like) harness and scores functional navigation fidelity, visual fidelity and maintainability together. It shows these dimensions diverge (visual leader ≠ maintainability leader), giving direct support for joint evaluation. Its gaps — structural prior given as input, unvalidated maintainability proxies, single trials, no behaviour beyond navigation — are concrete design points for RQ5.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Single-agent tool-using harness (8 tools, ≤50 iterations, tsc+vite repair loop) rebuilds React+TS+Tailwind projects from app screenshots plus a page-relationship description | p. 6 | V | moderate |
| RQ2 | Navigation fidelity via 701 state-isolated Playwright tests: NavPass 58% (GPT-5 Mini) to 92% (Opus 4.6); build 100% for all | p. 7 | V | moderate |
| RQ2 | Visual fidelity not saturated: point-wise means 1.60–2.99/5; Borda 0.13–0.91 | p. 6–7 | V | moderate |
| RQ2 | Navigation failures: click has no effect 48.4%, target unreachable 32.8%, route error 10.9%, blank page 7.8% (n = 64, Wilson CIs) | p. 8 | V | weak |
| RQ3 | Maintainability proxies (LoC, LoC/file, reuse, dead components, colour consistency): GPT-5 668 LoC, 7.8% dead vs Opus 1,441 LoC, 19.9% dead | p. 4, 7 | V | moderate |
| RQ3 | Visual-fidelity leader is not maintainability leader; authors call them uncorrelated (no coefficient computed) | p. 6–8 | A | weak |
| RQ4 | Anchor-referenced list-wise VLM judge vs human ranking on 55 scenarios: Kendall τ = 0.716, top-1 83.6%; cross-judge τ = 0.867 | p. 13 | V | moderate |
| RQ4 | Pair-wise VLM judging shows 23.3% position bias; point-wise shows ties-in-the-middle (3-scenario smoke test) | p. 12–13 | V | weak |
| RQ4 | Single trial per app–model cell; no significance tests between models | p. 6, 9 | V | moderate |
| RQ4 | Build success saturates when a verify-repair loop is present and stops discriminating models | p. 12 | A | moderate |
| RQ5 | Output is a web proxy, not native; agent also receives human-reviewed navigation description | p. 3, 9 | V | moderate |

## 14. Key quotes
> "Can a multimodal LLM read a folder of mobile-app screenshots and generate the source code for that app?" (p. 1)
> "Build verification catches type errors but not silent event-handler bugs" (p. 8)
> "Build success is a property of the harness, not the model." (p. 12)

## Analyst notes
- Reading coverage: whole PDF read (pp. 1–26), including appendices A–J; failure-gallery figures (pp. 18–26) seen only via captions; references skimmed.
- Uncertainties: Table 4 vs Table 11 C4 shares do not reconcile; number of human raters for the 55-scenario alignment is not stated; the drafting VLM is not named. Peer-reviewed (EMNLP 2026 main, tier 1), very recent (Oct 2026), not yet replicated. The paper cites a concurrent submission by overlapping authors on interactive single-file webpages (p. 2) — unknown which paper.
