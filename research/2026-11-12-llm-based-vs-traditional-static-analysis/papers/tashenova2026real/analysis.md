---
key: tashenova2026real
status: complete
evidence_basis: full-text
design: empirical benchmark; plugin-grouped 5-fold CV (de-duplicated, clone-collapsed) of an in-house static taint analyser vs classical ML and LSTM detectors vs 3 trivial baselines; no LLMs
dataset: new WordPress plugin PHP benchmark from 1757 real CVEs (NVD + cvelistV5), 1281 plugins; function-level diff labels; Variant A (patched-twin negatives) and Variant B (untouched same-plugin negatives)
sample_size: 15,294 (Variant A) and 24,917 (Variant B) PHP functions after leakage control (30,860 each before); 400 functions expert-reviewed
metrics: macro-F1 (fold mean, 95% CI), accuracy, balanced accuracy, MCC, PR-AUC, vulnerable-class FNR, per-class P/R/F1; paired fold- and plugin-level tests with Cohen's d
main_finding: Best binary macro-F1 0.563/0.601; neural models never lead; token-count baseline rivals TF-IDF RF; unnamed intra-procedural lexical taint analyser misses ~98%; 48.8% of cleaned positives genuine.
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# A Real CVE-Backed Benchmark for WordPress Plugin Vulnerability Detection: Re-Evaluating Static and Learning-Based Detectors Under Leakage-Controlled Evaluation

- Authors: Tashenova, Zhuldyz; Aitmagambetuly, Aisultan; Urynbassarova, Altyn; Zhetkerbay, Askhat; Amanzholova, Shirin; Kerim, Akerke
- Year / venue: 2026, Big Data and Cognitive Computing (published)
- DOI: 10.3390/bdcc10090303 · URL: https://doi.org/10.3390/bdcc10090303
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

