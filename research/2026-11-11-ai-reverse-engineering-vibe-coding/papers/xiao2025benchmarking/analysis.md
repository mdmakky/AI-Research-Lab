---
key: xiao2025benchmarking
status: complete
evidence_basis: full-text
design: benchmark construction + empirical study of MLLMs and prompting strategies, automatic metrics + human evaluation + failure taxonomy + small user study
dataset: Interaction2Code: 127 real webpages (100 from C4 validation set, 27 from popular GitHub projects) with 374 annotated interactions
sample_size: 127 webpages / 374 interactions; 6 MLLMs x 3 prompts; user study with 4 participants and 4 tasks
metrics: Full page: CLIP, SSIM, OCR+BLEU text, Widget Similarity, Widget Match Rate; interaction part: CLIP, SSIM, text, Position, Implement Rate; human Usability Rate and pairwise Win/Tie/Lose
main_finding: MLLMs reproduce interactions worse than static page; best Usability Rate 81% (GPT-4o Mark); 10 failure types, chiefly missing or partial interactions.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Interaction2Code: Benchmarking MLLM-based Interactive Webpage Code Generation from Interactive Prototyping

- Authors: Xiao, Jingyu; Wan, Yuxuan; Huo, Yintong; Wang, Zixin; Xu, Xinyi; Wang, Wenxuan; Xu, Zhiyao; Wang, Yuhang; Lyu, Michael R.
- Year / venue: 2025, 2025 40th IEEE/ACM International Conference on Automated Software Engineering (ASE) (published)
- DOI: 10.1109/ase63991.2025.00028 · URL: https://doi.org/10.1109/ase63991.2025.00028
- Source text: `fulltext.txt` (page refs = PDF page index), extracted from arXiv:2411.03292v3 (1 Mar 2026), not the ASE proceedings PDF

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- Formulate the Interaction-to-Code task (generate an interactive webpage from an "interactive prototype": screenshots before and after each interaction), build a real-world benchmark for it, and systematically study how well MLLMs reproduce webpage interactions, why they fail, and how prompting can help [A] (pp. 1–2).

## 2. Research questions / hypotheses
- No formal RQs. The study is organised around four reported "limitations" of MLLMs: (1) worse generation of interactive parts than of the full page; (2) ten failure types; (3) poor performance on visually subtle interactions; (4) insufficient understanding from visual input alone — each paired with an improvement strategy [V] (pp. 1–2).

## 3. Methodology
- Research design: benchmark construction plus empirical comparison of models and prompts; automatic evaluation via Selenium-driven interaction replay; human usability and pairwise evaluation; qualitative failure taxonomy; sub-experiments on visual saliency and input modality; ablation; small user study [V] (pp. 3–11).
- Approach / model / intervention: MLLM receives the original screenshot plus post-interaction screenshot(s) and must output one HTML+CSS+JavaScript file, tagging interactive elements with ids (e.g. id="interact1") so a webdriver can trigger them [V] (pp. 3–5). Prompts: Direct, Chain-of-Thought (CoT), Mark (red bounding boxes on interactive areas), Failure-aware Prompt (FAP: lists the ten failure types) [V] (p. 5). Further enhancements: Visual Saliency Enhancement (crop to enlarge the interaction area) and adding human-written textual descriptions of interactions [V] (pp. 9–10).
- Baselines or comparison conditions: Gemini-1.5-flash, GPT-4o-20240806, Claude-3.5-Sonnet-20240620, Qwen2.5-VL-instruct 3B/7B/72B; Direct prompting is the baseline for prompt comparisons; Gemini-1.5-flash Direct is the human pairwise baseline [V] (pp. 4, 6). No non-LLM or prior UI-to-code system (e.g. DCGen) is run as a baseline [I] (based on p. 4 model list).

