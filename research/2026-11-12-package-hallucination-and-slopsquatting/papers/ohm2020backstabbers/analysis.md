---
key: ohm2020backstabbers
status: complete
evidence_basis: full-text
design: Manually curated dataset of real malicious packages + qualitative attack-tree taxonomy (descriptive statistics)
dataset: 174 malicious packages from npm (109), PyPI (28), RubyGems (37) used in real attacks, Nov 2015-Nov 2019
sample_size: 174 packages analysed (of 469 identified; 59 proof-of-concept packages excluded)
metrics: descriptive shares (trigger phase, injection technique, conditional execution, objective, OS, obfuscation), Levenshtein distance, days to disclosure, code clusters
main_finding: Among 174 real malicious npm/PyPI/RubyGems packages, 61% used typosquatting and 56% executed at install time (PyPI: 75% and 96%).
relevance: medium
analysed: 2026-11-12
---
<!-- Frontmatter: single-line values; they feed literature-matrix.md via `rlab index`.
     status: draft (in progress) -> ready (analyst self-check passed) -> complete (critical review passed).
     evidence_basis: full-text | abstract-only. abstract-only analyses must not fill methodology detail.
     relevance: high | medium | low. -->

# Backstabber’s Knife Collection: A Review of Open Source Software Supply Chain Attacks

- Authors: Ohm, Marc; Plate, Henrik; Sykosch, Arnold; Meier, Michael
- Year / venue: 2020, Lecture Notes in Computer Science (book)
- DOI: 10.1007/978-3-030-52683-2_2 · URL: https://doi.org/10.1007/978-3-030-52683-2_2
- Source text: `fulltext.txt` (page refs = PDF page index)

Labels: **[V]** verified in the paper's own data/tables/results · **[A]** author claim · **[I]** our interpretation.
Every [V]/[A] item ends with a page ref `(p. N)`. Write "not reported" when the paper does not say.

**Source tier:** Tier 2 (an LNCS proceedings chapter, per metadata), 2020.
- The analysed text is the arXiv v1 version (arXiv:2005.09535v1, 19 May 2020; p. 1). It may differ slightly from the published chapter.
- We use it as **background** because it predates LLMs, not because of its source quality. It is a seminal paper (241 citations per metadata).

## 1. Research objective
- [A] Give a structured overview of how attackers inject malicious code into open-source dependency trees and trigger it. The goal is to support preventive and detective safeguards (p. 1).
- [A] Provide a manually curated dataset of malicious packages used in real-world attacks (pp. 1–2).

## 2. Research questions / hypotheses
- No formal RQs. There are two contributions (p. 2):
  1. manual analysis and categorisation of 174 real malicious packages (2015–2019);
  2. two attack trees, one for *injection* and one for *execution*.

## 3. Methodology
- Research design: [V] Qualitative and descriptive (pp. 4–5).
  - The attack trees were built iteratively. Each malicious package or information source was mapped to a node; a new node was added when none fitted.
  - Packages were analysed and categorised by hand.
- Approach — the attack trees (read from Fig. 2, p. 7, and Fig. 3, p. 9):
  - [V] **Injection tree.** Root: "Injection of Malicious Code (into dependency tree)" (p. 7).
    - **Create New Package**: Trojan Horse; Typosquatting; Use After Free (p. 7).
    - **Infect Existing Package** (p. 7):
      - Inject into Source: a pull request as a contributor; or a commit as a maintainer, using weak/compromised credentials or API tokens, or social engineering to become maintainer.
      - Inject during the Build: compromise the build system, by manipulating the package download or running a malicious build on shared systems.
      - Inject into Repository System: weak/compromised credentials or API tokens; exploiting vulnerabilities; deploying to an alternative repository or mirror.
  - [V] **Execution tree** (p. 9). Root: "Execute Malicious Behavior".
    - During Different Life Cycle Phases: Install Scripts; Test Case; Runtime.
    - Conditional Execution: Application State; Dependency Tree; Operating System.
  - [A] **New packages.** A new package "using a name that is not used by anybody else avoids interference with other legitimate project maintainers. However, such a package has to be discovered and referenced by downstream users", for example via typosquatting or by promoting a trojan horse (p. 7).
  - [A] **Install-time execution.** "Such install scripts exist for Python and Node.js" and run automatically during installation (p. 8).
  - [A] **Import-time execution.** In Python, code can be triggered at runtime by putting it in `__init__.py`, which runs on `import` (p. 9).
