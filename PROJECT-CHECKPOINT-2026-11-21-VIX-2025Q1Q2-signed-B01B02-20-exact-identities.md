# CHECKPOINT — VIX 2025-Q1 / 2025-Q2 separate statements B01/B02 original audited 21/11/2026

## Objective and scope
Continue from prior checkpoint `PROJECT-CHECKPOINT-2026-11-21-VIX-Q1Q2-2025-original-B03-cash-reconciliation.md` (merged PR #101). Verify remaining B01/B02 from signed issuer PDF, never redo already original-verified B03, never mix parent/separate source with consolidated.

## Original scanned PDF source visually inspected, not OCR
- VIX 2025Q1 signed issuer https://vixs.vn/wp-content/uploads/2025/04/20250418-VIX-Bao-cao-tai-chinh-Quy-I.2025.pdf SHA256 `216fe041cc81154b3d3b5ed6c4fa0f3e4b0b677c188b407d388397455a9294ee`, 45 pages; EXACT SHA256 also Vietstock Q1 PDF.
- VIX 2025Q2 issuer https://vixs.vn/wp-content/uploads/2025/07/20250718-VIX-Baoaotaichinh-Quy-2.2025-VIE.pdf SHA256 `9a2a0aa50ef32c5a87bc5f62005c376f2b423874e139bf7b4b3c77c4db911328`, 43 pages. Vietstock 43p SHA256 `1131acc3cfefeb0a6c52ea554362b4545dfe80bbe899cc7ae8af9c0da44e2e20`; PDF page 2 cover differs while remaining 42 page renders identical. Distinguish variant bytes, same financial pages.
- Both PDF B01 scan pages 8–10, outside-B01 customer assets p11, B02 pages 13–15, previously validated B03 pages16–17 visually read. These statement pages contain no native selectable text; never call a plain OCR snippet visual verification. Units originally exact VND.

## Main original corrections exact VND (not 0.1% approximation)
| Metric | 2025-Q1 as filed | 2025-Q2 as filed (standalone) |
|---|---:|---:|
| Total assets B01 code 270 | 20,610,738,530,166 | 24,385,197,959,515 |
| Current assets B01 | 20,563,916,458,536 | 24,339,768,830,051 |
| Noncurrent assets | 46,822,071,630 | 45,429,129,464 |
| Total liabilities | 4,193,720,690,957 | 6,666,569,152,664 |
| Equity | 16,417,017,839,209 | 17,718,628,806,851 |
| Cash B01 / B03 (closing) | 487,051,070,917 | 1,053,870,185,574 |
| Short term broker loans | 3,970,500,000,000 | 6,207,000,000,000 |
| B02 operating revenue | 979,684,153,559 | 1,976,150,333,018 |
| B02 operating expenses | 467,829,446,160 | 288,624,680,113 |
| B02 pretax profit | 465,204,861,310 | 1,602,507,328,938 |
| B02 income tax | 92,927,921,539 | 300,896,361,296 |
| B02 net profit | 372,276,939,771 | 1,301,610,967,642 |
| Customer brokerage cash B01 OFF-balance code026 | 889,333,145,197 | 1,304,612,755,731 |

- Current + noncurrent assets = total assets; liabilities+equity=assets; current + long liabilities = total liabilities; financial/nonfinancial current assets and financial detail components sum exactly; operating P/L+other P/L=pretax, current+deferred tax=tax total, pretax-tax=profit. **10 independently computed exact source identities per signed period, residual 0 VND**.
- B02 H1 signed YTD independently equals Q1+Q2 for revenue `2,955,834,486,577`, pretax `2,067,712,190,248`, net profit `1,673,887,907,413` (all VND exactly).
- Q1 source EPS = 255 VND/share, Q2 signed B02 quarterly EPS cell is **blank**; YTD EPS 1,093 VND/share. Q2 quarterly EPS kept null (not calculated by subtraction).
- Client brokerage cash is *off* issuer B01, so `broker_customer_deposits` stays null instead of incorrectly displaying 1,304,613 million as a company liability. Off-balance original saved under `client_brokerage_cash_off_balance`.
- Old serious errors: Q1 noncurrent assets 1 million instead of 46,822.071630 million; Q2 0 instead of 45,429.129464 million; Q2 operating expenses 625 million instead of 288,624.680113 million; Q2 financial expenses 34,059 million instead of 70,244.408220 million; original Q1/Q2 tax current/deferred were mistaken. Corrected from signed images.
- Previous B03 exact VND CFO/CFI/CFF and cash bridge from PR101 **unchanged**.

## Code and quality gates
- Original exact VND structured ledger: `reports/source-audits/VIX-2025Q1Q2-original-B01-B02-exact-vnd.json`.
- `data/financials-VIX.json`: corrected Q1+Q2 B01/B02, separate scope, source metadata SHA and page map, EPS quarter vs YTD; unrelated 2025Q3–2026Q3 untouched.
- `scripts/verify_vix_2025q1q2_original_b01_b02.py`: checks independent 20 B01/B02 arithmetic identities, exact-mapped source amounts, H1 signed B02 bridges, EPS and no missing-scope false pass and negative test mutated B01 totals/tax.
- `.github/workflows/validate.yml` now requires verifier in addition to unchanged earlier B03 and PLX regressions.
- This checkpoint created on isolated branch and does **not** claim merged / live CI until successfully checked.

## Next item
1. Run PR CI, merge only when PASS; postmerge validate and 45/45 HTTPS/SHA website, Pages deployment success; make durable final main checkpoint.
2. Mark VIX separate **Q1/Q2 2025 completed** after the above gates; do not treat separate report as consolidated.
3. Continue VIX 2025-Q3 (currently source-only and severe data corruption) from issuer signed original. Do not blindly accept preexisting source fields; 0.1% tolerance only for same data item and cross-source source-confirmed subtotal.
