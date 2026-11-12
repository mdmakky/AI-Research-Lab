## IRIS: LLM-Assisted Static Analysis for Detecting Security Vulnerabilities

> **Takeaway:** In the authors' own test, letting GPT-4 help the CodeQL static analyser roughly doubled the number of known Java vulnerabilities found (55 vs 27 of 120), but most warnings were still false and the gain needed a strong model. A later independent study found IRIS much noisier than CodeQL on new code, so the benefit is contested.

| Item | Detail |
|---|---|
| Authors | Ziyang Li, Saikat Dutta, Mayur Naik |
| Year | 2024 (our copy is arXiv version 3, April 2025) |
| Venue | arXiv. Our copy's header reads "Published as a conference paper at ICLR 2025" |
| Status | Preprint in our records, because we hold the arXiv copy. The text is the ICLR 2025 conference version, so it is peer-reviewed in substance |
| Identifier | doi:10.48550/arxiv.2405.17238 (arXiv 2405.17238) |
| Paper type | Tool proposal with benchmark evaluation |
| Relevance to us | High: RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
A static analysis tool reads source code without running it and looks for known bug patterns. Security-focused ones are called SAST (static application security testing) tools; CodeQL is a widely used one. Many use taint analysis: they follow untrusted data from a "source" (for example, input from a web request) to a "sink" (a dangerous place, such as a shell command or a file path). If the data reaches a sink without being cleaned, the tool raises a warning.

This only works if someone has listed which library functions are sources and sinks (the specifications). Missing specifications mean missed bugs; missing context means false alarms (false positives: warnings about safe code).

IRIS is a hybrid tool. It asks a large language model (LLM, an AI model trained on huge amounts of text and code, such as GPT-4) to write the missing source and sink lists. A second LLM step then judges each warning as real or false [A] [@li2024iris, p. 2].

### How they did it
IRIS works in four stages [V] [@li2024iris, p. 4]:

1. CodeQL extracts candidate library functions and internal function parameters.
2. An LLM labels them as sources or sinks for a given weakness type.
3. These labels become CodeQL rules, and a taint query runs over the whole project.
4. An LLM looks at each reported data path and decides whether it is a true or false positive ("contextual analysis").

The comparison tools were CodeQL 2.15.3 with all its built-in security queries, plus Facebook Infer, SpotBugs and Snyk [V] [@li2024iris, p. 7]. Seven LLMs were tried, plus ablations (removing one part at a time to see what it contributes) [V] [@li2024iris, p. 10]. A vulnerability counted as "detected" if at least one reported path passed through the method that the official fix changed [V] [@li2024iris, p. 6]. No LLM-only detector and no deep-learning detector was tested [V] [@li2024iris, p. 7].

### Data and setup
The authors built a new benchmark, CWE-Bench-Java. It holds 120 real vulnerabilities, one per Java project [V] [@li2024iris, p. 7]. Each is a CVE, a public ID for a known vulnerability. Each belongs to a CWE, a standard category of weakness. There are four CWEs: path traversal (CWE-22, 55 cases), OS command injection (CWE-78, 13), cross-site scripting (CWE-79, 31) and code injection (CWE-94, 21). Projects average 300,000 lines of code, the largest about 7 million [V] [@li2024iris, p. 7]. The 120 cases were filtered from 1,065 candidates and checked by two of the authors [V] [@li2024iris, p. 19].

Models ran at temperature 0 (the most repeatable setting), and the OpenAI queries ran in April–May 2024 [V] [@li2024iris, p. 20]. Code and data are public [V] [@li2024iris, p. 2].

