## A Review of Source Code Vulnerability Detection Methods Based on Large Language Models: Models, Techniques, and Evaluation

> **Takeaway:** This is the review closest to ours: it also argues that benchmark design inflates LLM results. But it is a small, single-author narrative review in a venue with undocumented peer review, it leaves static-analysis tools out of scope, and it mostly repeats sources we already have. Use it to position our work, not as independent evidence.

| Item | Detail |
|---|---|
| Authors | Letong Qin |
| Year | 2026 |
| Venue | Computers and Artificial Intelligence (Zeus Press) |
| Status | Listed as a published journal article, but peer review is not documented. The PDF has no received or accepted dates and no peer-review statement, and the venue is low-visibility. We weight it like grey literature. Our copy is the publisher PDF (DOI printed in it). |
| Identifier | DOI 10.70267/cai.v3n5.122137 |
| Paper type | Narrative literature review (no search protocol) |
| Relevance to us | High for positioning (closest competing review); weak as evidence — RQ2, RQ5 (conceptual only for RQ1 and RQ3) |

### In plain words
This paper reviews how researchers use AI language models to find vulnerabilities (security flaws) in source code. It covers smaller "code Transformer" models, such as CodeBERT, and large language models (LLMs), such as GPT-4 [A] [@qin2026review, p. 1].

Its main message is about trust in results. High scores on benchmarks are easily inflated by duplicate samples, wrong labels, random data splits and "temporal leakage", meaning that test examples come from the same period the model learned from [A] [@qin2026review, p. 1]. A benchmark is a fixed test set with known answers. This framing is very close to our own review, which is why the paper matters to us.

### How they did it
It is a narrative review: the author picked and discussed papers without a written search plan. No databases, search strings, screening steps, study counts or quality checks are reported [I] [@qin2026review, p. 4]. It has 32 references in total [I].

The author sorts methods by how they acquire knowledge about vulnerabilities, for example fine-tuning (further training on labelled examples), direct prompting, or combining models [A] [@qin2026review, p. 4]. SAST tools (static application security testing: rule-based scanners that check code without running it) are explicitly not reviewed. They appear only as baselines or helper tools [A] [@qin2026review, p. 4].

### Data and setup
- No new data or experiments; it re-reports numbers from cited papers [I].
- Its main numerical example repeats a results table from the PrimeVul study. Five code models scored F1 62.88–68.26% on the older Big-Vul dataset but only 1.91–5.82% when moved to PrimeVul [A] [@qin2026review, p. 12]. F1 is a 0-to-100% score that balances found flaws against false alarms. We checked these ranges against the original study, and they match [@ding2025vulnerability, p. 7].
- Its quantitative claims rest mainly on three sources already in our corpus: ding2025vulnerability, gnieciak2025large and sheng2025llms [I] [@qin2026review, p. 15].

### Key findings
- Scores from a random data split should be called "within-benchmark performance", not a real-world detection rate [A] [@qin2026review, p. 10].
- Testing on later code ("out-of-time" testing) should be the basic reliability check [A] [@qin2026review, p. 10].
- Training-data contamination should be audited as one possible explanation for good scores, not assumed [A] [@qin2026review, p. 10].
- Different LLM methods cannot be ranked against each other, because their datasets, model versions and test rules differ [A] [@qin2026review, p. 12].
- On LLMs versus SAST, the review says SAST is "usually more stable" within its rules, LLMs are better at explaining, and the two are complementary, not replacements [A] [@qin2026review, p. 12]. No numbers are given.
- It recommends a workflow in which SAST proposes candidates, an LLM reviews or explains them, and a human confirms. It says such a workflow should be judged by audit time and missed flaws, not only by F1 [A] [@qin2026review, p. 8; @qin2026review, p. 13].

### Limitations and weaknesses
- It is not systematic. Its selection of studies cannot be checked for bias, so it cannot count as a systematic review [I].
- The corpus is small and selective. It misses the project-scale and alarm-filtering studies that we have, such as li2026llm, du2026reducing and xiong2026sifting [I].
- The LLM-versus-SAST conclusion is under-supported. SAST is out of scope, and the only head-to-head study it cites (gnieciak2025large) found LLMs above SAST on mean F1 (0.75–0.80 vs 0.26–0.55) [@gnieciak2025large, p. 10]. The review does not mention this pro-LLM result [I].
- It is not independent evidence. Its numbers come from studies already in our corpus. Counting it as extra support would count the same evidence twice [I].
- It does not line up conflicting results study by study against their test setups [I].
- There are editorial loose ends. Three opening questions are not matched to its four formal research questions, and a "C2" label is used but never defined [I] [@qin2026review, p. 2; @qin2026review, p. 4; @qin2026review, p. 12].
- The venue is uncertain: there is no peer-review statement, no submission dates and no DOAJ listing. We did not confirm that it is predatory [I].

### Gaps and future work this paper leaves open
The author recommends out-of-time and project-separated testing, data cards (documents that describe how a dataset was built), recall at a fixed false-alarm budget, checks of each part of an explanation, studies that record audit time per real vulnerability, and SAST-plus-LLM systems judged by total audit cost [A] [@qin2026review, p. 13]. In our gap report it appears under gap G1: it recommends better reporting but re-scores no published results itself. It also appears under gap G6: it calls for audit-time and total-cost measurement but supplies no figures [I].

### Why it matters for your research
Reviewers of our work are likely to point to this paper. It shares our framing, but it lacks what we add: coverage of LLMs, SAST, deep learning and hybrids together, plus a study-by-study audit that explains contradictions through test setup. So it strengthens our novelty claim rather than weakening it. Cite it for positioning only, not as evidence [I].

### Connections to other papers
- It relies on ding2025vulnerability for benchmark inflation. Agreement G1 in the evidence matrix (realistic evaluation lowers scores) should cite ding directly [@ding2025vulnerability, p. 7].
- It relies on gnieciak2025large for LLM versus SAST, but leaves out that study's pro-LLM result. Contradiction C3 in the evidence matrix gives the full picture [@gnieciak2025large, p. 10; @khare2025understanding, p. 9].
- It also leans on sheng2025llms. kaniewski2026systematic is the stronger, systematic review with a similar "evaluation pitfalls" message [I].
- Its suggested SAST-then-LLM workflow is tested in du2026reducing and xiong2026sifting, which find large false-alarm cuts but lose 12–25% of real bugs [@du2026reducing, p. 8; @xiong2026sifting, p. 18].

