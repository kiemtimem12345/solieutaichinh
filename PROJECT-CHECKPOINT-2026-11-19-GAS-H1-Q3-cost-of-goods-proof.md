# CHECKPOINT — GAS H1/2026 bridge from Q3 nine-month original, 19/11/2026

## Exact resume pointer
- Main last checkpoint before this investigation: `PROJECT-CHECKPOINT-2026-11-19-GAS-audited-2025-B03-cross-vintage.md` commit `4ae47d249e1e96b256aad6135be0a681b2270f79`.
- Follow existing issuer-visual completed GAS consolidated records 2025Q1–2026Q2, and GAS 2026Q3 both parent/consolidated PASS. No reprocessing of accepted quarters.
- Earlier PR #56 and website 45/45 PASS; audited 2025 and reviewed H1/2026 financial statement versions stored separately in `source_validation`.

## New evidence, direct Q3/2026 original B02
- GAS consolidated Q3 original PV GAS: https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14699&documentid=3432&moduleid=648&portalid=0 .
- Public PDF mirror independently visually inspected on 19/11: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/GAS_Baocaotaichinh_Q3_2026_Hopnhat.pdf ; PDF page 5, B02 consolidated columns Quý III Năm nay / Lũy kế Năm nay.
- GAS Q1 original B02 PDF page 6; Q2 original B02 PDF page 5, both visually reviewed in previous PR #52. Reviewed H1 2026 original PR #54.

| B02 chỉ tiêu | Q3 9M lũy kế (VND) | Riêng Q3 (VND) | Hiệu = H1/2026 (VND) |
|---|---:|---:|---:|
| Doanh thu thuần | 120.977.138.230.990 | 39.708.393.248.033 | 81.268.744.982.957 |
| Giá vốn hàng bán | 102.456.747.387.133 | 33.489.588.538.355 | 68.967.158.848.778 |
| Lợi nhuận gộp | 18.520.390.843.857 | 6.218.804.709.678 | 12.301.586.134.179 |
| LNTT | 16.980.511.052.183 | 5.772.611.091.561 | 11.207.899.960.622 |
| LNST | 13.594.648.848.851 | 4.568.974.088.511 | 9.025.674.760.340 |
| LNST cổ đông mẹ | 13.381.162.041.937 | 4.576.462.445.604 | 8.804.699.596.333 |
| LNST cổ đông không kiểm soát | 213.486.806.914 | -7.488.357.093 | 220.975.164.007 |
| Thuế TNDN hiện hành | 3.391.122.703.113 | 1.201.321.393.743 | 2.189.801.309.370 |
| Thuế TNDN hoãn lại | -5.260.499.781 | 2.315.609.307 | -7.576.109.088 |

- All nine Q3-nine-month-minus-Q3 comparisons equal published original H1 as well as later reviewed H1, with only a **1 VND** cross-report difference in parent-attributable vs noncontrolling-profit split that cancels in consolidated LNST; below project tolerance 0.01%.
- GAS original Q1 B02 COGS **33.511.417.706.493**, Q2 original standalone B02 COGS **35.465.901.292.563**, sum **68.977.318.999.056**, while original Q2 H1/YTD and corroborating Q3 9M-minus-Q3 COGS **68.967.158.848.778**: difference **-10.160.150.278** VND.
- Resulting H1 gross, PBT, net profit and parent-attributable net profit are each **+10.160.150.278 VND** above original Q1+Q2 reported individual-quarter sums; revenue, current and deferred income-tax sums, noncontrolling profit match H1 exactly.
- This localizes the issue to a **Q1/Q2 standalone column versus H1 YTD cost-of-goods inconsistency**, not PDF parsing, currency-unit conversion, or later Q3 restatement. Reconciliation still cannot authoritatively assign the difference to Q1 or Q2.
- If Q1 remains unchanged, purely algebraic (NOT issuer-confirmed) implied Q2 COGS would be **35.455.741.142.285** and implied Q2 PBT **7.453.216.304.771** VND; these are NOT published as corrected Q2. Do not substitute into quarterly canonical data without issuer confirmation.
- Q3 B02 source original already PASS; **no modification to any Q3 core financials**.

## Changes in PR
- `data/financials-GAS.json` 2026Q2 `source_validation.reviewed_h1_version_comparison.q3_source_nine_month_consistency`: detailed exact-VND original, H1, Q3 nine-month and Q3 standalone cross-comparison for nine fields, derived hypothetical Q2 marked as **noncanonical**.
- `scripts/verify_gas_2026_h1_q3_bridge.py` asserts exact original source data and 9 source identities, plus 1 VND parent/NCI offset, and prevents overwriting original Q1/Q2.
- `.github/workflows/validate.yml` new gate. Run CI before merge and production site 45/45 when merged.

## Remaining / next actions
1. Verify CI and PR, merge only PASS; keep authoritative H1 confirmed and quarter allocation flagged, not silently corrected.
2. Search for official corrected Q1 or Q2 standalone 2026 B02 or issuer note explicitly identifying 10,160,150,278 VND; if none is found, leave the discrepancy open (do not block progress on all other tickers).
3. After GAS cross-vintage issue is documented and controlled, move to VDS Q3/2026, then GEG unverified gaps, IDC Q3/2026. Do not redo GEG Q3/2026 already PASS.
4. PLX Q3/2026 parent B03 87,654,015,000 VND remains independently blocked.
