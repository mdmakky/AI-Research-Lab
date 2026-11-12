---
key: fu2023chatgpt
status: complete
evidence_basis: full-text
design: Short empirical comparison; prompted ChatGPT (gpt-3.5-turbo, gpt-4) vs fine-tuned code LMs on four vulnerability tasks
dataset: Big-Vul (C/C++, random 80/10/10 split); Big-Vul+CVEFixes repair pairs (Chen et al.)
sample_size: ~188k C/C++ functions (Big-Vul) + 5.5k repair pairs; number of functions actually sent to ChatGPT not reported
metrics: F1, precision, recall, top-10 line accuracy, multiclass accuracy, MSE/MAE, %PP, BLEU, METEOR
main_finding: Prompted gpt-4 reaches F1 29% (gpt-3.5: 10%) vs fine-tuned AIBugHunter 94% on Big-Vul; ChatGPT worst on all four tasks.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# ChatGPT for Vulnerability Detection, Classification, and Repair: How Far Are We?

- Authors: Fu, Michael; Tantithamthavorn, Chakkrit Kla; Nguyen, Van; Le, Trung
- Year / venue: 2023, 2023 30th Asia-Pacific Software Engineering Conference (APSEC) (published)
- DOI: 10.1109/apsec60848.2023.00085 · URL: https://doi.org/10.1109/apsec60848.2023.00085
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] To assess how well prompted ChatGPT (gpt-3.5-turbo and gpt-4) performs on four vulnerability tasks (function- and line-level vulnerability prediction, CWE-type classification, CVSS severity estimation, vulnerability repair) compared with smaller language models fine-tuned for these tasks (p. 1).
- [A] Motivation: ChatGPT's weights are proprietary, so the authors cannot fine-tune it; the comparison is therefore prompted ChatGPT vs fine-tuned code LMs (p. 1).

## 2. Research questions / hypotheses
- [A] RQ1 accuracy of ChatGPT for function- and line-level vulnerability prediction; RQ2 for vulnerability-type (CWE-ID) classification; RQ3 for severity (CVSS) estimation; RQ4 for automated vulnerability repair (p. 1–2).
- No formal hypotheses.

## 3. Methodology
- Research design: [V] Benchmark comparison on held-out test splits of existing datasets; ChatGPT used via prompting through the paid OpenAI API; baselines replicated with the original authors' parameter settings (p. 3).
- Approach / model / intervention: [V] gpt-3.5-turbo and gpt-4 with task prompts (Fig. 1–4). Detection: task description plus return-format instruction; for vulnerable functions a follow-up prompt asks for the top-10 most vulnerability-prone lines (p. 2). Classification: ChatGPT is told the function is vulnerable and given a list of candidate CWE-IDs (p. 2). Repair: prompt includes three repair examples (p. 3). [I] The detection prompt appears to be zero-shot (based on the description on p. 2; the prompt itself is only shown as a figure).
- Baselines or comparison conditions: [V] AIBugHunter (fine-tuned LMs, ~120M parameters), CodeBERT, GraphCodeBERT (all fine-tuned); VulExplainer added for CWE classification (p. 3–4). [V] No static-analysis (SAST) tool baseline is included (p. 3).

## 4. Dataset and sample
- Data source(s): [V] Big-Vul (Fan et al.) for RQ1–RQ3: 188k C/C++ functions from 348 GitHub projects, 3,754 vulnerabilities across 91 types, vulnerable functions labelled with CWE-ID and CVSS score, vulnerable:benign ratio 1:20 (p. 3). [V] Big-Vul + CVEFixes as pre-processed by Chen et al. for repair: 5.5k vulnerable-function/patch pairs (p. 3).
- Sample size (N) and unit: [V] Function. Big-Vul split 80/10/10 (train/val/test); repair data split 70/10/20 (p. 3). The number of test functions actually submitted to ChatGPT is not reported.
- Sampling / selection method: [V] Split "similar to previous studies" (p. 3); no de-duplication or time-based split is reported.
- Data availability (public? link?): [A] Dataset, prompts and results published at https://github.com/awsm-research/ChatGPT4Vul (p. 1).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Baselines replicated with original settings on AMD Ryzen 9 5950X, 64 GB RAM, RTX 3090 (p. 3). [V] Greedy decoding for fine-tuned repair models "to ensure a fair comparison with ChatGPT" (p. 5). ChatGPT temperature, model snapshot/date and number of runs: not reported.
- Code availability: [A] repository above (p. 1).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [V] F1, precision, recall (function level) and top-10 accuracy (share of vulnerable functions with at least one true vulnerable line in the top-10 ranking), following LineVul (p. 3); multiclass accuracy for CWE classification (p. 4); MSE and MAE for CVSS v3.1 estimation (p. 4); %PP (exact match with ground-truth patch), BLEU and METEOR for repair (p. 4–5).
- Statistical testing (tests used, significance, effect sizes, confidence intervals): not reported (single point estimates in bar charts).

