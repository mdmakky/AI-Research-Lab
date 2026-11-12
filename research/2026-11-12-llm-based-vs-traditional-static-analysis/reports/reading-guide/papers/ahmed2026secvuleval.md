## SecVulEval: Context-Aware Benchmarking of LLMs for Vulnerability Detection

> **Takeaway:** Five LLMs had to point to the exact faulty lines in real C/C++ code and give the right reason. The best one reached only 23.83% F1, less than half its score on the easier "is this function vulnerable?" question. The study tests no static-analysis tool and no trained deep-learning detector, and our copy is the arXiv preprint, which was not peer-reviewed.

| Item | Detail |
|---|---|
| Authors | Md Basim Uddin Ahmed, Nima Shiri Harzevili, Jiho Shin, Hung Viet Pham, Song Wang |
| Year | 2026 |
| Venue | Proceedings of the 3rd ACM International Conference on AI-Powered Software (AIware 2026) |
| Status | Peer-reviewed conference paper. Our copy is the earlier arXiv preprint 2505.19828v1 (May 2025, "Preprint. Under review."), with a different title. The authors match, but rlab could not confirm the identity automatically because the PDF has no DOI. Numbers in the published version may differ. |
| Identifier | DOI 10.1145/3805760.3814932; arXiv 2505.19828 |
| Paper type | New benchmark plus an evaluation of 5 LLMs |
| Relevance to us | High — RQ2, RQ4, RQ5 (indirectly RQ1 and RQ3) |

### In plain words
A large language model (LLM) is an AI system trained on huge amounts of text and code, such as GPT-4.1 or Claude. Many papers ask an LLM a simple yes/no question: "Is this function vulnerable?" A function is one named block of code. A vulnerability is a flaw an attacker could exploit. This paper asks a harder question. Can the LLM point to the exact statements (lines of code) that cause the flaw, and explain why correctly?

To test this, the authors built a new dataset called SecVulEval. A benchmark or dataset like this is a fixed collection of examples with known answers, so tools can be scored and compared. The answer is sobering. When the reason must be right, scores drop by more than half [V] [@ahmed2026secvuleval, p. 8].

### How they did it
The authors collected real vulnerabilities from the NVD, the US public database of known security flaws. Each flaw there has a CVE number, a public ID for one specific vulnerability. They kept only CVEs linked to a fix in the project's own code history, and only fixes made in a single change [A] [@ahmed2026secvuleval, p. 4; @ahmed2026secvuleval, p. 5].

They then tested five LLMs inside a "multi-agent" pipeline. This means several LLM prompts work in sequence, each with its own job. One plans what to look for. One asks for missing code context, such as definitions of other functions the code calls. One gives the verdict and names the faulty statements. One double-checks the answer [V] [@ahmed2026secvuleval, p. 7]. The models were three open models (22–33 billion parameters), GPT-4.1 and Claude-3.7-Sonnet [@ahmed2026secvuleval, p. 8].

The scoring used precision, recall and F1. Precision is the share of flagged items that are really vulnerable. Recall is the share of real vulnerabilities that were found. F1 combines both into one number between 0 and 100%. Humans judged the statement-level answers by hand, using four rules. These rules are fairly lenient. For example, naming only the "sink" statement (where the harm happens) with the right reason counted as correct [A] [@ahmed2026secvuleval, p. 8].

### Data and setup
- SecVulEval holds 25,440 C/C++ functions (10,998 vulnerable, 14,442 not vulnerable) from 5,867 CVEs, 707 projects and 145 CWE types. A CWE is a standard category of weakness, such as "use after free" [V] [@ahmed2026secvuleval, p. 6].
- The dataset has no duplicate functions. The authors cite earlier figures of up to 18.9% duplicates in older datasets [V] [@ahmed2026secvuleval, p. 3].
- The detection test used only 300 functions, 120 of them vulnerable, drawn from the 25 most common CWE types [V] [@ahmed2026secvuleval, p. 8; @ahmed2026secvuleval, p. 13].
- Each model ran once, at a low randomness setting. No confidence intervals or significance tests are given for the main scores [V] [@ahmed2026secvuleval, p. 8].
- Dataset, code and full prompts are public [V] [@ahmed2026secvuleval, p. 3].

