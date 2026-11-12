---
key: ehsani2026faster
status: complete
evidence_basis: full-text
design: Multivocal literature review (Garousi MLR guidelines + SEGRESS); qualitative deductive/inductive coding; no meta-analysis
dataset: 31 peer-reviewed papers (ACM DL, IEEE Xplore, Springer, ScienceDirect + snowballing) and 73 grey sources (Google via SerpAPI, first 10 pages); search Jan 2026
sample_size: 104 sources (31 formal from 551 retrieved + 1,737 snowballed; 73 grey from 132 quality-scored)
metrics: Frequency of mentions per debt type, strategy, tool and metric; grey-source quality score (22 criteria); Cohen's kappa for extraction
main_finding: LLM use is linked mostly to code, design and documentation debt plus new LLM-specific debts; no standard benchmarks or LLM-specific TD metrics exist.
relevance: high
analysed: 2026-11-11
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Faster Code, Deeper Debt? A Multivocal Literature Review on Technical Debt and Its Early Signs in LLM-Assisted Software Development

- Authors: Ehsani, Ramtin; Rawal, Shriya; Cai, Yuanfang; Chatterjee, Preetha
- Year / venue: 2026, ACM Transactions on Software Engineering and Methodology (published)
- DOI: 10.1145/3820165 · URL: https://doi.org/10.1145/3820165
- Source text: `fulltext.txt` (page refs = PDF page index). Our PDF is the arXiv version (arXiv:2606.14796v1, 11 Jun 2026, 38 pages), and it is the **pre-acceptance manuscript**: every page footer reads "Manuscript submitted to ACM" (p. 1 onward), and the p. 1 citation is a template ("ACM Trans. Softw. Eng. Methodol. 1, 1 (January 2026)"). Page numbers refer to this PDF, not the TOSEM pagination. Counts are pre-review numbers and may have changed in the published TOSEM article (DOI 10.1145/3820165); re-check headline counts if the published version becomes accessible.

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

This is a secondary study. A *multivocal literature review* (MLR) is a literature review that also includes "grey" sources such as blogs, company reports and forums, alongside peer-reviewed papers. In this analysis, "dataset" means the review's source corpus, and "findings" are the review's synthesis of what those sources say, not new measurements.

## 1. Research objective
- [A] Examine the forms of technical debt (TD) and their early signs introduced by LLM-assisted development, the risks they bring, and the strategies, tools, metrics and benchmarks available or missing to manage them, from both practitioner (grey) and academic (formal) perspectives (p. 3).
- [A] Motivation: prior work on LLM code correctness and quality covers local, task-specific quality but not how issues accumulate into long-term TD (p. 3).

## 2. Research questions / hypotheses
- [V] RQ1: What forms of TD are introduced by integrating LLM-generated code into software projects? (p. 7).
- [V] RQ2: What strategies or guidelines exist to mitigate TD introduced by LLMs? (p. 7).
- [V] RQ3: What tools or techniques exist to detect or measure TD in LLM-generated code? (p. 7).
- [V] RQ4: Are there benchmarks or datasets to evaluate the TD of LLM-generated code? (p. 8).
- [V] RQ5: Do existing TD metrics sufficiently capture LLM-introduced debt, and if not, what new metrics or dimensions are suggested? (p. 8).
- No hypotheses (descriptive review).

## 3. Methodology
- Research design: [V] MLR following Garousi et al.'s MLR guidelines for SE and Kitchenham et al.'s SEGRESS reporting guidelines (built on PRISMA). Phases: planning, source selection, classification and data extraction, and synthesis (p. 6).
- Approach / model / intervention: [V] Deductive coding against the 13-type TD taxonomy of Alves et al. (2014), combined with inductive coding for new LLM-specific categories (p. 7, p. 14). Sources are also classified as "direct TD evidence" or "supporting TD evidence" depending on whether TD framing is explicit in the title and main discussion (p. 13–14).
- Baselines or comparison conditions: [V] Grey (practitioner) and formal (academic) findings are reported separately and compared for each RQ (p. 14–15). There is no quantitative synthesis or meta-analysis.
- Justification for grey literature: [V] Garousi's seven questions (Table 1); the authors answer "Yes" to 5 of 7 and "No" to Q2 ("lack of volume or quality of evidence ... in the formal literature") (p. 7).