## 1. Research objective
[A] To test whether high accuracies reported for learning-based detectors on synthetic corpora and random splits (including the authors' own SentinelCMS, ~93% accuracy on 600 synthetic snippets) transfer to real, disclosed WordPress plugin vulnerabilities. The second aim is to quantify how much duplicate leakage, contradictory labels and in-sample stacking inflated the authors' own first release (p. 2). The paper is a self-correcting re-evaluation prompted by an audit of the first release (p. 2; acknowledgment p. 14).

## 2. Research questions / hypotheses
- [A] RQ1 (transfer): does training on real CVE data beat training on synthetic data? (p. 2)
- [A] RQ2 (detector families): how do static, classical and neural detectors compare under duplicate-controlled evaluation? (p. 2)
- [A] RQ3 (negatives and granularity): how do the negative-sampling variant and label granularity affect results? (p. 2)
- [A] RQ4 (evaluation validity): how much do duplicate leakage and in-sample stacking inflate reported performance? (p. 2)
- No formal hypotheses are stated.

## 3. Methodology
- Research design: [V] Benchmark construction plus a comparative evaluation of ten detector configurations under plugin-grouped five-fold cross-validation on complete held-out folds (p. 1, p. 5–6).
- Approach / model / intervention:
  - [V] **Static analysis (SAST arm):** a "two-pass intra-procedural analyzer" that propagates taint from user-controlled sources to security-sensitive sinks without sanitisation (p. 5). It is **not named and no version is given** (p. 5). The authors call it "intra-procedural and lexical" (p. 13).
  - [I] From the description alone it does not match an established PHP SAST tool (e.g. Pixy, RIPS, Psalm/Phan taint mode, Semgrep), and it is most likely the taint component of the authors' own SentinelCMS (p. 2). The paper says neither; this rests on the missing name/version (p. 5) and the SentinelCMS description (p. 2).
  - [V] **Classical ML:** Random Forest and linear SVM on character 2–4-gram TF-IDF (char_wb, max_features 5000) (p. 5–6).
  - [V] **Neural:** Bi-LSTM with attention, a unidirectional LSTM ablation, and a "combined" model that concatenates the taint verdict to the Bi-LSTM representation (p. 5).
  - [V] **Stacking:** logistic-regression meta-learner, in an in-sample form (the original buggy implementation, kept only to measure bias) and a nested out-of-fold form (the citable one). The LSTM tower is omitted from both (p. 5–6).
  - [V] **No LLMs and no pre-trained transformers were run.** CodeBERT was not run "because the transformers library is not installed in the evaluation environment and the host has no GPU" (p. 13). LLMs appear only in related work (p. 3).
- Baselines or comparison conditions: [V] Three deliberately trivial baselines (p. 5):
  - majority class (always predicts the most frequent training class);
  - a source/sink presence rule (the same rule used for label cleaning);
  - a one-feature logistic regression on function token count.
  - [V] RQ1 also compares a Bi-LSTM trained on the 600-snippet synthetic corpus with real-to-real CV (p. 7).

## 4. Dataset and sample
- Data source(s): [V] NVD CVE API v2 and CVEProject/cvelistV5. 6666 unique indexed CVE records; 1757 CVEs in 1281 plugins could be resolved to downloadable pre-fix/post-fix source pairs (p. 3). About 54% of indexed CVEs were unrecoverable because old releases/SVN tags were pruned (p. 3).
- Sample size (N) and unit: [V] PHP functions. 30,860 snippets per variant before de-duplication; 15,294 (Variant A) and 24,917 (Variant B) after leakage control (p. 5, Table 2).
  - **Class balance / prevalence:**
    - [V] Variant A: Safe/XSS/SQLi/RCE = 3895/8446/2104/849 (p. 5, Table 2), so vulnerable is the majority class; the majority baseline accuracy is 0.745 (p. 9).
    - [V] Variant B: 13,396/8531/2142/848 (p. 5, Table 2); majority baseline accuracy 0.538 (p. 8, Table 6).
    - [I] Vulnerable prevalence is therefore 74.5% (A) and 46.2% (B) (our calculation from Table 2 counts). Both are far above realistic prevalence because negatives come only from vulnerable plugins: the patched twins of vulnerable functions in Variant A, untouched functions of the same plugin in Variant B (p. 3).
  - [V] Test folds are complete and prevalence-preserving; no balancing or subsampling of test folds (p. 6).
- Sampling / selection method: [V] Labels come from tree-sitter diffs of vulnerable vs patched versions (p. 3):
  - functions touched by the fix are positives and receive the CVE's vulnerability type; untouched functions are negatives;
  - Variant A uses the patched twin as the negative; Variant B uses unmodified functions from the same plugin.
- Leakage control: [V] An audit of the first release found (p. 4, Table 1):
  - duplicate groups crossing folds: 166 groups / 1086 records (A) and 151 / 676 (B);
  - contradictory-label groups: 730 / 456 (1852 / 1199 records).
  - [V] Three corrections were applied (p. 4):
    - all conflicting-label hash groups were removed;
    - exact duplicates (SHA-256 of whitespace-normalised code) were merged;
    - near-duplicates were grouped into clone families (MinHash over 5-token shingles, Jaccard ≥ 0.9; AST node-type sequences, Jaccard ≥ 0.9) and each family was collapsed to one record.
  - [V] Grouping by connected components was rejected because one giant component covered 59.4% (A) / 72.1% (B) of the corpus (p. 4).
  - [V] Final folds share 0 hashes, 0 clone families and 0 plugins (p. 5, Table 2).
  - [V] All three corrections together reduced the published 30,860 records by 50.4% (A) and 19.3% (B). Clone-family collapse alone removed 11,123 (A) and 3714 (B) records; conflict removal plus exact deduplication left 26,417 / 28,631 before that step (p. 5, Table 2).
  - [V] There is no temporal split; all CVEs predate the experiments and no date cut-off is applied (pp. 3–6). [I] Temporal leakage is not addressed; it is less relevant here because no pre-trained model is used.
- Label quality: [V] A stratified 400-function expert review (single annotator, blind to the automated verdict) found (p. 11, Table 10):
  - HIGH tier precision 73.0% (27/37);
  - MEDIUM tier 44.7% (97/217);
  - LOW (discarded) tier 0.7% (1/146);
  - cleaned subset (HIGH+MEDIUM) 48.8% (124/254).
- Data availability (public? link?): [V] Labels, metadata, hashes, folds and a loader script are on GitHub (Aisultan05/wordpress-cve-benchmark) and Zenodo; the audited rebuild is release v2.1.0. Plugin source is not redistributed but reconstructed from WordPress.org (p. 14). [V] A 125-vulnerability / 247-safe expert-verified subset is released (p. 11).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools:
  - [V] Splits and losses: StratifiedGroupKFold (scikit-learn 1.8.0), 5 folds, seed 42, grouped by plugin slug; class-weighted cross-entropy (p. 6, Table 3).
  - [V] LSTM settings (p. 6, Table 3):
    - sequence length 128, 40 epochs, embedding 64, hidden 128, 2 layers, dropout 0.3, batch 16, Adam lr 1e-3;
    - at most 4000 training records per fold; CPU only.
  - [V] RF: 300 trees, balanced class weights. LinearSVC: C 1.0, balanced (p. 6).
  - [V] Software: Python 3.14, PyTorch 2.11 (CPU), NumPy 2.4, tree-sitter-php (p. 7).
  - [V] The 128-token bound was chosen for tractability, not tuned; its effect is unmeasured (p. 6).
  - [V] Granularities: binary, three-class (Safe/SQLi/XSS) and four-class (+RCE), crossed with the two variants, giving six settings (p. 6).
  - [V] Result files are keyed to SHA-256 fingerprints of the dataset index and fold file (p. 6).
- Code availability: [V] Data, folds, per-fold predictions, scores and fingerprinted results are released (p. 1, p. 14). [I] Whether training code is in the same repository is implied ("released training scripts", p. 6) but the repository was not inspected.

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] Macro-F1 is the headline metric (fold mean ± SD, 95% CI with t, 4 df) (p. 6).
  - [V] Also reported: accuracy, per-class precision/recall/F1, vulnerable-class recall and FNR, balanced accuracy, MCC and PR-AUC (p. 6).
  - [A] Accuracy is not comparable with the earlier release because collapsing changed the majority class; macro-F1, balanced accuracy and MCC should be used instead (p. 5, Table 2 note).
  - [V] **Vulnerable-class F1 alone is not reported for most models** (only per-class F1 for the Variant B four-class setting, p. 9, Table 7). [I] Headline numbers are therefore not directly comparable with the vulnerable-class F1 used by most studies in our corpus.
