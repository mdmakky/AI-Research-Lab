## When LLMs Invent Rust Crates: An Empirical Study of Hallucination Patterns and Mitigation
> **Takeaway:** In Rust code written by six AI models, about one in five references to a crate (a Rust package) pointed to a crate that does not exist, and model size and temperature barely changed this [@zheng2026when, p. 5; @zheng2026when, p. 6]. Almost half of these "invented crates" are mix-ups with Rust's own standard library, and part of the count may come from the authors' name parser, so treat the headline rate with care.

| Item | Detail |
|---|---|
| Authors | Jieming Zheng, Hao Guan, Yepang Liu |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (not peer-reviewed); a reported conference acceptance is not verified |
| Identifier | arXiv 2606.08444 (DOI 10.48550/arxiv.2606.08444) |
| Paper type | Measurement study plus a prompt-based mitigation experiment |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
Rust is a programming language. Its packages are called "crates" and are published on the registry crates.io. A package hallucination happens when an AI model names a package that does not exist. An attacker can register such an invented name and fill it with malware; this attack is called slopsquatting. Earlier studies looked at Python and JavaScript; the authors present this as the first large study for Rust [@zheng2026when, p. 1]. One caveat matters for us: in Rust, mentioning a crate in a source file does not download it [@zheng2026when, p. 1]. So this paper measures names in generated text, not what actually gets installed.

### How they did it
1. They built 2,794 Rust coding tasks from three sources: 1,001 Stack Overflow questions, 793 tasks made from documented functions in popular GitHub projects, and 1,000 tasks that a Qwen model wrote from crate descriptions [@zheng2026when, p. 2; @zheng2026when, p. 3].
2. Each model wrote code for every task with its default settings [@zheng2026when, p. 4].
3. A script pulled crate names out of the code with three text patterns: use lines, path prefixes such as name::item, and extern crate lines [@zheng2026when, p. 4].
4. Each name was compared with a reference list: every crates.io name, plus Rust's standard and compiler crates and known aliases. Any name not on the list counted as hallucinated [@zheng2026when, p. 4; @zheng2026when, p. 5].
5. The main measure is the Crate Hallucination Rate (CHR): hallucinated references divided by all extracted references [@zheng2026when, p. 5].
6. To describe patterns they used edit distance (how many single-letter changes turn one name into another) and the overlap of invented names between models [@zheng2026when, p. 7].
7. They tested two prompt-based fixes on the three open models. Self-refinement asks the model to check its own crate names and regenerate up to 3 times. RAG (retrieval-augmented generation) adds descriptions of 5 matching crates, drawn from the 10,000 most-downloaded, to the prompt [@zheng2026when, p. 8].

### Data and setup
- 14 model variants from six families: GPT-5, Gemini 2.5 Pro, Claude 4 Opus, Qwen2.5-Coder (0.5B to 32B), DeepSeek-Coder-V2 (16B and 236B) and OpenCoder (1.5B and 8B). "B" means billions of parameters, a rough measure of model size [@zheng2026when, p. 4].
- Main run: 16,764 code snippets with 48,494 extracted crate references [@zheng2026when, p. 5]. [I] That is one answer per task per model.
- Temperature (a setting that makes output more random) was varied from 0 to 2 on four models [@zheng2026when, p. 6].
- Open models were run through Ollama, a tool for running models locally, on a server with 8 RTX 6000 Ada GPUs [@zheng2026when, p. 5].
- Not reported: the quantization level of the Ollama models and the date of the crates.io name list.
- Tasks, prompts, scripts and results are shared on figshare [@zheng2026when, p. 10].

