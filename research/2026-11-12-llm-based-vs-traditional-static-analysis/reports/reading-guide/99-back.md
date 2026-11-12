# Research Gaps and Opportunities

A **research gap** is a question that the existing studies leave open and that a new study could answer. We list a gap only when two conditions hold. First, evidence from the analysed papers supports it: authors' own future-work statements, repeated limitations, or contradictions. Second, a **novelty check** found no paper that already fills it. A novelty check is a set of targeted literature searches run specifically to look for such a paper.

All novelty checks were run on 2026-11-12. We used 35 database queries on OpenAlex, arXiv and Crossref, limited to 2024 onwards or 2025 onwards, plus 12 web searches for very recent work. In the second pass, the arXiv service timed out on several queries. We covered arXiv instead with one further query and by reading the abstract pages of the two papers we most needed to check. "We found no study" therefore always means "we found none in these searches on that date", never "this has never been done".

The gaps are called **Gap 1 to Gap 6** here. In the project's gap report they are G1 to G6. They are not the same as Agreements 1 to 11 in the Overview.

## The six gaps at a glance

The ranking combines how strong the evidence is with how feasible a study would be for a beginner.

| Gap | Short name | Evidence | Feasibility for a beginner | Confidence that it is still open | Second-pass verdict |
|---|---|---|---|---|---|
| Gap 1 | No common yardstick: published results are not re-scored against trivial baselines and realistic prevalence across studies | strong (9 or more papers) | easy | medium to high | unchanged |
| Gap 2 | No like-for-like test of LLMs, full SAST and fine-tuned DL on new, real code with context | strong (6 or more papers) | moderate | medium | narrowed |
| Gap 3 | Real bugs lost when LLMs filter SAST warnings are not controlled per vulnerability type | moderate (2 papers plus author future work) | easy to moderate | low to medium | unchanged |
| Gap 4 | Hybrid tools (IRIS, RepoAudit) lack an independent replication that explains the conflicting results | moderate | moderate to hard | medium | unchanged |
| Gap 5 | No real-vulnerability comparison of LLMs with standard SAST tools for PHP and Go | moderate | moderate | low to medium | narrowed |
| Gap 6 | No cost per confirmed vulnerability that includes human checking time and costs all three families | moderate | moderate | low to medium | narrowed |

"Narrowed" means a paper found in the second pass covers part of the gap. The rest remains open and is described below.

## Gap 1: No common yardstick for comparing published results

> **In one sentence:** many published LLM, SAST and DL results sit at or near the score of a "detector" that flags everything, yet nobody has systematically re-scored the published numbers across studies against such trivial baselines and at realistic prevalence.

### Evidence that the gap exists

- **Results sit at the flag-everything level.** On a balanced test set, flag-all scores F1 0.667 [I]. One study's flag-all baseline scored 0.6693 against a best model of 0.7075 [@shu2026evaluating, p. 11; @shu2026evaluating, p. 17] [V]. Another study's best F1 was 0.665–0.666 [@tan2026think, p. 7]. A third reports GPT F1 values of 48–66 [@yildiz2025benchmarking, p. 6]. In a fourth, "always vulnerable" rows appear among the best F1 values [@khare2025understanding, p. 16].
- **The same pattern appears at other prevalences.** On a sample with 35.4% vulnerable functions, LLM F1 was 0.405–0.615 against 0.523 for always-vulnerable [@deininger2026open, p. 7] [V]. At realistic 1:44 prevalence, every LLM's precision was 2.3–3.8% against 2.21% for flag-all [@deininger2026open, p. 8] [V]. In PHP, a baseline that only counts tokens matched or beat a random-forest model in 4 of 6 settings [@tashenova2026real, p. 8] [V]. On 2025 vulnerabilities, by our calculation, 7 of 12 LLM F1 values fell below the flag-all level of about 3.87% [@lu2025lab, p. 14] [I].
- **Changing the balance changes the winner.** Fine-tuned GPT-4o wins on balanced data, smaller models win on the imbalanced test [@shu2026evaluating, p. 17; @shu2026evaluating, p. 40] [V].
- **Scoring is unequal between families.** One study gives only LLMs a lenient rule for where a bug is located [@gnieciak2025large, p. 6] [V]. One benchmark's prompt tells the LLM how it will be scored [@dubniczky2025castle, p. 9] [V]. Scoring the exact line instead of the whole function halves F1 [@ahmed2026secvuleval, p. 8] [V].
- **Headline LLM-against-SAST numbers use five incompatible metrics** [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 10; @khare2025understanding, p. 9; @zhou2024comparison, p. 5; @li2026llm, p. 11] [I].
- **Simple tricks score well.** A word-count classifier reaches F1 0.86 on Big-Vul [@risse2025top, p. 11] [V]. GPT-4's pairwise score is below a random reference [@ding2025vulnerability, p. 9] [V].
- **The decision rule and the prompt can flip conclusions.** With the default cut-off, a good fine-tuned detector looked like it always said "safe"; the authors nearly concluded that trained detectors are no better than LLMs [@deininger2026open, p. 11] [V]. Rewording the prompt changed the winning LLM [@deininger2026open, p. 20] [V].
- **Authors ask for better evaluation rules** [@yildiz2025benchmarking, p. 2; @ding2025vulnerability, p. 2; @lu2025lab, p. 16] [A].