- Statistical testing (tests used, significance, effect sizes, confidence intervals):
  - [V] Paired tests across folds and across plugins, with Cohen's d; the plugin-level test is "the better-powered" (p. 6).
  - [V] Only one comparison is reported in the text: RF vs majority on Variant A macro-F1 is "significant across folds but not across plugins (Wilcoxon p = 0.295, Cohen's d = 0.057)" (p. 9). The only quantified result is the plugin-level one (p = 0.295, d = 0.057); the fold-level test is not named and its p-value is not reported (p. 6, p. 9).
  - [I] With only five paired fold observations (p. 6), a two-sided exact Wilcoxon signed-rank test cannot reach p < 0.05 (smallest attainable p = 2/32 = 0.0625), so the fold-level "significant" result must come from a different test (e.g. a paired t-test) or a one-sided test. Basis: standard property of the exact Wilcoxon test at n = 5.
  - [V] 95% CIs are reported for Variant B binary (p. 8, Table 6).
  - [V] No multiple-comparison correction is mentioned (pp. 6–9).

## 7. Key findings
1. **Overall detector ranking (RQ2)** — [V] Best macro-F1 is 0.563 (Variant A binary, SVM) and 0.601 (Variant B binary, nested stacking) (p. 7–8, Table 5). No neural configuration leads in any of the six settings; the gap to the best classical model is 2.1–6.4 pp (p. 8).
2. **Variant B binary in detail** — [V] Macro-F1 (95% CI) / MCC / vulnerable FNR / PR-AUC (p. 8, Table 6):

   | Detector | Macro-F1 (95% CI) | Bal. acc. | MCC | Vuln. FNR | PR-AUC |
   |---|---|---|---|---|---|
   | Nested stacking | 0.601 (0.579–0.624) | 0.601 | 0.203 | 0.455 | 0.590 |
   | RF + TF-IDF | 0.586 (0.574–0.598) | 0.594 | 0.203 | 0.593 | 0.600 |
   | uni-LSTM | 0.578 (0.563–0.594) | 0.584 | 0.168 | 0.401 | 0.555 |
   | Bi-LSTM | 0.573 (0.550–0.595) | 0.581 | 0.162 | 0.356 | 0.558 |
   | Function-length baseline | 0.572 (0.551–0.593) | 0.582 | 0.177 | 0.610 | 0.575 |
   | Combined taint + Bi-LSTM | 0.569 (0.530–0.609) | 0.579 | 0.157 | 0.425 | 0.552 |
   | SVM + TF-IDF | 0.562 (0.526–0.599) | 0.565 | 0.135 | 0.560 | 0.542 |
   | Source/sink rule | 0.480 (0.446–0.515) | 0.524 | 0.063 | 0.796 | 0.476 |
   | Static taint analyser | 0.366 (0.360–0.373) | 0.504 | 0.035 | 0.982 | 0.465 |
   | Majority baseline | 0.350 (0.349–0.350) | 0.500 | 0.000 | 1.000 | 0.462 |

   [V] Per-tool precision and recall for the vulnerable class are not reported separately; vulnerable recall = 1 − FNR (p. 8, Table 6).

