---
key: chen2025iwr
status: complete
evidence_basis: full-text
design: Benchmark study; 28 LVLMs reconstruct interactive webpages (single HTML file) from a user-interaction video plus crawled assets; agent-as-a-judge replays ground-truth actions
dataset: IWR-Bench, 113 tasks from 100 real-world websites (curated 200 -> 161 -> 113), 1,001 annotated actions, 620 visual checkpoints, 403 logical assertions
sample_size: 113 tasks x 28 models (runs per model not reported); human alignment study 60 instances x 5 raters; agent check 100 pages x 3 raters
metrics: Interactive Functionality Score (IFS, share of actions executed and assertions passed); Visual Fidelity Score (VFS, OCR+DINO low-level + MLLM high-level); Final = 0.7*IFS + 0.3*VFS
main_finding: Best model (GPT-5) reaches only 36.35 Final; IFS (24.39) lags VFS (64.25) for all models, partly by construction: VFS scores only reached checkpoints.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# IWR-Bench: Can LVLMs reconstruct interactive webpage from a user interaction video?

- Authors: Chen, Yang; Liu, Minghao; Shen, Yufan; Li, Yunwen; Huang, Tianyuan; Fang, Xinyu
- Year / venue: 2025, arXiv (preprint)
- DOI: 10.48550/arxiv.2509.24709 · URL: https://arxiv.org/abs/2509.24709
- Source text: `fulltext.txt` (page refs = PDF page index). Version read: arXiv v3, 19 Nov 2025 (p. 1). **Preprint, not peer-reviewed.**

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] Introduce and formalise Interactive Webpage Reconstruction (IWR): given a video of a user interacting with a webpage plus the page's static assets, a model must generate code that reproduces both the visual appearance and the interactive behaviour seen in the video (p. 4, p. 5).
- [A] Motivation: existing webpage-to-code benchmarks are static (screenshot-to-code, e.g. Design2Code, WebSight) or treat interactions as single-step, stateless events (Interaction2Code), and do not provide the static assets needed for a realistic rebuild (p. 2, p. 6).

## 2. Research questions / hypotheses
- [A] Central question: "Can LVLMs reconstruct the dynamic, interactive functionalities of a webpage from observing a user interaction video?" (p. 2).
- [I] No formal hypotheses are stated; the study is a descriptive benchmark evaluation (p. 7-9).

## 3. Methodology
- Research design: [V] Benchmark construction plus a cross-sectional comparison of 28 large vision-language models (LVLMs) on the same tasks, scored automatically by an "agent-as-a-judge" that replays a ground-truth action sequence on the generated page (p. 4, p. 6-8).
- Approach / model / intervention: [V] Each model receives the interaction video (sampled at 1 fps, max 64 frames) and a composite image of all crawled static assets, and must output one self-contained `index.html` with all HTML, CSS and JS; backend logic must be mocked in JS; no external libraries or fonts (p. 8, p. 20). Asset filenames are anonymised (e.g. `asset_001.png`) so models must match assets visually rather than by name (p. 5).
- Baselines or comparison conditions: [I] No method baseline is described (checked pp. 7-9). [V] The comparison is across 28 models in three groups: 17 proprietary MLLMs, 9 open-source MLLMs, 2 open-source video-specialised models; three models are also run in "thinking" (reasoning-enhanced) and non-thinking variants (p. 8). [I] Because those three thinking variants are counted separately, the 28 entries cover 25 distinct base models (based on Table 3, p. 8).