## 4. Dataset and sample
- Source corpus and search:
  - [V] Search conducted in January 2026, covering all sources available up to January 2026 (p. 8).
  - [V] Final query: any of 13 TD-type terms (technical, code, design, documentation, infrastructure, architecture, test, defect, build, requirement, service, test automation, process debt) AND ("large language models" OR "AI-generated code" OR "LLMs" OR "LLM" OR "ChatGPT" OR "Copilot" OR "AI code" OR "AI assistance") (p. 9).
  - [V] The query was developed through exploratory refinement rounds; it was widened from "technical debt" only to all 13 Alves et al. types (p. 8–9).
- Grey literature:
  - [V] Google via SerpAPI, about 375,000 hits, limited to the first 10 result pages on the basis of relevance saturation (p. 9).
  - [V] After de-duplication and removal of academic papers: 132 unique sources (p. 9).
  - [V] Quality assessment with 22 binary criteria in 7 categories (authority, methodology, objectivity, date, significance, impact, outlet type), adapted from Garousi; outlet type could score 0.5 (p. 8–9).
  - [V] Inclusion threshold: score above 11 of 22, giving 73 grey sources (p. 9). Mean score 14.4 (SD 2.52), 75th percentile 15.5 (p. 10).
  - [V] By tier (Table 3): tier 1 company blogs 38; tier 2 developer platforms 18 and media outlets 14; tier 3 personal blogs 3 (p. 10).
- Formal literature:
  - [V] Google Scholar and DBLP were tried and dropped as too noisy (p. 11).
  - [V] Searched ACM DL (258), Springer (182), ScienceDirect (94) and IEEE Xplore (17): 551 hits (p. 11).
  - [V] Two authors screened titles and abstracts (49 kept), then full texts (27 kept, 22 excluded) (p. 11).
  - [V] Forward and backward snowballing of the 27 retrieved 1,737 papers and added 4, for a total of 31 (p. 12).
  - [V] Peer-reviewed only (IC1); preprints were excluded because "results in preprints may change substantially over time" (p. 11–12).
  - [V] Exclusion criteria (Table 5) include EC2: papers on functional quality or correctness of LLM code that do not directly assess or discuss TD (p. 12).
- Sample size (N) and unit: [V] 104 sources: 31 formal and 73 grey (p. 1, p. 3).
- Year distribution: [V] Fig. 4 shows mentions rising from 2022–2023 to a peak in 2025 for both literatures (p. 19).
- Data availability (public? link?): [V] Assessments, annotation sheets and traceability links are in a figshare supplement (p. 4, p. 13).

## 5. Experimental setup
- Procedure:
  - [V] Two authors independently applied data-extraction forms to all sources, and a third author resolved conflicts (p. 12).
  - [V] Extraction fields: TD types; LLM-unique TD concerns; mitigation strategies; tools; benchmarks or datasets; new metrics; notes (p. 12–13).
  - [V] For formal sources, Cohen's kappa was 0.93 for TD types and 0.90–1.00 for the other fields (p. 13).
  - [V] For grey-source quality scoring, the reported agreement of 1.0 "reflects consensus after reconciliation, rather than an initial inter-rater reliability statistic"; a third author reviewed all annotations (p. 9).
  - [V] Synthesis: the first two authors drafted it qualitatively, and all authors reviewed it in meetings (p. 14).
- Quality assessment of formal sources: [I] The method sections describe no formal-source quality appraisal beyond peer-review status (p. 11–12). The threats section nevertheless states that a "rigorous quality assessment process" was followed for both formal and grey sources (p. 29).
- Code availability: [V] Supplementary materials on figshare (p. 4). There is no analysis code; the review is qualitative.

