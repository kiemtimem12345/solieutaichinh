# CHECKPOINT — VCB consolidated 2025 Q2 signed issuer bank 6M source, Q2 standalone (22/11/2026)

## Repo and step
- Repo `kiemtimem12345/solieutaichinh`, branch `work/vcb-2025q2-signed-consolidated-6m-20261122`, PR #137 target `main`.
- Q1/2025 already issuer-source-verified and merged PR #136, DO NOT reread or reprocess.
- Signed **Q2/2025** original consolidated B02a/TCTD-HN balance, B03a/TCTD-HN income (quarter + 6M) and B04a/TCTD-HN cashflows (6M) recovered, validated in `reports/source-audits/VCB-2025Q2-original-signed-consolidated-H1-million-vnd.json`; `data/financials-VCB.json` only 2025-Q2 changed.
- **Next** VCB 2025-Q3 signed consolidated original; then Q4/2025 and Q1–Q3/2026 sequentially. Save checkpoint per period; never pause for permission, no 2024 dashboard rows. Private financial exceptions `reports/financial-exception-queue.json` stay hidden unless explicitly asked which tickers/periods remain. No claim production deploy until witnessed.

## Signed source
- Exact original `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/VCB_Baocaotaichinh_Q2_2025_Hopnhat.pdf`; signed **30/07/2025**, 53 pages, **15,489,752 bytes**, SHA-256 **`789948b37004bdfcb11e56c0efa153bc745e4ec2b79b4336d2a8413ac87f034a`**; GitHub source run `44970514105` PASS, source artifact `14733112765` 32 selected page JPEGs retained 1 day. PDF has no meaningful text layer, read page images directly. Source **triệu VND** as PRINTED; don't invent 1VND precision.
- Consolidated bank **B02a/TCTD-HN** balance PDF pages 4–5, off balance p6; **B03a/TCTD-HN** quarter and 6M income PDF pp7–8, signatures p8; **B04a/TCTD-HN** 6M cashflow PDF pp9–10. No mixing with securities-company B01/B02/B03 layouts.
- `scripts/verify_vcb_2025q2_signed_consolidated_h1.py`: 136 original source million-VND fields, **38 source B02/B03/B04 identities 0 residual**, 24 quarterly P&L 6M minus signed Q1 exact zero residual, quarterly B04 CFO+CFI+CFF, cash opening/closing both zero residual, four corrupted source/data negative controls. `.github/workflows/validate.yml` must PASS before PR #137 merge. Preview retrieval step may run independently; no original copyrighted PDFs committed into repo.

## B02a consolidated balance (TRIỆU VND 30/06/2025)
| Item | Signed source |
|---|---:|
| Total assets | **2.217.941.098** |
| Liabilities | 2.004.191.676 |
| Equity including noncontrolling | 213.749.422 |
| Vault cash | 14.790.170 |
| Deposits at SBV | 37.686.004 |
| Deposits/loans to other banks | 432.536.864 |
| Net customer loans | 1.522.462.472 |
| Securities investments | 162.434.366 |
| Customer deposits liability | 1.586.682.675 |

## B03a Q2 current quarter & 6M 2025 (TRIỆU VND)
| Item | Direct signed Q2 | Signed 6M |
|---|---:|---:|
| Interest income | 25.224.403 | 49.799.307 |
| Interest expenses | -11.064.211 | -21.951.962 |
| Net interest income | 14.160.192 | 27.847.345 |
| Net service income | 860.944 | 1.666.908 |
| Total operating revenue | 17.868.237 | 35.132.963 |
| Operating expenses | -6.024.732 | -11.677.169 |
| Pre-provision operating income | 11.843.505 | 23.455.794 |
| Credit risk provision | -809.590 | -1.561.946 |
| Profit before tax | 11.033.915 | 21.893.848 |
| Corporate income tax | 2.196.544 | 4.354.751 |
| Profit after tax (consolidated) | **8.837.371** | 17.539.097 |
| PAT attributable parent | 8.831.885 | 17.528.114 |

The Q2 current-quarter column matches exact 6M−source-signed Q1 for 24 current-year P&L fields (including noncontrolling equity), 0 **triệu VND** discrepancies.

## Bank B04a consolidated quarterly cash (TRIỆU VND)
| Item | H1 2025 signed six-month | Q1 2025 signed | Derived Q2 alone |
|---|---:|---:|---:|
| CFO | **+24.736.707** | -13.180.595 | **+37.917.302** |
| CFI | **-354.102** | -174.898 | **-179.204** |
| CFF | **0** | 0 | **0** |
| Net cash movement | **+24.382.605** | -13.355.493 | **+37.738.098** |
| Bank cash/equivalents opening | 430.614.185 | 430.614.185 | **417.258.692** |
| Bank cash/equivalents closing | **454.996.790** | 417.258.692 | **454.996.790** |

- 6M CFO+CFI+CFF=6M net; cash beginning+net=closing, Q2 sections and cash bridge all zero residual at printed million-VND unit.
- 6M bank CFO original direct subtotal **24.736.707**; do not mistakenly treat interest receipts **50.041.309** as CFO.
- B04 CFI includes investing asset disposal and dividend flows; source is -354.102, not capex only -381.054. Bank vault cash on B02 14.790.170 is NOT B04 cash/equivalents ending 454.996.790; different definitions.
- Q2 half-year original signed source has B03a 6M income and B04a 6M; if independent EY-reviewed H1 later differs in restatement/vintage, store both original and revised without silent overwrite.

## Resume steps, without interruption
1. Run full branch CI and source-proof PASS, merge PR #137 when both statuses successful; read main JSON + audit + checkpoint and confirm 2025Q2 status is issuer signed. Do not claim deploy or website smoke without proof.
2. Continue **VCB Q3 2025** original signed bank consolidated `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/VCB_Baocaotaichinh_Q3_2025_Hopnhat.pdf`. Q3 bank B04 standalone=9M−6M same issuer scope/vintage, with an independent H1 reviewed report as cross-check if possible, not sourced from generic third-party price pages. Pay special attention to revised 2025 H1 signed source 2025-Q2 when comparing B04.
3. After verified, continue sequentially VCB Q4, Q1/Q2/Q3 2026; then next ticker from newest checkpoint. Do not list private queue unless user directly asks for incomplete stock tickers.