3. **Static taint analyser (the only SAST arm)** — [V] Macro-F1 across the six settings: 0.221 / 0.160 / 0.116 (Variant A binary / 3-class / 4-class) and 0.366 / 0.256 / 0.188 (Variant B) (p. 8, Table 5). [V] It detects 1.7–1.8% of vulnerabilities (p. 9); vulnerable FNR is 0.982 on Variant B binary (p. 8, Table 6). [V] On Variant A binary its macro-F1 (0.221) is below the majority baseline (0.427) (p. 8, Table 5). [A] The low recall "reflects that implementation rather than taint analysis in general" (p. 13).
4. **Trivial baselines are hard to beat** — [V] The token-count baseline matches or exceeds the TF-IDF RF in four of six settings (p. 8, Table 5). [A] The authors say it is "within one percentage point of the best neural model in Variant B binary (0.572 against 0.573)", i.e. the Bi-LSTM (p. 8). [V] In Table 5, however, the best neural model on Variant B binary is the uni-LSTM at 0.578, so the length baseline is 0.006 below the best neural model and 0.001 below the Bi-LSTM (p. 8, Table 5). [V] The Bi-LSTM's real-to-real Variant B binary macro-F1 is 0.572 in Table 4 but 0.573 in Table 5 (p. 7, p. 8). [V] The source/sink rule's MCC is −0.001 to 0.063 (p. 8). [A] "Much of what the models exploit is correlated with function size rather than with security-relevant structure" (p. 8).
5. **Degenerate predictors hidden by aggregate scores** — [V] On Variant A the RF labels 15,068 of 15,294 records vulnerable (Safe recall 0.032); its accuracy 0.747 exceeds the majority baseline's 0.745 by 0.15 pp (p. 9). [V] On Variant B the same RF has a vulnerable-class FNR of 0.84–0.87 (p. 9). [V] Several models almost never predict RCE: RF RCE F1 0.000, uni-LSTM 0.002 (p. 9, Table 7).
6. **Synthetic vs real training (RQ1)** — [V] Real-to-real Bi-LSTM beats synthetic-to-real only in binary settings (+0.034 and +0.078 macro-F1); in four-class settings synthetic is marginally ahead (−0.019, −0.017) (p. 7, Table 4).
7. **In-sample stacking bias (RQ4)** — [V] Mean +1.27 pp macro-F1; optimistic in 5 of 6 settings (max +2.95 pp) but −1.62 pp in Variant B binary (p. 10, Table 8). [A] Duplicate leakage is not expressed as a single number; the authors state that before correction "1086 and 676 records were exact copies of training material appearing in test folds" (p. 10). [V] Table 1 defines these numbers differently: 1086 (A) / 676 (B) are all records in the 166 / 151 duplicate groups that span more than one fold, which includes the training-side copies (p. 4, Table 1). How many of them were on the test side is not reported.
8. **Label cleaning confounded** — [V] Restricting to source-to-sink functions raises Variant A 3-class macro-F1 by +0.112 to +0.222 for learned models but only +0.009 to +0.013 on Variant B binary; the taint analyser gains +0.129 / +0.085 (p. 10, Table 9). [A] The filtered subset is easier as well as cleaner, so cleaning is "a plausible but unproven lever" (p. 10).
9. **Label quality** — [V] 48.8% of cleaned positive labels are genuine vulnerabilities (124/254); the discarded LOW tier is 0.7% genuine (p. 11, Table 10). [V] Only 0.3% of discarded pairs contain a genuine inter-procedural source-to-sink path; 71% contain no taint source at all (p. 12).
10. **Comparison with prior work** — [V] Prior PHP detector DeepTective reported F1 0.881 on a random split vs this work's best macro-F1 0.601 (plugin-grouped, de-duplicated) (p. 12, Table 12). [A] The gap is "best explained by methodology rather than model quality" (p. 12).
11. **Trivial-baseline comparison** — [I] Our calculation from Table 2 counts (p. 5):
    - Variant B binary (46.2% vulnerable): an always-vulnerable predictor would score vulnerable-class F1 ≈ 0.632 and macro-F1 ≈ 0.316. The reported majority (always-Safe) baseline is 0.350 (p. 8).
    - Variant A binary (74.5% vulnerable): the majority baseline *is* always-vulnerable, at macro-F1 0.427 (p. 8, Table 5).
    - Margins of the best detectors: Variant A, SVM 0.563 vs majority 0.427 = +0.136 (p. 8, Table 5); Variant B, nested stacking 0.601 vs majority 0.350 = +0.251, and vs our always-vulnerable 0.316 = +0.285 (p. 8, Table 6).
    - MCC ≤ 0.203 holds for Variant B binary only (p. 8, Table 6); MCC for the Variant A detectors is not reported.
    - Caveat: the paper's macro-F1 values are fold means (p. 6), whereas our always-vulnerable values are pooled over the whole corpus. Because Variant A folds are less class-balanced (p. 5), the fold-mean always-vulnerable score would differ somewhat; the margins are approximate.
    - The 0.667 balanced-data reference does not apply, because neither variant is balanced and the metric is macro-F1.

