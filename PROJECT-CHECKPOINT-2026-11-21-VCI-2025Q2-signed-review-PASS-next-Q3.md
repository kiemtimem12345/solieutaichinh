# CHECKPOINT VCI 2025-Q2 — issuer signed B01/B02 + PwC-reviewed H1 B03, 21/11/2026

## Repository and scope
- Repo: `kiemtimem12345/solieutaichinh`, PR #123, work branch `work/vci-2025q2-original-exact-source-20261121`, target `main`.
- Prior PASS VCI 2025Q1 PR #122 and VCI 2026Q3 PR #121 are preserved. This period is Q2/2025, not an instruction to redo Q1 or Q3/2026.
- Q2 issuer 47-page original PDF `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/VCI_Baocaotaichinh_Q2_2025.pdf`, signed 18/07/2025, 8,011,665 bytes, SHA-256 `70c08fb3733de0e582bd8a35870d2d52253d1972b07ba9675539f22ad8a7e761`. Visual PDF pages B01 5–7, B02 10–12, B03 13–14, Note1 19 `Công ty không có công ty con`. Source job `44921419236` PASS; artifact `14714430008`, 22 limited preview JPEG pages, 1-day retention. Not a legally issuer titled consolidated statement; no sub group perimeter.
- PwC-reviewed, issuer disclosed 2025H1 report `https://www.vietcap.com.vn/api/cms-api/uploads/froala/files/20250814%20-%20VCI%20-%20CBTT%20BCTC%206T%20nam%202025.pdf` official Vietcap site; reviewed 12/08/2025 and released 14/08/2025. This original searchable PDF provides exact B03 6M source codes 60/70/80/90/101/103. The original Q2 scan visually obscures parentheses on total CFF/net rows; **do not treat ambiguity as positive**; PwC-reviewed report explicitly prints those two with parentheses, and signed components/period cash reconcile to 0 VND.
- Source JSON `reports/source-audits/VCI-2025Q2-signed-original-reviewed-H1-exact-VND.json` has 57 exact-VND items, original hashes / cited PDF pages, income 6M cross-check, no customer-money contamination, and Q2 standalone B03 derivation.
- Regression `scripts/verify_vci_2025q2_signed_original_reviewed_h1.py`, CI `.github/workflows/validate.yml`; 16 dynamic equations and 4 deliberately corrupted controls, PASS PR financial CI run `44921881659`. PDF inspection run `44921881653` PASS. Do not invent post-merge deploy/smoke success.

## Signed Q2/2025 source, VND
| Item | Exact VND |
|---|---:|
| B01 assets | 21.897.761.800.316 |
| Liabilities | 9.458.706.053.920 |
| Equity | 12.439.055.746.396 |
| Current assets | 21.777.317.137.834 |
| Non-current assets | 120.444.662.482 |
| Company cash at 30/06 | 472.276.928.356 |
| Quarter operating revenue | 1.159.674.866.340 |
| Quarter operating expense | 772.258.024.779 |
| Quarter pretax profit | 211.490.551.060 |
| Quarter income tax expense | 27.588.714.170 |
| Quarter net profit | 183.901.836.890 |
| 6M cumulative revenue | 2.010.603.829.672 |
| 6M cumulative pretax profit | 566.597.571.738 |
| 6M cumulative net profit | 478.769.619.296 |

## 2025 H1 / Q2-only corporate cashflows (not client custody), VND
| Cashflow | Signed H1 6M | Signed Q1 3M | Standalone Q2 = 6M−3M |
|---|---:|---:|---:|
| CFO | -109.179.436.687 | +10.325.858.831 | **-119.505.295.518** |
| CFI | -27.279.627.952 | -9.337.876.940 | **-17.941.751.012** |
| CFF | -4.135.035.939.750 | -2.442.495.939.750 | **-1.692.540.000.000** |
| Net cash change | -4.271.495.004.389 | -2.441.507.957.859 | **-1.829.987.046.530** |
| Opening cash | 4.743.771.932.745 | 4.743.771.932.745 | **2.302.263.974.886** |
| Closing cash | 472.276.928.356 | 2.302.263.974.886 | **472.276.928.356** |

- 6M cashflow sections/bridge are exact 0 VND residual, verified PwC-reviewed issuer report.
- Q2 quarter sections/bridge exact 0 VND, using same issuer reporting scope and signed Q1 original; **do not add brokerage customers' ending cash 3.001.604.933.090 VND**.
- Reviewed H1 B03 positive/negative sign evidence is essential because scanned as-filed PDF total signs ambiguous. Do not overwrite with rounded feeds or false zero.
- Q2 original old bootstrap incorrectly had `cash_ending=277` triệu VND and `foreign_exchange_effect_ytd=3.001.605` triệu (actually client deposits) and rounded AFS. Corrected `cash_ending=472.276928356` triệu, FX 0 where original code102 is blank, client deposits stored in own broker field; exact AFS 7.782.930.658.026 VND.
- Website row stores VND/1,000,000, manually verified fields and source note, `cashflow_period_basis=year_to_date` for lũy kế, quarter cashflow keys for quý độc lập.

## Next action
- Once PR #123 is merged, independently verify main data and CI/deploy where observable, store completion checkpoint.
- Continue **VCI 2025-Q3** signed 9M, compare 9M minus above signed 6M; then Q4/2025, Q1/2026, Q2/2026, one period at a time. VCI Q3/2026 already validated, do not reprocess.
- MBB, VIX, GAS, VDS 7/7 QA PASS; GEG and IDC 7/7 case closed with Q2 2026 qualified cashflow null until audited FY2026; PLX 2026Q3 parent B03 CFF abnormal above 0.1% remains blocked until signed corrected disclosure.
