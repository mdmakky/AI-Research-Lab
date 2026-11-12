---
key: guo2025repoaudit
status: complete
evidence_basis: full-text
design: tool paper with empirical evaluation; LLM agent vs industrial static analyzers (Meta Infer, Amazon CodeGuru) and LLM baselines (CoT prompting, LLMDFA); ablations; model/temperature variation
dataset: 15 C/C++ benchmark projects from prior bug-detection papers (NPD, MLK, UAF; avg 251 KLoC) + 9 further open-source projects
sample_size: 15 benchmark projects (21 previously reported bugs); 9 additional projects; 3 bug types
metrics: TPs, FPs, precision; recall = share of 21 known bugs reproduced; prompts, input/output tokens, USD and seconds per project
main_finding: RepoAudit (Claude 3.5 Sonnet) finds 40 TPs/11 FPs (78.43% precision) on 15 projects at $2.54 and 0.44 h each; Infer 7 TPs, CodeGuru 0 TPs.
relevance: high
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# RepoAudit: An Autonomous LLM-Agent for Repository-Level Code Auditing

- Authors: Guo, Jinyao; Wang, Chengpeng; Xu, Xiangzhe; Su, Zian; Zhang, Xiangyu
- Year / venue: 2025, arXiv (preprint)
- DOI: 10.48550/arxiv.2501.18160 · URL: https://arxiv.org/abs/2501.18160
- Source text: `fulltext.txt` (page refs = PDF page index). Our PDF is arXiv:2501.18160v3 (29 May 2025). Its p. 1 already carries the footer "Proceedings of the 42nd International Conference on Machine Learning, Vancouver, Canada. PMLR 267, 2025" (p. 1), so it appears to be the camera-ready text, but rlab records the paper as an arXiv preprint.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
Build and evaluate an LLM agent that audits whole C/C++ repositories for path-sensitive memory bugs without compilation, overcoming context limits, hallucination and cost of direct prompting [A] (p. 1, p. 2).

## 2. Research questions / hypotheses
- No explicit RQs. Implicit questions: effectiveness on known bugs, comparison with LLM-based and industrial detectors, contribution of components (ablation), sensitivity to model and temperature, real-world impact [V] (p. 7, p. 8).
- Underlying claim: LLMs are good at function-local abstraction, pointer handling and feasible-path exploration, but poor at whole-repository reasoning [A] (p. 3, p. 4).

