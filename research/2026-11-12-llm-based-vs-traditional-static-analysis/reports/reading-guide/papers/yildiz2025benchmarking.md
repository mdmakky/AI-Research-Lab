## Benchmarking LLMs and LLM-based Agents in Practical Vulnerability Detection for Code Repositories

> **Takeaway:** On a new benchmark of 879 real C/C++ vulnerabilities, each paired with its fixed version, GPT-4o and GPT-4o-mini reached F1 scores of about 48–66% but correctly labelled both versions of a pair in at most about 20% of cases. On realistic, mostly-safe data their F1 fell to about 5–12%, so F1 on balanced data greatly overstates how useful these detectors are.

| Item | Detail |
|---|---|
| Authors | Alperen Yildiz, Sin G Teo, Yiling Lou, Yebo Feng, Chong Wang, Dinil Mon Divakaran |
| Year | 2025 |
| Venue | Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025, Volume 1: Long Papers) |
| Status | Peer-reviewed (conference). Our copy is the published ACL Anthology version |
| Identifier | doi:10.18653/v1/2025.acl-long.1490 |
| Paper type | Benchmark paper with comparative evaluation |
| Relevance to us | Medium: RQ1 (LLM-only), RQ2, RQ5 |

### In plain words
Real vulnerabilities often depend on code outside the function where they appear. A practical detector should therefore look at related functions too. It should also tell a vulnerable function apart from its fixed version, which usually looks almost the same.

The authors build a benchmark, JITVul, for "just-in-time" detection: checking code at the moment a change (commit) is made [A] [@yildiz2025benchmarking, p. 1]. They use it to compare plain large language models (LLMs, AI models trained on huge amounts of text and code) with LLM agents. An agent is an LLM that can call tools, here tools that look up the functions that call or are called by the target function [V] [@yildiz2025benchmarking, p. 6].

### How they did it
Three detection methods were compared [V] [@yildiz2025benchmarking, p. 5; @yildiz2025benchmarking, p. 6]:

1. Plain LLM: sees only the target function.
2. Dependency-augmented LLM: also sees the five most similar calling or called functions, chosen by word overlap.
3. ReAct agent: an LLM that alternates between reasoning and tool calls to fetch callers, callees and definitions on demand.

Each method was tried with four prompting styles: plain, chain-of-thought (asking the model to reason step by step), few-shot (adding 10 hand-made example pairs) and both together [V] [@yildiz2025benchmarking, p. 6]. The main models were GPT-4o-mini and GPT-4o at temperature 0 (the most repeatable setting); Llama-3.1-8B and DeepSeek-Coder-V2-16B appear in an appendix [V] [@yildiz2025benchmarking, p. 6; @yildiz2025benchmarking, p. 15].

No SAST tools (static analysers) and no fine-tuned deep-learning detectors were tested [V] [@yildiz2025benchmarking, p. 5].

### Data and setup
JITVul contains 879 CVEs (public IDs for known vulnerabilities) from the PrimeVul dataset, covering 91 weakness types (CWEs), with at most 10 per type [V] [@yildiz2025benchmarking, p. 4]. Each CVE gives two samples: the function as it was when the vulnerability was introduced, and the function after the fix. That makes 1,758 samples, half vulnerable [V] [@yildiz2025benchmarking, p. 5]. The repositories are large, on average about 989,000 lines of code, and 91% C [V] [@yildiz2025benchmarking, p. 5].

Two scores were used. F1 combines precision (share of flagged samples that are vulnerable) and recall (share of vulnerable samples flagged). Pairwise accuracy (pAcc) is the share of pairs where both versions are labelled correctly [V] [@yildiz2025benchmarking, p. 6]. Code and data are released [V] [@yildiz2025benchmarking, p. 2].

