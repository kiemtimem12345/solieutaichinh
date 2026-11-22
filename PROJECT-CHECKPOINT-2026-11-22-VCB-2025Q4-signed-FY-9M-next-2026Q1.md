# CHECKPOINT — VCB signed consolidated 2025Q4 and full-year source, 2026-11-22

Repo: `kiemtimem12345/solieutaichinh`; PR **#139**; branch `work/vcb-2025q4-signed-FY-audited-source-20261122`, target main.
**Sequence:** VCB 2025Q1/Q2/Q3 already individually source PASS and merged; Q4 signed original B02/B03/B04 source verified, financial CI needed then merge/check main. Next **VCB Q1/2026**, Q2/2026, Q3/2026, then next requested ticker per latest checkpoint. Never redo completed quarters, don't import 2024 periods.

## Source provenance
- Vietcombank consolidated Q4 and FY2025 **first-issued issuer signed 30/01/2026** PDF `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/VCB_Baocaotaichinh_Q4_2025_Hopnhat.pdf`, 71 scanned pages, **18,635,021 bytes**, SHA256 **`1f71919eae463bd24e6978e4ebb89d54c5c53f5b0645adf0fd439e71bdb86aa8`**; GitHub source Action `44971548969` SUCCESS, short-lived image artifact `14734205695`. Original PDF pages B02a/TCTD-HN consolidated balance pp4–5, off-balance 6, B03a/TCTD-HN Q4+FY earnings pp7–8, B04a/TCTD-HN FY cash pp9–10. All amounts **triệu VND** as PRINTED. Not labelled FY audited; later independent audited version requires separate comparison if found, never silently overwrite.
- `reports/source-audits/VCB-2025Q4-original-signed-consolidated-FY-million-vnd.json`: **138 signed million-VND values**, 30 source accounting equations zero million residual. `scripts/verify_vcb_2025q4_signed_original_FY.py`: independently recomputes 30 source equations, **24 exact current quarter B03a vs FY minus verified 9M B03a** bridges, Q4 bank B04 exact cash and four corruption negative controls. Enforce via `.github/workflows/validate.yml`.
- `data/financials-VCB.json`: only Q4/2025 signed data changed, keep original 2024 as comparative only; independently source-verified Q1–Q3 2025 unchanged. Bank B04 cash/equivalents != vault cash in B02 (different account definitions). Correct Q4 financing outflow **cash dividends** signed -3,776,798 million, not a balancing plug.
- Private exceptions `reports/financial-exception-queue.json`: do not show contents or list missing tickers unless user explicitly asks. Work sequentially without waiting for user.

## B02a consolidated bank 31/12/2025, TRIỆU VND
| Item | Signed original |
|---|---:|
| Total assets | **2.441.928.945** |
| Liabilities | 2.214.393.069 |
| Equity including NCI | 227.535.876 |
| Vault cash | 15.542.768 |
| State Bank deposits | 37.445.504 |
| Interbank deposits/loans | 521.938.509 |
| Customer loans net | 1.648.557.141 |
| Investment securities | 162.104.164 |
| Customer deposits (bank liability) | 1.672.534.103 |

## B03a Q4 directly signed / FY2025 12M, TRIỆU VND
| Item | Direct Q4 2025 | FY 2025 |
|---|---:|---:|
| Net interest income | 16.169.790 | 58.674.375 |
| Net service income | 864.624 | 3.469.867 |
| Total operating income | 19.172.495 | 72.357.586 |
| Operating expenses | -7.437.685 | -25.152.290 |
| Pre-provision profit | 11.734.810 | 47.205.296 |
| Credit risk provision | -847.507 | -3.185.040 |
| Pretax profit | **10.887.303** | 44.020.256 |
| CIT | 2.253.520 | 8.821.823 |
| PAT consolidated | **8.633.783** | 35.198.433 |
| PAT parent | 8.629.542 | 35.178.155 |

All 24 source B03a Q4 directly printed fields equal 12M current year minus previously PASS signed 9M at printed million precision, **0 million discrepancy**.

## B04a corporate bank cash, TRIỆU VND
| Item | FY2025 source 12M | Q3 report signed 9M | Standalone Q4 |
|---|---:|---:|---:|
| CFO | +115.341.217 | +106.283.289 | **+9.057.928** |
| CFI | -1.379.136 | -718.369 | **-660.767** |
| CFF | -3.776.798 | 0 | **-3.776.798** |
| Net change | +110.185.283 | +105.564.920 | **+4.620.363** |
| Cash/equivalents opening | 430.614.185 | 430.614.185 | **536.179.105** |
| Cash/equivalents closing | **540.799.468** | 536.179.105 | **540.799.468** |

FY CFO+CFI+CFF=FY net; FY opening+net=FY closing. Q4 CFO+CFI+CFF=Q4 net; Q4 opening+net=Q4 closing, all exact **0 triệu VND** residual. Bank B04 corporate cash/equiv ending 540.799.468 vs B02 vault cash 15.542.768, do not enforce equality of unlike concepts.

## Resume w/o question
1. Financial CI and source visual workflow latest PR #139 PASS, merge, re-fetch main, record completion.
2. Next signed VCB consolidated **2026 Q1** from Vietstock/HOSE/issuer original, then 2026Q2, Q3. Reported unit million VND, B02a B03a B04a. Calculate Q1 CFO directly, H1 Q2 standalone B04=6M−Q1, Q3 B04=9M−6M, never substitute interest received as CFO.
3. Save checkpoint per PASS. If true source-vintage discrepancy, append private queue, don't show ticker list, move on. Keep 2024 separate source comparator only; no 2024 row. Don't claim website deployment without proof.
