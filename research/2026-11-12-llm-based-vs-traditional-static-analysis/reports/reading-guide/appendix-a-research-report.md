# Appendix A: Full Research Report

- Project: `2026-11-12-llm-based-vs-traditional-static-analysis`
- Date: pass 2 (24 papers), 2026-11-12
- **What changed since the pass-1 report** (`research-report-2026-11-12.md`, 20 papers, kept unchanged): four papers were added and read in full (deininger2026open, lu2025lab, tashenova2026real, qin2026review). As a result, all five research-question answers, two new contradictions (C7, C8), the gap list (G2, G5 and G6 narrowed) and the recommended next steps have been updated.
- Based on: 24 full-text analyses, `evidence-matrix.md`, `reports/methodology-comparison.md`, `gap-report.md`, four critical reviews (A and B for pass 1, C and D for pass 2, all 2026-11-12), `search/screening.md`, `search/search-log.md`.
- How to read the labels: **[V]** means we checked the number in the paper's own tables or results, **[A]** means the authors say it but we cannot check it, and **[I]** is our own interpretation. Unlabelled numbers are [V] from the cited page. Citations give the paper's folder name and the PDF page, e.g. `[@risse2025top, p. 8]`.

## 1. Summary in plain language

We asked whether large language models (LLMs, such as GPT-4 or Claude) find security bugs in source code better than two older approaches: rule-based scanners (SAST tools such as CodeQL or Semgrep) and neural networks trained on labelled vulnerable code (deep-learning or "DL" detectors). After reading 24 papers in full, the short answer is still that **no approach wins everywhere**: LLMs come out ahead on small, self-contained programs [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11], CodeQL on synthetic test suites [@khare2025understanding, p. 9], and on large real projects both miss many bugs and raise many false alarms [@li2026llm, p. 7; @li2026llm, p. 11]. The only study that tests all three families on the same real functions finds that the winner depends on the score you choose: a fine-tuned DL model has the best overall score, two of the scanners are the most precise (their warnings are least often false alarms), and the LLMs sit in between [@deininger2026open, p. 8; @deininger2026open, p. 11]. The most consistent pattern [I] is that LLMs find more of the real bugs (higher recall) but also flag much more harmless code (lower precision); when vulnerable code is as rare as in real software (about 2% of functions), their precision is barely better than a rule that flags everything, and on vulnerabilities from 2025 trained DL detectors do little better [@deininger2026open, p. 8; @lu2025lab, p. 13; @lu2025lab, p. 14]. A large part of the disagreement between papers comes from **how** they test, not from the tools themselves: label quality, overlap between training and test data, the share of vulnerable samples, and how lenient the scoring is [@risse2025top, p. 8; @ding2025vulnerability, p. 4; @shu2026evaluating, p. 40; @gnieciak2025large, p. 6]. Letting an LLM filter a scanner's alarms removes most false alarms cheaply but also throws away 12–25% of real bugs [@du2026reducing, p. 8; @xiong2026sifting, p. 18]. For your comparative review, this "setup explains the contradictions" angle, applied across all three families, is still the contribution we could not find in existing reviews (medium confidence). The easiest concrete addition is to re-score the published results against a "flag everything" baseline, which needs only a spreadsheet.

## 2. What we did

- **Scope.** Source-code vulnerability detection by LLMs, SAST tools, DL detectors and LLM+SAST hybrids, published 2020–2026. Binary analysis, fuzzing and repair-only work were excluded (`RESEARCH.md`).
- **Searches.** Three search agents covered six facets: head-to-head LLM vs SAST, LLM vs DL, hybrids, evaluation realism, reasoning/agentic LLMs, and surveys. They ran about 19 searches on OpenAlex, Crossref and arXiv, plus *snowballing*, which means following the references and citations of central papers. Every search is logged in `search/search-log.md`, and every screening decision with its reason is in `search/screening.md`.
- **Two passes.** Pass 1 analysed 20 papers. The pass-1 gap check found four papers that bore directly on our gaps and on the positioning of the review; with your approval they were added in pass 2.
- **Included papers.** 24 papers in total: 20 primary studies and 4 reviews (kaniewski2026systematic, zhou2025large, sheng2025llms and qin2026review). `rlab status` counts 4 of the 24 as preprints:
  - IRIS [@li2024iris, p. 1] and RepoAudit [@guo2025repoaudit, p. 1] appeared at ICLR 2025 and ICML 2025. Both are peer-reviewed, but `rlab` records them as arXiv preprints because those venues issue no DOIs.
  - lu2025lab is recorded as an arXiv preprint, but it is published in the *Journal of Systems and Software* (2026, doi:10.1016/j.jss.2026.113185), so we treat it as peer-reviewed. We read the arXiv v4 accepted manuscript, and its page references follow that version [@lu2025lab, p. 1].
  - Only zhou2024comparison is a true preprint, meaning it is **not peer-reviewed** [@zhou2024comparison, p. 1].
  - qin2026review is published, but in a low-visibility venue that does not document peer review [@qin2026review, p. 1]. It is a weak narrative review (single author, no search protocol), so we give it the weight of *grey literature* (material outside the normal peer-reviewed channels) and use it only to position our review.
  - One pass-1 candidate (VulnLLM-R) was dropped to keep to the 20-paper target, because it is a preprint with no venue.
