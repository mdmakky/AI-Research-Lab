# Overview

## What this research is about

Software often contains security bugs. A security bug that an attacker can use is called a **vulnerability**. Examples are SQL injection (an attacker smuggles database commands into an input field) and buffer overflows (a program writes past the end of a memory area).

There are three main ways to find vulnerabilities in source code without running it:

- **SAST tools.** SAST means static application security testing. These are programs such as CodeQL, Semgrep or Flawfinder. They scan code with hand-written rules.
- **Deep-learning (DL) detectors.** These are neural networks, such as LineVul or a fine-tuned CodeBERT, that learn from many examples of code labelled "vulnerable" or "safe".
- **Large language models (LLMs).** These are general AI models such as GPT-4, Claude or Llama. Since about 2023 people simply ask them whether a piece of code is vulnerable, or let them act as "agents" that explore a whole project.

A fourth group, **hybrids**, combines an LLM with a SAST tool. For example, the LLM can tell the SAST tool what to look for, or it can check the SAST tool's warnings and throw away false ones.

Published studies disagree about which approach works best. This project collected 24 papers and compared their evidence side by side. The goal was to find out which approach finds more real vulnerabilities, with fewer false alarms, at what cost, and how far the published numbers can be trusted.

## The five research questions in plain words

A **research question (RQ)** is the exact question a review tries to answer. This project has five.

1. **RQ1. Who wins?** When LLMs, SAST tools and DL detectors are tested on the same code, which one finds more vulnerabilities with fewer false alarms?
2. **RQ2. Why do studies disagree?** How do the test setups differ (test data, programming languages, vulnerability types, real or artificial code, data leaks), and do these differences explain the disagreements?
3. **RQ3. Do hybrids help?** Does combining an LLM with a SAST tool beat either one alone, and what does it cost in money, time and explainability?
4. **RQ4. Where does each approach work?** Which vulnerability types, programming languages and code sizes suit each approach?
5. **RQ5. What is still missing?** Which open problems block reliable, deployable LLM-based vulnerability detection?

## How to use this guide

The guide has five parts:

1. This **Overview**: the main findings, a map of all 24 papers, five papers to read first, and where studies disagree.
2. **Paper Summaries**: one brief of one to two pages per paper, in the same order as the paper map below. Each brief starts with a one-sentence takeaway.
3. **Research Gaps and Opportunities**: six open problems that a new study could address, each with a study a beginner could run.
4. **Glossary**: plain-language definitions of more than 30 terms.
5. **Appendices**: the full research report, the methodology comparison and the evidence matrix, for readers who want every detail.

**Evidence labels.** Every important statement carries a label:

- **[V] Verified**: we checked it against the paper's own tables or results.
- **[A] Author claim**: the authors say it, but we cannot check it ourselves.
- **[I] Interpretation**: our own reasoning across papers. Treat it as an informed opinion.

Numbers without a label are [V] from the cited page.

**Citations.** A citation looks like [@deininger2026open, p. 8]. The part after the @ is the paper's key: first author's surname, year and the first word of the title. "p. 8" is the page of the PDF file we read, which can differ from the page number printed in the journal.

**Evidence strength.** Strong means several independent studies agree and their designs are sound. Moderate means a sound design but one study or few data. Weak means small or unclear samples, design problems, or unreplicated preprints.

**Peer review and preprints.** A **peer-reviewed** paper was checked by independent experts before publication. A **preprint** was posted online without that check. Points to keep in mind:

- zhou2024comparison is a **preprint, not peer-reviewed** [@zhou2024comparison, p. 1].
- lu2025lab is published in the Journal of Systems and Software (2026). Our copy is the arXiv accepted manuscript, so its page numbers follow that copy [@lu2025lab, p. 1].
- li2024iris (IRIS) and guo2025repoaudit (RepoAudit) appear as arXiv preprints in our database because their conferences issue no DOI. They are the peer-reviewed ICLR 2025 and ICML 2025 papers [@li2024iris, p. 1; @guo2025repoaudit, p. 1].
- ahmed2026secvuleval is published at the AIware 2026 conference. Our copy is its arXiv version, which has a different title ("Benchmarking LLMs for Real-World C/C++ Vulnerability Detection"). We confirmed by hand that the authors match.
- khare2025understanding is the ICST 2025 paper. Our metadata check flags a year mismatch only because its arXiv version dates from 2023.
- qin2026review is a single-author narrative review in a low-visibility venue that does not document peer review [@qin2026review, p. 1]. We treat it as weak and use it only to show how our review differs from it.
- Most other papers were read from arXiv copies of the published version. Numbers in the final published version may differ slightly.

