# CHECKPOINT — 2026-11-18 23:35 ICT — SFTP data restored, original UI pending

## Confirmed done (never reprocess without new contradiction)
- SSH/SFTP `195.35.62.53:65002` with account `u154814653` authenticates by SSH password; Hostinger hPanel ED25519 fingerprint pinned in workflows (verification run 44324833181).
- Exact Hostinger path `/home/u154814653/domains/solieutaichinh.online/public_html`. Initial inventory run 44344737929 had no `index.html`, `index.php`, `assets`, `css`, `js`, or `data` directory.
- Restored `public_html/data` containing 41 JSON files (32 financial snapshots, 9 auxiliary). **GitHub Actions run 44347764540: SUCCESS; all 41/41 remote SHA-256 matched**. No HTML, CSS, JS or PHP changes; no existing remote file deleted.
- ZIP source: `so-lieu-hostinger-restore-2026-11-18-fixed.zip`, unchanged. Prep stage filters before 2025-Q1 and caps 20 periods/ticker. These are archived recovery snapshots (10/32 tickers latest Q3/2026; others mainly Q2), NOT a complete Q3 update.
- Separate SFTP check run 44343907023 (attempt 2) PASS: website root and data path accessible. Independent public HTTP test run 44345151319 (attempt 2): `/data/category-data.json` returned **HTTP 200, application/json**. Home `/` remained **HTTP 403**, `/index.html` and `/assets/app.js` HTTP 404.

## Blocker to finish website recovery
- Original UI/index.html/CSS/PHP is missing from both Hostinger `public_html` and repository/Library recovery ZIPs. GitHub history from initial uploads never had HTML/CSS. Do not rebuild a different-looking UI or invent source.
- User should obtain Hostinger **Files backup** dated before the interface disappeared (Websites → Dashboard → Backups → Restore and Download → Files backups → Download files). **Do not click whole-site Restore**, which can overwrite recovered JSON and other files. If the user uploads archive, inspect exact files and deploy only missing original frontend assets without touching current data.
- Read-only Hostinger backup candidate scan run 44345738658 found no obvious backup folders (one entry under domain `.builds`, not proven a valid frontend backup).

## Future automation
- Existing `deploy-sftp.yml` is MANUAL and guarded by `SFTP_DEPLOY_ENABLED=YES_AFTER_UI_RESTORE` (not enabled). It still uses sshpass and should be upgraded to verified Paramiko before routine deployment; no automatic overwrite of production data without backup/versioning.
- Next: restore original frontend → verify homepage 200, assets and per-ticker JSON → resume financial validation/checkpoints. Respect <=0.01% tolerance and ticker-by-ticker workflow.

## Evidence
- https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44347764540
- https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44343907023
- https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44345151319
- https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44344737929