## 3. Methodology
- Research design: design-and-evaluate tool paper with comparative experiments, ablations and a field deployment [V] (p. 7, p. 8, p. 15).
- Approach / model / intervention: three components [V] (p. 5–7): an initiator (tree-sitter pattern matchers find source values, e.g. NULL literals); an explorer that prompts the LLM one function at a time to derive data-flow facts along feasible paths, stores them in agent memory (also used as a cache) and moves to callers/callees on demand; a validator that checks control-flow order of data-flow facts with a parser and asks the LLM whether inter-procedural path conditions are satisfiable. Calling-context bound K = 4 functions, temperature 0.0, default model Claude 3.5 Sonnet [V] (p. 7).
- Baselines or comparison conditions: Meta Infer and Amazon CodeGuru (industrial static analyzers) [V] (p. 8, p. 14); single-function and multiple-function few-shot CoT prompting and the LLMDFA agent (only on functions related to RepoAudit's TPs, or reachable from sources) [V] (p. 13). No open-source SAST such as CodeQL/Semgrep/CSA, no deep-learning detectors.

## 4. Dataset and sample
- Data source(s): 15 projects (5 per bug type) taken from bug reports of prior papers (Huang et al. 2024; Shi et al. 2021, 2018) [V] (p. 7). NPD: sofa-pbrpc, ImageMagick/MagickCore, coturn, libfreenect, openldap; MLK: libsass, memcached, linux/driver/net, linux/sound, linux/mm; UAF: Redis, linux/drivers/peci, shadowsocks-libev, wabt-tool, icu i18n; 2,130–1,378,262 LoC [V] (p. 7, Table 1).
- Sample size (N) and unit: 15 projects with 21 previously reported bugs (counted as "Old" TPs) [V] (p. 8, p. 17); 9 further projects of 14K–1.7M LoC (avg 420K LoC) for the field study [V] (p. 8).
- Sampling / selection method: "well-maintained" projects from prior bug reports [A] (p. 7). The paper says both "ten actively maintained repositories" (p. 2) and "nine open-source GitHub projects" (p. 8, p. 9); Table 4 lists nine [V] (p. 9).
- Data availability (public? link?): code at https://github.com/PurCL/RepoAudit [V] (p. 1). A labelled dataset release is not reported.

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: tree-sitter for parsing/call graphs; Claude 3.5 Sonnet at temperature 0; K = 4 [V] (p. 7). Additional runs with DeepSeek R1, Claude 3.7 Sonnet and OpenAI o3-mini, and temperatures 0.25–1.0 [V] (p. 16, p. 17). Infer tried in v1.2.0, v1.0.0 and v0.9.0; 2 projects failed to build and 5 crashed or were incompatible [V] (p. 15). Infer and CodeGuru reports were manually labelled TP/FP [V] (p. 14). How RepoAudit's own reports were judged TP or FP (who labelled, criteria, agreement) is not reported.
- Code availability: yes (p. 1).

## 6. Evaluation metrics
- Metric — what it measures — why chosen: TP, FP, precision = TP/(TP+FP); "recall" is the share of the 21 previously reported bugs reproduced (p. 17); prompting rounds, input/output tokens, USD and seconds per project (p. 8). Overall recall against all bugs in the projects is not measured.
- Statistical testing (tests used, significance, effect sizes, confidence intervals): none; single run per setting (temperature study gives one run per temperature) [V] (p. 17).

## 7. Key findings
1. RepoAudit (Claude 3.5 Sonnet) reproduces all 21 known bugs and finds 19 new ones (14 fixed in the latest commit): 40 TPs, 11 FPs, precision 78.43%; 21 TPs are inter-procedural — [V] (p. 7, Table 2 p. 8).
2. Cost: average 0.44 h (1,577.22 s), 100.67 prompts, 614,625.73 input and 46,153.07 output tokens, $2.54 per project, $0.95 per true bug; most expensive project (icu) $18.15 and 10,661.98 s — [V] (p. 7, p. 8).
3. Meta Infer: 13 projects build but 5 crash; on 8 analysed projects 7 TPs and 2 FPs, no MLK or UAF bug found — [V] (p. 8, p. 15). Amazon CodeGuru (NPD and UAF only, 10 projects): 0 TPs and 18 FPs — [V] (p. 8, p. 15).
4. LLM baselines: single-function CoT finds 1 true bug, multiple-function CoT 10; LLMDFA needs on average 165.23× (path scan) to 1,737.04× (source scan) the prompts and 123.18×–1,193.63× the input tokens of RepoAudit — [V] (p. 8, p. 14).
5. Ablations: without abstraction TPs −47.50%, FPs +181.82% (precision 40.38%); without validators FPs +245.45% (31 FPs); without caching ~3.5× prompts, 3.48× cost, 3.75× time, icu exceeds 72 h — [V] (p. 8, p. 15, p. 16).
6. Other models: DeepSeek R1 46 TPs, precision 88.46%, $0.57 but 4,571.72 s per project; Claude 3.7 Sonnet 46 TPs, 86.79%, $1.59; o3-mini 42 TPs, 82.35%, $0.30, ~625 s — [V] (p. 8, p. 16, p. 17).
7. Temperature 0–1.0: precision 72.92–78.43%, recall of known bugs 85.71–100% — [V] (p. 17, Table 11).
8. Field study on 9 projects: 185 new bugs reported at 85.71% precision; 95 confirmed and 79 fixed (174 total); libuv (86 NPD) and memcached (67 MLK) dominate — [V] (p. 8, p. 9, Table 4).
9. 19 of 25 CWE Top-25 (2024) weaknesses need global path-sensitive reasoning — [A] (p. 3).

## 8. Limitations stated by the authors
- [A] FPs and FNs from LLM hallucination (p. 9).
- [A] Cost is highly sensitive to the number of source elements in a repository (p. 9).
- [A] Not sound inter-procedurally: limited to four functions, may miss bugs with longer call chains (p. 9).
- [A] FP example: unaware of external (YANG schema) constraints; FN example: Claude 3.5 Sonnet missed an error-handling path (p. 18).
- [A] Possible leakage of private source code to LLM providers and token costs (p. 10).

## 9. Limitations we identified
- [I] Evaluation by the tool's own authors; the TP/FP judgement procedure for RepoAudit's reports is not described, while Infer/CodeGuru reports were "manually" checked (p. 14). Based on p. 7–8, p. 14.
- [I] Recall is only measured on 21 previously reported bugs (one per project for most), so true recall is unknown; FNs beyond these are not counted. Based on Table 2 (p. 8) and Table 11 (p. 17).
- [I] Industrial baselines are disadvantaged by build failures and crashes (Infer analysed only 8/15 projects); no compile-free open-source SAST (Semgrep, CodeQL build-less modes) or CSA baseline. Based on p. 15.
- [I] Benchmark projects come from prior papers' public bug reports, so model memorisation of known bugs cannot be excluded; not discussed. Based on p. 7.
- [I] Internal inconsistencies: "ten" (p. 2) vs "nine" (p. 8, p. 9) field-study repositories; Table 4 MLK TP column sums to 75 while the printed total is 76 (NPD 107 + MLK 75 + UAF 3 = 185, matching the text; the 85.71% precision matches 186/217). Based on Table 4 (p. 9).
- [I] Documented tension with the later independent evaluation in li2026llm. Both sides are confirmed in the texts, but li is not a replication on the same bugs. Based on the pages cited below.
  - Effectiveness. guo: all 21 previously reported bugs are reproduced and 19 new ones found, for 40 TPs / 11 FPs and a precision of 78.43% on 15 C/C++ projects (p. 7, Table 2 p. 8). li: RepoAudit (Sonnet 3.5) detects 0 of 110 and RepoAudit (GPT-5.4) 2 of 110 known C/C++ vulnerabilities [@li2026llm, p. 7]. Its real-world SFDR is 92.77%, a 9-project average [@li2026llm, p. 11].
  - Dataset. guo's "Old" bugs are bug reports from prior tools/papers (p. 7; Table 2 caption, p. 8). li's 0/110 comes from its *controlled* ReposVul set. That set uses "the three repositories with the most cases" per CWE, and li does not name them [@li2026llm, p. 5]. The shared targets are linux/sound, linux/mm, linux/drivers/net, linux/drivers/peci and ImageMagick (Table 1, p. 7; [@li2026llm, p. 6]). They appear only in li's *real-world* set, where recall is not measured. For 3 of the 5 the bug type differs:
    - ImageMagick: NPD here, CWE-401 in li.
    - linux/driver/net: MLK here, CWE-416 in li.
    - peci: UAF here, CWE-476 in li.

    The sizes differ at every shared target (here vs li): linux/sound 1,378,262 vs 1,253,234; linux/mm 171,721 vs 133,952; peci 2,130 vs 1,715; ImageMagick/MagickCore 242,555 vs the whole ImageMagick repository at 680,878. guo's "linux/driver/net" (914,025 LoC) is closer in size to li's linux/net (962,143) than to li's linux/drivers/net (3,924,621), so it is unclear which li module it corresponds to. Both li modules are CWE-416, and on linux/net RepoAudit emits 3 warnings with an SFDR of 66.67% [@li2026llm, p. 6, p. 11]. On the other shared projects li's RepoAudit (Sonnet 3.5) emits 0 warnings (linux/sound, linux/mm, ImageMagick), 1 warning (linux/drivers/net, an FP) and 3 warnings (peci, all FPs) [@li2026llm, p. 11].
  - Commit. guo analyses the versions used by the earlier works. Its new bugs are found "in historic versions", 14 of them fixed in the latest commit (p. 7, p. 8). li uses recent commits: 6093a68 for Linux and 3bf1076 for ImageMagick [@li2026llm, p. 6]. guo's 4 Linux known bugs are all intra-procedural (Table 2, p. 8), as li also notes [@li2026llm, p. 7].
  - Metric. guo reports precision on the tool's own reports plus reproduction of 21 known bugs (p. 17). li reports recall on CVEs and SFDR [@li2026llm, p. 6].
  - Labeller. guo does not describe how RepoAudit's reports were judged; only the Infer/CodeGuru reports are said to be checked manually (p. 14). li labels warnings with Codex and validates manually [@li2026llm, p. 11].
  - Explanation (ours). Target selection, code version, bug-type mapping, scale, metric and labeller all differ, so the results are not directly comparable. li records 0.00 input tokens for RepoAudit on at least one project [@li2026llm, p. 16] and attributes all 108/108 misses of RepoAudit (GPT-5.4) to incomplete API modelling / candidate exploration [@li2026llm, p. 7]. guo's own Linux runs used only 1–35 prompts each (Table 2, p. 8). Together these point to source/sink coverage as one plausible mechanism.
- [I] Cost contradiction with li2026llm. guo reports an average of $2.54 and 0.44 h per project, with a maximum of $18.15 and 10,661.98 s on icu (p. 7, Table 2 p. 8). li measures RepoAudit (Sonnet 3.5) at an average of $172.77 and a maximum of $1,247.66 per project, with a maximum runtime over 800 min [@li2026llm, p. 15, p. 16]. The projects and their sizes differ:
  - guo's projects average 251 KLoC, and its Linux modules cost $0.03–$0.86 (p. 7, p. 8).
  - li analyses modules of up to 3,924,621 LOC plus gpac and bitlbee, with no budget or timeout limits [@li2026llm, p. 6]. Which project cost the most in li is not reported in li's main text.
  - guo itself says cost depends on the number of source elements (p. 9).

  guo's per-project cost therefore should not be generalised to large repositories.
- [I] "Bugs" (NPD/MLK/UAF) are memory-safety defects, not necessarily exploitable vulnerabilities.

## 10. Threats to validity
- Internal (confounds, leakage, selection): author-evaluated; labelling procedure not reported; possible pretraining exposure to known bugs; baselines restricted to RepoAudit-related functions in the LLM comparison (p. 13).
- External (generalisability of sample/context): C/C++ only, 3 bug types, 15 + 9 projects (p. 7, p. 9).
- Construct (do metrics measure the concept?): "recall" = reproduction of 21 known bugs, not overall recall (p. 17).
- Statistical conclusion (power, multiple comparisons, variance): no tests; one run per configuration; small counts (11 FPs).
- Reproducibility (data/code/setup reported?): code public (p. 1); prompts partly shown (p. 6, p. 7); full labelled report set not reported.

## 11. Future research directions
- Stated by authors [A]: stronger or fine-tuned models for sub-tasks such as feasible-path exploration (p. 9); a richer compilation-free tool suite to expose branches/loops to the model (p. 9); extension to other languages (Python, JavaScript) (p. 10).
- Suggested by us [I]: independent replication with blinded labelling and recall on unseen, post-cutoff bugs; comparison with build-free SAST (Semgrep) and CSA on identical targets.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ1, RQ3, RQ4, RQ5.
- How it informs our work [I]: a representative agentic LLM detector with explicit cost data and a direct comparison with industrial static analyzers (Infer, CodeGuru). Its strong self-reported precision and low cost vs li2026llm's independent evaluation (on different targets, commits and metrics; see §9) is a key tension for RQ1/RQ2/RQ3 and illustrates how evaluation setup drives reported results.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | RepoAudit (Claude 3.5 Sonnet) finds 40 TPs / 11 FPs (precision 78.43%) on 15 C/C++ projects for NPD/MLK/UAF | p. 7, p. 8 | V | weak |
| RQ1 | Meta Infer finds 7 TPs / 2 FPs on the 8 projects it could analyse; Amazon CodeGuru 0 TPs / 18 FPs | p. 8, p. 15 | V | weak |
| RQ1 | With reasoning models RepoAudit precision rises to 82.35–88.46% (42–46 TPs) | p. 8, p. 16 | V | weak |
| RQ2 | Recall is measured only as reproduction of 21 previously reported bugs; overall recall unknown | p. 17 | V | moderate |
| RQ3 | Average cost $2.54, 0.44 h and ~615K input tokens per project; $0.95 per true bug; o3-mini $0.30, DeepSeek R1 $0.57 | p. 7, p. 8, p. 16, p. 17 | V | moderate |
| RQ3 | Cost contradiction: li2026llm measures RepoAudit (Sonnet 3.5) at avg $172.77, max $1,247.66 and >800 min per project vs $2.54 / 0.44 h here; different projects and sizes (avg 251 KLoC here vs Linux modules up to 3.9M LOC, gpac, bitlbee in li) | p. 7, p. 8 | I | weak |
| RQ2 | Tension with li2026llm (0/110 known C/C++ vulns, 92.77% SFDR): overlapping projects only in li's real-world set, at newer commits and partly different bug types; precision vs recall/SFDR; different labellers (see §9) | p. 7, p. 8 | I | weak |
| RQ3 | Validator removal raises FPs by 245.45%; abstraction removal cuts TPs by 47.50% and raises FPs by 181.82% | p. 8, p. 15 | V | weak |
| RQ3 | Compilation-dependent analyzers fail on some projects (2 build failures, 5 Infer crashes of 15); RepoAudit needs no build | p. 15 | V | moderate |
| RQ4 | Evaluated only on C/C++ memory bugs (CWE-476/401/416); call-chain depth limited to 4 functions | p. 7, p. 9 | V | moderate |
| RQ5 | Field study: 185 new bugs in 9 projects, 174 confirmed or fixed | p. 8, p. 9 | A | weak |

## 14. Key quotes
> "In total, it reports 40 TPs and 11 FPs, resulting in a precision of 78.43%." (p. 7)

> "Amazon CODEGURU reports 18 false positives (FPs) with no true positives (TPs), while Meta INFER also only reports seven TPs along with two FPs." (p. 2)

> "it currently limits flow analysis to a maximum of four functions" (p. 9)

## Analyst notes
- Reading coverage: all 18 PDF pages read, including Appendices A–F.
- Version: arXiv v3 (29 May 2025). The ICML 2025 (PMLR 267) proceedings version exists per the footer on p. 1 and li2026llm's reference list; we did not compare with the PMLR copy, so published numbers may differ slightly. Metadata still records it as an arXiv preprint (tier 3); consider re-adding via the published record if rlab can resolve it.
- Uncertainties: the CodeGuru quote has the small-caps name split by extraction ("C ODE G URU"); the wording is otherwise verbatim. The confirmed (95) and fixed (79) counts are treated by the authors as disjoint (sum 174) (p. 2, p. 9).
