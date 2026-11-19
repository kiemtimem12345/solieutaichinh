# CHECKPOINT — VDS Q1–Q2/2025 issuer originals and 2025 Q2/Q3 standalone cash — 19/11/2026

## Resume chain
- Previous durable checkpoint: `PROJECT-CHECKPOINT-2026-11-19-VDS-2025Q3-original-and-Q4-cash-bridge.md`. Main prior to this branch `280eb115da1f8c2c2c7ede5a5087108eea511a63`, PR #65 Q3/2025 original B01/B02/B03 9M and Q4/2025 standalone B03 merged; main financial CI PASS; site SHA256 45/45 PASS.
- Already verified VDS Q3/Q4 2025, Q1/Q2/Q3 2026. The remaining Q1/Q2 2025 historical auto records have now been visually verified and replaced. Don't reprocess earlier completed periods.
- Only in-scope 2025-Q1 through latest Q3/2026, seven periods, 20-period limit intact. Company consolidated scope and VND source. Customer brokerage money is off company B01.

## Original official VDS issuer sources and proof
- Q1/2025 issuer public announcement: https://www.vdsc.com.vn/quan-he-co-dong/cong-bo-thong-tin/rong-viet-cong-bo-bao-cao-tai-chinh-hop-nhat-quy-1-2025-va-giai-trinh-chenh-lech-loi-nhuan-i880
- Q1 PDF signed 28/04/2025, original 48 pages: https://www.vdsc.com.vn/data/api/app/file-storage/a25b294e-079e-495b-8ca7-08dd86f386db/VDSC_Cong%20bo%20BCTC%20HN%20Quy%201%20nam%202025.pdf?downloadFrom=ManagementDocument-880
  - SHA256 `632be5538c0b2b29c975f311388a2b33e97046e0cafc6a609e78b786771fbc86`, bytes 10,068,095. GitHub Actions original PDF renderer `44515175266` PASS; artifact `14524592497` original page images. B01 PDF pp6–8, B02 pp11–13, B03 pp14–17 visually checked.
- Q2/2025 issuer public announcement: https://www.vdsc.com.vn/quan-he-co-dong/cong-bo-thong-tin/rong-viet-cong-bo-bao-cao-tai-chinh-hop-nhat-quy-2-2025-va-giai-trinh-chenh-lech-loi-nhuan-i912
- Q2 PDF signed 30/07/2025, original 50 pages: https://www.vdsc.com.vn/data/api/app/file-storage/e3e3cf34-e344-47e1-b7f1-08ddcef672b6/VDSC_Cong%20bo%20BCTC%20HN%20Quy%202%20nam%202025%20va%20Giai%20trinh%20chenh%20lech%20loi%20nhuan.pdf?downloadFrom=ManagementDocument-912
  - SHA256 `48934ed3df3d6b47271c563448fc908ecf68533a990dd205397f87dd78525a36`, bytes 10,126,141. Original PDF GitHub Actions renderer `44514831020` PASS; artifact `14524867063` original page images. B01 PDF pp7–9, B02 pp12–14, B03 pp15–18 visually checked.
- Tool renderer `scripts/inspect_vds_q1_2025_pdf.py` and `scripts/inspect_vds_q2_2025_pdf.py` run ephemeral, public original-only, no production writes. OCR helper never treated as authoritative without visual review.

## Issuer primary numbers
| Consolidated VDS | Q1/2025 standalone VND | Q2/2025 standalone VND |
|---|---:|---:|
| B01 total assets at period end | 6,348,196,110,824 | 6,856,334,146,952 |
| B01 total liabilities | 3,502,234,864,743 | 4,022,130,711,905 |
| B01 equity | 2,845,961,246,081 | 2,834,203,435,047 |
| B01 corporate cash | 663,750,989,889 | 1,289,345,078,324 |
| CTCK B02 total operating revenue (not just FVTPL) | 168,952,311,087 | 180,998,605,171 |
| B02 operating expenses | 112,661,705,215 | 160,666,996,283 |
| B02 PBT | 22,643,851,018 | -17,442,687,286 |
| B02 consolidated net after tax | 19,012,342,256 | -11,193,905,667 |
| B02 parent-attributable net | 19,089,097,924 | -9,900,252,664 |
| B02 EPS VND/share | 79 | -41 |

- Original Q1 B01/B02/B03: **120 fields**, 27 independent exact-VND identities all zero.
- Original Q2 B01/B02/H1 B03: **120 fields** including 7 verified derived Q2 cash fields, 30 independent exact-VND source identities all zero.
- Old auto-extracted wrong figures preserved in `financial_line_items_prior_values` and `financial_line_items_rejected_values`; original issuer URLs and SHA256 saved in `source_validation`.
- The company B01 cash is **not** the customer brokerage deposit `1,727,897,394,701` VND Q1 and `1,944,403,214,851` VND H1. Separate client fields validated.