- **Full text.** 24 of 24 papers were read in full and none were abstract-only (`rlab status`).
  - Pass 1: 18 PDFs were fetched automatically from legal open-access sources, SecVulEval came from its arXiv preprint, and tan2026think came from a publisher PDF that you supplied.
  - Pass 2: lu2025lab and qin2026review were fetched automatically. tashenova2026real and deininger2026open are open access, but the publisher blocked automated download, so you supplied the PDFs.
  - 15 published papers, plus lu2025lab, were read from their arXiv versions, not the publisher's final text (the *version of record*). Numbers could differ slightly between the two (see §7).
- **Quality control.** Four independent critical reviews checked every analysis against the paper text.
  - Pass 1 (reviews A and B): 36 findings, all fixed. Most were small: labels, wording, or relative vs absolute percentages. None changed a paper's headline result.
  - Pass 2 (reviews C and D): 9 findings for qin2026review, 16 for lu2025lab, 10 plus minor notes for tashenova2026real and 12 for deininger2026open, all fixed. Several were substantive, e.g. separating measured from estimated energy figures and limiting tashenova2026real's "SAST misses ~98%" result to the authors' own in-house analyser.
- **Gap checks.** Before any gap was claimed we ran targeted novelty searches, as our standards require (`gap-report.md`): 26 searches and 8 web searches in pass 1, and 9 more searches (Q27–Q35), 4 web searches and 2 directly read arXiv abstract pages in pass 2, all on 2026-11-12. The arXiv service timed out on 6 of the pass-2 searches (see §7).

## 3. Answers to the research questions

### RQ1 — Which family detects vulnerabilities better in head-to-head tests?

**Answer.** It depends on the setting and on which score you use:
- **Small, self-contained code.** Frontier LLMs beat SAST: macro F1 0.75–0.80 vs 0.26–0.55 on ten C# projects [@gnieciak2025large, p. 10], and a CASTLE score of 977 for GPT-o3-mini vs 661 for the best non-LLM tool [@dubniczky2025castle, p. 11].
- **Synthetic suites.** CodeQL beats the best LLM's accuracy on OWASP, Juliet Java and Juliet C/C++ [@khare2025understanding, p. 9].
- **Whole projects.** General coding agents reach much higher recall than SAST on C/C++ (59.55% vs 0–34.29%). Most LLM detectors and SAST tools produce mostly false warnings [@li2026llm, p. 7; @li2026llm, p. 11].
- **All three families on the same real functions (new in pass 2).** deininger2026open tests 8 LLMs, 3 lightweight SAST tools and fine-tuned CodeBERT detectors on the same 1549 C/C++ functions from the PrimeVul dataset.
  - Seven of the eight LLMs, asked without examples (*zero-shot*), beat the SAST tools on *balanced accuracy*, a score that averages how well a tool handles vulnerable and safe code [@deininger2026open, p. 7; @deininger2026open, p. 10].
  - A fine-tuned CodeBERT beats all eight LLMs (balanced accuracy 0.765 vs ≤ 0.711) [@deininger2026open, p. 11; @deininger2026open, p. 17].
  - When the functions are re-scored at the dataset's natural mix (about 1 vulnerable function for every 44 safe ones, "1:44"), Flawfinder and Semgrep are more precise than every LLM. LLM precision is 2.3–4.6%, barely above the 2.21% of a rule that flags everything [@deininger2026open, p. 8; @deininger2026open, p. 17].
- **Against fine-tuned DL elsewhere.** The ranking depends on the dataset, the share of vulnerable samples and the *decision threshold* (the score above which a model says "vulnerable") [@fu2023chatgpt, p. 4; @shu2026evaluating, p. 40; @deininger2026open, p. 11]. On PrimeVul pairs of vulnerable and fixed code, every family scores near or below chance [@ding2025vulnerability, p. 9; @tan2026think, p. 6].
- **Recent code (new in pass 2).** On Linux and Chromium vulnerabilities disclosed from May 2025, where 1.97% of functions are vulnerable, trained DL detectors reach F1 3.47–8.65 and four open LLMs of up to 32B parameters reach 0.79–5.36 [@lu2025lab, p. 13; @lu2025lab, p. 14]. By our calculation, a rule that flags everything would score about 3.87, so both families sit close to it [I].
- **PHP (new in pass 2).** No LLM has been tested on PHP in our corpus. The authors' own in-house analyser detects only 1.7–1.8% of vulnerabilities in WordPress plugins [@tashenova2026real, p. 9], which says nothing about established PHP SAST tools [I].

**Evidence strength: weak to moderate.** The studies are mostly single runs, use incompatible headline metrics, and cannot be pooled [I] (methodology comparison §3.5). Only one study compares all three families on identical real functions, and its SAST arm is lightweight: CodeQL could not be run on isolated functions [@deininger2026open, p. 10]. The most robust pattern [I] is that LLMs have higher recall and lower precision, and that at realistic prevalence their margin over trivial baselines is small.

**What would change it.** A study that runs all three families, including a *semantic* SAST tool such as CodeQL, on the same real code released after the models' training cutoff, with file or repository context and one shared metric (gap G2). khare2025understanding runs all three, but its SAST arm is on synthetic data only [@khare2025understanding, p. 7]; deininger2026open uses pre-2023 CVEs and single functions [@deininger2026open, p. 24]. A preprint comparing LLMs, fine-tuned small models and SAST in Python, Java and JavaScript (Zhang et al. 2025, arXiv 2503.01449; abstract only, not analysed) could extend the answer beyond C/C++ if added (§8).