## 6. Evaluation metrics
The review's own measure is the number of sources mentioning each debt type, strategy, tool or metric (Table 8, p. 16). Below are the measurement tools and metrics that the reviewed literature reports.
- Tools (Table 9, p. 23; text p. 20, p. 22):
  - [V] Static analysers: SonarQube, ESLint, Pylint.
  - [V] AI assistants with quality or security features: Amazon CodeWhisperer, Copilot, Tabnine.
  - [V] Documentation tools: Swimm, HopeAI, Graphite.
  - [V] Code review tools: CRken, CodeScene.
  - [V] Quality and security SaaS: Codacy, Snyk, CAST, DeepSource, ArmorCode.
  - [V] Research prototypes: CodeSmellEval (open source) and QualAI (under development).
  - [V] SonarQube is the most frequently mentioned grey-literature tool, but in only 4 sources (p. 22).
- Metrics and measures from the formal literature:
  - [V] Propensity Smelly Code (PSC) in CodeSmellEval: the likelihood that LLM code contains smells (p. 18, p. 22).
  - [V] API Usage Plausibility (AUP) and Deprecated Usage Rate (DUR) (Wang et al.) (p. 25).
  - [V] Data Smell Strength and Data Smell Density (Foidl et al.) (p. 25).
  - [V] SonarQube rules, used in several studies; one study combined them with human raters and another argued for context-sensitive metrics (p. 24–25).
  - [V] Arcan architectural-smell detection combined with prompting and RAG (Pandini et al.) (p. 24).
  - [V] An LLM-vs-SonarQube comparison (Simoes et al.): SonarQube rates by the cost of fixing bad practices, the LLM by ease of reading (p. 24–25).
- Metrics proposed in the grey literature (speculative, not validated):
  - [V] Understandability, adaptability, reviewability (p. 24).
  - [V] Post-fix behaviour (p. 24).
  - [V] Prompt reliability, token cost sprawl, integration fragility (p. 24).
- Statistical testing: not applicable. The review reports only counts and kappa; it does not aggregate effect sizes and appraises no primary-study statistics.

## 7. Key findings
1. [V] Traditional debt types (mentions, formal / grey): code 14 / 56, design 2 / 30, documentation 0 / 17, infrastructure 1 / 12, architecture 1 / 10, test 2 / 6, defect 3 / 1. Build, people, requirement, service, test-automation and process debt: 0 / 0 (Table 8, p. 16).
2. [V] Six debt types new in this review (formal / grey): governance 0 / 19, prompt 8 / 5, fast-integration 0 / 13, data 9 / 0, ethical 3 / 2, provenance 1 / 1 (Table 8, p. 16). 40 grey sources discuss five of the six new forms (all except data debt, which is formal-only) (p. 16, p. 17).
3. [A] "Fast-integration debt" means rapidly integrating LLM output without validation; the authors link it explicitly to vibe coding ("developers implement AI suggestions quickly, or vibe code, without understanding their implications") and say it leads to governance debt (p. 17). [V] It rests on grey sources only (0 formal mentions, p. 16).
4. [A] Quantitative primary evidence cited by the review (we have not checked the primary studies):
   - He et al. (ref [90], p. 34; this primary study is in our corpus as he2026speed): the review reports that Cursor adoption (difference-in-differences with matched controls) produced "a statistically significant large increase" in velocity and "a substantial and persistent increase in complexity and code debt", with static-analysis warnings +30% and code complexity +41% (p. 18). **Secondary claim reported from [@he2026speed], not ehsani's own evidence; do not count separately.** [I] The review omits the primary study's own caveats: the quality effects turn negative and non-significant under the Callaway–Sant'Anna estimator [@he2026speed, p. 16], and once codebase size is controlled (GMM) Cursor has no significant direct effect on warnings, so the warning rise runs mainly through more code [@he2026speed, p. 8].
   - Wang et al.: 7 LLMs, 145 API mappings, 28,125 prompts; all models produced deprecated API usages (p. 18).
   - O'Brien et al.: over 1,000 Copilot function bodies from 380 TODO prompts; the model often replicated self-admitted TD verbatim (p. 19).
   - Zhang et al.: eight smell types in Copilot Python code; well-structured prompts mitigated up to 87.1% of them (p. 19, p. 21).