### Key findings
- [V] With GPT-4o and GPT-4o-mini, F1 ranged from about 48% to 66%, but pairwise accuracy only from 1.02% to 20.17% [@yildiz2025benchmarking, p. 6].
- [V] ReAct agents had the highest pairwise accuracy for every prompting style with the GPT models, by up to 16.61 points, while the non-agent methods usually had higher F1 [@yildiz2025benchmarking, p. 7].
- [V] Some settings labelled over 90% of samples vulnerable, and precision was about 50% for all methods, so F1 rewards over-flagging [@yildiz2025benchmarking, p. 7].
- [V] On the original PrimeVul test set, which is mostly safe code (695 vulnerable vs 25,216 safe functions), GPT-4o-mini's F1 fell to 5.41–12.21% [@yildiz2025benchmarking, p. 7].
- [V] Adding related functions by word overlap did not consistently help and sometimes lowered pairwise accuracy [@yildiz2025benchmarking, p. 7].
- [V] The most common error was calling both versions vulnerable: about 40–95% of errors for plain LLMs and 35–50% for agents [@yildiz2025benchmarking, p. 8].
- [V] Agents called tools far more often on the vulnerable version than on the fixed one (5.85 vs 1.79 calls), so they analysed pairs inconsistently [@yildiz2025benchmarking, p. 9].
- [V] With DeepSeek-Coder-V2, the dependency-augmented LLM reached F1 82.09 and pairwise accuracy 69.24, the best in the paper, while its agent stayed at 21.39 or below [@yildiz2025benchmarking, p. 15].

### Limitations and weaknesses
The authors say the point where a vulnerability was introduced may be traced imperfectly, the balanced dataset may bias F1, and some statistics (such as how many vulnerabilities span several functions) are missing [A] [@yildiz2025benchmarking, p. 9].

Our own concerns [I]:

- Pairwise accuracy of 20% or less is below the 25% a random guesser can reach at most, so "agents are better" means "less bad".
- The agent advantage does not hold for DeepSeek-Coder-V2, so it is not robust across models.
- Training-data contamination is not discussed, although PrimeVul is public and probably in GPT-4o's training data.
- There are no repeated runs, variance or significance tests, and no cost data.
- The number of pairs per setting is not stated. Some values look like they were computed on about 119 pairs rather than 879, so compare settings with caution.

### Gaps and future work this paper leaves open
- Gap G1 (trivial baselines and realistic prevalence): this paper is key evidence. It shows the F1 collapse from balanced to realistic data, and the authors call for evaluation guidelines for this kind of benchmark [A] [@yildiz2025benchmarking, p. 2].
- Gap G2 (same-benchmark comparison with SAST and deep learning): no traditional or deep-learning baseline is included, and contamination is not controlled [I].
- The authors also suggest combining LLMs with constraint solving or program analysis [A] [@yildiz2025benchmarking, p. 9].

### Why it matters for your research
This paper is mainly methodological evidence for RQ2. It explains why reported LLM results vary so much: F1 on balanced data looks moderate, while pairwise accuracy and realistic class ratios show near-random discrimination [I]. It does not compare LLMs with traditional tools.

### Connections to other papers
- tan2026think finds the same pattern with open models on PrimeVul pairs: higher F1 by flagging more, with weak pair-wise accuracy. Both feed agreement G3 in the evidence matrix (LLMs over-flag and cannot separate vulnerable from fixed code) [@tan2026think, p. 7; @yildiz2025benchmarking, p. 8].
- Its F1 drop on realistic data is part of contradiction C5 (class balance flips rankings), together with shu2026evaluating [@shu2026evaluating, p. 40; @yildiz2025benchmarking, p. 7].
- The 22.70% random-guessing reference for pairs that it cites comes from ding2025vulnerability, which also finds GPT-4 below it [@ding2025vulnerability, p. 9].
- Its finding that extra context alone does not help echoes xiong2026sifting, where giving a model more files did not help but step-by-step evidence gathering did [@xiong2026sifting, p. 15].

