# Research report: LLM-based vs traditional static analysis and deep learning for source-code vulnerability detection

- Project: `2026-11-12-llm-based-vs-traditional-static-analysis`
- Date: 2026-11-12
- Based on: 20 full-text analyses, `evidence-matrix.md`, `reports/methodology-comparison.md`, `gap-report.md`, two critical reviews (A and B, 2026-11-12), `search/screening.md`, `search/search-log.md`.
- How to read the labels: **[V]** means we checked the number in the paper's own tables or results, **[A]** means the authors say it but we cannot check it, and **[I]** is our own interpretation. Unlabelled numbers are [V] from the cited page. Citations give the paper's folder name and the PDF page, e.g. `[@risse2025top, p. 8]`.

## 1. Summary in plain language

We asked whether large language models (LLMs, such as GPT-4 or Claude) find security bugs in source code better than the two older approaches: rule-based scanners (SAST tools such as CodeQL) and neural networks trained on labelled vulnerable code (deep-learning or "DL" detectors). The short answer is that **no approach wins everywhere**. LLMs come out ahead on small, self-contained programs [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11]. CodeQL comes out ahead on synthetic test suites [@khare2025understanding, p. 9]. On large real projects both families miss many bugs and raise many false alarms [@li2026llm, p. 7; @li2026llm, p. 11]. The most consistent pattern [I] is that LLMs find more of the real bugs (higher recall) but also flag much more harmless code (lower precision). A large part of the disagreement between papers comes from **how** they test, not from the tools themselves. Studies differ in label quality, overlap between training and test data, the share of vulnerable samples, and how lenient the scoring is [@risse2025top, p. 8; @ding2025vulnerability, p. 4; @shu2026evaluating, p. 40; @gnieciak2025large, p. 6]. Combining the two, by letting an LLM filter a scanner's alarms, removes most false alarms cheaply but also throws away 12–25% of real bugs [@du2026reducing, p. 8; @xiong2026sifting, p. 18]. For your comparative review, this "setup explains the contradictions" angle, applied across all three families, is the contribution we could not find in existing reviews (medium confidence).

## 2. What we did

- **Scope.** Source-code vulnerability detection by LLMs, SAST tools, DL detectors and LLM+SAST hybrids, published 2020–2026. Binary analysis, fuzzing and repair-only work were excluded (`RESEARCH.md`).
- **Searches.** Three search agents covered six facets: head-to-head LLM vs SAST, LLM vs DL, hybrids, evaluation realism, reasoning/agentic LLMs, and surveys. They ran about 19 searches on OpenAlex, Crossref and arXiv, plus *snowballing*, which means following the references and citations of central papers. Every search is logged in `search/search-log.md`, and every screening decision with its reason is in `search/screening.md`.
- **Included papers.** 20 papers in total:
  - 17 are published papers with a DOI.
  - IRIS [@li2024iris, p. 1] and RepoAudit [@guo2025repoaudit, p. 1] appeared at ICLR 2025 and ICML 2025. Both are peer-reviewed, but `rlab` records them as arXiv preprints because those venues issue no DOIs.
  - Only zhou2024comparison is a true preprint, meaning it is **not peer-reviewed** [@zhou2024comparison, p. 1].
  - Three of the 20 are reviews: kaniewski2026systematic, zhou2025large and sheng2025llms.
  - One candidate (VulnLLM-R) was dropped to keep to the 20-paper target, because it is a preprint with no venue.
- **Full text.** 20 of 20 papers were read in full and none were abstract-only (`rlab status`).
  - 18 PDFs were fetched automatically from legal open-access sources.
  - SecVulEval came from its arXiv preprint.
  - tan2026think came from a publisher PDF that you supplied.
  - 15 published papers were read from their arXiv versions, not the publisher's final text (the *version of record*). Numbers could differ slightly between the two (see §7).
- **Quality control.** Two independent critical reviews checked every analysis against the paper text and raised 36 findings, all of which were fixed. Most were small: labels, wording, or relative vs absolute percentages. None changed a paper's headline result.
- **Gap checks.** Before any gap was claimed we ran 26 targeted searches and 8 web searches (2026-11-12), as our standards require (`gap-report.md`).

## 3. Answers to the research questions

### RQ1 — Which family detects vulnerabilities better in head-to-head tests?

