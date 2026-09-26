# Efficiency rules (usage budget is limited)

- Read only files needed for the current step. No repo-wide scans, no re-reading unchanged files.
- Pass file paths between subtasks, not contents.
- Never rewrite a whole file for a small change; use targeted edits.
- Run only the relevant test first, then the full suite once per fix.
- Keep replies short: status of 3 lines max, no restating the task, no summaries of code you just wrote.
- Cap output: max 8 findings, max 5 fixes, coaching notes max 60 words each.
- Ask a question only when blocked; otherwise state the assumption in one line and proceed.
- After 2 failed attempts at a step, stop and report instead of retrying.
