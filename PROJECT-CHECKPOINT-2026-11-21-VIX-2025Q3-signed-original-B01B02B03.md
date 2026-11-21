# CHECKPOINT — VIX 2025-Q3 riêng: khôi phục B01/B02/B03 PDF ký gốc, sửa đơn vị, 21/11/2026

## Source and scope
- Source **issuer signed VIX Q3/2025 separate financial statements**, published 08/10/2025 https://vixs.vn/wp-content/uploads/2025/10/VIX-BCTC-QuyIII-2025.pdf.
- Original PDF **44 pages, 13,211,181 bytes, SHA256 `66bafedaede09d88847aa40b7278d559e21adfcd02d51a23fc7735127347f7e9`**, downloaded fully in GitHub Actions `44862199627`.
- Vietstock Q3 mirror https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/VIX_Baocaotaichinh_Q3_2025.pdf, **44 pages, 13,242,888 bytes SHA256 `e6b35015581bb224bc82b61c0ba25ddb15d22aea54bfb2ea63917653fd355285`**. Exact per-page rendered comparisons **43 of 44 identical**, only cover page 2 differs. Do not claim binary identical.
- Signed scan pages B01 **8-10**, off-balance customer cash **11**, B02 **13-15**, B03 **16-17**, visually reviewed, no selectable page text. Report scope **RIÊNG** not consolidated.

## Verified original monetary VND
| Metric | Signed Q3 2025 |
|---|---:|
| Assets B01 | 31,534,673,037,863 |
| Liabilities B01 | 11,366,620,883,443 |
| Equity B01 | 20,168,052,154,420 |
| Cash B01 = B03 | 909,902,606,614 |
| Current liabilities | 10,735,210,958,329 |
| Q3 operating revenue | 3,221,825,111,028 |
| Q3 operating expenses | 50,461,306,513 |
| Q3 FVTPL cost line 21 **as signed, negative** | -11,207,793,585 |
| Q3 pretax profit | 3,047,932,095,844 |
| Q3 tax | 598,508,748,275 |
| Q3 net profit | 2,449,423,347,569 |
| 9M signed CFO | -7,221,911,471,398 |
| 9M signed CFI | +286,250,000 |
| 9M signed CFF | +7,438,000,000,000 |
| 9M signed net cash | +216,374,778,602 |
| 9M opening / closing cash | 693,527,828,012 / 909,902,606,614 |

- Prior Q2/2025 **signed H1 B03** from PR #101: CFO -3,002,293,892,438; CFI +636,250,000; CFF +3,362,000,000,000; net +360,342,357,562; ending cash 1,053,870,185,574.
- Standalone **Q3 = 9M minus H1** (same VIX separate scope): CFO -4,219,617,578,960; CFI -350,000,000; CFF +4,076,000,000,000; net **-143,967,578,960**; opening 1,053,870,185,574, closing **909,902,606,614**; all cash equations 0 VND difference.
- Source 9M revenue 6,177,659,597,605, pretax 5,115,644,286,092, PAT 4,123,311,254,982. Every 9M metric equals **signed H1 + signed Q3 standalone** to VND exact.
- EPS Q3 standalone original B02 cell blank; 9M YTD EPS **2,692 VND/share**, do not copy to quarter.
- Customer brokerage cash off-B01 code026 **2,901,037,830,725 VND**, stored in separate field `client_brokerage_cash_off_balance`, **not** B01 firm cash/liabilities.
- Prior JSON had raw **VND mistaken for triệu VND** in numerous source values (e.g. cash 909,902,606,614 incorrectly displayed as 909 trillion million), tax wrongly set 1001/1002/2003 (line codes, not money), `broker_operating_expenses` incorrectly set to signed FVTPL loss, and EPS YTD used as quarter. Corrected.

## Changes and QA
- `reports/source-audits/VIX-2025Q3-original-B01-B02-B03-exact-vnd.json`: signed source VND and both original PDF SHA; no copyrighted PDF body committed.
- `data/financials-VIX.json`: Q3 original source exact fields normalized to million VND; off B01 client balances; YTD/quarter cash and B02 separate. Q1/Q2 2025 PASS records and VIX other periods preserved.
- `scripts/verify_vix_2025q3_signed_original.py`: **15 original signed B01/B02/B03 identities** exact, original source mapping, Q3 separate 9M−H1 B03, B02 9M−H1, missing quarter EPS, off-B01 client cash and sign of signed FVTPL cost, tamper negative tests.
- `.github/workflows/validate.yml` runs added test along with all previous financial regressions.
- **NOT YET PRODUCTION PASS** until PR validation CI PASS, merge into main, postmerge site smoke **45/45 URL SHA256** PASS, final durable checkpoint. Do not mark Q4/2025 or later VIX periods complete from this work.

## Next item
After post-merge all checks pass: VIX **2025-Q3 separate** completed, then **2025-Q4 separate** from original signed PDF and audited FY2025 period-vintage check; do not assume FY cash 12M and original Q4 12M are same vintage. Numeric subtotal tolerance <=0.1% after independent cross-source display agreement only; wrong unit/sign/period never excused.