## 4. Dataset and sample
- Data source(s): (1) C4 validation set (CommonCrawl), filtered as in Design2Code, 1,000 pages sampled across 15 topics, from which four PhD students each picked about 25 → 100 pages; (2) 27 popular GitHub projects (average 13k stars) with deployed links, found via "open-production-web-projects" and "awesome-opensource-apps", to include UI-framework pages [V] (pp. 2–3).
- Sample size (N) and unit: 127 webpages and 374 interactions; 15+ topics; 23 tag categories and 8 visual categories (31 interaction categories) [V] (pp. 1, 3). Most frequent interactive tags: button 235, input 52, span 37, link 36 [V] (p. 3).
- Sampling / selection method: manual selection by four PhD students for complexity (at least one meaningful interaction) and diversity; 1–10 "important and functional" interactions kept per page; trivial interactions (e.g. hover underline) excluded [V] (pp. 2–3). Selection guidelines are only in the external artifact [V] (p. 3).
- Data availability (public? link?): data and code at https://github.com/WebPAI/Interaction2Code [A] (p. 1).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: temperature 0; max output 4,096 tokens (commercial) and 2,048 (Qwen); other parameters default [V] (p. 4). Selenium webdriver locates elements by id, performs the interaction and screenshots the result; the changed region is extracted by pixel subtraction (same-size pages) or a Git-diff of rows/columns (size-changing pages) (Algorithm 1) [V] (p. 4). Data-contamination check: BLEU between generated and original HTML is 0.12–0.14 for the four main models [V] (p. 5). FAP experiment: 2/3 of the dataset used to derive failure types, 1/3 for testing [V] (p. 8). Saliency and modality experiments use 10 randomly sampled failure-case webpages each [V] (pp. 9–10).
- Code availability: GitHub repository above [A] (p. 1). Appendix H (tool) and detailed human-evaluation instructions are referenced but are not in our 13-page PDF [V] (pp. 6, 11).

## 6. Evaluation metrics
- Full-page metrics: CLIP score (visual similarity); SSIM (structural similarity); Text similarity = BLEU on OCR-extracted text; Widget Similarity (WS) and Widget Match Rate (WMR) computed with the GUIPilot method [V] (p. 4).
- Interaction-part metrics (on the extracted changed region): CLIP, SSIM, Text; Position similarity P = 1 − max(|xo − xg|, |yo − yg|) of normalised interaction-area centres; Implement Rate IR = implemented / (implemented + unimplemented), where "implemented" means detectable by the webdriver [V] (p. 4).
- Human metrics: Usability Rate UR = usable / (usable + unusable), judged by four PhD students (three years front-end experience) — usable if the implementation "precisely matches the behavior specified in the interactive prototype"; pairwise Win/Tie/Lose by five annotators against Gemini-1.5-flash Direct, majority (≥3) rule; failure-type annotation [V] (pp. 4, 6–7).
- Validation against human judgement: authors state human results "are consistent with Section V-A, confirming the validity of our automatic evaluation metrics" [A] (p. 6). No correlation coefficient, agreement statistic or regression is reported — not reported. Inter-annotator agreement for usability, pairwise or failure annotation — not reported (failure types reached by discussion to consensus on a 25% sample) [V] (p. 7). Number of items in the human evaluations — not reported.
- Widget metrics are acknowledged as unreliable for web pages: WS is "consistently poor" (0.02–0.05) and GUIPilot omits many elements because it was designed for mobile UIs [V] (pp. 5–6).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): none for model or prompt comparisons; saliency effect described as "significantly increases" without a test [V] (pp. 8–9). Not reported.

