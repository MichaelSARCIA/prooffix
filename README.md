# ProofFix: Prove, Fix, Coach with IBM Bob

ProofFix is an agentic code-quality loop that dramatically accelerates the most expensive parts of software development. Developers report spending roughly 5 hours per week on code review — about 12.5 % of a standard work week — and approximately 45 % of their total time fixing bugs or paying down technical debt rather than shipping new features.[^1] ProofFix addresses both drains at once: across five bug classes in a realistic Python shopping-cart module, the Reviewer → Debugger → Coach loop completed in **7 minutes total** compared to an estimated **225 minutes (3 h 45 min) of equivalent manual work** — a **~32× speedup** — while producing a machine-verified proof test and a targeted coaching note for every single finding.

[^1]: Codacy Developer Survey. "The State of Code Quality." https://blog.codacy.com/codacy-developer-survey

## Why this is different

Most AI review tools stop at *suggesting* a fix. ProofFix goes three steps further: it first **proves** the bug exists by writing a test that goes red, then **verifies** the fix by running the full suite green, and only then **coaches** the developer on root cause and prevention — so every finding arrives with evidence, not opinion.

## Problem

Code review is slow, manual, and inconsistent. Reviewers spot symptoms but rarely write a reproducible test case. Fixes land without suite validation. Coaching notes are written once and forgotten. The result: the same classes of bug recur sprint after sprint.

## Approach

ProofFix implements a four-phase agentic loop, each phase handled by a dedicated IBM Bob mode:

1. **Reviewer** — static analysis of `demo_app/`, ranked findings written to `out/findings.json`
2. **Debugger** — for each top finding: write a failing repro test → apply the minimal patch → run full suite
3. **Coach** — produce `out/REVIEW.md` with risk, proof, diff, root-cause analysis, and prevention advice
4. **Scoring** — compare findings against `eval/seeded_bugs.json` ground truth

Each mode is constrained by `AGENTS.md` and `.bob/` rules files so it stays focused and never over-reaches.

## Bob Features Used

| Feature | Role |
|---|---|
| **Reviewer mode** | Read-only static analysis; ranks findings by risk; no edits allowed |
| **Debugger mode** — write tools + `execute_command` | Writes repro tests, applies patches, runs `pytest` |
| **Coach mode** — write tools | Produces structured markdown report with scoring |
| **`AGENTS.md`** | Defines project layout, stack, conventions, and money-type rule enforced across all modes |
| **`.bob/` rules files** | Efficiency rules (no re-reads, targeted edits, short replies) applied globally |

## Results

*Assumptions: manual times are estimates for an experienced developer on unfamiliar code; loop times include AI review, test generation, patching, and full pytest run.*

| Finding | Severity | Category | Manual est. | Loop time | Speedup |
|---|---|---|---|---|---|
| F-01 — `eval()` RCE in `apply_discount` | Critical | security/unsafe-input | 55 min | 2 min | 28× |
| F-02 — off-by-one in `subtotal()` | High | logic/off-by-one | 40 min | 1 min | 40× |
| F-03 — `add_item` accepts `qty ≤ 0` | High | edge-case/unhandled-input | 40 min | 1 min | 40× |
| F-04 — `float` arithmetic for money | Medium | correctness/float-arithmetic | 60 min | 2 min | 30× |
| F-05 — deep nesting in `grand_total` | Medium | maintainability/duplication | 30 min | 1 min | 30× |
| **Total** | — | — | **225 min** | **7 min** | **~32×** |

**Recall:** 5/5 seeded bugs found (100 %) · **Precision:** 5/8 reported findings matched ground truth (62 %; 3 bonus findings were valid but untracked) · Full suite: **15 tests passing**

## Data Sources

Self-authored code only. `demo_app/cart.py` was purpose-built for this project with intentionally seeded bugs. No external datasets, no network calls, no personal or sensitive data anywhere in the repository.

## How to Run

```bash
# 1 — install dependencies (pytest only)
python -m pip install pytest

# 2 — run the full passing suite
python -m pytest -q

# 3 — run a single repro test (example: off-by-one)
python -m pytest -q tests/repro/test_F02.py

# 4 — read the full review report
cat out/REVIEW.md
```

To run the full agentic loop yourself, open IBM Bob and follow the phase prompts in `MASTER_PROMPT.md`:

| Phase | Bob mode | Command |
|---|---|---|
| 0 — Scaffold | Agent | Create `demo_app/`, `tests/`, `eval/` |
| 1 — Review | Reviewer | Analyse `demo_app/`, write `out/findings.json` |
| 2 — Repro & Fix | Debugger | Failing test → patch → green suite per finding |
| 3 — Coach | Coach | Write `out/REVIEW.md` with scoring and time-saved |