## 7. Key findings
1. Function-level detection, Big-Vul test split, F1: AIBugHunter 94%, CodeBERT 87%, GraphCodeBERT 35%, gpt-4 29%, gpt-3.5-turbo 10% — [V] (p. 4, Fig. 5; text p. 3).
2. Precision: AIBugHunter 98%, CodeBERT 92%, GraphCodeBERT 50%, gpt-4 25%, gpt-3.5-turbo 11%. Recall: AIBugHunter 90%, CodeBERT 83%, gpt-4 33%, GraphCodeBERT 27%, gpt-3.5-turbo 9% — [V] (p. 4, Fig. 5).
3. Line-level top-10 accuracy: AIBugHunter 99%, CodeBERT 99%, GraphCodeBERT 87%, gpt-4 65%, gpt-3.5-turbo 25% — [V] (p. 4, Fig. 5; text p. 3).
4. CWE-ID classification accuracy: fine-tuned baselines 62–65% (AIBugHunter 65%, VulExplainer 65%, CodeBERT 63%, GraphCodeBERT 62%) vs gpt-4 20% and gpt-3.5-turbo 13% — [V] (p. 4, Fig. 6).
5. CVSS severity: MSE 1.8–1.86 for fine-tuned baselines vs 5.4 (gpt-3.5-turbo) and 5.85 (gpt-4); MAE 0.83–0.93 vs 1.84 and 1.86 — [V] (p. 4, Fig. 7).
6. Repair %PP: AIBugHunter (VulRepair) 30, GraphCodeBERT 9, CodeBERT 7, gpt-3.5-turbo 0, gpt-4 0 — [V] (p. 5, Fig. 8).
7. Despite ~14,000× more parameters than CodeBERT, ChatGPT needs domain-specific fine-tuning to generalise to vulnerability tasks — [A] (p. 1, p. 5).

## 8. Limitations stated by the authors
- [A] None. The paper has no limitations or threats-to-validity section; the only constraint mentioned is that ChatGPT's parameters are proprietary and cannot be fine-tuned (p. 1).

## 9. Limitations we identified
- [I] Short paper (5 PDF pages including references): method detail is thin — number of test samples sent to ChatGPT, temperature, model snapshot dates, repeated runs and the full detection prompt text are not given in the text.
- [I] Evaluation uses a random Big-Vul split with no de-duplication or temporal split. Ding et al. report 12.7% exact-copy leakage for Big-Vul [@ding2025vulnerability, p. 4]; Big-Vul vulnerable-label accuracy is ~25% per Chen et al., as reported by [@ding2025vulnerability, p. 4], and 39% in Risse et al.'s own n=100 audit [@risse2025top, p. 8]; Risse et al. also reach 86% F1 on Big-Vul from word counts alone; both suggest the 94% F1 of the fine-tuned baseline is inflated by dataset artefacts that in-distribution fine-tuning can exploit but prompting cannot. The size of the LLM-vs-fine-tuned gap may therefore partly reflect benchmark artefacts (based on [@ding2025vulnerability, p. 4] and [@risse2025top, p. 11]).
- [I] Asymmetric comparison: baselines are fine-tuned on Big-Vul training data, ChatGPT is prompted. The result answers "prompting vs in-distribution fine-tuning", not "LLM vs DL" in general.
- [I] The first two authors also built the strongest baselines (AIBugHunter, LineVul, VulRepair, VulExplainer — refs [8]–[11], p. 5). Not a funding conflict, but the comparison favours the authors' own tools and should be read with that in mind.
- [I] GraphCodeBERT F1 35% vs CodeBERT 87% on the same data is an unusually large gap that the paper does not discuss (p. 4, Fig. 5); the dagger marks on CodeBERT/GraphCodeBERT in Fig. 5–7 are not explained in the text.
- [I] %PP (exact match) is a very strict repair metric; 0% for ChatGPT may partly reflect format mismatch with Chen et al.'s patch representation, which the authors tried to mitigate with three in-prompt examples (p. 3).

