# CHECKPOINT — VCI Q1/2026 signed-source B01 B02 B03 — 21/11/2026

Repository: `kiemtimem12345/solieutaichinh`, PR **#126**. Prior PASS Q1–Q4/2025 and Q3/2026 already merged; do not reprocess. Q1/2026 is the current ticker/quarter.

## Source document and accounting scope
- Official Vietcap issuer source URL: `https://www.vietcap.com.vn/api/cms-api/uploads/froala/files/20260420%20-%20VCI%20-%20Bao%20Cao%20Tai%20Chinh%20Q1.2026.pdf`, published/signed **20/04/2026**.
- Signed scanned original PDF: **48 pages, 15,121,284 bytes, SHA256 `b5562dc6db6a785388e8e2de6e4ea5c10d5c759448de22f27e6d2fcfdcbad2a1`**; direct source worker GitHub Action run **44924314308 PASS**, artifact **14714518427**, 26 JPEG page previews retention 1 day. PDF text only 48 chars, so visual source used, not unverified OCR.
- B01 source images PDF p5–7, B02 PDF pp10–12 horizontal layout, B03 source PDF pp13–14, Note1 p19 says **“Công ty không có công ty con.”** Do not falsely declare this as separate issuer-signed consolidated PDF. Keep brokerage client cash outside company B01/B03; TT210/2014 and TT334/2016 securities-company layout.
- Original signed prior FY2025 PwC FY cash end **3,213,693,581,406 VND** exactly equals 2026Q1 signed B03 cash opening. No unsupported 2025→2026 opening adjustment.
- Audit ledger `reports/source-audits/VCI-2026Q1-issuer-signed-original-B01-B02-B03-vnd.json`: **59 VND fields, 18 source accounting equations** (all zero VND residual); regression `scripts/verify_vci_2026q1_signed_original.py` includes 4 negative controls.
- CI `.github/workflows/validate.yml` includes new verifier; verify CI result before merge. No claim production smoke/Pages until observed.

## Core statements (VND)
| Item | Signed original Q1/2026 |
|---|---:|
| Total assets | 37.097.383.539.481 |
| Liabilities | 19.777.956.737.216 |
| Equity | 17.319.426.802.265 |
| Current assets | 35.816.715.628.040 |
| Non-current assets | 1.280.667.911.441 |
| Company cash 31/03 | 2.048.249.191.640 |
| Operating revenue | 1.406.482.341.875 |
| Operating expense | 631.834.532.493 |
| Profit before tax | 403.873.870.132 |
| CIT expense total | 63.143.989.044 |
| Profit after tax | 340.729.881.088 |
| CFO (B03 Q1) | -2.900.034.543.773 |
| CFI (B03 Q1) | -19.436.706.493 |
| CFF (B03 Q1) | +1.754.026.860.500 |
| Net cash movement | -1.165.444.389.766 |
| Quarter cash opening | 3.213.693.581.406 |
| Quarter cash closing | 2.048.249.191.640 |

- `CFO+CFI+CFF = net`, `cash open+net=cash close`, `assets=liabs+equity`, P&L and CIT net: all exact zero VND residual.
- Fixed tangible assets 84.447.178.868 + intangible 4.382.322.545 = 88.829.501.413 VND.
- Source dividend outflow -424.944.139.500, borrowing proceeds +12.203.971.000.000, repayments -10.025.000.000.000; CFF 1.754.026.860.500 VND exact.
- Website row is VND/1,000,000 in `data/financials-VCI.json` only 2026-Q1 updated. `cashflow_period_basis=quarter` (Q1 QTD=YTD), separate ytd fields kept for website.

## Next checkpoint
- After PR #126 CI success, merge and re-fetch main data, save checkpoint.
- **Last uncompleted VCI Q2/2026**: original Q2 48-page? source already recovered previously for Q3 2026 B03 source bridge; 6M audited/reviewed original PDF 98 pages and as-filed Q2 48 pages:
  - Q2 signed PDF mirror SHA256 `a8fec422bac195c1b4d9743a995da35ec5066fa6dc0f951e6fbb36f2218823b5`, 17,064,259 bytes.
  - PwC-reviewed H1 SHA256 `1ea814d02563a136d11d718c62c1ffc3c08463ffaf12369c517111cd26f6b9af`, 15,650,240 bytes.
  - Ledger `reports/source-audits/VCI-2026Q3-reviewed-H1-signed-Q2-quarter-cash-vnd.json` already has 6M CFO -4.539.879.183.965, CFI -26.547.106.493, CFF +5.001.663.109.500, net +435.236.819.042, cash start 3.213.693.581.406, end 3.648.930.400.448. Q2 standalone now can be derived using newly verified Q1 source from THIS checkpoint; check cash bridge equals 0 and B01/B02 original. Do not redo verified 2026Q3.
- Once VCI reaches 7/7, continue VCK, then remaining Q3/2026. MBB/VIX/GAS/VDS 7/7 PASS, GEG/IDC completed with issuer-vintage FY2026 caveat, PLX parent 2026Q3 CFF 87.654.015.000 VND mismatch still BLOCKED pending signed amendment.