## 4. Dataset and sample
- Data source(s): [V] Live real-world websites; 113 tasks from 100 websites; videos recorded by trained annotators while a browser extension logs action type and parameters; static assets collected with automated crawlers plus manual inspection (p. 1, p. 5).
- Sample size (N) and unit: [V] 113 tasks/videos; 1,001 actions in total (mean 8.9 per video); 620 actions carry a visual checkpoint and 403 carry a logical assertion; mean video length 35.4 s (max 172.9 s); 19 unique resolutions; 10.62% mobile (p. 6). Interaction-logic mix: L1 static 7.96%, L2 simple state 47.79%, L3 complex workflow 33.63%, L4 algorithm/game 10.62% (p. 3).
- Sampling / selection method: [V] 200 candidate tasks proposed by web-development experts -> deduplication and diversity balancing across domain, visual complexity and interaction logic -> 161 -> cross-verification by a second annotator and an LLM check of assertions -> disputed, ambiguous or overly trivial tasks removed -> 113 (p. 5-6). [I] Exact criteria for "trivial" or "disputed" are not reported.
- Data availability (public? link?): [A] Benchmark and evaluation code "will be made publicly available" at https://github.com/SIGMME/IWR-Bench (p. 1). We did not check whether the release happened.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Video sampled at 1 fps, capped at 64 frames (longer videos uniformly downsampled); video frames and asset image given as a sequential multi-image input; "All other inference parameters utilize the default settings recommended by the model providers" (p. 8). A standard system prompt is used for all models (p. 18, p. 20). Evaluation executor built on the `browser-use` library; Gemini-2.5-Pro is the MLLM judge for logical assertions and for the high-level visual score (p. 6-7). Actions target elements by natural-language description rather than coordinates (p. 17). [I] Number of runs per model, temperature/seed and variance: not reported (checked pp. 7-9, 17).
- Evaluator determinism: [A] The executor is described as "deterministic" (p. 6). Which model resolves the natural-language element descriptions (p. 17) into page elements, and whether replays are repeatable, is not reported.
- Code availability: [A] Announced for release at the GitHub link above (p. 1); not verified by us.

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] **IFS (Interactive Functionality Score)** = successful actions / total actions; an action succeeds only if it is operationally feasible (target element found) and all its logical assertions pass (p. 7). Chosen to measure functional correctness, because pixel-wise metrics "cannot appraise functionality" (p. 3).
  - [V] **VFS (Visual Fidelity Score)** = macro-average over reached checkpoints with a visual flag of 0.5 x low-level score (mean of OCR Levenshtein text similarity and DINO cosine similarity) + 0.5 x high-level MLLM score (p. 7). The MLLM rubric weights Layout 10, Elements 15, Content and Text 40, Style 15, Overall 20 points (p. 20).
  - [V] **Final Score** = 0.7 x IFS + 0.3 x VFS, macro-averaged across the benchmark (p. 7).
  - [V] Weights w = 0.5 and alpha = 0.7 were chosen by grid search to maximise Spearman's rho with human judgements of 60 instances (20 random tasks x 3 random models) rated by five PhD-level students; best rho = 0.57 for VFS and 0.65 for the Final Score (p. 17). [I] Agreement among the five raters is not reported; their judgements were aggregated (p. 17).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): [I] None found for model comparisons: Table 3 and the results text give single point estimates without confidence intervals or significance tests (checked pp. 8-9, 16-19). [V] Only Spearman correlations are reported, for metric calibration (p. 17).