**Naming of lists.** Three numbered lists appear in this guide. They come from different project files, so we renamed them to avoid confusion:

- **Agreement 1 to Agreement 11** are points where several studies agree. In the evidence matrix (Appendix C) they are called G1 to G11.
- **Contradiction C1 to C8** are points where studies disagree. They keep their names from the evidence matrix.
- **Gap 1 to Gap 6** are the research gaps in the back part of this guide. In the project's gap report they are also called G1 to G6, but they are different from the agreements.
- Weaknesses W1 to W11 refer to the methodology comparison (Appendix B).

## Five terms you need first

- **Precision**: of all the warnings a tool raises, the share that are real vulnerabilities. Low precision means many false alarms.
- **Recall**: of all the real vulnerabilities, the share the tool finds. Low recall means many missed bugs.
- **F1**: a single score that combines precision and recall. It is high only when both are high.
- **Prevalence**: the share of vulnerable samples in the test data. Real code has few vulnerable functions, roughly 2% in two of our studies [@deininger2026open, p. 8; @lu2025lab, p. 4]. Many test sets are instead **balanced** (50% vulnerable).
- **Trivial baseline**: a "detector" that ignores the code, for example one that flags everything as vulnerable ("flag-all"). On a balanced test set, flag-all already reaches an F1 of 0.667. A real detector should clearly beat such baselines [I].

## Main findings per research question

### RQ1. Who wins? No approach wins everywhere

**Evidence strength: weak to moderate.**

- **On small, self-contained code, frontier LLMs beat SAST.** On 10 small C# projects, LLMs reached a mean F1 of 0.75–0.80 against 0.26–0.55 for SAST tools [@gnieciak2025large, p. 10]. On 250 tiny C programs, the best LLM scored 977 against 661 for the best non-LLM tool [@dubniczky2025castle, p. 11]. That first study, however, counted LLM findings as correct even when they pointed to the wrong line, a leniency it did not give SAST tools [@gnieciak2025large, p. 6].
- **On artificial test suites, CodeQL beats LLMs.** CodeQL had higher accuracy than the best LLM on all three synthetic datasets in one study [@khare2025understanding, p. 9].
- **On whole projects, LLM agents find more but warn too often.** General coding agents found far more known vulnerabilities than SAST (recall 59.55% against 0–34.29% on C/C++) [@li2026llm, p. 7]. Yet most LLM detectors and SAST tools produced mostly false warnings [@li2026llm, p. 11].
- **On the same functions, the winner depends on the score.** One study tested all three families on the same 1549 functions. Seven of eight LLMs beat lightweight SAST on balanced accuracy [@deininger2026open, p. 7; @deininger2026open, p. 10]. But at a realistic prevalence of 1 vulnerable function in 45 (written 1:44), Flawfinder and Semgrep were more precise than every LLM. LLM precision was 2.3–4.6%, barely above the 2.21% of flag-all [@deininger2026open, p. 8; @deininger2026open, p. 17].
- **Against fine-tuned DL, the ranking depends on data, class balance and threshold.** A small fine-tuned CodeBERT beat all eight LLMs on those functions (balanced accuracy 0.765 against at most 0.711) [@deininger2026open, p. 11; @deininger2026open, p. 17]. On pairs of vulnerable and fixed code, all families were near or below chance [@ding2025vulnerability, p. 9; @tan2026think, p. 6].
- **On brand-new 2025 vulnerabilities, everything struggles.** Trained DL detectors reached F1 3.47–8.65 and four open LLMs 0.79–5.36 [@lu2025lab, p. 13; @lu2025lab, p. 14]. By our calculation, flag-all would reach about 3.87 there [I].
- **The most robust pattern** [I]: LLMs tend to have higher recall and lower precision than SAST. At realistic prevalence, their margin over trivial baselines is small.

### RQ2. Why do studies disagree? Mostly because of the test setup

**Evidence strength: strong** for label noise and for the collapse under realistic testing. **Moderate** for prompt and threshold effects and for trivial baselines.

