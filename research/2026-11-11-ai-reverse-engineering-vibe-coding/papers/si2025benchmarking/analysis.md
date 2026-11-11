---
key: si2025benchmarking
status: ready
evidence_basis: full-text
design: benchmark construction + automatic metrics + human evaluation (comparative evaluation of MLLMs and prompting methods)
dataset: Design2Code: 484 manually curated real-world webpages from C4 validation set; Design2Code-HARD: 80 harder webpages
sample_size: 484 webpages (+80 HARD); human eval on 100 sampled webpages x 5 annotators (60 Prolific participants)
metrics: Block-Match, Text (Sørensen-Dice), Position, Color (CIEDE2000), CLIP visual similarity; human pairwise Win/Tie/Lose; direct assessment
main_finding: GPT-4o best on all screenshot-to-HTML visual metrics; models mainly fail at recalling elements and layout; 49% of GPT-4V pages judged interchangeable.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End Engineering

- Authors: Si, Chenglei; Zhang, Yanzhe; Li, Ryan; Yang, Zhengyuan; Liu, Ruibo; Yang, Diyi
- Year / venue: 2025, Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers) (published)
- DOI: 10.18653/v1/2025.naacl-long.199 · URL: https://doi.org/10.18653/v1/2025.naacl-long.199
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- Build the first real-world benchmark for converting a webpage screenshot (visual design) directly into HTML/CSS code with multimodal LLMs (MLLMs), with automatic visual-fidelity metrics and human evaluation, and use it to compare models and prompting methods [A] (p. 1).

## 2. Research questions / hypotheses
- No formal RQs or hypotheses. Implicit questions: how well current MLLMs turn screenshots into code that renders into the reference page; whether text-augmented and self-revision prompting help; whether automatic metrics agree with human judgement; what makes a webpage hard [I] (based on sections 3–4, pp. 4–8).

## 3. Methodology
- Research design: benchmark construction plus comparative evaluation; automatic metric evaluation on all 484 test pages, human evaluation on a 100-page sample; regression analysis of metrics against human preferences [V] (pp. 2–7).
- Approach / model / intervention: three prompting methods: (1) Direct prompting (screenshot + instruction to produce one HTML+CSS file); (2) Text-Augmented prompting (screenshot + all text extracted from the original page appended, to remove the OCR burden); (3) Self-Revision prompting (model sees reference screenshot, screenshot of its text-augmented output and that code, and is asked to revise) [V] (p. 4–5). Prompts explicitly say no JavaScript is needed for dynamic interactions [V] (p. 14). The authors also fine-tune their own Design2Code-18B (CogAgent-18B, LoRA rank 8, on a random 20% of WebSight v0.1) [V] (pp. 5, 15).
- Baselines or comparison conditions: commercial GPT-4o, GPT-4V, Claude 3 Opus, Gemini 1.0 Pro Vision; open models LLaVA-V1.6-Mixtral-7B, DeepSeek-VL-7B, Idefics2-8B; fine-tuned WebSight VLM-8B and Design2Code-18B [V] (p. 5). On Design2Code-HARD: GPT-4o, GPT-4o Mini, Claude 3.5 Sonnet, Claude 3 Opus, Gemini 1.5 Pro, Gemini 1.5 Flash [V] (p. 8). Authors state comparisons are "not apple-to-apple" because of model size and training-data differences [A] (p. 5). Human pairwise comparisons use Gemini Pro Vision Direct as the single reference baseline [V] (p. 5).

