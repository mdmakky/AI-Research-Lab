# Methodology comparison — LLM-based vs traditional static analysis and deep learning for source-code vulnerability detection

- Project: `2026-11-12-llm-based-vs-traditional-static-analysis`
- Date: 2026-11-12
- Inputs: 24 analyses (`status: complete`, all full text), `evidence-matrix.md`, `literature-matrix.md`, critical reviews A–D of 2026-11-12. Updated pass 2, 2026-11-12: added qin2026review, lu2025lab, tashenova2026real and deininger2026open.
- Labels: **[V]** verified in the paper's own data, **[A]** author claim, **[I]** our interpretation. Unlabelled numeric statements are [V] from the cited page.
- Source tiers: four items are recorded by `rlab` as arXiv preprints. IRIS [@li2024iris, p. 1] and RepoAudit [@guo2025repoaudit, p. 1] are the ICLR 2025 and ICML 2025 camera-ready texts. lu2025lab was read as the arXiv v4 accepted manuscript [@lu2025lab, p. 1]. The orchestrator confirmed via Crossref that it is published in the Journal of Systems and Software (2026, doi 10.1016/j.jss.2026.113185). We treat it as peer-reviewed; its page refs follow arXiv v4. Only zhou2024comparison is a true preprint without a known peer-reviewed version (**not peer-reviewed**) [@zhou2024comparison, p. 1]. Of the other 20 papers, 15 were read from arXiv copies rather than the version of record. Five were read in publisher form: tan2026think, yildiz2025benchmarking, deininger2026open, tashenova2026real and qin2026review (see §5, W9). qin2026review appears in a low-visibility venue (Zeus Press) that does not document peer review [@qin2026review, p. 1]. We give it the weight of grey literature and use it for positioning only.

A short glossary for readers new to the area:
- *SAST* (static application security testing) tools such as CodeQL or Semgrep scan code with hand-written rules.
- *DL detectors* (e.g. LineVul, Devign) are neural networks trained on labelled vulnerable code.
- *Prevalence* is the share of vulnerable samples in a test set. A *balanced* test set has 50% vulnerable samples; real code has far fewer (about 2% in two pass-2 studies).
- A *trivial baseline* is a classifier that ignores the code, for example "always vulnerable", "always safe" (majority class) or a rule based only on function length.
- *Balanced accuracy* is the mean of the recall on vulnerable and on safe samples, so every trivial baseline scores 0.5.
- *Pairwise correctness (P-C / pAcc)* is the share of vulnerable/patched function pairs where both versions are classified correctly. lu2025lab calls the same idea *patch pair accuracy (PACC)*.
- *SFDR* is the sampled false discovery rate, i.e. the share of a tool's warnings that are false.
- *Out-of-distribution (OOD)* test data come from a different source or time period than the training data.

## 1. Overview table

