## HFuzzer: Testing Large Language Models for Package Hallucinations via Phrase-based Fuzzing
> **Takeaway:** HFuzzer is a testing tool that automatically writes many varied coding tasks to provoke package hallucinations. It triggered them in all nine models tested and found on average 2.60 times more unique invented Python packages than an adapted baseline. Its GPT-4o case study shows that most errors are wrong install names for code that imports correctly.

| Item | Detail |
|---|---|
| Authors | Yukai Zhao, Menghan Wu, Xing Hu, Xin Xia |
| Year · Venue | 2025 · 40th IEEE/ACM International Conference on Automated Software Engineering (ASE 2025) |
| Status | Peer-reviewed. Our copy is the arXiv v2 version (2509.23835), so page numbers follow that copy |
| Identifier | DOI 10.1109/ase63991.2025.00225 (arXiv 2509.23835) |
| Paper type | Tool proposal with a controlled comparison, ablation study and case study |
| Relevance to us | High — RQ1, RQ2, RQ4, RQ5 |

### In plain words
Fuzzing means automatically generating many varied inputs to find where a system fails. Here the inputs are coding tasks and the failure is a package hallucination: the AI model suggests installing a Python library that does not exist on PyPI, the main Python package registry. One model (the "tester") writes the tasks. Another model (the "target") writes code and is then asked how to install the packages it used [@zhao2025hfuzzer, p. 3; @zhao2025hfuzzer, p. 4]. The authors argue that fixed prompt sets from earlier studies are too small and narrow to test models well [@zhao2025hfuzzer, p. 1].

### How they did it
1. Extract phrases. The tester model turns the names and descriptions of popular Python packages into short phrases (object, action, detail) stored in pools [@zhao2025hfuzzer, p. 3].
2. Run rounds. Each round combines phrases, the tester writes a task, the target writes code, and the target is then asked for install commands [@zhao2025hfuzzer, p. 3; @zhao2025hfuzzer, p. 4].
3. Classify each package as standard library, existing before the model's knowledge cutoff, a package from another language, or non-existent [@zhao2025hfuzzer, p. 4].
4. Learn as it goes. Phrases that trigger hallucinations get more weight, and successful tasks seed new ones [@zhao2025hfuzzer, p. 4; @zhao2025hfuzzer, p. 5].
5. Compare with GPTFuzzer-A, a jailbreak fuzzer the authors adapted, because no earlier tool tests package hallucination [@zhao2025hfuzzer, p. 5].
6. Remove parts one at a time (an ablation study) to see what each contributes [@zhao2025hfuzzer, p. 8], and measure task variety with a Diversity Index based on clustering text embeddings [@zhao2025hfuzzer, p. 5].

### Data and setup
- Seeds: the top 100 Python packages on Libraries.io by SourceRank; the top 1,000 for the case study [@zhao2025hfuzzer, p. 6; @zhao2025hfuzzer, p. 8].
- Nine models, from 7–8B open models (Llama-3, Llama-3.1, Qwen2.5-Coder, DeepSeek-Coder, Mistral-7B) to Llama-3.3-70B, DeepSeek-V3, GPT-4o mini and GPT-4o [@zhao2025hfuzzer, p. 5].
- Every model was used as both tester and target: 81 pairs, 1,000 rounds each [@zhao2025hfuzzer, p. 6].
- Tester temperature 0, target temperature 0.7, maximum 3,000 tokens, run on a server with four A800 GPUs [@zhao2025hfuzzer, p. 6].
- Python only [@zhao2025hfuzzer, p. 5]. The case study ran 10,000 rounds against GPT-4o [@zhao2025hfuzzer, p. 8].
- Code is released on GitHub [@zhao2025hfuzzer, p. 2]. The number of responses per model and the registry query date are not reported.