## 7. Key findings
1. Interactive reconstruction from video is far from solved: GPT-5 is best with Final 36.35, IFS 24.39, VFS 64.25; no model exceeds 25 IFS — [V] (p. 8, p. 9).
2. IFS is below VFS for every model: e.g. Claude-Sonnet-4 VFS 61.34 vs IFS 22.29; GPT-4o (latest) VFS 57.55 vs IFS 17.55 — [V] (p. 8, p. 9). [I] Caveat: the two scores do not share a denominator. VFS is computed only over checkpoints that were successfully reached (p. 7), IFS over every action in the trajectory (p. 7), so part of the gap is built into the metric definitions (see §9). The low absolute IFS (finding 1) does not depend on this caveat.
3. Hierarchy: the top eight models by Final Score are all proprietary (GPT-5 36.35 down to GPT-4.1 31.99); proprietary models span Final 16.50-36.35; the best open-source model, Qwen3-VL (thinking), scores 31.15 and is above 9 of the 17 proprietary models; video-specialised models are lowest (VideoLLaMA3-7B 13.67, InternVideo-2.5-Chat-8B 10.07) — [V] (p. 8, p. 9). So the proprietary and open-source ranges overlap. [A] Authors conclude general multimodal reasoning and code generation matter more than video-specialised architectures (p. 9).
4. Thinking variants raise IFS and Final slightly in all three pairs: Claude-Sonnet-4 Final 34.62 vs 34.00 (IFS 23.65 vs 22.29); Claude-Opus-4 34.13 vs 33.33 (IFS 23.61 vs 21.83); Gemini-2.5-Pro 30.36 vs 30.31 (IFS 21.65 vs 20.51). But they lower VFS in all three pairs: 60.20 vs 61.34; 58.67 vs 60.18; 50.67 vs 53.18 — [V] (p. 8, p. 9). [A] The authors describe the gains as "Consistent but Moderate" (p. 9); this goes beyond the data, given the VFS drops and the Gemini Final difference of 0.05 points.
5. Final Score drops sharply from static L1 tasks to interactive ones: GPT-5 61.85 on L1 vs 35.43 / 35.12 / 25.26 on L2 / L3 / L4 — [V] (p. 17). L1 is the highest category for every model, but L2 and L3 are similar and their order varies by model (e.g. Claude-Sonnet-4 31.04 vs 32.86; Claude-Opus-4 (thinking) 31.52 vs 32.57; GPT-4.1 30.32 vs 31.98) — [V] (p. 17). By visual category, Final Score is lowest on data-dense layouts (GPT-5 26.05 on V4 vs 44.77 on V1), with V3 above V2 (43.77 vs 30.73) — [V] (p. 18). By domain, Life & Community is the weakest and Entertainment & Media the strongest (GPT-5 22.80 vs 47.24) — [V] (p. 19). All three category tables report Final Score only, not IFS or VFS (p. 16). So they do not show whether functional or visual fidelity drives the differences. [I] The robust contrast is L1 vs the rest; strata are small (about 9 L1 and 12 L4 tasks, see §9).
6. Judge reliability: three PhD students watched the agent run on 100 random generated pages; agent evaluation failed in only three cases (ambiguous element descriptors), which were then fixed — [V] (p. 9).
7. Case studies show distinct failure points, e.g. a model completing filter and sort but failing "add to cart"; a model failing to merge tiles in a 2048 rebuild; missing first-step elements blocking all later actions — [V] (p. 19-21).

## 8. Limitations stated by the authors
- Not reported: the paper has no limitations or threats-to-validity section (checked pp. 1-21). Design notes and disclosures that are not limitations (alternative weighting rejected, p. 7; agent-evaluation errors fixed, p. 9; LLM-assisted editing, p. 21) are recorded in Analyst notes.

