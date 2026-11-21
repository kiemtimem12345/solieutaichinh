# CHECKPOINT — VPS/VCK 2025Q2 signed-source evidence queued, continue 2025Q3

**Date:** 2026-11-22 ICT. **Repo:** kiemtimem12345/solieutaichinh. **Processing:** VCK Q1/2025 PASS #128; Q2 evidence retained, qualified source discrepancy in private queue; next **VCK Q3/2025**. No user confirmation required and do not print exception lists unless user asks.

## Source
- VPS securities original Q2 issuer signed as-filed `https://static2.vietstock.vn/data/OTC/2025/BCTC/VN/QUY%202/VPSS_Baocaotaichinh_Q2_2025.pdf`, 39-page PDF dated 18 Jul 2025; signed issuer standalone, *not* similarly ticker-named pesticide-company VPS.
- EY audited 2025 H1 securities issuer report signed 19 Sep 2025, certified appendix `https://cafef1.mediacdn.vn/download/091225/vck-ban-cao-bach-niem-yet-va-cac-phu-luc-cong-ty-co-phan-chung-khoan-vps-9.pdf`. Correct source vintage and audit label; not mistaken for Aug 2025 review copy.
- Original issuer has cash ending 5,153,921,569,830 VND; signed first H1 and audited H1 cash bridge exact. Signed Q2 financial asset 32,138,287,500,860 VND, liabilities 19,337,465,192,969 VND, equity 12,800,822,307,891 VND. Direct Q2 B02 PAT 702,214,269,106 VND. 6M cumulative PAT 1,437,902,026,594 VND; Q1 signed 734,774,225,105 VND. No undocumented plug and no tolerance for 1 VND cash bridge differences.
- Ledger `reports/source-audits/VCK-2025Q2-VPSS-original-and-EY-H1-vintage-vnd.json` contains 45 original signed VND source fields, separate original and EY half-year cashflow, 20 accounting/source checks, and explicit exact vintages.
- Private queue `reports/financial-exception-queue.json` contains queue entry `VCK-2025Q2-signed-vintage-bridge`; entry `queued_not_blocking_other_periods`. **Do not display or list unless explicitly asked.** Do not retry without new issuer evidence.
- VCK Q2 numeric row remains NULL in public financial data until full reconciliation; Q2 source status `issuer_signed_Q2_2025_source_recovered_vintage_exception_queued`. Protected by `scripts/verify_vck_2025q2_vintage_pending_queue.py` with negative controls and mandatory `.github/workflows/validate.yml`.
- Legal scope: VPS divested VPBS Myanmar in Q1 2025, no mandatory consolidated filing since Q1; report as issuer standalone. Broker client cash excluded.

## Resume
1. Verify CI PASS, merge PR. Check main carries ledger + hidden queue without publishing qualified numeric data.
2. **Continue VCK 2025Q3** using issuer-original source ZIP:
`https://static2.vietstock.vn/data/OTC/2025/BCTC/VN/QUY%203/VPSS_Baocaotaichinh_Q3_2025.zip`.
Validate archive magic, pdf member, scope, B01/B02, B03 9M versus EY-audited 6M when comparable; check any reclassification before deriving independent Q3 cash.
3. Continue VCK Q4/2025, Q1–Q3/2026 then next ticker by existing checkpoints, one at a time. VCI 7/7 and VCK Q1 PASS must not be reloaded. Do not import 2024.