| Paper | Tier / text read | Design | Data, N, unit | Metrics | Comparators | Statistics / runs | Data & code |
|---|---|---|---|---|---|---|---|
| ahmed2026secvuleval [@ahmed2026secvuleval, p. 6; @ahmed2026secvuleval, p. 8] | AIware 2026; arXiv v1 | Benchmark + 5 LLMs in a multi-agent pipeline | SecVulEval 25,440 C/C++ functions; detection on 300 functions (~120 vulnerable) | P/R/F1 at function and statement level (manual judging) | none outside LLMs | one run; Mann-Whitney only for function length [@ahmed2026secvuleval, p. 13] | dataset + code public [@ahmed2026secvuleval, p. 3] |
| chakraborty2024revisiting [@chakraborty2024revisiting, p. 4] | TSE; arXiv author copy | Replication of 4 DL detectors + 2 fine-tuned LLMs on new realistic data | Real-Vul: 5,528 vulnerable + ~1.68M "uncertain" functions, 10 C/C++ projects, time split | Acc, P, R, F1, AUC | DeepWukong, LineVul, ReVeal, IVDetect; CodeLlama, Mixtral | no CIs; Mann-Whitney in side analyses only [@chakraborty2024revisiting, p. 10] | Zenodo [@chakraborty2024revisiting, p. 2] |
| deininger2026open [@deininger2026open, p. 4] | Computers 2026; publisher PDF | Benchmark: 8 zero-shot LLMs vs 3 SAST tools vs 2 fine-tuned CodeBERT detectors on identical functions; cost and energy | PrimeVul test split, C/C++; 1549 functions (all 549 vulnerable + 1000 safe; 35.4% vulnerable), re-scored at the natural 1:44 prevalence | balanced accuracy, MCC, F1, precision at 1:44, FP per TP, USD and kJ per TP | Flawfinder, Cppcheck, Semgrep; CodeBERT-Devign, CodeBERT-PrimeVul; always-safe / always-vulnerable [@deininger2026open, p. 6; @deininger2026open, p. 7] | paired bootstrap with Holm correction; one generation at T = 0 [@deininger2026open, p. 6] | Zenodo [@deininger2026open, p. 26] |
| ding2025vulnerability [@ding2025vulnerability, p. 6] | ICSE 2025; arXiv v2 | Label/duplication audit + PrimeVul benchmark + 7 code LMs | 6,968 vulnerable / 228,800 benign C/C++ functions, 755 projects; 564 test pairs for GPT models | Acc, F1, VD-S, P-C | fine-tuned code LMs vs prompted/fine-tuned GPT-3.5/4; random | runs/seeds not reported | public artifact [@ding2025vulnerability, p. 3] |
| du2026reducing [@du2026reducing, p. 4] | ICSE-SEIP 2026; arXiv v1 | Industrial study: interviews + offline evaluation of alarm triage | 433 alarms (328 FP / 105 TP) from Tencent's BkCheck, mostly C/C++ | Acc, P, R, F1, false-alarm removal; seconds and USD per alarm | prompting LLMs, hybrid LLM4SA/LLM4PFA, 4 DL models | 3 runs, majority vote; no tests [@du2026reducing, p. 6] | data confidential; replication package [@du2026reducing, p. 2] |
| dubniczky2025castle [@dubniczky2025castle, p. 6] | LNCS chapter; arXiv v2 | Micro-benchmark; 13 SAST + 2 formal tools vs 10 LLMs | CASTLE: 250 hand-written C programs (150 vulnerable / 100 clean), 25 CWEs | TP/FP/FN, P, R, CASTLE score | each other | repeats "<3%" deviation, number not reported [@dubniczky2025castle, p. 14] | public [@dubniczky2025castle, p. 1] |
| fu2023chatgpt [@fu2023chatgpt, p. 3] | APSEC 2023; arXiv v1 | Prompted ChatGPT vs fine-tuned LMs, 4 tasks | Big-Vul (C/C++), random 80/10/10 split, 1:20 ratio | F1, P, R, top-10 line accuracy | AIBugHunter, CodeBERT, GraphCodeBERT | single point estimates | data, prompts public [@fu2023chatgpt, p. 1] |
| gnieciak2025large [@gnieciak2025large, p. 6] | IEEE Access; arXiv v1 | Head-to-head, 3 SAST vs 3 LLMs | 10 author-prepared C# projects, 63 seeded vulnerabilities | macro P/R/F1, runtime | SonarQube, CodeQL, Snyk Code | single run; no tests | tool code public [@gnieciak2025large, p. 1] |
| guo2025repoaudit [@guo2025repoaudit, p. 7] | ICML 2025 (rlab: preprint) | Agent tool paper + ablations | 15 C/C++ projects (avg 251 KLoC), 21 known NPD/MLK/UAF bugs; 9 field projects | TP, FP, precision; reproduction of known bugs; tokens, USD, time | Meta Infer, Amazon CodeGuru, CoT prompting, LLMDFA | one run per setting [@guo2025repoaudit, p. 17] | code public [@guo2025repoaudit, p. 1] |
| kaniewski2026systematic [@kaniewski2026systematic, p. 8] | TOSEM; arXiv v2 | Systematic literature review (SLR) | 263 studies (78 arXiv preprints), 2020–Nov 2025 | taxonomy counts, dataset statistics | n/a | none | artifacts public [@kaniewski2026systematic, p. 3] |
| khare2025understanding [@khare2025understanding, p. 3] | ICST 2025; arXiv v3 | 16 LLMs × 3 prompts vs SAST and DL | 5,000 balanced function snippets: OWASP, Juliet Java/C, CVEFixes Java/C | Acc, P, R, F1 | CodeQL (synthetic only), DeepDFA, LineVul [@khare2025understanding, p. 7] | one run, T = 0; no tests | prompts given; code not linked [@khare2025understanding, p. 14] |
| li2024iris [@li2024iris, p. 7] | ICLR 2025 (rlab: preprint) | Hybrid tool: LLM-inferred taint specs + CodeQL + LLM triage | CWE-Bench-Java: 120 real Java CVEs (avg 300K SLOC); 30 latest-version projects | detections, AvgFDR, AvgF1 | CodeQL, Infer, SpotBugs, Snyk; 7 LLMs | runs not reported (T = 0, fixed seed) [@li2024iris, p. 21] | code + data public [@li2024iris, p. 2] |
| li2026llm [@li2026llm, p. 5] | TSE; arXiv v2 | Project-scale comparison + FP taxonomy + cost | 265 known vulnerabilities (110 C/C++, 155 Java), 8 CWEs; 24 real-world projects | recall, precision, SFDR, tokens/USD/minutes | 5 specialised LLM detectors, Codex, Claude Code vs CodeQL, Semgrep, CSA, SpotBugs | no tests between tools; CI only for labelling accuracy [@li2026llm, p. 11] | artifacts public [@li2026llm, p. 2] |
| lu2025lab [@lu2025lab, p. 7] | JSS 2026; arXiv v4 accepted manuscript | 4×4 within/cross-dataset DL matrix + temporally separated OOD test of DL and open LLMs | Juliet, Devign, BigVul, ICVul (C/C++); VentiVul: 13,326 functions, 200 Linux/Chromium CVEs disclosed from May 2025, 263 pairs; prevalence 1.97% [I] [@lu2025lab, p. 4] | Acc, P, R, F1, CVE detection rate, PACC | ReVeal, LineVul (trained on 4 datasets) vs 4 open LLMs ≤ 32B, zero/few-shot/CoT; no SAST, no trivial baseline | none; one deterministic LLM run; DL runs not reported [@lu2025lab, p. 8] | GitHub [@lu2025lab, p. 2] |
| qin2026review [@qin2026review, p. 1] | Computers and AI (Zeus Press), peer review not documented; publisher PDF | Narrative review, single author, no search protocol | 32 references, 2019–2026 [@qin2026review, p. 14] | none (qualitative) | n/a | none | no study list |
| risse2025top [@risse2025top, p. 6] | PACMSE (FSE 2025); arXiv v2 | 81-paper survey + expert labelling + word-count probe | 300 vulnerable- + 90 secure-labelled functions (BigVul, Devign, DiverseVul), 2 annotators | label accuracy, Cohen's κ, F1 | published SOTA scores | κ only | public [@risse2025top, p. 13] |
| sheng2025llms [@sheng2025llms, p. 8] | ACM CSUR; arXiv v2 | Narrative survey | 58 studies, 2019–2024 | counts, F1 listing | n/a | none | paper list [@sheng2025llms, p. 1] |
| shu2026evaluating [@shu2026evaluating, p. 7] | EMSE; arXiv v2 | 8 fine-tuned PLMs vs 5 LLMs (zero/few-shot, instruction tuning), function + line level | REEF, 7 languages, balanced test 2,026 functions; imbalanced and 2024–25 time-split variants | Acc, P, R, F1, MCC, AUC, cost | CodeT5P etc.; dummy classifiers [@shu2026evaluating, p. 11] | none; ~30 configurations on one split | public [@shu2026evaluating, p. 48] |
| tan2026think [@tan2026think, p. 3] | ASE 2026; publisher PDF | Factorial study, 64 configurations | PrimeVul Pair: 870 functions (435 pairs), 4 open LLMs | Acc, P, R, F1, P-C, FPR; energy, USD | instruct vs thinking; 4 orchestrations; call-matched self-revision | Wilcoxon + Cohen's d; single runs at T = 0 [@tan2026think, p. 6] | Zenodo [@tan2026think, p. 12] |
| tashenova2026real [@tashenova2026real, p. 5] | BDCC 2026; publisher PDF | Benchmark + plugin-grouped 5-fold CV; in-house static taint analyser vs classical ML vs LSTMs vs 3 trivial baselines; **no LLM** | WordPress plugins, PHP: 1757 CVEs in 1281 plugins [@tashenova2026real, p. 3]; 15,294 (Variant A) / 24,917 (Variant B) functions after leakage control | macro-F1 (fold mean, 95% CI), balanced accuracy, MCC, PR-AUC, vulnerable-class FNR | unnamed intra-procedural lexical taint analyser; RF, SVM; Bi-LSTM; majority, source/sink rule, token count [@tashenova2026real, p. 5] | paired tests described; one reported (plugin-level Wilcoxon p = 0.295) [@tashenova2026real, p. 9]; single seed [@tashenova2026real, p. 7] | labels, folds, predictions on GitHub/Zenodo; plugin code re-downloaded [@tashenova2026real, p. 14] |
| xiong2026sifting [@xiong2026sifting, p. 6] | PACMSE (ISSTA 2026); arXiv v3 | 3 agent frameworks × 3 backbones vs vanilla prompting for SAST false-positive filtering | OWASP v1.2 (2,740 cases); 50 Vul4J alerts; 50 post-cutoff OSS-Fuzz alerts | residual FPR, FP recall/precision/F1, TP miss rate, USD | vanilla LLM; 4 SAST tools | no tests; κ only | Zenodo [@xiong2026sifting, p. 21] |
| yildiz2025benchmarking [@yildiz2025benchmarking, p. 5] | ACL 2025 | Benchmark + plain / dependency-augmented / ReAct LLMs | JITVul: 879 PrimeVul CVEs → 1,758 paired samples, 91 CWEs | F1, pairwise accuracy | LLM designs only | runs not reported; no tests | public [@yildiz2025benchmarking, p. 2] |
| zhou2024comparison [@zhou2024comparison, p. 3] | arXiv preprint, **not peer-reviewed** | 15 SAST vs 12 open LLMs at repository level | 270 CVEs in 134 repos (Java, C, Python); ~8–10 test CVEs per language [I] [@zhou2024comparison, p. 6] | detection ratio S1/S2, marked-function ratio (no precision/F1) | each other | single run | "public", no link [@zhou2024comparison, p. 10] |
| zhou2025large [@zhou2025large, p. 7] | TOSEM; arXiv v3 | SLR with quality scoring | 58 studies, 2018–Mar 2024 | counts | n/a | none | keywords only [@zhou2025large, p. 5] |

[I] There are 19 primary detection studies (all except the four reviews and risse2025top). Only tan2026think and deininger2026open apply significance tests to their main comparison [@tan2026think, p. 6; @deininger2026open, p. 6]. tashenova2026real describes paired tests but reports only one [@tashenova2026real, p. 9]. Seven report monetary cost: du, guo, li2026llm, shu, tan, xiong and deininger [@du2026reducing, p. 8; @guo2025repoaudit, p. 7; @li2026llm, p. 16; @shu2026evaluating, p. 42; @tan2026think, p. 10; @xiong2026sifting, p. 17; @deininger2026open, p. 7]. Only three report trivial-classifier baselines next to their headline metric: shu, deininger and tashenova [@shu2026evaluating, p. 11; @deininger2026open, p. 7; @tashenova2026real, p. 5] (§5, W1).

## 2. Approach families