## 4. Dataset and sample
- Data source(s): webpages linked from the C4 validation set; CSS embedded into one HTML file per page, giving 127.9k pages [V] (p. 2). Design2Code-HARD source is listed as "Real-World (GitHub)" in Table 4 (p. 14), while the main text says it uses "the same filtering process" (p. 8) — the exact origin of HARD pages is not further described [V] (pp. 8, 14).
- Sample size (N) and unit: 484 webpages (test cases) [V] (p. 3); HARD: 80 webpages [V] (p. 8). Average 31,216 GPT-2 tokens per file (min 784, max 98,637), 158 tags on average, 84 HTML5 tag types, DOM depth 13 on average [V] (p. 3). Domain annotation on a random 25% subsample (N=120): company/org 27.7%, blog 25.3%, homepage 13.3% most common [V] (p. 3).
- Sampling / selection method: automatic filtering (drop files >100k tokens, image-only or text-only layouts, deduplication) → 14k pages; strip external dependencies (script, iframe, svg, external links, href, media replaced by placeholders); first two authors manually curated a random 7k of the 14k for stand-alone rendering, no sensitive content and good formatting, after reaching 75% agreement on 200 jointly annotated pages → 484 pages; about one week of work [V] (pp. 2–3, 13). Diversity was sought "as possible" but no formal stratification is described [V] (p. 13).
- Data availability (public? link?): authors state they release the dataset under the ODC-By license [A] (p. 10); no URL is given in our PDF [V] (p. 10).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: commercial models with greedy decoding and max 4,096 new tokens; model versions gpt-4o-2024-05-13, gpt-4-1106-vision-preview, claude-3-opus-20240229, gemini-1.0-pro-vision [V] (p. 14). Open models: temperature 0.5, repetition penalty 1.1; reference and generated screenshots concatenated into one image for single-image models; Qwen-VL-Chat and Mantis excluded because they failed to produce HTML in >80% of cases [V] (pp. 14–15). Fine-tuning: batch 32, lr 1e-5, 5,000 steps, 4× A6000 for about 2 days, checkpoint chosen on a 20-example dev set [V] (p. 15). Gemini 1.5 gave empty responses in the main experiment [V] (p. 14). Human evaluators: Prolific, US only, ≥2,500 surveys with ≥98% pass rate, 60 participants, $16/hour, 5 annotators per item, majority vote [V] (pp. 5, 15).
- Code availability: authors promise "clear ethical use guidelines for all data, code, and model releases" [A] (p. 10); no repository link in our PDF — not reported.

## 6. Evaluation metrics
- High-level visual similarity — CLIP(IR, IG): cosine similarity of CLIP-ViT-B/32 embeddings of the reference and rendered screenshots after resizing to squares, with text regions in-painted (Telea) to remove text [V] (p. 3).
- Low-level element matching, after detecting text blocks in both screenshots (by recolouring text segments in the HTML and tracking pixels, not OCR) and matching them with the Jonker-Volgenant algorithm on text similarity (pairs with similarity <0.5 ignored; neighbouring blocks may be merged) [V] (pp. 4, 13):
  - Block-Match — share of total block area covered by matched blocks; unmatched (missing or hallucinated) blocks lower it — measures element recall/precision [V] (pp. 4–5).
  - Text — character-level Sørensen-Dice similarity of matched blocks, averaged [V] (p. 4).
  - Position — 1 − max(|Δx|, |Δy|) of normalised block centres, averaged [V] (p. 4).
  - Color — CIEDE2000 perceptual colour difference of text in matched blocks, averaged [V] (p. 4).
  - Why chosen: text-based code similarity (edit distance, htmlBLEU) cannot judge visual result because many different codes render the same page [A] (p. 3).
- Human evaluation: (a) pairwise Win/Tie/Lose vs Gemini Pro Vision Direct on 100 sampled pages, priority content > layout > style; (b) direct assessment of GPT-4V self-revision outputs: "can it replace the original?" and "which is better designed?" [V] (pp. 5–6, 15–16).
- Validation against human judgement: logistic regression on metric differences predicting Win/Lose, 50/50 split of the 100 annotated pages, 435 pairwise annotations, 79.9% test accuracy; coefficients Block-Match 0.7429, Position 0.7605, CLIP 0.4929, Color 0.3461 (all p ≤ 0.001), Text −0.3541 (p = 0.021) [V] (p. 7). Simulated win rates from a refit linear model (text removed) correlate with human "win + tie" rates across 10 systems: Pearson r = 0.975, Kendall τ = 0.931 [V] (p. 17). Inter-annotator agreement: Fleiss' κ = 0.46 (pairwise), 0.32 (replaceability), 0.26 (which is better) [V] (p. 16).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): only regression coefficient p-values and correlation significance (Table 7, p < 0.05 marks) [V] (pp. 7, 15). No significance tests, confidence intervals or variance across runs for model comparisons — not reported.

