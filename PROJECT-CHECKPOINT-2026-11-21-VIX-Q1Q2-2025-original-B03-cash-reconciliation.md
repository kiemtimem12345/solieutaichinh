# CHECKPOINT — VIX Q1–Q2/2025 B03 signed original recovery and cashflow correction

Date 2026-11-21. Production repo `kiemtimem12345/solieutaichinh`. Workstream: VIX separate statements (NOT consolidated). Previous Q1, Q2 were numeric OCR pending visual; B03 CFO was mis-mapped to pretax profit and Q1 cash opening/closing was incorrect.

## Signed original sources recovered and cross-checked
- Q1/2025 issuer: https://vixs.vn/wp-content/uploads/2025/04/20250418-VIX-Bao-cao-tai-chinh-Quy-I.2025.pdf — 45 pages, 7,343,885 bytes, SHA256 `216fe041cc81154b3d3b5ed6c4fa0f3e4b0b677c188b407d388397455a9294ee`; exactly matches Vietstock 2025Q1 PDF SHA256.
- Q2/2025 issuer: https://vixs.vn/wp-content/uploads/2025/07/20250718-VIX-Baoaotaichinh-Quy-2.2025-VIE.pdf — 43 pages, 5,990,019 bytes SHA256 `9a2a0aa50ef32c5a87bc5f62005c376f2b423874e139bf7b4b3c77c4db911328`.
- Q2/2025 Vietstock `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/VIX_Baocaotaichinh_Q2_2025.pdf`, 43 pages 6,021,822 bytes SHA256 `1131acc3cfefeb0a6c52ea554362b4545dfe80bbe899cc7ae8af9c0da44e2e20`. Independent page-by-page image render at 90% shows **42/43 identical pages**, only PDF page 2 differs (cover disclosure text). Therefore signed B01/B02/B03 pages are visually identical. Do not infer exact same PDF bytes.

## VND original and derived cash
| Field | Original Q1 B03 (3M) | Original Q2 B03 (6M YTD) | Q2 standalone (=6M−3M) |
|--|--:|--:|--:|
| CFO | -1,331,196,257,095 | -3,002,293,892,438 | -1,671,097,635,343 |
| CFI | -780,500,000 | +636,250,000 | +1,416,750,000 |
| CFF | +1,125,500,000,000 | +3,362,000,000,000 | +2,236,500,000,000 |
| Net cash flow | -206,476,757,095 | +360,342,357,562 | +566,819,114,657 |
| Opening cash | 693,527,828,012 | 693,527,828,012 | 487,051,070,917 |
| Closing cash | 487,051,070,917 | 1,053,870,185,574 | 1,053,870,185,574 |
| Capex | -780,500,000 | -1,613,750,000 | -833,250,000 |

- Every CFO+CFI+CFF identity and opening+net=closing identity above **exactly 0 VND residual**.
- Original Q1 B01 PDF page8 cash 487,051,070,917 and original Q2 B01 PDF page8 cash 1,053,870,185,574 match B03 page17. Original B03 pages16–17 signed, checked as images.
- Note Q1 previous JSON B03 `operating_cash_flow=465205` million actually matches pre-tax profit, NOT source CFO. Q2 prior `operating_cash_flow=1602507` million also matched pre-tax profit, NOT source quarterly CFO. Previous Q1 `cash_ending=889333` million was not the reported B01/B03 closing cash; corrected.
- Preserve Q1/Q2 separate-report scope, no consolidated figures substituted, all original VND converted only by exact /1e6. Q1 Q2 B01/B02 **other values remain pending detailed visual QA**, not marking fully completed yet.
- The new 0.1% tolerance rule **does not excuse wrong sign, wrong B03 category or period scope**.

## Implementation checkpoint
- New source ledger `reports/source-audits/VIX-2025Q1Q2-original-cash-vnd.json`.
- Regression `scripts/verify_vix_2025q1q2_original_cash.py` enforces exact signed Q1 and H1 cash, Q2 source subtraction, negative tests wrong-sign and broken cash bridge, and honest partial validation status.
- `data/financials-VIX.json`: update only Q1/Q2 B03 and B01 cash fields, preserve all other numeric original amounts and unrelated periods.
- `.github/workflows/validate.yml` must invoke regression test.
- Download job https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44859322696 PASS, source artifact `14689560438` contains original issuer and Vietstock PDFs + images; full PDFs must not be committed to Git.
- Merge production only after CI PASS, then 45/45 HTTPS SHA source smoke and deployment. Continue VIX Q2 B02, B01 remainder; do not prematurely mark VIX complete.