### Novelty verdict and closest prior work

**Still open (unchanged after the second pass).** Several studies now report trivial baselines for their own results: shu2026evaluating, deininger2026open and tashenova2026real; for lu2025lab, the baseline can be calculated. Each applies it only to its own numbers, and none re-scores other studies [I]. qin2026review recommends better reporting but recomputes no published results [@qin2026review, p. 13; @qin2026review, p. 12]. General "pitfalls" catalogues (CACM 2024, doi 10.1145/3643456; TOSEM 2025, doi 10.1145/3748647) re-score no vulnerability-detection results. A 2026 study re-scores models against a simple reference, but for warning triage, not vulnerability detection, and in a venue of unknown quality (doi 10.66308/air.e80134906). We found no study that recomputes published LLM, SAST and DL results across studies against trivial baselines and realistic prevalence (searches on 2026-11-12). **Confidence: medium to high.**

### What filling it would contribute

A "re-scored results table" for the field. It would show which reported LLM advantages survive once each result is compared with flag-all and evaluated at realistic prevalence [I]. It would also give a short reporting checklist: full error counts, prevalence, trivial baselines, scoring unit, number of runs. A new study should credit the existing within-study baselines rather than claim to be first to use them.

### A study a beginner could run

- **Type:** secondary analysis of published numbers. No models are run.
- **Data:** the results tables of the 20 primary studies in this project. Extract every row (study, tool, dataset, setting) that reports enough numbers to rebuild the counts of correct and wrong answers.
- **Method:** for each row compute MCC, Youden's J (recall minus false-positive rate), the F1 margin over flag-all, and the precision the tool would have at 1%, 5% and 17% prevalence. The flag-all F1 at prevalence p is 2p divided by (1 + p).
- **Validity check:** where a study published its own baseline, check that your calculation reproduces it.
- **Analysis:** within each study, rank tools before and after re-scoring and count how often the ranking changes. Do not pool datasets that the methodology comparison marks "not comparable". Report how many rows fail to beat flag-all.

### Feasibility

**Easy** [I]. A spreadsheet or a short Python script is enough; no GPU and no API cost. We estimate 2–4 weeks. It can go straight into the comparative review as an added-value table.

### Risks

Many rows lack the numbers needed (true negatives or false-positive rate), which can bias the sample; list those rows instead of dropping them silently. Rounding in published tables adds error. Lenient scoring rules cannot be undone afterwards. Copying errors are likely, so extract twice and spot-check against the PDFs.

## Gap 2: No like-for-like test of LLMs, full SAST and fine-tuned DL on new, real code with context

> **In one sentence:** one study now compares all three families on the same functions, but with lightweight SAST tools, isolated functions and old vulnerabilities; nobody has done it with a full semantic SAST tool such as CodeQL, on vulnerabilities published after the models were trained, and with surrounding file or repository context.

### Evidence that the gap exists

- **Two studies run all three families, each in a limited setting.** khare2025understanding runs CodeQL on artificial data only [@khare2025understanding, p. 7] [V]. deininger2026open runs 8 LLMs, Flawfinder, Cppcheck, Semgrep and two CodeBERT detectors on the same 1549 C/C++ functions [@deininger2026open, p. 6; @deininger2026open, p. 10] [V]. Its limits define what is left: CodeQL could not run because isolated functions cannot be built [@deininger2026open, p. 10] [V]; all vulnerabilities date from 2008–2022, before the models' training cutoffs, and recall is 7–15 points higher on pre-2020 ones [@deininger2026open, p. 24] [V]; it is function level, one dataset and C/C++ only [@deininger2026open, p. 25] [A].
- **That study shows why the gap matters.** Fine-tuned CodeBERT leads on balanced accuracy, Semgrep and Flawfinder lead on precision at realistic prevalence, and every LLM is at 2.3–3.8% precision [@deininger2026open, p. 8; @deininger2026open, p. 10] [V].
- **Other studies miss a family.** zhou2024comparison has no classic DL detector [@zhou2024comparison, p. 4] [V]. lu2025lab tests DL and LLMs on 2025 vulnerabilities but has no SAST tool [@lu2025lab, p. 4] [V]. tashenova2026real has no LLM [@tashenova2026real, p. 13] [V].
- **Results reverse across setups**, both for LLMs against SAST [@gnieciak2025large, p. 10; @khare2025understanding, p. 9; @li2026llm, p. 7] and for LLMs against DL [@fu2023chatgpt, p. 4; @ding2025vulnerability, p. 9; @shu2026evaluating, p. 40] [V].
- **Data leaks and training-data overlap are rarely controlled.** Exact copies between training and test data reach 18.9% [@ding2025vulnerability, p. 4] [V]. Benchmarks are probably in LLM training data [@kaniewski2026systematic, p. 30] [A]. Only three studies test on code published after the models were trained [@xiong2026sifting, p. 15; @li2026llm, p. 5; @lu2025lab, p. 4], and none of them runs all three families [I].
- **Authors call for it** [@chakraborty2024revisiting, p. 13; @ding2025vulnerability, p. 10] [A].

