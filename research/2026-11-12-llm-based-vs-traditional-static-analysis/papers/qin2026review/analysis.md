---
key: qin2026review
status: complete
evidence_basis: full-text
design: narrative (non-systematic) literature review, single author; no search protocol or quality assessment
dataset: none (secondary); 32 cited references, 2019-2026
sample_size: 32 references (no stated corpus of primary studies)
metrics: none (qualitative synthesis; re-reports P/R/F1, VD-S, Top-k, Effort@Recall from cited papers)
main_finding: LLM gains on benchmarks are inflated by duplicates, label noise, random/temporal splits; evidence supports SAST-LLM-human complementarity, not replacement.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# A Review of Source Code Vulnerability Detection Methods Based on Large Language Models: Models, Techniques, and Evaluation

- Authors: Qin, Letong
- Year / venue: 2026, Computers and Artificial Intelligence (published) — **venue flag [I]:** published by Zeus Press (p. 1); no peer-review statement or received/accepted dates in the PDF (pp. 1–16); low-visibility source not in DOAJ (OpenAlex, 2026-11-12). Peer review is not documented; weight like grey literature (see Analyst notes).
- DOI: 10.70267/cai.v3n5.122137 · URL: https://doi.org/10.70267/cai.v3n5.122137
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
- [A] Review source-code vulnerability detection with "lightweight code Transformers and large-scale language models" as the two lines of discussion, covering input construction, task adaptation, use of program-analysis information and multi-model collaboration, and compare them by datasets, metrics and deployment conditions (p. 1).
- [A] Scope is limited to source-code-level detection, localization and classification; network intrusion, malware, smart contracts, vulnerability generation and automatic repair are excluded (p. 1).

## 2. Research questions / hypotheses
- [A] Three organising questions in the introduction: what capabilities methods actually improve, under what data conditions/protocols the gains are obtained, and whether evidence suffices for real-world deployment (p. 2).
- [A] Four formal RQs: RQ1 development from sequence/graph models to code pretraining and LLM interaction; RQ2 performance evidence of direct prompting, in-context learning, fine-tuning, structural enhancement and multi-model collaboration; RQ3 effects of label noise, duplication, class imbalance and temporal leakage; RQ4 how cross-project, out-of-time, false-positive-cost, localization and explanation evaluation approach deployment (p. 4).
- [I] The two framings are not reconciled: the introduction organises the paper around "three closely related questions" (p. 2), while Section 3.1 sets four formal RQs (p. 4), and the paper does not map one onto the other. Separately, it gives "medium confidence to C2" (p. 12), but no claim labelled C1/C2 is defined anywhere in the text.

## 3. Methodology
- Research design: [I] Narrative (traditional) review. The paper calls itself a "review" (p. 1) and gives no search strategy, databases, search strings, date window, inclusion/exclusion screening, PRISMA flow, or study-quality assessment — all "not reported". The only inclusion rule stated is that it "includes only studies that directly analyze source code" and excludes repair (p. 4).
- Approach / taxonomy: [A] Methods are classified "by how vulnerability knowledge is acquired" rather than by model scale, core technology or supply-chain stage as in earlier reviews (p. 4). Two routes: (a) lightweight code Transformers — code pretraining + supervised fine-tuning, input granularity, structural fusion (pp. 5–6); (b) large-scale LLMs — supervised fine-tuning/steering, multitask learning, direct prompting, few-shot/ICL, hybrid detection with program analysis, ensembles/multi-model collaboration, explanation (pp. 6–9). Figure 1 adds cross-cutting layers "Data and bias", "Reliability evaluation" and "Discussion and outlook" (p. 3) [V, from figure].
- Baselines or comparison conditions: [A] Traditional methods (SAST, GNNs) are discussed "only in two situations": to motivate structural information for Transformers and as baselines or external tools for LLMs; "this paper does not provide a separate review of traditional detection methods" (p. 4). Section 7.1 nevertheless compares LLMs with DL and SAST qualitatively (pp. 11–12).