## 7. Key findings
1. GPT-4o is best on every automatic dimension (Direct: Block 93.0, Text 98.2, Position 85.5, Color 84.1, CLIP 90.4) [V] (p. 6); in human pairwise evaluation GPT-4o Direct wins 92% vs the Gemini baseline [V] (p. 7).
2. Text-augmented prompting raises Block-Match and Text for most models (e.g. GPT-4V Block 85.8 → 87.6; Gemini 80.2 → 84.8); self-revision helps GPT-4V and Claude 3 a little and does not help Gemini or open models (DeepSeek-VL self-revision collapses to Block 30.1) [V] (pp. 5–6).
3. Main weakness: models "mostly lag in recalling visual elements ... and generating correct layout designs" [A] (p. 1); on Design2Code-HARD, state-of-the-art models miss 30–40% of block elements (GPT-4o Direct Block 56.6) [V] (p. 8).
4. Fine-tuned open models (WebSight VLM-8B, Design2Code-18B) roughly match Gemini 1.0 Pro Vision Direct (Block 55.9 / 78.5 vs 80.2; CLIP 87.6 / 85.8 vs 84.4) [V] (p. 6).
5. Direct assessment: 49% of GPT-4V self-revision pages judged interchangeable with the reference; generated pages preferred over the original in 64% of cases [V] (p. 6). Kappa for these questions is low (0.32, 0.26) [V] (p. 16).
6. Humans weight high-level layout and presence of content, not exact text: text similarity has a negative coefficient in predicting preference [V] (p. 7). Human and automatic rankings disagree in places (e.g. humans prefer WebSight VLM-8B over Design2Code-18B despite worse Block-Match/Text) [V] (pp. 6–7).
7. Total tag count is the strongest difficulty indicator (r = −0.28 with Block-Match for GPT-4V self-revision); non-English pages are harder [V] (pp. 8, 15).
8. Code quality, maintainability or functional behaviour of the generated code is not measured; all metrics are visual/textual on rendered screenshots [V] (pp. 3–4).

## 8. Limitations stated by the authors
- Better prompting is needed for complex pages, e.g. incremental generation of page parts [A] (p. 10).
- Training directly on real webpages is hard because they are long and noisy [A] (p. 10).
- Input is screenshot-only; Figma frames or sketches would need a re-designed evaluation [A] (p. 10).
- Only static webpages; dynamic pages need evaluation of "interactive functions beyond just visual similarity" [A] (p. 10).
- Human evaluation should not be "blindly trusted as the oracle" because of human top-down attention bias [A] (pp. 7–8).
- Text-block matching may be imperfect when granularity differs (non-contiguous merges not searched) [A] (p. 13).

## 9. Limitations we identified
- [I] Fidelity is purely visual (screenshot similarity). No functional, behavioural, or code-level quality measure (e.g. HTML validity, semantic structure, maintainability, responsiveness) — based on metric definitions pp. 3–4. For our project this means Design2Code says nothing about whether a rebuilt page works or is maintainable.
- [I] JavaScript, iframes, SVG and external links are stripped and prompts say no JS is needed (pp. 13–14); the task is reconstruction of a static, de-functionalised snapshot, not of an application.
- [I] Human validation is modest: 100 pages, Fleiss' κ only 0.46/0.32/0.26 (p. 16), logistic regression accuracy 79.9% on a 50-page test half (p. 7). The very high Pearson r = 0.975 is computed over only 10 system-level points (p. 17) and compares predicted wins with human "win + tie" — an aggregation that inflates agreement.
- [I] Test pages come from C4, a common pretraining corpus; data contamination is not discussed (grep for "contamin" finds nothing).
- [I] Single run per configuration with greedy decoding; no variance or significance testing between models (pp. 5–6, 14).
- [I] Design2Code-HARD origin is inconsistent: "same filtering process" (p. 8) vs source "GitHub" (p. 14).
- [I] Element metrics are text-anchored (blocks come from text segments, p. 13); images, icons and non-text elements are only covered by CLIP.

