# CHECKPOINT — VDS 2026-Q2 H1 B03 corrected and consolidated Q3 standalone cash (2026-11-19)

## Starting verified state
- VDS consolidated Q3/2026 issuer original B01/B02/B03 9M restored in `data/financials-VDS.json`, PR #59 merged commit `0b5153a740bd108e88a52cda4e969ac377e5d357`, CI `44501791172` PASS, website `44501791096` 45/45 PASS.
- Q3 original issuer: https://www.vdsc.com.vn/data/api/app/file-storage/0a48e73d-8e80-4aeb-52c9-08df35c2eb9d/VDSC_Cong%20bo%20BCTC%20HN%20Quy%203.2026.pdf?downloadFrom=ManagementDocument-1061 .
- VDS previous Q1/2025–Q2/2026 auto-source records remain unverified. Do not mark VDS wholly PASS until prior quarterly B01/B02/B03 figures independently checked.

## New source, verified original VDS consolidated Q2/2026
- Issuer announcement: https://www.vdsc.com.vn/quan-he-co-dong/cong-bo-thong-tin/rong-viet-cong-bo-bao-cao-tai-chinh-hop-nhat-quy-2-2026-va-giai-trinh-chenh-lech-loi-nhuan-i1034
- Original signed consolidated PDF: https://www.vdsc.com.vn/data/api/app/file-storage/b0d720b4-5481-47f3-a9ad-08deed64b48e/VDSC_Cong_bo_BCTC_HN_Q2.2026.pdf?downloadFrom=ManagementDocument-1034 .
- Visually checked 2026-Q2 B01 cash (PDF page 6) and B03 6M YTD (PDF pages 14–16). This is consolidated *issuer* source, matching 2026-Q3 scope.

| B03 VDS | 6M 2026 YTD (VND) | 9M 2026 YTD (VND) | Q3 stand-alone = 9M-6M (VND) |
|---|---:|---:|---:|
| CFO kinh doanh | -2.620.903.680 | 284.201.617.114 | +286.822.520.794 |
| CFI đầu tư | -90.786.936.920 | -89.200.647.564 | +1.586.289.356 |
| CFF tài chính | -101.950.000.000 | -320.450.000.000 | -218.500.000.000 |
| Dòng tiền thuần | -195.357.840.600 | -125.449.030.450 | +69.908.810.150 |
| Tiền cuối kỳ | 801.617.758.652 | 871.526.568.802 | Q3 mở 801.617.758.652, đóng 871.526.568.802 |

- B03 H1 tiền đầu kỳ: 996.975.599.252 VND (đúng với 9M); H1 ending 801.617.758.652; Q3 ending 871.526.568.802. FX H1 không có số (0); sum/bridge identities exact.
- Q2/2026 earlier unverified auto-parsed `operating_cash_flow_ytd=6677` **triệu VND** was mistakenly copied from B03 pretax profit 6.677.335.807 VND instead of actual CFO **-2.620.903.680 VND**; its `foreign_exchange_effect_ytd=801618` mistakenly copied closing cash, while FX entry is blank/zero. These false historical values are moved into `financial_line_items_prior_values` and `financial_line_items_rejected_values` with explanation.
- Q2 standalone cash flow previously derived from unreliable Q1 is reset null; other Q2 B01/B02 auto-extracted values **still pending visual QA**. Only B03 H1 and B01 cash are currently confirmed, Q2 quarter not marked fully complete.
- Q3 B03 standalone source: 9M original minus H1 original, same consolidated scope; Q3 standalone source-derived `operating_cash_flow=286822.520794` triệu VND, `investing_cash_flow=1586.289356`, `financing_cash_flow=-218500`, `net_cash_change=69908.81015`. Q3 cashflow bridge exact.
- Capex H1 -1.058.807.300 VND, 9M -1.517.717.300, Q3 standalone -458.910.000 VND.
- Client brokerage cash funds remain off-balance and separate from company CFO/B01 cash.

## Test / changes
- Data source `data/financials-VDS.json` modifies only Q2 B03/cash & Q3 standalone B03; older 2025 rows untouched.
- `scripts/verify_vds_q3_2026_source.py` now expects 96 Q3 issuer/derived fields rather than 90.
- `scripts/verify_vds_q2h1_q3cash_bridge.py` asserts 5 exact source checks Q2 H1 and 3 derived Q3 checks at full VND, no fabricated Q2 cashflow.
- `.github/workflows/validate.yml` runs new source QA regression.
- Merge after CI PASS, rerun 45/45 production smoke and record commit.

## Next
- VDS 2026-Q2 B01/B02 (currently unverified auto-extract) must be fully inspected to finish quarter; then 2026-Q1 and 2025-Q1–Q4 source verification, do not reprocess Q3 finished.
- GAS cross-source H1 10.160.150.278 VND still attribution unresolved but well documented, no fabricated correction.
- After VDS complete progress to GEG historical gaps, IDC Q3/2026 (do not redo GEG Q3 already PASS). PLX Q3 parent CFF discrepancy still blocked until original reconciliation.
- Dates >=2025-Q1, max 20 quarters, amounts `triệu VND` except EPS, tolerated diff <=0.01%, preserve all source-version audit trails and GitHub main as deployment source of truth.