### Key findings
- [V] IRIS with GPT-4 detected 55 of 120 vulnerabilities; CodeQL alone detected 27. The average false discovery rate (FDR, the share of warnings that are not the known bug) was 84.82% for IRIS vs 90.03% for CodeQL [@li2024iris, p. 8].
- [V] Other SAST tools found fewer: Infer 0, SpotBugs 4, Snyk 23 of 120 [@li2024iris, p. 8].
- [V] Gains differ by weakness type: code injection 0 to 8, cross-site scripting 4 to 13, path traversal 22 to 31, command injection 1 to 3 (CodeQL vs IRIS with GPT-4) [@li2024iris, p. 8].
- [V] Only GPT-4 lowered the FDR below CodeQL. Smaller models reached FDRs of about 95%, and the LLM warning check made two small models slightly worse [@li2024iris, p. 8; @li2024iris, p. 10].
- [V] Both LLM-written sources and sinks were needed: 27 detections with CodeQL's lists, 36 with GPT-4 sources only, 24 with GPT-4 sinks only, 55 with both [@li2024iris, p. 10].
- [V] A manual check of 50 random IRIS warnings found 27 with potential attack surfaces, giving an estimated FDR of 46% [@li2024iris, p. 7].
- [V] On the latest versions of 30 projects, IRIS found 4 previously unknown vulnerabilities that CodeQL missed. Whether developers confirmed them is not reported [@li2024iris, p. 8].
- [V] Runtime with a small open model ranged from 43 seconds to 4 hours per project. Dollar or token cost is not reported [@li2024iris, p. 22].

### Limitations and weaknesses
The authors say many vulnerabilities are still missed, that IRIS makes many LLM calls and so costs more, and that only Java was tested [A] [@li2024iris, p. 10]. They also note that the FDR is an upper bound, because unknown real bugs count as false alarms [A] [@li2024iris, p. 7].

Our own concerns [I]:

- The CVEs and fixes are public and older than the 2024 queries, so GPT-4 may have seen them in training (contamination). The paper does not discuss this.
- An 84.82% FDR still means most warnings are not the known bug. The friendlier 46% estimate rests on only 50 warnings.
- IRIS ran on a patched CodeQL engine [@li2024iris, p. 20]. It is unclear whether the CodeQL baseline used the same patched engine.
- "Detected" is lenient: any path touching the fixed method counts.
- There is one run per setting, with no significance tests and no cost in dollars.

### Gaps and future work this paper leaves open
- Gap G4 (independent replication of hybrid tools): the authors' result and the independent result disagree, and no study yet separates the causes. The gap report proposes an IRIS replication on public CWE-Bench-Java data [@li2024iris, p. 2].
- Gap G5 (other languages): the authors list other languages as future work [A] [@li2024iris, p. 10].
- Gap G2 (same-benchmark comparison of all three families on recent code): IRIS has no LLM-only or deep-learning baseline and no contamination control [I].
- Gap G6 (cost): no token or dollar cost is given [I].

### Why it matters for your research
IRIS is the central "LLM inside SAST" study in our corpus, with a real SAST baseline on large real-world Java projects. It shows the hybrid idea can raise recall on known CVEs. It also shows that precision stays poor and that the gain depends on model strength [I]. CWE-Bench-Java is a reusable benchmark for RQ2.

### Connections to other papers
- li2026llm is an independent, peer-reviewed study and the main counter-evidence (contradiction C6 in the evidence matrix). On new real-world Java projects it measured a sampled FDR (SFDR) of 97.80% for IRIS vs 77.00% for CodeQL [V] [@li2026llm, p. 12]. The two studies are not like-for-like: known CVEs vs new code, detections vs SFDR, and different labelling. li2026llm also labels warnings with Codex, an LLM it evaluates itself [V] [@li2026llm, p. 11]. Neither side settles the question [I].
- CodeQL finding only 27 of 120 fits agreement G4 in the evidence matrix: SAST recall is low on real code [@li2024iris, p. 8; @li2026llm, p. 7].
- guo2025repoaudit, the other hybrid tool, is contested in the same way (contradiction C2).
- du2026reducing excluded IRIS from its industrial study because IRIS needs a compilable repository for CodeQL [V] [@du2026reducing, p. 5].