| Family | Papers | Typical strengths | Typical weaknesses |
|---|---|---|---|
| A. Head-to-head LLM vs SAST | gnieciak2025large, dubniczky2025castle, khare2025understanding, zhou2024comparison, li2026llm, deininger2026open | Same targets for both families; directly answers RQ1 | Small or synthetic targets, SAST on default rules or lightweight tools only, unequal scoring, single runs |
| B. LLM vs fine-tuned DL / PLM | fu2023chatgpt, ding2025vulnerability, chakraborty2024revisiting, khare2025understanding, shu2026evaluating, zhou2024comparison, du2026reducing, deininger2026open, lu2025lab | Large N; standard metrics; trivial baselines sometimes reported | Noisy function-level C/C++ datasets; F1 on balanced data; no SAST arm except khare, zhou2024 and deininger |
| B2. SAST vs classical ML/DL, no LLM | tashenova2026real | Real CVEs in a new language (PHP); leakage-controlled; trivial baselines | Single bespoke SAST tool; no LLM; about half of positive labels wrong |
| C1. Hybrid: LLM inside the analyser (spec inference, dataflow) | li2024iris, guo2025repoaudit; independently re-evaluated in li2026llm | Real projects; builds on mature analysers; new bugs found | Evaluated by tool authors on chosen targets; recall rarely measured |
| C2. Hybrid: LLM filters SAST alarms | du2026reducing, xiong2026sifting | Large false-alarm reduction; cost per alarm measured | True vulnerabilities also filtered; small real-world samples |
| D. Agentic / reasoning LLMs | tan2026think, yildiz2025benchmarking, ahmed2026secvuleval, li2026llm (general agents), xiong2026sifting | Repository context and tool use; controlled factorial designs (tan) | Cost; gains often explained by more inference or more flagging |
| E. Benchmark-realism studies | chakraborty2024revisiting, ding2025vulnerability, risse2025top, ahmed2026secvuleval, yildiz2025benchmarking, dubniczky2025castle, li2024iris, lu2025lab, tashenova2026real, deininger2026open | Audit labels and leakage; temporal and realistic-prevalence testing; trivial baselines; build better benchmarks | Mostly C/C++; some audits are second-hand or single-annotator |
| F. Surveys and reviews | kaniewski2026systematic, sheng2025llms, zhou2025large, qin2026review | Field-wide view of datasets and methods | No performance meta-analysis; overlap with primary studies; qin is narrative and not independent |

**A. Head-to-head LLM vs SAST.** Results depend on the unit of analysis. On small, self-contained targets, prompted frontier LLMs score above SAST: macro F1 0.75–0.80 vs 0.26–0.55 on C# projects [@gnieciak2025large, p. 10]; CASTLE score 977 for GPT-o3-mini vs 661 for the best non-LLM tool [@dubniczky2025castle, p. 11]. On function-level synthetic suites, CodeQL has higher accuracy than the best LLM on all three datasets [@khare2025understanding, p. 9]. At repository level, LLMs detect more CVEs but mark up to 77.4% of functions [@zhou2024comparison, p. 7]. General coding agents reach far higher recall than SAST [@li2026llm, p. 7; @li2026llm, p. 9]. deininger2026open scores both families on the same 1549 PrimeVul functions. Seven of eight zero-shot LLMs (balanced accuracy 0.604–0.676) score above the best lightweight SAST configuration (Flawfinder 0.589, Cppcheck up to 0.592; Semgrep 0.501–0.514) [@deininger2026open, p. 7; @deininger2026open, p. 10]. At the natural 1:44 prevalence, however, Flawfinder and Semgrep are more precise than every LLM [@deininger2026open, p. 8; @deininger2026open, p. 10]. Its SAST arm has no CodeQL, because isolated functions cannot be built [@deininger2026open, p. 10]. [I] The family's main weakness is that each study uses its own targets and scoring, so the papers measure different things (see §3.5).

**B. LLM vs fine-tuned DL/PLM.** On random-split Big-Vul, fine-tuned small models clearly beat prompted ChatGPT (F1 94% vs 29%) [@fu2023chatgpt, p. 4]. Under realistic splits all models collapse [@ding2025vulnerability, p. 7; @chakraborty2024revisiting, p. 7]. The only multilingual comparison finds that the winner depends on class balance [@shu2026evaluating, p. 17; @shu2026evaluating, p. 40]. Two pass-2 studies add:
- On unpaired PrimeVul functions, a fine-tuned 125M CodeBERT beats all eight zero-shot LLMs (balanced accuracy 0.765 vs ≤ 0.711) [@deininger2026open, p. 11; @deininger2026open, p. 17]. With a default 0.5 decision threshold, the same detector looks like an always-safe classifier [@deininger2026open, p. 11].
- On 2025 CVEs (VentiVul), trained DL detectors reach F1 3.47–8.65 and four open LLMs ≤ 32B reach conservative F1 0.79–5.36 [@lu2025lab, p. 13; @lu2025lab, p. 14]. [I] Both are close to the all-positive F1 of about 3.87%.

[I] This family inherits the label noise and leakage of Big-Vul-type data (§5, W2). Its results also depend on the decision threshold and the test prevalence (C1, C5, C8).

**B2. SAST vs classical ML/DL without an LLM.** tashenova2026real is the only PHP study in the corpus. On real WordPress plugin CVEs, an unnamed in-house intra-procedural lexical taint analyser detects 1.7–1.8% of vulnerabilities [@tashenova2026real, p. 9]. The authors say this low recall reflects "that implementation rather than taint analysis in general" [@tashenova2026real, p. 13] [A]. The best learned model reaches macro-F1 0.601, and no neural model leads in any of six settings [@tashenova2026real, p. 8]. [I] The paper says nothing about LLMs and cannot stand for established PHP SAST tools.

**C1. Hybrid detection (LLM inside the analyser).** IRIS doubles CodeQL's detections on CWE-Bench-Java (55 vs 27 of 120), with AvgFDR 84.82% vs 90.03% [@li2024iris, p. 8]. Only GPT-4 lowers FDR below CodeQL; smaller LLMs worsen it [@li2024iris, p. 10]. RepoAudit reports 78.43% precision [@guo2025repoaudit, p. 8]. Both look much weaker in li2026llm's independent re-evaluation (§4, C2 and C6).

**C2. Hybrid false-positive filtering.** The industrial LLM4PFA hybrid removes 94–98% of false alarms while keeping 75–88% of real bugs [@du2026reducing, p. 8]. The best agent configuration cuts OWASP FPR from 98.3% to 6.3% [@xiong2026sifting, p. 12] but drops 22.25% of true vulnerabilities [@xiong2026sifting, p. 18]. [I] This is the most consistent benefit in the corpus, but it is a trade-off, not a free gain (§3.9, G7).

**D. Agentic/reasoning LLMs.** Thinking mode raises F1 mainly through recall (0.31 → 0.41) at 2.7–4.4× the energy [@tan2026think, p. 6; @tan2026think, p. 10]. A four-call self-revision matches the multi-agent pipeline on P-C, so much of the agent gain is extra inference budget [@tan2026think, p. 11] [A]. ReAct agents give the best pairwise accuracy with GPT-4o models, but it stays ≤20.17% [@yildiz2025benchmarking, p. 6].

**E. Benchmark realism.** Manual audits find only 39–65% of vulnerable labels correct in BigVul, Devign and DiverseVul [@risse2025top, p. 8], and 24–36% in CodeXGLUE/Devign and VulnPatchPairs [@ding2025vulnerability, p. 4]. A word-count classifier reaches F1 0.86 on BigVul [@risse2025top, p. 11]. Statement-level scoring halves LLM F1 [@ahmed2026secvuleval, p. 8]. The pass-2 papers add three things:
- **Label audit outside C/C++.** An expert review finds only 48.8% of cleaned positive WordPress-PHP labels genuine (single annotator, n = 400) [@tashenova2026real, p. 11]. A one-feature token-count baseline matches or beats TF-IDF Random Forest in 4 of 6 settings [@tashenova2026real, p. 8].
- **Temporal separation.** VentiVul uses CVEs disclosed from May 2025, with the sample size fixed before collection [@lu2025lab, p. 4].
- **Realistic prevalence.** deininger re-scores all detectors at PrimeVul's natural 1:44 ratio [@deininger2026open, p. 8].

**F. Surveys and reviews.** Two SLRs and one narrative survey describe a field dominated by function-level C/C++ classification on noisy datasets [@kaniewski2026systematic, p. 26; @zhou2025large, p. 18; @sheng2025llms, p. 20]. A second narrative review, qin2026review, is discussed below. None of the four pools effect sizes. kaniewski2026systematic excludes studies that only post-process tool output [@kaniewski2026systematic, p. 8], so it does not cover family C2.

qin2026review is a single-author narrative review with 32 references and no search protocol [@qin2026review, p. 14]. Its quantitative claims re-report ding2025vulnerability and gnieciak2025large [@qin2026review, p. 12], so it is not independent support for either. It concludes that SAST is "usually more stable" within rule coverage [@qin2026review, p. 12] [A]. [I] Its only head-to-head source, however, found LLMs above SAST on F1 [@gnieciak2025large, p. 10]. We use qin2026review only to position our review.

## 3. Comparable results

Numbers are compared only where dataset, metric and setup match.