5. [V] Mitigation strategies:
   - Grey: human-in-the-loop review is recommended in 58 of 73 sources; prompt quality and usage boundaries in 4; 11 discuss no strategy (p. 20).
   - Formal: data quality and standards alignment in 8 studies, prompt design in 7, tool-chains and reflective workflows (RAG, LLM-as-judge) in 10; 6 of 31 discuss no strategy (p. 21).
6. [V] Tools: few are LLM-specific. Formal literature names three (QualAI, CodeSmellEval, ReplaceAPI) (p. 22). Apart from research prototypes and open-source static analysers, all cited tools are commercial (p. 23).
7. [A] No standardised benchmarks or datasets for TD in LLM-generated code exist in either literature. Existing benchmarks focus "almost exclusively on binary correctness" (p. 23–24). Formal studies adapt code-smell benchmarks (CodeXGLUE, CodeSmellData) or pre-LLM TD datasets (p. 24).
8. [A] Existing TD metrics (e.g. SonarQube rules) are considered inadequate for LLM-specific debt. The grey literature says they "fail to capture semantic accuracy, architectural fit, and adaptability" (p. 24). No new metric is widely adopted (p. 24, p. 29).
9. [A] Commercial LLM-aware tools "are rarely subject to independent or rigorous external evaluation" (p. 28).

Evidence-strength caveats given by the authors:
- [A] Sources are classified as direct or supporting TD evidence, and this classification guides interpretation (p. 13).
- [A] Personal blogs (tier 3) are interpreted "with caution" (p. 11).
- [A] 52% of grey sources are company blogs or industry reports, which may bias the review toward practitioner perspectives (p. 30).
- [A] Tools risk "remaining vendor marketing claims rather than evidence-backed solutions" without reproducible benchmarks (p. 28).
- [A] Even for human-written code, comprehensive TD benchmarks remain scarce (p. 24).

## 8. Limitations stated by the authors
- [A] Manual source selection is open to human error; mitigated by independent dual review (p. 29).
- [A] Search-string formulation; mitigated by testing variants (p. 29).
- [A] Screening judgement may cause selection bias (p. 30).
- [A] Undocumented ranking algorithms of search engines and digital libraries (p. 30).
- [A] Grey literature varies in rigour; mitigated by the quality checklist and threshold (p. 30).
- [A] English-only sources (p. 30).
- [A] The TD-term search string may miss work framed as maintainability, software evolution or code quality (p. 30).
- [A] Findings may not generalise across ecosystems or organisations (p. 30).
- [A] Company blogs make up 52% of the grey corpus, which may bias results (p. 30).