- **Wrong labels.** When experts re-checked "vulnerable" labels in popular datasets, only 39–65% were correct [@risse2025top, p. 8]. In a PHP dataset, 48.8% were [@tashenova2026real, p. 11].
- **Data leaks.** Up to 18.9% of test functions also appeared in the training data [@ding2025vulnerability, p. 4]. A model can then score well by remembering, not by understanding.
- **Balanced versus realistic test sets.** The ranking of models flips when the test set is imbalanced like real code [@shu2026evaluating, p. 40; @yildiz2025benchmarking, p. 7; @deininger2026open, p. 8].
- **Missing trivial baselines.** They are rarely reported, but often competitive [@tashenova2026real, p. 8; @deininger2026open, p. 7; @lu2025lab, p. 14].
- **New code and other datasets.** Performance drops sharply on code from a different source or a later time [@lu2025lab, p. 12; @lu2025lab, p. 13].
- **Prompt wording and decision threshold.** Rewording the question to the LLM, or moving the cut-off between "vulnerable" and "safe", can change the winner [@deininger2026open, p. 11; @deininger2026open, p. 20].
- **Artificial versus real code** [@khare2025understanding, p. 5], and **scoring a whole function versus the exact faulty line** [@ahmed2026secvuleval, p. 8].
- **Home-made datasets with inconsistent splits** are common [@kaniewski2026systematic, p. 35]. The same model on the same named dataset can differ by 28 F1 points between two papers [@lu2025lab, p. 12; @ding2025vulnerability, p. 7].

### RQ3. Do hybrids help? Yes for filtering false alarms, with a price

- **Filtering SAST warnings works, but loses real bugs** (moderate). LLMs removed most false alarms for under $0.20 per alarm, but also discarded 12–25% of real bugs [@du2026reducing, p. 8; @xiong2026sifting, p. 18].
- **Hybrid detectors are contested** (weak). IRIS and RepoAudit beat SAST in their authors' own tests [@li2024iris, p. 8; @guo2025repoaudit, p. 8], but not in an independent project-scale study [@li2026llm, p. 7; @li2026llm, p. 12]. IRIS also needs a strong LLM [@li2024iris, p. 10].
- **LLM cost varies enormously.** It ranges from cents per alarm to $1,247.66 per project, while SAST runs in minutes with no token cost [@li2026llm, p. 16].
- **Cost per real vulnerability found** (moderate, one study): USD 0.003–0.212 and 3.7–119.6 kJ of energy per true positive at 1:44 prevalence. This is computing cost only. It leaves out the human time needed to check the 25.6–41.9 false alarms that come with each real one [@deininger2026open, p. 8]. Small open models matched a frontier model at 1/66 of the cost [@deininger2026open, p. 17].
- **Explanations are unreliable.** LLMs point to the wrong place in the code [@gnieciak2025large, p. 11], and a fluent explanation does not mean the answer is right [@tan2026think, p. 9].

### RQ4. Where does each approach work? Patchy evidence

**Evidence strength: weak** (small samples per vulnerability type, results that diverge, and a single PHP study).

- **Vulnerability types.** LLMs do best on self-contained injection bugs. They do worst on bugs that need wider context, on weak cryptography and on pinpointing memory bugs [@khare2025understanding, p. 7; @xiong2026sifting, p. 18; @shu2026evaluating, p. 30]. CodeQL is better on integer overflow (CWE-190) [@khare2025understanding, p. 8].
- **Code size.** LLM performance falls as functions and files get longer [@ahmed2026secvuleval, p. 13; @li2026llm, p. 9].
- **Projects.** One DL detector found 76% of Chromium vulnerabilities but none in Linux, while all LLMs covered Linux better [@lu2025lab, p. 13].
- **Languages.** Evidence is concentrated on C/C++ and Java [@kaniewski2026systematic, p. 28]. The only PHP study tested no LLM. Its home-made SAST tool found 1.7–1.8% of vulnerabilities [@tashenova2026real, p. 9].

### RQ5. What is still missing?

**Evidence strength: moderate**, as a description of recurring limitations [I].

