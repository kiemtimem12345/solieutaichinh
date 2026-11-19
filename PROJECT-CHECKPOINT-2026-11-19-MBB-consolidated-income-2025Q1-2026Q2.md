# CHECKPOINT — MBB consolidated income statement 2025-Q1 through 2026-Q2

Date: 2026-11-19 (Asia/Ho_Chi_Minh).  
Scope: **MBB, Báo cáo hợp nhất, Kết quả kinh doanh**, in the original website UI; six quarterly periods `2025-Q1`–`2026-Q2`. **NOT** a declaration that all MBB balance sheet / cash flow metrics or Q3/2026 are completed.

## Done / verified
- Original B03a/TCTD-HN consolidated income-statement PDFs for Q1, Q2, Q3, Q4 2025 and Q1, Q2 2026 were visually inspected on **PDF page 6**. Used **current-quarter actual** column `Số phát sinh trong quý → Năm nay`, **not YTD**.
- `data/financials-MBB.json`: 18 previously absent detailed income-statement fields added to every one of 6 period records, preserving existing verified net profit/pre-tax profit/assets/cashflow fields. Uses **million VND**; site converts to billion VND.
- Income / expense sign preserved: signed interest and service expenses, FX/investment trading losses, provision, current/deferred income taxes. `income_tax` continues as positive magnitude for backward compatibility with existing UI, while original signed current/deferred fields are recorded. Original PDF page and source URL are recorded per quarter.
- 21 bank income fields × 6 periods = **126 validated displayed values**; all 8 accounting identities per quarter have **exactly zero residual** (48/48 PASS), better than allowed 0.01%.
- Dedicated regression test `scripts/verify_mbb_income.py` wired into `.github/workflows/validate.yml`; CI PASS at run `44451766037`.
- Production website smoke test PASS `45/45` URL/SHA256, including new MBB JSON, at run `44451766180`.
- PR #38 merged to `main` commit `dec363d4dd24e0b3a8334dc90f38a0218f2dad67`.
- Keep original frontend and all other tickers untouched; use Git main as source of truth (Hostinger auto Git checkout).

## Primary PDFs
- 2025-Q1: https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/MBB_Baocaotaichinh_Q1_2025_Hopnhat.pdf
- 2025-Q2: https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/MBB_Baocaotaichinh_Q2_2025_Hopnhat.pdf
- 2025-Q3: https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/MBB_Baocaotaichinh_Q3_2025_Hopnhat.pdf
- 2025-Q4: https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/MBB_Baocaotaichinh_Q4_2025_Hopnhat.pdf
- 2026-Q1: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/MBB_Baocaotaichinh_Q1_2026_Hopnhat.pdf
- 2026-Q2: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/MBB_Baocaotaichinh_Q2_2026_Hopnhat.pdf?ver=8b5fd9ba

## Resume point
- Income statement for **MBB 2025-Q1..2026-Q2** is validated and should **not** be reprocessed in the absence of source contradictions. Do not mark all MBB quarters complete until balance/cashflow are separately checked.
- MBB Q3/2026 availability and detailed balance/cashflow remain distinct tasks. For other companies continue source retrieval and normalization at latest saved project checkpoints: PLX → GAS → VDS → GEG → IDC.
- Follow project rules: start 2025-Q1; max 20 periods/ticker; <= 0.01% numeric difference acceptable; checkpoint per verified scope.