### Novelty verdict and closest prior work

**Narrowed.** deininger2026open fills the function-level, older-vulnerability, C/C++ version with lightweight SAST. A second three-family comparison exists for Python, Java and JavaScript at function level: Zhang et al. 2025 (arXiv 2503.01449, preprint, read as abstract only). It mentions no time separation and does not name its SAST tools. Dahiya et al. 2026 (arXiv 2605.23243, preprint, abstract only) has no SAST and no DL arm, so it does not fill the gap. Other near misses lack DL (RealVuln, arXiv 2604.13764) or SAST (VulEval, arXiv 2404.15596). We found no study that runs semantic SAST, fine-tuned DL and LLMs on the same real, de-duplicated, post-cutoff targets with file or repository context and a shared scoring unit (searches on 2026-11-12). **Confidence: medium.** Near misses now lack only one or two conditions, so re-check before publishing.

### What filling it would contribute

The first like-for-like answer to RQ1 on realistic, recent code. Comparing results on older and newer vulnerabilities would also estimate how much of the LLM advantage comes from having seen the test data during training. It would test whether deininger's finding (DL best on balanced accuracy, SAST best on precision) still holds with context and with CodeQL.

### A study a beginner could run

- **Data:** Python or Java vulnerabilities from GitHub Security Advisories or OSV, split into about 100 disclosed after the newest model's training cutoff and about 100 from before. Use each vulnerable function and its fixed version, and add unchanged functions from the same files to reach a realistic ratio such as 1:20. Have two people re-check 50 positive labels.
- **Arms:** Semgrep and CodeQL; a CodeBERT or UniXcoder fine-tuned on older data with project-separated splits; two or three open 7–14B LLMs, plain and step-by-step prompts, three runs each.
- **Baselines:** flag-all, random, and a function-length classifier.
- **Metrics:** recall, precision and MCC at the natural ratio; pairwise correctness on pairs; cost.
- **Analysis:** McNemar tests between arms on identical functions; bootstrap confidence intervals by project; older-versus-newer difference per arm.
- **Cheaper variant:** reuse the public VentiVul dataset of 2025 vulnerabilities [@lu2025lab, p. 2] and add a SAST arm, an LLM with file context, and a flag-all baseline.

### Feasibility

**Moderate** [I]. All tools are free and a 7B model runs on a laptop GPU or Colab. The hard parts are building the dataset and mapping SAST warnings to functions. Expect 6–10 weeks. A CodeQL arm on C/C++ projects such as Linux or Chromium requires building them, which is hard for a beginner.

### Risks

Labels from fix commits are noisy. Mapping warnings to functions can disadvantage SAST, so also report file-level results. Fine-tuning data for Python may be small. LLM results depend on the prompt. Some advisories are public before the official vulnerability date, so leakage may remain. Results may not generalise beyond one language.

## Gap 3: Real bugs lost when LLMs filter SAST warnings

> **In one sentence:** letting an LLM throw away SAST false alarms works, but it also throws away real vulnerabilities, unevenly across vulnerability types, and no study has tested a filter that is only applied where it is known to be safe.

### Evidence that the gap exists

- **One study measures the loss per vulnerability type.** The best agent cuts the false-alarm rate on the OWASP test suite from 98.3% to 6.3% [@xiong2026sifting, p. 12] but drops 22.25% of true vulnerabilities [@xiong2026sifting, p. 18] [V]. The miss rate is low for injection bugs (1.10% for SQL injection, 0.41% for cross-site scripting) but 77.17% for weak cryptography and 84.50% for weak hashing [@xiong2026sifting, p. 18] [V]. The authors plan vulnerability-type-aware strategies [@xiong2026sifting, p. 20] [A].
- **An industrial study shows the same trade-off.** It removes 94–98% of false alarms while keeping 75–88% of real bugs, on general bug types [@du2026reducing, p. 8] [V].
- **Recommended but not reviewed.** The largest systematic review recommends SAST-then-LLM filtering pipelines [@kaniewski2026systematic, p. 42] [A], but excludes such studies from its corpus [@kaniewski2026systematic, p. 8].
- **Real-world samples are small:** 50 alerts per set [@xiong2026sifting, p. 13] [V].

