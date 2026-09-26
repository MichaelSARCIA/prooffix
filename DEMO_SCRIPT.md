# ProofFix — 3-Minute Demo Script

*Total runtime: 3 min 00 s. Timings are cumulative from the start of the demo.*

---

## [0:00 – 0:15] Mission / Hook

> "Developers spend roughly 5 hours a week on code review and 45 % of their total time fixing bugs instead of building features. ProofFix cuts that cost by **~32×** — turning a 3 h 45 min manual review-and-fix cycle into a 7-minute agentic loop powered by IBM Bob."

*[keep slides off — talk to the audience directly]*

---

## [0:15 – 0:30] Problem + Why This Is Different

> "Most AI review tools stop at *suggesting* a fix. ProofFix goes further: it **proves** the bug with a failing test, **verifies** the fix with the full suite, and then **coaches** — so every finding arrives with evidence, not opinion."

*[open `demo_app/cart.py` in the editor — show the raw buggy code briefly]*

---

## [0:30 – 0:50] Setup

> "The project is a small Python shopping cart — about 100 lines — with five intentionally seeded bugs covering security, logic, edge cases, money arithmetic, and maintainability. We have a passing test suite that deliberately avoids the bugs. We have three custom Bob modes and an `AGENTS.md` that guides every mode."

*[show the file tree: `demo_app/`, `tests/`, `.bob/`, `AGENTS.md`]*

---

## [0:50 – 2:20] Live Agentic Loop — 90 seconds

### [0:50] Switch to Reviewer mode → paste Phase 1 prompt

> "Reviewer mode is read-only — it can't edit anything. It analyses `demo_app/` and ranks findings by risk."

*[paste the Phase 1 block; watch findings stream in — point out F-01 at the top]*

> "Eight findings, ranked critical to low. F-01: `eval()` on a user-supplied string — arbitrary code execution. F-02: off-by-one in `subtotal()` — the last item is silently excluded from every order total."

### [1:10] Switch to Debugger mode → paste Phase 2 prompt

> "Debugger mode runs the prove-fix-verify loop. Watch: it writes a failing test first."

*[paste Phase 2 block; point to the red test output for F-01]*

> "`eval()` attempted to execute injected code — the test goes red, bug proven. Now the patch: one line, replace `eval` with `DISCOUNT_CODES.get(code)`."

*[point to the green suite output]*

> "Fifteen tests passing. It does this for all five top findings — each one: red test, minimal patch, green suite."

### [1:55] Switch to Coach mode → paste Phase 3 prompt

> "Coach mode writes `out/REVIEW.md` — root cause, prevention advice, and a time-saved estimate per finding."

*[open `out/REVIEW.md`, scroll to the summary table]*

---

## [2:20 – 2:40] Coaching Highlight

> "Here's what makes this useful beyond the fix itself. For the `eval` bug, the coach notes: *'the `# noqa: S307` comment suppressed the only automated warning — the developer silenced the linter and the risk went unnoticed.'* Prevention: *'never pass user strings to `eval`; use a dict lookup.'* One sentence. Actionable. The developer won't make this mistake again."

*[point to the F-01 coaching block in `REVIEW.md`]*

---

## [2:40 – 3:00] Results

> "Five seeded bugs found — 100 % recall. Every one reproduced with a failing test. Every one fixed with the full suite green. 225 minutes of estimated manual work completed in 7 minutes — roughly 32× faster. The loop also caught three additional real issues beyond the seeded set."

*[show the summary table from `REVIEW.md` or `README.md`]*

> "That's ProofFix: Prove, Fix, Coach — with IBM Bob."

---

*End of demo.*
