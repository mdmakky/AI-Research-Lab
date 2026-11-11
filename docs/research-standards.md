# Research standards

The rules every skill and agent in this workspace follows. One source of truth: change rules here, not in individual skills.

## 1. Evidence labels
Every substantive statement about a paper or the literature carries one label:

| Label | Short | Meaning | Requirement |
|---|---|---|---|
| VERIFIED | [V] | Checked against the paper's own data, tables, figures or results text. | Page ref `(key, p. N)` |
| AUTHOR-CLAIM | [A] | The authors state it; we cannot independently check it (e.g. claims of novelty, interpretations, conclusions beyond the data). | Page ref |
| INTERPRETATION | [I] | Our own reasoning, synthesis or critique. | Say what it is based on |

Page refs use the `=== [PDF page N] ===` markers in `fulltext.txt` (PDF page index, not printed page number). When a quote is used, it is copied verbatim from `fulltext.txt`.

Citation syntax:
- Inside a paper's own `analysis.md`: `(p. N)`.
- Everywhere else (evidence matrix, reports, reviews): pandoc style `[@key, p. N]` or `[@key1; @key2]`. Keys are the folder names under `papers/`. This works with `references.bib` and pandoc.
- `rlab cite-check <project> <file...>` must pass before any written document is handed to the user.

## 2. Never invent
- Every DOI, title, author, year and venue comes from `metadata.json` (resolved by `rlab add` from Crossref/OpenAlex/arXiv/PubMed). Never type a DOI from memory.
- Every finding, number, limitation and quote comes from the paper text. If the paper does not report something, write "not reported".
- Every citation in written output uses an existing paper key in the project. A claim with no source is either removed or labelled [I].
- If something cannot be found or verified, say so plainly. An honest "unknown" beats a plausible guess.

## 3. Source quality tiers
Prefer higher tiers; state the tier when it matters to the argument.

1. Peer-reviewed journal articles and full papers at reputable conferences (`venue_kind: published`); systematic reviews and meta-analyses at the top for evidence synthesis.
2. Peer-reviewed workshop papers, book chapters from academic publishers.
3. Preprints (`venue_kind: preprint`, e.g. arXiv): usable, always flagged "not peer-reviewed". If a published version exists, use it instead.
4. Theses, technical reports, grey literature: background only, flagged.
5. Blogs, news, Wikipedia, vendor material: never cited as evidence. May guide searching.

`venue_kind: published` means the work appeared in a journal or proceedings; it is not proof of rigorous review. Watch for predatory venues (unknown publisher, implausibly fast review, no indexing) and flag them.
Retracted papers (`RETRACTED` flag from `rlab`) are excluded from evidence; mention only as retracted.

## 4. Reading depth
- Detailed methodology, dataset, setup, metrics, findings and limitations require the full text (`evidence_basis: full-text`).
- Abstract-only analysis (`evidence_basis: abstract-only`) may fill objective and headline claims labelled [A] only. All method sections say "full text not available". Abstract-only papers carry less weight in synthesis and gap claims; say so.
- Read the whole paper: methods, results, tables, limitations, appendix if relevant. Note skipped parts in "Analyst notes".

## 5. Critical appraisal checklist
For every empirical paper check and record:
- Sample size and how it was chosen; power or uncertainty reporting.
- Baselines and whether they are fair and current.
- Evaluation design: train/test separation, leakage, cross-validation, held-out data, blinding, control groups.
- Statistical testing: tests, effect sizes, confidence intervals, multiple comparisons.
- Reproducibility: data, code, hyper-parameters, protocol available?
- Conflicts of interest and funding where relevant.
- Whether conclusions go beyond the data (mark those [A] and note it).

Evidence strength: **strong** = adequate N, sound design, replicated or consistent across studies; **moderate** = sound design but single study or limited N; **weak** = small/unclear N, design flaws, abstract-only, or preprint without replication.

## 6. Contradictions
When papers disagree: record both sides in the evidence matrix "Contradictions" section with page refs, then compare data, population, method, metric and time. Offer an explanation only as [I]. Never silently pick a side.

## 7. Research gaps and novelty
A gap is reported only when:
1. It is supported by evidence from analysed papers (explicit future-work statements, consistent limitations, contradictions, untested populations/conditions, missing method comparisons).
2. A dedicated novelty check was run: at least 3 targeted searches (`rlab search`) across at least 2 sources, recent years included, plus a web search for very recent work. Queries, date and closest hits are recorded in the gap entry.
3. Confidence is stated. "No paper found" is phrased as "we found no paper that ... (searches on DATE)", never "this has never been studied".

## 8. Copyright and access
- Download only legal open-access copies: OpenAlex/Unpaywall OA locations, arXiv, Europe PMC, publisher OA pages. `rlab fetch` enforces this and refuses shadow libraries.
- Never bypass paywalls, logins, CAPTCHAs, or rate limits. Never use Sci-Hub, LibGen, Anna's Archive or similar.
- When no OA copy exists: tell the user and ask them to obtain it through their library, then `rlab attach`. Otherwise analyse abstract-only and label it.
- Quotes stay short and attributed. PDFs stay inside the project folder and are not redistributed.

## 9. Preservation
- Original PDFs (`paper.pdf`), extracted text (`fulltext.txt`) and completed analyses (`status: complete`) are never overwritten or deleted without the user's explicit permission. A hook asks the user first (once `setup/claude-settings.json` is installed).
- Analysis status flow: `draft` (in progress) -> `ready` (analyst self-check passed) -> `complete` (critical review passed). Fix review findings while the analysis is `ready`.
- Revisions to a completed analysis go in a new section `## Revision YYYY-MM-DD` with what changed and why, after the user agrees.
- `research-log.md` is append-only.

## 10. Talking to the user (a beginner researcher)
- Progress updates: short, what was done, what was found, what is next.
- Explain research terms on first use in one plain sentence (e.g. "a *systematic review* is a study that collects and evaluates all studies on a question").
- Explain important decisions and their reason: scope cuts, exclusions, weak evidence, gaps.
- Ask only for: scope or research-question choices that change the direction, missing full-text access, paid or restricted resources, and anything destructive.
