## To Think or Not to Think: Evaluating LLM Reasoning and Agents in Vulnerability Detection

> **Takeaway:** In a carefully controlled experiment with four open LLMs, "thinking" modes and multi-agent designs mostly made models flag more code as vulnerable, which raises F1 without making them better at telling vulnerable code from its fixed version. They also cost several times more energy, and the quality of an explanation did not reveal whether the answer was right.

| Item | Detail |
|---|---|
| Authors | Hua Beng Tan, Ratnadira Widyasari, Merve Astekin, Arda Goknil, Hasan Sözer, Yan Naing Tun, Erik Johannes Husom, Lwin Khin Shar, Lingxiao Jiang |
| Year | 2026 |
| Venue | Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering (ASE 2026) |
| Status | Peer-reviewed (conference). Our copy is the publisher's version of record, supplied by you |
| Identifier | doi:10.1145/3832783.3837521 |
| Paper type | Controlled (factorial) empirical study |
| Relevance to us | Medium: RQ1 (LLM-only), RQ2, RQ3, RQ5 |

### In plain words
Large language models (LLMs, AI models trained on huge amounts of text and code) are now often used in two newer ways. Some have a "thinking" or reasoning mode: the model writes out a long chain of reasoning before answering. Others are used as agents: several LLM "roles" (for example, an author and a reviewer) talk to each other before deciding.

Both are claimed to help in finding vulnerabilities (security flaws in code). Earlier studies tested them separately and under different settings. This paper tests them together in one controlled design, so that each effect can be separated [A] [@tan2026think, p. 1; @tan2026think, p. 2]. It also asks whether "thinking" produces better explanations.

### How they did it
The design is factorial: every combination of factors is tested [V] [@tan2026think, p. 3]. The factors were:

1. Four open models: Nemotron-Nano-8B, Nemotron-Super-49B, Qwen3-4B and Qwen3-30B-A3B.
2. Thinking mode on or off.
3. Zero-shot (no examples) or few-shot (a few solved examples in the prompt).
4. Four designs: no agent, a single agent, a dual agent (one proposes, one reviews and decides) and a multi-agent team with four roles [V] [@tan2026think, p. 4].

That gives 64 configurations. Extra "call-matched" runs gave a single model the same number of calls as the agent teams, for example by letting it revise its own answer [V] [@tan2026think, p. 11]. Explanations were rated by two blinded humans (who did not know which mode produced them) and by an LLM judge [V] [@tan2026think, p. 5].

There are no SAST tools (static analysers) and no fine-tuned deep-learning detectors [I].

### Data and setup
The data are PrimeVul Pair: 435 vulnerable C/C++ functions, each paired with its fixed (benign) version, 870 functions in total [V] [@tan2026think, p. 3]. The model sees one function at a time, never the pair.

Two scores matter. F1 combines precision (share of flagged functions that are vulnerable) and recall (share of vulnerable functions flagged). Pair-wise correctness (P-C) is the share of pairs where both the vulnerable and the fixed version are labelled correctly. It tests whether the model really sees the flaw [V] [@tan2026think, p. 5].

Models ran at temperature 0 (the most repeatable setting) with one run per configuration [V] [@tan2026think, p. 4]. Code, prompts and data are public [V] [@tan2026think, p. 12].

### Key findings
- [V] Without agents, thinking raised mean F1 from 0.31 to 0.41 (Wilcoxon test p = 0.023; Cohen's d = 1.37, a large effect). Accuracy barely changed (0.518 vs 0.523), so the gain came from flagging more code [@tan2026think, p. 6].
- [V] The best single-model F1 was 0.620, and the best pair-wise correctness was only 22.5% [@tan2026think, p. 6].
- [V] The dual-agent design had the highest mean F1 (0.634) because it flagged 88.2% of all functions; its false-positive rate was 0.880 and its pair-wise correctness only 6.2% [@tan2026think, p. 7].
- [V] F1 and P-C ranked designs differently: the multi-agent team had the best P-C in 11 of 16 settings, the dual agent in none [@tan2026think, p. 7; @tan2026think, p. 8].
- [V] In the dual-agent and team designs, thinking lowered F1 (by 0.054 and 0.066), while pair-wise correctness still rose slightly [@tan2026think, p. 8].
- [V] A single model that revised its own answer four times reached mean P-C 24.7, vs 21.9 for the multi-agent team. The authors conclude that much of the agent benefit is simply extra computing budget [@tan2026think, p. 11].
- [V] Thinking used 2.7–4.4 times more energy. All 64 configurations together cost about $2,448 and 481 kWh [@tan2026think, p. 10].
- [V] In blinded ratings, explanations of correct and wrong answers scored the same (all p > 0.3) [@tan2026think, p. 9].

### Limitations and weaknesses
The authors note: one run per configuration, prompt and design choices that are representative rather than optimal, a rating scheme that measures perceived quality rather than truthfulness, and function-level data with no project context [A] [@tan2026think, p. 11].

Our own concerns [I]:

- On this 50/50 dataset, a classifier that flags everything scores F1 0.667. No configuration beats it (best 0.665–0.666), so the "best" F1 is at the flag-everything level.
- A random guesser can reach at most 25% pair-wise correctness. Almost all results are at or below that level.
- Training-data contamination is not discussed; PrimeVul is public.
- Tests on 8 or 16 configuration averages have little statistical power.

### Gaps and future work this paper leaves open
- Gap G1 (trivial baselines and realistic prevalence): this paper shows why F1 on balanced data must be compared with a flag-everything baseline, which it does not report.
- Gap G2 (same-benchmark comparison with SAST and deep learning): no traditional or deep-learning baseline is included [I]. The authors call for repository-level settings with dependency resolution, retrieval and tools [A] [@tan2026think, p. 11].
- Gap G6 (cost): it gives detailed energy and dollar costs, but not cost per confirmed vulnerability [I].

### Why it matters for your research
It is the most rigorous test in our corpus of whether reasoning and agents help, and one of only two primary studies in our corpus (with deininger2026open) that test their main comparison for statistical significance [I]. For RQ3 it shows that higher F1 can be bought by flagging more, at real energy cost. For RQ5 it warns that a convincing explanation is not evidence of a correct answer [@tan2026think, p. 9].

### Connections to other papers
- yildiz2025benchmarking finds the same pattern with GPT models: decent F1 but near-random pair-wise accuracy. Both feed agreement G3 in the evidence matrix (LLMs over-flag and cannot separate vulnerable from fixed code) [@yildiz2025benchmarking, p. 8; @tan2026think, p. 7].
- On whether reasoning reduces false positives (contradiction C4), this paper is evidence "against": thinking raises recall, not discrimination. dubniczky2025castle reports the opposite, and deininger2026open finds the effect depends on the model [@dubniczky2025castle, p. 14; @deininger2026open, p. 17].
- ding2025vulnerability, which introduced the pair-wise metric used here, also finds all model families near or below chance on PrimeVul pairs [@ding2025vulnerability, p. 9].