| Comparison | Dataset / metric | Verdict |
|---|---|---|
| 3.1 CodeQL on OWASP Benchmark (khare vs xiong) | OWASP Java; P/R/F1 | **Comparable** (different sample size) |
| 3.2 PrimeVul pairs (ding, tan, yildiz) | PrimeVul-derived pairs; P-C / pAcc | **Partly comparable** |
| 3.3 Big-Vul F1 (fu, ding, chakraborty, risse, lu) | "Big-Vul"; F1 | **Not comparable** |
| 3.4 CodeQL on CWE-Bench-Java (li2024iris vs li2026llm) | Java CVEs; recall | **Partly comparable** |
| 3.5 LLM-vs-SAST headline scores | different units and metrics | **Not comparable** |
| 3.6 LLM filtering of SAST alarms (du vs xiong) | different alarms and metrics | **Not numerically comparable** |
| 3.7 Unpaired PrimeVul functions (deininger) vs PrimeVul pairs (ding, tan, yildiz) | same source dataset; different unit, prevalence and metric | **Not comparable; do not pool** |
| 3.8 Detection at realistic prevalence (deininger at 1:44, lu at 1.97%) | different datasets; each scored against its own trivial baseline | **Not numerically comparable; same direction** |

**3.1 CodeQL on OWASP (comparable).** khare reports CodeQL P 0.58, R 0.96, F1 0.72 on a 1,000-snippet balanced OWASP sample [@khare2025understanding, p. 9]. xiong reports P 60.3%, R 97.0%, F1 74.4% on the full 2,740-case OWASP v1.2 [@xiong2026sifting, p. 11]. [I] Two independent groups agree within about 2 points. This is the only cross-paper SAST figure we can treat as replicated. Both describe a high-recall, low-precision tool (FPR 68.2% [@xiong2026sifting, p. 11]) whose F1 is near the always-vulnerable value of 0.667 on balanced data.

**3.2 PrimeVul pairs (partly comparable).** All three studies use pairs of vulnerable and patched functions drawn from PrimeVul:
- ding: GPT-4 CoT P-C 12.94% on 564 test pairs, below a random reference of 22.70% [@ding2025vulnerability, p. 9].
- tan: best non-agent P-C 22.5% on 435 pairs with open models [@tan2026think, p. 6]; self-revision 24.7 on 193 pairs [@tan2026think, p. 11].
- yildiz: GPT-4o/4o-mini pAcc 1.02–20.17% on 879 CVE pairs from JITVul, with repository context [@yildiz2025benchmarking, p. 6].

The pair subsets, models, context and dates differ. [I] The direction agrees: GPT-class and open LLMs stay at or below the ~25% ceiling that independent random labelling can reach. One outlier exists: DeepSeek-Coder-V2 with dependency augmentation reaches pAcc 69.24, reported in an appendix only [@yildiz2025benchmarking, p. 15]. All three use one dataset family, so this is related evidence, not independent replication. deininger2026open also uses PrimeVul but scores single, unpaired functions, so it is kept out of this comparison (§3.7). lu2025lab's PACC values on VentiVul pairs (all < 6%) [@lu2025lab, p. 13] come from a different dataset. [I] They point the same way: a random labeller would reach up to 25% PACC.

**3.3 Big-Vul F1 (not comparable).** Reported F1 on "Big-Vul" varies widely:
- CodeBERT: 87% [@fu2023chatgpt, p. 4] vs 62.88% [@ding2025vulnerability, p. 7].
- Replicated LineVul: 90% [@chakraborty2024revisiting, p. 6].
- LineVul with its original pipeline: 91.00 [@lu2025lab, p. 12]. lu used the original authors' code and recommended settings [@lu2025lab, p. 8].
- Literature SOTA (DeepDFA): 96.46% [@risse2025top, p. 7].
- Word-count baseline: 0.86 [@risse2025top, p. 11].

Splits, preprocessing and de-duplication differ. Neither lu nor ding explains the 28-point gap between their in-distribution CodeBERT/LineVul values (contradiction C7). [I] A spread of about 25–28 points for one model on one named dataset means Big-Vul F1 values should be cited only as a range. Because a word-count baseline reaches 0.86, high Big-Vul F1 is not evidence of vulnerability understanding.

**3.4 CodeQL on CWE-Bench-Java (partly comparable).** CodeQL detects 27 of 120 CVEs (22.5%) in the IRIS paper [@li2024iris, p. 8] and has 14.19% recall on li2026llm's Java set [@li2026llm, p. 9]. That set mixes a Maven-only CWE-Bench-Java subset with 50 JLeaks resource leaks [@li2026llm, p. 5]. [I] Both values are low, and the gap is plausibly due to the different CWE mix and CodeQL versions.

**3.5 LLM-vs-SAST headline numbers (not comparable).** gnieciak counts LLM findings as true positives even when the line or column is wrong, which SAST tools are not allowed [@gnieciak2025large, p. 6]. dubniczky uses a severity-weighted score [@dubniczky2025castle, p. 10]. khare uses function-level accuracy on balanced sets [@khare2025understanding, p. 9]. zhou2024 uses CVE detection ratio and marked-function ratio [@zhou2024comparison, p. 5]. li2026llm uses recall on known CVEs and SFDR on new code [@li2026llm, p. 11]. deininger2026open scores LLMs and SAST on identical functions with identical metrics (balanced accuracy and precision at 1:44) [@deininger2026open, p. 10]. Within that one study, the comparison is like-for-like. Its SAST arm is lightweight, though: Flawfinder, Cppcheck and Semgrep, with no CodeQL [@deininger2026open, p. 10]. [I] These six studies cannot be pooled or ranked against each other. tashenova2026real reports macro-F1 on PHP for a bespoke analyser [@tashenova2026real, p. 8] and does not add to this comparison.

**3.6 False-positive filtering (not numerically comparable).** du measures removal of false alarms on 433 industrial alarms of general bug types [@du2026reducing, p. 8]. xiong measures residual FPR and TP miss rate on OWASP and 100 sampled alerts [@xiong2026sifting, p. 12; @xiong2026sifting, p. 18]. Only the qualitative pattern can be compared (§3.9, G7).

**3.7 Unpaired PrimeVul functions vs PrimeVul pairs (not comparable; do not pool).** The two designs differ as follows:
- **deininger** samples 1549 single functions (35.4% vulnerable) from the PrimeVul test split [@deininger2026open, p. 4]. It reports balanced accuracy 0.511–0.711 for LLMs and 0.765 for fine-tuned CodeBERT [@deininger2026open, p. 7; @deininger2026open, p. 11; @deininger2026open, p. 17].
- **ding, tan and yildiz** score both members of each vulnerable/patched pair together (§3.2).

The unit, prevalence and metric all differ. [I] Balanced accuracy on single functions and pair-wise correctness answer different questions. The first asks whether a detector ranks vulnerable functions above safe ones. The second asks whether it notices the fix. So "fine-tuned CodeBERT beats all LLMs" (deininger) and "GPT-4 beats fine-tuned models on pairs" (ding) are not a numerical contradiction; C1 discusses them. Even inside one study, yildiz's F1 drops from ~49–65% on balanced pairs to 5.41–12.21% on non-paired PrimeVul [@yildiz2025benchmarking, p. 7]. deininger's PrimeVul test split (24,788 functions, 549 vulnerable) also differs from the split recorded by ding (695 vulnerable / 25,216 benign) [@deininger2026open, p. 4; @ding2025vulnerability, p. 6]. deininger explains this only as "after loading".

**3.8 Detection at realistic prevalence (not numerically comparable; same direction).** Two studies score detectors at about 2% prevalence against a trivial baseline:
- **deininger** (PrimeVul, 1:44 ≈ 2.2%): every LLM's precision is 2.3–3.8% in the first epoch and 2.8–4.6% in the budget-matched epoch, vs 2.21% for flag-all [@deininger2026open, p. 8; @deininger2026open, p. 17].
- **lu** (VentiVul, 1.97% [I]): trained DL reaches F1 3.47–8.65, and 7 of 12 LLM conservative F1 values fall below the all-positive F1 of about 3.87% [@lu2025lab, p. 13; @lu2025lab, p. 14].

The datasets, metrics (precision vs F1) and models differ (frontier and open LLMs vs open LLMs ≤ 32B). [I] Both show LLMs only slightly above, or below, a classifier that flags everything.

### 3.9 Agreements / converging evidence

Numbering follows the "Agreements" section of `evidence-matrix.md`.

