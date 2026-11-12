## LLM Ghostbusters: Surgical Package Hallucination Suppression via Adaptive Unlearning
> **Takeaway:** A preprint that retrains a whole model to "unlearn" its own fake package names while reinforcing real ones. On two DeepSeek-Coder models the rate fell from 21.23% to 2.56% and from 27.75% to 6.13% on 40 held-out paraphrased prompts. It needs 12–24-hour full fine-tuning runs on data-centre GPUs. For you, its most useful part is the warning that attacker-registered names poison any check based only on the registry.

| Item | Detail |
|---|---|
| Authors | Joseph Spracklen, Pedram Aghazadeh, Farinaz Koushanfar, Murtuza Jadliwala |
| Year · Venue | 2026 · arXiv (cs.CR) |
| Status | Preprint (arXiv v2, September 2026), not peer-reviewed |
| Identifier | arXiv 2605.01047 (DOI 10.48550/arxiv.2605.01047) |
| Paper type | Technique proposal with a controlled comparison against other unlearning methods, plus ablations |
| Relevance to us | Medium — RQ3 (main), RQ4, RQ2 |

### In plain words
Machine unlearning means training a model to stop producing specific outputs. Here the outputs to forget are invented package names. The method, Adaptive Unlearning (AU), works in a loop: the model writes code, a registry check finds the fake names, and the model is trained to make those names less likely while keeping the real names and the surrounding code unchanged. No human labelling is needed [@spracklen2026llm, p. 1; @spracklen2026llm, p. 2]. Once trained, the fix lives in the model's weights, so answering costs no extra time [@spracklen2026llm, p. 12].

### How they did it
1. Sample answers to hallucination-prone prompts, check every package name against a PyPI snapshot, and mark each token as context, real name or fake name [@spracklen2026llm, p. 5; @spracklen2026llm, p. 7].
2. Train with two pulls at once: reinforce real names with an ordinary training loss, and push fake names down with NPO (negative preference optimisation, a loss that lowers chosen outputs relative to a frozen copy of the original model) [@spracklen2026llm, p. 5].
3. Keep the signal fresh. When a prompt stops producing fake names, or after 5 rounds, the model rewrites the original prompt to create a new variant [@spracklen2026llm, p. 7].
4. Detect names in two ways: parse "pip install" lines, and ask the model which packages are required (Mode 1) and which would be useful (Mode 2) [@spracklen2026llm, p. 8; @spracklen2026llm, p. 21].
5. Compare with gradient ascent (GA, simply pushing the fake outputs down), NPO alone and PMC, all through the same pipeline [@spracklen2026llm, p. 8].

### Data and setup
- Two models: DeepSeek-Coder-7b-instruct-v1.5 and DeepSeek-Coder-V2-Lite-Instruct (16B in total, about 2.4B active) [@spracklen2026llm, p. 8].
- 20 training prompts, chosen because they make the model hallucinate. The test set is 40 prompts: two ChatGPT paraphrases of each training prompt [@spracklen2026llm, p. 8].
- Ground truth: a static PyPI snapshot taken before the experiments [@spracklen2026llm, p. 21]. Snapshot date, standard-library handling and the number of names behind each rate are not reported.
- Coding skill was measured on EvalPlus (HumanEval and MBPP coding problems with extra tests) [@spracklen2026llm, p. 9].
- Hardware: AMD MI210/MI300 data-centre GPUs [@spracklen2026llm, p. 8]. Training is full-parameter (every weight changes), not LoRA, with runs capped at 24 h (7B) and 12 h (16B) [@spracklen2026llm, p. 19]. The number of GPUs is not reported.
- Single runs. Code is in an anonymous repository [@spracklen2026llm, p. 13].

