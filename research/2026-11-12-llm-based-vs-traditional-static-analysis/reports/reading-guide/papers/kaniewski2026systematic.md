## A Systematic Literature Review on Detecting Software Vulnerabilities with Large Language Models

> **Takeaway:** The largest review in our project (263 studies, up to November 2025) shows that LLM vulnerability-detection research is fragmented. Most studies use old, noisy, imbalanced C/C++ datasets with their own splits, so their numbers cannot be compared fairly. It does not compare LLMs with static-analysis tools or other detectors.

| Item | Detail |
|---|---|
| Authors | Sabrina Kaniewski, Fabian Schmidt, Markus Enzweiler, Michael Menth, Tobias Heer |
| Year | 2026 |
| Venue | ACM Transactions on Software Engineering and Methodology (TOSEM) |
| Status | Peer-reviewed journal article. Our copy is the arXiv version 2507.22659v2 (December 2025), not the typeset journal version. |
| Identifier | DOI 10.1145/3815425; arXiv 2507.22659 |
| Paper type | Systematic literature review (mapping study, no pooled performance numbers) |
| Relevance to us | High — RQ2, RQ5, RQ4 (qualitative only for RQ3; not RQ1) |

### In plain words
A systematic literature review (SLR) collects all studies on a question by following a written plan, so that others can repeat it. This SLR looks at how researchers use large language models (LLMs) to find vulnerabilities, meaning security flaws in source code. Here "LLM" is used broadly and even includes smaller models such as CodeBERT [A] [@kaniewski2026systematic, p. 2].

It does not ask "which tool is best?" Instead it maps how studies set up their tests, and which datasets they use. A dataset (or benchmark) is a fixed set of code examples with known answers. The review's main message is that studies use such different datasets and data splits that their results are hard to compare [A] [@kaniewski2026systematic, p. 2].

### How they did it
The authors followed the Kitchenham guidelines, a standard method for software-engineering reviews [A] [@kaniewski2026systematic, p. 5]. They searched three databases (IEEE Xplore, ACM Digital Library and arXiv) with a printed search string, then followed references forward and backward ("snowballing") [A] [@kaniewski2026systematic, p. 7].

They kept studies that build and test LLM-based detectors. They excluded studies that only use an LLM to post-process the output of other tools [A] [@kaniewski2026systematic, p. 8]. This matters for us. SAST tools (static application security testing: rule-based scanners that read code without running it) often produce many false alarms. Studies where an LLM filters those alarms are therefore outside this review.

They also re-analysed 20 popular datasets themselves, measuring size, share of vulnerable samples and CWE coverage. A CWE is a standard category of weakness, such as "buffer overflow" [V] [@kaniewski2026systematic, p. 28; @kaniewski2026systematic, p. 30].

### Data and setup
- 4,155 database hits; 263 studies included, of which 185 are peer-reviewed and 78 (29.7%) are arXiv preprints [V] [@kaniewski2026systematic, p. 8].
- Time window: January 2020 to November 2025 [A] [@kaniewski2026systematic, p. 2].
- A quality check is described, but its scoring and threshold are not reported. The number of reviewers and their agreement are also not reported [I].
- The list of studies and other materials are public on GitHub [A] [@kaniewski2026systematic, p. 3].

### Key findings
- Most studies treat detection as a yes/no question: 195 studies use binary classification [V] [@kaniewski2026systematic, p. 11].
- The most-used datasets are old, function-level C/C++ sets: Devign in 69 studies, Big-Vul in 63, ReVeal in 40 [V] [@kaniewski2026systematic, p. 26].
- Class balance differs hugely between datasets. "Class balance" means the share of vulnerable examples. It is 4.5% in Big-Vul and 2.9% in PrimeVul, but 48.0% in Devign [V] [@kaniewski2026systematic, p. 28].
- 87 studies use or create custom datasets, and only nine datasets are reused in more than ten studies [V] [@kaniewski2026systematic, p. 35]. Few datasets come with fixed training and test splits [V] [@kaniewski2026systematic, p. 39].
- 555 CWE types that may be used for mapping flaws appear in none of the analysed datasets [V] [@kaniewski2026systematic, p. 34].
- The authors warn of data leakage: popular datasets are probably in LLM training data, so high scores may reflect memory rather than skill [A] [@kaniewski2026systematic, p. 30; @kaniewski2026systematic, p. 39].
- They note that models often perform worse outside curated benchmarks [A] [@kaniewski2026systematic, p. 39; @kaniewski2026systematic, p. 40].
- They recommend combining SAST and LLMs as a path to industry use: SAST finds candidates and the LLM filters false alarms, or the reverse. No numbers support this [A] [@kaniewski2026systematic, p. 42].

### Limitations and weaknesses
- It is a mapping study, not a performance synthesis. It pools no precision, recall or F1 numbers, so it cannot answer RQ1 [I].
- The hybrid it recommends (SAST then LLM filtering) is excluded from its own corpus by design [I] [@kaniewski2026systematic, p. 8; @kaniewski2026systematic, p. 42].
- Only three databases were searched [I].
- Screening and quality checks are not transparent [I].
- Counting BERT-size models as LLMs blurs the line between "LLM" and "deep learning", which matters for our three-way comparison [I].
- Nearly 30% of the included studies are preprints, which were not peer-reviewed [I] [@kaniewski2026systematic, p. 8].
- The authors themselves name possible missed papers, selection bias and subjective classification [A] [@kaniewski2026systematic, p. 43].

### Gaps and future work this paper leaves open
The authors list seven open themes. These include repository-level detection and richer context, languages beyond C/C++, verified labels, datasets built after model training cutoffs, documented splits and workflow integration [A] [@kaniewski2026systematic, p. 38; @kaniewski2026systematic, p. 40; @kaniewski2026systematic, p. 41]. In our gap report this paper supports gap G2 (benchmarks probably sit in training data, and post-cutoff datasets are recommended), gap G3 (it recommends SAST-then-LLM filtering but does not evaluate it) and gap G5 (evidence is concentrated on C/C++ and Java). None of its directions asks for same-benchmark comparisons of LLMs with SAST and DL detectors [I].

### Why it matters for your research
This is the strongest source for RQ2 (why numbers differ across studies). Its dataset statistics were recomputed by the authors, which makes them more reliable than claims copied from abstracts. It is also a main "competing review" to position against. It covers LLMs only, while our review covers LLMs, SAST, DL and hybrids together [I].

### Connections to other papers
- Agreement G1 in the evidence matrix (realistic evaluation lowers scores): this review agrees with the primary studies there [@kaniewski2026systematic, p. 39].
- zhou2025large and sheng2025llms are the two other large reviews. All three find a C/C++, function-level focus. This one is the newest and the most systematic [I].
- qin2026review shares the "benchmarks inflate results" message but is a much weaker narrative review [I].
- It includes several of our primary studies, among them ahmed2026secvuleval, chakraborty2024revisiting, ding2025vulnerability, khare2025understanding, li2024iris, yildiz2025benchmarking and zhou2024comparison [I].
- The alarm-filtering studies du2026reducing and xiong2026sifting supply the hybrid evidence this review leaves out [@du2026reducing, p. 8; @xiong2026sifting, p. 18].