- Realistic, verified test data at repository level, with surrounding code as context [@zhou2025large, p. 19; @sheng2025llms, p. 25].
- Trivial baselines and realistic prevalence in every evaluation [@tashenova2026real, p. 13; @deininger2026open, p. 8].
- Better labels and control of data leaks [@tashenova2026real, p. 12; @lu2025lab, p. 17].
- Comparisons of all three families on the same data. Only two studies do this, each with clear limits [@khare2025understanding, p. 7; @deininger2026open, p. 10].
- Independent labelling, statistical tests and checks of prompt sensitivity [@li2026llm, p. 11; @deininger2026open, p. 20].
- Cost figures that include human checking time [@deininger2026open, p. 8], and control of how many real bugs filtering throws away [@xiong2026sifting, p. 19].
- Integration into developers' daily work [@zhou2025large, p. 19].

The authors of the broadest three-family study conclude that no method they tested is ready to sort vulnerable from safe functions on its own [@deininger2026open, p. 26] [A]. The six research gaps at the back of this guide turn these problems into concrete study ideas.

## Where studies agree

| Agreement | What several studies agree on | Strength | Key sources |
|---|---|---|---|
| 1 | Performance collapses when the test is realistic (real code, later code, realistic prevalence) | strong | [@chakraborty2024revisiting, p. 7; @ding2025vulnerability, p. 7; @lu2025lab, p. 13] |
| 2 | Labels in vulnerability datasets are often wrong | strong | [@risse2025top, p. 8; @ding2025vulnerability, p. 4; @tashenova2026real, p. 11] |
| 3 | Prompted LLMs over-flag and cannot tell vulnerable code from its fixed version | moderate | [@ding2025vulnerability, p. 9; @yildiz2025benchmarking, p. 8; @tan2026think, p. 7] |
| 4 | SAST finds few vulnerabilities in real code and does well only on artificial suites | moderate | [@zhou2024comparison, p. 6; @li2026llm, p. 7; @khare2025understanding, p. 9] |
| 5 | CodeQL's results on the OWASP test suite were reproduced by two independent groups | moderate | [@khare2025understanding, p. 9; @xiong2026sifting, p. 11] |
| 6 | Missing context (code outside the function) is the shared cause of failure | moderate | [@risse2025top, p. 9; @ahmed2026secvuleval, p. 9; @li2026llm, p. 15] |
| 7 | LLM filtering of SAST warnings removes many false alarms but also some real bugs | moderate | [@du2026reducing, p. 8; @xiong2026sifting, p. 18] |
| 8 | Prompted-only LLMs trail models adapted to the task | moderate | [@fu2023chatgpt, p. 4; @zhou2024comparison, p. 10; @shu2026evaluating, p. 17] |
| 9 | LLM cost far exceeds SAST cost and varies by orders of magnitude | moderate | [@li2026llm, p. 16; @du2026reducing, p. 8; @shu2026evaluating, p. 42] |
| 10 | Trivial baselines are surprisingly competitive | moderate | [@tashenova2026real, p. 8; @deininger2026open, p. 7; @lu2025lab, p. 14] |
| 11 | Computing cost per real vulnerability found is cents or less, but excludes human checking | moderate, one study | [@deininger2026open, p. 8] |

## Paper map

All 24 papers, grouped by the kind of comparison they make. Many papers fit more than one group; each appears once, under its main group. The group letters follow the methodology comparison (Appendix B). The Paper Summaries follow the same order.

### A. LLMs against SAST tools on the same code (6 papers)

