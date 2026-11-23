# SOP: Rerun financial snapshot CI without a data or dummy commit (2026-11-23)

## Scope and checkpoint
Repository: `kiemtimem12345/solieutaichinh`, default branch `main`.
Primary suite: `.github/workflows/validate.yml` — `Validate financial snapshots`.
First independent rerun after the 2026-11-22 VCB Q3 consolidation checkpoint:
- Source commit: `d0f4aedc311f38d02c9a8d89b794bc7d98e96a2c`
- Run: https://github.com/kiemtimem12345/solieutaichinh/actions/runs/45034776611
- Existing job: `validate` / `137245974172`
- New attempt: **2**; new job ID: `137581807722`
- Result confirmed 2026-11-23: **completed / success**, 93/93 successful job steps, 0 failures.

This checkpoint certifies the checked-out repository's automated tests on that SHA; it **does not by itself** prove current live Hostinger files match Git, nor does it mean every source document was downloaded anew or every accounting exception was resolved.

## Repeatable execution sequence
1. Fetch repository metadata and current `main` commit SHA. Read `.github/workflows/validate.yml` to determine the actual gate; do not infer CI status from old commit messages.
2. Query `GET /repos/kiemtimem12345/solieutaichinh/actions/runs?per_page=10`, filter on `path=.github/workflows/validate.yml`, `head_branch=main`, and the **same SHA**. Inspect `status`, `conclusion`, and `run_attempt`. The commit-associated workflow-runs helper may return zero runs because it only enumerates PR-triggered runs; an empty traditional commit-status list is also not proof of missing CI.
3. Fetch jobs for the chosen run; identify the real `validate` job ID. Request **rerun of that job**, including if it previously passed, using the GitHub Actions rerun-job operation. This creates a new attempt without changing data and without committing a synthetic file. Confirm the response is successful, then confirm `run_attempt` increased.
4. Poll the run and latest-attempt job (not the old job ID). A rerun request alone is **not** a passing test. Require `status=completed`, `conclusion=success`, and verify there are no failed or cancelled steps. For failures, read the current job's steps/logs, identify the first failing source test and the scope of the failure.
5. Classify failures:
   - Syntax, JSON shape, missing files, stale test/schema: fix the smallest root cause on a separate branch; add a regression check; open PR and require green CI.
   - Regulatory-source access/PDF timeout: bounded retries and a documented alternate official issuer or exchange source; no fabricated PDF hash or values. Archive the blocker in the private exception queue.
   - Accounting mismatch: compare signed B01/B02/B03 and same-scope, same-vintage FY/H1/9M periods; use exact VND/units/signs and original source. Do not plug balancing numbers or replace signed originals to force PASS.
   - Quarantined accepted-vintage cases (e.g., GEG/IDC/PLX): preserve fail-closed source and publishing guards; resume only when new documentary evidence changes the decision.
6. After confirmed green CI, record the commit, run URL, attempt, latest job ID, pass/fail count, accounting coverage and outstanding nonblocking exception policy in a durable checkpoint. Move to the next unfinished ticker/period; never rerun previously accepted source extraction unless contradictory new evidence is found.
7. Independently validate the public site when publishing changes, using `scripts/verify_live_site.py` / the manual `Verify restored production website and 41 JSON (read-only)` workflow. The standard validation CI does not establish live deployment success.

## Safety and deployment
- Financial scope: 2025-Q1 through 2026-Q3, latest 20 distinct periods maximum; preserve different report scopes; `triệu VND` conversion and negative operating/investing/financing cash signs; no 2024 reintroduction.
- A documented, acceptable source-vintage difference is distinct from a mathematically verified zero difference. Preserve the latest user-approved tolerance only where cross-source evidence supports it, without changing original printed figures.
- The exception queue is internal; show missing tickers or periods only when the user asks.
- Hostinger FTPS/SFTP deployment workflows are **manual workflow_dispatch**; rerunning `validate` is read-only and does not deploy. Never auto-deploy from an exception or a failed gate.
- If GitHub Actions write permissions disappear, do not claim tests executed; use a PR-triggered CI run on a meaningful code/test change, or report the permission blocker.

## Evidence of successful new method
At 2026-11-23 the Actions rerun-job operation returned success, the run changed to attempt 2 / in_progress, and its latest job later finished success with **93 successful steps and no failed or skipped steps**. This procedure replaces the earlier incorrect inference that zero PR-associated runs meant no main CI was available.
