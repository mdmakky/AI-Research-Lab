## Evaluating large language models for multilingual vulnerability detection at dual granularities

> **Takeaway:** Across seven programming languages, only one setup (GPT-4o, fine-tuned and given retrieved examples) clearly beat smaller fine-tuned code models, and only on balanced test data. On realistic, imbalanced data the smaller models won. No static-analysis tool was tested.

| Item | Detail |
|---|---|
| Authors | Honglin Shu, Michael Fu, Junji Yu, Dong Wang, Chakkrit Tantithamthavorn, Junjie Chen, Yasutaka Kamei |
| Year | 2026 |
| Venue | Empirical Software Engineering (journal) |
| Status | Peer-reviewed journal article. Our copy is the arXiv version 2506.07503v2 (March 2026), not the typeset journal version. |
| Identifier | DOI 10.1007/s10664-026-10832-4; arXiv 2506.07503 |
| Paper type | Empirical comparison (LLMs against fine-tuned pre-trained code models) |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
This paper compares two kinds of AI models for finding security flaws in code. The first kind are PLMs (pre-trained language models for code), such as CodeBERT or CodeT5. These are smaller models that are fine-tuned, meaning trained further on labelled examples of vulnerable and safe code. In our project they count as deep-learning (DL) detectors. The second kind are LLMs (large language models), such as GPT-4o, which are much bigger and are often just given instructions in a prompt.

The paper tests seven languages: C, C++, C#, Go, Java, JavaScript and Python. It asks two questions. Can a model tell whether a whole function (a named block of code) is vulnerable? And can it point to the vulnerable lines inside that function? The main lesson is that the winner depends on how the test data is built [V] [@shu2026evaluating, p. 17; @shu2026evaluating, p. 40].

### How they did it
The authors used five LLMs and several ways of using them [V] [@shu2026evaluating, p. 10; @shu2026evaluating, p. 12; @shu2026evaluating, p. 14]:
- zero-shot prompting: the model gets only the question;
- few-shot prompting: the model also gets three similar solved examples, picked from the training data by a text-search method (BM25);
- instruction tuning: the LLM is itself fine-tuned on the task, then prompted. The best setup combined instruction tuning with few-shot examples.

They compared these with eight PLMs and embedding models, and with "dummy" baselines that call everything vulnerable or everything safe [V] [@shu2026evaluating, p. 9; @shu2026evaluating, p. 11]. A baseline is a simple reference method; beating it shows a model learned something real.

Main metrics were accuracy (share of correct answers) and F1 (a single score that balances precision, the share of flagged items that are truly vulnerable, against recall, the share of real flaws found) [V] [@shu2026evaluating, p. 14; @shu2026evaluating, p. 15].

### Data and setup
- The data is REEF: real vulnerability fixes from 2016–2023. The version before the fix is labelled vulnerable, the version after the fix safe [V] [@shu2026evaluating, p. 6].
- Function level: 20,165 functions, about half vulnerable, with 2,026 in the test set [V] [@shu2026evaluating, p. 7].
- Line level: 8,134 vulnerable functions, 810 in the test set [V] [@shu2026evaluating, p. 8].
- Functions longer than 512 tokens (word pieces) were removed, so all code is short [V] [@shu2026evaluating, p. 6].
- Extra tests: newer 2024–2025 code, to check whether models just memorised old data, and an imbalanced test set where only about 17% of functions are vulnerable [V] [@shu2026evaluating, p. 38; @shu2026evaluating, p. 39].
- The split into training and test data was random by function [V] [@shu2026evaluating, p. 7]. There are no significance tests and no repeated runs [I].

