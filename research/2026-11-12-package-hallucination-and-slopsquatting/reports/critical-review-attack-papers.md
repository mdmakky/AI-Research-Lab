# Critical review — agent-attack papers (2026-11-12)

Scope: liu2026trust, wang2026package, hsu2026harmless. Reviewer: critical-reviewer agent (read-only); fixes applied by the orchestrator on 2026-11-12. `rlab validate` metadata verified and `rlab cite-check` OK for all three, before and after fixes.

## Verdicts
| Paper | Verdict | Fixes applied |
|---|---|---|
| liu2026trust | FIX NEEDED → fixed | 4 |
| wang2026package | FIX NEEDED → fixed | 4 |
| hsu2026harmless | FIX NEEDED → fixed | 5 |

## liu2026trust
1. Inferred per-cell denominators widened from "14–40" to "about 14–77" (Phi-4-mini 35.06% = 27/77, pp. 7–8); some values fit no simple fraction.
2. Benign status of target packages now cited to p. 14; whether they exist on PyPI is unclear.
3. RQ3 row corrected: two static scanners missed the Skills, one (SkillCheck, Repello) flagged them as low severity (p. 12).
4. RQ5 row rewritten to the authors' own limitation wording (p. 12); strength set to weak.

## wang2026package
1. "87 vs 267 numpy tasks" is not an inconsistency: 87 is the SASR denominator (27/87 = 31.03%, p. 16; Table 14 sums to 87, p. 27). Reworded as loose wording.
2. Inferred denominators corrected to about 9–100 (pp. 11, 14).
3. "Single run per cell" changed to "number of runs not reported".
4. Agent configuration table cited to p. 30.

## hsu2026harmless
1. Benign-Skill agent baselines (3.33% / 1.05% / 1.11%, p. 6) kept, with caveats: separate task configurations (not a funnel), "executed install" not defined as installing a non-existent package, no task counts or backbone models.
2. Runtime-safeguard table strengthened as ambiguous: "None" row equals the model-level Table 2 result, so safeguards were tested on model outputs; authors' "limited mitigation" labelled [A].
3. Snyk-evasion claim relabelled [A] (Table 8 shows no detection result).
4. Frontmatter range corrected to 60–91%.
5. RQ2 row split into model-level (moderate) and agent-level (weak).

## Cross-paper notes (recorded in the evidence matrix)
- liu2026trust and hsu2026harmless share three authors, the benchmark and the scanner set: scanner results are not independent replication.
- Baseline hallucination on the same model/dataset differs between them (Qwen2.5-Coder-32B LLM_AT: 0% GHR vs 3.53%; Llama-3.1-8B: 8.76% vs 16.43%); the metrics and prompt filtering differ.
- Claude Code install behaviour differs across setups (wang: reverted instead of installing in 37.9% of cases; hsu: 90.77% executed installs under NPA, backbone unreported); not poolable.
