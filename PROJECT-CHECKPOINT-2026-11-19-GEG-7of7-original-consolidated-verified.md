# CHECKPOINT — GEG consolidated Q1/2025 original and seven-quarter source verification — 19/11/2026

## Resume / completed period rule
- Continue from GEG 2025Q2 issuer original checkpoint `PROJECT-CHECKPOINT-2026-11-19-GEG-2025Q2-original-and-Q3-standalone-cash.md`, PR #74 merge commit `c0cd808d8fb84d7a45863dd49fc78fb50ea522f0`, CI run `44534284905` PASS.
- VDS consolidated 7/7 periods 2025Q1–2026Q3 PASS, no reload; GEG 2025Q2–2026Q2 prior signed-original periods PASS, GEG Q3/2026 both parent and consolidated PASS. **This checkpoint completes source verification of GEG consolidated Q1/2025–Q3/2026, 7/7 periods**, with one separately documented cross-version cash comparator anomaly.
- No source-verified financial period is reprocessed unless a later contradictory primary document is identified. Source unit VND, JSON `triệu VND` except EPS VND/share; >=2025Q1 cutoff, max20.

## GEG consolidated 2025 Q1 issuer original
- Original signed PDF 83 pages: https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/GEG_Baocaotaichinh_Q1_2025_Hopnhat.pdf
- Signed **28/04/2025**, disclosure letter 29/04/2025, consolidated title and B01-DN/HN, B02-DN/HN, B03-DN/HN visually confirmed from 1-based **PDF pages 7–8 (B01), 9 (B02), 10–11 (B03)**. Original report is a scan; only original images and independent VND identities were used, not unverified OCR. SHA256 not calculated; do not invent hash.
- B01 31/03/2025: assets **15,707,017,796,798**, liabilities **9,329,804,140,173**, equity **6,377,213,656,625**; NCI equity **1,567,565,680,628**, parent equity **4,809,647,975,997**. Cash/equivalents **175,400,032,558**, comprising cash 90,585,243,252 and equivalents 84,814,789,306 VND.
- B02 Quý I/Năm nay: revenue **1,112,755,859,981**, cost of goods sold 286,668,495,975, gross profit 826,087,364,006, pretax **605,294,735,430**, tax **-7,651,273,117** (current +30,035,228,409, deferred -37,686,501,526), consolidated after-tax **612,946,008,547**, parent net **378,240,835,561**, NCI net **234,705,172,986** VND; EPS **1056 VND/share**.
- B03 3M YTD = Q1 standalone: CFO **+62,310,535,515**, CFI **+76,527,759,434**, CFF **-127,159,459,528**, net change **+11,678,835,421**, opening cash **163,717,707,072**, FX **+3,490,065**, closing **175,400,032,558** VND. B01 cash = B03 ending exact. Q1 capex **-1,199,715,023**, dividends **-221,374,400** VND.
- 104 original source/standalone fields, **28 exact-VND original B01/B02/B03 and H1-minus-Q2 quarterly B02 checks residual zero**. Q1+original-Q2 revenue, COGS, PBT, net and parent net match H1 lũy kế exactly; no invented averaging or normalization.

## Separate GEG Q2/2025 cash from verified H1 less Q1 original
| Item (VND) | H1 2025 6M | Q1 2025 3M | Q2 standalone |
|---|---:|---:|---:|
| CFO | 555,421,075,993 | 62,310,535,515 | **+493,110,540,478** |
| CFI | +476,067,298,075 | +76,527,759,434 | **+399,539,538,641** |
| CFF | -721,712,954,268 | -127,159,459,528 | **-594,553,494,740** |
| Net change | +309,775,419,800 | +11,678,835,421 | **+298,096,584,379** |
| FX effect | +56,223,158 | +3,490,065 | +52,733,093 |
| Corporate cash beginning Q2 | — | Q1 ending 175,400,032,558 | 175,400,032,558 |
| Corporate cash ending Q2 | 473,549,350,030 | — | 473,549,350,030 |

- Exact Q2 bridge: **175,400,032,558 +298,096,584,379 +52,733,093 = 473,549,350,030 VND**, zero residual. Q2 standalone capex **-15,469,177,804**; dividends **-75,482,900** VND. Same consolidated scope, no quarterly cash inferred from unverified 2024 sources.
- GEG 2025Q2 `verification_status` advanced to `issuer_signed_original_visual_verified_B01_B02_B03_H1_ytd_and_Q2_standalone_cash`. 104 original/derived fields; original B01/B02/H1 B03 untouched. Q3 original 9M and Q4 original FY were already validated, not repeated.

## Durable implementation
- `data/financials-GEG.json` changes **only 2025-Q1** original signed source and **2025-Q2** newly derived standalone cash. Periods 2025Q3 onward unchanged, 2026Q3 two original scopes remain PASS. Bad legacy auto figures archived under `financial_line_items_prior_values` and `financial_line_items_rejected_values`.
- `scripts/verify_geg_q1_2025_original.py` asserts 28 source identities, source URL/signed date, H1 vs quarterly profit consistency and exact 6M minus 3M standalone cash.
- `scripts/verify_geg_q2_2025_original.py` updated from Q2 B03 standalone null to source-derived cash and updated source field count; `.github/workflows/validate.yml` requires new QA gate.
- Merge only **CI PASS**. Post-merge `main` financial CI and production website SHA smoke must be checked separately.

## External deployment blocker, kept explicit
- At original checkpoint before PR merge, GitHub `main` finance CI PASS, but production-site smoke run `44530634005` **44/45**: `data/financials-GEG.json` HTTP body 114,448 bytes versus tracked main 127,582 bytes, SHA mismatch. This is Hostinger stale-checkout/JSON sync, not a statement arithmetic error.
- Staging of 41 JSON was hardened in PR #72 to source GitHub latest, not outdated `so-lieu-hostinger-restore-2026-11-18-fixed.zip`. Guarded FTPS/SFTP deployments remain `workflow_dispatch` with production environment; GitHub connector supports reading Actions but does **not** authorize workflow dispatch or directly access Hostinger. Do not claim production updated merely because GitHub pages and CI PASS. Avoid SFTP deleting or overwriting protected files. Once authorized workflow run is accessible, stage current 41 JSON, deploy without deleting remote files, check 45/45 SHA.
- Original GEG 2025Q4/2026Q1 cash-only initial comparator discrepancy of **11,422,218,903 VND in cash-equivalents** across source vintages still unresolved; preserve issuer source versions in metadata, do not claim comparative harmonization. This does not invalidate independent original quarterly source arithmetic.

## Next action after this GEG period verification
1. Mark GEG **source-verified 7/7 consolidated plus parent Q3**, with cross-vintage cash comparator `open`, no repeat of validated rows. Save final commit/checkpoint.
2. Move to **IDC consolidated Q3/2026** as next ticker in user priority; inspect existing `data/financials-IDC.json` and obtain original issuer/HNX report, then complete B01/B02/B03 from signed source, one ticker/period at a time.
3. Keep PLX Q3/2026 parent B03 CFO/CFF 87,654,015,000 VND anomaly and GAS H1 2026 10,160,150,278 VND cost-of-goods quarter attribution separate, no fabricated fixes.
4. Independently resolve Hostinger site stale GEG JSON using a permitted guarded deployment action, verify production only if 45/45 exact SHA PASS.