## 10. Threats to validity
- Internal (confounds, leakage, selection): [I] Random Big-Vul split without reported de-duplication → possible train/test leakage that only benefits the fine-tuned baselines; prompt design not tuned or ablated; single run.
- External (generalisability of sample/context): [I] C/C++ only, one detection dataset, one 2023 snapshot of each ChatGPT model; results may not transfer to newer LLMs, other prompting strategies or other languages.
- Construct (do metrics measure the concept?): [I] F1 on a 1:20 dataset whose vulnerable labels are largely inaccurate per later audits, so "correct" predictions need not be detected vulnerabilities; %PP measures textual identity, not functional correctness.
- Statistical conclusion (power, multiple comparisons, variance): [I] No variance, confidence intervals or significance tests; LLM outputs are non-deterministic and only one run is implied.
- Reproducibility (data/code/setup reported?): [A] Data, prompts and results released (p. 1); [I] model versions and temperature are not stated, and hosted OpenAI models change over time.

## 11. Future research directions
- Stated by authors [A] (p. 5): fine-tuning on domain-specific data is "crucial" for ChatGPT to generalise to vulnerability repair, and "pivotal" for vulnerability tasks in general.
- Suggested by us [I]: re-run the prompted-LLM vs fine-tuned comparison on a de-duplicated, temporally split, label-verified benchmark (e.g. PrimeVul), add a SAST baseline, and report variance across repeated LLM runs.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ2, RQ4.
- How it informs our work [I]: An early, widely cited head-to-head of prompted ChatGPT vs fine-tuned code LMs showing a large gap in favour of fine-tuned models on Big-Vul. For RQ2 it illustrates how a random-split Big-Vul evaluation can make fine-tuned models look near-perfect. It should be read together with ding2025vulnerability, where the ordering reverses only under a different metric and test set: on 564 PrimeVul pairs scored by pair-wise correctness (P-C), GPT models beat fine-tuned models, although all are at or below random guessing [@ding2025vulnerability, p. 9]. On Big-Vul with F1, Ding's own fine-tuned rows (62.88–68.26%) agree with this paper's direction [@ding2025vulnerability, p. 7]; the apparent contradiction is therefore one of metric (F1 vs P-C) and dataset (random-split Big-Vul 1:20 vs de-duplicated temporal PrimeVul pairs).

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | On Big-Vul (random split), prompted gpt-4 F1 29% and gpt-3.5-turbo F1 10% vs fine-tuned AIBugHunter 94% and CodeBERT 87% for function-level detection | 4 | V | moderate |
| RQ1 | Line-level top-10 accuracy: gpt-4 65%, gpt-3.5-turbo 25% vs AIBugHunter/CodeBERT 99% | 4 | V | moderate |
| RQ4 | CWE-ID classification accuracy: ChatGPT 13–20% vs fine-tuned models 62–65% (C/C++, Big-Vul) | 4 | V | moderate |
| RQ1 | ChatGPT produced 0% exact-match repairs vs 7–30% for fine-tuned models | 5 | V | weak |
| RQ2 | Evaluation used an 80/10/10 Big-Vul split (1:20 ratio) with no de-duplication or temporal split reported | 3 | V | moderate |
| RQ5 | Authors argue prompted LLMs lack security domain knowledge and need fine-tuning for vulnerability tasks | 5 | A | weak |

## 14. Key quotes
> "the fine-tuned AIBugHunter achieves an F1-measure of 94% along with a top-10 accuracy of 99% with only 120 million parameters" (p. 3)

> "ChatGPT failed to generate correct repair patches for all of the vulnerable functions in our testing data." (p. 5)

## Analyst notes
- Reading coverage: whole paper read (5 PDF pages: abstract, introduction, related work, prompt design, experiments, conclusion, references). Bar-chart values in Fig. 5–8 were read from the rendered PDF pages 4–5 because text extraction garbles the axis labels.
- Source version: arXiv 2310.09810v1 (15 Oct 2023); the published version is APSEC 2023 (DOI above). Page refs are to the arXiv PDF; small differences from the APSEC version are possible.
- Short paper (5 pages, self-described "pilot study", p. 2): weight accordingly in synthesis.
- Uncertainties: ChatGPT test-set size, full detection prompt (figure only), model snapshot dates and temperature are not reported. In Fig. 5 gpt-4 recall (33%) is above GraphCodeBERT (27%) although its F1 is lower — values read from the rendered figure.
