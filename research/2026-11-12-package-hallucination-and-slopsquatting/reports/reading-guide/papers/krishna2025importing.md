## Importing Phantoms: Measuring LLM Package Hallucination Vulnerabilities
> **Takeaway:** Eleven models were tested in Python, JavaScript and Rust with the open-source probing tool garak. Every model invented packages, and larger or better-coding models tended to invent fewer. The paper is useful for its date-aware definition of "hallucinated" and its proposed defence, but its statistics are weaker than they look and the defence was never tested.

| Item | Detail |
|---|---|
| Authors | Arjun Krishna, Erick Galinkin, Leon Derczynski, Jeffrey Martin (University of Waterloo; NVIDIA) |
| Year · Venue | 2025 · arXiv |
| Status | Preprint (not peer-reviewed). A leftover ICML 2024 footer on page 1 does not show a real venue; we treat the venue as unverified |
| Identifier | DOI 10.48550/arxiv.2501.19012 (arXiv 2501.19012) |
| Paper type | Measurement study with correlation analysis |
| Relevance to us | High — RQ1, RQ3, RQ4, RQ5 |

### In plain words
A package hallucination is when an AI model writes code that uses a library that does not exist in the public registry (npm for JavaScript, PyPI for Python, crates.io for Rust). The authors ask how often this happens and whether it depends on the language, model size, or whether the model is specialised for code [@krishna2025importing, p. 2]. Their new idea is a date-aware definition. A package also counts as hallucinated if it was registered after the model's knowledge cutoff, the date its training data ends [@krishna2025importing, p. 3]. The model cannot have known such a package, so a match is suspicious and may be a squatter.

### How they did it
1. Build a prompt grid: 7 request stubs combined with 13 coding tasks for each language, each request repeated five times [@krishna2025importing, p. 4; @krishna2025importing, p. 12].
2. Send prompts through garak and extract imported names with regular expressions (simple text patterns) [@krishna2025importing, p. 3; @krishna2025importing, p. 12].
3. Compare names with registry lists and release dates collected on 30 January 2025 [@krishna2025importing, p. 4].
4. Label a name hallucinated if it is unregistered, registered after the cutoff, or (when the cutoff is unknown) registered less than 90 days before the model's release [@krishna2025importing, p. 3].
5. Compute the Package Hallucination Rate (PHR): the share of prompts with at least one hallucinated package [@krishna2025importing, p. 4].
6. Correlate PHR with model size and with HumanEval and MBPP coding benchmark scores, and compare code-specialised with general models using a t-test [@krishna2025importing, p. 6; @krishna2025importing, p. 7].

### Data and setup
- 11 models, including GPT-4o, Llama-3.1 8B and 70B, Qwen2.5-Coder 7B, StarCoder2-15B and Llama-3.1-Nemotron-70B [@krishna2025importing, p. 3].
- Registry sizes: npm 3,391,235, PyPI 604,814 and crates.io 169,823 packages [@krishna2025importing, p. 4].
- The number of generations is not reported. [I] All 33 published rates are exact multiples of 1/455, which points to 455 prompts per model-language cell [@krishna2025importing, p. 4].
- Temperature, hardware, quantization and how cutoffs were found are not reported. No code link is given [@krishna2025importing, p. 10].
- Three of the four authors work at NVIDIA [@krishna2025importing, p. 1].

### Key findings
- [V] Every model hallucinated in every language. PHR ranged from 0.22% (Nemotron-70B, JavaScript and Rust) to 46.15% (Granite-3.0, Python) [@krishna2025importing, p. 4]. [I] 0.22% is a single prompt out of 455.
- [V] Mean PHR: JavaScript 14.73%, Python 23.14%, Rust 24.74% [@krishna2025importing, p. 8].
- [V] GPT-4o: 1.76% in JavaScript, 3.52% in Python, 10.99% in Rust [@krishna2025importing, p. 4].
- [V] Larger models had lower PHR (r = −0.542, p = 0.00114) [@krishna2025importing, p. 6]. [I] This treats 33 model-language points as independent; with 11 models the p-value would be about 0.085, and GPT-4o's size is a 200B estimate [@krishna2025importing, p. 3].
- [V] Higher HumanEval scores went with lower PHR (r = −0.7887 over 10 models, no p-value) [@krishna2025importing, p. 7].
- [V] Code-specialised models had higher average PHR, but the difference was significant only for JavaScript and disappeared without GPT-4o. [A] The authors conclude there is likely no meaningful difference [@krishna2025importing, p. 6].
- [A] Leading ("induced") prompts gave nearly double the natural rate; no figures are given [@krishna2025importing, p. 5].
- [A] Proposed defence: a date-aware list of packages published before each model's cutoff. It is not evaluated [@krishna2025importing, p. 8].

### Limitations and weaknesses
- [A] Eleven models may be too few to show a difference between model types [@krishna2025importing, p. 6].
- [A] The proposed list cannot catch malicious packages that are already old [@krishna2025importing, p. 8].
- [I] There is no mapping from import name to package name and no standard-library filter [@krishna2025importing, p. 12]. Real imports such as sklearn or cv2 may therefore count as hallucinations. In churilov2026range such import names were the largest false-positive class [@churilov2026range, p. 10].
- [I] The text contradicts the paper's own tables, for example on Mamba-Codestral [@krishna2025importing, p. 6; @krishna2025importing, p. 7].
- [I] The abstract says defences were developed and evaluated [@krishna2025importing, p. 1], but the defence is only proposed [@krishna2025importing, p. 8].
- [I] The 13 tasks are unusual and include possibly fictional targets such as "StrombergDB", and some prompt stubs use unexplained personas [@krishna2025importing, p. 12].
- [I] NVIDIA authors evaluate NVIDIA models, and an NVIDIA model ranks best, with no conflict-of-interest statement [@krishna2025importing, p. 1; @krishna2025importing, p. 4].

### Gaps and future work this paper leaves open
- [I] G2: the date-aware list is proposed but untested [@krishna2025importing, p. 8]. It is a natural candidate rule for a guard benchmark.
- [I] G3: its per-prompt unit, regex extraction and date rule differ from other papers, a clear example of why rates cannot be pooled.
- [I] G1: only single chat responses were studied; no agent ever installed anything.
- [A] The authors call for defences that work across languages and for testing more models [@krishna2025importing, p. 6].

### Why it matters for your research
Reuse the date-aware definition: this is one of the few papers in our set that handle packages registered after a model's cutoff. The setup (garak and 7–8B models) is laptop-friendly [@krishna2025importing, p. 3]. Do not cite the size correlation as strong evidence, and do not compare its per-prompt rates with per-mention rates from other papers. If you build a guard, implementing its untested verification list is a cheap, novel step.

### Connections to other papers
- [V] Python above JavaScript agrees with churilov2026range [@churilov2026range, p. 7] and disagrees with spracklen2024we [@spracklen2024we, p. 7] (contradiction C1).
- [V] Its size trend conflicts with Rust results showing no size effect [@zheng2026when, p. 6] and with a newer Llama model producing more invented names in zhao2025hfuzzer [@zhao2025hfuzzer, p. 7] (C3).
- [V] zhao2025hfuzzer adopts this paper's PHR definition [@zhao2025hfuzzer, p. 5] and also uses a before-cutoff rule [@zhao2025hfuzzer, p. 4].
- [A] zhao2025hfuzzer argues that import-based extraction, as used here, misses errors made at the install step [@zhao2025hfuzzer, p. 9].