**Answer.** It depends on the setting:
- **Small, self-contained code.** Frontier LLMs beat SAST: macro F1 0.75–0.80 vs 0.26–0.55 on ten C# projects [@gnieciak2025large, p. 10], and a CASTLE score of 977 for GPT-o3-mini vs 661 for the best non-LLM tool [@dubniczky2025castle, p. 11].
- **Synthetic suites.** CodeQL beats the best LLM's accuracy on OWASP, Juliet Java and Juliet C/C++ [@khare2025understanding, p. 9].
- **Whole projects.** General coding agents reach much higher recall than SAST on C/C++ (59.55% vs 0–34.29%). Most LLM detectors and SAST tools produce mostly false warnings [@li2026llm, p. 7; @li2026llm, p. 11].
- **Against fine-tuned DL.** The ranking depends on the dataset and on the share of vulnerable samples [@fu2023chatgpt, p. 4; @shu2026evaluating, p. 40]. On PrimeVul pairs of vulnerable and fixed code, every family scores near or below chance [@ding2025vulnerability, p. 9; @tan2026think, p. 6].

**Evidence strength: weak to moderate.** The studies are mostly single runs, use five incompatible headline metrics, and cannot be pooled [I] (methodology comparison §3.5).

**What would change it.** A study that runs all three families on the same real, recent code with one shared metric (gap G2). Only khare2025understanding runs all three, and its SAST arm is on synthetic data only [@khare2025understanding, p. 7].

### RQ2 — How do evaluation setups differ, and do they explain the disagreements?

**Answer.** Yes, to a large extent. The main sources of variation are:
- **Wrong labels.** Only 39–65% of "vulnerable" labels in popular datasets are correct [@risse2025top, p. 8].
- **Test data copied from training data.** Up to 18.9% exact copies [@ding2025vulnerability, p. 4].
- **Balanced vs realistic test sets.** The class balance flips rankings [@shu2026evaluating, p. 40]. LLM F1 falls from about 49–65% to 5.41–12.21% when pairs are dropped [@yildiz2025benchmarking, p. 7].
- **Synthetic vs real code.** LLM accuracy is 10.5% lower on real code [@khare2025understanding, p. 5].
- **Function-level vs line-level scoring.** Line-level scoring halves F1 [@ahmed2026secvuleval, p. 8].
- **Custom datasets with inconsistent splits** [@kaniewski2026systematic, p. 35].

Even a word-count classifier reaches F1 0.86 on BigVul [@risse2025top, p. 11], so high scores on that dataset say little about real understanding.

**Evidence strength: moderate to strong.** Independent primary studies agree, and two systematic reviews concur [@kaniewski2026systematic, p. 39; @sheng2025llms, p. 20].

**What would change it.** A controlled study showing that rankings stay stable across clean and noisy versions of the same benchmark.

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
- **Explainability.** LLMs sometimes point at the wrong location [@gnieciak2025large, p. 11] [A], and a fluent explanation does not mean the verdict is correct [@tan2026think, p. 9].

**What would change it.** An independent, blinded replication of IRIS or RepoAudit (gap G4). For filtering, results on real security alerts rather than the synthetic OWASP suite (gap G3).

### RQ4 — Which vulnerability types, languages and code sizes suit each family?

**Answer.**
- **By vulnerability type.** LLMs do best on self-contained injection-type weaknesses. They do worst on weaknesses that depend on wider context or on cryptography policy, and on locating memory-safety bugs [@khare2025understanding, p. 7; @xiong2026sifting, p. 18; @shu2026evaluating, p. 30]. For example, the filtering agent misses only 0.41–2.38% of injection bugs but 77.17–84.50% of weak-crypto and weak-hash bugs [@xiong2026sifting, p. 18]. CodeQL is better on integer overflow (CWE-190) [@khare2025understanding, p. 8].
- **By code size.** LLM performance drops as functions or files get longer [@ahmed2026secvuleval, p. 13; @li2026llm, p. 9].
- **By language.** Evidence is concentrated on C/C++ and Java [@kaniewski2026systematic, p. 28].

**Evidence strength: weak.** The per-type counts are small and studies disagree. For example, khare finds LLMs beat CodeQL on CWE-476 [@khare2025understanding, p. 8], while ahmed reports that LLMs over-flag it [@ahmed2026secvuleval, p. 13].

**What would change it.** Larger per-type samples, and studies in PHP, Go and JavaScript (gap G5).

### RQ5 — What open problems remain?

**Answer.** The analysed papers repeatedly ask for:
- verified, realistic, repository-level benchmarks [@zhou2025large, p. 19; @sheng2025llms, p. 25];
- same-benchmark three-family comparisons;
- independent human labelling and statistical testing [@li2026llm, p. 11];
- cost reporting;
- control of *contamination*, i.e. test code that the LLM already saw during training;
- limiting the loss of real bugs during filtering [@xiong2026sifting, p. 19];
- integration into developer workflows [@zhou2025large, p. 19].

