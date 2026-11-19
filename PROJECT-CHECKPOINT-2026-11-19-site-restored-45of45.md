# PROJECT CHECKPOINT — Website restored and verified — 2026-11-19

## Status: WEB UI & STATIC DATA RESTORATION COMPLETE

**Production URL**: https://solieutaichinh.online/  
**Repository**: https://github.com/kiemtimem12345/solieutaichinh (branch `main`)  
**Snapshot source**: original 12,350,261,587-byte gzip TAR archived privately at Hostinger `/home/u154814653/domains/solieutaichinh.online/restore-source/` (do not publish, overwrite or delete).

### Completed and independently confirmed
1. Original dashboard `index.html`, `assets/styles.css`, `assets/app.js` retrieved from original Hostinger full backup, verified against the extracted staged files. This is the original design, not a replacement layout.
2. **41 JSON snapshots** are Git-tracked at `data/`: 32 financial ticker snapshots plus 9 auxiliary data files. They are no longer ephemeral untracked SFTP uploads.
3. Root cause of repeated disappearance: Hostinger `public_html` is an automatically refreshed Git checkout of `kiemtimem12345/solieutaichinh`. Direct SFTP-only uploads outside the repo were being lost on subsequent Git deployments. **Git main is now source of truth.**
4. Fixed app JavaScript to fetch same-origin `data/` first and use the *correct* GitHub repository as fallback, not obsolete `kiemtimem123/so-lieu`. Fixed response parsing for the research library JSON fallback.
5. **Live production HTTP/SHA256 smoke test PASS: 45/45** public URLs (home, index, app.js, styles.css, all 41 JSON) exactly match tracked Git contents. GitHub Actions run `44447941121`, **attempt 3 PASS after final hardening**, 19 Nov 2026.
6. Public HTTP HEAD-only privacy audit **PASS 5/5**: `/.git/config`, `/.git/HEAD`, `/.env` blocked HTTP 403; `/restore-source/` and `/restore-stage-ui-20261119/` return 404. GitHub run `44448772414`. This is a targeted check, not a complete penetration test.
7. GitHub PRs: #35 restored tracked frontend and JSON; #36 fixed live data source and added 45-URL smoke workflow; #37 disabled the old automatic backup scan / SFTP recovery pipelines. `main` after #37: `3470c49c7c5e07eeb2fa99df3fed90072c51b238`. Last CI validation PASS.
8. Workflow `.github/workflows/verify-live-site.yml` verifies all 45 URLs after relevant pushes to `main`; legacy SFTP bootstrap is manual and additionally gated by `LEGACY_SFTP_REPAIR_ALLOW=YES_MANUAL_REPAIR`. Stop using untracked writes into public_html.

### Not done / deliberate exclusions
- Original private `api/analysis-reports.php` (6,714 bytes) is preserved **outside public_html** in `restore-stage-ui-20261119`, not published to public GitHub nor deployed: any DB credentials/config must be audited before enabling a dynamic API. Website currently uses safe public `data/analysis-reports.json` fallback; this snapshot currently has 0 approved reports.
- Financial JSONs are *restored existing snapshots*, not proof that all 32 tickers have complete normalized Q3/2026 reports. Continue ticker-by-ticker validation, especially PLX → GAS → VDS → GEG → IDC.
- Financial project rules remain: quarters beginning 2025-Q1 only; max 20 recent periods; <=0.01% numeric difference acceptable; checkpoint per completed ticker, never revisit accepted periods absent a later contradiction.

### Resume point
Website restore checkpoint complete. Next work: financial BCTC source retrieval and normalization at latest per-ticker checkpoints (PLX Q3/2026 H1-reviewed and parent B03 issue, then GAS/VDS/GEG/IDC). Use Git-tracked `data/financials-*.json` for publishing updates. Preserve original UI, archived source and safety controls.

### Evidence
- https://github.com/kiemtimem12345/solieutaichinh/pull/35
- https://github.com/kiemtimem12345/solieutaichinh/pull/36
- https://github.com/kiemtimem12345/solieutaichinh/pull/37
- https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44447941121
- https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44448772414
