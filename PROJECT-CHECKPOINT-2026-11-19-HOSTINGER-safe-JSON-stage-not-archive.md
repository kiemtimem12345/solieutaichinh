# CHECKPOINT — Hostinger JSON deployment stale-archive rollback prevention (2026-11-19)

## Confirmed production blocker
- Main financial CI after GEG Q1/2026 PR #70 PASS. Main website verification run `44526085192` **failed twice**, specifically `data/financials-GEG.json` body **86,332 bytes** on production vs **98,635 bytes** in that Git commit, SHA256 mismatch. All other 44/45 assets matched. It was not safe to claim website up-to-date; do not mark full production PASS without a new successful verification.
- Main GEG Q4/2025 original verified later via PR #71 commit `62a0145c6fc0c47fdf902018be1a5c7b6e75caa5`, data CI PASS and 29 exact-VND identities, but website stale JSON needs separate remediation.
- Actual website `https://solieutaichinh.online/`, Hostinger public_html repository checkout, GitHub main canonical source. Avoid deleting remote files or replacing restored HTML/JS/CSS.

## Root deployment-package bug discovered
- Existing workflow `.github/workflows/deploy-hostinger.yml` is **manual workflow_dispatch**, uses `scripts/validate.py`, `scripts/prepare_deploy.py`, `scripts/deploy_ftp.py`. This path is guarded FTPS and uploads 41 JSON without remote deletes.
- Old `scripts/prepare_deploy.py` staged JSON **from immutable `so-lieu-hostinger-restore-2026-11-18-fixed.zip`**, rather than current `data/*.json` in GitHub. If triggered after later issuer corrections, it could **silently roll back GEG/VDS/GAS to original Nov18 archived auto-extracted data**. This package was NOT invoked while unsafe.
- Fixed `scripts/prepare_deploy.py` now verifies immutable ZIP integrity as provenance ONLY, then stages precisely 41 current Git `data/*.json` (32 finance + 9 support), checks ticker, period cutoff >=2025Q1/max20, and copies original bytes **unchanged**. Staged SHA256 for each of 41 must equal tracked Git source SHA, not just parse as JSON.
- Added `scripts/verify_deploy_stage.py` gate checking all 41 source and staged bytes, up-to-date issuer-verified VDS 7/7 and GEG Q4+Q1+Q2, no archive rollback.
- `.github/workflows/validate.yml` automatically executes staging verification after deployment preparation on every PR/main push. The existing manual FTPS deploy now sources the **correct current Git data** if run through the guarded workflow; still requires proper production FTPS secrets and runtime authorization.
- Do **NOT** enable automatic FTPS deploy without confirming Hostinger checkout integration; uploading to a Git checkout may be overwritten by a later Git pull. The staging correction alone is safe, but does not itself update Hostinger. A successful 45/45 public-site smoke after an authorized safe synchronization is necessary.
- Do not expose credentials or write FTP secret values to GitHub files/checkpoints. CNAME marker verification and FTPS TLS cert checks preserved.

## Resume / next
1. Merge this PR only if CI PASS. Check website run after merge; if still 44/45 (GEG JSON stale), use a safe Hostinger Git-pull/deploy path or explicitly guarded FTPS update of current Git JSON (do not use old ZIP) via authorized production workflow. The available GitHub connector does not directly trigger workflow_dispatch, so avoid claiming the remote deployment has run.
2. Resume **GEG 2025-Q3 original consolidated signed B01/B02/9M B03**, then derive stand-alone Q4 12M–9M. Next GEG 2025Q2 H1→2025Q1 and find official audited 2025 notes explaining the 11,422,218,903 VND cash-equivalents-only initial comparative difference.
3. VDS 7/7 verified, preserve; GEG Q3/2026 both scopes PASS; IDC Q3/2026 after GEG historically complete.
4. Confirm no user secrets or files in public_hostinger. Keep GitHub main source of truth; no reprocessing accepted periods.