### RQ2 — How do evaluation setups differ, and do they explain the disagreements?

**Answer.** Yes, to a large extent. The main sources of variation are:
- **Wrong labels.** Only 39–65% of "vulnerable" labels in popular datasets are correct [@risse2025top, p. 8], and 48.8% in a PHP benchmark [@tashenova2026real, p. 11].
- **Test data copied from training data.** Up to 18.9% exact copies [@ding2025vulnerability, p. 4]. Even when a PHP dataset was split by plugin, duplicate and contradictory-label groups still crossed the splits before cleaning [@tashenova2026real, p. 4].
- **Balanced vs realistic test sets.** The class balance flips rankings [@shu2026evaluating, p. 40; @deininger2026open, p. 8]. LLM F1 falls from about 49–65% to 5.41–12.21% when pairs are dropped [@yildiz2025benchmarking, p. 7].
- **Trivial baselines rarely reported.** Where they are reported, they are often competitive: a one-feature token-count rule matches learned models in PHP [@tashenova2026real, p. 8], and "flag everything" scores within reach of most LLMs [@deininger2026open, p. 7; @lu2025lab, p. 14].
- **Time and dataset shift.** Detectors trained on one dataset or period collapse on another [@lu2025lab, p. 12; @lu2025lab, p. 13].
- **Prompt wording and decision threshold.** Either can change the winner [@deininger2026open, p. 11; @deininger2026open, p. 20].
- **Synthetic vs real code.** LLM accuracy is 10.5% lower on real code [@khare2025understanding, p. 5].
- **Function-level vs line-level scoring.** Line-level scoring halves F1 [@ahmed2026secvuleval, p. 8].
- **Custom datasets with inconsistent splits** [@kaniewski2026systematic, p. 35].

Even a word-count classifier reaches F1 0.86 on BigVul [@risse2025top, p. 11], so high scores on that dataset say little about real understanding. The same model on the same named dataset can differ by 28 F1 points between papers [@lu2025lab, p. 12; @ding2025vulnerability, p. 7].

**Evidence strength: strong** for label noise and for the collapse of scores under realistic evaluation, which independent primary studies and two systematic reviews agree on [@kaniewski2026systematic, p. 39; @sheng2025llms, p. 20]. **Moderate** for prompt and threshold sensitivity and for trivial baselines, which rest on fewer studies.

**What would change it.** A controlled study showing that rankings stay stable across clean and noisy versions of the same benchmark, across prompts and across thresholds.

### RQ3 — Do LLM + static-analysis hybrids beat either family alone, and at what cost?

**Answer.** It depends on the type of hybrid.

- **LLM as alarm filter.** This is the most consistent benefit in the corpus, but it is a trade-off.
  - An industrial study removes 94–98% of false alarms while keeping 75–88% of real bugs, at $0.0011–$0.12 per alarm [@du2026reducing, p. 8]. This is the authors' own method at Tencent, and it covers general bug types, not only security bugs.
  - An agent study cuts the false-positive rate on OWASP from 98.3% to 6.3% [@xiong2026sifting, p. 12] but misses 22.25% of real vulnerabilities [@xiong2026sifting, p. 18].
  - **Strength: moderate.**
- **LLM inside the analyser** (IRIS, RepoAudit). The tool authors' own evaluations look strong:
  - IRIS found 55 of 120 Java CVEs vs CodeQL's 27 [@li2024iris, p. 8].
  - RepoAudit reports 78.43% precision [@guo2025repoaudit, p. 8].

  An independent project-scale study does not reproduce these gains [@li2026llm, p. 7; @li2026llm, p. 12]. IRIS's gain also depends on GPT-4, and smaller LLMs make it worse [@li2024iris, p. 10]. **Strength: weak and contested.**
- **Cost.** LLM costs range from cents per alarm to $1,247.66 for one project, while SAST takes minutes with no token cost [@li2026llm, p. 16].
  - The only *cost per true positive* (the cost of each real bug found) comes from a non-hybrid study: USD 0.003–0.212 and 3.7–119.6 kJ of energy per true positive at 1:44 prevalence [@deininger2026open, p. 8].
  - These are compute costs only. The analyst time needed to check the 25.6–41.9 false alarms that come with each real bug is not included [@deininger2026open, p. 8], and part of the energy values are estimates from operation counts (FLOP estimates), not measurements [@deininger2026open, p. 14].
  - Small open models can match a frontier model at 1/66 of the cost [@deininger2026open, p. 17]. **Strength: moderate, single study.**
- **Explainability.** LLMs sometimes point at the wrong location [@gnieciak2025large, p. 11] [A], and a fluent explanation does not mean the verdict is correct [@tan2026think, p. 9].

**What would change it.** An independent, blinded replication of IRIS or RepoAudit (gap G4). For filtering, results on real security alerts rather than the synthetic OWASP suite (gap G3).

### RQ4 — Which vulnerability types, languages and code sizes suit each family?

