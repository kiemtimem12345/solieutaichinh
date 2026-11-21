# FINAL CHECKPOINT — VIX 2025-Q1 through 2025-Q4 RIÊNG COMPLETE, signed-source verified

Date 2026-11-21 (ICT). Production repo `kiemtimem12345/solieutaichinh`, main.

## Completed periods (do NOT reprocess except future contradictory signed source)
- VIX 2025-Q1 + Q2 RIÊNG, PR #101 B03 original/cash corrected then PR #102 B01/B02 exact VND source and quarterly/YTD P&L: `https://github.com/kiemtimem12345/solieutaichinh/pull/102`, merged `7db3a49dea65789128c78a20b80589c426ff7c81`. All financial QA and site 45/45 successful.
- VIX 2025-Q3 RIÊNG, PR #103: `https://github.com/kiemtimem12345/solieutaichinh/pull/103` merge `5e59eff95778a996fed22d7eee9f0c0749fadd64`; original issuer 44pp SHA `66bafedaede09d88847aa40b7278d559e21adfcd02d51a23fc7735127347f7e9`; 15 identities exact to VND, 9M−H1 signed Q3 standalone cash, wrong VND/triệu unit fixed. Original 43/44 issuer and Vietstock financial pages same pixels, cover p2 differs. Financial postmerge CI `44862834486` PASS, website `44862834490` PASS, Pages `44862833649` PASS.
- VIX 2025-Q4 RIÊNG, PR #104: `https://github.com/kiemtimem12345/solieutaichinh/pull/104` merged main SHA **`ac88da46c1344a9189a94c6ffa0ea081c338935d`**. Original signed issuer 43p 1,743,460 bytes SHA256 `d5a6e87eeac220951bcbe35c5359940092f58e4080d40f94c6bbd2ab99717408`:
  https://vixs.vn/wp-content/uploads/2026/01/20260112-VIX-Baocaotaichinh-Quy-4-2025.pdf
  **17 exact-VND signed-source B01/B02/B03 identities** 0 VND, original 12M−signed 9M quarterly CFO/CFI/CFF and cash bridge exact. Net income Q4 standalone 1,286,710,923,220 VND, assets 34,167,047,236,850, quarter CFO +102,816,912,722, CFI −12,627,320,000, CFF +1,049,000,000,000, net +1,139,189,592,722, opening cash 909,902,606,614 and closing cash 2,049,092,199,336.
  - VIX FY2025 self-prepared amended 10/02/2026: source SHA `74d89731ce8efbb393f5f94a39cec377d9031c8889568a49aaaa8176133e22d8`; corrects its OWN self-filed B01 code312 short term borrowing typo from 1,332,000,000,000 to 11,332,000,000,000; original signed Q4 Jan already 11,332,000,000,000. Do not treat FY self-prepared correction as replacement for Q4 original, or mix audited FY vintage into the Q4 quarterly B03 bridge.
  - FY EPS 3533 VND/share, Q4 standalone EPS blank => null. Brokerage customer cash 3,020,481,537,835 VND is OFF B01, stored under `client_brokerage_cash_off_balance` only.
  - Source ledger `reports/source-audits/VIX-2025Q4-original-B01-B02-B03-exact-vnd.json`; regression `scripts/verify_vix_2025q4_signed_original.py`; original signed recovery `44863016591`.
  - **Postmerge financial CI PASS** `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44863280312`.
  - **Production website read-only 45/45 HTTPS content SHA256 PASS** `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44863280337`.
  - **GitHub Pages build/deploy PASS** `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44863279753`.

## Global rules unchanged
- Only Q1/2025 onward to Q3/2026, at most 20 periods; source VND normalization to triệu VND exact, separate vs consolidated never confused; quarterly B03 via same-source-scope and vintage YTD subtraction.
- Conditional <=0.1% only for independently crosschecked published totals, not for sign, unit, scope, quarter-vs-YTD or top-level cash/accounting identity failures.
- Checkpoint and never recompute completed 2025 VIX quarters unless official contradiction. No invented EPS or off-B01 customer money added to firm B01.
- Do not claim VIX ticker all completed; 2026-Q1, 2026-Q2 and 2026-Q3 VIX reports still `manual_review_required_pending_extraction` and must be processed individually.

## Exact next resume point
**VIX 2026-Q1 RIÊNG original signed issuer statement**, then 2026-Q2 → 2026-Q3 after each financial CI + live website smoke + source checkpoint. Search issuer https://vixs.vn/qhcd/bao-cao-rieng and archived Vietstock documents. Do not reload 2025 Q1–Q4 PASS.
