# CHECKPOINT 2026-11-22 — VCB consolidated 2026Q1 signed original, B04 CFO repair; next Q2

**Repository** `kiemtimem12345/solieutaichinh`, branch `work/vcb-2026q1-original-consolidated-20261122`, PR **#140** target main. This checkpoint describes verified issuer source in the working PR; never claim merged before newest CI PASS and main re-read.

## Preserve already verified
VCI all 2025–2026, VCK source-signed quarters, VCB 2025Q1/Q2/Q3/Q4 merged PR #136–#139; DO NOT repeat them unless later explicit contradiction. No 2024 dashboard periods; comparatives in 2025 source are allowed only as accounting starting balance. Use exact original banking **triệu VND** and B02/TCTD-HN, B03/TCTD-HN, B04/TCTD-HN original-form names, not generic industrial layout. Exceptions private in `reports/financial-exception-queue.json` and never enumerate unless user asks which tickers/periods remain. Work sequentially, without permission/confirmation.

## VCB 2026Q1 controlling signed source
- Original signed consolidated issuer Q1 PDF `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/VCB_Baocaotaichinh_Q1_2026_Hopnhat.pdf`, signed **29/04/2026**. PDF **53 pages, 8,505,770 bytes**, SHA256 **`fd4d634f10478caa9f5f1e0b2b85f3dbae86d1f619e20f2e797ffb6ede244879`** verified source worker GitHub Actions **44972227179 SUCCESS**, original-page artifact **14733699149**. Original page images reviewed B02 balance pp5–6, B03 income pp8–9, B04 bank cash pp10–11. Report PDF uses million VND printed integers, text layer 164 characters.
- Detailed `reports/source-audits/VCB-2026Q1-consolidated-original-29april-million-vnd.json`: **116 signed source million-VND fields**, **30 independent core exact source equations all zero**, plus explicitly retained 2025 audited starting-comparison values. CI `scripts/verify_vcb_2026q1_signed_original_consolidated.py` with 30 re-computed equations and 4 deliberately corrupted controls. Mandatory in `.github/workflows/validate.yml`.
- `data/financials-VCB.json` Q1 2026 only updated; previously provisional CFO erroneous +31,437,617 million (gross interest receipts) replaced with actual signed B04 CFO **+35,398,194**; CFI erroneously -308,060 (capex) replaced by original B04 section **-294,108**. All Q1 same-source current-year financials have 0 million-VND source reconciliation residual.
- Row status `issuer_signed_VCB_2026Q1_consolidated_B02_B03_B04_signed_30_exact_checks`; Q1 signed B04 financing zero. Do not use consolidated bank vault cash as B04 cash-equivalents ending.

## 31/03/2026 issuer signed consolidated B02 (million VND)
| Field | Signed |
|---|---:|
| Total assets | 2.550.963.342 |
| Liabilities | 2.316.932.013 |
| Equity | 234.031.329 |
| Cash on hand | 12.930.996 |
| State Bank deposits | 17.957.497 |
| Deposits/loans to other banks net | 581.521.607 |
| Loans to customers net | 1.727.390.880 |
| Customer deposits liability | 1.682.032.374 |

## Q1 original B03 income (million VND)
| Field | Signed |
|---|---:|
| Gross interest income | 32.091.990 |
| Net interest income | 17.651.083 |
| Net service income | 943.415 |
| Total operating income | 21.179.810 |
| Pre-provision profit | 14.295.755 |
| Credit risk provision | -2.493.102 |
| Pretax profit | **11.802.653** |
| Corporate income tax | 2.340.558 |
| Consolidated net profit | **9.462.095** |
| Parent attributable profit | 9.456.566 |

## Original Q1 2026 B04 signed cash (million VND)
| Field | Correct |
|---|---:|
| CFO | **+35.398.194** |
| CFI | **-294.108** |
| CFF | 0 |
| Net cash increase | **+35.104.086** |
| Opening bank cash/equivalents | 541.688.802 |
| Closing bank cash/equivalents | **576.792.888** |

CFO+CFI+CFF=net and opening+net=closing, exact zero million residual. Original B04 gross cash interest receipts +31.437.617 is NOT operating cashflow subtotal.

## Source-vintage isolation, no signed-number plug
- Source Q1 2026 original B02 31/12/2025 **audited comparative**: assets 2.442.279.166 million, liabilities 2.217.720.440, equity 224.558.726. Original signed asfiled Q4 2025 (first release) B02 assets 2.441.928.945, liabilities 2.214.393.069, equity 227.535.876.
- Original Q1 2026 B04 FY2025 **audited** opening cash equivalent is 541.688.802; first-issued signed Q4 2025 B04 cash ended 540.799.468; **+889.334 million difference** between editions. Do NOT apply 0.1% tolerance to patch cash or alter prior Q4 signed values.
- Private nonblocking evidence row `VCB-2026Q1-FY2025-audited-comparative-vs-first-asfiled-vintage` in `reports/financial-exception-queue.json`: preserve both first-issued and audited FY2025 source versions; revisit when audited FY2025 B02/B04 original obtained with revision notes. Signed Q1 itself is internally source-validated and production eligible.
- **Never surface queued details/uncompleted ticker list to user unless specifically asked.**

## Immediate continuation
1. Confirm latest PR #140 signed original worker and financial CI PASS, merge, re-fetch main row and checkpoint; do not assume deployment.
2. Continue VCB **2026Q2** next from actual issuer signed consolidated Q2 B02/B03/B04, and H1 reviewed FY2026 where available. Extract direct Q2 B03 and H1 6M, derive Q2 B04 CFO/CFI/CFF/net from H1 minus Q1 **on same source vintage**, preserve Q1 and audited FY2025 baseline.
3. Then VCB 2026Q3, then next ticker per latest checkpoint. Always save source exact numeric, 2025+ no redundant reprocessing, unresolved anomalies silently queued internally, no confirmations.