### Key findings
- [V] 10,779 of 48,494 crate references were hallucinated, an overall CHR of 22.23% [@zheng2026when, p. 5].
- [V] Gemini 2.5 Pro had the lowest rate (16.18%) and Claude 4 Opus the highest (26.90%) [@zheng2026when, p. 5].
- [V] Size did not predict the rate within Qwen2.5-Coder (p = 0.912). Temperature had no significant effect (p = 0.4859), while the choice of model did (p = 0.0173) [@zheng2026when, p. 5; @zheng2026when, p. 6].
- [V] 45.47% of hallucinations are standard-library or internal modules treated as outside crates, led by thread and duration [@zheng2026when, p. 6].
- [V] The other invented names sit close to real ones: 40.78% are 1–2 edits from a real crate and 86.48% within 5; 32.96% drop a hyphen that the real crate has [@zheng2026when, p. 7].
- [V] 38.9% of frequently invented names are borrowed from other ecosystems, such as queryparser from Python [@zheng2026when, p. 8].
- [V] Self-refinement lowered the rate by 2.22–3.26 points. RAG lowered it by 1.92 and 0.96 points for two models and raised it by 0.34 for Qwen2.5-Coder [@zheng2026when, p. 9].

### Limitations and weaknesses
- [A] Whether invented crates would be installed, break builds or be exploitable was not measured [@zheng2026when, p. 10].
- [A] Alias coverage is incomplete, so the true rate is "likely slightly lower" [@zheng2026when, p. 4].
- [A] A third of the tasks were written by a Qwen model, and models change fast [@zheng2026when, p. 10].
- [I] The path-prefix pattern may also catch type names such as Duration::from_secs. Odd top-10 names such as trefcell and tu32 look like a parser bug that the paper does not discuss [@zheng2026when, p. 6].
- [I] The counts do not match: 10,779 hallucinated references in one section, 13,332 non-module occurrences in the next [@zheng2026when, p. 5; @zheng2026when, p. 7].
- [I] The abstract claims "surprisingly consistent" rates and no loss of code quality, but the model effect is significant and code quality was never measured [@zheng2026when, p. 1; @zheng2026when, p. 6].
- [I] The paper does not say how hyphens in crate names were matched to underscores in code, which affects the 32.96% hyphen finding.
- [I] Ollama's default downloads are usually quantized, which may blur size comparisons. One answer per task and no confidence intervals.

### Gaps and future work this paper leaves open
- [A] G1: installation through Cargo, Rust's package tool, was not measured [@zheng2026when, p. 10]. What models actually install remains open.
- [A] G2: the authors propose a Rust-aware guard that separates standard modules from outside crates, checks near-miss names against the registry and cross-checks the project's Cargo.toml file, but they do not test it [@zheng2026when, p. 9].
- [I] G3: its unit (every source-level reference, including standard-library mix-ups) differs from other papers' units, so 22% cannot be compared directly with Python or JavaScript rates [@zheng2026when, p. 4].
- [I] G4: the unreported quantization of the Ollama models is a hidden confound.
- [A] The prompt fixes still need testing on commercial models [@zheng2026when, p. 9].

### Why it matters for your research
This is the only Rust study in the set. Its main lesson is about measurement: the reference list and the parser decide much of the rate, so hand-check a sample of flagged names in any study of your own. The near-miss pattern (most invented names are a few letters from a real one) supports adding a lookalike check to a pre-install guard. The small Qwen2.5-Coder models it used run on a laptop through Ollama, and its data are public, so a partial replication is cheap.

### Connections to other papers
- [V] Temperature: spracklen2024we found rates rising sharply above temperature 1 [@spracklen2024we, p. 8]; here there was no effect for Rust (evidence matrix contradiction 4).
- [V] Size: krishna2025importing found that larger models hallucinate less [@krishna2025importing, p. 6]; no size effect here (contradiction 3).
- [V] RAG cut Python rates sharply in spracklen2024we [@spracklen2024we, p. 13] but helped little here (contradiction 6).
- [I] spracklen2024we reported that 48.6% of invented Python names are 6 or more edits from a real one [@spracklen2024we, p. 11]. This paper counts occurrences rather than names, so the two figures are not directly comparable.
- [V] When the fake name is planted in the prompt, dasu2026refusing finds nonexistent Rust crates fabricated on 87% of prompts [@dasu2026refusing, p. 8]. That measures accepting a name, not inventing one.