**Answer.**
- **By vulnerability type.** LLMs do best on self-contained injection-type weaknesses. They do worst on weaknesses that depend on wider context or on cryptography policy, and on locating memory-safety bugs [@khare2025understanding, p. 7; @xiong2026sifting, p. 18; @shu2026evaluating, p. 30]. For example, the filtering agent misses only 0.41–2.38% of injection bugs but 77.17–84.50% of weak-crypto and weak-hash bugs [@xiong2026sifting, p. 18]. CodeQL is better on integer overflow (CWE-190) [@khare2025understanding, p. 8].
- **By code size.** LLM performance drops as functions or files get longer [@ahmed2026secvuleval, p. 13; @li2026llm, p. 9].
- **By project.** One DL detector (LineVul trained on BigVul) finds 76% of the 2025 Chromium CVEs but none in Linux, while all LLMs cover Linux better [@lu2025lab, p. 13].
- **By language.** Evidence is concentrated on C/C++ and Java [@kaniewski2026systematic, p. 28]. The only PHP study tests no LLM. In it, learned models detect cross-site scripting (XSS, F1 up to 0.500) far better than SQL injection (≤ 0.146) or remote code execution (≤ 0.085) [@tashenova2026real, p. 9].

**Evidence strength: weak.** The per-type counts are small, studies disagree, and PHP rests on a single study. For example, khare finds LLMs beat CodeQL on CWE-476 [@khare2025understanding, p. 8], while ahmed reports that LLMs over-flag it [@ahmed2026secvuleval, p. 13].

**What would change it.** Larger per-type samples, and LLM-vs-established-SAST studies in PHP and Go (gap G5).

### RQ5 — What open problems remain?

**Answer.** The analysed papers repeatedly ask for:
- verified, realistic, repository-level benchmarks [@zhou2025large, p. 19; @sheng2025llms, p. 25];
- trivial baselines and realistic prevalence in every evaluation [@tashenova2026real, p. 13; @deininger2026open, p. 8];
- label quality and control of *contamination*, i.e. test code that the LLM already saw during training [@tashenova2026real, p. 12; @lu2025lab, p. 17];
- same-benchmark three-family comparisons. Two studies run all three: khare, with SAST on synthetic data only [@khare2025understanding, p. 7], and deininger, with lightweight function-level SAST on pre-2023 CVEs [@deininger2026open, p. 10; @deininger2026open, p. 24];
- independent human labelling and statistical testing, including how sensitive results are to the prompt [@li2026llm, p. 11; @deininger2026open, p. 20];
- cost reporting that includes human triage and states where energy figures come from [@deininger2026open, p. 8];
- limiting the loss of real bugs during filtering [@xiong2026sifting, p. 19];
- integration into developer workflows [@zhou2025large, p. 19].

deininger's authors judge that no method they tested (LLM, SAST or fine-tuned DL) is ready for independent function-level triage [@deininger2026open, p. 26] [A].

**Evidence strength: moderate** [I] as a description of recurring limitations. Six of these became novelty-checked gaps (§6).

## 4. Key papers to read first

1. **deininger2026open** (*Computers* 2026) is the only study that runs LLMs, SAST tools and fine-tuned DL detectors on the same real functions with the same metrics, and the only one that reports cost and energy per true positive [@deininger2026open, p. 8; @deininger2026open, p. 10]. It also uses proper significance tests [@deininger2026open, p. 6] and shows how a reworded prompt or a default threshold can change the winner [@deininger2026open, p. 11; @deininger2026open, p. 20]. Be aware of its limits: lightweight SAST without CodeQL, CVEs from 2008–2022 that the LLMs may have seen in training, and single functions without context [@deininger2026open, p. 10; @deininger2026open, p. 24].
2. **li2026llm** (TSE 2026) is the only independent, project-scale comparison of LLM detectors, agents and SAST tools that also reports cost. Read it to understand C2, C3 and C6 [@li2026llm, p. 7; @li2026llm, p. 16]. Be aware that it labels warnings partly with an LLM that it also evaluates [@li2026llm, p. 11].
3. **lu2025lab** (JSS 2026) builds a test set of Linux and Chromium vulnerabilities disclosed from May 2025, after the evaluated models were released [@lu2025lab, p. 4]. On it, a DL detector that scores F1 91.00 on its own benchmark drops to 6.87 [@lu2025lab, p. 12; @lu2025lab, p. 13], and the best open LLM reaches F1 5.36 [@lu2025lab, p. 13]. It is the clearest picture of what happens on genuinely new code. It has no SAST arm and runs each LLM once [@lu2025lab, p. 8].
4. **risse2025top** (FSE 2025) shows that common benchmark labels are often wrong and that trivial classifiers score highly. It is the backbone of the "setup explains results" argument [@risse2025top, p. 8; @risse2025top, p. 11].
5. **kaniewski2026systematic** (TOSEM 2026) is the most current systematic review (263 studies). You must position your review against it [@kaniewski2026systematic, p. 8].

If you have time for two more: **ding2025vulnerability** (ICSE 2025, PrimeVul) audits label noise and duplication and introduces the vulnerable/patched pair test that defeats every model [@ding2025vulnerability, p. 4; @ding2025vulnerability, p. 9]; **khare2025understanding** (ICST 2025) was the first study in our corpus to run LLMs, SAST and DL together, with SAST on synthetic data only [@khare2025understanding, p. 7; @khare2025understanding, p. 9].

## 5. Where studies disagree

We found eight contradictions (evidence matrix C1–C8; C7 and C8 are new in pass 2). Each can be traced, at least in part, to a difference in setup. The explanations are our interpretation [I].