**Evidence strength: moderate** as a description of recurring limitations. Six of these became novelty-checked gaps (§6).

## 4. Key papers to read first

1. **li2026llm** (TSE 2026) is the only independent, project-scale comparison of LLM detectors, agents and SAST tools that also reports cost. Read it to understand C2, C3 and C6 [@li2026llm, p. 7; @li2026llm, p. 16]. Be aware that it labels warnings partly with an LLM that it also evaluates [@li2026llm, p. 11].
2. **risse2025top** (FSE 2025) shows that common benchmark labels are often wrong and that trivial classifiers score highly. It is the backbone of the "setup explains results" argument [@risse2025top, p. 8; @risse2025top, p. 11].
3. **ding2025vulnerability** (ICSE 2025, PrimeVul) audits label noise and duplication and introduces the vulnerable/patched pair test that defeats every model [@ding2025vulnerability, p. 4; @ding2025vulnerability, p. 9].
4. **khare2025understanding** (ICST 2025) is the only study that runs LLMs, SAST and DL together, so it is the nearest thing to a three-way comparison [@khare2025understanding, p. 7; @khare2025understanding, p. 9].
5. **kaniewski2026systematic** (TOSEM 2026) is the most current systematic review (263 studies). You must position your review against it [@kaniewski2026systematic, p. 8].

## 5. Where studies disagree

We found six contradictions (evidence matrix C1–C6). Each can be traced to a difference in setup. The explanations are our interpretation [I].

- **C1. Fine-tuned models vs GPT-4.**
  - What disagrees: on Big-Vul, fine-tuned models far exceed prompted GPT-4 (F1 94% and 87% vs 29%) [@fu2023chatgpt, p. 4]. On PrimeVul pairs, GPT-4 beats every fine-tuned model (12.94% vs ≤3.01%) [@ding2025vulnerability, p. 9].
  - Likely reason: the metric, the data split and the dataset cleaning differ. On pairs, every model is below the 22.70% random reference, so the reversal reflects the benchmark more than the model family.
- **C2. RepoAudit: own paper vs independent study.**
  - What disagrees: the authors report 78.43% precision and all 21 known bugs reproduced [@guo2025repoaudit, p. 8]. The independent study finds 0 of 110 known C/C++ vulnerabilities and 92.77% false warnings [@li2026llm, p. 7; @li2026llm, p. 11].
  - Likely reason: the targets, code versions, metric, labeller and scale all differ. The tool's dependence on built-in API models probably matters, because API modelling explains all 108 analysed misses [@li2026llm, p. 7]. Unresolved.
- **C3. LLM vs SAST.**
  - What disagrees: LLMs win on small programs [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11]. CodeQL wins on synthetic suites [@khare2025understanding, p. 9]. At repository level, LLMs detect more but flag up to 77.4% of functions (preprint) [@zhou2024comparison, p. 7].
  - Likely reason: synthetic suites match SAST rules and small programs fit an LLM's context window. Scoring was also more lenient for LLMs in two studies [@gnieciak2025large, p. 6; @dubniczky2025castle, p. 9].
- **C4. Does "reasoning" reduce false alarms?**
  - What disagrees: CASTLE says reasoning models produce fewer false positives [@dubniczky2025castle, p. 14] [A], yet its own table shows DeepSeek R1 with more false positives than GPT-4o (166 vs 116) [@dubniczky2025castle, p. 11]. A controlled factorial study finds that thinking mode raises recall, not accuracy [@tan2026think, p. 6].
  - Likely reason: the claim holds for some proprietary models in some settings only.
- **C5. Class balance flips rankings.**
  - What disagrees: fine-tuned GPT-4o wins on a balanced test set, but smaller pre-trained models win when only about 17% of samples are vulnerable [@shu2026evaluating, p. 17; @shu2026evaluating, p. 40].
  - Likely reason: balanced sets reward models that flag a lot.
- **C6. IRIS: own paper vs independent study.**
  - What disagrees: IRIS beats CodeQL on known Java CVEs [@li2024iris, p. 8] but has 97.80% false warnings vs CodeQL's 77.00% on new Java projects [@li2026llm, p. 12].
  - Likely reason: the comparison is not like-for-like. Open.

Where results do agree, the agreement is useful. CodeQL's results on OWASP replicate across two groups within about 2 points [@khare2025understanding, p. 9; @xiong2026sifting, p. 11]. Realistic evaluation lowers every family's scores [@chakraborty2024revisiting, p. 7; @ding2025vulnerability, p. 7].

