# CHECKPOINT — IDC 2026 Q2 consolidated issuer PDF + Q3 exact standalone cash (19 Nov 2026)

## Starting commit and non-reprocessing
- Earlier IDC Q3 original issuer report PR #76 merged into main `93516a72158dfec121a9df8429eea39234a14790`. Production main financial CI `44542770740` PASS and 45/45 live-site URL+SHA256 smoke `44542770760` PASS.
- IDC 2026Q3 *original B01/B02/9M B03* were already verified, 105 source fields and 29 exact-VND identities; **do not reload** them. This checkpoint only adds quarterly Q3 cashflow by verifying Q2/2026 H1, and fills IDC Q2 original source.
- VDS 7/7 consolidated quarters and GEG 7/7 source verified; don't redo them. IDC 2025Q1–2026Q1 remained unverified/partially verified and must be handled from issuer originals separately.

## Signed issuer original IDC Q2/2026
- Original HNX consolidated Q2 2026 filing (31 July 2026): https://www.hnx.vn/vi-vn/cophieu-etfs/chi-tiet-chung-khoan-ny-IDC.html?_des_tab=1
- Public Vietstock source index original ZIP: https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%202/IDC_Baocaotaichinh_Q2_2026_Hopnhat.zip?ver=fec9e0e5
- ZIP byte SHA256 `5e5637e71fa303a7968f306b645e95fa391b633126a4aff83fcabeeb412220c6`, bytes 29,274,705.
- Original Vietnamese **consolidated** signed issuer PDF `3_idc_2026_7_31_cc5f147_vi_baocaotaichinhhn_q2_2026_s.pdf` inside ZIP: 67 pages, SHA256 `f0bee9c4554b166380098034650b09c0e45f85da55fd016086f0ef08a596354c`, 16,931,131 bytes, signed 30 July 2026.
- Source images visually checked: B01-DN/HN PDF pages 8–11, B02-DN/HN page 12, B03-DN/HN pages 13–14 via read-only GitHub Actions visual renderer `44542982923`. Source VND, normalize million VND in JSON (EPS VND/share).
- The old Q2 financial snapshot had rounded core values in millions and precomputed ROA/ROE from unverified average balances, plus wrong/empty cashflow detail. Replaced only after primary source visual QA and quarantined old values. ROA and ROE now null pending independently validated denominators.

## Q2 standalone B01/B02 (VND)
| Original item | Q2 2026 original VND |
|---|---:|
| B01 assets 30 June | 23,546,025,947,580 |
| B01 liabilities | 14,715,877,209,906 |
| B01 equity | 8,830,148,737,674 |
| B01 cash and equivalents | 608,684,579,632 |
| B02 standalone Q2 net revenue | 2,270,489,379,557 |
| B02 standalone Q2 pretax profit | 832,935,368,526 |
| B02 standalone Q2 consolidated net profit | 663,333,806,279 |
| B02 standalone Q2 parent net | 609,810,412,292 |
| B02 standalone Q2 NCI net | 53,523,393,987 |
| B02 standalone Q2 EPS | 1,461 VND/share |
- YTD/6M B02 separately retained: revenue **3,756,014,019,978**, pretax **1,253,232,495,504**, consolidated net **1,001,240,987,338**, parent net **880,406,329,931** VND. YTD EPS 2,109 VND/share.
- 105 issuer source numeric fields including full detailed original B03; **29 exact accounting identities across B01, B02 quarters/YTD, B03 H1 YTD** residual zero.

## B03 original H1/2026; Q3 standalone derivation
| B03 (VND) | H1 2026 six-month | Q3 2026 nine-month | Q3 standalone = 9M−6M |
|---|---:|---:|---:|
| CFO | **-5,019,037,910** | +211,600,221,432 | **+216,619,259,342** |
| CFI | +412,225,133,057 | +505,984,662,907 | **+93,759,529,850** |
| CFF | -352,471,108,238 | -801,577,203,462 | **-449,106,095,224** |
| Net cash change | +54,734,986,909 | -83,992,319,123 | **-138,727,306,032** |
| FX | +6,117,592 | -17,137,387 | **-23,254,979** |
| Ending cash | 608,684,579,632 | 469,934,018,621 | Q3 start 608,684,579,632, end 469,934,018,621 |
- **Exact Q3 bridge:** 608,684,579,632 − 138,727,306,032 − 23,254,979 = 469,934,018,621 VND. The CFO+CFI+CFF quarterly sum and B01 corporate cash reconciles, residual 0.
- Q3 original source 9M B03 dividend paid -710,532,693,375 less H1 dividend paid -74,115,054,425 = **-636,417,638,950 VND** Q3 standalone dividends.
- Q3 capex 9M -357,115,441,830 less H1 -158,418,483,835 = **-198,696,957,995 VND**.
- Q2 B03 **standalone** remains null because IDC Q1/2026 B03 original has not been independently checked. Do not infer it from Q2 cumulative alone.

## Implemented files
- `data/financials-IDC.json` corrects Q2 2026 original B01/B02/H1 B03 to exact-VND source and adds Q3-only CFO/CFI/CFF/net/FX/paid dividends from issuer-verified 9M–6M; Q3 source B01/B02/9M figures untouched. Older periods 2025Q1–2026Q1 untouched.
- `scripts/emit_idc_q2_2026_visual_jpeg.py` and `.github/workflows/visual-idc-q2-2026-pages.yml`: original archive extraction, report SHA256, source screenshots for independent visual QA, read-only.
- `scripts/verify_idc_q2_2026_original.py`: Q2 105 fields, 29 exact-VND source identities and Q3 8 separate quarterly cash fields with 4 exact derivation checks.
- `scripts/verify_idc_q3_2026_original.py` now expects derived Q3 standalone B03 from H1 source and the new 113 fields rather than null quarterly data.
- `.github/workflows/validate.yml` requires the new signed-source regression. Merge only CI PASS, record main SHA and production website 45/45 exact SHA.

## Next priority
1. After merge, verify live site 45/45. Then validate **IDC consolidated 2026Q1 original B03 3M**, derive Q2 standalone CF=H1–Q1, inspect Q1 B01/B02 as well.
2. Continue IDC consolidated 2025Q4 then 2025Q3, Q2, Q1. Do not mark ticker complete before all user-scope periods checked.
3. GEG 2025Q4/2026Q1 source cash comparator -11,422,218,903 VND remains open, GAS H1 2026 B02 COGS 10,160,150,278 VND and PLX parent Q3 2026 B03 87,654,015,000 VND differences remain logged; don't fabricate period adjustments.
4. Keep 2025-Q1 cutoff, max 20 quarters/ticker, source VND to normalized million VND, 0.01% acceptable tolerance, keep parent/consolidated scopes separate and prior auto parser errors for auditability; never overwrite production Hostinger with a stale restore ZIP.
