## Mitigating Package Hallucinations in Large Language Models via Model Editing
> **Takeaway:** A preprint proposing BOUND, a small add-on (731 KB) trained into the parts of a model most responsible for choosing fake package names. On prompts that already made the model hallucinate often, it cut fake names by about 65–80% (relative) while coding scores stayed within ±2%. Still, 9–20% of names stay fake on new prompts, and the method needs model weights and GPU training.

| Item | Detail |
|---|---|
| Authors | Shuhan Liu, Yukai Zhao, Xing Hu, Kui Liu, Xiaohu Yang, Xin Xia |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (arXiv v1, July 2026), not peer-reviewed |
| Identifier | arXiv 2607.02052 (DOI 10.48550/arxiv.2607.02052) |
| Paper type | Technique proposal with a controlled comparison against fine-tuning and model-editing baselines |
| Relevance to us | Medium — RQ3 (main), RQ4 |

### In plain words
Model editing means changing a small part of a model's internal numbers to fix one specific behaviour, instead of retraining the whole model. This paper treats package hallucination as a boundary problem: in a given task, the model should be able to tell real package names from invented ones [@liu2026mitigating, p. 1; @liu2026mitigating, p. 2]. The method finds where in the model that decision is made and trains a small LoRA add-on there. LoRA (low-rank adaptation) adds a few small trainable matrices while the original model stays frozen.

### How they did it
1. Find hard prompts. Each prompt was asked 5 times and kept as "high-risk" if more than half the answers contained a fake name [@liu2026mitigating, p. 5].
2. Locate the responsible parts. One pass through the model plus a gradient (a measure of how much each internal number affects the outcome) scores every module; the top 5 are chosen [@liu2026mitigating, p. 3; @liu2026mitigating, p. 4; @liu2026mitigating, p. 6].
3. Edit. A LoRA add-on is trained on those modules. It rewards the real names the model itself produced, penalises its own fake names, and keeps other behaviour close to the original [@liu2026mitigating, p. 4; @liu2026mitigating, p. 5].
4. Validity rule. A name counts as real only if it exists on PyPI and had a release before the model's knowledge cutoff [@liu2026mitigating, p. 5].
5. Compare with full fine-tuning, Self-Refinement with registry feedback, and three other editing methods (ROME, MEMIT, DINM), all using the same edit cases [@liu2026mitigating, p. 5; @liu2026mitigating, p. 6].

### Data and setup
- Three open models: deepseek-coder-6.7b-instruct, Qwen3-8B and Llama-3.1-8B-Instruct [@liu2026mitigating, p. 6].
- Prompts: the recent Python subset of the prompt set from spracklen2024we. Per model there were 609–1,134 high-risk prompts, split into 4 edit sets of 50 and 409–934 "unseen" prompts [@liu2026mitigating, p. 5].
- Five samples per prompt at temperature 0.7 [@liu2026mitigating, p. 6].
- Hardware: a server with 8× NVIDIA A100 80 GB GPUs [@liu2026mitigating, p. 6].
- Not reported: the PyPI query date, the cutoff date per model, standard-library handling, code or data release, and variance.

### Key findings
- [V] On edit prompts, the share of fake names fell from 0.4463 to 0.0897 (−79.9% relative) [@liu2026mitigating, p. 6].
- [V] On unseen high-risk prompts it fell from 0.4421 to 0.1529 (−65.4%), against −37.8% for full fine-tuning [@liu2026mitigating, p. 6; @liu2026mitigating, p. 7].
- [V] The remaining share of fake names on unseen prompts was 0.0927–0.1955, depending on the model [@liu2026mitigating, p. 7].
- [V] Full fine-tuning beat BOUND in one case: on DeepSeekCoder edit prompts, 0.0188 vs 0.0745 fake-name share [@liu2026mitigating, p. 7].
- [V] Some baselines "succeed" only by collapsing: ROME on Llama left valid answers in just 1.1% of cases (Valid-Rate 0.0110) [@liu2026mitigating, p. 7].
- [V] The effect carried over partly to other tasks: −12.8% in code generation and −34.0% in "pip install" recommendation (relative) [@liu2026mitigating, p. 8].
- [V] HumanEval coding scores changed by under 2%, for example 68.96% to 67.58% [@liu2026mitigating, p. 9].
- [V] Cost per edit run (unit not defined): 23.81 s to locate, 83.09 s to edit, with a 731 KB add-on, against 14.27 GB for full fine-tuning [@liu2026mitigating, p. 9].

### Limitations and weaknesses
- [A] Regex extraction may miss names; only three open models, PyPI only, and three tasks were tested [@liu2026mitigating, p. 9; @liu2026mitigating, p. 10].
- [I] The test set is extreme: only prompts with base rates around 85% were kept. Relative cuts on this subset do not say how much the rate would fall on ordinary prompts.
- [I] "Unseen" prompts come from the same filtered pool. If the same invented names recur, part of the gain may be suppression of memorised names. Name overlap is not reported.
- [I] Qwen3 got worse at giving valid answers on unseen prompts (0.7990 to 0.7434) [@liu2026mitigating, p. 7], and its baseline HumanEval score of 23.29% is unexpectedly low [@liu2026mitigating, p. 9].
- [I] In code generation, an unedited model maps imports to PyPI names, so a language model sits inside the measurement [@liu2026mitigating, p. 7].
- [I] The claim of lower edit time leaves out DINM, which is faster [@liu2026mitigating, p. 9].

### Gaps and future work this paper leaves open
- [A] More ecosystems and languages (e.g. Java); configuration files, build scripts and repository-level workflows [@liu2026mitigating, p. 10].
- [I] G3: its release-date cutoff is one of only two in the set [@liu2026mitigating, p. 5; @krishna2025importing, p. 3]. A shared protocol should adopt it, with the dates reported.
- [I] G2: 9–20% of names stay fake, so a client-side check before installing is still needed.
- [I] G1: agents and repository workflows are not covered.

### Why it matters for your research
You cannot run this on a laptop without a GPU. The editing step trains through 7–8B models, and the authors used A100s. [I] The small add-on could in principle be loaded by a local runtime for inference, but this was not tested. Closed API models cannot be edited at all. The most reusable idea is the validity rule: count a name as real only if it existed before the model's cutoff. That stops later-registered names, including attacker-registered ones, from counting as correct. Treat the effect sizes as weak evidence: one preprint, no variance, and extreme prompts.

### Connections to other papers
- [I] Three authors (Zhao, Hu, Xia) also wrote HFuzzer (zhao2025hfuzzer) [@liu2026mitigating, p. 1].
- [V] PackMonitor reaches 0% without training [@liu2026packmonitor, p. 13], while BOUND leaves 9–20% on unseen prompts. Prompts and scoring differ, so compare with care.
- [V] spracklen2026llm also changes model weights, but with full-parameter unlearning on data-centre GPUs [@spracklen2026llm, p. 8].
- [V] Earlier full fine-tuning lowered HumanEval pass@1 from 51.4% to 25.3% for one model [@spracklen2024we, p. 13]. BOUND's small add-on avoids that loss in this paper's tests.
