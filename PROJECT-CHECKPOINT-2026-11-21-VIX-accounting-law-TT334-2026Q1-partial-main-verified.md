# FINAL CHECKPOINT — chuẩn mực kế toán + pháp luật áp dụng, VIX 2026Q1 partially verified (21/11/2026)

## Confirmed production state
Main repository `kiemtimem12345/solieutaichinh`.
- **PR #105**: https://github.com/kiemtimem12345/solieutaichinh/pull/105 — merged commit `deae9190737f9dea495abe1103cd294d54c4cc3f`. Adds accounting/legal source rules, VAS and CTCK special regime policy, five negative tests and CI gate. All prior VIX 2025 Q1-Q4 signed-source checks stay PASS. PLX 2026Q1 has only original, previously cross-sourced **PASS_WITH_TOLERANCE 0.1%** for two known subtotal exceptions, not exact component arithmetic. Main CI `44864386046` and Pages `44864385708` SUCCESS.
- **PR #106**: https://github.com/kiemtimem12345/solieutaichinh/pull/106 — merged commit **`fd7f4b1fdaa2e7557fc894482830bc08c9e8d464`**. VIX Q1/2026 source-specific CTCK form and exact signed main B01/B02/B03 totals. Main financial CI `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44864825135` SUCCESS; production HTTPS 45/45 exact content SHA-256 `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44864825133` SUCCESS; GitHub Pages `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44864825014` SUCCESS.

## Legal/source precedence
- Luật Kế toán 88/2015/QH13 (as amended); VAS 01, VAS 21, VAS 24; for interim reports VAS 27.
- VIX is a securities company: TT210/2014/TT-BTC and TT334/2016/TT-BTC specialized CTCK form (B01, B02, B03b, B09). Confirmed by **issuer's actual Q1/2026 filing and notes §2.1**, not inferred from generic forms.
- TT99/2025/TT-BTC is broadly effective for financial years beginning from 01/01/2026, but it is NOT used as a reason to replace a CTCK's issuer-signed specialized form blindly; specific 2026 policies must be checked case-by-case. Luật Doanh nghiệp 59/2020, amended 76/2025; TT96/2020 securities disclosure as amended 68/2024, 18/2025. These require separate supporting evidence for timeliness, auditor, corporate decision-making. **Automated arithmetic QA is not an opinion on legal compliance.**
- Tolerance <=0.1% allowed only for original subtotal arithmetic discrepancies matched to at least 2 outside sources at display precision. No tolerance for unit/sign/scope/classification/YTD version mistakes, essential B01 balance and B03 cash.

## VIX 2026Q1 issuer signed source — partial, source and legal-form confirmed
Original official source: https://vixs.vn/wp-content/uploads/2026/04/20260417-VIX-BAO-CAO-TAI-CHINH-QUY-I-2026.pdf, dated **17/04/2026**, CTCK separate form.
- B01: assets 29,598,210,995,041; liabilities 8,005,077,648,346; equity 21,593,133,346,695; source balance 0 VND. B01 cash 970,994,021,164.
- B02: pretax 156,353,886,858; current tax +44,096,616,869; deferred tax **-26,112,999,066**; total tax 17,983,617,803; net profit 138,370,269,055. Original all 0 VND arithmetic difference.
- B03b: CFO **+3,243,431,300,446**; CFI -529,478,618; CFF -4,321,000,000,000; net cash -1,078,098,178,172; opening cash **2,049,092,199,336** equals previously signed/verified **VIX 2025Q4 ending cash**; closing cash 970,994,021,164 equals B01 and Note 5; all 0 VND difference.
- Previous VIX Q1/2026 stale `operating_cash_flow=156354` million was an incorrect proxy for PBT, fixed to signed +3,243,431,300,446 VND; all updated fields stored in million VND exactly.
- Source ledger: `reports/source-audits/VIX-2026Q1-issuer-TT334-legal-form-and-headline-vnd.json`, specific regression `scripts/verify_vix_2026q1_issuer_tt334_core.py`; legal policy and framework `reports/accounting-legal-validation-framework.json`, `reports/accounting-legal-crosscheck-policy-2026-11-21.md` and automated `scripts/verify_accounting_legal_framework.py`.
- **NOT full financial PASS**: `verification_status=issuer_signed_2026Q1_partial_core_B01_B02_B03_verified_FULL_DETAIL_PENDING`; complete binary SHA-256 issuer PDF is still unavailable and full B01/B02/B03 component-level checks not finished. EPS source Q1 standalone cell blank, EPS YTD 90; do not invent quarter EPS. No legal certification is asserted.

## Resume point, no duplicate work
1. Recover COMPLETE VIX issuer Q1/2026 PDF bytes (full SHA256) and check each B01/B02/B03 signed row vs financials, client cash off-B01 and 2025 comparatives/notes. Reject wrong units/sign/period and do not auto-upgrade on tolerance.
2. Only after detailed source and CI/web validations pass: mark VIX 2026-Q1 separate FULL PASS and checkpoint.
3. Continue VIX 2026-Q2 then Q3; **VIX 2025Q1–Q4 already complete, must not be reprocessed**.
