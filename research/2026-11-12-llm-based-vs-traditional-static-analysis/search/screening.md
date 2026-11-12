# Screening decisions

Record every candidate considered and the decision. Included papers are also logged by `rlab add --reason`.

| results file | idx | title (short) | decision | reason |
|---|---|---|---|---|
| 044426-large-language-model-versus-static | – | zhou2024comparison: SAST vs LLMs repo-level | include | F1 central head-to-head (15 SAST vs 12 LLMs); preprint, no published version found — flagged |
| scout F1 | – | li2026llm: LLM vuln detection at project scale (TSE 2026) | include | F1/F3/F5 LLM detectors vs static analysers on 265 CVEs, cost data |
| scout F1 | – | khare2025understanding (ICST 2025) | include | F1 16 LLMs vs CodeQL, 25 CWEs |
| 044436-benchmark-large-language-models-static | – | gnieciak2025large (IEEE Access) | include | F1 GPT-4.1/Mistral/DeepSeek vs SonarQube/CodeQL/Snyk on C# |
| scout F1/F4 | – | dubniczky2025castle (LNCS) | include | F1/F4 SAST-vs-LLM CWE benchmark; published version preferred over arXiv 2503.09433 |
| scout F2/F4 | – | ding2025vulnerability PrimeVul (ICSE 2025) | include | F2/F4 dataset label noise and duplication; realistic evaluation |
| scout F2 | – | shu2026evaluating (EMSE 2026) | include | F2 LLMs vs pre-trained code models, 7 languages |
| scout F2 | – | fu2023chatgpt (APSEC 2023) | include | F2 counter-evidence: ChatGPT below fine-tuned models |
| scout F4 | – | chakraborty2024revisiting Real-Vul (TSE) | include | F4 DL detectors collapse on realistic data |
| scout F4 | – | risse2025top (FSE 2025) | include | F4 function-level labels often undecidable without context |
| scout F4 | – | ahmed2026secvuleval (AIware 2026) | include | F4 context-aware real-world benchmark; published version of arXiv 2505.19828 |
| scout F6 | – | kaniewski2026systematic (TOSEM 2026 SLR) | include | F6 most current SLR (263 studies to Nov 2025) |
| scout F6 | – | zhou2025large (TOSEM) | include | F6 highly cited detection+repair review |
| scout F6 | – | sheng2025llms (CSUR) | include | F6 survey contrasting LLMs with static/dynamic analysis |
| 044426-neuro-symbolic-llm-taint-specification | – | li2024iris IRIS | include | F3 leading LLM+CodeQL hybrid; published at ICLR 2025 (no DOI; rlab record is arXiv) |
| scout F3 | – | xiong2026sifting (FSE 2026) | include | F3/F5 LLM agents filter SAST false positives |
| scout F3 | – | du2026reducing (ICSE-SEIP 2026) | include | F3 industrial FP reduction with cost data; check bug types are security-relevant |
| scout F5 | – | tan2026think (ASE 2026) | include | F5 reasoning vs instruct, agent designs on PrimeVul |
| scout F5 | – | yildiz2025benchmarking JITVul (ACL 2025) | include | F5/F4 repository-level benchmark, LLMs vs agents |
| scout F5 | – | guo2025repoaudit RepoAudit | include | F5 repo-level agent; published at ICML 2025 (PMLR 267, no DOI; rlab record is arXiv) |
| scout F5 | – | VulnLLM-R arXiv 2512.07533 | exclude | preprint, no venue; target size reached with peer-reviewed alternatives |
| scout F2 | – | Chakraborty 2022 "Are we there yet" (TSE, 10.1109/tse.2021.3087402) | reserve | seminal but no OA copy; covered by chakraborty2024revisiting |
| scout F2 | – | 10.1145/3639476.3639762 GPT-4 beats DL (ICSE-NIER 2024) | reserve | short paper; contradicts fu2023chatgpt — add if contradiction analysis needs it |
| scout F2 | – | VulBench arXiv 2311.12420 | reserve | preprint, no published version |
| scout F1 | – | RealVuln arXiv 2604.13764 | exclude | vendor-authored preprint, conflict of interest |
| scout F1 | – | arXiv 2610.38617 SAST vs AI security agents | exclude | very recent unreviewed preprint on commercial products |
| scout F3 | – | SAST-Genius arXiv 2509.15433 | exclude | preprint technical report, thin evaluation |
| scout F3 | – | MAVUL 10.1109/tps-isa67132.2025.00040 | exclude | no SAST/DL baseline, minor venue |
| scout F1 | – | NDSS 2025 "From Large to Mammoth" | exclude | LLM-only evaluation, no baseline |
| scout F6 | – | 10.1145/3769676, 10.1186/s42400-025-00361-w | exclude | general LLM-for-cybersecurity surveys, too broad |
| scout F6 | – | IGI book chapters 10.4018/979-8-3693-9311-6.* | exclude | low tier, unclear method |
| gap-report novelty checks | – | qin2026review: CAI 2026 LLM vuln-detection review | include (pass 2) | closest competing review; positioning; must be cited — user approved 2026-11-12 |
| gap-report novelty checks | – | lu2025lab: From Lab to Reality | include (pass 2) | DL vs open LLMs on temporally separated data; closest to G2; preprint (reported accepted at JSS — check) |
| gap-report novelty checks | – | tashenova2026real: WordPress plugin CVE benchmark (BDCC) | include (pass 2) | static vs learning-based detectors, leakage-controlled, PHP; RQ2/G5; MDPI, 0 citations — appraise venue |
| gap-report novelty checks | – | deininger2026open: Open or Frontier? (Computers) | include (pass 2) | cost/energy of LLMs vs small fine-tuned detector at realistic prevalence; G6; MDPI |