| Key | Short title | Year and venue | Status | What it adds |
|---|---|---|---|---|
| gnieciak2025large | Large Language Models Versus Static Code Analysis Tools | 2025, IEEE Access | Peer-reviewed; arXiv copy read | 3 SAST tools against 3 LLMs on 10 small C# projects; LLMs win, mainly through recall [@gnieciak2025large, p. 10] |
| dubniczky2025castle | CASTLE benchmark | 2025, LNCS book chapter | Peer-reviewed; arXiv copy read | 250 tiny C programs; 13 SAST and 2 formal tools against 10 LLMs; top LLMs score highest [@dubniczky2025castle, p. 11] |
| khare2025understanding | Understanding the Effectiveness of LLMs in Detecting Security Vulnerabilities | 2025, ICST | Peer-reviewed; arXiv copy read | 16 LLMs against CodeQL (artificial code only) and DL detectors; CodeQL wins on artificial suites [@khare2025understanding, p. 9] |
| zhou2024comparison | Comparison of SAST Tools and LLMs for Repo-level Vulnerability Detection | 2024, arXiv | Preprint, not peer-reviewed | 15 SAST tools against 12 open LLMs on whole repositories; LLMs find more but flag up to 77.4% of functions [@zhou2024comparison, p. 7] |
| li2026llm | LLM-based Vulnerability Detection at Project Scale | 2026, IEEE TSE | Peer-reviewed; arXiv copy read | LLM detectors and coding agents against 4 SAST tools on real projects; agents find most, most warnings are false, cost up to $1,247.66 per project [@li2026llm, p. 7; @li2026llm, p. 16] |
| deininger2026open | Open or Frontier? A Cost- and Energy-Aware Benchmark | 2026, Computers | Peer-reviewed; publisher PDF | 8 LLMs, 3 SAST tools and 2 CodeBERT detectors on the same 1549 functions, with cost and energy per real vulnerability found [@deininger2026open, p. 8] |

### B. LLMs against fine-tuned deep-learning detectors (4 papers)

| Key | Short title | Year and venue | Status | What it adds |
|---|---|---|---|---|
| fu2023chatgpt | ChatGPT for Vulnerability Detection, Classification, and Repair | 2023, APSEC | Peer-reviewed; arXiv copy read | Early test: fine-tuned models far beat prompted ChatGPT on Big-Vul (F1 94% against 29%) [@fu2023chatgpt, p. 4] |
| ding2025vulnerability | Vulnerability Detection with Code Language Models: How Far are We? (PrimeVul) | 2025, ICSE | Peer-reviewed; arXiv copy read | New cleaner dataset PrimeVul; models collapse under realistic testing; GPT-4 below random on vulnerable/fixed pairs [@ding2025vulnerability, p. 7; @ding2025vulnerability, p. 9] |
| shu2026evaluating | Evaluating LLMs for Multilingual Vulnerability Detection at Dual Granularities | 2026, Empirical Software Engineering | Peer-reviewed; arXiv copy read | 8 smaller pre-trained models against 5 LLMs in 7 languages; the winner flips with class balance [@shu2026evaluating, p. 40] |
| lu2025lab | From Lab to Reality | 2025 (arXiv); published 2026, Journal of Systems and Software | Peer-reviewed; our copy is the arXiv accepted manuscript | DL and open LLMs on vulnerabilities disclosed from May 2025; LineVul F1 falls from 91 to 4.39–6.87 [@lu2025lab, p. 12; @lu2025lab, p. 13] |

### B2. SAST against classical machine learning, no LLM (1 paper)

| Key | Short title | Year and venue | Status | What it adds |
|---|---|---|---|---|
| tashenova2026real | A Real CVE-Backed Benchmark for WordPress Plugin Vulnerability Detection | 2026, Big Data and Cognitive Computing | Peer-reviewed; publisher PDF | Only PHP study; home-made taint analyser finds 1.7–1.8% of vulnerabilities; no LLM tested [@tashenova2026real, p. 9; @tashenova2026real, p. 13] |

### C1. Hybrids: the LLM works inside the analyser (2 papers)

| Key | Short title | Year and venue | Status | What it adds |
|---|---|---|---|---|
| li2024iris | IRIS: LLM-Assisted Static Analysis | 2024 (arXiv); ICLR 2025 | Peer-reviewed conference paper; recorded as preprint | LLM tells CodeQL what to look for; 55 against 27 of 120 Java vulnerabilities found [@li2024iris, p. 8] |
| guo2025repoaudit | RepoAudit: An Autonomous LLM-Agent for Repository-Level Code Auditing | 2025 (arXiv); ICML 2025 | Peer-reviewed conference paper; recorded as preprint | LLM agent audits C/C++ repositories; 40 real and 11 false findings (78.43% precision) in the authors' test [@guo2025repoaudit, p. 8] |

### C2. Hybrids: the LLM filters SAST warnings (2 papers)

