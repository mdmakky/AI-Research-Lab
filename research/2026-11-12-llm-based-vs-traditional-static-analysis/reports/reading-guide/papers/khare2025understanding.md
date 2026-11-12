## Understanding the Effectiveness of Large Language Models in Detecting Security Vulnerabilities

> **Takeaway:** Across 5,000 short code samples, 16 prompted LLMs reached only modest accuracy, and CodeQL beat the best LLM on accuracy on all three synthetic test suites. LLMs beat CodeQL on some vulnerability types, but on real code neither the LLMs nor the deep-learning tools clearly beat simply calling every sample vulnerable.

| Item | Detail |
|---|---|
| Authors | Avishree Khare, Saikat Dutta, Ziyang Li, Alaia Solko-Breslin, Rajeev Alur, Mayur Naik |
| Year | 2025 |
| Venue | 2025 IEEE Conference on Software Testing, Verification and Validation (ICST) |
| Status | Peer-reviewed. Our copy is the arXiv version (2311.16169, v3, October 2024). The arXiv record starts in 2023 while the conference is 2025; this year difference is normal and harmless. |
| Identifier | DOI 10.1109/icst62969.2025.10988968 |
| Paper type | Empirical study |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
This paper asks how good off-the-shelf LLMs (chatbot-style AI models) are at spotting security flaws in a single function. It covers all three families in our review. The LLMs are compared with CodeQL, a widely used static analysis (SAST) tool that searches code with hand-written rules. They are also compared with two deep-learning (DL) detectors, DeepDFA and LineVul. A DL detector is a smaller neural network trained specifically on labelled examples of vulnerable and safe code.

The answer is sobering. The LLMs are only somewhat better than guessing. CodeQL wins overall on artificial test suites. The LLMs do better than CodeQL on a few specific vulnerability types.

### How they did it
The authors prompted 16 LLMs, from small open models to GPT-4, with three prompts [@khare2025understanding, p. 4]. The Basic prompt asks whether there is any vulnerability. The CWE-specific prompt names the target weakness type; a CWE is a standard catalogue number for a type of weakness. The CWE-DF prompt asks the model to trace dataflow first. That means following data from a source (where untrusted input enters), through any sanitizer (code that cleans it), to a sink (where it could do harm). The models got no extra training, and temperature was set to 0 to make answers as repeatable as possible [@khare2025understanding, p. 5].

Each answer is a yes/no verdict per code sample. Results are reported as accuracy, precision, recall and F1. Accuracy is the share of all verdicts that are correct. Precision is the share of "vulnerable" verdicts that are right. Recall is the share of real flaws found. F1 combines precision and recall.

### Data and setup
- Five datasets with 1,000 samples each, half vulnerable and half safe, covering 25 CWEs [@khare2025understanding, p. 5].
- Three are synthetic, meaning artificial test suites written to contain textbook flaws: OWASP Benchmark (Java), Juliet Java and Juliet C/C++. Two are real-world: CVEFixes Java and CVEFixes C/C++, taken from fixes of publicly reported vulnerabilities [@khare2025understanding, p. 3].
- Comments and revealing names were removed, so the models could not read the answer from the code [@khare2025understanding, p. 5].
- CodeQL ran on the synthetic datasets only, because real projects must be built (compiled) first [@khare2025understanding, p. 7].
- The DL tools were tested on CVEFixes C/C++, after training on Juliet, CVEFixes or another dataset called BigVul [@khare2025understanding, p. 9].
- Each setup ran once [@khare2025understanding, p. 10].