## 8. Limitations stated by the authors
- [A] The protocol is "duplicate-controlled rather than provably leakage-free"; semantic clones that differ lexically and structurally may persist (p. 13).
- [A] About 54% of indexed CVEs were unrecoverable, so the corpus may be biased toward plugins that retain historical versions (p. 13).
- [A] Rare-class estimates are unreliable (RCE 848 records in Variant B; several models never predict it); four-class results are indicative only (p. 13).
- [A] Neural models trained on ≤4000 records/fold for 40 epochs on CPU, so their numbers are a lower bound (p. 13).
- [A] No transformer comparison (CodeBERT not run; no GPU); the 256-token sensitivity run is outstanding (p. 13).
- [A] The taint analyser is intra-procedural and lexical (p. 13).
- [A] Labels are only about half correct on the positive class, which "bounds what any model trained on them can demonstrate" (p. 13).
- [A] The expert sample was labelled by a single annotator, so no inter-annotator agreement is reported (p. 11).

## 9. Limitations we identified
- [I] **The SAST arm is a weak straw-man for our RQ1.** It is an unnamed in-house intra-procedural lexical analyser (p. 5, p. 13). No established PHP SAST tool (e.g. Psalm taint analysis, Semgrep, RIPS/Pixy descendants) was run. (That CodeQL does not support PHP is our outside knowledge, not stated in the paper.) The "misses about 98%" result cannot be generalised to PHP SAST.
- [I] **No LLM arm at all** (p. 3, p. 13). For our review the paper informs SAST-vs-DL and evaluation methodology, not LLM-vs-anything.
- [I] **Label precision of the main benchmark is not reported.** The 48.8% figure (p. 11) refers to the cleaned HIGH+MEDIUM subset. The main experiments (Tables 5–6) use the full corpus, which also contains LOW-tier functions found 0.7% genuine (p. 11) and the 13,702 "noisy" discarded pairs (p. 11, Table 11). Genuine-positive precision in the evaluated corpus is therefore plausibly well below 48.8%, but is not reported. This makes every absolute score hard to interpret.
- [I] **Macro-F1 headline** mixes Safe-class and vulnerable-class F1. Combined with class proportions that differ between variants (74.5% vs 46.2% vulnerable), this makes cross-variant and cross-paper comparisons fragile.
- [I] **Function-level granularity, not repository-level.** It does not test inter-procedural or cross-file detection, which is the core of our G5 interest. The inter-procedural recovery experiment found only 39 paths (p. 11).
- [I] **Self-correction context.** The paper corrects the authors' own earlier release after reviewers audited the artifacts (p. 2, p. 14). This is commendable transparency, but it also means the earlier SentinelCMS numbers (~93%, p. 2) should not be cited.
- [I] **Minor presentation issues:**
  - The statements are in the singular ("The author declares", "The author thanks") for a six-author paper (p. 14).
  - Only one comparison is tested in the text, with only the plugin-level p-value given, despite paired tests being described for model comparisons (p. 6, p. 9; see §6).
- [I] **No negatives from unrelated code at realistic prevalence.** Both variants draw negatives from vulnerable plugins only, so the deployment false-alarm rate is unknown.

