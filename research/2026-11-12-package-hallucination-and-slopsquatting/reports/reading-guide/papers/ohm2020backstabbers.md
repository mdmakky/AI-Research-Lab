## Backstabber’s Knife Collection: A Review of Open Source Software Supply Chain Attacks
> **Takeaway:** Before AI coding tools existed, this study of 174 real malicious packages showed that most attacks used lookalike names and most ran their harmful code the moment the package was installed [@ohm2020backstabbers, p. 11; @ohm2020backstabbers, p. 12]. It explains why simply installing a hallucinated package name can be dangerous.

| Item | Detail |
|---|---|
| Authors | Marc Ohm, Henrik Plate, Arnold Sykosch, Michael Meier |
| Year · Venue | 2020 · Lecture Notes in Computer Science (proceedings chapter) |
| Status | Peer-reviewed (LNCS proceedings chapter); our copy is the arXiv version; a 2020 background paper that predates AI coding assistants |
| Identifier | DOI 10.1007/978-3-030-52683-2_2 (arXiv 2005.09535) |
| Paper type | Descriptive review: hand-curated dataset of real malicious packages plus attack trees |
| Relevance to us | Medium — RQ2 (main), RQ3 and RQ5 (background) |

### In plain words
A software supply chain attack hides malicious code in a package that other people's software depends on. Packages come from registries such as npm (JavaScript), PyPI (Python) and RubyGems (Ruby). Typosquatting means registering a name close to a popular package so that people install it by mistake. The authors collected real malicious packages from these registries, analysed them by hand and drew attack trees, diagrams of the different ways an attack can be carried out [@ohm2020backstabbers, p. 1; @ohm2020backstabbers, p. 2]. Slopsquatting is a newer variant of the same attack in which an AI model, not a human typo, supplies the wrong name.

### How they did it
1. They searched the Snyk vulnerability database, security advisories and research blogs in mid-2019 and updated the search in January 2020 [@ohm2020backstabbers, p. 4].
2. Registries had removed the malicious code, so they recovered it from old mirrors, internet archives and research repositories [@ohm2020backstabbers, p. 4].
3. They analysed each package by hand: when it runs, under what conditions, how it got in, what it tries to do and whether it hides its code [@ohm2020backstabbers, p. 4; @ohm2020backstabbers, p. 5].
4. They built two attack trees, one for getting malicious code into a dependency tree and one for running it [@ohm2020backstabbers, p. 7; @ohm2020backstabbers, p. 9].
5. Results are descriptive shares and averages, with no statistical tests [@ohm2020backstabbers, p. 11].

### Data and setup
- 469 malicious packages were identified, 59 proof-of-concept packages were excluded, and code was obtained for 174 [@ohm2020backstabbers, p. 9].
- Code was obtained for 109 of 374 npm packages, 28 of 44 PyPI packages, 37 of 41 RubyGems packages and none of 10 Maven packages [@ohm2020backstabbers, p. 9; @ohm2020backstabbers, p. 10].
- The dataset is on GitHub but shared only on justified request, for ethical reasons [@ohm2020backstabbers, p. 10].
- The number of people coding the packages and their agreement are not reported.

### Key findings
- [V] 56% of packages start their malicious code at install time; on PyPI the share is 96% [@ohm2020backstabbers, p. 11].
- [V] 61% used typosquatting. The mean edit distance (number of single-letter changes) to the imitated name is 2.3 [@ohm2020backstabbers, p. 12].
- [V] Some reuse the exact name of a package from another repository, such as python-sqlite from the Linux apt repository [@ohm2020backstabbers, p. 12].
- [V] Trojan horses, new packages with no lookalike target, are 11% overall [@ohm2020backstabbers, p. 13].
- [V] Malicious packages stayed available for 209 days on average before public reporting (median 67) [@ohm2020backstabbers, p. 11].
- [V] 41% run only under certain conditions, which helps them evade analysis sandboxes (isolated test environments) [@ohm2020backstabbers, p. 12].
- [V] Data theft is the most common goal, at 55% [@ohm2020backstabbers, p. 18]. Targets include SSH keys, npm credentials and environment variables [@ohm2020backstabbers, p. 13].
- [A] A new malicious package "has to be discovered and referenced" by users before it can do harm [@ohm2020backstabbers, p. 7].
- [A] The authors recommend version pinning and disabling install scripts, enforced by default [@ohm2020backstabbers, p. 16].

### Limitations and weaknesses
- [A] The dataset leans towards npm, and no packages could be obtained for Java or PHP [@ohm2020backstabbers, p. 18].
- [A] About 34% are droppers whose second-stage download may be gone [@ohm2020backstabbers, p. 18].
- [A] The attack trees are not complete [@ohm2020backstabbers, p. 4].
- [I] Only 28 PyPI packages, so PyPI shares rest on very few cases.
- [I] Only detected and retrievable attacks are included; undetected ones are missing.
- [I] Hand coding without any agreement check, and per-registry shares are read from bar charts.
- [I] The data end in 2019, before AI coding tools, and registry defences have changed since.

### Gaps and future work this paper leaves open
- [V] G1: install-time execution means the install itself is the harmful event [@ohm2020backstabbers, p. 11]. [I] Measuring generated text alone therefore misses the moment of harm.
- [A] G2: its user-side countermeasures (pinning, disabled install scripts) support a lightweight guard on the user's machine [@ohm2020backstabbers, p. 16].
- [V] G5: packages stayed live for 209 days on average [@ohm2020backstabbers, p. 11]. [I] Watching hallucinated names for six months or less can miss later abuse.
- [I] Its attack tree has no branch for discovery through AI recommendations, which is exactly the route slopsquatting uses.

### Why it matters for your research
This paper gives you the threat model. Slopsquatting is a "create new package" attack in which the AI performs the discovery step the authors saw as the attacker's main obstacle [@ohm2020backstabbers, p. 7]. Because most malicious packages run on install, a defence must act before installation. For a safe study, never install unknown packages; use read-only registry data. The typosquat edit-distance profile can help set thresholds for a lookalike check.

### Connections to other papers
- [V] okwor2026hallucination confirmed offline that install-time code runs through setup.py and npm postinstall scripts [@okwor2026hallucination, p. 7].
- [V] churilov2026range found 25 of 2,282 hallucinated names registered within about six months, one with malware [@churilov2026range, p. 12].
- [V] zheng2026when found 86.48% of invented Rust crate names within 5 edits of a real crate [@zheng2026when, p. 7], close to the typosquat distances here.
- [I] Its python-sqlite case resembles the import-name confusion that twist2026library and raj2026names handle in opposite ways [@twist2026library, p. 4; @raj2026names, p. 8].