- **C1. Fine-tuned models vs GPT-4.**
  - What disagrees: on Big-Vul, fine-tuned models far exceed prompted GPT-4 (F1 94% and 87% vs 29%) [@fu2023chatgpt, p. 4]. On PrimeVul pairs, GPT-4 beats every fine-tuned model (12.94% vs ≤3.01%) [@ding2025vulnerability, p. 9]. Pass 2: on single, unpaired PrimeVul functions, a fine-tuned CodeBERT again beats all eight LLMs (balanced accuracy 0.765 vs ≤ 0.711) [@deininger2026open, p. 11; @deininger2026open, p. 17].
  - Likely reason: the metric, the data split and the dataset cleaning differ. On pairs, every model is below the 22.70% random reference, so the reversal reflects the benchmark more than the model family. The threshold matters too: with the default rule, deininger's fine-tuned detector looks like an "always safe" classifier although it ranks functions well (ROC-AUC 0.845) [@deininger2026open, p. 11]. Unpaired and pair results must not be pooled.
- **C2. RepoAudit: own paper vs independent study.**
  - What disagrees: the authors report 78.43% precision and all 21 known bugs reproduced [@guo2025repoaudit, p. 8]. The independent study finds 0 of 110 known C/C++ vulnerabilities and 92.77% false warnings [@li2026llm, p. 7; @li2026llm, p. 11].
  - Likely reason: the targets, code versions, metric, labeller and scale all differ. The tool's dependence on built-in API models probably matters, because API modelling explains all 108 analysed misses [@li2026llm, p. 7]. Unresolved.
- **C3. LLM vs SAST.**
  - What disagrees: LLMs win on small programs [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11]. CodeQL wins on synthetic suites [@khare2025understanding, p. 9]. At repository level, LLMs detect more but flag up to 77.4% of functions (preprint) [@zhou2024comparison, p. 7]. Pass 2: on the same PrimeVul functions, LLMs lead on balanced accuracy, but Flawfinder and Semgrep are more precise at 1:44, while Cppcheck sits in the LLM range [@deininger2026open, p. 8; @deininger2026open, p. 10].
  - Likely reason: synthetic suites match SAST rules and small programs fit an LLM's context window. Scoring was also more lenient for LLMs in two studies [@gnieciak2025large, p. 6; @dubniczky2025castle, p. 9]. The two families also fail in opposite directions: LLMs over-flag, SAST finds little. So the ranking depends on the metric.
- **C4. Does "reasoning" reduce false alarms?**
  - What disagrees: CASTLE says reasoning models produce fewer false positives [@dubniczky2025castle, p. 14] [A], yet its own table shows DeepSeek R1 with more false positives than GPT-4o (166 vs 116) [@dubniczky2025castle, p. 11]. A controlled factorial study finds that thinking mode raises recall, not accuracy [@tan2026think, p. 6]. Pass 2: reasoning helps the frontier models but lowers DeepSeek-V3.2's *specificity* (the share of safe code correctly left alone) from 0.52 to 0.37 [@deininger2026open, p. 17; @deininger2026open, p. 20].
  - Likely reason: the effect depends on the model; the claim holds for some models in some settings only.
- **C5. Class balance flips rankings.**
  - What disagrees: fine-tuned GPT-4o wins on a balanced test set, but smaller pre-trained models win when only about 17% of samples are vulnerable [@shu2026evaluating, p. 17; @shu2026evaluating, p. 40]. Pass 2: deininger's precision ranking at 1:44 differs from its balanced-accuracy ranking [@deininger2026open, p. 8], and in the PHP study, changing how safe samples are drawn flips the direction in which the same model fails [@tashenova2026real, p. 9].
  - Likely reason: balanced sets reward models that flag a lot.
- **C6. IRIS: own paper vs independent study.**
  - What disagrees: IRIS beats CodeQL on known Java CVEs [@li2024iris, p. 8] but has 97.80% false warnings vs CodeQL's 77.00% on new Java projects [@li2026llm, p. 12].
  - Likely reason: the comparison is not like-for-like. Open.
- **C7. Same model, same benchmark, different score (new).**
  - What disagrees: a CodeBERT-based detector trained and tested on BigVul scores F1 91.00 in one paper [@lu2025lab, p. 12] and 62.88 in another [@ding2025vulnerability, p. 7]. Neither paper explains the 28-point gap.
  - Likely reason: different splits and preprocessing; lu used the detector's original pipeline [@lu2025lab, p. 8]. In-distribution BigVul numbers cannot be compared across papers.
- **C8. Does a fine-tuned detector survive on later code? (new)**
  - What disagrees: a CodeBERT trained on PrimeVul keeps balanced accuracy 0.765 on PrimeVul's chronologically later test split [@deininger2026open, p. 11], while DL detectors trained on BigVul, ICVul, Devign or Juliet fall to F1 3.47–8.65 on 2025 CVEs [@lu2025lab, p. 13].
  - Likely reason: the test data (2008–2022 PrimeVul CVEs vs 2025 CVEs), training data quality, threshold policy and metric all differ. Unresolved.

Where results do agree, the agreement is useful. CodeQL's results on OWASP replicate across two groups within about 2 points [@khare2025understanding, p. 9; @xiong2026sifting, p. 11]. Realistic evaluation lowers every family's scores [@chakraborty2024revisiting, p. 7; @ding2025vulnerability, p. 7; @lu2025lab, p. 13]. And where trivial baselines are reported, they are competitive [@tashenova2026real, p. 8; @deininger2026open, p. 7; @shu2026evaluating, p. 11].

## 6. Research gaps and possible contributions

All gaps passed a recorded novelty check on 2026-11-12 and were re-checked in pass 2. "No study found" means we found none in those searches, not that none exists. Gaps are ranked by evidence strength and by how feasible they are for a beginner; **the top three for you are G1, G2 and G3**.