### Key findings
- Statement-level F1 was low for every model: Claude 23.83%, GPT-4.1 22.38%, and down to 7.14% for the weakest open model [V] [@ahmed2026secvuleval, p. 8].
- Function-level F1 was at most 53.89% (Claude), and function-level precision was 47.41% or lower for all five models [V] [@ahmed2026secvuleval, p. 8].
- The two commercial models flagged far more functions: 214 and 215 of 300, against 116–124 for the open models. This gave them higher recall (about 73–76%) but lower precision [V] [@ahmed2026secvuleval, p. 8; @ahmed2026secvuleval, p. 13].
- Statement-level precision was only 5.65–15.35%, so most named lines or reasons were wrong [V] [@ahmed2026secvuleval, p. 8].
- All models found short functions and missed long ones: the median length was 14–33 lines for found flaws against 64–71 lines for missed ones [V] [@ahmed2026secvuleval, p. 13].
- LLMs were poor at saying which extra context they needed: at best 41.33% for one context type, and 0–5.31% for function arguments [V] [@ahmed2026secvuleval, p. 9].
- The authors report over-flagging of null-pointer, use-after-free and integer-overflow flaws, for example flagging a null pointer even when the code checks for it. No counts are given [A] [@ahmed2026secvuleval, p. 13].

### Limitations and weaknesses
- There is no non-LLM comparison at all: no static-analysis tool, no trained deep-learning detector, and no simple single-prompt LLM. So the paper cannot tell us how LLMs compare with traditional tools [I].
- Our own check of the results table suggests the statement-level recall was not computed as the paper defines it. Cases with the right function but the wrong reason were not counted as misses. Under the stated rule, Claude's recall would be about 27.7% instead of 53.23%, and its F1 about 19.8% instead of 23.83%. This is our arithmetic, not the authors' statement, and it means the headline numbers are, if anything, too optimistic [I] [@ahmed2026secvuleval, p. 7; @ahmed2026secvuleval, p. 8; @ahmed2026secvuleval, p. 13].
- 300 test functions is small. Gaps of one or two points between models are probably within noise [I].
- 40% of the test functions are vulnerable, far more than in real code. Precision would likely be lower in practice [I] [@ahmed2026secvuleval, p. 13].
- The "correct context" answers were themselves generated by GPT-4.1, which is also one of the tested models. This makes the context test partly circular [I] [@ahmed2026secvuleval, p. 6].
- Data contamination, meaning the models may have seen these public CVEs and fixes during training, is not discussed [I].
- The authors themselves note subjective manual judging and labels checked on only 100 samples [A] [@ahmed2026secvuleval, p. 12].

### Gaps and future work this paper leaves open
The authors call for better statement-level detection and for training models on their labels [A] [@ahmed2026secvuleval, p. 9; @ahmed2026secvuleval, p. 10]. In our gap report, this paper is evidence for gap G1: published scores are rarely checked against realistic conditions, and stricter scoring halves F1 [@ahmed2026secvuleval, p. 8]. It also relates to gap G2, the missing same-benchmark comparison of LLMs, static analysis and deep learning with file or repository context. This paper gives LLMs some context but runs no other tool family [I].

### Why it matters for your research
This paper shows that a "yes, this function is vulnerable" answer can hide wrong reasoning. That matters for RQ2: how you score changes the result. It also gives CWE-level and code-length weaknesses for RQ4. Do not use it to answer RQ1 (LLM against other tools), because it has no comparison arm [I].

### Connections to other papers
- Agreement G1 in the evidence matrix (realistic evaluation lowers scores): this paper's statement-level drop sits beside similar drops in chakraborty2024revisiting, ding2025vulnerability and shu2026evaluating [@chakraborty2024revisiting, p. 7; @ding2025vulnerability, p. 7; @shu2026evaluating, p. 39].
- Agreement G6 (missing context is the shared cause of failure): risse2025top finds that all audited truly vulnerable functions need outside context [@risse2025top, p. 9], and li2026llm also traces misses to missing context [@li2026llm, p. 15].
- The finding that LLMs fail on longer code matches li2026llm at project scale [@li2026llm, p. 9].
- kaniewski2026systematic includes this paper in its review [I].

