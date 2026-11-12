# Claude Code sessions for this workspace

Snapshot of `~/.claude/projects/-Users-makky-Downloads-AI-Research-Lab-main/` (conversation transcripts `*.jsonl`, subagent transcripts in the matching folders, and the auto-memory in `memory/`).

## Restore on another computer

1. Clone this repo, e.g. to `~/Downloads/AI-Research-Lab-main`.
2. Claude Code stores sessions per project folder. The folder name is the absolute path of the workspace with every `/` replaced by `-`. Copy the sessions there:

```bash
cd ~/Downloads/AI-Research-Lab-main          # your clone
DEST=~/.claude/projects/$(pwd | sed 's#/#-#g')
mkdir -p "$DEST"
rsync -a --exclude README.md claude-sessions/ "$DEST/"
```

3. Start `claude` in the clone and run `/resume` to pick a session (or `claude --resume`).

If your username or path differs from `/Users/makky/Downloads/AI-Research-Lab-main`, file paths inside old transcripts will point to the old location; the research itself lives in `research/` and can always be continued with "Resume research <project-id>".