## 7. Key findings
1. Interactive parts are generated worse than full pages for all models (e.g. GPT-4o average full-page CLIP 0.7059 vs interaction-part CLIP 0.5598) [V] (p. 6).
2. Claude-3.5-Sonnet has the best averages on most metrics (e.g. interaction IR 0.7870, full-page Text 0.5835); GPT-4o with Mark prompt has the highest single IR (0.8128); Qwen2.5-VL-72B ≈ Gemini-1.5-flash; performance rises with model size [V] (pp. 5–6).
3. Human Usability Rate (Fig. 6a, read from figure labels): GPT-4o Direct/CoT/Mark 73/74/81%; Claude 66/69/77%; Gemini 47/53/64%; Qwen-72B 41/43/54%; Qwen-3B 17–19% [V] (p. 6). Mark prompting gives the largest usability gain (Claude +11 points vs Direct) [V] (p. 6).
4. Ten failure types in two groups (interactive element: missing, no interaction, wrong element, wrong type, wrong position; interaction effects: wrong position, wrong type, effect on wrong element, partial implementation, wrong function) [V] (pp. 7–8). Failures (a) missing element, (b) no interaction and (j) wrong function have usability <10% (0%, 6.93%, 0%) [V] (pp. 7–8). Main failure modes are "No interaction", "Partial implementation", "Interactive element missing" and "Wrong function" [A] (p. 8).
5. Failures cluster into spatial (a, c, e, f), type (d, g) and behavioural (b, h, i, j) failures [A] (p. 8).
6. Low visual saliency (small interaction area) lowers SSIM and position similarity; cropping to enlarge the area (1.2–3×) recovers interactions on 10 failure pages [V] (pp. 9–10).
7. Authors state that combined visual + text input "consistently outperforms single-modality inputs across all prompt types" [A] (p. 10). On 10 failure pages with GPT-4o, V+T is best on most cells (e.g. Direct: Position 0.7157 V+T vs 0.3951 V) [V] (p. 10), but not all: under the Mark prompt, SSIM for V+T is 0.4336, below V (0.4520) and T (0.4454) [V] (p. 10). All four enhancements combined give the best ablation result (GPT-4o interaction CLIP 0.6937 vs 0.5700) [V] (p. 11).
8. FAP: authors claim it improves "all models" [A] (p. 8), but Table VI shows Qwen2.5-VL-3B drops on 7 of 8 metrics and Qwen-7B on 5 of 8 [V] (p. 9).
9. User study: with the tool, 4 tasks took 279 s vs 413 s on average and expert similarity rating 4.5 vs 3.875 (two participants per condition, two raters) [V] (p. 11).
10. Code quality or maintainability of the generated HTML/CSS/JS is not measured; the only code-level measure is BLEU against the original HTML, used as a contamination check [V] (pp. 4–5).

## 8. Limitations stated by the authors
- Limited context length: complex pages with many interactions may exceed the context window; iterative generation suggested [A] (p. 11).
- Model selection: only three main commercial MLLMs tested; others (e.g. Pixtral) left for future work [A] (p. 11).
- Back-end interactions (login, search) cannot be evaluated because the benchmark has no back-end code [A] (p. 11).
- Existing widget-consistency methods are designed for mobile UIs and miss web elements [A] (p. 5).

## 9. Limitations we identified
- [I] Validation of automatic metrics against humans is only a qualitative "consistent" statement (p. 6); no correlation, agreement (kappa) or item counts are given. The automatic metrics are therefore not shown to measure functional fidelity.
- [I] "Implement Rate" counts an interaction as implemented if the webdriver can find and trigger the element (p. 4) — this measures presence, not correct behaviour; functional correctness rests on the human Usability Rate alone.
- [I] Interaction fidelity is judged on screenshots of state changes, not on behavioural traces or DOM/state assertions; non-visual effects (data, network, storage) are out of scope (based on pp. 3–4, 11).
- [I] Several sub-experiments use only 10 pages (pp. 9–10) and the user study has 2 participants per condition (p. 11); these results are anecdotal.
- [I] The FAP claim ("improve ... on all models", p. 8) contradicts the paper's own Table VI (p. 9) for the two smaller Qwen models.
- [I] Similarly, the modality claim that V+T "consistently outperforms" single modalities "across all prompt types" (p. 10) is contradicted by Table VIII for SSIM under the Mark prompt (V+T 0.4336 < V 0.4520 and T 0.4454, p. 10), and rests on only 10 pages.
- [I] The FAP test uses failure types derived from 2/3 of the same dataset (p. 8); split procedure and whether it is by page or by interaction is not stated.
- [I] Fig. 9 "No failure" shares (about 36% for GPT-4o, about 40% for Claude, read from the figure, p. 9) look hard to reconcile with Usability Rates of 73–81% (p. 6); the denominators/definitions are not explained.
- [I] The contamination argument (C4 has only text; BLEU 0.12–0.14, p. 5) is weak: C4 URLs' HTML is widely crawled elsewhere, and low BLEU does not rule out memorised layout.
- [I] No code-quality, maintainability or code-structure measurement, despite generating JavaScript event logic.