## 10. Threats to validity
- Internal (confounds, leakage, selection):
  - [V] Strong exact- and near-duplicate control with verified 0/0/0 cross-fold overlap (p. 5).
  - [V] In-sample stacking leakage is measured and corrected (p. 10).
  - [A] Semantic clones may remain (p. 13).
  - [I] Label noise (≤48.8% genuine positives) is the dominant confound. Diff-based labelling marks every function touched by a fix as vulnerable, including non-security edits (p. 4, p. 11).
  - [V] The filtered-subset comparison is confounded by easier test cases (p. 10).
- External (generalisability of sample/context):
  - [V] WordPress plugins only, PHP only, XSS/SQLi/RCE only (p. 5).
  - [A] Survivorship bias toward plugins with retained history (p. 13).
  - [I] Results may not transfer to other PHP frameworks (Laravel, Drupal) or to repository-level detection.
- Construct (do metrics measure the concept?):
  - [I] Macro-F1 averages a Safe-class F1 that depends heavily on negative sampling (Variant A vs B).
  - [I] Labels measure "touched by a security fix" more than "vulnerable".
  - [V] The per-class tables expose degenerate predictors that aggregate scores hide (p. 9).
- Statistical conclusion (power, multiple comparisons, variance):
  - [V] 5 folds give only five paired observations; a plugin-level test is used as the better-powered alternative (p. 6).
  - [V] CIs are reported for Variant B binary only (p. 8).
  - [V] No multiple-comparison correction is reported (pp. 6–10).
  - [V] A single seed (42) is used throughout (p. 7).
  - [I] Many between-model gaps (e.g. 0.562–0.601 on Variant B binary) have overlapping CIs (p. 8, Table 6).
- Reproducibility (data/code/setup reported?): [V] Good — hyper-parameters (p. 6–7), folds, per-fold predictions, fingerprinted results and a loader script are released (p. 14). Plugin code must be re-downloaded from WordPress.org (p. 14). [I] Reproducibility therefore depends on WordPress.org continuing to host old versions, the same pruning that already lost 54% of CVEs (p. 3).
- Funding and conflicts of interest: [V] "This research received no external funding"; no conflicts of interest are declared (p. 14). [I] The study re-evaluates the authors' own SentinelCMS (p. 2), so it is a self-evaluation; however, any bias would run against the authors' own earlier claims (~93% accuracy, p. 2), which the paper largely retracts, so it is unlikely to inflate the reported results.

## 11. Future research directions
- Stated by authors [A]:
  - extend expert review to several thousand functions with ≥2 annotators and adjudication, and evaluate on an expert-verified test set (p. 13);
  - use curated feeds that name entry points and sinks (p. 13);
  - semantic clone detection (p. 13);
  - a fully resourced transformer comparison on identical folds and a 256-token sensitivity run (p. 13);
  - require future detectors to clear trivial baselines such as function length (p. 13).
- Suggested by us [I]:
  - Run established PHP SAST tools (Semgrep PHP rules, Psalm taint mode, Progpilot) and 1–2 open LLMs on the released expert-verified 125/247 subset (p. 11). That would give a small but clean PHP LLM-vs-SAST-vs-ML comparison, directly addressing G5 and G2.
  - Report vulnerable-class F1 and precision at realistic prevalence alongside macro-F1.