- **G1. Realistic evaluation collapses reported performance (strong).** Several studies show it:
  - DL precision falls to 1–10% on Real-Vul [@chakraborty2024revisiting, p. 7].
  - Code-LM F1 falls from 62.88–68.26% (BigVul) to 18.05–21.43% within PrimeVul and 1.91–5.82% cross-dataset [@ding2025vulnerability, p. 7].
  - LLM accuracy is 10.5% lower on real-world than synthetic data [@khare2025understanding, p. 5].
  - GPT-4o line-level F1 drops from 0.6641 to 0.3450 on 2024–25 code [@shu2026evaluating, p. 39].
  - Statement-level scoring halves F1 [@ahmed2026secvuleval, p. 8].
  - Pass 2: on post-May-2025 CVEs at 1.97% prevalence, DL F1 is 3.47–8.65, and 7 of 12 LLM conservative F1 values fall below the all-positive F1 of 3.87% [@lu2025lab, p. 13; @lu2025lab, p. 14].
  - Pass 2: at 1:44 prevalence, LLM precision is 2.3–4.6% vs 2.21% for flag-all [@deininger2026open, p. 8; @deininger2026open, p. 17].
  - Pass 2: on real WordPress PHP CVEs, the best macro-F1 is 0.601 [@tashenova2026real, p. 8].

  The surveys agree [@kaniewski2026systematic, p. 39; @sheng2025llms, p. 20].
- **G2. Benchmark labels are noisy (strong).** Two independent audits find 39–65% [@risse2025top, p. 8] and 24–36% [@ding2025vulnerability, p. 4] of vulnerable labels correct. ReVeal has 15% label inconsistency [@chakraborty2024revisiting, p. 3]. The 25% BigVul figure is Chen et al.'s, reproduced by Ding [@ding2025vulnerability, p. 4]; it is not an independent estimate. Pass 2 adds a third audit, in a new language: only 48.8% of cleaned positive WordPress-PHP labels are genuine (single annotator, n = 400) [@tashenova2026real, p. 11].
- **G3. Prompted LLMs over-flag and cannot separate vulnerable from patched code (moderate).**
  - GPT-4 two-shot calls both versions vulnerable in 71.63% of pairs [@ding2025vulnerability, p. 9].
  - "Both vulnerable" accounts for 40–95% of LLM failures [@yildiz2025benchmarking, p. 8].
  - The dual-agent design flags 88.2% of functions [@tan2026think, p. 7].
  - Several of khare's best F1 rows are "always vulnerable" outputs [@khare2025understanding, p. 16].
  - Frontier models over-flag CWE-476/416/190 [@ahmed2026secvuleval, p. 13] [A].

  [I] ding, yildiz and tan share PrimeVul, so this is partly one dataset family.
- **G4. SAST recall is low on real code and high only on synthetic suites (moderate).** On real code:
  - Best single SAST tools detect 30.0–44.4% of CVEs, and many detect 0% [@zhou2024comparison, p. 6].
  - CodeQL recall is 6.00–34.29% on C/C++ and 14.19% on Java [@li2026llm, p. 7; @li2026llm, p. 9].
  - CodeQL finds 27/120 on CWE-Bench-Java [@li2024iris, p. 8].
  - On CASTLE, CodeQL reaches 29% and the SAST average is 23% [@dubniczky2025castle, p. 12].

  On synthetic suites, CodeQL reaches accuracy 0.94 on Juliet Java [@khare2025understanding, p. 9].
- **G5. CodeQL on OWASP replicates across groups (moderate).** See §3.1 [@khare2025understanding, p. 9; @xiong2026sifting, p. 11].
- **G6. Missing context is the shared failure cause (moderate).**
  - All 151 truly vulnerable audited functions need context beyond the function [@risse2025top, p. 9].
  - LLMs identify required context in ≤41.33% of cases per context type [@ahmed2026secvuleval, p. 9].
  - Global context is the main failure cause on real C/C++ [@khare2025understanding, p. 7] [A].
  - Incomplete API modelling explains 108/108 RepoAudit (GPT-5.4) misses [@li2026llm, p. 7], and 14.60% of all FPs come from truncated inter-procedural context [@li2026llm, p. 15].
- **G7. LLM false-alarm filtering trades large FP reduction for lost true positives (moderate).** Evidence: du2026reducing reaches 94–98% false-alarm removal with real-bug recall of 0.75–0.88 [@du2026reducing, p. 8]; xiong2026sifting cuts FPR to 6.3% but misses 22.25% of true vulnerabilities [@xiong2026sifting, p. 12; @xiong2026sifting, p. 18]. du covers non-security bug classes, evaluates its authors' own method and has Tencent-affiliated authors [@du2026reducing, p. 1]. Strength is therefore moderate.
- **G8. Prompt-only LLMs trail adapted models (moderate).**
  - Prompted ChatGPT lags fine-tuned models on Big-Vul [@fu2023chatgpt, p. 4].
  - GPT-3.5 prompting detects 3.7–23.2% vs 89.2% for fine-tuned CodeBERT [@zhou2024comparison, p. 10].
  - Prompt-only LLMs are near chance on REEF, and only fine-tuned GPT-4o with few-shot stands out [@shu2026evaluating, p. 17].
- **G9. LLM cost far exceeds SAST cost and varies by orders of magnitude (moderate).** SAST runs in minutes with no token cost, while RepoAudit averages $172.77 per project [@li2026llm, p. 16]. Alarm filtering costs cents per alarm [@du2026reducing, p. 8; @xiong2026sifting, p. 17]. Instruction tuning GPT-4o costs about 15× a local PLM training run [@shu2026evaluating, p. 42].
- **G10. Trivial baselines are competitive (moderate).** Three studies show this:
  - A one-feature token-count baseline matches or beats TF-IDF Random Forest in 4 of 6 settings and is within 0.006 of the best neural model [@tashenova2026real, p. 8].
  - Always-vulnerable F1 is 0.523, against LLM F1 of 0.405–0.615 [@deininger2026open, p. 7].
  - The all-positive F1 of 3.87% is above most LLM F1 values on VentiVul [@lu2025lab, p. 14].

  shu2026evaluating also reports all-vulnerable and all-clean dummy baselines [@shu2026evaluating, p. 11]. [I] Few papers report such baselines, and most headline numbers are never compared with one (§5, W1).
- **G11. Cost per true positive (moderate, single study).** Each true positive costs USD 0.003 (Gemma-3-4B) to 0.212 (Claude Sonnet 5) and 3.7–119.6 kJ at 1:44 prevalence [@deininger2026open, p. 8]. This excludes human triage of the 25.6–41.9 false positives that come with each true one [@deininger2026open, p. 8]. The kJ per TP for Gemma, Qwen and Llama come from FLOP estimates, not measured energy [@deininger2026open, p. 14] (§5, W6).

## 4. Contradictions

**C1. Fine-tuned models vs GPT-4: fu2023chatgpt vs ding2025vulnerability.**
- Claim A: fine-tuned AIBugHunter (F1 94%) and CodeBERT (87%) far outperform prompted gpt-4 (29%) [@fu2023chatgpt, p. 4].
- Claim B: GPT-4 CoT has a higher P-C (12.94%) than every fine-tuned model (≤3.01%) [@ding2025vulnerability, p. 9].
- Differences:
  - metric: F1 vs pairwise correctness;
  - data: noisy random-split Big-Vul at 1:20 vs de-duplicated, time-split PrimeVul pairs;
  - time: 2023 vs 2024 GPT versions.
- Ding's own BigVul rows (F1 62.88–68.26%) agree with Fu's direction [@ding2025vulnerability, p. 7].
- [I] Explanation: fine-tuned models probably exploit dataset artefacts that random splits reward and paired, de-duplicated tests remove [@risse2025top, p. 11]. On pairs, every model is below the random reference (22.70%), so neither side shows real detection skill there, and the reversal says more about the benchmark than about the model families.
- Pass 2: on 1549 unpaired PrimeVul functions, a fine-tuned CodeBERT-PrimeVul beats all 8 zero-shot LLMs (balanced accuracy 0.765 vs ≤ 0.711) [@deininger2026open, p. 11; @deininger2026open, p. 17]. With an argmax decision rule, the same detector looks like an always-safe classifier (0.500) despite ROC-AUC 0.845 [@deininger2026open, p. 11].
- [I] A conservative threshold would fit Ding's fine-tuned models labelling both pair members benign in 84–88% of pairs [@ding2025vulnerability, p. 9]. Unpaired and pair-wise results must not be pooled (§3.7).