## 9. Limitations we identified
- [I] Frequency of mentions is not strength of evidence. Table 8 counts how many sources mention a debt type (p. 16), mostly from grey sources, and primary-study quality is not weighted. The headline new categories rest entirely on practitioner commentary: governance debt (19 grey, 0 formal) and fast-integration debt (13 grey, 0 formal) (p. 16). They are hypotheses, not established effects.
- [I] Fig. 4's y-axis reads "Number of Sources", but grey-source counts for 2025 (84 + 25 = 109) exceed the 73 grey sources (p. 19; values read from the Fig. 4 image, not in the text layer; re-checked 2026-11-12). The figure therefore counts mentions, not sources, which can inflate the visual trend.
- [I] No formal quality appraisal of the 31 peer-reviewed sources is described (p. 11–12), although the threats section claims one (p. 29). Weak primary studies (e.g. vision or position papers such as Mitchell et al.'s "Position: Vibe Coding Needs Vibe Reasoning", p. 21, p. 36) are counted like empirical studies.
- [I] Inclusion inconsistency: the review restricts formal sources to peer-reviewed work (p. 11), yet Della Porta et al. [157] is listed under EASE in Table 6 (p. 13) while its reference entry gives only an arXiv preprint (p. 36). PromptDebt also appears twice in the references, as a published version [14] and an arXiv version [15] (p. 31).
- [I] EC2 excludes papers on correctness or functional quality that do not frame findings as TD (p. 12). Empirical maintainability studies of LLM code that never use the term "debt" (for example SonarQube-based LLM vs human comparisons) may therefore be missing. molison2025llm (ESEM 2025, SonarQube effort-to-fix) does not appear in the reference list; we checked by text search of `fulltext.txt`. The authors partly acknowledge this term-based bias (p. 30).
- [I] The grey search covers only the first 10 Google result pages (p. 9), so results depend on Google's ranking at search time. The authors note that the ranking is undocumented (p. 30), and replication is likely to give different results.
- [I] Table 1 answers "No" to whether the formal literature lacks volume or quality of evidence (p. 7). This sits uneasily with the review's own conclusion that formal work is "small but growing" (p. 18) and lacks benchmarks and metrics (p. 24).
- [I] Grey quality scoring split the 132 sources between two authors with consensus afterwards, and no pre-reconciliation reliability was reported (p. 9). Kappa was computed only for formal-source extraction (p. 13).
- [I] The scope is LLM-assisted development in general, not application reconstruction or vibe-coded apps specifically. Vibe coding appears as a cause of fast-integration debt (p. 17, p. 26), and one formal source is a vibe-coding position paper (p. 21).

## 10. Threats to validity
- Internal (confounds, leakage, selection): [A] Selection bias in screening and search-engine opacity are acknowledged (p. 30). [I] The keyword strategy is anchored on "debt"; with EC2 (p. 12) it selects sources that frame issues as debt, which may over-represent sources that already argue LLMs create debt.
- External (generalisability of sample/context): [A] English only; company blogs dominate (p. 30). [I] The corpus ends in January 2026 (p. 8); the field moves quickly (most sources are from 2025, p. 19).
- Construct (do metrics measure the concept?): [I] TD is operationalised as mentions of TD categories. Static-analysis indicators (SonarQube) are treated as "early signs" of TD (p. 22), which is itself an assumption. The review notes that TD tools disagree on what counts as real debt (p. 5).
- Statistical conclusion (power, multiple comparisons, variance): [I] Not applicable (no inferential statistics). Counts are descriptive and come from heterogeneous source types.
- Reproducibility (data/code/setup reported?): [V] Search string, databases, date, criteria, QA checklist and per-stage counts are reported (p. 8–12), and annotation sheets are on figshare (p. 4, p. 13). [I] The grey search is hard to reproduce (Google ranking, SerpAPI, first 10 pages). Per-source exclusion reasons at full-text stage are summarised but not itemised in the paper (p. 11).

## 11. Future research directions
- Stated by authors [A]:
  - Extend TD taxonomies with LLM-specific debts such as prompt and governance debt (p. 25).
  - Run longitudinal studies of how LLM-related debt accumulates (p. 25–26).
  - Study socio-technical impacts such as prompt sprawl (p. 26).
  - Characterise and measure prompt debt (p. 26).
  - Develop detection of data debt (p. 27–28).
  - Ground ethical and provenance debt empirically (p. 28).
  - Build open tooling that tracks prompts, reproducibility and provenance (p. 28).
  - Evaluate tools reproducibly (p. 28).
  - Design new metrics for semantic accuracy, maintainability, adaptability, reproducibility across runs, provenance and ethics (p. 29).
  - Build community-driven benchmarks analogous to CodeXGLUE and SWE-Bench (p. 29).
- Suggested by us [I]:
  - Test the grey-only debt categories (fast-integration, governance) empirically, e.g. by controlled vibe-coding sessions with maintenance follow-up tasks.
  - Include maintainability studies that do not use the term "technical debt" in a follow-up review.
  - Weight synthesis by primary-study quality.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ3 (primary), RQ4, RQ5; RQ1 (minor, vibe coding as a debt source).
- How it informs our work [I]:
  - It is the only secondary study in our set focused on long-term maintainability (TD) of LLM-assisted code (TOSEM, peer-reviewed).
  - It gives a debt taxonomy (13 Alves types + 6 LLM-specific types) that can structure the maintainability arm of a reconstruction study.
  - Its RQ4/RQ5 findings support a project gap: no standard benchmarks or LLM-specific maintainability/TD metrics exist, and evaluation is dominated by binary correctness (p. 23–24, p. 29).
  - Its evidence base is mostly grey literature, so we use it as a map of concerns and measurement options (SonarQube, PSC, DUR, data-smell metrics), not as evidence of effect sizes.
  - Its exclusion of correctness-only and non-TD-framed studies means it complements, but does not cover, the code-quality comparisons in our corpus (e.g. molison2025llm).

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ3 | Across 104 sources, the debt types most often linked to LLM-assisted code are code (14 formal / 56 grey), design (2 / 30) and documentation (0 / 17) debt | 16 | V | moderate as a map of the discourse; weak as evidence of effect (mention counts, mostly grey) |
| RQ3 | Six LLM-specific debts are proposed: governance, prompt, fast-integration, data, ethical, provenance. Governance (19) and fast-integration (13) appear only in grey sources | 16–17 | V | weak (practitioner commentary, no formal support for two of six) |
| RQ1 | Vibe coding is framed as a driver of fast-integration debt, which leads to governance debt | 17, 26 | A | weak (grey only) |
| RQ3 | DO NOT COUNT SEPARATELY. Secondary claim reported from [@he2026speed] (ref [90]): the review restates its +30% warnings / +41% complexity without the primary study's estimator-sensitivity and codebase-size caveats [@he2026speed, p. 8; @he2026speed, p. 16]. Cite the primary study, not the review, for this effect | 18 | A | n/a (duplicate of he2026speed) |
| RQ4 | No standardised benchmarks or datasets exist to evaluate TD or maintainability of LLM-generated code; benchmarks focus on binary correctness | 23–24 | A | moderate (consistent across both literatures; review search to Jan 2026) |
| RQ4 | SonarQube and general linters are the main measurement tools, but they are not designed for LLM-specific debt; candidate LLM-specific metrics (PSC, AUP/DUR, data-smell strength/density) are early and not standardised | 22, 24–25, 28 | A | moderate |
| RQ4 | Commercial LLM-aware quality tools are rarely independently evaluated | 28 | A | weak |
| RQ5 | Authors call for longitudinal studies of debt accumulation, LLM-specific metrics (incl. reproducibility across runs) and community benchmarks | 25–26, 29 | A | moderate (review-level gap statement) |

## 14. Key quotes
> "no standardized benchmarks or LLM-specific metrics yet exist, leaving an important gap." (p. 1)

> "existing benchmarks focus almost exclusively on binary correctness." (p. 23)

> "developers implement AI suggestions quickly, or vibe code, without understanding their implications, leading to unstable software foundations" (p. 17)

> "The reported agreement of 1.0 (100%) therefore reflects consensus after reconciliation, rather than an initial inter-rater reliability statistic." (p. 9)

## Analyst notes
- Reading coverage:
  - Pages 1–31 (all body text, tables, threats, conclusion) were read in full. PDF page 19 (Fig. 4) was inspected as an image.
  - References (pp. 31–38) were consulted selectively to check the venues of specific sources ([14], [15], [90], [144], [145], [157], [171], [200]) and whether molison2025llm is cited.
  - Figs. 2, 3 and 5 (process diagram, QA-score histogram, debt-to-strategy map) were not inspected as images. Their content is described in the text (p. 6, p. 10, p. 26).
- Uncertainties:
  - Primary-study numbers (Wang et al., Zhang et al., O'Brien et al.) are labelled [A] because they are reported second-hand; we have not checked them in the primary papers. He et al. is the exception: it is in our corpus as he2026speed, whose own analysis is the source of record for that effect.
  - Our PDF is the pre-acceptance manuscript ("Manuscript submitted to ACM", p. 1 onward); counts may have changed in the published TOSEM article (DOI 10.1145/3820165). Re-check headline counts if the published version becomes accessible.
  - Review fixes applied 2026-11-12 (critical-review-batch-a): finding 2 corrected to "five of the six new forms"; He et al. marked as a secondary claim from he2026speed, with its omitted caveats, and the evidence row marked "do not count separately"; version note strengthened; Fig. 4 values marked as read from the image.
  - Table 3 lists [179] under both company blogs and developer platforms (p. 10) while the total is still 73; this is a minor bookkeeping issue.