### Novelty verdict and closest prior work

**Still open (unchanged).** Several 2025–2026 preprints measure or reduce the loss, mostly on artificial suites: ZeroFalse (arXiv 2510.02534), an adjudication study reaching high recall on Juliet and similar suites (arXiv 2607.09979), QASecClaw (arXiv 2605.01885), a study of the same trade-off for dynamic scanners (arXiv 2610.08406) and Trusting the Tool (arXiv 2610.32876). We found no study that tests a filter applied only to vulnerability types with proven low miss rates, evaluated on held-out real-world security alerts with full trade-off curves (searches on 2026-11-12). **Confidence: low to medium**, because this area moves fast.

### What filling it would contribute

A practical view of filtering: how many real vulnerabilities are lost per type for a given reduction in false alarms, plus a simple rule that practitioners can adopt.

### A study a beginner could run

- **Data:** the OWASP Benchmark (Java, 2,740 labelled cases with an official scorer) for development, and about 100 SAST alerts from recent open-source Java projects, labelled by two people, for testing.
- **Method:** run Semgrep and CodeQL; ask two open 7–8B LLMs whether each alert is real, with a confidence score, three runs.
- **Policies compared:** no filter; filter everything; filter only the vulnerability types whose miss rate was below 5% on one half of OWASP, then test on the other half and on the real set.
- **Metrics:** share of false alarms removed, share of real bugs kept, and an expected checking cost for cost ratios from 1:10 to 1:100 between a false alarm and a missed bug.

### Feasibility

**Easy to moderate** [I]. Labels and the scorer are public, Java SAST runs easily on OWASP, and 7B models run locally. Expect 4–6 weeks. The main effort is labelling the real-world alerts.

### Risks

OWASP is artificial and probably in LLM training data. Groups per vulnerability type are small. Human labellers can be biased.

## Gap 4: No independent replication of hybrid tools that explains the conflicting results

> **In one sentence:** IRIS and RepoAudit look strong in their authors' papers and weak in the one independent study, and no one has re-run them in a way that shows which difference (targets, metric or labeller) causes the gap.

### Evidence that the gap exists

- **RepoAudit.** Authors: 78.43% precision and all 21 known bugs found, one run per setting [@guo2025repoaudit, p. 8; @guo2025repoaudit, p. 17] [V]. Independent study: 0 of 110 known C/C++ vulnerabilities and 92.77% false warnings [@li2026llm, p. 7; @li2026llm, p. 11] [V], at up to $1,247.66 per project [@li2026llm, p. 16] [V].
- **IRIS.** Authors: 55 against 27 of 120 vulnerabilities compared with CodeQL [@li2024iris, p. 8] [V]. Independent: 97.80% against 77.00% false warnings on new Java projects [@li2026llm, p. 12] [V].
- **The independent study's labeller is not independent.** It labels warnings with Codex, a tool it also evaluates [@li2026llm, p. 11] [V].
- **Gains need a strong LLM.** IRIS improves on CodeQL only with GPT-4; smaller LLMs make the false-discovery rate worse [@li2024iris, p. 10] [V].

### Novelty verdict and closest prior work

**Still open (unchanged).** li2026llm is itself the only independent re-evaluation in our searches. A 2026 preprint re-runs software-engineering technique papers in general (arXiv 2609.00468), not these tools. New agent tools (arXiv 2606.22263, arXiv 2604.11950) are not replications. We found no study that re-runs IRIS or RepoAudit on the original benchmark and on new targets with the same blinded human labelling (searches on 2026-11-12). **Confidence: medium**; replications may exist in artifact-evaluation reports that search engines do not index.

### What filling it would contribute

It tells practitioners whether published hybrid gains carry over to new code, and tells researchers which evaluation choices drive the reported differences.

### A study a beginner could run