### Key findings
- [V] HFuzzer triggered hallucinations in all nine models and found 2.60 times more unique invented packages than the baseline; over three repeated runs the gain was 3.02 times, significant for most pairs [@zhao2025hfuzzer, p. 7].
- [V] Average hallucination rates ranged from 0.26–0.66% (GPT-4o, GPT-4o mini, DeepSeek-V3, Qwen2.5-Coder) to 16.47% (Mistral-7B) [@zhao2025hfuzzer, p. 6].
- [V] 190 non-existent and 176 other-language names were suggested by more than one model; pkg_resources was suggested by all nine [@zhao2025hfuzzer, p. 7].
- [V] In the GPT-4o case study, 34 of 46 invented packages were "package errors" (correct import, wrong install name) and 12 were "code errors" [@zhao2025hfuzzer, p. 9].
- [V] In 12 cases the model's own code comments marked a name as a placeholder or assumption, yet it still gave an install command [@zhao2025hfuzzer, p. 9].
- [V] Packages released after the model's cutoff, used as seeds, triggered more hallucinations [@zhao2025hfuzzer, p. 9].
- [V] Removing the phrase step cut the number of unique invented packages by 2.06 times [@zhao2025hfuzzer, p. 8].
- [A] Llama-3.1 produced more unique invented names than the older Llama-3, and Qwen2.5-Coder's low rate partly reflects frequent refusals [@zhao2025hfuzzer, p. 7].

### Limitations and weaknesses
- [A] Python only; extraction by text patterns can misfire; temperature effects were tested on only two model pairs [@zhao2025hfuzzer, p. 10].
- [I] The low rates for strong models are not base rates. The fuzzer hunts for unique names, not for a typical mix of developer prompts [@zhao2025hfuzzer, p. 6].
- [I] Counting pkg_resources as a hallucination is debatable, because it is an import name shipped with the setuptools package [@zhao2025hfuzzer, p. 7].
- [I] The baseline was adapted by the authors themselves [@zhao2025hfuzzer, p. 5], repeated runs used only three runs and three targets [@zhao2025hfuzzer, p. 7], and case-study labels have no agreement statistic [@zhao2025hfuzzer, p. 9].
- [I] How release dates were obtained is not reported; the registry date can only be approximated from a reference accessed in March 2025 [@zhao2025hfuzzer, p. 12].
- [A] A GPT-4o invented name appearing in GitHub repositories is reported without counts [@zhao2025hfuzzer, p. 10].

### Gaps and future work this paper leaves open
- [I] G1: models give install commands even for names they mark as placeholders [@zhao2025hfuzzer, p. 9]. What a coding agent that really runs those commands does is untested.
- [I] G2: HFuzzer's found names are a ready test set for a pre-install guard, and the placeholder cases suggest a comment-aware filter.
- [I] G3: most GPT-4o errors are install-name errors for correct imports [@zhao2025hfuzzer, p. 9]. This shows why studies need a shared rule for import names versus package names.
- [A] The authors call for more models and languages [@zhao2025hfuzzer, p. 11] and for using HFuzzer output as fine-tuning data [@zhao2025hfuzzer, p. 10].

### Why it matters for your research
HFuzzer is a reusable generator of hard test prompts, and its two-step protocol (write code, then ask how to install it) catches errors that reading import lines misses. The authors report that it still works with smaller tester models [@zhao2025hfuzzer, p. 7], so a local 7B pair may be feasible on a laptop. Do not quote its rates as typical; quote its counts of unique names and its error types.

### Connections to other papers
- [V] It uses the PHR definition from krishna2025importing [@krishna2025importing, p. 4].
- [I] Its install-name finding supports spracklen2024we's choice not to parse imports [@spracklen2024we, p. 6], and contrasts with churilov2026range, which does parse imports [@churilov2026range, p. 5].
- [V] Names shared across models echo the 104 names invented by all five 2026 models in churilov2026range [@churilov2026range, p. 9].
- [V] A newer Llama inventing more names [@zhao2025hfuzzer, p. 7] contrasts with the size trend in krishna2025importing [@krishna2025importing, p. 6] (contradiction C3).
