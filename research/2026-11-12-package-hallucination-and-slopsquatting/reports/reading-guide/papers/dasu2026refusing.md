## Refusing the Impossible: A Taxonomy and Benchmark for Code Hallucination in Large Language Models
> **Takeaway:** When a coding request names a package that does not exist, open AI models usually write code for it instead of saying it does not exist, and bigger models barely do better on this [@dasu2026refusing, p. 6; @dasu2026refusing, p. 8]. The fake name is written into the prompt, so this paper measures how often models accept a planted name, not how often they invent one.

| Item | Detail |
|---|---|
| Authors | Vishnu Asutosh Dasu, Ashish Kundu, Gang Tan |
| Year · Venue | 2026 · arXiv |
| Status | Preprint (not peer-reviewed) |
| Identifier | arXiv 2609.03267 (DOI 10.48550/arxiv.2609.03267) |
| Paper type | Benchmark and evaluation study with an AI judge checked against human labels |
| Relevance to us | High — RQ1, RQ2, RQ3, RQ4, RQ5 |

### In plain words
Most coding benchmarks contain only tasks that can be solved. This paper asks what happens when a request cannot be satisfied, for example because it names a package that does not exist or asks for an impossible algorithm. The right answer is to refuse [@dasu2026refusing, p. 1]. The authors call code built on something that does not exist "code hallucination", sort these failures into a taxonomy (a structured list of types), and release a benchmark to test them [@dasu2026refusing, p. 1]. Matched solvable tasks check that a model is not simply refusing everything.

### How they did it
1. They hand-wrote 270 unsatisfiable requests in 24 subcategories. One family covers plausible but nonexistent things, such as packages on PyPI, npm, crates.io and Go, Java APIs and C headers [@dasu2026refusing, p. 4].
2. Each request comes with a note naming the planted fake item, for example a crate called serde_ultra [@dasu2026refusing, p. 4].
3. They added 91 solvable control tasks that differ only slightly from the fake ones [@dasu2026refusing, p. 4].
4. Requests cover six programming languages and ten "framings", such as internal documentation or a learner's question [@dasu2026refusing, p. 4].
5. 17 open-weight models (models whose weights can be downloaded) each answered once at temperature 0, the least random setting [@dasu2026refusing, p. 5].
6. Claude Opus 4.6 acted as judge with a fixed rubric, labelling each answer as correct, hallucination or refusal [@dasu2026refusing, p. 4].
7. The judge was checked against 138 human labels, and results carry 95% bootstrap intervals (ranges of likely values found by resampling the prompts) [@dasu2026refusing, p. 5].

### Data and setup
- 6,137 judged responses from 17 models with 6.7B to 671B parameters [@dasu2026refusing, p. 1].
- Models up to 32B ran with 4-bit quantization (weights stored with fewer bits to save memory); larger ones ran at full precision [@dasu2026refusing, p. 10].
- The package subsets are small: twelve nonexistent npm prompts and ten nonexistent crate prompts [@dasu2026refusing, p. 9].
- Judge agreement with humans: 94% on outcomes, Cohen's kappa 0.91 (an agreement score corrected for chance, where 1 is perfect) [@dasu2026refusing, p. 5].
- Inference software and hardware are not reported. Code and prompts are released [@dasu2026refusing, p. 2].

### Key findings
- [V] Models wrote ungrounded code for 54% of unsatisfiable requests and refused 31% [@dasu2026refusing, p. 5]. Only 1 of 1,547 control answers was a wrongful refusal [@dasu2026refusing, p. 2].
- [V] Scale helps with impossible tasks (hallucination 0.84 for small models, 0.32 for the largest) but much less with nonexistent things (0.88 to 0.61), and least with fake npm packages and Rust crates (1.00 to 0.85) [@dasu2026refusing, p. 6].
- [V] DeepSeek-V3.2 (671B) and gpt-oss 120B fabricated code for every nonexistent npm and crate prompt [@dasu2026refusing, p. 6].
- [V] By ecosystem, nonexistent npm packages were fabricated on 94% of prompts, Rust crates 87%, Go modules and PyPI modules 63% each, and Java APIs 33% [@dasu2026refusing, p. 8].
- [V] A misspelled real package name led to fabrication on only 14% of prompts, against 94% for a correctly spelled fake one [@dasu2026refusing, p. 8].
- [V] 66% of hallucinations were confident fabrications without any caveat [@dasu2026refusing, p. 6].
- [V] Wording matters more than the model: prompt identity explains 34% of outcome variation against 15% for model identity [@dasu2026refusing, p. 8].
- [V] One model suggested pip install pywfm, a name that already exists on PyPI as an unrelated 2015 package [@dasu2026refusing, p. 9].

### Limitations and weaknesses
- [A] Template prompts may differ from what developers type, so absolute rates belong to this benchmark [@dasu2026refusing, p. 10].
- [A] One answer per prompt; the judge sees the note on the fake item, and the human gold set was labelled by one author [@dasu2026refusing, p. 10].
- [A] Model size is confounded with 4-bit quantization, and closed models were not tested [@dasu2026refusing, p. 10].
- [I] The user supplies the fake name, so rates such as 94% are not comparable with spontaneous invention rates from other studies.
- [I] Package results rest on 22 prompts per model, so per-model package rates are uncertain.
- [I] The judge agreed with humans on only 67% of behaviour labels, so behaviour shares are indicative [@dasu2026refusing, p. 5].
- [I] Publishing the fake names lets anyone register them, which could change the ground truth for future replications.

### Gaps and future work this paper leaves open
- [A] G1: closed frontier models and agentic settings are not evaluated [@dasu2026refusing, p. 10].
- [A] G2: the authors recommend checking package names against registries at generation time but do not test it [@dasu2026refusing, p. 9].
- [A] G4: size is confounded with quantization [@dasu2026refusing, p. 10]. The gap report lists this as a hidden confound across studies.
- [I] Typo amplification was dropped as a gap in our gap report because this paper and twist2026library already measure it [@dasu2026refusing, p. 8].

### Why it matters for your research
This is the clearest evidence that larger models do not fix fake-package acceptance. Its benchmark is small and public, and its small models already ran at 4-bit, the setting a laptop uses. A laptop study could re-run the npm, crate and PyPI subsets on local 7B models and test whether a simple registry check before installing reduces harm. Two design habits are worth copying: matched solvable controls and an AI judge validated against human labels.

### Connections to other papers
- [V] twist2026library finds the same acceptance of fake names, up to 99.22% of tasks [@twist2026library, p. 6], as does djire2026evaluating [@djire2026evaluating, p. 9].
- [V] twist2026library reports one-character typos accepted in up to 25.86% of tasks [@twist2026library, p. 6]. Here a typo that the model corrects counts as correct, which may explain the lower 14% [@dasu2026refusing, p. 4].
- [I] On model size, krishna2025importing finds a size effect [@krishna2025importing, p. 6] and zheng2026when none [@zheng2026when, p. 5]. The quantization confound here shows why size results disagree (evidence matrix contradiction 3).
- [V] The pywfm case is a real-world example of what spracklen2024we warns: a plain existence check passes names that are already registered [@spracklen2024we, p. 12].