- **Design:** 2 by 2. Target set (original benchmark subset against recent Java vulnerabilities) crossed with metric (the original "vulnerabilities detected" against the share of false warnings), on the same runs.
- **Data:** 30 vulnerabilities from the IRIS benchmark across 4 types plus 10–15 recent Java vulnerabilities. IRIS code and data are public [@li2024iris, p. 2].
- **Arms:** IRIS with one affordable model and one open model; CodeQL alone as baseline.
- **Labelling:** at least 100 warnings labelled by two people who do not know which tool produced them; report agreement (Cohen's kappa).

### Feasibility

**Moderate to hard** [I]. Building Java projects for CodeQL and running a hybrid pipeline is demanding. A reduced IRIS-only replication on 20–30 vulnerabilities with an open model is feasible in about 8 weeks. RepoAudit (C/C++, high API cost) is not recommended for a beginner.

### Risks

The original GPT-4 versions are being retired. CodeQL versions change. Builds can fail. API costs can grow.

## Gap 5: No comparison of LLMs with standard SAST tools on real PHP and Go vulnerabilities

> **In one sentence:** almost all evidence is about C/C++ and Java; for PHP, the only study in our set tests no LLM and uses a home-made analyser, and for Go we found nothing comparing LLMs with SAST.

### Evidence that the gap exists

- **The field is concentrated on C/C++ and Java** [@kaniewski2026systematic, p. 28] [V]. 555 vulnerability types appear in no analysed dataset [@kaniewski2026systematic, p. 34] [V]. The review calls for Python, Java, Rust and multi-language benchmarks [@kaniewski2026systematic, p. 40] [A].
- **Many authors list other languages as future work** [@guo2025repoaudit, p. 10; @li2024iris, p. 10; @du2026reducing, p. 10; @xiong2026sifting, p. 20; @li2026llm, p. 18; @deininger2026open, p. 25; @lu2025lab, p. 17] [A].
- **The multi-language studies are thin.** The 7-language study has no SAST arm [@shu2026evaluating, p. 7] [V]. zhou2024comparison covers Python with only about 8–10 test vulnerabilities per language [@zhou2024comparison, p. 6] [I].
- **The only PHP study cannot answer the question.** tashenova2026real built a benchmark of 1757 real vulnerabilities in 1281 WordPress plugins [@tashenova2026real, p. 3] [V]. Its SAST arm is an unnamed, home-made analyser that finds only 1.7–1.8% of vulnerabilities [@tashenova2026real, p. 9] [V]; the authors blame that implementation, not the technique [@tashenova2026real, p. 13] [A]. No LLM was run [@tashenova2026real, p. 13] [V].

### Novelty verdict and closest prior work

**Narrowed.** Neef et al. 2026 (arXiv 2606.21397; to appear at an ARES 2026 workshop; read as abstract only) tests six LLMs on real WordPress-plugin vulnerabilities. According to its abstract, the best model detected 63%, and it names no SAST baseline. deininger2026open cites it as a comparison of open and frontier LLMs on WordPress plugins [@deininger2026open, p. 3]. Zhang et al. 2025 (arXiv 2503.01449, abstract only) covers Python, Java and JavaScript at function level. A PHP SAST benchmarking framework exists without LLMs (Entropy 2025, doi 10.3390/e27090926). No Go-specific study turned up. We found no study comparing LLMs with an established SAST tool on real vulnerabilities in PHP or Go, and only function-level, snippet-level or artificial-repository evidence for JavaScript and Python (searches on 2026-11-12). **Confidence: low to medium**; the Neef et al. full text may contain a tool baseline its abstract does not mention.

### What filling it would contribute

A test of whether "LLMs have higher recall and lower precision" holds in web languages, where injection bugs (which LLMs handle best [@xiong2026sifting, p. 18]) are common [I].

### A study a beginner could run

- **PHP data:** the expert-checked subset released with tashenova2026real (125 vulnerable and 247 safe functions) [@tashenova2026real, p. 11], plus the plugin versions for file-level runs, rebuilt with the released loader [@tashenova2026real, p. 14]. If Neef et al. released their plugin set, reuse it so results can be compared.
- **Go data:** about 60 Go vulnerabilities from the Go vulnerability database (OSV).
- **Arms:** established SAST (Semgrep; for PHP also a taint tool such as Psalm or Progpilot; for Go, gosec); two open LLMs at function level and at file level; the token-count baseline [@tashenova2026real, p. 8]; and flag-all.
- **Metrics:** recall on known vulnerabilities; precision on a hand-labelled sample of warnings; cost; per-type recall with confidence intervals.

### Feasibility

**Moderate** [I]. The tools are free and need no build step for PHP and Go, and PHP labels already exist. The main cost is labelling warnings that fall outside the labelled subset.

### Risks

Label quality: only 48.8% of cleaned positive PHP labels were genuine [@tashenova2026real, p. 11]; using the expert-checked subset reduces this. 125 positives give wide confidence intervals. Tools cover different vulnerability types. Old plugin versions may be gone; about 54% of indexed vulnerabilities could not be recovered in the PHP study [@tashenova2026real, p. 3]. Older vulnerabilities are likely in LLM training data.

## Gap 6: No cost per confirmed vulnerability that includes human checking time

> **In one sentence:** we now know the computing cost of an LLM per real vulnerability found, but not the far larger cost of the human time spent checking the many false alarms, and not the matching cost for SAST and DL on the same code.

### Evidence that the gap exists

- **Most studies report no money cost.** 13 of our 20 primary studies report none [I, our count]. The seven that do are du, guo, li2026llm, shu, tan, xiong and deininger [@du2026reducing, p. 8; @guo2025repoaudit, p. 7; @li2026llm, p. 16; @shu2026evaluating, p. 42; @tan2026think, p. 10; @xiong2026sifting, p. 17; @deininger2026open, p. 7].
- **Where measured, cost is decisive.** Per project, cost ranges from $2.54 in the RepoAudit paper to an average of $172.77 and a maximum of $1,247.66 in the independent study [@guo2025repoaudit, p. 7; @li2026llm, p. 16] [V]. Reasoning mode costs 4.5–12.1 times more per task [@deininger2026open, p. 18] [V].
- **Compute cost per true positive exists only for LLMs.** It is USD 0.003–0.212 and 3.7–119.6 kJ per true positive at 1:44 prevalence [@deininger2026open, p. 8] [V]. Flawfinder is given as about zero; no figure is given for CodeBERT, Cppcheck or Semgrep [@deininger2026open, p. 8; @deininger2026open, p. 11] [V].
- **Human checking is left out.** Each LLM true positive comes with 25.6–41.9 false positives [@deininger2026open, p. 8] [V], but analyst time is not costed [I]. At such ratios, analyst time would plausibly dominate a compute cost of a few cents [I].
- **Part of the energy figures are estimates.** Some energy values per true positive come from calculation estimates, not measurement [@deininger2026open, p. 14] [V].
- **Authors call for audit-time measurement** [@li2026llm, p. 18; @qin2026review, p. 13] [A].

### Novelty verdict and closest prior work

**Narrowed.** deininger2026open gives compute cost per true positive for LLMs but no human checking time and no costed SAST or DL arm. A 2026 preprint argues that checking capacity, not bug finding, is the bottleneck, but its abstract reports no measured time (arXiv 2605.24632). Vendor benchmarks report dollars per true positive for their own products, but they are not peer-reviewed, have conflicts of interest and exclude analyst time. We found no peer-reviewed study reporting cost per confirmed vulnerability that includes human checking time, for LLM, SAST and DL arms on the same targets (searches on 2026-11-12). **Confidence: low to medium.**

### What filling it would contribute

A decision-ready number for practitioners: dollars and analyst minutes per real vulnerability found, for each family [I].

### A study a beginner could run

Add it to the Gap 2 study as a second outcome. Record compute cost per arm; for SAST and DL use processor time times a stated hourly price, so they are not left at "about zero". Time two people checking a random 50 warnings per arm. Cost per confirmed vulnerability equals compute cost plus checking minutes times an hourly wage, divided by the number of confirmed vulnerabilities. Report it at realistic prevalence and for a range of wages.

### Feasibility

**Moderate** [I]. Cheap as an add-on to Gap 2; on its own it needs the same set-up.

### Risks

Checking time depends on the checker's skill and on the order in which warnings are shown. API prices change, and one model's price varied up to 14 times between providers [@deininger2026open, p. 5].

## Is our own review new? (positioning check)

Besides the six gaps, we checked whether a review like ours already exists. No separate follow-up topic novelty checks have been saved in the reports folder yet; this positioning check is recorded in the gap report.

**Verdict.** We found no review that both (1) combines evidence across all three families plus both kinds of hybrid, and (2) explains specific contradictions between studies through their test setup (searches on 2026-11-12). **Confidence: medium.**

- kaniewski2026systematic covers LLM detection only and excludes studies that filter tool output [@kaniewski2026systematic, p. 8].
- zhou2025large predates almost all hybrid, agent and project-scale evidence; its only LLM-against-SAST study is the authors' own preprint [@zhou2025large, p. 22].
- sheng2025llms is a narrative survey that does not compare families on matched results [I].
- qin2026review is the closest competitor. It shares our "evaluation reliability" framing [@qin2026review, p. 10], but it has no search protocol, puts SAST out of scope [@qin2026review, p. 4] and reuses studies we already cover [@qin2026review, p. 15], so it is not independent evidence [I].

[I] Our review should present itself as a critical comparative review, not a full systematic review, because it has 24 papers. Its distinct contribution is the cross-family, contradiction-explaining angle. The Gap 1 re-scoring table would make that contribution concrete.

## Next steps checklist

1. Decide whether to run an optional third pass that adds the two high-priority papers below (Zhang et al. 2025 and Neef et al. 2026).
2. If yes, find a legal open-access copy or ask your library, then analyse both papers from full text and re-check Gap 2 and Gap 5.
3. Screen the Information and Software Technology 2026 paper (doi 10.1016/j.infsof.2026.108213); we could not retrieve its abstract.
4. Build the Gap 1 re-scored results table. It is the easiest gap and adds the most value to the review.
5. Frame the paper as a critical comparative review and cite qin2026review and kaniewski2026systematic as the nearest reviews.
6. Re-run the novelty searches for Gap 2, Gap 3 and Gap 5 shortly before submitting, because these areas move fast.
7. Where a paper was read from its arXiv copy, check key numbers against the published version before quoting them.
8. If you want a follow-up empirical study, pick Gap 3 (4–6 weeks) or the cheaper variant of Gap 2 that reuses VentiVul.

## Recommended papers not yet included

These were found during novelty checks. They are **not analysed**; anything we say about them comes from abstracts or titles only.

1. **Zhang et al. 2025**, Benchmarking Large Language Models for Multi-Language Software Vulnerability Detection (arXiv 2503.01449, preprint). High priority. A second same-data comparison of LLMs, fine-tuned small models and SAST, and the only one in Python, Java and JavaScript. Relevant to RQ1, Gap 2 and Gap 5. Our first-pass searches returned it, but we missed it.
2. **Neef et al. 2026**, Evaluating LLMs for Real-World Web Vulnerability Detection (arXiv 2606.21397; AI&CCPS Workshop at ARES 2026, doi 10.1007/978-3-032-35576-8_3). High priority. Six LLMs on real WordPress-plugin vulnerabilities, with code and data released. The closest work to Gap 5; the full text must show whether it has a tool baseline.
3. **[SoK] Large Language Models in Security Code Review and Testing** (Journal of Systems Research 2026, doi 10.5070/sr3.62177). A second review competitor that compares LLMs with traditional tools.
4. **RealVuln** (arXiv 2604.13764, preprint). SAST against LLMs on Python repositories. The authors evaluate their own company's scanner, a conflict of interest.
5. **Leveraging Large Language Models for advanced static code analysis** (Information and Software Technology 2026, doi 10.1016/j.infsof.2026.108213). Screen first; relevance unknown.
6. **Dahiya et al. 2026**, Are Frontier LLMs Ready for Cybersecurity? (arXiv 2605.23243, preprint). Low priority; no SAST or DL arm in its abstract.
7. Optional: ZeroFalse (arXiv 2510.02534) and Trusting the Tool (arXiv 2610.32876) for the filtering discussion; Out of Distribution, Out of Luck (arXiv 2507.21817, ICSE 2026) for RQ2; and a web-snippet study comparing against an all-vulnerable classifier (doi 10.66571/tsarka-3134-6057-11, venue quality unknown) for Gap 1.

# Glossary

| Term | Plain-language meaning |
|---|---|
| Vulnerability | A security bug that an attacker can exploit. |
| CVE | Common Vulnerabilities and Exposures: a public ID for one known vulnerability, such as CVE-2025-1234. |
| CWE | Common Weakness Enumeration: a catalogue of vulnerability types; for example CWE-89 is SQL injection. |
| SQL injection, XSS | Injection bugs: an attacker smuggles commands into a database query (SQL injection) or scripts into a web page (cross-site scripting, XSS). |
| Static analysis | Examining code without running it. |
| SAST | Static application security testing: tools that scan source code with hand-written rules to find vulnerabilities. |
| CodeQL | A semantic SAST tool that turns code into a database and runs queries on it; it usually needs a buildable project. |
| Semgrep, Flawfinder, Cppcheck | Lighter SAST tools that match patterns in code; they work on single files or functions without building. |
| Taint analysis | A SAST technique that follows untrusted input (a "source") to a dangerous operation (a "sink"). |
| Large language model (LLM) | A very large AI model trained on text and code, such as GPT-4 or Llama, that answers questions in natural language. |
| Frontier model | One of the most capable commercial LLMs, used through a paid API. |
| Open-weight model | An LLM whose model files are public, so it can run on your own computer. |
| Deep-learning (DL) detector | A neural network trained on labelled examples to classify code as vulnerable or safe, such as LineVul or Devign. |
| Pre-trained language model (PLM) | A smaller model such as CodeBERT that is pre-trained on code and then fine-tuned for one task. |
| Fine-tuning | Further training a pre-trained model on task-specific labelled data. |
| Prompting, zero-shot, few-shot | Asking an LLM directly; zero-shot gives no examples, few-shot gives a few solved examples in the prompt. |
| Chain-of-thought | A prompt that asks the LLM to reason step by step before answering. |
| Reasoning or thinking mode | An LLM setting that generates long internal reasoning before the answer; it costs more. |
| Agent | An LLM that can use tools, such as opening files or running searches, over several steps. |
| Hybrid | A system that combines an LLM with a SAST tool. |
| Alarm filtering (triage) | Sorting tool warnings into real and false ones; here, done by an LLM. |
| True positive / false positive | A correct warning about a real bug / a warning about code that is actually safe (a false alarm). |
| False negative | A real vulnerability that the tool missed. |
| Precision | Share of warnings that are real vulnerabilities. |
| Recall | Share of real vulnerabilities that the tool finds. |
| F1 score | One number combining precision and recall; high only when both are high. |
| Accuracy | Share of all answers that are correct; misleading when vulnerable code is rare. |
| Balanced accuracy | The average of recall on vulnerable code and recall on safe code; any trivial baseline scores 0.5. |
| MCC | Matthews correlation coefficient: a score from -1 to 1 that stays fair when classes are imbalanced; 0 means no better than chance. |
| False-positive rate (FPR) | Share of safe code that is wrongly flagged. |
| False discovery rate (FDR, SFDR) | Share of warnings that are false; SFDR estimates it from a random sample of warnings. |
| ROC-AUC | A score from 0.5 (chance) to 1 that measures how well a model ranks vulnerable above safe code, regardless of the cut-off. |
| Decision threshold | The cut-off score above which a model says "vulnerable"; moving it trades precision against recall. |
| Prevalence | Share of vulnerable samples in the test data; real code has few. |
| Balanced test set | A test set with 50% vulnerable samples; easier than reality. |
| Trivial baseline | A "detector" that ignores the code, for example flag-all (always vulnerable), always safe, or a rule based on function length. |
| Pairwise correctness (P-C, pAcc, PACC) | Share of vulnerable/fixed code pairs where both versions are classified correctly; tests whether a model notices the fix. |
| VD-S | A PrimeVul metric: the share of vulnerabilities missed when false alarms are held at 0.5% or lower. |
| Benchmark | A shared test dataset used to compare tools. |
| Synthetic benchmark | Artificial test code written to contain known bugs, such as Juliet or the OWASP Benchmark. |
| Big-Vul, Devign, PrimeVul | Popular C/C++ vulnerability datasets; PrimeVul is a cleaner, de-duplicated and time-split version built from older ones. |
| Label noise | Wrong labels in a dataset, such as "vulnerable" code that is not vulnerable. |
| Data leakage | Test examples that also appear in the training data, which inflates scores. |
| Data contamination, training cutoff | An LLM may have seen the test code during training; the training cutoff is the date after which it saw no data. Post-cutoff code is safer to test on. |
| Temporal split, out-of-distribution | Testing on code from a later time or another source than the training data. |
| Function, statement and repository level | Judging a whole function, the exact faulty line, or a whole project. |
| Systematic literature review (SLR) | A review that searches, selects and appraises studies with a written, repeatable protocol. |
| Narrative review | A review without a fixed search protocol; more open to selective reading. |
| Peer review, preprint | Expert checking before publication; a preprint is posted without it. |
| Novelty check | Targeted searches to see whether a proposed gap has already been filled. |
| Cohen's kappa | A measure of how well two human labellers agree beyond chance. |
| Bootstrap confidence interval | A range of plausible values found by re-sampling the data many times. |
| McNemar test, Holm correction | A test for whether two classifiers differ on the same items; Holm correction adjusts for running many tests. |

# About this guide

**What it is.** A plain-language guide to the project "LLM-based vs Traditional Static Analysis and Deep Learning Approaches for Source Code Vulnerability Detection: A Comparative Review". It was produced on 2026-11-12.

**How the evidence was gathered.**

1. **Scoping.** The topic, five research questions and inclusion rules were fixed first. The time window was 2020–2026, with peer-reviewed work preferred and preprints allowed only if central and flagged.
2. **Search.** Queries on six themes were run on OpenAlex, Crossref and arXiv, followed by snowballing (checking the references and citations of key papers). The project log records 54 database searches, including the novelty checks.
3. **First pass.** 20 papers were selected and analysed.
4. **Second pass.** Four more papers were added to test the gaps and to cover the closest competing review: qin2026review, lu2025lab, tashenova2026real and deininger2026open. The final set is 24 papers: 20 primary studies and 4 reviews.
5. **Reading.** All 24 papers were read in full text; none is abstract-only. Each analysis records findings with page references and the labels [V], [A] and [I].
6. **Checking.** Four critical reviews (A to D) re-checked every analysis against the paper text, and all findings were fixed before analyses were marked complete.
7. **Synthesis.** An evidence matrix (221 rows), a methodology comparison, answers to RQ1–RQ5 and a gap report with recorded novelty checks were built from the analyses. This guide is written only from those files.

**Limitations.**

- 24 papers is a focused set, not a complete systematic review. Relevant studies may be missing, and two recommended papers are not yet analysed.
- Most papers were read from arXiv copies rather than the final published version, so a few numbers may differ.
- Analyses and critical reviews were written by AI research agents (Claude) under the user's direction. No second human extractor re-checked them.
- Several results come from single studies with one run and no statistical tests; evidence strength is stated for each finding.
- In the second-pass novelty checks the arXiv service timed out on several queries; we compensated with other sources, but coverage of very recent arXiv preprints is weaker.
- Novelty verdicts are valid as of 2026-11-12. The field publishes very quickly, so re-check before relying on them.
- Papers found during novelty checks were judged from abstracts only.