- Baselines or comparison conditions: not applicable (descriptive study).

## 4. Dataset and sample
- Data source(s):
  - [V] The authors reviewed the Snyk vulnerability database, language-specific security advisories and research blogs between 2 July and 2 August 2019, and updated the review on 27 January 2020 (p. 4).
  - [V] The registries had removed the malicious code, so it was retrieved from deprecated mirrors, internet archives and research repositories (p. 4).
  - [V] Publication dates come from Libraries.io (p. 5).
- Sample size (N) and unit:
  - [V] 469 malicious packages were identified; 59 proof-of-concept packages were excluded; at least one malicious version was obtained for 174 (p. 9).
  - [V] Download success by registry (pp. 9–10):

    | Registry | Obtained / identified | Rate |
    |---|---|---|
    | npm | 109/374 | 29.14% |
    | PyPI | 28/44 | 63.64% |
    | RubyGems | 37/41 | 90.24% |
    | Maven Central | 0/10 | 0% |

  - [V] Composition of the 174: npm 62.6%, PyPI 16.1%, RubyGems 21.3% (p. 10).
- Sampling / selection method: [V] Every malicious package found in the sources whose code could be obtained (pp. 4, 9). This is a convenience sample of *disclosed* and *retrievable* attacks.
- Data availability: [V] On GitHub, but "access will be granted on justified request only due to ethical reasons" (p. 10).

## 5. Experimental setup
- Procedure, settings, hyper-parameters, tools: [V] Manual code analysis (pp. 4–5, 11–16).
  - Confirms maliciousness.
  - Classifies each package by trigger, conditions, injection technique, objective, targeted OS and obfuscation.
  - Finds clusters through code reuse and dependency relations.
  - The number of coders and their agreement are not reported.
- Code availability: not applicable / not reported.

## 6. Evaluation metrics
- Metric — what it measures — why chosen:
  - [V] Category shares per registry and overall (Figs. 6–11).
  - [V] Days between publication and disclosure.
  - [V] Levenshtein (edit) distance from a typosquat to its target.
  - [V] Cluster size and timing (pp. 10–16).
- Statistical testing: descriptive statistics only (mean, min, max, standard deviation, median; pp. 11–12, 15). No tests.

## 7. Key findings
1. [V] **Exposure time.** On average a malicious package was available for 209 days before public reporting (median 67, max 1,216). PyPI had the highest average (p. 11).
2. [V] **Install-time execution dominates.**
   - Overall: 56% of packages trigger at install time, 43% at runtime, 1% in tests (p. 11).
   - By registry (Fig. 6, p. 11):
     - npm: 64% install, 34% runtime, 2% test.
     - PyPI: 96% install.
     - RubyGems: 100% runtime, because Ruby has no install hooks.
   - [I] The remaining 4% for PyPI appears to be runtime, judging from the bar shading and consistency with the overall 43%.
3. [V] **Conditional execution** (p. 12).
   - 41% of packages check a condition (application state, dependency tree or OS) before running. This helps them evade analysis sandboxes.
   - PyPI and RubyGems packages mostly run unconditionally.
4. [V] **Typosquatting dominates injection** (p. 12).
   - 61% of packages mimic existing names.
   - The mean edit distance to the target is 2.3 (median 1, max 11; e.g. `pythonkafka` → `kafka-python`).
   - Common techniques: adding or removing hyphens, dropping letters, swapping commonly mistyped letters.
   - [V] Some typosquats have distance 0: they reuse the exact name of a package from another repository, e.g. `python-sqlite`, which exists under the same name in the Linux apt repository (p. 12).
   - From Fig. 8: PyPI is 75% typosquatting and 25% trojan horse; overall, trojan horses are 11% (p. 13).
   - [V] A trojan horse is "a new package which consist of nothing but the malicious package", with "No meaningful typo-squatting targets" (p. 13).
