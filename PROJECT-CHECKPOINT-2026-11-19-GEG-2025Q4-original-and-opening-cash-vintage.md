# CHECKPOINT — GEG hợp nhất Q4/2025 từ PDF gốc và đối chiếu tiền đầu năm 2026 (19/11/2026)

## Resume pointer
- VDS consolidated 2025Q1–2026Q3: **7/7 periods original PASS**, PR #66; preserve finished rows.
- GEG 2026Q3 (parent & consolidated) previously PASS; GEG 2026Q1 original 90 fields / 23 identities PASS PR #70 commit `f88af1866355923da8de40d4e9ba65125d7f7dcf`; GEG 2026Q2 original 101 fields / 31 identities PASS PR #69. Do not reprocess these.
- GEG original 2025Q1–Q4 still auto `pending_visual_review` before this update. Next is 2025Q4 original signed consolidated source; thereafter 2025Q3→Q1 original in that order.

## Public signed GEG original 2025Q4
- Source original PDF `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/GEG_Baocaotaichinh_Q4_2025_Hopnhat.pdf` (84 PDF pages); issuer signature 26 January 2026, public disclosure 29 January 2026; visually inspected signed pages **p6 balance sheet assets**, **p7 liabilities/equity**, **p8 separate Q4 and 12M income**, **p9 and p10 annual 12M cash flow** using original page screenshots. Signed parent+consolidated layouts separated; all extracted numbers from consolidated B01/B02/B03.
- PDF source fetch in external container failed, but public PDF screenshot explicitly verified: SHA256 remains **unknown** and must not be invented, `pdf_sha256=not_yet_computed_retain_source_url`; original URL and page index retained. All exact accounting identities verified directly against screenshots, not unverified OCR.
- Source VND. JSON `triệu VND`, EPS VND/share, cumulative FY and Q4 quarter separate.

## Original issuer 2025Q4 figures (VND)
- **B01 end 2025:** assets `15.110.888.031.702`; liabilities `8.613.176.165.875`; equity `6.497.711.865.827`; parent equity `4.964.645.836.433`, noncontrolling equity `1.533.066.029.394`.
- **B01 end cash** `86.364.663.248`; cash `46.702.358.323`, equivalents `39.662.304.925`. Compare original 2026Q1 opening B03 cash `86.364.663.248` **exact match**.
- **B02 standalone Q4/Năm nay**: revenue `590.444.253.989`, COGS `297.744.769.538`, gross `292.699.484.451`, PBT `90.552.211.754`, tax cost **negative `-5.502.853.068`**, consolidated net **`96.055.064.822`**, parent net `83.445.048.823`, NCI net `12.610.015.999`. EPS basic 111, diluted 570 (reported distinct, preserve issuer column).
- **B02 FY 2025/12M**: revenue `2.998.867.342.581`, PBT `978.664.595.389`, net `946.778.853.120`, parent net `702.152.457.423` VND.
- **B03 FY 2025/12M**, NOT standalone Q4: CFO **`932.884.327.033`**, CFI **`1.921.143.888`**, CFF **`-1.012.240.268.026`**, net cash change `-77.434.797.105`, starting `163.717.707.072`, FX `81.753.281`, ending `86.364.663.248` VND. Exact B01/B03 cash bridge residual 0. FY capex `-408.566.559.815`, dividends paid `-76.830.949.700`.
- **96 source fields**, **29 independent exact-VND B01/B02/FY B03 accounting identities all residual 0**. Record 2025Q4 `verification_status=issuer_signed_original_visual_verified_B01_B02_B03_FY_ytd_Q4_standalone_cash_deferred`. Do not fill Q4 standalone CFO/CFI/CFF until 2025Q3 9M report is independently visually verified.

## Critical restatement/localization of 2026 opening cash
- Original **2025Q4 31/12 cash = 86.364.663.248**, same as independently signed original **2026Q1 opening cash 86.364.663.248**, so Q4 2025→Q1 2026 vintage is **internally continuous**.
- 2026Q2 signed H1 report uses **74.942.444.345** and 2026Q3 repeats same comparative, both difference **-11.422.218.903 VND** from original 2025Q4/Q1 vintage. 2026Q2 B03 standalone cash cannot bridge when subtracting Q1 3M, so Q2 standalone cash remains NULL with source-vintage exception. All original FY/quarter standalone source figures preserved.
- 2026Q2 note states its B01 comparative is 2025/12/31 **audited**. This is a strong hypothesis that restatement/comparative version changed, but exact audited B01/B03 and item-5 cash note **still require original audited FY2025 or H1 reviewed PDF verification**. Do not call it proven reclassification until those sources are visually reconciled.
- The 11.422bn difference cannot be silently forced into Q2 operating/investing/financing flows. No ticker completion claim until all 2025 periods and this cross-vintage issue addressed as far as source permits.

## Changed files / CI
- `data/financials-GEG.json` 2025-Q4 only, originally unverified auto snapshot overwritten by verified source; pre-change values archived under `financial_line_items_prior_values` / `financial_line_items_rejected_values`. Previously verified 2026 records left unchanged.
- `scripts/verify_geg_q4_2025_original.py`: independent 29 exact-VND identities + original source figure fixtures, Q1 opening equality, Q2 comparative exception, no fabricated standalone Q4 cash.
- `.github/workflows/validate.yml` adds regression gate. PR acceptance only after CI green and 45/45 site smoke after merge.

## Website deployment alert
- At base commit `f88af186`, GitHub main **financial CI PASS**, but read-only public site smoke run `44526085192` failed twice on `data/financials-GEG.json` hash mismatch (site served **86.332 bytes** vs main **98.635 bytes**), all other 44/45 checks passed. This is a **real website deployment lag/stale GEG JSON issue**, not a financial-logic failure.
- Fix/check remote deployment separately; do NOT claim 45/45 production success until a new verified live-site job reports PASS. Hostinger public_html is a Git checkout; avoid hand-written SFTP asset deletion. `.github/workflows/deploy-hostinger.yml` and `deploy-sftp.yml` are manual guarded deployments only.

## Next
1. CI & PR, merge only green; investigate stale Hostinger GEG JSON, sync safe trusted Git-derived data without deleting public assets, verify 45/45 SHA.
2. Validate GEG signed **2025Q3 9M B03 original**, then compute standalone 2025Q4 CFO/CFI/CFF from FY 12M minus original 9M. Then GEG 2025Q2 H1 → 2025Q1.
3. Inspect official FY2025 audited (HOSE 30 March 2026) and H1 2026 reviewed (HOSE 25 August 2026) original PDFs. Determine where initial 11.422bn cash comparative was revised; preserve both source vintages.
4. Once GEG complete/blocked with source-specific explanation, move IDC Q3/2026. Independent prior exceptions: PLX parent Q3/2026 CFF difference 87.654.015.000 VND; GAS H1/2026 COGS 10.160.150.278 VND not allocated.
5. All periods >=2025Q1, <=20 periods/ticker; tolerance <=0.01%; signed issuer sources and exact-VND accounting checks; durable checkpoints and no reprocessing completed periods.
