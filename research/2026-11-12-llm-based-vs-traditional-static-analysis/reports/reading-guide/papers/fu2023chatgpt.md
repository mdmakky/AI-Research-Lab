## ChatGPT for Vulnerability Detection, Classification, and Repair: How Far Are We?

> **Takeaway:** In this early, short study, prompted ChatGPT (gpt-4 F1 29%, gpt-3.5 F1 10%) loses clearly to small fine-tuned models (AIBugHunter F1 94%) on the Big-Vul benchmark, and it is worst on all four tasks [@fu2023chatgpt, p. 4; @fu2023chatgpt, p. 5]. Big-Vul was split at random and has noisy labels, which later studies show favours fine-tuned models, so part of the gap may be a benchmark artefact.

| Item | Detail |
|---|---|
| Authors | Michael Fu, Chakkrit Kla Tantithamthavorn, Van Nguyen, Trung Le |
| Year | 2023 |
| Venue | 2023 30th Asia-Pacific Software Engineering Conference (APSEC) |
| Status | Peer-reviewed (conference short paper). Our copy is the arXiv version (2310.09810v1), so page numbers follow the arXiv PDF |
| Identifier | DOI 10.1109/apsec60848.2023.00085; arXiv 2310.09810 |
| Paper type | Short empirical comparison (5 pages; the authors call it a pilot study) |
| Relevance to us | Medium (RQ1, RQ2, RQ4) |

### In plain words
ChatGPT is OpenAI's chat-based large language model (LLM), a big general AI model trained on huge amounts of text and code. The authors ask how well it handles four security tasks. It must find vulnerable functions and lines, name the weakness type, estimate how severe the flaw is, and repair it. ChatGPT is compared with much smaller models that were fine-tuned, meaning given extra training on exactly this data. ChatGPT itself could not be fine-tuned because its model is closed, so it was only prompted [@fu2023chatgpt, p. 1]. Prompting means giving the model instructions in plain text.

### How they did it
- Models: gpt-3.5-turbo and gpt-4, called through OpenAI's paid service with task prompts [@fu2023chatgpt, p. 2; @fu2023chatgpt, p. 3].
- Detection: ChatGPT is asked whether a function is vulnerable. For vulnerable functions it is then asked for the 10 most suspicious lines [@fu2023chatgpt, p. 2]. [I] From the description, the detection prompt appears to give no examples (zero-shot).
- Weakness type: ChatGPT is told the function is vulnerable and given a list of possible CWE IDs [@fu2023chatgpt, p. 2]. A CWE is a standard category of software weakness.
- Repair: the prompt includes three example fixes [@fu2023chatgpt, p. 3].
- Comparison models: AIBugHunter (about 120 million parameters), CodeBERT and GraphCodeBERT, all fine-tuned, plus VulExplainer for weakness types [@fu2023chatgpt, p. 3; @fu2023chatgpt, p. 4].
- No static analysis tool was included [@fu2023chatgpt, p. 3].
- Scores: F1, precision and recall for detection; top-10 line accuracy; accuracy for weakness type; error size for severity; and exact-match patches for repair [@fu2023chatgpt, p. 3; @fu2023chatgpt, p. 4; @fu2023chatgpt, p. 5].

### Data and setup
- Big-Vul: about 188,000 C/C++ functions from 348 GitHub projects, with 3,754 vulnerabilities of 91 types. There is about 1 vulnerable function for every 20 safe ones [@fu2023chatgpt, p. 3].
- Split: 80% train, 10% validation and 10% test, chosen at random "similar to previous studies". No duplicate removal or time-based split is reported [@fu2023chatgpt, p. 3].
- Repair data: 5.5k vulnerable/fixed function pairs from Big-Vul and CVEFixes [@fu2023chatgpt, p. 3].
- Not reported: how many test functions were sent to ChatGPT, the temperature setting, the model version dates, and the number of runs.
- Data, prompts and results are released [@fu2023chatgpt, p. 1].

