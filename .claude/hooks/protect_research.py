#!/usr/bin/env python3
"""PreToolUse hook: ask the user before anything overwrites or deletes protected research files.

Protected: paper.pdf, fulltext.txt, completed analyses (frontmatter `status: complete`),
research-log.md (append-only), registry.json (managed by rlab), and any rm/mv inside research/.
Prints a permission decision of "ask" on stdout; silent exit 0 means "no opinion".
"""
import json
import re
import sys
from pathlib import Path


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


def completed(path):
    m = re.match(r"^---\s*\n(.*?)\n---", path.read_text(encoding="utf-8", errors="replace"), re.S)
    return bool(m and re.search(r"^status:\s*complete\s*$", m.group(1), re.M))


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return
    tool, inp = event.get("tool_name", ""), event.get("tool_input") or {}
    if tool == "Bash":
        cmd = inp.get("command", "")
        if "research" in cmd and re.search(r"(^|[\s;&|(])(rm|rmdir|mv|shred|truncate|unlink)\s", cmd):
            ask("This command may delete or move research files (papers, analyses, logs). Approve only if intended.")
        return
    if tool not in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        return
    raw = inp.get("file_path") or inp.get("notebook_path") or ""
    p = Path(raw)
    if not raw or "research" not in p.parts or not p.exists():
        return
    if p.name in ("paper.pdf", "fulltext.txt"):
        ask(f"{p.name} is an original source file and must not be modified.")
    if p.name == "analysis.md" and completed(p):
        ask("This paper analysis is marked complete. Changing it needs your explicit permission "
            "(the change should be added as a dated revision section).")
    if p.name == "research-log.md" and tool == "Write":
        ask("The research log is append-only; a Write would replace its history.")
    if p.name == "registry.json":
        ask("registry.json is managed by scripts/rlab.py; edit it by hand only if you are sure.")


if __name__ == "__main__":
    main()