### Key findings
- [V] DeepSeek-7B: the hallucination rate fell from 21.23% to 2.56%, against 7.2% for GA, 14.17% for NPO and 11.84% for PMC [@spracklen2026llm, p. 10].
- [V] DeepSeek-16B: the rate fell from 27.75% to 6.13% [@spracklen2026llm, p. 10].
- [V] Coding skill rose slightly on 7B (EvalPlus average 66.98 to 68.57) but fell on 16B (77.4 to 73.17; HumanEval 81.1 to 73.2). GA kept the 16B average at 77.35 [@spracklen2026llm, p. 10].
- [V] On 7B, GA already reached 7.2% with unchanged coding skill and much less drift from the original model (code KL divergence 0.0031 vs 0.0796) [@spracklen2026llm, p. 10]. KL divergence measures how far the changed model's outputs move from the original.
- [V] Both pulls are needed: reinforcement alone left 12.06% and suppression alone 12.42% [@spracklen2026llm, p. 11].
- [V] Rewriting prompts helps: 10.7% without it, falling with more rewrites [@spracklen2026llm, p. 12].
- [A] If attackers register hallucinated names, the registry check calls them valid, and AU "reinforces what it was deployed to suppress" [@spracklen2026llm, p. 12].

### Limitations and weaknesses
- [A] The check only tests whether a name exists, not whether it is used correctly, and packages hosted outside PyPI may be mislabelled [@spracklen2026llm, p. 12].
- [A] Only two DeepSeek models and Python were tested; frontier-scale fine-tuning exceeded the compute budget [@spracklen2026llm, p. 12].
- [I] The test prompts are paraphrases of the training prompts, so this is close to an in-distribution test. With the number of names unreported, 2.56% may rest on few names.
- [I] The comparison is not evenly tuned. AU reports "the checkpoint that yielded best results" with no stated validation set, while GA and NPO report their final checkpoint at a lower learning rate [@spracklen2026llm, p. 19].
- [I] Numbers disagree inside the paper: 12.7% vs 10.7% for no rewriting, and a restart at checkpoint 60 vs "50 restarted" [@spracklen2026llm, p. 7; @spracklen2026llm, p. 12; @spracklen2026llm, p. 18; @spracklen2026llm, p. 19].
- [I] "Surgical" is overstated. The result is a trade-off: lower rates bought with more drift (7B) or lower coding scores (16B).
- [I] There is no standard-library filter or release-date cutoff, so modules like os may count as fake, and later-registered names count as real.

### Gaps and future work this paper leaves open
- [A] Other ecosystems (npm, vcpkg, Conan), other model families, and checks of semantic correctness [@spracklen2026llm, p. 12; @spracklen2026llm, p. 13].
- [I] G2: oracle poisoning means a guard must look beyond "does the name exist" and use age, history or a vetted list.
- [I] G3: a static, undated snapshot without standard-library handling is exactly the scoring variation our protocol gap describes.
- [I] G5: how serious the poisoning risk is depends on how often hallucinated names actually get registered over time, which is still thinly measured.

### Why it matters for your research
This is not laptop work. It needs full fine-tuning of 7B/16B models on MI210/MI300-class GPUs for half a day or more, and it cannot be applied to closed API models; the authors pitch it to model vendors [@spracklen2026llm, p. 13]. Use it for two things. First, as background: training-based fixes can lower but not remove fake names. Second, as an argument for your design: a check that only asks "is this name registered?" is weak, because attackers can register names. Treat its numbers as weak evidence (one preprint, single runs, paraphrased test set).

### Connections to other papers
- [I] It shares authors with spracklen2024we and builds on its prompt benchmark [@spracklen2026llm, p. 8]. In that earlier paper, full fine-tuning lowered HumanEval from 51.4% to 25.3% for one model [@spracklen2024we, p. 13]; here the 7B model kept its coding skill.
- [V] liu2026mitigating also changes weights, but with a small LoRA add-on and a release-date validity rule that this paper lacks [@liu2026mitigating, p. 5].
- [I] PackMonitor has the same poisoning weakness: any name on the list passes [@liu2026packmonitor, p. 6]. spracklen2024we made the same point about plain registry checks [@spracklen2024we, p. 12].
- [V] So far, real registration is rare: 25 of 2,282 hallucinated names within about six months in churilov2026range [@churilov2026range, p. 12], and publicly listed names were claimed mostly by defensive placeholders in okwor2026hallucination [@okwor2026hallucination, p. 5].