**C2. RepoAudit: guo2025repoaudit vs li2026llm.**
- Claim A: 40 TP / 11 FP (78.43% precision) on 15 C/C++ projects, all 21 known bugs reproduced, $2.54 and 0.44 h per project [@guo2025repoaudit, p. 7; @guo2025repoaudit, p. 8].
- Claim B: in li2026llm, RepoAudit (Sonnet 3.5) detects 0 of 110 known C/C++ vulnerabilities [@li2026llm, p. 7]. On real projects it has 92.77% SFDR [@li2026llm, p. 11] and costs $172.77 on average, up to $1,247.66 per project [@li2026llm, p. 16].
- Differences:
  - targets: prior tools' bug reports vs ReposVul CVEs;
  - code version: older commits vs current HEAD (the five overlapping Linux/ImageMagick modules are in li's real-world set only);
  - metric: precision on own reports vs recall/SFDR;
  - labeller: authors vs Codex;
  - scale: avg 251 KLoC vs multi-million-LOC modules.
- [I] Explanation: RepoAudit depends on source/sink API coverage. li2026llm records zero-token runs and 108/108 misses due to API modelling [@li2026llm, p. 7; @li2026llm, p. 16], so the tool may perform well only on targets matching its built-in specifications. Neither paper alone settles this.

**C3. "LLMs beat SAST" vs "SAST beats LLMs" vs repository level.**
- Claim A: LLMs win on 10 small C# projects [@gnieciak2025large, p. 10] and on CASTLE C micro-programs [@dubniczky2025castle, p. 11].
- Claim B: CodeQL beats the best LLM in accuracy on OWASP, Juliet Java and Juliet C/C++ [@khare2025understanding, p. 9].
- Claim C (repository level): LLMs detect more but mark up to 77.4% of functions [@zhou2024comparison, p. 7]. General agents reach the highest recall, while specialised LLM detectors and SAST both have near-zero recall on some CWEs and 75–100% SFDR [@li2026llm, p. 7; @li2026llm, p. 11].
- Differences: language (C#, C, Java), unit (project, program, function, repository), scoring (lenient LLM location rule in gnieciak [@gnieciak2025large, p. 6]; the CASTLE prompt reveals the scoring rule to the LLM [@dubniczky2025castle, p. 9]), and synthetic vs real code.
- [I] Explanation: synthetic suites match SAST rule sets, while small self-contained programs fit inside an LLM's context. Real repositories defeat both families through missing API and context models (G4, G6). The answer depends on setting and metric, so there is no single winner.
- Pass 2: deininger scores LLMs and SAST on the same 1549 PrimeVul functions:
  - LLMs lead on balanced accuracy [@deininger2026open, p. 7; @deininger2026open, p. 10].
  - At 1:44 prevalence, Flawfinder (6.2–13.4%) and Semgrep (26.0%, CI 5.7–66.9) are more precise than every LLM (2.3–4.6%) [@deininger2026open, p. 8; @deininger2026open, p. 10].
  - Cppcheck's precision is within the LLM range [@deininger2026open, p. 10].
- [I] The two families fail in opposite directions: LLMs over-flag, while SAST finds little. Which family "wins" therefore depends on the metric. This fits the pattern "LLMs higher recall, lower precision".

**C4. Does reasoning reduce false positives?**
- Claim A: reasoning models "consistently produced fewer false positives" [@dubniczky2025castle, p. 14]. RepoAudit precision rises to 82.35–88.46% with reasoning backbones [@guo2025repoaudit, p. 16].
- Claim B:
  - In CASTLE's own table, DeepSeek R1 has 166 FP vs GPT-4o's 116 [@dubniczky2025castle, p. 11].
  - Thinking mode raises F1 through recall with unchanged accuracy, and its F1 benefit turns negative under dual- and multi-agent designs [@tan2026think, p. 6; @tan2026think, p. 8].
  - Reasoning LLMs are near chance on REEF (Acc 0.52–0.53) [@shu2026evaluating, p. 37].
- Differences: OpenAI o-series vs open reasoning models; micro-benchmark and repository agent vs balanced function pairs; FP count vs F1 and accuracy.
- [I] Explanation: the claim holds for some proprietary reasoning models in some settings and does not generalise to "reasoning" as such.
- Pass 2, against: reasoning lowers DeepSeek-V3.2's specificity from 0.52 to 0.37 [@deininger2026open, p. 17; @deininger2026open, p. 20]. In the same study it raises the balanced accuracy of the frontier models [@deininger2026open, p. 17]. [I] The effect of reasoning on false positives is model-dependent.

**C5. Class balance flips the ranking (shu2026evaluating, internal).**
- Claim A: on balanced REEF, fine-tuned GPT-4o + few-shot beats CodeT5P (Acc 0.7196 vs 0.6037; MCC 0.4360 vs 0.2860) [@shu2026evaluating, p. 17].
- Claim B: on the imbalanced (~17% vulnerable) test, PLMs win (UniXcoder F1 0.4626, CodeT5P MCC 0.3627 vs GPT-4o F1 0.4010, MCC 0.2774) [@shu2026evaluating, p. 40; @shu2026evaluating, p. 41].
- yildiz shows the same sensitivity: F1 falls from ~49–65% on balanced pairs to 5.41–12.21% on non-paired PrimeVul [@yildiz2025benchmarking, p. 7].
- Pass 2 adds two more cases:
  - deininger's precision ranking at 1:44 differs from its balanced-accuracy ranking [@deininger2026open, p. 8].
  - In tashenova, changing how negatives are drawn flips the majority class and the direction in which the same Random Forest fails [@tashenova2026real, p. 9].
- [I] Explanation: LLMs flag positives more liberally, which balanced sets reward. Rankings from balanced benchmarks should not be carried over to deployment, where vulnerable code is rare.

**C6. Hybrid IRIS: original vs independent evaluation.**
- Claim A: IRIS+GPT-4 beats CodeQL on 120 Java CVEs (55 vs 27 detected; AvgFDR 84.82% vs 90.03%) [@li2024iris, p. 8].
- Claim B: on 15 real-world Java projects, IRIS (GPT-4) has 97.80% SFDR vs 77.00% for CodeQL [@li2026llm, p. 12].
- Differences: known CVEs vs new code, detections vs SFDR, CodeQL-protocol FDR vs Codex-labelled sampling.
- [I] Explanation: hybrids may raise recall on benchmark CVEs while adding noise on unseen projects. The comparison is not like-for-like, so the tension stays open.

**C7. Same model, same benchmark, different in-distribution score: lu2025lab vs ding2025vulnerability.**
- Claim A: LineVul (CodeBERT) trained and tested on BigVul reaches F1 91.00 [@lu2025lab, p. 12].
- Claim B: CodeBERT trained and tested on BigVul reaches F1 62.88 [@ding2025vulnerability, p. 7].
- Differences: neither paper explains the 28-point gap. lu used LineVul's original pipeline and recommended settings [@lu2025lab, p. 8], whereas ding trains its own set of code LMs [@ding2025vulnerability, p. 7].
- [I] Explanation: likely split and preprocessing differences. In-distribution BigVul numbers are not comparable across papers (§3.3).

**C8. Does a time-split fine-tuned detector survive? deininger2026open vs lu2025lab.**
- Claim A: CodeBERT-PrimeVul keeps balanced accuracy 0.765 on PrimeVul's chronologically later test split [@deininger2026open, p. 3; @deininger2026open, p. 11]. At 1:44 prevalence this corresponds to F1 ≈ 0.15 (our calculation from reported TPR and precision).
- Claim B: DL trained on BigVul, ICVul, Devign or Juliet falls to F1 3.47–8.65 on post-May-2025 VentiVul [@lu2025lab, p. 13].
- Differences:
  - test data: PrimeVul functions with CVEs from 2008–2022 [@deininger2026open, p. 24] vs VentiVul 2025 CVEs scored per function across whole files [@lu2025lab, p. 4];
  - training data: PrimeVul's own training split vs older, noisier benchmarks;
  - threshold policy: validation-tuned [@deininger2026open, p. 11] vs the original implementations' settings [@lu2025lab, p. 8];
  - metric: balanced accuracy vs F1.
- [I] Explanation: unresolved. A detector trained on cleaner data from the same source, with a tuned threshold, may hold up better than detectors trained on other benchmarks. Neither study tests this directly.

## 5. Methodological weaknesses across the field

- **W1. Trivial baselines rarely reported.** On a 50/50 set, "flag everything" scores F1 0.667, so balanced-data F1 near that value shows no skill. Examples:
  - shu's DummyClf_vul scores 0.6693 against a best of 0.7075 [@shu2026evaluating, p. 17].
  - tan's best F1 is 0.665–0.666 [@tan2026think, p. 7; @tan2026think, p. 11].
  - All of yildiz's GPT F1 values (48–66) are at or below it [@yildiz2025benchmarking, p. 6].
  - khare's best-per-dataset F1s include always-vulnerable rows [@khare2025understanding, p. 16].

  Pass 2 shows the same problem at other prevalences (G10):
  - deininger: the best LLM F1 (0.615) is 0.092 above always-vulnerable (0.523), and Qwen3-Coder-30B (0.405) is below it [@deininger2026open, p. 7].
  - tashenova: a token-count baseline is within 0.006 of the best neural model [@tashenova2026real, p. 8].
  - lu reports no trivial baseline. [I] By our calculation, 7 of its 12 LLM conservative F1 values fall below the all-positive F1 of about 3.87% [@lu2025lab, p. 14].

  [I] Only shu, deininger and tashenova report trivial-classifier baselines (3 of 19 primary studies). ding reports a random reference only for pair-wise correctness [@ding2025vulnerability, p. 9]. tashenova's authors argue that detectors should be required to clear such baselines [@tashenova2026real, p. 13] [A].
- **W2. Label quality and leakage.** Problems include:
  - **Exact-copy leakage** from test to train reaches 12.7% (BigVul) and 18.9% (CVEFixes) [@ding2025vulnerability, p. 4]. Even plugin-grouped PHP folds contained duplicate groups spanning folds (166 / 151 groups) and 730 / 456 groups with contradictory labels before cleaning [@tashenova2026real, p. 4].
  - **Label quality** is low wherever it is audited: 39–65% [@risse2025top, p. 8], 24–36% [@ding2025vulnerability, p. 4] and 48.8% for PHP [@tashenova2026real, p. 11] of positive labels are correct. [I] tashenova's evaluated corpus also contains lower-tier labels, so its true label precision is probably lower still. Its authors argue that label quality, not architecture, is "the more plausible binding constraint" [@tashenova2026real, p. 12] [A].
  - **Contamination.** Benchmarks probably sit in LLM pre-training data [@kaniewski2026systematic, p. 30] [A]. deininger finds recall 7–15 points higher on pre-2020 than on 2021–2022 CVEs for better-balanced LLMs, which is consistent with memorisation [@deininger2026open, p. 24].
  - **Post-cutoff testing** is rare. Only xiong, li2026llm and lu test explicitly on code disclosed after the evaluated models' release [@xiong2026sifting, p. 15; @li2026llm, p. 5; @lu2025lab, p. 5]. lu notes that release-date separation cannot fully exclude contamination [@lu2025lab, p. 17]. shu adds a time split [@shu2026evaluating, p. 39].
- **W3. LLM-as-labeller.** li2026llm labels real-world warnings with Codex, a tool it also evaluates (94.36% accurate on 621 validated warnings) [@li2026llm, p. 11]. tan's LLM judge rates explanations higher in ways humans corroborate only for informativeness [@tan2026think, p. 8]. [I] Self-labelling can favour the labelling model.
- **W4. Unequal scoring between LLMs and SAST.** gnieciak applies a lenient location rule only to LLMs [@gnieciak2025large, p. 6]. CASTLE's LLM prompt states the reward and penalty scheme [@dubniczky2025castle, p. 9]. SAST tools run on default configurations [@gnieciak2025large, p. 8], and khare tests CodeQL only on synthetic data [@khare2025understanding, p. 7]. [I] These choices favour LLMs in two studies and SAST in one.
- **W5. Single runs, no statistics.** Most studies report one run of non-deterministic models without variance (§1). Examples:
  - zhou2024's results rest on about 8–10 test CVEs per language [I] [@zhou2024comparison, p. 6].
  - xiong's real-world samples are 50 alerts each [@xiong2026sifting, p. 13].
  - shu chooses the best of ~30 configurations post hoc [@shu2026evaluating, p. 17].
  - lu runs each LLM once and does not report DL run counts [@lu2025lab, p. 8].
  - tashenova uses a single seed [@tashenova2026real, p. 7].

  deininger shows why this matters. A reworded prompt moves balanced accuracy by up to 0.088 and changes which model wins [@deininger2026open, p. 19; @deininger2026open, p. 20]. Absolute scores shift by up to 0.06 between measurement epochs seven weeks apart [@deininger2026open, p. 20].
- **W6. Little cost reporting; energy figures of mixed provenance.** Twelve of 19 primary studies report no monetary cost (§1). Where cost is measured it is decisive: up to $1,247.66 per project [@li2026llm, p. 16]. Only deininger reports cost per true positive (G11), and it excludes human triage [@deininger2026open, p. 8]. Its energy figures mix three sources:
  - Frontier-model energy is a FLOP estimate that assumes 100B active parameters [@deininger2026open, p. 7].
  - The kJ per TP for Gemma, Qwen and Llama come from FLOP estimates (64, 40 and 944 J per task), not from measured energy [@deininger2026open, p. 8; @deininger2026open, p. 14].
  - The FLOP estimator overstates measured batched energy by 5.4–16.9× [@deininger2026open, p. 14].

  [I] With measured single-request energy, our recalculation gives about 4.9 (Gemma), 8.8 (Qwen) and 34.9 (Llama) kJ per TP. The ordering among open models changes, but the gap to frontier models remains. Energy numbers should always state whether they are measured or estimated.
- **W7. Narrow scope.** Data are C/C++-biased and long-tailed, and 555 mappable CWEs appear in no analysed dataset [@kaniewski2026systematic, p. 34]. 87 studies build custom datasets and only nine datasets are reused in more than ten studies [@kaniewski2026systematic, p. 35]. Only one of 40 detection studies to March 2024 worked at repository level [@zhou2025large, p. 18]. PHP is covered by a single function-level study, which has no LLM arm and only a bespoke analyser [@tashenova2026real, p. 13].
- **W8. Three-way comparisons are rare.** [I] Two studies evaluate LLMs, SAST and DL together:
  - khare, whose SAST arm covers synthetic data only [@khare2025understanding, p. 7];
  - deininger, on identical PrimeVul functions with lightweight SAST and no CodeQL [@deininger2026open, p. 10], using CVEs from 2008–2022 that predate the models' training cutoffs [@deininger2026open, p. 24].

  zhou2024 compares fine-tuned and prompted LLMs with SAST but no classic DL detector [@zhou2024comparison, p. 4]. lu compares DL with LLMs but has no SAST arm, and tashenova compares SAST with ML/DL but has no LLM arm [@lu2025lab, p. 7; @tashenova2026real, p. 13].
- **W9. Preprint text vs version of record.** Fifteen published papers were analysed from arXiv copies (xiong2026sifting's copy is the formatted published article). lu2025lab was read as the arXiv v4 accepted manuscript of its JSS 2026 version [@lu2025lab, p. 1]. du2026reducing comes from a v1 with a placeholder header [@du2026reducing, p. 2], so it has the highest risk that numbers changed. zhou2025large's only LLM-vs-SAST study is the authors' own zhou2024comparison [@zhou2025large, p. 22], so it is not independent support.
- **W10. Independence.** [I] Several sources overlap:
  - guo and li2026llm share five C/C++ modules.
  - ding, yildiz, tan and deininger all draw on PrimeVul.
  - Duplication figures reused elsewhere trace back to ding alone (critical review B).
  - qin2026review's quantitative claims re-report ding and gnieciak, so they add no independent support [@qin2026review, p. 12].
  - ICVul, one of lu's four training benchmarks, is the authors' own dataset [@lu2025lab, p. 3].
- **W11. Test prevalence rarely realistic.** Most test sets are balanced or close to it (W1), while vulnerable code is rare in practice. The pass-2 studies show what this hides:
  - Re-scored at PrimeVul's natural 1:44 ratio, LLMs raise 25.6–41.9 false positives per true one [@deininger2026open, p. 8].
  - At BigVul's 6% prevalence, DL accuracy of 87–94% hides F1 as low as 0.19 [@lu2025lab, p. 11].
  - tashenova draws negatives only from vulnerable plugins [@tashenova2026real, p. 3]. [I] Its prevalence is therefore 74.5% (Variant A) and 46.2% (Variant B), and the false-alarm rate in deployment is unknown.

  [I] Results from balanced sets should be re-scored at realistic prevalence before any deployment claim.

## 6. What this means for our research questions

Updated pass 2, 2026-11-12 (24 papers). The same answers appear in `RESEARCH-QUESTIONS.md`.

**RQ1 — effectiveness head-to-head.** No family wins across settings.
- **LLMs vs SAST.** Frontier LLMs beat SAST on small, self-contained code [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11]. CodeQL beats LLMs on synthetic function-level suites [@khare2025understanding, p. 9]. At project scale, general coding agents reach much higher recall than SAST (59.55% vs 0–34.29% on C/C++) [@li2026llm, p. 7], but most LLM detectors and SAST tools produce mostly false warnings [@li2026llm, p. 11].
- **Same functions, all three families.** On 1549 unpaired PrimeVul functions, seven of eight zero-shot LLMs beat lightweight SAST on balanced accuracy [@deininger2026open, p. 7; @deininger2026open, p. 10]. At the natural 1:44 prevalence, though, Flawfinder and Semgrep are more precise than every LLM. LLM precision there (2.3–4.6%) is barely above flag-all (2.21%) [@deininger2026open, p. 8; @deininger2026open, p. 17].
- **LLMs vs fine-tuned DL.** The ranking depends on dataset, class balance and decision threshold [@fu2023chatgpt, p. 4; @shu2026evaluating, p. 40; @deininger2026open, p. 11]. A fine-tuned CodeBERT beats all eight LLMs on the same unpaired PrimeVul functions (balanced accuracy 0.765 vs ≤ 0.711) [@deininger2026open, p. 11; @deininger2026open, p. 17]. All families are near or below chance on PrimeVul pairs [@ding2025vulnerability, p. 9; @tan2026think, p. 6].
- **Recent code.** On temporally separated 2025 CVEs at 1.97% prevalence, trained DL (F1 3.47–8.65) and four open LLMs ≤ 32B (0.79–5.36) both sit near the all-positive F1 of about 3.87% [I] [@lu2025lab, p. 13; @lu2025lab, p. 14].
- **PHP.** No LLM has been tested. A bespoke lexical taint analyser detects 1.7–1.8% of vulnerabilities, and ML reaches macro-F1 ≤ 0.601 [@tashenova2026real, p. 8; @tashenova2026real, p. 9].

**Strength: weak to moderate.** Most results come from single-run studies with incompatible metrics and no pooling. Only one study compares all three families on identical real functions, and its SAST arm is lightweight. The most robust pattern is "LLMs higher recall, lower precision" [I]. A second pattern [I] is that at realistic prevalence, LLMs show only a small margin over trivial baselines.

**RQ2 — evaluation setups.** Setup explains much of the disagreement. Sources of variation:
- label noise: 39–65% [@risse2025top, p. 8] and 48.8% for PHP [@tashenova2026real, p. 11] of positive labels correct;
- leakage, including duplicates and contradictory labels across folds [@ding2025vulnerability, p. 4; @tashenova2026real, p. 4];
- balanced vs realistic class ratios [@shu2026evaluating, p. 40; @yildiz2025benchmarking, p. 7; @deininger2026open, p. 8];
- missing trivial baselines, which are often competitive [@tashenova2026real, p. 8; @deininger2026open, p. 7; @lu2025lab, p. 14];
- temporal and cross-dataset shift [@lu2025lab, p. 12; @lu2025lab, p. 13];
- prompt wording and decision threshold, each of which can change the winner [@deininger2026open, p. 11; @deininger2026open, p. 20];
- synthetic vs real code [@khare2025understanding, p. 5];
- function vs statement granularity [@ahmed2026secvuleval, p. 8];
- custom datasets with inconsistent splits [@kaniewski2026systematic, p. 35]. The same model on the same named dataset can differ by 28 F1 points between papers [@lu2025lab, p. 12; @ding2025vulnerability, p. 7].

**Strength: strong** for label noise and the collapse under realistic evaluation, which are consistent across independent primary studies and two SLRs. **Moderate** for prompt and threshold sensitivity and for trivial baselines, which rest on fewer studies.

**RQ3 — hybrids, cost, explainability.**
- **Alarm filtering.** LLM filtering of SAST alarms removes most false alarms at under $0.20 per alarm but loses 12–25% of real bugs [@du2026reducing, p. 8; @xiong2026sifting, p. 18]. **Strength: moderate.**
- **Hybrid detection.** IRIS and RepoAudit beat SAST in the authors' own evaluations [@li2024iris, p. 8; @guo2025repoaudit, p. 8] but not in an independent project-scale study [@li2026llm, p. 7; @li2026llm, p. 12]. The gain depends on a strong LLM [@li2024iris, p. 10]. **Strength: weak/contested.**
- **Cost.** Costs range from cents to $1,247.66 per project, against minutes and no token cost for SAST [@li2026llm, p. 16]. deininger, which is not a hybrid study, gives the only cost per true positive at 1:44 prevalence: USD 0.003–0.212 and 3.7–119.6 kJ [@deininger2026open, p. 8]. These are compute costs only. They exclude human triage of the 25.6–41.9 false positives per true one [@deininger2026open, p. 8], and part of the energy values are FLOP estimates [@deininger2026open, p. 14]. Small open models can match a frontier model at a fraction of the cost (1/66) [@deininger2026open, p. 17]. Reasoning mode costs 4.5–12.1× more per task [@deininger2026open, p. 18]. **Strength: moderate (single study)** for cost per TP.
- **Explainability.** LLMs mislocate findings [@gnieciak2025large, p. 11] [A], and fluent explanations do not signal correctness [@tan2026think, p. 9].

**RQ4 — CWEs, languages, scale.**
- **CWEs.** LLMs do best on self-contained injection-style CWEs and worst on context-dependent and crypto/policy CWEs and on localising memory-safety bugs [@khare2025understanding, p. 7; @xiong2026sifting, p. 18; @shu2026evaluating, p. 30]. CodeQL is better on CWE-190 [@khare2025understanding, p. 8].
- **Scale.** LLM performance falls with function or file length [@ahmed2026secvuleval, p. 13; @li2026llm, p. 9].
- **Projects.** Results also vary by project: LineVul (BigVul) finds 76% of Chromium CVEs but none in Linux, while all LLMs cover Linux better [@lu2025lab, p. 13].
- **Languages.** Evidence is concentrated on C/C++ and Java [@kaniewski2026systematic, p. 28]. The only PHP evidence comes from tashenova, which tests no LLM and uses a bespoke analyser. There, learned models detect XSS (F1 up to 0.500) far better than SQLi (≤ 0.146) or RCE (≤ 0.085) [@tashenova2026real, p. 9].

**Strength: weak.** Per-CWE cells are small and per-CWE results diverge across studies. For example, khare finds LLMs beat CodeQL on CWE-476 [@khare2025understanding, p. 8], while ahmed reports over-flagging of it [@ahmed2026secvuleval, p. 13].

**RQ5 — open problems.** Recurring problems:
- verified, realistic, repository-level benchmarks with context [@zhou2025large, p. 19; @sheng2025llms, p. 25];
- trivial baselines and realistic prevalence (W1, W11);
- label quality, leakage and contamination control (W2) [@tashenova2026real, p. 12; @lu2025lab, p. 17];
- same-benchmark three-way comparisons beyond lightweight SAST and pre-cutoff function-level code (W8);
- independent labelling and statistics, including prompt sensitivity (W3, W5);
- cost reporting that includes triage, with clear energy provenance (W6);
- true-positive loss in filtering [@xiong2026sifting, p. 19];
- workflow integration: none of 58 reviewed studies was integrated into developer workflows [@zhou2025large, p. 19].

deininger's authors conclude that no method they tested (LLM, SAST or fine-tuned DL) is ready for independent function-level triage [@deininger2026open, p. 26] [A]. qin2026review lists similar open problems [@qin2026review, p. 13], but it is not independent of our sources.

**Strength: moderate** as a description of recurring limitations. [I] These are candidate gaps only. Novelty checks and gap specifics are in `gap-report.md` (standards §7).