| Gap | After pass 2 | Confidence | Suggested study | Beginner feasibility |
|---|---|---|---|---|
| **G1.** Published LLM, SAST and DL results are not re-scored *across studies* against trivial baselines ("flag everything") or realistic prevalence; no shared evaluation protocol exists | unchanged (premise strengthened) | medium–high | Re-compute MCC, ΔF1 vs flag-all, and precision at 1%, 5% and 17% prevalence from the published tables of the 20 primary studies; check the formulas against the studies that report their own baselines | **easy** (spreadsheet or ~50 lines of Python, 2–4 weeks, no compute) |
| **G2.** No same-benchmark LLM vs *semantic* SAST vs fine-tuned DL comparison on real code released after the models' training cutoff (*post-cutoff* code), with file or repository context | narrowed: a function-level, pre-cutoff C/C++ three-family study now exists (deininger2026open) | medium | ~100 post-cutoff + ~100 pre-cutoff Python or Java CVEs; Semgrep and CodeQL, a fine-tuned UniXcoder or CodeBERT, 2–3 open LLMs, plus flag-all. Cheaper variant: reuse the public 2025-CVE set from lu2025lab [@lu2025lab, p. 2] and add a SAST arm, an LLM arm with file context and a flag-all baseline | moderate (6–10 weeks) |
| **G3.** Loss of real bugs in LLM alarm filtering is not controlled per vulnerability type on real security alerts | unchanged | low–medium | Filter only the CWE types with low miss rates; tune on half of OWASP, test on the other half and on ~100 real alerts | easy–moderate (4–6 weeks) |
| **G4.** No independent, blinded replication of IRIS / RepoAudit that separates target, metric and labeller effects | unchanged | medium | 2 × 2 design: original vs new targets × original vs false-discovery metric, labelled by humans blinded to the tool | moderate–hard (an IRIS-only version on 20–30 CVEs: about 8 weeks) |
| **G5.** No real-CVE comparison of LLMs with *established* SAST tools for PHP and Go | narrowed: LLM-only WordPress evidence (Neef et al. 2026) and function-level Python/Java/JavaScript three-family evidence (Zhang et al. 2025) exist, both abstract only | low–medium | Reuse tashenova2026real's expert-verified PHP subset (125 vulnerable, 247 safe functions) [@tashenova2026real, p. 11] or ~60 Go CVEs; Semgrep plus a PHP or Go taint tool, 2 open LLMs, token-count and flag-all baselines | moderate |
| **G6.** No cost per *confirmed* vulnerability that includes analyst triage time and a costed SAST and DL arm on the same targets | narrowed: compute cost per true positive for 8 LLMs now exists (deininger2026open) | low–medium | Add to G2 as a secondary outcome: time two raters triaging 50 warnings per tool | moderate (piggybacks on G2) |

**Why G1 matters and why it is the easiest contribution.** On a 50/50 test set, flagging everything already gives F1 0.667. Several published best results sit at or just above that line: a dummy classifier at 0.6693 vs a best model at 0.7075 [@shu2026evaluating, p. 17], best F1 values of 0.665–0.666 [@tan2026think, p. 7] and GPT F1 values of 48–66 [@yildiz2025benchmarking, p. 6]. Pass 2 shows the same at other prevalences:
- LLM F1 0.405–0.615 against 0.523 for "always vulnerable", and at 1:44 LLM precision only just above flag-all [@deininger2026open, p. 7; @deininger2026open, p. 8];
- a one-feature token-count rule matching learned PHP detectors [@tashenova2026real, p. 8];
- 7 of 12 LLM F1 values on 2025 CVEs below the flag-all level, by our calculation [I] [@lu2025lab, p. 14].

These studies apply baselines only to their own results; none re-scores other studies' published numbers on a common scale [I]. Statistics are also rare: among the first 16 primary studies only tan2026think applies significance tests to its main comparison [@tan2026think, p. 6] [I, our count]; of the four pass-2 papers, deininger2026open does [@deininger2026open, p. 6]. G1 needs only published tables and a spreadsheet, and the studies that report their own baselines give you a built-in check that your formulas are right. Credit those within-study baselines; the contribution is the *systematic cross-study* re-scoring.

**Positioning of the review** (medium confidence). We found no review that combines (a) a synthesis across LLM, SAST and DL plus both hybrid types with (b) a setup-based explanation of specific contradictions. Reviews in the corpus are either LLM-only [@kaniewski2026systematic, p. 8], predate most hybrid and project-scale work [@zhou2025large, p. 18], or are narrative [@sheng2025llms, p. 25]. The closest competitor, qin2026review, has now been read in full. It shares our "evaluation reliability" framing [@qin2026review, p. 10] [A], but it reports no search protocol, puts SAST explicitly out of scope [@qin2026review, p. 4], and its numbers re-report papers already in our corpus [@qin2026review, p. 12; @qin2026review, p. 15], so it is not independent evidence [I]. It strengthens rather than weakens our novelty claim, but reviewers will likely point to it and to kaniewski2026systematic, so the claim must stay narrow. Several other reviews outside the corpus were checked from their abstracts only (`gap-report.md`).

## 7. Limitations of this review

