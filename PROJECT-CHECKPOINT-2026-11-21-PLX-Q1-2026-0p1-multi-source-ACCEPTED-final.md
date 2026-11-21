# PROJECT CHECKPOINT — PLX Q1/2026: PASS_WITH_TOLERANCE 0.1% — 21/11/2026

## Quyết định nghiệm thu
User approved accepting source-reported B01 subtotal values when their detailed component arithmetic differences are <= 0.1% AND the printed subtotal values match multiple additional public financial datasets at each provider's disclosed precision. **The printed values remain unchanged.** B01 component arithmetic is *not* represented as exact; issuer-origin discrepancies are preserved.

- **PLX Q1/2026 hợp nhất, B01: accepted for financial data use with tolerance.**
- B02/B03 remain exact original-source checks PASS. Q1 original cash opening FY2025 comparison reclassification already independently explained by original Note 16.
- No values from another period, scope, or company modified. Historical 0.01% threshold is superseded by conditional 0.1% policy for future eligible discrepancies, not a blanket weakening of accounting identity tests.

## Signed original and cross-checks
Source signed PDF 29/04/2026: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/PLX_Baocaotaichinh_Q1_2026_Hopnhat.pdf
SHA256: 158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f4bc5f9

| Item | Printed VND | Sum of B01 original detail VND | Residual VND | Percent |
|---|---:|---:|---:|---:|
| Code 130 short-term receivables | 19,662,068,640,316 | 19,652,984,670,130 | 9,083,970,186 | 0.046200% |
| Code 310 current liabilities | 76,146,303,967,243 | 76,137,215,001,801 | 9,088,965,442 | 0.011936% |

- Stockbiz https://web.stockbiz.vn/Stocks/PLX/FinancialStatements.aspx, B01 Q1/2026: 19,662,069 and 76,146,304 million VND integer.
- Cophieu68 https://cophieu68.vn/quote/financial_detail.php?hideIC=1&id=plx: same Q1/2026 two values at integer million VND.
- iWinStock https://www.iwinstock.com/stock/PLX/financial-reports/: 19,662.1 and 76,146.3 billion VND to one decimal.
- Values agree at provider display precision; **do not infer exact-VND independent verification from rounded feeds**, nor full independence of their upstream datasets. The B01 signed source sums are still inaccurate by the residuals above; codes 133/317 are not fabricated.
- Full official HOSE PDF binary comparison remains inaccessible in current environment; the previous range HTTP 206 result did not enable complete retrieval. No assertion of HOSE exact matching.

## Implementation and CI
- PR #100: https://github.com/kiemtimem12345/solieutaichinh/pull/100 — **merged** into main.
- Merge commit: `b449241858b4aaa768847271d3c6e11839ff5166`.
- Financial CI after merge: https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44858014326 — **SUCCESS**; includes original 34 exact-VND identities, forensic signed source checks, conditional 0.1% tolerance crosscheck, and synthetic source disagreement/missing-source fail-closed tests.
- Post-merge production HTTPS smoke: https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44858014367 — **SUCCESS 45/45 exact SHA256** (41 JSON plus site assets).
- GitHub Pages build/deploy: https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44858013891 — **SUCCESS**.
- Q1 consolidated `data/financials-PLX.json`: `verification_status=signed_original_B01_B02_B03_Q1_2026_PASS_WITH_TOLERANCE_0p1`; `source_validation.b01_tolerance_status=PASS_WITH_TOLERANCE`, `full_b01_component_arithmetic_passed=false`; `b01_original_subtotal_discrepancies_still_unexplained=true`.
- Cross-source audit snapshot: `reports/source-audits/PLX-2026Q1-B01-cross-source-tolerance.json`.
- Regression: `scripts/verify_plx_q1_2026_b01_tolerance.py`.
- Policy: `reports/validation-tolerance-policy-0p1percent.md`.
- Earlier signed-original ledger, note16 and forensic check preserved, no changes to unrelated ticker periods.

## Next checkpoint
PLX **Q1/2026 consolidated accepted/complete WITH TOLERANCE** as agreed; do not replay it unless issuer publishes an official correction or a contradictory independent source. Stay alert for future Q1 issuer amendments; a tolerance acceptance is not an issuer correction. The previous hard block is lifted **only for this validated reporting item**. Next unresolved PLX item in project queue can be resumed from its own checkpoint, respecting separate parent/combined accounting scope.