### Key findings
- [V] Taking the best model and prompt for each dataset, average accuracy is 62.8%. Best accuracy on synthetic data is 10.5% higher on average than on real-world data [@khare2025understanding, p. 5].
- [V] CodeQL beats the best LLM on accuracy on all three synthetic suites: OWASP 0.63 vs 0.60, Juliet Java 0.94 vs 0.76, Juliet C/C++ 0.72 vs 0.65 [@khare2025understanding, p. 9].
- [V] LLMs beat CodeQL on some CWEs, for example path traversal (CWE-22), command injection (CWE-78), null pointer (CWE-476) and use-after-free (CWE-416). CodeQL is better on integer overflow (CWE-190) by 11–21% [@khare2025understanding, p. 8].
- [V] The dataflow prompt raises real-world F1 by up to 0.18 [@khare2025understanding, p. 5]. In a manual check, the model found the right sources and sinks in 18 of 20 real Java samples [@khare2025understanding, p. 6].
- [A] Bigger models are not reliably better. Qwen-2.5 with 14 or 32 billion parameters beat GPT-4 on real-world data [@khare2025understanding, p. 5].
- [V] On CVEFixes C/C++, DL tools reach F1 0.02–0.64 depending on the training data, and LineVul trained on BigVul collapses to 0.02. The best LLM, Qwen-2.5-32B, reaches 0.65 [@khare2025understanding, p. 10].
- [I] On a half-and-half dataset, answering "vulnerable" every time gives F1 0.667. Qwen's 0.65 and every DL score are below that. Several LLM setups behave exactly like this always-vulnerable rule [@khare2025understanding, p. 16].
- [A] Missing wider context (code outside the function) is the main reason for poor results on real C/C++ [@khare2025understanding, p. 7].

### Limitations and weaknesses
- [I] The best of 48 model-and-prompt combinations was picked after seeing the test results [@khare2025understanding, p. 5]. This favours the LLMs against a single CodeQL setup.
- [I] CodeQL was never run on real code, where its rules are less well tuned.
- [I] Half-and-half datasets are far from reality, where few functions are vulnerable. Precision would be much lower at a realistic rate.
- [I] The public datasets predate the models' training data cutoff, so models may have seen them (data contamination). This is not discussed beyond renaming identifiers.
- [A] Single runs, and a possible bias from the choice of models and datasets [@khare2025understanding, p. 10].
- [I] There are no statistical tests, no costs, and no released code or samples in our version.

### Gaps and future work this paper leaves open
- [A] The authors propose "neuro-symbolic" hybrids, in which an LLM infers the sources, sinks and sanitizers and a static analyser then reasons over them [@khare2025understanding, p. 11].
- [I] CodeQL on synthetic data only is a named limitation in gap G2: there is still no fair three-family test on real, recent code with repository context.
- [I] Always-vulnerable rows among the best F1 scores are part of the evidence for gap G1: published results are rarely checked against trivial baselines or realistic rates.
- [I] The proposed hybrid is close to how IRIS works (LLM-inferred sources and sinks plus CodeQL) [@li2026llm, p. 4]. Whether such hybrids hold up in independent tests is gap G4.

### Why it matters for your research
This is a peer-reviewed study that covers all three families: LLMs, SAST and DL. It is the main counterweight to the "LLMs beat SAST" papers: on synthetic suites CodeQL still wins overall. It is also the best source in our set for which vulnerability types suit LLMs (RQ4): self-contained flaws go well, context-dependent ones go badly. Finally, it shows how a balanced dataset can make near-trivial behaviour look like a decent F1 score.

### Connections to other papers
- It is the "SAST wins" side of contradiction C3, against gnieciak2025large and dubniczky2025castle [@gnieciak2025large, p. 10; @dubniczky2025castle, p. 11].
- Agreement G1 (realistic evaluation collapses performance): its 10.5% synthetic-to-real drop matches the larger drops in ding2025vulnerability [@ding2025vulnerability, p. 7] and deininger2026open [@deininger2026open, p. 8].
- Agreement G3 (LLMs over-flag): its always-vulnerable rows match ding2025vulnerability, where GPT-4 labels both versions of a vulnerable/fixed pair as vulnerable in 71.63% of pairs [@ding2025vulnerability, p. 9].
- Agreement G5: its CodeQL OWASP result (precision 0.58, recall 0.96) is replicated by xiong2026sifting (60.3%, 97.0%) [@xiong2026sifting, p. 11].
- Agreement G6 (missing context causes failures) links it to risse2025top and li2026llm [@risse2025top, p. 9; @li2026llm, p. 7].
