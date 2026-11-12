## Comparison of Static Application Security Testing Tools and Large Language Models for Repo-level Vulnerability Detection

> **Takeaway:** In whole Java, C and Python repositories, free SAST tools found few known vulnerabilities (at best 30–44%) but flagged few functions, while fine-tuned open LLMs found many more (up to 100%) but flagged up to 77.4% of all functions. This is a preprint built on only about 8–10 test vulnerabilities per language, so the evidence is weak.

| Item | Detail |
|---|---|
| Authors | Xin Zhou, Duc-Manh Tran, Thanh Le-Cong, Ting Zhang, Ivana Clairine Irsan, Joshua Sumarlin, Bach Le, David Lo |
| Year | 2024 |
| Venue | arXiv |
| Status | Preprint, not peer-reviewed. The "ESEC/FSE'23" page header is a template leftover, not a sign of peer review. |
| Identifier | arXiv 2407.16235 (DOI 10.48550/arxiv.2407.16235) |
| Paper type | Empirical comparison study |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
A preprint is a paper posted online before, or without, peer review, so no outside experts have checked it. This one asks a practical question. If you scan a whole software repository (all of a project's code), which works better: SAST tools or LLMs? SAST tools read code and apply fixed rules. LLMs here means language models trained on code, from small ones such as CodeBERT to larger ones such as CodeLlama-7B.

The paper finds a clear trade-off. SAST tools miss most vulnerabilities but raise few alarms. LLMs catch more but mark a large share of all functions as suspicious, which a developer would then have to check by hand.

### How they did it
Each repository is split into functions, and every function is classified as vulnerable or not [@zhou2024comparison, p. 3]. The authors ran 15 free SAST tools and 12 open LLMs [@zhou2024comparison, p. 4]. Four small models were fully fine-tuned, which means they got extra training on labelled examples from this task. Eight larger models (3.8–8 billion parameters) were either fine-tuned with LoRA, a cheap method that trains only a small add-on, or prompted with no extra training [@zhou2024comparison, p. 4]. A small side test also prompted ChatGPT (GPT-3.5) [@zhou2024comparison, p. 9].

Because there may be unknown flaws in the code, the authors do not compute precision or F1 [@zhou2024comparison, p. 5]. Instead they use two measures. The detection ratio is the share of known vulnerabilities found. In Scenario 1 one flagged function counts as a find; in Scenario 2 all affected functions must be flagged. The marked function ratio is the share of all functions flagged, used as a rough stand-in for the false alarm rate [@zhou2024comparison, p. 5].

### Data and setup
- 270 known vulnerabilities in 134 repositories: Java (50 projects, 87 vulnerabilities), C (6 projects, 85) and Python (78 projects, 98). Only 0.008–0.18% of functions are vulnerable [@zhou2024comparison, p. 3].
- The Python dataset is new, built from the US National Vulnerability Database [@zhou2024comparison, p. 3].
- Vulnerabilities were split randomly 8:1:1 into training, validation and test sets [@zhou2024comparison, p. 5].
- [I] Test-set sizes are not reported. The steps between scores imply about 8, 9 and 10 test vulnerabilities for Java, C and Python [@zhou2024comparison, p. 6].
- SAST tool versions and settings are not reported. Runtime and cost are not reported.

### Key findings
- [V] SAST detection is low. Many tools found nothing. The best single tools found 37.5% in Java (Horusec), 44.4% in C (CodeQL) and 30.0% in Python (DevSkim) in Scenario 1, while marking only 0.2–5.2% of functions [@zhou2024comparison, p. 7].
- [V] LLMs found up to 100% in Java and C and 90% in Python, but marked 3.5–77.4% of functions depending on model and language [@zhou2024comparison, p. 6; @zhou2024comparison, p. 7].
- [V] Fine-tuning beats prompting. In Java, LoRA models found 73.4% (Scenario 1) while marking 19.4% of functions; prompted models marked 52.1–55.0% [@zhou2024comparison, p. 7].
- [V] Plain ChatGPT prompting found only 3.7–23.2%, against 89.2% for a fine-tuned CodeBERT in the same test [@zhou2024comparison, p. 10].
- [V] Combining all SAST tools helps at little cost. In Python, Scenario 1 detection rose from 30.0% to 50.0% while marked functions rose from 4.5% to 7.7% [@zhou2024comparison, p. 8].
- [V] A majority vote across the 12 fine-tuned LLMs cut the marked ratio by 40.9–74.6%, with detection close to the best single LLM [@zhou2024comparison, p. 9].
- [V] By weakness type, CWE-119 (memory buffer errors) was found best; CWE-835 (infinite loop) and CWE-89 (SQL injection) were missed by both groups [@zhou2024comparison, p. 8].
- [A] Combined LLMs work best for Java, combined SAST tools for C and Python [@zhou2024comparison, p. 9].

### Limitations and weaknesses
- [I] With only about 8–10 test vulnerabilities per language, one vulnerability moves a score by 10 or more points. There are no repeated runs or confidence intervals.
- [I] Several cells in the main results table lost their first digit in typesetting (for example 7.5 where the text says 37.5) [@zhou2024comparison, p. 6; @zhou2024comparison, p. 7]. We quote the text values.
- [I] The abstract says combining SAST tools and LLMs reduces both families' drawbacks [@zhou2024comparison, p. 1]. But the experiments only combine SAST with SAST and LLM with LLM [@zhou2024comparison, p. 8].
- [I] The LLMs were trained on the same data source as the test set, possibly even the same projects, while SAST tools ran untuned. The comparison is uneven.
- [I] The marked function ratio is not a true false alarm rate, so results cannot be pooled with studies that report precision.
- [A] Models were capped at 8 billion parameters for compute reasons, and pre-training data leakage is possible [@zhou2024comparison, p. 4; @zhou2024comparison, p. 10].

### Gaps and future work this paper leaves open
- [A] The authors call for repository-level evaluation, fewer flagged functions (filtering, repository context, better prompts) and better ways to combine LLMs with SAST [@zhou2024comparison, p. 10].
- [I] Its detection ratio is one of five incompatible headline metrics across LLM-vs-SAST studies, which is part of gap G1.
- [I] It has no classic deep-learning detector and uses older, pre-cutoff code, so it does not close gap G2.
- [I] It is one of the few Python sources, but with about 10 test vulnerabilities, and it has no PHP or Go. This is gap G5.
- [I] No runtime or cost is reported, so it adds nothing to gap G6.

### Why it matters for your research
This is one of the few studies that compares many SAST tools with many LLMs on the same real repositories in three languages. Its pattern recurs across the review: SAST is quiet but misses most flaws, while LLMs catch more but bury real findings in alarms. Because it is a preprint with very small test sets, cite it as supporting evidence for that pattern, not as proof on its own.

### Connections to other papers
- Contradiction C3 (LLM vs SAST rankings reverse): its "LLMs detect more but flag up to 77.4%" result sits between the small-code wins in gnieciak2025large [@gnieciak2025large, p. 10] and the project-scale study li2026llm, where most tools' real-world warnings are mostly false [@li2026llm, p. 11].
- Agreement G4 (SAST recall is low on real code): it agrees with CASTLE [@dubniczky2025castle, p. 12] and li2026llm [@li2026llm, p. 7].
- Agreement G8 (prompt-only LLMs trail adapted models): its ChatGPT result matches fu2023chatgpt [@fu2023chatgpt, p. 4] and shu2026evaluating [@shu2026evaluating, p. 17].
- [I] Its huge marked ratios foreshadow deininger2026open, where every LLM's precision is barely above flagging everything at a realistic vulnerability rate [@deininger2026open, p. 8].
