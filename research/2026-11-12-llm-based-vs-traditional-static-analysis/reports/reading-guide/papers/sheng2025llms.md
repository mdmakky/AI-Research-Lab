## LLMs in Software Security: A Survey of Vulnerability Detection Techniques and Insights

> **Takeaway:** A broad but loosely run survey of 58 LLM studies (2019–2024). Its most useful messages are that most work tests isolated code snippets and that, on whole codebases, LLMs usually assist static-analysis tools rather than replace them. Its numbers contain inconsistencies, so cite primary studies for any performance figure.

| Item | Detail |
|---|---|
| Authors | Ze Sheng, Zhicheng Chen, Shuning Gu, Heqing Huang, Guofei Gu, Jeff Huang |
| Year | 2025 |
| Venue | ACM Computing Surveys |
| Status | Peer-reviewed journal article. Our copy is the arXiv version 2502.07049v2 (February 2025), not the typeset journal version. The published version may cover a different time window. |
| Identifier | DOI 10.1145/3769082; arXiv 2502.07049 |
| Paper type | Narrative survey (not a systematic review) |
| Relevance to us | Medium — RQ2, RQ3, RQ4, RQ5 |

### In plain words
A survey collects and describes many studies on one topic. This one covers large language models (LLMs), such as GPT-4, used to find vulnerabilities (security flaws) in software. It describes which models are used, which datasets, which techniques, and which problems remain.

It is a narrative survey. That means the authors chose papers by their own judgement, not by a written, repeatable search plan. Such surveys are useful for an overview but are less reliable for counting things than a systematic review [I].

### How they did it
The authors started from top security conferences and journals, then searched with key terms such as "vulnerability detection" and "LLM" every three weeks for two months [A] [@sheng2025llms, p. 3; @sheng2025llms, p. 4]. They excluded studies using older machine-learning models, such as recurrent neural networks, and studies of malware or network attacks [A] [@sheng2025llms, p. 3].

No search string, database list, formal inclusion table or quality check is reported [I]. They screened roughly 500–600 papers and kept 58 highly relevant ones [A] [@sheng2025llms, p. 3; @sheng2025llms, p. 4].

### Data and setup
- 58 studies from 2019–2024 [A] [@sheng2025llms, p. 3].
- The corpus includes smart-contract (Solidity) studies, which our project treats as a separate topic [I] [@sheng2025llms, p. 4].
- The authors estimate that about 60% of research in this area appears only as arXiv preprints, which are not peer-reviewed [A] [@sheng2025llms, p. 26]. The preprint share of their own corpus is not reported [I].
- They catalogue 42 datasets in one table [V] [@sheng2025llms, p. 13].

### Key findings
- Half of the studies (50%) target C/C++, then Java (21.1%) and Solidity (11.8%) [V] [@sheng2025llms, p. 11].
- Only two of the 42 catalogued datasets work at the level of whole repositories (entire code projects). The rest work on single functions or files [V] [@sheng2025llms, p. 13].
- About 40 studies (stated as 83%) test isolated code snippets. The authors argue that results on snippets look better than real-world detection [A] [@sheng2025llms, p. 20].
- For whole codebases, "LLMs typically assist static analysis tools or support fuzzing tasks" rather than work alone [A] [@sheng2025llms, p. 20]. Static analysis means tools that inspect code without running it. Fuzzing means feeding a program many random inputs to make it crash.
- 41.3% of studies add code-processing steps, such as syntax trees or retrieval of related code. The authors judge the gains as only modest, shrinking for flaws that span several files [V for the share, A for the judgement] [@sheng2025llms, p. 16].
- Reported F1 scores range widely by dataset. F1 is a 0-to-1 score that balances found flaws against false alarms. The survey cites 0.21 on PrimeVul for one study, and CodeBERT at 0.099 on PrimeVul but 0.66 on another dataset. These are second-hand figures [A] [@sheng2025llms, p. 18; @sheng2025llms, p. 19].
- Named challenges include data leakage (test data that the model already saw in training, which inflates scores), complex context, high false-positive rates and weak performance on new, unknown flaws [A] [@sheng2025llms, p. 14].
- LLMs give inconsistent explanations between runs, even when the detection is right [A] [@sheng2025llms, p. 23].

### Limitations and weaknesses
- The review method is weak: no search protocol, no quality appraisal, no flow counts. Its counts about the field are less reliable than those of kaniewski2026systematic [I].
- Several numbers do not add up. It reports 58 studies but uses 56 for the language statistics. "About 40 studies (83%)" implies about 48 studies, not 58 [I] [@sheng2025llms, p. 8; @sheng2025llms, p. 10; @sheng2025llms, p. 20].
- It defines precision as "true positive rate", which is actually the definition of recall [I] [@sheng2025llms, p. 14].
- One claim about CWE-787 versus CWE-862 is cited to a reference that seems to be the wrong paper. Do not reuse that claim without checking the original [I] [@sheng2025llms, p. 22].
- It lists F1 scores from different datasets side by side, which are not comparable [I] [@sheng2025llms, p. 18].
- It offers no quantified comparison of LLMs with static-analysis tools or other deep-learning detectors [I].

### Gaps and future work this paper leaves open
The authors call for moving beyond snippets to whole projects and code changes, for better datasets (accurate labels, little leakage, repository-level annotations), and for better combined "neuro-symbolic" tools that pair LLMs with program analysis [A] [@sheng2025llms, p. 3; @sheng2025llms, p. 20; @sheng2025llms, p. 25]. In our gap report this paper supports gap G2: surveys ask for verified, repository-level benchmarks, but not for a controlled comparison of LLMs, SAST and DL on the same data [I].

### Why it matters for your research
Use it for background on RQ2 and RQ5: its dataset catalogue and its list of challenges. Its point that LLMs assist static analysis in practice is relevant context for RQ3 on hybrids. Because of its weak method and inconsistent numbers, cite primary studies for any figure [I].

### Connections to other papers
- Agreement G1 in the evidence matrix (realistic evaluation lowers scores): this survey agrees with the primary studies there [@sheng2025llms, p. 20].
- zhou2025large is an earlier, more systematic review with a similar scope. kaniewski2026systematic is newer and larger and also classifies this survey as non-systematic [I].
- qin2026review relies on this survey as one of its main sources, so qin is not independent of it [I].
- The survey cites ding2025vulnerability (PrimeVul) and li2024iris (IRIS, an LLM plus static-analysis hybrid), both analysed in full in our project [I].

