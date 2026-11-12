## CASTLE: Benchmarking Dataset for Static Code Analyzers and LLMs Towards CWE Detection

> **Takeaway:** On CASTLE, a new set of 250 small hand-written C programs, the best LLMs (top score 977 for GPT-o3-Mini) beat all 13 static analysers and 2 formal verification tools (best 661). The programs are tiny and the result table has counting problems, so the win may not carry over to real code. The authors' own test on a 400-line program suggests it does not.

| Item | Detail |
|---|---|
| Authors | Richard A. Dubniczky, Krisztofer Zoltan Horvát, Tamás Bisztray, Mohamed Amine Ferrag, Lucas C. Cordeiro, Norbert Tihanyi |
| Year | 2025 |
| Venue | Lecture Notes in Computer Science (proceedings book chapter) |
| Status | Peer-reviewed (published chapter). Our copy is the arXiv version (2503.09433, v2), so numbers may differ from the published chapter. |
| Identifier | DOI 10.1007/978-3-031-98208-8_15 |
| Paper type | Benchmark dataset paper with a comparative evaluation |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
A benchmark is a fixed test set that lets different tools be scored in the same way. This paper builds a new benchmark for the C language called CASTLE. It then runs three kinds of tools on it. The first kind is static analysers (SAST), which read code and apply rules. The second is formal verification (FV) tools, which try to prove mathematically that a program cannot reach a bad state. The third is LLMs, chatbot-style AI models asked to review the code.

Each program has at most one flaw, and each flaw is tied to a CWE. A CWE (Common Weakness Enumeration) is a standard catalogue number for a type of weakness, for example CWE-476 for "null pointer dereference". On these short programs the large LLMs come out on top.

### How they did it
Security experts wrote the 250 programs by hand and marked the exact vulnerable line [@dubniczky2025castle, p. 6]. The authors ran 13 static analysers, 2 FV tools and 10 LLMs [@dubniczky2025castle, p. 11]. The LLMs were prompted zero-shot (no examples, no extra training) to act as a "professional security analyst". The prompt also told them the scoring rule: "5 points for each vulnerability you find, but get -1 for all false positives" [@dubniczky2025castle, p. 9].

Results are given as true and false positives (correct and wrong warnings), precision, recall and accuracy. The authors also define a new metric, the CASTLE Score. It gives points for each correct find, a bonus for more dangerous CWEs, points for staying quiet on clean programs, and penalties for each false alarm [@dubniczky2025castle, p. 10]. The maximum is 1,250 [@dubniczky2025castle, p. 12].

### Data and setup
- 25 CWEs × 10 programs = 250 programs: 150 vulnerable and 100 clean. They are 7–164 lines long, with a mean of 42 [@dubniczky2025castle, p. 6].
- The CWEs come mostly from the MITRE Top-25 list of most dangerous weaknesses [@dubniczky2025castle, p. 7].
- Tool versions are reported, for example CodeQL 2.20.1 and ESBMC 7.8.1 [@dubniczky2025castle, p. 11]. LLM temperature, model snapshots and costs are not reported.
- The dataset and tool wrappers are public [@dubniczky2025castle, p. 1].

