## PackMonitor: Towards Zero Package Hallucinations via Decoding-Time Monitoring
> **Takeaway:** PackMonitor is a training-free add-on that stops a model from writing any package name after "pip install" that is not on a fixed PyPI list. On five small open models it brought package hallucination to 0% at a small speed cost. The 0% is largely guaranteed by design, an attacker-registered name still passes, and the method needs direct access to a model's internals; it was only tested on a data-centre GPU server.

| Item | Detail |
|---|---|
| Authors | Xiting Liu, Yuetong Liu, Yitong Zhang, Jia Li, Shi-Min Hu |
| Year · Venue | 2026 · Proceedings of the ACM on Software Engineering (PACMSE, ISSTA 2026 issue) |
| Status | Peer-reviewed. Our copy is the arXiv v2 version (it carries the ACM DOI), so page numbers follow that copy |
| Identifier | DOI 10.1145/3832118 (arXiv 2602.20717) |
| Paper type | Technique proposal with a controlled experiment against baseline defences |
| Relevance to us | High — RQ3 (main), RQ4, RQ5 |

### In plain words
When an AI coding assistant writes "pip install X", the package X may not exist. This is a package hallucination. An attacker can register that missing name and fill it with malware, which is called slopsquatting. Earlier defences only lowered the hallucination rate. This paper aims to make hallucinated names impossible. The key idea is simple: the set of real PyPI package names is a finite list, so while the model is writing a name, the tool can forbid anything that cannot become a name on that list [@liu2026packmonitor, p. 1; @liu2026packmonitor, p. 2].

### How they did it
1. Watch the output. A parser follows whether the model is writing prose, ordinary code, or the package names after "pip install" inside a code block. It switches the guard on only for those names [@liu2026packmonitor, p. 8].
2. Restrict the choices. The PyPI name list is compiled into a DFA (a deterministic finite automaton: a small state machine that accepts exactly the names on the list). A language model writes text one token (a short piece of text) at a time and gives every possible next token a score called a logit. At each step PackMonitor sets the logit of every token that cannot lead to a listed name to minus infinity, so the model cannot pick it. A name may end only once it is a complete listed name [@liu2026packmonitor, p. 6; @liu2026packmonitor, p. 9].
3. Save time. The DFA is built once offline, stored, and loaded when the model starts [@liu2026packmonitor, p. 10].
4. Compare. Baselines were RAG (retrieval-augmented generation: real package names are pasted into the prompt), self-refinement (the model re-checks its own answer), both together, and the fine-tuned models released by an earlier study [@liu2026packmonitor, p. 11; @liu2026packmonitor, p. 14].
5. Check side effects. Speed per response, and coding skill on HumanEval, a standard set of Python programming problems [@liu2026packmonitor, p. 14; @liu2026packmonitor, p. 16].

What it needs: the next-token logits and the tokenizer of a model you run yourself. It needs no training and no weight changes [@liu2026packmonitor, p. 3; @liu2026packmonitor, p. 9]. [I] So it cannot be added to closed chat services such as ChatGPT, Claude or Copilot, which do not let you edit token scores at every step.

### Data and setup
- Five open-weight models of 7–8B parameters (a rough measure of model size): DeepSeek-Coder-6.7B, CodeLlama-7B, Qwen2.5-Coder-7B, Llama-3-8B and Llama-3.1-8B [@liu2026packmonitor, p. 11].
- Prompts came from HFuzzer, a "fuzzer" in which a tester model (DeepSeek-V3) keeps writing new coding tasks for the target model. Each model and setting got one round of 1,000 iterations [@liu2026packmonitor, p. 12]. A subset of an earlier prompt set (Package4U) was used for the fine-tuning comparison; its size is not reported [@liu2026packmonitor, p. 14].
- Ground truth: 706,618 PyPI names "at the time of our experiments". The snapshot date and name normalisation (for example upper case, "-" vs "_") are not reported [@liu2026packmonitor, p. 12].
- Hardware: a server with 8× NVIDIA A100 80 GB GPUs and 1 TB RAM [@liu2026packmonitor, p. 12]. There are no CPU or laptop timings.
- Single runs, no statistical tests. Code is public on GitHub [@liu2026packmonitor, p. 20].