## B03 source lũy kế → quarterly independently derived
| VDS cashflow VND | Original Q1 3M | Original H1 6M | Q2 standalone = H1−Q1 |
|---|---:|---:|---:|
| CFO | -553,201,398,548 | 423,813,880,703 | **+977,015,279,251** |
| CFI | +78,014,969,203 | -766,006,221,613 | **-844,021,190,816** |
| CFF | -68,200,000,000 | +424,400,000,000 | **+492,600,000,000** |
| Net cash change | -543,386,429,345 | +82,207,659,090 | **+625,594,088,435** |
| Cash ending period | 663,750,989,889 | 1,289,345,078,324 | same |

- Q2 opening cash 663,750,989,889 + 625,594,088,435 net = Q2 ending 1,289,345,078,324; quarterly cash component sum exactly equals net, capex Q2 -4,086,102,431 VND.
- Q3 standalone B03 re-derived (original 9M Q3 minus original 6M Q2), exact at VND:
  - CFO **-1,214,198,760,707**, CFI **-98,906,047,822**, CFF **+612,012,000,000**, net **-701,092,808,529**; Q3 begins 1,289,345,078,324, ends 588,252,269,795. Capex Q3 -1,698,866,634 VND.
- Q4 FY-minus-9M cash already verified in previous PR #65; no changes. All VDS seven consolidated B01 B02 B03 periods now have source-verification flags and standalone quarter cash values. Cross-period note below remains open.

## Noncanonical cross-period source-vintage differences, do not force values
- Q1+Q2 B02 standalone securities revenue 349,950,916,258 vs H1 report 349,950,141,337 VND: **-774,921 VND**, exactly mirrored by H1 operating expenses (same -774,921); PBT and consolidated net **match exactly**. This discrepancy is far below 0.01% project tolerance but provenance still retained.
- H1 parent profit attribution 8,071,151,977 VND vs Q1+Q2 separate issuer parent profit 9,188,845,260 VND, **-1,117,693,283 VND**; H1 NCI allocation has equal opposite +1,117,693,283; consolidated total net unchanged. **Significant split attribution difference remains unresolved**, do not attribute it to a specific quarter without issuer note or corrective announcement; keep warning.
- Q3 9M-minus-Q3 standalone B02 securities revenue is 26,645,133 VND below H1 as originally published, ~0.0076%, within project tolerance, offsetting expense presentation. Q3 year-to-date PBT and net match H1+Q3 standalone exactly.
- GAS separate 2026H1 COGS cross-vintage 10,160,150,278 VND and PLX parent 2026Q3 B03 financing 87,654,015,000 VND remain documented independent blockers.

## Tests, merge, deployment
- `data/financials-VDS.json`: Q1 and Q2 source originals and Q3 standalone cash only; prior completed Q4 2025 and all 2026 periods unchanged.
- `scripts/verify_vds_q1q2_2025_source.py` independent 27 + 30 source B01/B02/B03 exact-VND identities and Q2/Q3 cash, checks historical bad parser and 2025 H1 source-vintage notes.
- `scripts/verify_vds_q3_2025_source.py` updated to require source-derived standalone 2025 Q3 corporate cash flows from signed H1 original, not null and not old auto parse.
- `.github/workflows/validate.yml` runs the new regression; merge PR only after PASS, verify production 45/45 HTTPS SHA256 and record merged main commit.
- After merge ticker VDS has source-verified **7/7 consolidated quarter rows** (Q1/2025–Q3/2026), but do not mark ticker fully harmonized until the significant 2025H1 parent/NCI split source-vintage discrepancy has a defensible resolution or explicit documented exception.
- Next in scope: finish VDS classification exception investigation; then GEG historical gaps (do not redo completed GEG Q3 2026), then IDC Q3 2026. Maintain one ticker at a time, source originals and checkpoints, <0.01% tolerance.

## CI / production after PR #66
- PR #66 merged into `main` as `0423fb7323a461e9c01a16574c8153cbda97f817`.
- GitHub Actions financial validation `44518130016` PR PASS; main financial validation `44518227512` PASS.
- Production read-only smoke run `44518228001` PASS, confirmed log `45/45 HTTPS URLs serve exact tracked Git content (SHA256)`.
- All 7 VDS consolidated quarter rows have issuer-source B01/B02/B03 verified. **Exception**: 2025 H1 parent/NCI attribution difference of 1,117,693,283 VND remains open; source report cumulative and standalone columns both internally balance. Keep `verified_originals_with_documented_cross_period_exception`, not `fully_harmonized`.
- Additional research now targets official VDS H1/2025 **reviewed consolidated report**, 13/08/2025, published at https://www.vdsc.com.vn/quan-he-co-dong/cong-bo-thong-tin/rong-viet-cong-bo-bao-cao-tai-chinh-rieng-bao-cao-tai-chinh-hop-nhat-va-bao-cao-ty-le-attc-ban-nien-2025-da-duoc-soat-xet-i921 . Original issuer PDF: https://www.vdsc.com.vn/data/api/app/file-storage/6d34c594-a07c-4fc9-88a1-08ddd9f82764/VDSC_Cong%20bo%20BCTC%20hop%20nhat%20ban%20nien%202025%20da%20soat%20xet.pdf?downloadFrom=ManagementDocument-921 . Original scanned PDF 84 pages; visual-review tool PDF screenshot endpoint timed out, so use bounded GitHub Actions original source renderer rather than make accounting adjustments from OCR.
