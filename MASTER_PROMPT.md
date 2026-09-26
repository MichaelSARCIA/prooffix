# MASTER PROMPT: run phase by phase (no Orchestrator mode in this build)

Project title: "ProofFix: Prove, Fix, Coach with IBM Bob"

Build "Review → Repro → Fix → Coach": an agentic code-quality loop on a small Python app.
Follow AGENTS.md and .bob/rules. Before each phase below, switch the mode dropdown yourself to the mode named in that phase's heading, then paste only that phase's block. Do not paste the whole file at once. After each phase, read its output file yourself before switching modes and moving on. If a step fails twice, stop and fix it manually rather than retrying.

## Phase 0: Scaffold — switch to Agent mode, then paste this block
Create:
- `demo_app/cart.py` (~100 lines, shopping cart: add/remove items, discount codes, totals, CSV export) with exactly 5 seeded bugs:
  1. logic/off-by-one in totals
  2. unhandled edge case (empty cart, qty <= 0)
  3. unsafe input handling (e.g., eval on a discount code)
  4. float arithmetic for money
  5. maintainability (deep nesting, duplicated logic)
- `tests/test_cart.py`: 6-8 passing pytest tests that do NOT expose the bugs.
- `eval/seeded_bugs.json`: id, function, category (scoring only; reviewer must not read it).
Run `pytest -q`; it must pass.

## Phase 1: Review — switch to Reviewer mode, then paste this block
Review `demo_app/` only. Write `out/findings.json`: max 8 items ranked by risk, each `{id, file, line, severity, category, evidence, suggested_test}`. No edits.

## Phase 2: Repro and Fix — switch to Debugger mode, then paste this block
For the top 5 findings, one at a time:
1. Write a failing test in `tests/repro/test_<id>.py`; run only that test (must fail).
2. Apply the smallest patch in `demo_app/`.
3. Run full `pytest -q` (must pass).
Log `out/results.json`: `{id, repro_failed_first, fixed, suite_green}`. After 2 failed attempts, mark unfixed and move on.

## Phase 3: Coach and Report — switch to Coach mode, then paste this block
Write `out/REVIEW.md`: summary table (found / reproduced / fixed), then per finding: risk, proof test, diff summary, 2 sentences on why it happened, 1 sentence on how to avoid it. Score against `eval/seeded_bugs.json`: found, reproduced, fixed, false positives.
Add a "Time saved" line per finding: rough manual time (spot, reproduce, fix, verify by hand) vs. loop time, plus a total. State assumptions in one line; these are estimates, not measurements.

## Phase 4: Submission assets — switch to Agent mode, then paste this block
- `README.md`, starting with the title "ProofFix: Prove, Fix, Coach with IBM Bob" as an H1, then in this order: (1) one paragraph up top on how this enhances developer productivity, using the total time-saved figure from `out/REVIEW.md` plus this stat: developers report spending roughly 5 hours (about 12.5% of a work week) on code review, and about 45% of their time fixing bugs or paying down tech debt rather than building features (source: Codacy developer survey, cite as a footnote link, do not fabricate a different number); (2) "Why this is different" (3-4 lines): most AI review tools stop at suggesting a fix; this loop proves the bug first with a failing test, then verifies the fix against the full suite, before coaching; (3) problem; (4) approach; (5) Bob features used (three custom modes — Reviewer, Debugger, Coach — plus AGENTS.md and rules files guiding every mode); (6) results table with time-saved column; (7) data sources ("self-authored code; no external or personal data"); (8) how to run.
- `DEMO_SCRIPT.md`: 3-minute demo script (mission/hook 15s: "enhances developer productivity" + the time-saved figure, problem 15s incl. the one-line "why this is different" from README, setup 20s, live loop 90s, coaching 20s, results 20s).

Done when: pytest green, `out/REVIEW.md` complete, README written.