## 6. Research gaps and possible contributions

All gaps passed a recorded novelty check on 2026-11-12. "No study found" means we found none in those searches, not that none exists.

| Gap | Confidence | Suggested study | Beginner feasibility |
|---|---|---|---|
| **G1.** Published results are never re-scored against trivial baselines ("flag everything") or realistic prevalence | medium–high | Re-compute MCC, ΔF1 vs flag-all, and precision at 1–17% prevalence from the published tables of the 16 primary studies | **easy** (spreadsheet, 2–4 weeks, no compute) |
| **G2.** No same-benchmark LLM vs SAST vs DL comparison on real code released after the models' training cutoff (*post-cutoff* code) | medium | ~100 post-cutoff + ~100 pre-cutoff Python or Java CVEs; Semgrep/CodeQL, a fine-tuned UniXcoder, 2–3 open LLMs | moderate (6–10 weeks) |
| **G3.** Loss of real bugs in LLM alarm filtering is not controlled per vulnerability type on real alerts | low–medium | Filter only the CWE types with low miss rates; tune on half of OWASP, test on the other half and on ~100 real alerts | easy–moderate (4–6 weeks) |
| **G4.** No independent, blinded replication of IRIS / RepoAudit | medium | 2 × 2 design: original vs new targets × original vs false-discovery metric, labelled by humans blinded to the tool | moderate–hard |
| **G5.** No repository-level, real-CVE LLM vs SAST evidence for PHP and Go | low–medium | ~60 real PHP or Go CVEs; Semgrep + 2 open LLMs | moderate |
| **G6.** No cost per confirmed vulnerability (compute + analyst triage time) across all three families | low–medium | Add to G2 as a secondary outcome | moderate |

Why G1 matters: on a 50/50 test set, flagging everything already gives F1 0.667. Several published best results sit at or just above that line. One example is a dummy classifier at 0.6693 vs a best model at 0.7075 [@shu2026evaluating, p. 17]. Others are best F1 values of 0.665–0.666 [@tan2026think, p. 7] and GPT F1 values of 48–66 [@yildiz2025benchmarking, p. 6]. Only one primary study applies significance tests to its main comparison [@tan2026think, p. 6] [I, our count].

**Positioning of the review** (medium confidence). We found no review that combines (a) a synthesis across LLM, SAST and DL plus both hybrid types with (b) a setup-based explanation of specific contradictions. Reviews in the corpus are either LLM-only [@kaniewski2026systematic, p. 8], predate most hybrid and project-scale work [@zhou2025large, p. 18], or are narrative [@sheng2025llms, p. 25]. The closest competitor outside the corpus is a 2026 review in *Computers and Artificial Intelligence* (doi:10.70267/cai.v3n5.122137). We read only its abstract, which already raises the duplicates, label noise and leakage point, so the novelty claim must stay narrow.

## 7. Limitations of this review

- **Size.** 20 papers, chosen to keep the first pass manageable. This is a focused critical review, not a complete systematic review. Several relevant 2026 papers were found during gap checks but not analysed (§8).
- **Speed of the field.** Searches ran on 2026-11-12. Many near-miss studies appeared in 2026, so gaps G2, G3 and G5 could close soon.
- **Preprints and versions.**
  - zhou2024comparison is not peer-reviewed. Its per-language results rest on about 8–10 test CVEs [@zhou2024comparison, p. 6] [I].
  - Fifteen published papers were read from arXiv copies. du2026reducing came from an early version with a placeholder header [@du2026reducing, p. 2], so it carries the highest risk that its numbers changed.
  - One paper's identity (ahmed2026secvuleval) is marked "unverified" by `rlab` because its title differs from the arXiv version. A reviewer confirmed it manually by its authors.
- **Independence.**
  - Three studies share the PrimeVul dataset family [I].
  - zhou2025large's only LLM-vs-SAST study is its own authors' preprint [@zhou2025large, p. 22].
  - The independent project-scale study uses an LLM as labeller [@li2026llm, p. 11].
- **No pooling.** Metrics are too varied for a meta-analysis (a statistical combination of results), so our answers are narrative.
- **Language bias.** The evidence comes mostly from C/C++ and Java [@kaniewski2026systematic, p. 28].
- **Abstract-only material.** Statements about papers outside the corpus (§6, §8) are based on abstracts only.

## 8. Recommended next steps

