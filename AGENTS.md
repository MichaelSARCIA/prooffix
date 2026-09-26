# Project: ProofFix — Prove, Fix, Coach with IBM Bob

Agentic code-quality loop (review → reproduce → fix → coach) demonstrated on a small Python app. Hackathon build, solo, 2 days.

## Layout
- `demo_app/`: code under review (seeded bugs)
- `tests/`: passing suite; `tests/repro/`: one failing-then-passing test per finding
- `eval/seeded_bugs.json`: ground truth for scoring only
- `out/`: findings.json, results.json, REVIEW.md
- `.bob/`: custom modes and rules

## Stack and commands
- Python 3.11+, pytest. No other dependencies.
- Full suite: `pytest -q`. Single test: `pytest -q tests/repro/test_<id>.py`

## Conventions
- Small, targeted patches. Type hints and short docstrings on public functions.
- Money uses `decimal.Decimal`.
- No external data, network calls, or personal data anywhere.