### Key findings
- [V] Package hallucination rate (PHR, the share of recommended packages that do not exist) and response hallucination rate fell to 0% on all five models. For example, DeepSeek-Coder went from 8.39% / 11.60% to 0% / 0% [@liu2026packmonitor, p. 13].
- [V] The other training-free defences left 1.30–7.55% PHR. The lowest value, 1.30% (CodeLlama with RAG plus self-refinement), rests on only 231 recommended packages, against 1,004 without a defence [@liu2026packmonitor, p. 13].
- [V] RAG can make things worse: Qwen2.5-Coder PHR rose from 3.25% to 3.33% [@liu2026packmonitor, p. 13].
- [V] The fine-tuned models still hallucinated 2.66% and 10.27% of packages, against 0% for PackMonitor [@liu2026packmonitor, p. 14].
- [V] With the cached DFA, time per response rose by ×1.07 to ×1.28 (about +0.06 s to +0.58 s), against up to ×2.65 for RAG plus self-refinement. Without the cache it rose by ×2.81 to ×6.24 [@liu2026packmonitor, p. 14; @liu2026packmonitor, p. 17]. The text calls the worst case "around 0.2s" [@liu2026packmonitor, p. 15]; use the table values.
- [V] HumanEval scores were unchanged, for example 72.6% vs 72.6% [@liu2026packmonitor, p. 16].

### Limitations and weaknesses
- [A] The guarantee only holds if the name list is correct and complete, so it must be refreshed regularly [@liu2026packmonitor, p. 18].
- [A] Only chat answers with "pip install" are covered. Requirements files, Dockerfiles, CI configurations and coding agents are not [@liu2026packmonitor, p. 19].
- [I] The 0% is largely true by construction: the model is forced onto the list, and the paper does not say whether scoring used the same list.
- [I] "Valid" does not mean "safe". Any name on PyPI passes, including names attackers have already registered. Vetted allowlists are mentioned but not tested [@liu2026packmonitor, p. 6; @liu2026packmonitor, p. 19].
- [I] When the model would have written a missing name, the mask forces it onto some listed name. Whether that name is the right one is never measured. The paper's own example, "google-protobuf" for the import path google.protobuf, is this case [@liu2026packmonitor, p. 6].
- [I] Each setting saw a different, self-generated prompt stream: CodeLlama produced 1,004 packages without the guard and 1,514 with it [@liu2026packmonitor, p. 13]. With one run per setting, there is no measure of chance variation.
- [I] HumanEval cannot reveal harm here: it contains almost no "pip install" lines and was run with greedy decoding, so the guard rarely or never fires [@liu2026packmonitor, p. 16].

### Gaps and future work this paper leaves open
- [A] Extend to conda and npm, private allowlists, requirements files, Dockerfiles, CI and agents; refresh the list over time [@liu2026packmonitor, p. 19].
- [I] G1: coding-agent workflows are explicitly out of scope [@liu2026packmonitor, p. 19], so what agents actually install is untested.
- [I] G2: a plain client-side registry or allowlist check gives the same "no missing name gets installed" property without logit access. It was not compared, and neither tool handles names that attackers have already registered.
- [I] G3: no snapshot date or normalisation rule is reported, and import-path vs install-name confusion is not handled.

### Why it matters for your research
This paper shows that blocking non-existent names is essentially solved when you control the model's decoding. That leaves the harder and more practical problems open. On a laptop with closed API models you cannot use it as published. [I] In principle the same idea could be tried with a small local model if your runtime lets you constrain tokens, but the paper never tested this or reported CPU timings. Its main use for you is as a reference point: a cheap client-side check that queries the registry before installing should be compared against this "zero" result. Your study should also measure what PackMonitor ignores, namely registered lookalikes and whether the substituted package is the right one.

### Connections to other papers
- [V] It reuses the HFuzzer prompt generator and earlier metrics. HFuzzer itself reported 5.68% PHR for DeepSeek-Coder-6.7B [@liu2026packmonitor, p. 12; @zhao2025hfuzzer, p. 6].
- [V] Its fine-tuning numbers (2.66% / 10.27%) match spracklen2024we, where fine-tuning also lowered HumanEval pass@1 from 51.4% to 25.3% for one model [@spracklen2024we, p. 13]. Count these numbers once, from spracklen2024we.
- [V] RAG effects disagree across papers: a slight increase here [@liu2026packmonitor, p. 13], a rise for JavaScript in djire2026evaluating [@djire2026evaluating, p. 6], and large reductions in Python in spracklen2024we [@spracklen2024we, p. 13] (contradiction 6 in our evidence matrix).
- [A] The same weakness as registry-checked training: names that attackers pre-register count as valid [@spracklen2026llm, p. 12; @spracklen2024we, p. 12].
- [V] Like model editing (liu2026mitigating) and unlearning (spracklen2026llm), it was run on data-centre GPUs [@liu2026mitigating, p. 6; @spracklen2026llm, p. 8].