**(a) Turn this into the comparative review paper.**
1. Frame it as a **critical comparative review**, not a systematic review. With 20 papers, reviewers would criticise a "comprehensive" framing. State two distinct contributions:
   - a synthesis across all three families and both hybrid types;
   - an explanation of each contradiction (C1–C6) through the study setup, together with a comparability audit that says which numbers may be compared across papers (methodology comparison §3).
2. Suggested structure:
   - introduction and positioning against kaniewski2026systematic, zhou2025large, sheng2025llms and the CAI 2026 review;
   - method (searches, screening, appraisal);
   - results by family (methodology comparison §2);
   - comparable results (§3);
   - contradictions (§4);
   - field-wide weaknesses (§5);
   - gaps and guidance;
   - threats to validity (this report §7).
3. Include **G1 as a table inside the review**. Re-scoring the published numbers against flag-all baselines and realistic prevalence needs only the published tables and a spreadsheet, so it adds a concrete result at no compute cost. Extract twice and spot-check against the PDFs. Rows without enough data to rebuild a confusion matrix go in a separate list.

**(b) Decide on adding recommended papers.** This is your decision, because it raises the corpus above the 20-paper target. The **CAI 2026 review (doi:10.70267/cai.v3n5.122137) must be read and cited in any case**, since it is the closest competitor. Also recommended:
- *From Lab to Reality* (arXiv 2512.10485, accepted at JSS);
- the WordPress PHP benchmark (doi:10.3390/bdcc10090303);
- *Open or Frontier?* (doi:10.3390/computers15090623).

If you agree, they would be added with `rlab add`, fetched, and analysed like the others.

**(c) Before submission.**
- Re-check every key number against the version of record, starting with du2026reducing and the other 14 papers read from arXiv.
- Re-run the novelty searches for G1, G2 and the positioning claim.

**A first concrete step this week:** start the G1 extraction sheet with the four studies whose best balanced-data F1 sits near the flag-all line (shu, tan, yildiz, khare), then add the remaining primary studies.

## 9. Glossary

- **Vulnerability:** a security bug that an attacker could exploit.
- **CVE:** a public ID for one known, real-world vulnerability.
- **CWE:** a category of vulnerability type, e.g. CWE-89 for SQL injection.
- **SAST (static application security testing):** tools such as CodeQL or Semgrep that scan code with hand-written rules without running it.
- **DL detector:** a neural network (e.g. LineVul) trained on examples of vulnerable and safe code.
- **LLM (large language model):** a very large text model such as GPT-4 that can read and reason about code.
- **Prompting / zero-shot / few-shot:** asking an LLM directly, with no examples (zero-shot) or a few examples (few-shot) in the request.
- **Fine-tuning:** further training a model on task-specific labelled data.
- **Agent:** an LLM that can call tools and take several steps, e.g. open other files.
- **Hybrid:** a system that combines an LLM with a SAST tool.
- **Precision:** the share of the tool's warnings that are real vulnerabilities.
- **Recall:** the share of real vulnerabilities that the tool finds.
- **F1:** a single score that balances precision and recall.
- **False-positive rate (FPR):** the share of safe code wrongly flagged as vulnerable.
- **SFDR (sampled false discovery rate):** the share of warnings that are false, estimated from a sample.
- **MCC:** a score that stays fair when vulnerable code is rare.
- **Prevalence / class balance:** the share of vulnerable samples in a test set. *Balanced* means 50%.
- **Trivial baseline:** a deliberately dumb method, e.g. "flag everything", that any real tool should beat.
- **Pairwise correctness:** the share of vulnerable/fixed code pairs where both versions are judged correctly.
- **Label noise:** wrong "vulnerable"/"safe" labels in a dataset.
- **Data leakage:** test samples that also appear in the training data, which inflates scores.
- **Contamination / training cutoff:** an LLM may have seen benchmark code during training. Code released after its training cutoff avoids this.
- **Synthetic vs real-world code:** code written to demonstrate a bug (e.g. the Juliet, OWASP and CASTLE suites) vs code from real projects.
- **Repository level:** analysing a whole project rather than single functions.
- **Benchmark:** a shared test dataset used to compare tools.
- **Systematic literature review (SLR):** a review that searches for and assesses all studies on a question using a fixed protocol.
- **Meta-analysis:** statistically combining the results of many studies.
- **Peer review / preprint:** expert checking before publication. A preprint has not been through it yet.
- **Version of record:** the final published version of a paper.
- **Novelty check:** targeted searches to confirm that a gap has not already been filled.
- **Significance test:** a statistical test of whether a difference could be due to chance.