## 4. Dataset and sample
- Data source(s): [V] Secondary literature; the reference list has 32 entries (pp. 14–16).
- Sample size (N) and unit: [I] No corpus size is stated; we counted 32 references (pp. 14–16), of which about 16 are LLM-based detection or evaluation studies (our count of the reference list). Table 1 lists 12 representative methods, 8 of them LLM-based (GRACE, EnStack, DLAP, fine-tuning LLM, LLMVulExp, cross-project zero-shot, context-enhanced, M2CVD; pp. 6–7). Several references are themselves reviews/surveys [2–4, 18–21] (pp. 14–15).
- Sampling / selection method: not reported. [I] Reference years run 2019–2026 (pp. 14–16), but no time window is stated. Figure 2 places milestones from 2019 (Devign) to 2026 (context enhancement, M2CVD) (p. 4) [V, from figure].
- Data availability: not applicable / not reported (no extraction sheet or study list released).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: not applicable (no experiments). [A] One quantitative re-report (no new analysis): the review restates PrimeVul Table V for five code LMs — BigVul train/test F1 62.88%–68.26%, BigVul→PrimeVul F1 1.91%–5.82%, PrimeVul train/test F1 18.05%–21.43%, VD-S 88.78%–91.51%, paired-both-correct 1.06%–3.01%, paired-both-benign 84.22%–88.30% (p. 12). [I] We checked all six ranges against the primary source: they match Table V [@ding2025vulnerability, p. 7]. For evidence, cite ding2025vulnerability directly, not this review.
- Code availability: not applicable.

## 6. Evaluation metrics
- Metric — what it measures — why chosen: [A] The review recommends reporting at least Precision, Recall, F1 and a confusion matrix, grouped by project, time, language or CWE; Top-k and audit effort at fixed recall for localization; separate checks of location/type/cause/suggestion for explanations; Accuracy only as supplementary; mean, fluctuation range and parse-failure rate for repeated LLM calls (p. 11). It re-reports VD-Score and paired metrics from PrimeVul (p. 11) and Top-10 Accuracy/Effort@20%Recall from LineVul (p. 5).
- Statistical testing: not applicable; the review does no pooling, meta-analysis or effect-size synthesis (not reported).