### Key findings
- [V] Detection F1: AIBugHunter 94%, CodeBERT 87%, GraphCodeBERT 35%, gpt-4 29%, gpt-3.5-turbo 10% [@fu2023chatgpt, p. 4]. F1 balances precision (share of alarms that are real) and recall (share of real flaws found).
- [V] Precision: AIBugHunter 98%, gpt-4 25%, gpt-3.5-turbo 11%. Recall: AIBugHunter 90%, gpt-4 33%, gpt-3.5-turbo 9% [@fu2023chatgpt, p. 4].
- [V] Finding the right lines (top-10 accuracy): AIBugHunter and CodeBERT 99%, gpt-4 65%, gpt-3.5-turbo 25% [@fu2023chatgpt, p. 4].
- [V] Naming the weakness type: fine-tuned models 62–65% correct, gpt-4 20%, gpt-3.5-turbo 13% [@fu2023chatgpt, p. 4].
- [V] Severity on the CVSS scale, a standard 0–10 severity score: mean squared error 1.8–1.86 for fine-tuned models against 5.4 (gpt-3.5) and 5.85 (gpt-4); lower is better [@fu2023chatgpt, p. 4].
- [V] Exact-match repairs: AIBugHunter's repair model 30%, GraphCodeBERT 9%, CodeBERT 7%, both ChatGPT models 0% [@fu2023chatgpt, p. 5].
- [A] Despite about 14,000 times more parameters than CodeBERT, ChatGPT needs fine-tuning on security data to do these tasks well, the authors argue [@fu2023chatgpt, p. 1; @fu2023chatgpt, p. 5].

### Limitations and weaknesses
- [A] The paper has no limitations section. The only constraint it mentions is that ChatGPT cannot be fine-tuned [@fu2023chatgpt, p. 1].
- [I] Method details are thin, as listed above under "not reported".
- [I] The random Big-Vul split favours fine-tuned models. Another study found 12.7% of Big-Vul test functions copied from training [@ding2025vulnerability, p. 4]. An expert audit found only 39% of its vulnerable labels correct [@risse2025top, p. 8]. A word-count model reaches F1 0.86 on it [@risse2025top, p. 11]. The 94% F1 is therefore likely inflated.
- [I] The comparison is uneven: prompting against fine-tuning on the same data. It answers "prompting vs fine-tuning", not "LLMs vs deep learning" in general.
- [I] The first two authors also built the strongest comparison models. This is not a funding conflict, but readers should note it.
- [I] The large gap between GraphCodeBERT (35%) and CodeBERT (87%) is not explained [@fu2023chatgpt, p. 4]. There are single runs, no confidence intervals, and 2023 model versions only.

### Gaps and future work this paper leaves open
- Gap G1 (no shared protocol and no simple baselines): no chance-level or trivial baseline is reported, so the 94% cannot be put in context.
- Gap G2 (no same-benchmark LLM vs static analysis vs deep-learning comparison on clean data): this paper has no static analysis arm and uses leaky, randomly split data. Its ranking reverses on cleaner data (see C1 below).
- [A] The authors see fine-tuning on security data as "crucial" for ChatGPT [@fu2023chatgpt, p. 5].

### Why it matters for your research
This paper is often cited as proof that LLMs lose to fine-tuned models. That is true for its setup (RQ1), but the setup is exactly what RQ2 warns about. Its weakness-type results also help RQ4. Cite it together with the later, cleaner studies, never alone.

### Connections to other papers
- Contradiction C1: on cleaned, time-split PrimeVul pairs, GPT-4 with step-by-step reasoning beats fine-tuned models (12.94% vs at most 3.01% pair-wise correct), although all are below random guessing (22.70%) [@ding2025vulnerability, p. 9]. Ding's own Big-Vul F1 rows agree with this paper's direction [@ding2025vulnerability, p. 7].
- Agreement G8 (prompt-only LLMs trail trained models): zhou2024comparison, a preprint, finds GPT-3.5 prompting detects 3.7–23.2% against 89.2% for fine-tuned CodeBERT [@zhou2024comparison, p. 10]; shu2026evaluating finds prompt-only LLMs near chance [@shu2026evaluating, p. 17]; deininger2026open finds a fine-tuned CodeBERT ahead of 8 zero-shot LLMs [@deininger2026open, p. 11].
- risse2025top explains why fine-tuned models can score high on Big-Vul through shortcuts [@risse2025top, p. 11] [I].

