# DAS-1 Agent + Skills Refresh Lessons

- 2026-09-23: **A time-gated check needs a time-driven trigger.** The core and
  all five platform overlay jobs failed from 2026-09-08 to 2026-09-23 because
  the example drills, executed 2026-06-10, crossed the 90-day AEC-05 window.
  Nothing reported it: `conformance.yml` ran only on `push` and
  `pull_request`, and the last push was 2026-08-22. The verifier was correct
  the whole time; the repository was the non-conformant party. (The local
  `*-report.json` artifacts on the maintainer's disk went on saying
  `"pass": true` throughout, but they are gitignored and were untracked in
  `469e80a`, so no clone ever carried a stale claim. The exposure was a red
  gate nobody could see, not published false evidence.) Fixed by adding a
  weekly `schedule` trigger and a separate
  `freshness` job (`tools/check_freshness.py`) that goes red while there is
  still a month of runway, rather than at the moment the evidence is already
  invalid. Generalized rule: if evidence expires on a clock, something that
  runs on a clock must check it.

- 2026-09-23: **Refreshing the fixtures alone leaves the repository failing.**
  `refresh_example_dates.py` re-dates drills and claims but not the generated
  `*-report.json` files, and the claim packets cross-check their disclosed
  drill dates against those reports. Before a refresh the two are consistently
  stale and agree; after one they disagree, and `verify-claims` fails with
  sixteen "Disclosure for D1 does not match referenced report" errors. The
  reports are verifier output, not source, and must be regenerated in the same
  pass. `tools/refresh_and_verify.sh` now encodes that order so it cannot be
  half-done.

- 2026-09-23: **A checker that reads the wrong field reports all-clear
  forever.** The first draft of `check_freshness.py` looked for
  `last_exercise_at` on IR annexes. The real field, and the one
  `verify_ir_annexes` reads, is nested at `tabletop.last_executed_at`. The
  draft found zero annexes and exited green, which is indistinguishable from
  having checked them. Verify a detector against the thing it claims to
  detect, on data known to be in range, before trusting a green result.