| Key | Short title | Year and venue | Status | What it adds |
|---|---|---|---|---|
| du2026reducing | Reducing False Positives in Static Bug Detection with LLMs: An Empirical Study in Industry | 2026, ICSE-SEIP | Peer-reviewed; arXiv copy read | At Tencent, a hybrid removes 94–98% of false alarms and keeps 75–88% of real bugs [@du2026reducing, p. 8] |
| xiong2026sifting | Sifting the Noise: LLM Agents in Vulnerability False Positive Filtering | 2026, PACMSE (ISSTA) | Peer-reviewed | Best agent cuts the false-alarm rate from 98.3% to 6.3% but drops 22.25% of real vulnerabilities [@xiong2026sifting, p. 12; @xiong2026sifting, p. 18] |

### D. Agents and reasoning LLMs (2 papers)

| Key | Short title | Year and venue | Status | What it adds |
|---|---|---|---|---|
| tan2026think | To Think or Not to Think | 2026, ASE | Peer-reviewed; publisher PDF | Controlled test of "thinking" mode and multi-agent setups; thinking raises F1 mainly via recall at 2.7–4.4 times the energy [@tan2026think, p. 6; @tan2026think, p. 10] |
| yildiz2025benchmarking | Benchmarking LLMs and LLM-based Agents in Practical Vulnerability Detection for Code Repositories | 2025, ACL | Peer-reviewed | Repository-context benchmark of 879 vulnerabilities; GPT-4o methods stay at or below 20.17% pairwise accuracy [@yildiz2025benchmarking, p. 6] |

### E. How realistic are the benchmarks? (3 papers)

| Key | Short title | Year and venue | Status | What it adds |
|---|---|---|---|---|
| chakraborty2024revisiting | Revisiting the Performance of DL-Based Vulnerability Detection on Realistic Datasets | 2024, IEEE TSE | Peer-reviewed; arXiv copy read | On whole-project test data, DL precision falls to 1–10% [@chakraborty2024revisiting, p. 7] |
| risse2025top | Top Score on the Wrong Exam | 2025, PACMSE (FSE) | Peer-reviewed; arXiv copy read | Only 39–65% of "vulnerable" labels are correct; counting words alone gives F1 0.86 [@risse2025top, p. 8; @risse2025top, p. 11] |
| ahmed2026secvuleval | SecVulEval: Context-Aware Benchmarking of LLMs | 2026, AIware | Peer-reviewed; our copy is the arXiv version under a different title | Line-level scoring: the best LLM reaches only 23.83% F1 [@ahmed2026secvuleval, p. 8] |

### F. Surveys and reviews (4 papers)

| Key | Short title | Year and venue | Status | What it adds |
|---|---|---|---|---|
| kaniewski2026systematic | A Systematic Literature Review on Detecting Software Vulnerabilities with LLMs | 2026, ACM TOSEM | Peer-reviewed systematic review; arXiv copy read | 263 studies; field dominated by C/C++ function-level tests on noisy data [@kaniewski2026systematic, p. 8; @kaniewski2026systematic, p. 28] |
| zhou2025large | Large Language Model for Vulnerability Detection and Repair: Literature Review | 2025, ACM TOSEM | Peer-reviewed systematic review; arXiv copy read | 58 studies to March 2024; only one of 40 detection studies worked at repository level [@zhou2025large, p. 18] |
| sheng2025llms | LLMs in Software Security: A Survey of Vulnerability Detection Techniques | 2025, ACM Computing Surveys | Peer-reviewed narrative survey; arXiv copy read | Overview of techniques and datasets; names data leaks and label errors as key challenges [@sheng2025llms, p. 25] |
| qin2026review | A Review of Source Code Vulnerability Detection Methods Based on LLMs | 2026, Computers and Artificial Intelligence | Weak: peer review not documented; positioning only | Single-author narrative review of 32 references with the same "evaluation reliability" framing as ours, but no search protocol [@qin2026review, p. 14] |

## Five papers to read first

If you only have time for five papers, read these, in this order:

1. **deininger2026open** (2026). The only study that runs LLMs, SAST tools and fine-tuned DL on exactly the same real functions, and then re-scores them at a realistic prevalence. It shows in one paper how the winner changes with the score you choose, and it gives the first cost per real vulnerability found [@deininger2026open, p. 8; @deininger2026open, p. 11]. Look at its tables on precision at 1:44 and on cost.
2. **ding2025vulnerability** (2025, PrimeVul). The key paper on why many published numbers are too good. It audits labels and data leaks, builds a cleaner dataset, and shows models collapse on it [@ding2025vulnerability, p. 4; @ding2025vulnerability, p. 7]. Many later studies build on PrimeVul.
3. **li2026llm** (2026). The largest independent test at the scale of whole projects. It compares LLM detectors, coding agents and SAST tools, explains why warnings are false, and measures cost [@li2026llm, p. 7; @li2026llm, p. 16]. It is also the independent check on IRIS and RepoAudit.
4. **risse2025top** (2025). Short and readable. It shows that many "vulnerable" labels are wrong and that a classifier counting words scores almost as high as the best published models [@risse2025top, p. 8; @risse2025top, p. 11]. It will change how you read every number in this field.
5. **kaniewski2026systematic** (2026). The most recent systematic review, covering 263 studies [@kaniewski2026systematic, p. 8]. Read it for the big picture of datasets and methods, and to see what our review adds (it does not compare LLMs with SAST).

## Where studies disagree

These eight contradictions come from the evidence matrix. In each case we compared the data, method, metric and timing. Our explanations are interpretations [I], not settled facts.

- **C1. Fine-tuned models or GPT-4?** Fine-tuned models far beat GPT-4 on Big-Vul (F1 94% and 87% against 29%) [@fu2023chatgpt, p. 4]. On vulnerable/fixed pairs from PrimeVul, GPT-4 beats every fine-tuned model, although all stay below a random guesser (12.94% against at most 3.01%, random 22.70%) [@ding2025vulnerability, p. 9]. On single PrimeVul functions, a fine-tuned CodeBERT beats all eight LLMs again [@deininger2026open, p. 11]. [I] The benchmark and the score, not the model family, drive the reversal.
- **C2. Does RepoAudit work?** Its authors report 78.43% precision and all 21 known bugs found [@guo2025repoaudit, p. 8]. An independent study found 0 of 110 known C/C++ vulnerabilities and 92.77% false warnings [@li2026llm, p. 7; @li2026llm, p. 11]. The two studies differ in targets, code versions, metric and who labelled the results. Unresolved.
- **C3. LLMs or SAST?** LLMs win on small programs [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11], CodeQL wins on artificial suites [@khare2025understanding, p. 9], and at repository level both have problems [@li2026llm, p. 11]. On identical functions, LLMs lead on balanced accuracy but SAST is more precise at realistic prevalence [@deininger2026open, p. 8; @deininger2026open, p. 10]. [I] LLMs over-flag and SAST finds little, so the ranking depends on the metric.
- **C4. Does "reasoning" reduce false alarms?** One paper says reasoning models made fewer false alarms [@dubniczky2025castle, p. 14], but its own table shows DeepSeek R1 with more false alarms than GPT-4o [@dubniczky2025castle, p. 11]. A controlled study finds thinking raises F1 mostly through recall [@tan2026think, p. 6]. Reasoning lowered one model's ability to recognise safe code [@deininger2026open, p. 17]. [I] The effect depends on the model.
- **C5. Balanced or realistic test sets?** On a balanced test, fine-tuned GPT-4o wins; on an imbalanced test, smaller pre-trained models win [@shu2026evaluating, p. 17; @shu2026evaluating, p. 40]. F1 drops from about 49–65% on balanced pairs to 5.41–12.21% on realistic data [@yildiz2025benchmarking, p. 7]. [I] Rankings on balanced data do not carry over to real use.
- **C6. Does IRIS beat CodeQL?** In the authors' test, IRIS finds 55 of 120 vulnerabilities against CodeQL's 27 [@li2024iris, p. 8]. On new real-world Java projects, 97.80% of IRIS warnings were false against 77.00% for CodeQL [@li2026llm, p. 12]. The setups are not like-for-like. Open.
- **C7. Same model, same dataset, different score.** LineVul on Big-Vul scores F1 91.00 in one paper [@lu2025lab, p. 12] and the same model type 62.88 in another [@ding2025vulnerability, p. 7]. Neither paper explains the 28-point gap. [I] Probably different data splits and preprocessing.
- **C8. Does a detector trained on time-split data survive new code?** A CodeBERT trained on PrimeVul keeps balanced accuracy 0.765 on PrimeVul's later test split [@deininger2026open, p. 11]. DL detectors trained on older datasets fall to F1 3.47–8.65 on 2025 vulnerabilities [@lu2025lab, p. 13]. The datasets, training data and thresholds differ. Unresolved.
