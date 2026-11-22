# CHECKPOINT — VCB issuer signed consolidated 2025 Q3, 9M-minus-6M B04 (22 Nov 2026)

Repository: `kiemtimem12345/solieutaichinh`, PR #138, branch `work/vcb-2025q3-9m-signed-consolidated-20261122`. **Before merging** require newest financial CI and source-proof run PASS; read back main and checkpoint. VCB 2025Q1/Q2 already PASS PRs #136/#137, do not re-read. No 2024-period records. Continue next 2025Q4 signed original, then 2026Q1/Q2/Q3.

## Controlling original source
- Vietcombank consolidated issuer signed **30/10/2025** PDF `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/VCB_Baocaotaichinh_Q3_2025_Hopnhat.pdf`
- Signed scanned PDF **54 pages, 15,527,017 bytes**, SHA-256 **`3afd2b964267c9ec5882fbaec57dabbef2707b40cace4dc0ecdab5b0f52791e7`**, verified in source Actions **44971063344** SUCCESS, artifact **14732904352** contains 32 selected JPEGs, 1-day retention. Original B02a/TCTD-HN balance PDF pp5–6, off-balance p7, B03a/TCTD-HN income pp8–9, B04a/TCTD-HN cash pp10–11. Use original **triệu VND** integers as reported; no guessed 1VND precision.
- Exact ledger `reports/source-audits/VCB-2025Q3-original-signed-consolidated-9M-million-vnd.json`: 136 issuer source million-VND values, 19 core signed accounting equations 0 residual. `scripts/verify_vcb_2025q3_signed_consolidated_9m.py` independently checks source and 24 9M−signed H1 income bridges, four deliberately corrupted data controls, full B04 cash bridge and bank B02 cash vs bank B04 cash distinction. Mandatory `.github/workflows/validate.yml`.
- `data/financials-VCB.json` only Q3/2025 is updated, retaining source million VND precision; signed direct Q3 income column is authoritative. Q3 standalone bank cash from 9M minus already PASS Q2 6M same consolidated scope.

## B02a signed balance 30/09/2025 (triệu VND)
| Item | Value |
|---|---:|
| Assets | **2.378.185.628** |
| Liabilities | 2.155.394.083 |
| Equity | 222.791.545 |
| Vault cash on B02 | 12.909.550 |
| Deposits at State Bank | 56.577.155 |
| Deposits/loans at credit institutions | 497.858.712 |
| Customer loans net | 1.595.933.982 |
| Investment securities | 165.634.799 |
| Customer deposits (bank liabilities) | 1.611.966.698 |

## B03a signed income direct Q3 and 9M (triệu VND)
| Item | Q3 standalone signed | 9M signed |
|---|---:|---:|
| Net interest income | 14.657.240 | 42.504.585 |
| Net service income | 938.335 | 2.605.243 |
| Total operating income | **18.052.128** | 53.185.091 |
| Operating expenses | -6.037.436 | -17.714.605 |
| Pre-provision operating income | 12.014.692 | 35.470.486 |
| Credit provision | -775.587 | -2.337.533 |
| Profit before tax | 11.239.105 | 33.132.953 |
| Corporate tax total | 2.213.552 | 6.568.303 |
| Consolidated PAT | **9.025.553** | 26.564.650 |
| PAT attributable parent | 9.020.499 | 26.548.613 |

The Q3 signed direct income agrees 9M−signed source H1 Q2 for **22 of 24 source lines exactly**. Two gross interest lines offset perfectly: income (9M−H1−direct Q3) **-6,904 million**; interest expense **+6,904 million**. Net interest and all earnings subtotals/profit/tax remain exact. Each gross-line deviation under latest **0.1%** user tolerance, preserved without source plug. Details hidden in internal `reports/financial-exception-queue.json` entry `VCB-2025Q3-gross-interest-9M-minus-H1-vintage-6904m`. Do **NOT** show pending list unless asked.

## Bank B04a corporate cash 9M and Q3 standalone (triệu VND)
| Flow | Signed 9M | Signed 6M | Standalone Q3=9M−6M |
|---|---:|---:|---:|
| CFO | +106.283.289 | +24.736.707 | **+81.546.582** |
| CFI | -718.369 | -354.102 | **-364.267** |
| CFF | 0 | 0 | **0** |
| Net cash change | +105.564.920 | +24.382.605 | **+81.182.315** |
| Cash/equivalents opening | 430.614.185 | 430.614.185 | **454.996.790** |
| Cash/equivalents ending | 536.179.105 | 454.996.790 | **536.179.105** |

9M CFO+CFI+CFF=net, opening+net=ending, Q3 CFO+CFI+CFF=Q3 net, Q3 opening+net=ending, residual 0 million VND. The original 9M bank gross cash interest receipts is +76.029.283 million but **CFO is +106.283.289 million**, don't confuse them. Bank B04 cash/equiv 536.179.105 differs from B02 vault cash 12.909.550 million.

## Next
1. Check latest PR #138 CI success; merge only then, read main `data/financials-VCB.json` and checkpoint verify. Do not claim website deployment unless separately validated.
2. Continue VCB 2025Q4 original `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/VCB_Baocaotaichinh_Q4_2025_Hopnhat.pdf`, audited FY2025 for a second vintage, Q4 B04=FY2025 12M−signed 9M, if compatible. Do not reprocess earlier source-verified Q1–Q3.
3. Continue Q1/Q2/Q3 2026 VCB sequentially then next ticker in newest approved checkpoint. Internal exception queue hidden, no questions, no 2024 row, at most 20 most recent 2025+ periods, no invented zeros/negative signs.