## 9. Limitations we identified
- [I] **IFS and VFS are not comparable in scale.** VFS averages only over checkpoints that were "successfully reached" (p. 7). It therefore cannot be lowered by functional failures that block later states. IFS divides successful actions by all actions in the trajectory (p. 7). Part of the IFS < VFS gap is therefore a property of the metrics, not only of the models. The authors mention unreachable states only to justify alpha = 0.7 (p. 7). How VFS is scored for a task where no visual checkpoint is reached is not reported. This weakens the headline "visual is solved better than function" reading. It does not weaken the finding that IFS is low in absolute terms.
- [I] **No code-quality or maintainability measurement.** The task forces a single self-contained HTML file with no libraries (p. 20), and only behaviour and appearance are scored. The benchmark therefore says nothing about code structure, readability or maintainability (our RQ3), and the single-file format is far from how real apps are built.
- [I] **Judge overlap.** Gemini-2.5-Pro is both the assertion/visual judge (p. 7) and one of the evaluated models (p. 8). Self-preference bias is not tested; its mid-table rank makes a large bias unlikely, but it is not ruled out.
- [I] **Moderate human alignment, tuned in-sample.** The weights were chosen to maximise rho on the same 60 instances used to report rho = 0.57 / 0.65 (p. 17); there is no held-out check. These are moderate correlations, so the Final Score is only partly aligned with human judgement. Agreement among the five raters is not reported (p. 17). The same is true of agreement among the three PhD students who observed the agent (p. 9).
- [I] **Evaluator re-scoring after fixes unclear.** The 3/100 agent failures were "rectified" (p. 9). Whether all 28 x 113 evaluations were re-run after the fixes is not reported. Element resolution from natural-language descriptions (p. 17) may itself involve a model, so the "deterministic" label (p. 6) is an author claim we cannot check.
- [I] **No variance reporting.** Single point estimates with default sampling settings (p. 8) and no repeated runs reported; several model gaps are tiny (e.g. 30.36 vs 30.31, p. 9) and could be noise.
- [I] **Unclear failure propagation.** It is not stated whether a failed early action stops the replay or whether later actions are still attempted (p. 7); Case 4 suggests failures cascade (p. 21). This affects how IFS should be read.
- [I] **Possible contamination.** Tasks come from popular live websites (e.g. an IMDb mock in Figure 2, p. 2); models may have seen similar code in training. Asset anonymisation (p. 5) reduces name cues but not memorised page structure. Not discussed by the authors.
- [I] **Small strata.** L1 (about 9 tasks) and L4 (about 12 tasks), derived by us from the percentages on p. 3, give unstable per-category scores.

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Task filtering removed "overly trivial" and "disputed" tasks without stated criteria (p. 6), which may shift difficulty. All models get identical inputs and prompt (p. 18), which supports a fair comparison. Video downsampling to at most 64 frames (p. 8) may remove interaction evidence from long videos (max 172.9 s, p. 6); this affects all models equally but penalises long tasks.
- External (generalisability of sample/context): [I] Front-end only, one HTML file, mocked backend (p. 20); 113 tasks. Results do not transfer directly to multi-file apps, backends, or native desktop/mobile apps.
- Construct (do metrics measure the concept?): [I] IFS measures replay of one ground-truth trajectory, not general behavioural equivalence; VFS mixes OCR, DINO and an MLLM rubric in which text content carries 40 of 100 points (p. 20). Both are proxies for "functional fidelity" and "visual fidelity". They also use different denominators: VFS covers only reached checkpoints, IFS all actions (p. 7). So the size of the IFS-VFS gap is partly metric-induced and should not be read as a direct comparison of the two capabilities. The fixed alpha = 0.7 encodes a value judgement (functionality matters more), supported only by rho = 0.65 (p. 17).
- Statistical conclusion (power, multiple comparisons, variance): [I] No CIs, tests or repeated runs (p. 8-9); conclusions about small differences (thinking vs non-thinking) are not statistically supported.
- Reproducibility (data/code/setup reported?): [I] Prompts are published in the appendix (p. 20-21) and data and code are promised (p. 1). Proprietary model versions, default sampling settings and a proprietary judge model (p. 7) limit exact reproduction.