### Key findings
- On balanced data, the best LLM setup (GPT-4o, instruction-tuned plus few-shot) reached accuracy 0.7196 against 0.6037 for the best PLM, CodeT5P. Their F1 scores were essentially tied (0.7069 vs 0.7075) [V] [@shu2026evaluating, p. 17].
- The "flag everything" dummy reached F1 0.6693, so the best F1 is only a little above this trivial level [V] [@shu2026evaluating, p. 17].
- LLMs used only with prompts were near chance at function level, with accuracy around 0.48–0.51 for zero-shot [V] [@shu2026evaluating, p. 17].
- At line level, the best LLM setup reached F1 0.6641 against 0.4841 for CodeT5P [V] [@shu2026evaluating, p. 23; @shu2026evaluating, p. 26].
- On the imbalanced test, the ranking flipped. UniXcoder (a PLM) had the best F1, 0.4626, against 0.4010 for the best GPT-4o setup [V] [@shu2026evaluating, p. 40; @shu2026evaluating, p. 41].
- On 2024–2025 code, function-level accuracy held (0.7874), but line-level F1 fell from 0.6641 to 0.3450 [V] [@shu2026evaluating, p. 39].
- Memory-safety flaws were hardest to locate. For CWE-787 (writing outside a memory buffer; a CWE is a standard weakness category), only 6.25% were located correctly at line level [V] [@shu2026evaluating, p. 30].
- Fine-tuning GPT-4o cost $86.07 for the function task, about 15 times more than a local PLM training run [V] [@shu2026evaluating, p. 42].

### Limitations and weaknesses
- No static-analysis tool (SAST) was tested. SAST tools are rule-based programs that scan code for known bad patterns. So this paper only supports LLM-versus-DL claims, not LLM-versus-SAST claims [I].
- The headline result rests on one configuration. Every other LLM setup was near chance [I] [@shu2026evaluating, p. 17].
- Possible leakage: each vulnerable function and its fixed twin can land on opposite sides of the random split. Few-shot search could then hand the model a near-copy with the opposite label. This is our hypothesis. The steady accuracy on 2024–2025 code argues partly against it [I] [@shu2026evaluating, p. 7; @shu2026evaluating, p. 39].
- Line-level accuracy may be inflated, because metrics seem to be computed over padded empty line slots. This is our arithmetic, not confirmed by the authors [I] [@shu2026evaluating, p. 8; @shu2026evaluating, p. 23].
- The text claims GPT-4o beat all models in all seven languages, but in JavaScript CodeT5P scored higher (0.7062 vs 0.6642) [V] [@shu2026evaluating, p. 21; @shu2026evaluating, p. 22].
- The authors note only one dataset, short functions and only exact-copy leakage filtering [A] [@shu2026evaluating, p. 43; @shu2026evaluating, p. 44].

### Gaps and future work this paper leaves open
The authors ask for larger multilingual benchmarks and better learning strategies [A] [@shu2026evaluating, p. 47]. In our gap report, this paper is evidence for gap G1 (results are rarely checked against trivial baselines and realistic class ratios), gap G2 (rankings reverse with class balance, and no SAST arm), gap G5 (the only multi-language LLM study in our corpus, including Go, has no SAST arm) and gap G6 (it is one of the few studies that report money cost).

### Why it matters for your research
It is our clearest example that the class ratio of the test set can flip which model family wins (RQ2). It also gives per-language and per-CWE results (RQ4) and cost figures (RQ3). For RQ1, use it for LLM-versus-DL only [I].

### Connections to other papers
- Contradiction C5 in the evidence matrix (class balance flips rankings): yildiz2025benchmarking and deininger2026open show the same effect [@yildiz2025benchmarking, p. 7; @deininger2026open, p. 8].
- Agreement G8 (prompt-only LLMs trail adapted models): fu2023chatgpt and zhou2024comparison agree [@fu2023chatgpt, p. 4; @zhou2024comparison, p. 10].
- Agreement G10 (trivial baselines are competitive): tashenova2026real and lu2025lab also report them [@tashenova2026real, p. 8; @lu2025lab, p. 14].
- Contradiction C4 (does reasoning help?): here, reasoning LLMs were near chance [@shu2026evaluating, p. 37].
- Agreement G9 (LLM cost far exceeds the alternatives) uses this paper's cost figure.