- **Size.** 24 papers (20 primary studies, 4 reviews). This is a focused critical review, not a complete systematic review. Several relevant papers were found during gap checks but not analysed, including a second three-family comparison (Zhang et al. 2025) that the pass-1 searches returned but we missed (§8).
- **Speed of the field.** Searches ran on 2026-11-12. Many near-miss studies appeared in 2026; pass 2 already narrowed G2, G5 and G6, and G3 could close soon too.
- **Search coverage.** The arXiv service timed out on 6 of the 9 pass-2 novelty searches (Q27–Q29 and Q31–Q33). We covered arXiv instead with one further arXiv search (Q34) and by reading the abstract pages of the two papers flagged for checking. Some recent arXiv preprints may still have been missed.
- **Corrections made in pass 2.** Some pass-1 gap notes were based on abstracts and turned out wrong once the full texts were read: deininger2026open *does* run SAST tools (the pass-1 notes said it did not), tashenova2026real is now read in full rather than known from its abstract, and lu2025lab turned out to be published in a journal. The gap report and this report now follow the full texts. [I] Abstract-based judgements about the papers still outside the corpus (§8) could be wrong in the same way.
- **Energy and cost figures.** Part of deininger2026open's energy per true positive comes from estimates based on counted operations (FLOP estimates), not from measured energy [@deininger2026open, p. 14], and that estimator overstates measured batched energy by 5.4–16.9× [@deininger2026open, p. 14]. Its cost figures also leave out human triage [@deininger2026open, p. 8]. Treat these numbers as rough orders of magnitude.
- **Preprints and versions.**
  - zhou2024comparison is not peer-reviewed. Its per-language results rest on about 8–10 test CVEs [@zhou2024comparison, p. 6] [I].
  - Fifteen published papers, plus lu2025lab (arXiv v4 accepted manuscript), were read from arXiv copies. du2026reducing came from an early version with a placeholder header [@du2026reducing, p. 2], so it carries the highest risk that its numbers changed.
  - qin2026review's venue does not document peer review [@qin2026review, p. 1]; we use it for positioning only.
  - One paper's identity (ahmed2026secvuleval) is marked "unverified" by `rlab` because its title differs from the arXiv version. A reviewer confirmed it manually by its authors.
- **Independence.**
  - Four studies share the PrimeVul dataset family (ding, yildiz, tan, deininger) [I].
  - One of lu2025lab's four training datasets (ICVul) is the authors' own [@lu2025lab, p. 3].
  - qin2026review re-reports papers already in our corpus, so it adds no independent support [@qin2026review, p. 12].
  - zhou2025large's only LLM-vs-SAST study is its own authors' preprint [@zhou2025large, p. 22].
  - The independent project-scale study uses an LLM as labeller [@li2026llm, p. 11].
- **Single runs and prompts.** Most primary studies run each model once. deininger2026open shows that rewording the prompt can move balanced accuracy by up to 0.088 and change the winner [@deininger2026open, p. 19; @deininger2026open, p. 20], so small differences elsewhere should not be over-read [I].
- **No pooling.** Metrics are too varied for a meta-analysis (a statistical combination of results), so our answers are narrative.
- **Language bias.** The evidence comes mostly from C/C++ and Java [@kaniewski2026systematic, p. 28]; PHP rests on one study with no LLM arm [@tashenova2026real, p. 13].
- **Abstract-only material.** Statements about papers outside the corpus (§6, §8) are based on abstracts only.
- **Record keeping.** The `metadata.json` files of three pass-2 papers carry a wrong, shared reason for inclusion; the correct reasons are in `search/screening.md`. This does not affect any finding.

## 8. Recommended next steps

**(a) Turn this into the comparative review paper.**
1. Frame it as a **critical comparative review**, not a systematic review. With 24 papers, reviewers would criticise a "comprehensive" framing. State two distinct contributions:
   - a synthesis across all three families and both hybrid types;
   - an explanation of each contradiction (C1–C8) through the study setup, together with a comparability audit that says which numbers may be compared across papers (methodology comparison §3).
2. Suggested structure:
   - introduction and positioning against kaniewski2026systematic, zhou2025large, sheng2025llms and qin2026review;
   - method (searches, screening, appraisal);
   - results by family (methodology comparison §2);
   - comparable results (§3);
   - contradictions (§4);
   - field-wide weaknesses (§5);
   - gaps and guidance;
   - threats to validity (this report §7).
3. Include **G1 as a table inside the review**. Re-scoring the published numbers against flag-all baselines and realistic prevalence needs only the published tables and a spreadsheet, so it adds a concrete result at no compute cost. Extract twice and spot-check against the PDFs. Rows without enough data to rebuild a confusion matrix go in a separate list.
4. Cite deininger2026open as the current best same-function evidence, but state its limits (lightweight SAST, pre-2023 CVEs, single functions), and cite qin2026review only for positioning.

**(b) Decide whether to run a pass 3 (your decision).** The pass-2 gap check recommends adding further papers, which would raise the corpus to about 26. They would be added with `rlab add`, fetched, analysed and critically reviewed like the others. In order of value:
- **Zhang et al. 2025**, *Benchmarking Large Language Models for Multi-Language Software Vulnerability Detection* (arXiv 2503.01449; preprint, check for a published version). High priority: from its abstract, it is a second same-benchmark comparison of LLMs, fine-tuned small models and SAST, and the only one in Python, Java and JavaScript. It bears on RQ1, G2 and G5.
- **Neef et al. 2026**, *Evaluating LLMs for Real-World Web Vulnerability Detection* (arXiv 2606.21397; AI&CCPS Workshop at ARES 2026). It tests six LLMs on real WordPress-plugin vulnerabilities and is the closest work to G5. Its full text must show whether it includes any tool baseline and at what level (function, file or plugin) it works.
- Optional: the SoK *LLMs in Security Code Review and Testing* (doi:10.5070/sr3.62177) as a second positioning competitor, and an *Information and Software Technology* 2026 paper (doi:10.1016/j.infsof.2026.108213) whose title suggests an LLM-vs-traditional comparison but whose abstract we could not retrieve, so screen it first.