## 11. Future research directions
- Stated by authors [A] (p. 9): focus on "temporal reasoning, dynamic asset binding, and robust code synthesis"; structured code generation and state management as key directions (p. 9).
- Suggested by us [I]: (a) add code-quality/maintainability measures (static analysis, modularity) to IWR-style tasks so fidelity and code quality are measured together (our RQ5); (b) allow multi-file or framework-based outputs and agentic, iterative generation; (c) report repeated runs with variance and a held-out human-alignment set; (d) use a judge model that is not also evaluated.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ4, RQ5 (indirectly). Not RQ3.
- How it informs our work [I]: IWR-Bench is a direct example of AI "reverse engineering" an application from observable behaviour (a video) rather than from a written spec, so it fits RQ1. Its main result is central evidence for RQ2: functional correctness is low for every model (IFS < 25), and IFS sits far below VFS. The size of that gap is partly a product of how VFS is defined (only reached checkpoints, see §9). Its metric design (action replay with an agent judge, visual composite, human-calibrated weights) and weaknesses (no variance, in-sample calibration, judge overlap) inform RQ4 and our own study design. It illustrates the gap behind RQ5: fidelity is measured, but code quality and maintainability are not. [I] The result is directionally consistent with [@bai2026recreationworld], which finds static structure reproduced better than action-conditioned behaviour within its programmatic tests [@bai2026recreationworld, p. 16-17]. However, bai's visual channel is not higher than its programmatic channel in aggregate [@bai2026recreationworld, p. 11]. The two papers measure the gap differently, and here the gap is partly metric-induced (see §9). The convergence supports "static structure is easier than interaction logic". It does not support "visual fidelity systematically exceeds functional fidelity".

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | LVLMs can be asked to rebuild an interactive webpage from a user-interaction video plus crawled assets (one HTML file); 28 models were evaluated on 113 real-site tasks | 5, 8 | V | weak |
| RQ2 | Best model (GPT-5) scores Final 36.35 and IFS 24.39; IFS < 25 for all 28 models | 8, 9 | V | moderate |
| RQ2 | IFS < VFS for all 28 models (GPT-5 24.39 vs 64.25), but VFS averages only over reached checkpoints while IFS counts all actions, so the gap is partly metric-induced | 7, 8 | V | weak |
| RQ2 | Final Score falls from static (L1) to interactive tasks (GPT-5 61.85 vs 25.26 on L4); L2/L3 order varies by model; strata are about 9-12 tasks; category tables report Final Score only | 16, 17 | V | weak |
| RQ2 | Thinking variants add little to Final/IFS (e.g. Final 34.62 vs 34.00; 30.36 vs 30.31) and lower VFS in all three pairs | 8, 9 | V | weak |
| RQ4 | Functional fidelity measured by agent replay of a ground-truth action sequence plus MLLM-judged assertions; visual fidelity by OCR + DINO + MLLM rubric | 7, 20 | V | weak |
| RQ4 | Metric weights tuned on 60 human-rated instances (5 raters); Spearman rho 0.57 (VFS) and 0.65 (Final); no held-out check is described (I) | 17 | V | weak |
| RQ4 | Agent-judge errors in 3 of 100 manually observed runs | 9 | V | weak |
| RQ4 | VFS and IFS use different denominators (reached checkpoints vs all actions), so their gap is not a like-for-like comparison | 7 | I | weak |
| RQ4 | No repeated runs, confidence intervals or significance tests for model comparisons were found (our check of the results and tables) | 8, 9 | I | weak |
| RQ5 | Benchmark scores behaviour and appearance only; single-file output means code quality/maintainability is not assessed (our appraisal of the metric definitions and prompt) | 7, 20 | I | weak |

Strength note [I]: rows are rated weak because this is a single, non-peer-reviewed benchmark without variance reporting. The low-IFS row is rated moderate because it holds for all 28 models. The IFS < VFS gap row is downgraded to weak because the gap is partly metric-induced (§9). It is only directionally consistent with [@bai2026recreationworld], which measures a different contrast (structure vs action-conditioned tests within one programmatic channel).

## 14. Key quotes
> "the best model achieves an overall score of only 36.35%" (p. 1)

> "the primary bottleneck for current models is not visual understanding but the synthesis of complex interaction logic" (p. 9)

> "Failures in the agent’s evaluation were observed in only three instances." (p. 9)

## Analyst notes
- Reading coverage: sections read / skipped and why: all 25 PDF pages read via `fulltext.txt`, including appendices A-G (taxonomy, per-dimension tables, metric validation, prompts, case studies). Reference list (p. 11-15) and contributor list (p. 10) skimmed only. Figures (bar chart p. 1, case screenshots p. 22-25) are images and not readable as text; their captions were used.
- Uncertainties: (1) runs per model and sampling settings beyond "default" are not reported; (2) whether failed actions stop the replay is not stated; (3) per-category task counts are derived by us from percentages (p. 3), not given directly; (4) we did not check whether the promised data/code release happened; (5) the PDF header says "IWR-Bench Team" and lists contributors on p. 10, consistent with the 21 authors in metadata.json.
- Design notes and disclosures (not limitations): an alternative weighting scheme for the Final Score "proved ineffective for differentiating model performance" (p. 7); agent-evaluation failures caused by ambiguous element descriptors were corrected (p. 9); an LLM was used for grammar correction and language refinement of the paper (p. 21).
- Critical-review fixes applied 2026-11-12 (C1-C9 of `reports/critical-review-batch-c.md`). C9 was applied with corrected numbers: Table 3 (p. 8) shows the top eight models are proprietary (GPT-4.1 31.99 > Qwen3-VL 31.15), and Qwen3-VL beats 9, not 11, of the 17 proprietary models.