## 7. Key findings
1. Benchmark inflation — [A] Gains from code pretraining, prompting, fine-tuning and structural enhancement hold "on specific benchmarks" but are "easily affected by duplicate samples, label noise, random splits, temporal leakage, and changes in model versions" (p. 1). Supported by the PrimeVul re-report (primary source: [@ding2025vulnerability, p. 7]): StarCoder2 F1 68.26% on BigVul vs 3.09% on the PrimeVul test set (p. 2) and the five-model ranges above (p. 12).
2. Random-split F1 should be called "within-benchmark performance", not a real-world detection rate; out-of-time testing should be a reliability baseline, combined with project isolation and reporting of time windows, data-freeze dates and model knowledge cutoffs (p. 10) — [A].
3. Contamination from pretraining corpora is treated "as an alternative explanation that needs to be audited", not a confirmed fact; knowledge-cutoff dates are not proof of no contamination (p. 10) — [A].
4. Cross-study ranking is not possible: GRACE, DLAP, context enhancement and M2CVD "all report gains in their own settings, but datasets, model versions, and evaluation protocols differ, so they cannot be directly ranked" (p. 12) — [A]. [A] Table 2 is a normative risk matrix (the author's recommendations, not data): label noise, exact/near duplicates, pretraining contamination, random splitting, cross-project/language failure, class imbalance, false-positive cost, explanation/version validity, each with identification signals and mitigations (pp. 10–11).
5. LLM vs SAST vs DL — [A] "SAST is usually more stable within the scope covered by existing rules, whereas LLMs are better at semantic summarization and alert explanation"; unified benchmarks "support complementarity rather than complete replacement", with the two tool types finding different vulnerabilities and different false positives (p. 12). It cites [1] and [15]. [1] is a SAST-only study of query-based C/C++ tools (p. 14); [15] is the Gnieciak & Szandala LLM-vs-SAST benchmark (p. 15), its only head-to-head source. No numbers for this comparison are given. [I] Qin leaves out that [15] found LLMs above SAST on mean F1 (0.75–0.80 vs 0.26–0.55) [@gnieciak2025large, p. 10]. "SAST is usually more stable" is therefore not supported by its own cited comparison. Cite gnieciak2025large directly for this comparison.
6. Hybrids — [A] Proposed workflow: "SAST candidate generation-LLM review or explanation-human confirmation" (p. 8), to be judged by audit time, false-negative control and explanation consistency rather than overall F1 (p. 8); outputs should not be "simply concatenate[d]" (p. 13). Evidence cited is GRACE (structure + ICL, ≥28.65% relative F1 gain over six baselines, p. 8), DLAP (DL-augmented prompting, p. 8) and the context-enhancement study [29] (p. 8). No quantitative evidence on SAST+LLM hybrids is reported.
7. Cost — [A] API calls, GPU memory, latency, model updates and prompt maintenance should be counted; sensitive code and local large-scale scanning suit lightweight models or SAST; high-risk scenarios should use hybrid workflows with human confirmation (p. 12). No cost figures are reported.
8. Re-reported primary numbers (all [A], from cited papers): LineVul 188k+ functions, F1 +160%–379% over baselines, Top-10 Accuracy +12%–25%, Effort@20%Recall −29%–53% (p. 5); DiverseVul 7,514 commits, 18,945 vulnerable / 330,492 non-vulnerable functions, 150 CWEs (p. 9); LLMVulExp average F1 92.4% on SeVC single-type setting (p. 8).

## 8. Limitations stated by the authors
- [A] No separate limitations section. Scope exclusions: network intrusion, malware, smart contracts, generation, repair (p. 1).
- [A] Traditional detection methods are not reviewed separately (p. 4).
- [A] Specific caveats on cited evidence: the PrimeVul conclusion "is limited to the five models and three settings in Table V" (p. 12); LLMVulExp results "cannot be directly generalized to PrimeVul, cross-project testing, or real deployment" (pp. 8–9); GRACE gain is relative and applies only to the tested configurations (p. 8).

## 9. Limitations we identified
- [I] Not systematic: no search protocol, databases, screening, corpus count or quality assessment (absence across pp. 1–4). Its conclusions cannot be checked for selection bias, and it cannot be cited as a systematic review.
- [I] Small and selective corpus (32 references, pp. 14–16). Missing, among others, project-scale LLM/SAST studies and LLM-based SAST-alarm filtering work that we have (e.g. li2026llm, du2026reducing, xiong2026sifting, li2024iris, guo2025repoaudit); hybrid claims rest on GRACE, DLAP and one context-enhancement study (p. 8), not on SAST+LLM evaluations.
- [I] SAST is explicitly out of scope (p. 4), yet the review draws an LLM-vs-SAST conclusion (p. 12) from two references [1, 15] with no numbers. Only [15] compares the two families, and it favours LLMs on F1 [@gnieciak2025large, p. 10]. That conclusion is under-supported.
- [I] Contradictions are explained only in general terms. Apart from the PrimeVul Table V re-reading (p. 12), it does not tabulate conflicting results from different studies side by side against their evaluation setups (benchmark, split, class ratio, granularity). Table 1 (pp. 6–7) is qualitative: no numbers, no split type per study.
- [I] Cites PrimeVul as a 2024 arXiv preprint (p. 15) and leans heavily on that one study for the inflation argument.
- [I] Editorial loose ends (the three framing questions on p. 2 are not reconciled with the four formal RQs on p. 4; "C2" on p. 12 is undefined) suggest light editorial review (see Analyst notes on venue).

## 10. Threats to validity
- Internal (selection): [I] Unknown selection process, so selection bias cannot be judged; the reviewer's framing (evaluation pitfalls) may have driven which studies were cited.
- External: [I] Mostly C/C++ function-level benchmarks (BigVul, PrimeVul, DiverseVul, SeVC, ReVeal, FFmpeg+Qemu; pp. 8–9, 12); multilingual evidence is one reference [32] (p. 13).
- Source dependence: [I] Its quantitative claims rest on a handful of cited studies, mainly PrimeVul [14] for benchmark inflation (pp. 2, 12) and Gnieciak & Szandala [15] for LLM vs SAST (p. 12). Both are already in our corpus (ding2025vulnerability, gnieciak2025large). Counting this review as extra support for the same claims would double-count them.
- Construct: [I] Good conceptual separation of label correctness, localization and explanation evidence (p. 4); recommends metrics beyond F1 (p. 11).
- Statistical conclusion: [I] No quantitative synthesis; confidence levels ("medium confidence to C2", p. 12) are given without a stated grading scheme.
- Reproducibility: [I] Not reproducible as a review (no protocol, no study list beyond references).

## 11. Future research directions
- Stated by authors [A]: traceable data pipelines with commit, time, label-source and duplicate statistics and updateable data cards (p. 13); out-of-time and project-isolated testing as main evidence, random splits only for historical comparison (p. 13); uncertainty calibration, risk-coverage curves and recall at a fixed false-positive budget (p. 13); decomposed verification of explanations (location, trigger, path, CWE, fix) (p. 13); human-machine studies recording audit time per real vulnerability (p. 13); SAST-LLM systems that measure candidate recall, LLM filtering gain, explanation correctness and total audit cost separately (p. 13); preserving system prompts, model IDs, call dates, temperatures and repetition counts (p. 13).
- Suggested by us [I]: a systematic, protocol-based review that puts SAST, DL and LLM results on the same evaluation-setup axes. This is exactly the gap between this review and ours.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2 (primary), RQ3 (conceptual only), RQ1 (qualitative only), RQ5.
- How it informs our work [I]: This is the closest competing review and must be cited for positioning. Overlap: evaluation-reliability framing (duplicates, label noise, temporal splits, contamination) and the SAST-LLM-human workflow recommendation. Difference: it is narrative, has a small corpus (32 references), explicitly excludes SAST as a reviewed family, gives no quantitative LLM-vs-SAST or hybrid evidence, and does not map contradictions study-by-study onto evaluation setup. Our contribution should be stated against those four points. Its recommendations agree with our RQ2 answer, but they do not corroborate it independently: qin cites ding2025vulnerability [14], gnieciak2025large [15] and sheng2025llms [21] (p. 15), which are all in our corpus. Weak strength; use it for positioning only.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | Benchmark gains are inflated by duplicates, label noise, random splits, temporal leakage and model-version changes; random-split F1 = "within-benchmark performance" only | 1, 10 | A | weak (narrative review) |
| RQ2 | Re-reports PrimeVul Table V: five code LMs F1 62.88–68.26% on BigVul vs 1.91–5.82% BigVul→PrimeVul vs 18.05–21.43% PrimeVul→PrimeVul; all ranges match the primary source [@ding2025vulnerability, p. 7] — cite ding directly | 12 | A | weak (secondary re-report; not independent of ding2025vulnerability) |
| RQ2 | LLM methods (GRACE, DLAP, context enhancement, M2CVD) cannot be ranked because datasets, model versions and protocols differ | 12 | A | weak |
| RQ1 | SAST more stable within rule coverage; LLMs better at semantic summarisation/explanation; unified benchmarks support complementarity, not replacement (no numbers; its only head-to-head source found LLMs above SAST on F1 [@gnieciak2025large, p. 10]) | 12 | A | weak |
| RQ3 | Recommends SAST candidates → LLM ranking/explanation → human confirmation; judge by audit time, false negatives, explanation consistency, not F1 | 8, 13 | A | weak (no quantitative hybrid evidence) |
| RQ3 | Costs (API calls, GPU memory, latency, version drift, prompt maintenance) should be reported; none quantified | 9, 12 | A | weak |
| RQ5 | Open problems: out-of-time + project-isolated testing, data cards, uncertainty calibration, fixed-FP-budget recall, explanation verification, audit-time studies | 13 | A | weak |

## 14. Key quotes
> "this paper does not provide a separate review of traditional detection methods" (p. 4)

> "Existing evidence from unified benchmarks supports complementarity rather than complete replacement by one tool" (p. 12)

> "F1 obtained from a random split should be called “within-benchmark performance” and cannot be directly described as a “real-world detection rate”" (p. 10)

## Analyst notes
- Reading coverage: all 16 PDF pages read in full, including references, funding and copyright notes (pp. 14–16). Figures 1–2 (pp. 3–4) read from the PDF images because pdftotext dropped them.
- Venue quality [I]: Computers and Artificial Intelligence, Vol. 3 No. 5 (2026), E-ISSN 3006-3728, published by "Zeus Press" (p. 1). The PDF has no received/revised/accepted dates and no editor or peer-review statement (pp. 1–16). OpenAlex (queried 2026-11-12) lists the source with no host organisation, `is_in_doaj: false`, `is_core: false`, no indexing lists, and publication date 2026-10-29; cited_by 0 in metadata. The acknowledgment reads only "This paper is an output of the science project." (p. 16). There is a single author, and editorial loose ends remain (framing questions not reconciled with the formal RQs; "C2" undefined). Together these are warning signs of a low-visibility venue with uncertain peer review. We did not confirm that it is predatory. Treat it as tier 1 by `venue_kind` but weight it like grey literature. Cite it for positioning, not as evidence.
- Competitor positioning [I]: SAST tools are covered only as baselines/external tools, not reviewed (p. 4). Hybrids are covered conceptually (pp. 8, 13), with no SAST+LLM empirical studies. Cross-study contradictions are explained via evaluation setup in general terms and through one worked example (PrimeVul, p. 12), not systematically.
- Uncertainties: whether a systematic search was done but simply not reported. Numbers it gives for other papers are labelled [A] here; only the PrimeVul numbers (all six ranges, ding2025vulnerability Table V, p. 7) and the cited LLM-vs-SAST result (gnieciak2025large, p. 10) were cross-checked against a primary text.
- Review fixes 2026-11-12 (critical review C, findings 1–9): PrimeVul re-report relabelled [A] and its evidence row downgraded to weak; Table 1 count corrected to 12 methods (8 LLM-based); [1] identified as SAST-only, and the omitted gnieciak F1 result added; "independent corroboration" removed; Table 2 relabelled [A] (normative); RQ-framing wording softened; venue flag added to header; source-dependence threat added.
