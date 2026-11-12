## RepoAudit: An Autonomous LLM-Agent for Repository-Level Code Auditing

> **Takeaway:** In its authors' evaluation, the RepoAudit LLM agent found 40 real memory bugs with 78.43% precision in 15 C/C++ projects at about $2.54 per project, far ahead of two industrial analysers. An independent later study found it missed almost all known vulnerabilities on different targets and cost much more, so the result is contested.

| Item | Detail |
|---|---|
| Authors | Jinyao Guo, Chengpeng Wang, Xiangzhe Xu, Zian Su, Xiangyu Zhang |
| Year | 2025 (our copy is arXiv version 3, 29 May 2025) |
| Venue | arXiv. Our copy carries the footer of the ICML 2025 proceedings (PMLR 267) |
| Status | Preprint in our records, because we hold the arXiv copy. It appears to be the ICML 2025 camera-ready text, which we did not compare |
| Identifier | doi:10.48550/arxiv.2501.18160 (arXiv 2501.18160) |
| Paper type | Tool paper with empirical evaluation |
| Relevance to us | High: RQ1, RQ3, RQ4, RQ5 |

### In plain words
Code auditing means reviewing code to find bugs. A large language model (LLM, an AI model trained on huge amounts of text and code) can read code without compiling it. But a whole repository (all the code of a project) is too big to fit into one prompt, and LLMs sometimes "hallucinate", that is, state things that are not true [A] [@guo2025repoaudit, p. 1].

RepoAudit is an LLM agent. An agent is an LLM that works in several steps and decides by itself what to read next. RepoAudit follows how a value moves through the program (data flow), one function at a time. It stores what it has learned in a memory and then checks its own findings before reporting them [V] [@guo2025repoaudit, p. 5]. It targets three memory bugs in C/C++: null pointer dereference (NPD, using a pointer that points to nothing), memory leak (MLK, memory that is never freed) and use-after-free (UAF, using memory after it has been released) [V] [@guo2025repoaudit, p. 7].

### How they did it
RepoAudit has three parts [V] [@guo2025repoaudit, p. 5]:

1. An initiator finds starting points, such as places where a value is set to NULL, using a code parser.
2. An explorer asks the LLM about one function at a time and moves to calling or called functions only when needed.
3. A validator checks that the reported steps happen in a possible order and asks the LLM whether the path conditions can all be true together.

It follows a bug across at most four functions [V] [@guo2025repoaudit, p. 9]. The default model was Claude 3.5 Sonnet at temperature 0 (the most repeatable setting) [V] [@guo2025repoaudit, p. 7].

Comparison tools were two industrial static analysers, Meta Infer and Amazon CodeGuru, plus simple LLM prompting and another LLM agent, LLMDFA [V] [@guo2025repoaudit, p. 8; @guo2025repoaudit, p. 13]. No open-source SAST tool (static application security testing, such as CodeQL or Semgrep) and no deep-learning detector was tested [I].

### Data and setup
The benchmark is 15 C/C++ projects, 5 per bug type, taken from bug reports in earlier papers. They range from about 2,000 to 1.4 million lines of code [V] [@guo2025repoaudit, p. 7]. These projects contain 21 previously reported bugs [V] [@guo2025repoaudit, p. 17]. A field study then ran RepoAudit on 9 further open-source projects [V] [@guo2025repoaudit, p. 8].

Precision is the share of reports that are real bugs. "Recall" here means only the share of the 21 known bugs that RepoAudit found again. Recall against all bugs in the projects was not measured [V] [@guo2025repoaudit, p. 17]. Who judged RepoAudit's own reports as true or false is not reported; Infer and CodeGuru reports were checked manually [V] [@guo2025repoaudit, p. 14]. The code is public [V] [@guo2025repoaudit, p. 1].