## 10. Threats to validity
- Internal (confounds, leakage, selection): pages and interactions hand-picked by the authors' annotators (pp. 2–3); FAP failure types derived from the same benchmark (p. 8); Table VI direct baselines differ from Table IV (different subset), so improvements are relative to a subset [I].
- External (generalisability of sample/context): 127 pages, front-end only, no back-end; mostly click-type interactions on buttons (235 of tagged elements) (p. 3); single-file output, not multi-file framework projects [I].
- Construct (do metrics measure the concept?): visual metrics on changed regions approximate interaction fidelity; IR measures element presence; widget metrics admitted unreliable for web (p. 5) [I].
- Statistical conclusion (power, multiple comparisons, variance): single deterministic run (temperature 0); no tests, CIs or agreement statistics; small N in sub-studies [I].
- Reproducibility (data/code/setup reported?): data and code released (p. 1); prompts shown (p. 5); key guidelines and appendix only in the artifact; the PDF is arXiv v3 (1 Mar 2026), the ASE 2025 version may differ [I].

## 11. Future research directions
- Stated by authors [A]: iterative multi-round generation for many interactions; testing more MLLMs (e.g. Pixtral) (p. 11); handling interactions that require back-end code (p. 11); designing widget-level consistency detection suited to web pages (pp. 5–6).
- Suggested by us [I]: validate interaction metrics against human usability with reported correlations; add behavioural assertions (DOM state, event sequences) and code-quality/maintainability analysis of generated JS; extend to multi-page apps with back-end.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ4, RQ5 (RQ3 only by absence).
- How it informs our work [I]: this is the closest web benchmark to reverse engineering from observable behaviour: input is before/after screenshots of interactions, and the target is a page that reproduces that behaviour. It supplies a usable failure taxonomy and the Usability Rate as a human functional-fidelity measure, but its automatic metrics are weakly validated and it ignores code quality.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Interaction-to-Code: MLLM generates one HTML/CSS/JS file from before/after interaction screenshots; Direct, CoT, Mark, FAP prompts | p. 2–5 | V | moderate |
| RQ2 | Interaction fidelity measured by interaction-part CLIP/SSIM/Text/Position, Implement Rate (webdriver), and human Usability Rate | p. 4 | V | moderate |
| RQ2 | Best human Usability Rate 81% (GPT-4o Mark); Claude 66–77%; Qwen-3B 17–19% (number of evaluated items not reported, p. 6) | p. 6 | V | moderate |
| RQ2 | Interactive parts scored lower than full pages for all six models | p. 6 | V | moderate |
| RQ2 | Ten failure types; missing element, no interaction, wrong function yield <10% usability | p. 7–8 | V | moderate |
| RQ3 | No code quality or maintainability measured; code compared to original only via BLEU 0.12–0.14 for contamination | p. 5 | V | moderate |
| RQ4 | Automatic metrics declared "consistent" with human evaluation; no correlation or inter-annotator agreement reported | p. 6 | V | weak |
| RQ4 | Widget Similarity/Match (GUIPilot) unreliable for web pages (WS 0.02–0.05) | p. 5–6 | V | moderate |
| RQ4 | Claimed FAP gain on all models contradicted by Table VI for Qwen-3B/7B | p. 8–9 | V | moderate |
| RQ4 | Saliency, modality sub-studies on 10 pages; user study 2 vs 2 participants | p. 9–11 | V | weak |
| RQ5 | Back-end-dependent interactions (login, search) not evaluable; future work | p. 11 | A | moderate |

## 14. Key quotes
> "existing benchmarks only contain static web pages for evaluation and ignore the dynamic interaction" (p. 1)
> "An interaction is considered usable if its implementation precisely matches the behavior specified in the interactive prototype." (p. 6)
> "The benchmark we collect does not include back-end code; we cannot verify the generation effect of such interactions" (p. 11)

## Analyst notes
- Reading coverage: whole PDF read (pp. 1–13); garbled Figure 6 and Table VI/Figure 9 checked on PDF pages 6, 8 and 9. References skimmed. Appendix H and annotation guidelines are external (artifact) and were not read.
- Uncertainties: usability percentages are read from figure labels (p. 6); Fig. 9 percentages are approximate. Our PDF is arXiv v3 (dated 1 Mar 2026), later than the ASE 2025 publication; page numbers refer to this PDF. Peer-reviewed (ASE 2025, tier 1). Same group (CUHK, Lyu) as DesignBench/DCGen — related benchmarks in our set may share authors and methods.
