## Large Language Model for Vulnerability Detection and Repair: Literature Review and the Road Ahead

> **Takeaway:** Up to March 2024, LLM vulnerability detection was mostly small fine-tuned models judging single functions on heuristically labelled data, and no study was built into developers' daily tools. The review's only evidence on LLMs versus static-analysis tools is the authors' own earlier study.

| Item | Detail |
|---|---|
| Authors | Xin Zhou, Sicong Cao, Xiaobing Sun, David Lo |
| Year | 2025 |
| Venue | ACM Transactions on Software Engineering and Methodology (TOSEM) |
| Status | Peer-reviewed journal article. Our copy is the arXiv version 2404.02525v3 (October 2024), not the typeset journal version. |
| Identifier | DOI 10.1145/3708522; arXiv 2404.02525 |
| Paper type | Systematic literature review (descriptive, no pooled performance numbers) |
| Relevance to us | Medium — RQ2, RQ5 (marginally RQ1 and RQ4) |

### In plain words
This is a systematic literature review (SLR): a study that collects all relevant papers by a written, repeatable plan. It covers how large language models (LLMs) are used for two tasks. The first is detecting vulnerabilities (security flaws) in source code. The second is repairing them. It describes which models people used, how they adapted them, and what data they tested on. It then proposes a research roadmap.

It is a snapshot of the field up to March 2024. That is before most of the newer "agent" and whole-project studies in our project appeared [I].

### How they did it
The authors searched 13 top conferences and 4 journals by hand, then searched 7 databases automatically, then followed references (snowballing) [A] [@zhou2025large, p. 5]. Each candidate paper was scored from 0 to 3 on five quality criteria and needed at least 12 points to stay in [A] [@zhou2025large, p. 6]. One criterion is "published in a prestigious venue", which mixes venue fame with method quality [I].

They sorted the studies into a taxonomy, that is, a structured list of categories. Models were grouped by architecture. Adaptation methods were grouped as fine-tuning (further training on labelled examples), prompt engineering (careful instructions, with or without examples) and retrieval augmentation (fetching related information to add to the prompt) [A] [@zhou2025large, p. 9].

Studies that used only older deep-learning models, such as graph neural networks, were excluded [A] [@zhou2025large, p. 6].

### Data and setup
- 1,535 records screened; 58 studies included [V] [@zhou2025large, p. 4; @zhou2025large, p. 7].
- 40 detection studies and 19 repair studies [V] [@zhou2025large, p. 10; @zhou2025large, p. 16].
- Time window: January 2018 to March 2024 [A] [@zhou2025large, p. 5].
- The number of screeners, their agreement and the per-study quality scores are not reported [I].

### Key findings
- Encoder-only models dominated detection. These are models that read code and produce a label, rather than generating text. CodeBERT alone accounted for 26.1% of model uses [V] [@zhou2025large, p. 7; @zhou2025large, p. 8].
- Fine-tuning was by far the most common approach for detection (about 73% of studies), ahead of prompting (about 17%) and retrieval (about 10%) [V] [@zhou2025large, p. 9].
- Most detection studies worked on single functions. Seven worked at line level, and only one at repository (whole-project) level [V] [@zhou2025large, p. 18].
- Detection datasets mostly use heuristic labels: code changed by a security fix is called vulnerable and everything else safe. Earlier work showed these labels are noisy [A] [@zhou2025large, p. 18].
- None of the 58 studies was built into developers' workflows or tools. All were tested offline on old data [V] [@zhou2025large, p. 19].
- The only comparison of LLMs with SAST tools came from one study. SAST (static application security testing) tools are rule-based scanners. That study found that SAST finds few vulnerabilities with few false alarms, while LLMs find more but raise many false alarms [A] [@zhou2025large, p. 22]. It is the survey authors' own study (zhou2024comparison).
- Cited studies report that LLMs are not robust to small code changes and struggle with rare flaw types and with flaws spread across several functions [A] [@zhou2025large, p. 20; @zhou2025large, p. 21].

### Limitations and weaknesses
- The corpus is dated. It ends in March 2024, before most agent-based, project-scale and LLM-plus-SAST hybrid work [I].
- The LLM-versus-SAST statement is effectively self-citation, not a synthesis of independent studies [I].
- Excluding older deep-learning detectors means it cannot say whether LLMs beat them [I].
- Screening details and quality scores are not public [I].
- Half the scope is repair, so detection gets less depth [I].
- Minor counting slips exist: by our count the tables list 57 unique studies, not 58 [I].
- The authors discuss only one threat to validity: missing papers because of keyword choice [A] [@zhou2025large, p. 24].

### Gaps and future work this paper leaves open
The authors propose a small, manually verified, "living" test set; repository-level detection with long-context LLMs; agents and tool use; benchmarks that do not overlap with model training data; and integration into developer tools [A] [@zhou2025large, p. 20; @zhou2025large, p. 22; @zhou2025large, p. 23]. In our gap report this paper supports gap G2. Surveys ask for verified, contamination-free, repository-level benchmarks, but not for a controlled comparison of LLMs, SAST and deep learning on the same data [I].

### Why it matters for your research
It sets the baseline for RQ2 and RQ5. Already in early 2024, label noise, small input units and missing workflow integration were known problems. It also shows how thin head-to-head LLM-versus-SAST evidence was at that time. For that comparison, cite the primary study zhou2024comparison, not this survey [I].

### Connections to other papers
- Contradiction C3 in the evidence matrix (LLM vs SAST) includes the authors' primary study, zhou2024comparison, where LLMs flagged up to 77.4% of functions [@zhou2024comparison, p. 7].
- kaniewski2026systematic and sheng2025llms are later reviews. Both report that decoder-only models (text-generating models such as GPT-4) now dominate, which shows how fast this survey's picture dated [I].
- Its call for agents, tool use and repository-level work has since been taken up by guo2025repoaudit, li2024iris and li2026llm. The independent study li2026llm, however, finds most such tools still produce mostly false warnings [@li2026llm, p. 11].