### Key findings
- [V] RepoAudit found all 21 known bugs plus 19 new ones: 40 true positives and 11 false positives, a precision of 78.43% [@guo2025repoaudit, p. 7; @guo2025repoaudit, p. 8].
- [V] Average cost per project was 0.44 hours and $2.54, or $0.95 per true bug. The most expensive project cost $18.15 [@guo2025repoaudit, p. 7; @guo2025repoaudit, p. 8].
- [V] Meta Infer could analyse only 8 projects (others failed to build or crashed) and found 7 true bugs with 2 false positives. Amazon CodeGuru found 0 true bugs and 18 false positives [@guo2025repoaudit, p. 8; @guo2025repoaudit, p. 15].
- [V] Simple prompting found far fewer bugs: 1 with single-function prompting and 10 with multi-function prompting [@guo2025repoaudit, p. 8].
- [V] Removing the validator raised false positives by 245.45%. Removing program abstraction (the step that keeps only the statements relevant to the bug type) cut true positives by 47.50% [@guo2025repoaudit, p. 8; @guo2025repoaudit, p. 15].
- [V] With reasoning models, precision was 82.35–88.46% with 42–46 true positives (DeepSeek R1: $0.57 per project, OpenAI o3-mini: $0.30) [@guo2025repoaudit, p. 16].
- [A] In the field study, RepoAudit reported 185 new bugs, of which 174 were confirmed or fixed by developers [@guo2025repoaudit, p. 9].

### Limitations and weaknesses
The authors name hallucinated false positives and missed bugs, cost that grows with the number of starting points, the four-function limit, and the risk of sending private code to LLM providers [A] [@guo2025repoaudit, p. 9; @guo2025repoaudit, p. 10].

Our own concerns [I]:

- The tool's own authors evaluated it, and the judging procedure for its reports is not described.
- True recall is unknown; only 21 known bugs were checked.
- The industrial baselines were handicapped by build failures and crashes. No build-free open-source SAST tool was compared.
- The benchmark bugs are public, so the model may have seen them in training. This is not discussed.
- One run per setting, no significance test, and small inconsistencies ("ten" vs "nine" field-study projects).
- The bugs are memory-safety defects, not necessarily exploitable security vulnerabilities.

### Gaps and future work this paper leaves open
- Gap G4 (independent replication of hybrid tools): the authors' and the independent results disagree, and no study separates target, metric and labeller effects.
- Gap G5 (other languages): the authors plan to extend RepoAudit to Python and JavaScript [A] [@guo2025repoaudit, p. 10].
- Gap G6 (full cost comparison): this paper reports cost, but per project and for small projects only; human checking time is not included [I].

### Why it matters for your research
RepoAudit is the main agent-style detector in our corpus with explicit cost data and a direct comparison against industrial analysers (RQ1, RQ3). The clash between its self-reported results and an independent evaluation shows how strongly the evaluation setup shapes reported numbers (RQ2) [I].

### Connections to other papers
- li2026llm, an independent peer-reviewed study, is the main counter-evidence (contradiction C2 in the evidence matrix). There, RepoAudit found 0 of 110 known C/C++ vulnerabilities, had a sampled false discovery rate (SFDR, the share of sampled warnings that are false) of 92.77% on real projects, and cost $172.77 per project on average and up to $1,247.66 [V] [@li2026llm, p. 7; @li2026llm, p. 11; @li2026llm, p. 16].
- The two studies differ in targets, code versions, bug types, project size, metric (precision vs recall and SFDR) and labeller (li2026llm uses the Codex LLM, then checks manually) [I]. li2026llm traces all 108 misses of one RepoAudit configuration to incomplete coverage of library functions [V] [@li2026llm, p. 7]. Our reading is that this coverage may explain part of the gap, but the question is unresolved [I].
- Agreement G6 in the evidence matrix (missing context is a shared failure cause) and agreement G9 (LLM cost varies by orders of magnitude) both draw on this pair of papers.
- li2024iris is the other contested hybrid tool (contradiction C6). Unlike IRIS, RepoAudit needs no build [V] [@guo2025repoaudit, p. 15].
- On contradiction C4 (does reasoning reduce false positives?), RepoAudit's higher precision with reasoning models counts "for"; tan2026think finds reasoning mainly raises recall [@tan2026think, p. 6].

