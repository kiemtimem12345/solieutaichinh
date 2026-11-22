# CHECKPOINT 2026-11-22 — VCK Q2/2026 signed source and reviewed H1 exact cash

## Repository / position
- Repo `kiemtimem12345/solieutaichinh`; PR **#134**, branch `work/vck-2026q2-issuer-pdf-b01-b02-b03-20261122`, target `main`.
- VCK Q1/2025, Q3/2025, Q4/2025, Q1/2026 are already individually PASS and must not be reprocessed. Do not import 2024 periods.
- Current VCK Q2/2026 source ledger and data row completed in PR #134; final CI PASS required before merge, then main re-read. Next sequential VCK **Q3/2026** source inspection; private exception queue is never displayed or enumerated unless user asks.

## Signed originals and independent reviewed check
- Signed issuer as-filed Q2 PDF `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCK_Baocaotaichinh_Q2_2026.pdf`: 61 pages, 3,588,837 bytes, SHA-256 `6652ed69f6a3c666194d5594813234e5458d45fc40691dd1a97736143dc0bfa9` verified GitHub source workflow **44968719866 SUCCESS**, original B01/B02/B03 images inspected, 19 JPEG previews retained only one day. Issuer signed 17/07/2026; published 20/07/2026 on VPS company investor relations. B01 PDF pages 5–7, B02 10–13, B03 corporate 14–15, customer broker custody separate 16–17.
- Independently reviewed H1 2026 original (signed 12/08/2026, released 14/08/2026) issuer page `https://www.vps.com.vn/bai-viet/vps-cong-bo-bao-cao-tai-chinh-ban-nien-nam-2026-da-duoc-soat-xet`, exact-document mirror `https://cdn.financialreports.eu/financialreports/media/filings/67046/2026/RNS/67046_rns_2026-08-17_18938e4a-bf13-458e-93eb-511024a13ac3.pdf`, 72 pages. Visually checked reviewed B03 corporate PDF pages 16–17; all six 6M CFO/CFI/CFF/net cash begin/end values **match the issuer Q2 original exactly 0 VND difference**. Original reviewed mirror PDF hash not asserted.
- The reporting company is **Công ty Cổ phần Chứng khoán VPS** (VCK), issuer company statements, not an intentionally labeled consolidated report. Broker customer deposits are **not** part of company B01 cash/B03 cash.
- Financial ledger `reports/source-audits/VCK-2026Q2-issuer-signed-original-and-Q1-quarter-vnd.json` has **84 exact issuer VND values, 34 source checks**: 30 exact-zero and four signed direct-Q2-vs-YTD-Q1-vintage comparison differences. New test `scripts/verify_vck_2026q2_original_reviewed_h1.py` independently recomputes >20 essential accounting equations plus four deliberately corrupted source/website controls.
- `data/financials-VCK.json` only Q2/2026 is newly normalized, in triệu VND as source VND divided by 1,000,000. `.github/workflows/validate.yml` includes required verifier; other prior completed quarters unchanged.

## Signed company Q2 2026 key values (exact VND)
| Indicator | Signed VND |
|---|---:|
| B01 total assets | 47.889.303.869.390 |
| Liabilities | 16.683.033.357.125 |
| Equity | 31.206.270.512.265 |
| Company cash 30/06 | 3.359.625.056.650 |
| Q2 standalone operating revenue | 2.353.844.251.179 |
| Q2 operating expenses | 626.831.258.189 |
| Q2 profit before tax | 1.378.410.312.930 |
| Q2 income tax expense | 274.079.899.738 |
| Q2 profit after tax | 1.104.330.413.192 |
| H1 (6M) revenue | 4.873.028.013.544 |
| H1 (6M) profit after tax | 2.339.601.212.206 |

## B03 corporate Q2 2026 separately, exact VND
| Cashflow | Signed + reviewed 6M | Signed Q1 | Standalone Q2=6M−Q1 |
|---|---:|---:|---:|
| CFO | -2.969.984.185.501 | -6.395.830.382.439 | **+3.425.846.196.938** |
| CFI | -66.449.390.863 | -6.733.321.692 | **-59.716.069.171** |
| CFF | -2.284.931.680.002 | +3.883.748.999.998 | **-6.168.680.680.000** |
| Net change | -5.321.365.256.366 | -2.518.814.704.133 | **-2.802.550.552.233** |
| Cash opening | 8.680.990.313.016 | | **6.162.175.608.883** |
| Cash closing | 3.359.625.056.650 | | **3.359.625.056.650** |

- 6M corporate CFO+CFI+CFF=net, and 6M opening+net=closing, **0 VND discrepancy**.
- Q2 standalone corporate CFO+CFI+CFF=net and Q2 cash opening+net=closing, **0 VND discrepancy**. Corporate cash 3,359,625,056,650 VND matches signed B01 and reviewed H1 B03, distinct from separately reported broker customer 14,449,037,907,097 VND.

## Small B02 signed-vintage note, internal only
- Signed Q2 standalone direct B02 is controlling source. H1 current-year cumulative minus original signed Q1 differs by precisely 29,595,000 VND in admin expense / operating profit / pretax and net income, while Q2 direct B02 balances and is reported as filed. No balancing plug or source changes.
- 29,595,000 / 1,378,410,312,930 = ~0.00215% of Q2 PBT; 29,595,000 / 174,435,742,281 ~0.01697% of Q2 admin expense. Both under user's later **0.1% acceptance**. Keep direct B02 numbers and note variance. Internal private queue record `VCK-2026Q2-B02-H1-Q1-vintage-delta-29595000` in `reports/financial-exception-queue.json` is nonblocking, production eligible; do not display queue list unless explicitly asked.
- Compared to 0.01% original tolerance, admin line difference is above that tighter threshold; no misleading claim all lines are under 0.01%.

## Next actions
1. Confirm final PR #134 financial CI pass and original PDF visual source workflow success; merge, re-read main source Q2 values and checkpoint.
2. Immediately process VCK 2026Q3, using already catalogued original signed Q3 PDF `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VCK_Baocaotaichinh_Q3_2026.pdf` or exact HOSE source `https://staticfile.hsx.vn/Uploads/UploadDocuments/2505926/20261020%20-%20VCK%20-%20Bao%20cao%20tai%20chinh%20Quy%203.2026%20-%20signed.pdf`. Compute standalone Q3 B03 as signed 9M−independently reviewed H1 6M **same reporting entity**. Verify B01/B02/B03 original visual source, units, signs, customer brokerage cash segregation, new CI. Then return to next ticker in current approved order, not old stale positions.
3. Persist checkpoints and audits after each period. Internal queue stays private to user and automation reports unless user asks for outstanding ticker list. No pause for routine confirmation.