### Key findings
- [V] CASTLE Scores: GPT-o3-Mini 977, GPT-o1 962, DeepSeek R1 956, GPT-4o 954. The best non-LLM tools are ESBMC 661 and CodeQL 634 [@dubniczky2025castle, p. 11].
- [V] Large LLMs have high recall: GPT-o3-Mini 78% with 63% precision, DeepSeek R1 90% with 47% precision. Small open models are weaker, for example Llama 3.1 8B with 20% precision [@dubniczky2025castle, p. 11].
- [A] CodeQL is the best SAST tool and finds 29% of the flaws, against a SAST average of 23% [@dubniczky2025castle, p. 12]. [I] The paper writes this as "45/150", which is 30%; 29% matches a different denominator in the table (see Limitations).
- [V] Some SAST tools are swamped by noise. Splint raised 1,027 false alarms and CodeThreat 1,101, which gave them negative scores [@dubniczky2025castle, p. 11].
- [V] Combining two non-LLM tools helps: ESBMC plus CodeQL scores 814, up from 661 for ESBMC alone [@dubniczky2025castle, p. 13]. No LLM-plus-tool combination was tested.
- [A] The authors say reasoning models "consistently produced fewer false positives" [@dubniczky2025castle, p. 14]. [I] Their own table shows this only for OpenAI's o-series: DeepSeek R1 made 166 false alarms against 116 for GPT-4o [@dubniczky2025castle, p. 11].
- [A] FV tools raise almost no false alarms but cannot detect issues such as SQL injection or hard-coded passwords [@dubniczky2025castle, p. 12].
- [A] In a preliminary test on one program of more than 400 lines, LLMs raised more false alarms and most missed the single hidden flaw. No numbers are given [@dubniczky2025castle, p. 14].

### Limitations and weaknesses
- [I] Counting problem: there are 150 vulnerable programs, but true positives plus missed flaws add up to 154–179 for all 10 LLMs and 155–157 for four SAST tools [@dubniczky2025castle, p. 11]. Recall and accuracy therefore use unclear denominators. Quote exact numbers with this caveat.
- [V] LLMs returned the content of the flagged line so that small line-number errors could be corrected [@dubniczky2025castle, p. 8]. [I] No such help is described for the SAST tools, and the prompt reveals the scoring rule. Both favour the LLMs.
- [A] The programs are tiny and single-file. Real flaws often span many files [@dubniczky2025castle, p. 14].
- [I] The CASTLE Score weights are the authors' own choice and are not checked against any outside standard.
- [I] There are no per-CWE results, no statistical tests, and no costs. The authors say repeated runs differ by under 3%, but do not say how many repeats there were [@dubniczky2025castle, p. 14].
- [A] Because the tests are public, tool vendors could tune for them; the authors suggest refreshing the dataset [@dubniczky2025castle, p. 14].

### Gaps and future work this paper leaves open
- [A] The authors call for refreshing the tests and studying scale-up to large codebases [@dubniczky2025castle, p. 14].
- [I] The prompt that reveals the scoring scheme and the new CASTLE Score both feed gap G1: studies use incompatible metrics and no shared protocol.
- [I] Single-file synthetic programs leave gap G2 open (a fair three-way test on real, recent code with repository context).
- [I] No hybrid LLM-plus-tool run is tested, and no cost is reported, so the paper says nothing on gap G4 (independent tests of hybrids) or gap G6 (cost per real flaw found).

### Why it matters for your research
CASTLE has the widest tool panel in our set: 13 SAST tools including commercial ones, 2 FV tools and 10 LLMs, all on one controlled benchmark with line-level labels. It is the cleanest evidence that frontier LLMs beat SAST on small, self-contained C code. For a comparative review it is just as useful as a contrast case. Its own large-file test, together with the real-code studies, shows why "who wins" depends on the size and realism of the code.

### Connections to other papers
- It sits on the "LLMs win" side of contradiction C3, together with gnieciak2025large [@gnieciak2025large, p. 10]. On synthetic Java and C/C++ suites, CodeQL beats LLMs on accuracy [@khare2025understanding, p. 9]. At project scale, most tools produce mostly false warnings [@li2026llm, p. 11].
- It is the "for" side of contradiction C4 (does reasoning reduce false alarms?). In deininger2026open, reasoning lowers DeepSeek-V3.2's specificity, its ability to correctly clear safe code, from 0.52 to 0.37 [@deininger2026open, p. 20].
- Its CodeQL recall of 29% supports agreement G4 (SAST recall is low outside synthetic suites), as do zhou2024comparison (preprint) [@zhou2024comparison, p. 6] and li2026llm [@li2026llm, p. 7].