If you decline, the report stands as is, but §6 must keep describing G2 and G5 as "narrowed, pending these papers".

**(c) Before submission.**
- Re-check every key number against the version of record, starting with du2026reducing, the other 14 papers read from arXiv, and lu2025lab's JSS version.
- Re-run the novelty searches for G1, G2 and the positioning claim, including the 6 searches where arXiv timed out.

**A first concrete step this week:** start the G1 extraction sheet with the three studies that report their own trivial baselines (shu, deininger, tashenova), because they let you check your formulas. Then add the studies whose best results sit near the flag-all line (tan, yildiz, khare, lu), then the remaining primary studies.

**Also pending:** the plain-English reading guide (Google Doc) you approved, updated for all 24 papers.

## 9. Glossary

- **Vulnerability:** a security bug that an attacker could exploit.
- **CVE:** a public ID for one known, real-world vulnerability.
- **CWE:** a category of vulnerability type, e.g. CWE-89 for SQL injection.
- **XSS (cross-site scripting):** a web vulnerability where an attacker gets their script to run in other users' browsers.
- **SAST (static application security testing):** tools such as CodeQL or Semgrep that scan code with hand-written rules without running it.
- **Lightweight vs semantic SAST:** lightweight tools (e.g. Flawfinder, Cppcheck) match patterns in the text of the code; semantic tools (e.g. CodeQL) build a model of the whole program and track how data flows through it, which usually requires building the project.
- **Taint analysis:** a SAST technique that follows untrusted input ("tainted" data) to see whether it reaches a dangerous operation.
- **DL detector:** a neural network (e.g. LineVul) trained on examples of vulnerable and safe code.
- **LLM (large language model):** a very large text model such as GPT-4 that can read and reason about code.
- **Prompting / zero-shot / few-shot:** asking an LLM directly, with no examples (zero-shot) or a few examples (few-shot) in the request.
- **Fine-tuning:** further training a model on task-specific labelled data.
- **Agent:** an LLM that can call tools and take several steps, e.g. open other files.
- **Hybrid:** a system that combines an LLM with a SAST tool.
- **Precision:** the share of the tool's warnings that are real vulnerabilities.
- **Recall:** the share of real vulnerabilities that the tool finds.
- **F1:** a single score that balances precision and recall. *Macro F1* averages the F1 of the "vulnerable" and "safe" classes.
- **False-positive rate (FPR):** the share of safe code wrongly flagged as vulnerable.
- **Specificity:** the share of safe code that the tool correctly leaves alone (1 − FPR).
- **Balanced accuracy:** the average of recall and specificity, so a tool cannot score well just by always giving the majority answer.
- **ROC-AUC:** how well a model ranks vulnerable code above safe code across all possible thresholds; 0.5 is chance, 1.0 is perfect.
- **Decision threshold:** the score above which a model's output is counted as "vulnerable"; changing it trades recall against precision.
- **Cost per true positive:** the money or energy spent for each real vulnerability a tool finds.
- **FLOP estimate:** an energy figure calculated from the number of computing operations a model needs, rather than measured on the hardware.
- **SFDR (sampled false discovery rate):** the share of warnings that are false, estimated from a sample.
- **MCC:** a score that stays fair when vulnerable code is rare.
- **Prevalence / class balance:** the share of vulnerable samples in a test set. *Balanced* means 50%.
- **Trivial baseline:** a deliberately dumb method, e.g. "flag everything", that any real tool should beat.
- **Pairwise correctness:** the share of vulnerable/fixed code pairs where both versions are judged correctly.
- **Label noise:** wrong "vulnerable"/"safe" labels in a dataset.
- **Data leakage:** test samples that also appear in the training data, which inflates scores.
- **Contamination / training cutoff:** an LLM may have seen benchmark code during training. Code released after its training cutoff (*post-cutoff* code) avoids this.
- **Temporally separated / out-of-distribution test:** testing on data from a later period or a different source than the training data, which is closer to real use.
- **Synthetic vs real-world code:** code written to demonstrate a bug (e.g. the Juliet, OWASP and CASTLE suites) vs code from real projects.
- **Repository level:** analysing a whole project rather than single functions.
- **Benchmark:** a shared test dataset used to compare tools.
- **Systematic literature review (SLR):** a review that searches for and assesses all studies on a question using a fixed protocol.
- **Narrative review:** a review that summarises a field without a fixed search and selection protocol; it is easier to write but less reliable.
- **Critical comparative review:** a focused review that compares approaches across a chosen set of studies and appraises them critically, without claiming to cover everything.
- **Grey literature:** material outside the normal peer-reviewed channels, e.g. reports or papers in venues that do not document peer review.
- **Meta-analysis:** statistically combining the results of many studies.
- **Peer review / preprint:** expert checking before publication. A preprint has not been through it yet.
- **Version of record:** the final published version of a paper.
- **Novelty check:** targeted searches to confirm that a gap has not already been filled.
- **Significance test:** a statistical test of whether a difference could be due to chance.
