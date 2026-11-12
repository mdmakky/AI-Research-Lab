# Screening decisions

Record every candidate considered and the decision. Included papers are also logged by `rlab add --reason`.

| results file | idx | title (short) | decision | reason |
|---|---|---|---|---|
| 044949 pilot | 4 | We Have a Package for You! (spracklen2024we) | include | Reference measurement study; published at USENIX Security '25 (pp. 3687–3706, no DOI) — registered via arXiv id |
| scout F1 | – | Range Shrinks (churilov2026range) | include | 2026 frontier-model replication with live registry check; v4 supersedes SCORED '26 version |
| 044949 pilot | 5 | HFuzzer (zhao2025hfuzzer) | include | ASE 2025 fuzzing method |
| 044949 pilot | 8 | Importing Phantoms (krishna2025importing) | include | Model/language/size drivers |
| 044949 pilot | 24 | Secure or Suspect? (haque2025secure) | include | Only quantization study |
| scout F1 snowball | – | When LLMs Invent Rust Crates (zheng2026when) | include | crates.io ecosystem; accepted Internetware 2026 per author |
| scout F1 | – | Static analysis for library hallucinations (mirandapena2026empirical) | include | Cheap detection ceiling; accepted TMLR per author |
| 044949 pilot | 7 | Refusing the Impossible (dasu2026refusing) | include | Benchmark incl. non-existent packages |
| scout F1 | 14 | LLM Hallucinations in Practical Code Generation (zhang2025llm) | include | Published version (PACMSE/FSE 2025) of arXiv 2409.20550 |
| scout F3 | – | Library Hallucinations risk analysis (twist2026library) | include | Peer-reviewed EMNLP 2026 measurement |
| scout F2 | – | PackHallu rule-file injection (wang2026package) | include | Agent-side attack (RQ2, RQ5) |
| scout F2 | – | Harmless Yet Harmful (hsu2026harmless) | include | Only peer-reviewed agent-side attack (EMNLP Findings 2026) |
| scout F2 | – | Trust Me, Import This (liu2026trust) | include | Induced dependency steering via skills |
| 045054 slopsquatting | – | From Hallucination to Registration (okwor2026hallucination) | include (flagged tier 4) | Only registry-side real-world claiming measurement; Zenodo single-author grey literature, low weight |
| 045130 typosquatting | – | Backstabber's Knife Collection (ohm2020backstabbers) | include (background) | Seminal attack taxonomy |
| 045058 mitigating | – | PackMonitor (liu2026packmonitor) | include | Training-free decoding-time defence (FSE 2026) |
| 045058 mitigating | – | Inference-time defences (djire2026evaluating) | include | ASE 2026 head-to-head of 7 defences |
| 044949 pilot | 3 | BOUND model editing (liu2026mitigating) | include | Model-editing defence |
| 044949 pilot | 21 | LLM Ghostbusters (spracklen2026llm) | include | Unlearning defence |
| web/snowball | – | Names Can Hurt (raj2026names) | include | Laptop-scale tool-side guard; closest template |
| scout F2 | – | Correct Code, Vulnerable Dependencies (2605.06279) | exclude (reserve) | Vulnerable versions, not hallucination; adjacent |
| scout F2 | – | Towards Measuring Supply Chain Attacks (NDSS 2021) | exclude (reserve) | Background quota used by Backstabber's |
| scout F3 | – | When Packages Lie RAG (ICICS 2026) / SlopsGuard (NOMS 2026) | exclude (reserve) | No abstract available; paywalled; short demo |
| scout F3 | – | CloudAPIBench (ICSE-SEIP 2025) | exclude (reserve) | API-level, not package-level |
| scout F1 | – | Beyond Functional Correctness (TSE 2026), CodeHalu (AAAI 2025) | exclude (reserve) | General code-hallucination taxonomies; no package focus |
| scout F1/F2 | – | Systematic review (Research Square rs-8007192) | exclude | Single-author preprint SLR |
| scout F1/F2/F3 | – | IJIRT slopsquatting (10.64643/...) | exclude | Metadata mismatch / likely predatory venue |
| scout F2 | – | MQRInvestigar npm slopsquatting | exclude | Low-tier venue; duplicates stronger work |
| scouts | – | General LLM hallucination surveys; malicious-package detectors; agent-skill benchmarks | exclude | Out of scope (no package-hallucination link) |