5. [V] **Objectives.** Data exfiltration is the most common goal, at 55% of packages (pp. 16, 18).
   - Targets include `~/.ssh/*`, `~/.npmrc` and environment variables (p. 13).
   - 34% are droppers, 5% backdoors, 3% denial-of-service, 3% financial gain (p. 13).
   - 53% are OS-agnostic (p. 14). 49% use obfuscation, mostly Base64/hex encoding (pp. 14–15).
6. [V] **Clusters** (pp. 15–16).
   - 21 clusters cover 157 of the 174 packages (90%).
   - The largest (crossenv) has 36 packages, published in two waves.
   - One cluster spans npm and RubyGems.
7. [A] **Countermeasures.** These include multi-factor authentication for maintainers, "version pinning and disablement of install scripts for open source users", and isolated builds. They should be "enforced by default" (p. 16).

## 8. Limitations stated by the authors
- [A] The dataset is biased toward npm. No malicious packages could be obtained for Java (Maven) or PHP (p. 18).
- [A] About 34% are droppers whose second-stage payload may no longer be available (p. 18).
- [A] Most packages were downloaded from mirrors or archives, which is itself an injection vector in the tree. The authors argue the packages are still valid because maliciousness was confirmed by hand (p. 18).
- [A] The attack trees are not complete: they omit vectors not yet observed or described (p. 4).
- [A] How attackers select which package to infect cannot yet be validated from the data (p. 7).

## 9. Limitations we identified
- [I] **Small PyPI sample.** Only 28 PyPI packages; the PyPI percentages rest on very few cases.
- [I] **Detected attacks only.** Only disclosed and retrievable attacks are included. Undetected or quickly deleted packages are missing, so the shares describe *detected* attacks.
- [I] **Unknown reliability of the hand coding.** Categorisation was done manually in a single pass, with no reported agreement between coders.
- [I] **Pre-LLM.** The attack tree has no node for discovery through automated recommendation, which is exactly the channel slopsquatting uses. Registry defences may have changed since 2019; the paper does not cover this.
- [I] **Bar-chart readings.** Per-registry shares are read from bar charts (Figs. 6–11), whose text extraction is garbled. We checked Figs. 6 and 8 against the PDF images.

## 10. Threats to validity
- Internal: the classification is subjective and manual, with no agreement measure.
- External: mostly npm; 2015–2019 only; registries and attacker tactics have changed since.
- Construct: "typosquatting" rests on a judgement of name similarity, and "trojan horse" is a catch-all category.
- Statistical conclusion: descriptive only; the PyPI subset is small.
- Reproducibility: the dataset is available on request (p. 10), and the attack trees are fully shown (pp. 7, 9).

## 11. Future research directions
- Stated by authors [A] (p. 18):
  - collect existing safeguards and run a gap analysis against the attack vectors;
  - scan whole repositories, exploiting code reuse across campaigns;
  - use the labelled dataset for supervised learning;
  - use the dataset as a benchmark, and keep curating it.
- Suggested by us [I]:
  - extend the injection tree with an "AI-recommended name" discovery node (slopsquatting) under Create New Package;
  - measure whether slopsquatted packages follow the same install-time and conditional-execution patterns.

## 12. Relevance to our research
- Research questions addressed (RQ ids):
  - RQ2: the attack model, i.e. how a registered name becomes malicious code running on the victim's machine.
  - RQ3: baseline countermeasures (disabling install scripts, version pinning).
  - RQ5: background for designing a safe study.