## 12. Relevance to our research
- Research questions addressed (RQ ids): RQ2 (primary), RQ1 (SAST vs ML/DL only; no LLM), RQ4 (PHP; per-CWE-class behaviour), RQ5.
- How it informs our work [I]:
  - **RQ2:** a clean demonstration that duplicate leakage, contradictory labels, in-sample stacking and label noise shape measured performance more than model family. It is also a second study (beside shu2026evaluating) that reports trivial baselines and finds they are competitive, which strengthens G1.
  - **G5 (PHP):** gives real-CVE PHP evidence, but at function level and without LLMs or a standard SAST tool. The released corpus and expert-verified subset are a ready data source for a G5 study. G5 stays open only pending a novelty check against a likely competitor: Neef et al. 2026 (arXiv:2606.21397, "Evaluating LLMs for Real-World Web Vulnerability Detection"), which deininger2026open cites as comparing models on "web vulnerability detection in WordPress plugins" [@deininger2026open, p. 3]. It is not in our corpus and was not read; its content is unknown beyond that citation.
  - **G2:** the closest PHP analogue to a leakage-controlled same-benchmark comparison, missing the LLM arm.
  - **RQ4:** XSS is detected far better than RCE by learned models (p. 9), and SQLi per-class F1 is ≤ 0.146 (p. 9, Table 7). This is a hint that rare classes are effectively undetected by small ML models on PHP.
  - **C5 (class balance):** the choice of negatives flips the majority class and the failure direction of the same RF model (p. 9).

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ1 | On 24,917 real WordPress PHP functions (Variant B binary, plugin-grouped, de-duplicated), best macro-F1 0.601 (nested stacking); Bi-LSTM 0.573, SVM 0.562; no neural model leads in any of 6 settings | 7, 8 | V | weak–moderate (single study, single seed, ≤48.8% label precision, overlapping CIs) |
| RQ1 | An unnamed, unversioned intra-procedural lexical taint analyser detects 1.7–1.8% of PHP vulnerabilities (FNR 0.982; macro-F1 0.366 vs majority 0.350; MCC 0.035) | 5, 8, 9, 13 | V | weak for SAST in general (single bespoke tool) |
| RQ1 | No LLM or pre-trained transformer evaluated (CodeBERT not run: no GPU/transformers) | 13 | V | n/a (scope) |
| RQ2 | Plugin-grouped folds still had exact-duplicate groups spanning folds: 166 / 151 groups holding 1086 (A) / 676 (B) records (test-side share not reported; authors call them test copies, p. 10); 730/456 groups had contradictory labels; conflict removal + dedup + clone collapse cut the corpus by 50.4% / 19.3% (collapse alone 11,123 / 3714 records) | 4, 5 | V | moderate |
| RQ2 | A one-feature token-count baseline matches or beats TF-IDF RF in 4/6 settings; on Variant B binary it scores 0.572 vs Bi-LSTM 0.573 and best neural (uni-LSTM) 0.578 | 8 | V | moderate |
| RQ2 | Expert review: only 48.8% of cleaned positive diff-derived labels are genuine (73.0% HIGH, 44.7% MEDIUM, 0.7% LOW; single annotator) | 11 | V | moderate (n=400, 1 annotator) |
| RQ2 | In-sample stacking inflates macro-F1 by +1.27 pp on average (range −1.62 to +2.95) | 10 | V | moderate |
| RQ2 | Re-scored vs trivial predictors: always-vulnerable macro-F1 ≈0.316 (B) / 0.427 (A, = majority); best detectors beat majority by +0.251 (B) / +0.136 (A) and always-vulnerable by +0.285 (B); MCC ≤0.203 (Variant B only; A not reported) | 5, 8 | I | moderate (our pooled calculation from Table 2 counts vs fold-mean scores) |
| RQ4 | PHP per-class F1 (Variant B 4-class): XSS up to 0.500, SQLi ≤0.146, RCE ≤0.085; RF never predicts RCE | 9 | V | weak (rare classes) |
| RQ5 | Authors: label quality, not architecture, is the binding constraint; detectors should be required to clear trivial baselines | 12, 13 | A | moderate |

## 14. Key quotes
> "the taint analyzer misses about 98% of vulnerabilities" (p. 1)

> "Neural models do not lead in any of the six configurations" (p. 1)

> "the static analyzer misses about 98% of vulnerabilities" (p. 13)

[I] Scope note for the two "misses about 98%" quotes: "the taint analyzer" / "the static analyzer" is the paper's single unnamed, unversioned two-pass intra-procedural analyser (p. 5), which the authors call "intra-procedural and lexical" and whose low recall they attribute to "that implementation rather than taint analysis in general" (p. 13). Do not cite these quotes as evidence about PHP SAST tools in general.

> "future detectors in this domain should be required to clear such trivial baselines before semantic detection is claimed" (p. 13)

## Analyst notes
- Reading coverage: All 15 pages read from `fulltext.txt` (abstract, all sections, tables 1–12, back matter, references). Figures 1–3 are images not in the text layer; their content is described in captions and text, and the numbers come from the tables.
- Uncertainties:
  - The identity and provenance of the static taint analyser are unclear (in-house, no name or version).
  - The exact label precision of the full evaluated corpus is unknown (see §9).
  - Prevalence figures (74.5% / 46.2%) and always-vulnerable macro-F1 values are our calculations from Table 2 counts. They match the paper's majority-baseline accuracy 0.745 (p. 9) and 0.538 (p. 8).
  - The gap-report entry (G5) still describes this paper as "abstract only"; it is now full text.