## 10. Threats to validity
- Internal (confounds, leakage, selection): manual curation by the authors (selection bias towards well-formatted pages) (p. 13); possible C4 pretraining contamination (not discussed); Design2Code-18B checkpoint chosen on a 20-example dev set (p. 15) [I].
- External (generalisability of sample/context): static, single-page, English-dominant web pages with placeholders for media; HARD set of 80 (p. 8); no mobile apps, multi-page or interactive apps [I].
- Construct (do metrics measure the concept?): metrics measure visual similarity of a rendered screenshot, not functional fidelity or code quality; Text metric is negatively associated with human preference (p. 7), so the five metrics do not all point the same way [I].
- Statistical conclusion (power, multiple comparisons, variance): no CIs or tests for model differences; low-moderate inter-annotator agreement (p. 16); system-level correlation on n = 10 (p. 17) [I].
- Reproducibility (data/code/setup reported?): prompts, model versions and decoding settings reported (p. 14); fine-tuning hyper-parameters reported (p. 15); dataset release claimed but no link in our PDF (p. 10); commercial model versions may be deprecated [I].

## 11. Future research directions
- Stated by authors [A]: incremental generation for complex pages; cleaning pipelines for training on real webpages; Figma/sketch inputs; dynamic webpages with interactive-function evaluation (p. 10); "generate UIs that support dynamic user interactions" (p. 9); website-design improvement tools (p. 6).
- Suggested by us [I]: pair the visual metrics with behavioural tests and static code-quality analysis of the generated HTML/CSS; report run-to-run variance; check pretraining contamination of C4-sourced pages.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ4, RQ5 (RQ3 only by absence).
- How it informs our work [I]: Design2Code is the reference benchmark for screenshot-to-code reconstruction and the origin of the Block/Text/Position/Color/CLIP metric family reused by later work. It shows how visual fidelity can be measured and partly validated against humans, and it clearly leaves out interaction, functionality and code quality — the dimensions our project needs.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | Screenshot-to-HTML/CSS with MLLMs via direct, text-augmented and self-revision prompting, plus fine-tuned open models | p. 4–5 | V | moderate |
| RQ2 | Visual fidelity measured by Block-Match, Text, Position, Color (CIEDE2000) and CLIP on rendered screenshots | p. 3–5 | V | moderate |
| RQ2 | GPT-4o Direct best: Block 93.0, Text 98.2, Position 85.5, Color 84.1, CLIP 90.4 on 484 pages | p. 6 | V | moderate |
| RQ2 | On 80 HARD pages SOTA models miss 30–40% of blocks (GPT-4o Direct Block 56.6) | p. 8 | V | moderate |
| RQ2 | 49% of GPT-4V self-revision pages judged interchangeable with the original (κ = 0.32) | p. 6, 16 | V | weak |
| RQ3 | No code quality or maintainability measure; only rendered visual similarity | p. 3–4 | V | moderate |
| RQ4 | Metrics predict human Win/Lose with 79.9% accuracy (logistic regression, 50-page test half); Text coefficient negative | p. 7 | V | moderate |
| RQ4 | Simulated vs human win rates: Pearson r = 0.975, Kendall τ = 0.931 over 10 systems | p. 17 | V | weak |
| RQ4 | Human agreement low-moderate: Fleiss' κ 0.46 / 0.32 / 0.26 | p. 16 | V | moderate |
| RQ4 | No significance tests or variance across runs for model comparisons | p. 5–6 | I | moderate |
| RQ5 | Authors call for dynamic webpages evaluated on interactive functions beyond visual similarity | p. 10 | A | moderate |

## 14. Key quotes
> "models mostly lag in recalling visual elements from the input webpages and generating correct layout designs" (p. 1)
> "We find that 49% of the AI-generated webpages are considered exchangeable with the reference webpages." (p. 6)
> "This also requires the evaluation to consider interactive functions beyond just visual similarity." (p. 10)

## Analyst notes
- Reading coverage: whole PDF read (pp. 1–19), including appendices A–I; reference list skimmed only.
- Uncertainties: dataset/code URL not given in our ACL PDF (the arXiv version may differ); HARD-set source inconsistent between p. 8 and p. 14; the logistic-regression test-set size in pairs is not stated separately (435 is the total of usable pairs). Peer-reviewed (NAACL 2025, tier 1).