- How it informs our work [I]:
  - **Placing slopsquatting in the tree.**
    - It is a *Create New Package* attack, closest to the "trojan horse": a fresh name with no lookalike target.
    - It differs from typosquatting in how victims find the package. Here the LLM supplies the "discovery and referencing" step that the authors identify as the obstacle for new packages (p. 7).
  - **Pre-LLM analogue of name confusion.** [V] Some typosquats have edit distance 0 because they reuse an existing name from another repository (`python-sqlite` from apt; p. 12). This is a pre-LLM analogue of the cross-ecosystem and import-name confusion seen in raj2026names and twist2026library: a correct-looking name that resolves to someone else's package.
  - **Installing is enough to be compromised.**
    - Install-time execution is the main trigger on PyPI (96%; p. 11), and code can also run on import via `__init__.py` (p. 9).
    - An agent or user that runs `pip install` / `npm install` on a hallucinated name can be compromised immediately, so a defence must act **before** installation.
  - **Implication for a measurement study.**
    - Use read-only registry metadata; do not install packages.
    - Any dynamic analysis must run in a sandbox, since 41% of malicious packages run only under certain conditions (p. 12) and may evade sandboxes.
  - **Implication for a lightweight defence.**
    - Combine a pre-install existence/metadata check with the authors' user-side countermeasures: version pinning and disabled install scripts (p. 16).
    - The edit-distance profile of typosquats (mean 2.3, median 1; p. 12) can inform a lookalike check for hallucinated names.
  - **Evidence strength: moderate** as background. The data are real-world, but the study is descriptive, pre-2020, and the PyPI subset is small.

## 13. Evidence table (for the evidence matrix)
| RQ | Claim | Page | Label | Strength |
|---|---|---|---|---|
| RQ2 | Attack tree: new malicious packages enter via Create New Package (trojan horse, typosquatting, use-after-free) but must be "discovered and referenced" by downstream users | 7 | A | moderate |
| RQ2 | 56% of 174 real malicious packages execute at install time (PyPI 96%, npm 64%); Python and Node.js support install scripts, and Python `__init__.py` runs on import | 8, 9, 11 | V | moderate |
| RQ2 | 61% of malicious packages used typosquatting (PyPI 75%); mean edit distance to target 2.3, median 1; some reuse another repository's exact name (distance 0, e.g. python-sqlite from apt) | 12, 13 | V | moderate |
| RQ2 | Trojan-horse packages with no lookalike target are 11% overall and 25% on PyPI, the closest pre-LLM analogue to slopsquatted names | 13 | V (shares) / I (analogy) | weak |
| RQ2 | Malicious packages stayed available for 209 days on average (median 67) before disclosure; data exfiltration is the most common goal (55%) | 11, 18 | V | moderate |
| RQ4 | 41% of malicious packages execute only under conditions (app state, dependency tree, OS), which hinders sandbox-based dynamic detection | 12 | V | moderate |
| RQ3 | Recommended user-side countermeasures: version pinning and disabling install scripts, enforced by default | 16 | A | weak |

## 14. Key quotes
> "such a package has to be discovered and referenced by downstream users in order to end up in the dependency trees of victim packages" (p. 7)

> "Such install scripts exist for Python and Node.js, and may be used to perform pre- or post-installation activities." (p. 8)

> "most malicious packages (56%) start their routines on installation" (p. 11)

## Analyst notes
- Reading coverage: all 21 PDF pages.
  - Figs. 2, 3, 6 and 8 were read from the PDF images, because the extracted text of the trees and bar charts is garbled.
  - Figs. 7, 9, 10 and 11 were used only where the body text states the overall figure.
- Uncertainties:
  - The PyPI 4% segment in Fig. 6 (runtime vs test) is inferred from shading and arithmetic.
  - The published LNCS version was not compared with the arXiv text.
  - The conference behind the LNCS volume is not stated in the metadata or the text, so we do not name it.
- Critical-review fixes applied (2026-11-12):
  - tier wording;
  - data exfiltration at 55% (pp. 16, 18);
  - `python-sqlite` distance-0 typosquat (§7.4, §12, §13).
