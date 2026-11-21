# CHECKPOINT — VCK/VPS 2026Q1 B01 B02 B03 signed issuer; next Q2/2026 (22/11/2026)

Repository `kiemtimem12345/solieutaichinh`, PR #132. User rule: proceed sequentially without approval; all unresolved cases internal `reports/financial-exception-queue.json`, do not display pending tickers unless user explicitly asks. Prior VCK Q1 2025, Q3 2025, Q4 2025 are signed-source PASS, do not retry. No 2024.

## Original signed source
- VPS VCK signed 10 April 2026 original Vietnamese issuer Q1 report from HOSE/Vietstock ZIP:
`https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/VCK_Baocaotaichinh_Q1_2026.zip`
- ZIP **7,118,356 bytes**, SHA-256 `4529f9f8c8bec23ebc49cf1ba7f66f3e8b9dcb9923f67f46a5989fb2063ef829`.
- Original PDF member `m88_20260413_vi_baocaotaichinh_q1_2026___signed1776053449448l3vklzs6.pdf`, **3,481,834 bytes**, **61 pages**, SHA-256 `0710073b8f6ef2d6ba1268d5831a6627b380b1a5359ff78c72d77fd3753a51d9`. Runner `44934211169` PASSED; artifact `14718867573` holds 24 JPEG preview pages (1-day retention). Original PDF has only 204 searchable chars; data read visually from signed pages.
- B01 company: PDF pp5–7; B02 Q1 current quarter: pp10–13 (portrait original printed sideways); B03 company pp14–15; client custody cash pp8–9. Financial company VCK only, no formally consolidated statement; **do not mix clients' cash** with company assets and CFO.
- Source ledger `reports/source-audits/VCK-2026Q1-issuer-signed-original-vnd.json` has **73 exact source VND fields, 23 independent accounting/cash identities, all 0 VND residual**. `scripts/verify_vck_2026q1_signed_original.py` verifies those and 4 corruption negatives; required in `.github/workflows/validate.yml`.

## Core B01/B02 signed values, VND
| Item | Exact source VND |
|---|---:|
| Total assets 31/03 | 53.217.094.278.047 |
| Liabilities | 23.119.760.683.460 |
| Equity | 30.097.333.594.587 |
| Cash and cash equivalents | 6.162.175.608.883 |
| Q1 operating revenues | 2.519.183.762.365 |
| Q1 operating expenses | 920.091.662.805 |
| Profit before tax | 1.546.916.549.570 |
| Current CIT expense | 311.675.345.556 |
| Net profit | 1.235.241.204.014 |

## B03 quarter (Q1=3M YTD), company VND
- CFO **-6.395.830.382.439**
- CFI **-6.733.321.692**
- CFF **+3.883.748.999.998**
- Net cash movement **-2.518.814.704.133**
- Company cash opening **8.680.990.313.016** (= signed and EY-audited FY2025 cash end)
- Company cash ending **6.162.175.608.883** (= signed Q1 B01 cash)
- Company client-custody deposits **23.299.257.486.855** shown separately outside B01, not in issuer cash.
- Exact B03 residual CFO+CFI+CFF−net = 0 and opening+net−end=0 VND.

## Implementation
- `data/financials-VCK.json`: only row 2026-Q1 normalized, VND source ÷ 1e6 with 6 decimal precision, `cashflow_period_basis=quarter` and YTD stored separately. All Q1/2025, Q3/2025 and Q4/2025 PASS unchanged.
- `scripts/inspect_vck_2026q1_signed_original.py` and workflow `inspect-vck-2026q1-original.yml`: select Vietnamese original ZIP member before EN, source hash/page, 24 early preview images only.
- `scripts/verify_vck_2026q1_signed_original.py`: 23 exact identities and 4 failed-on-corruption controls, attached financial CI.
- PR #132 must pass financial CI before merge; do not claim website deployment until independently checked. After merge re-read main.

## Next automatically
1. Complete PR #132 CI, merge and mark current signed issuer source PASS.
2. **VCK 2026-Q2** signed original PDF `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCK_Baocaotaichinh_Q2_2026.pdf`. Compare H1 6M B03 with signed Q1 3M from source ledger above (same scope, VND signs); verify audit-review vintage before subtracting. Visual source pages B01 B02 B03.
3. **VCK 2026-Q3** signed issuer, then next ticker per main checkpoint. All nonreconciled source rows remain only in private queue; do not list outstanding unless asked.
