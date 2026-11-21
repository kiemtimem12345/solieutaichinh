# CHECKPOINT — PLX 2026-Q1 B01: conditional acceptance at 0.1% after 3 cross-source matches

Date: 2026-11-21 ICT. Source PDF signed 2026-04-29 (consolidated), exact original 36-page SHA256 `158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f4bc5f9`. Historical PRs #96/#98/#99 remain authoritative for exact source, signed notes and forensic checks. No source numbers rewritten.

**Change of acceptance rule at user's direction:** Previously 0.01%; now numerical subtotal discrepancies **<=0.1%** can be accepted only when the signed original is validated and additional public-source totals match at the **published display precision**. Any disagreement at displayed precision, wrong reporting scope/period/sign/unit, or violation of top-level B01/B03 identities remains a blocker. A passed tolerance check is not a claim of exact signed-source component arithmetic.

## Exact original issuer amounts (VND)

| B01 item | Signed original printed | Sum of visible original detail | Difference | Difference / printed |
|---|---:|---:|---:|---:|
| Code 130 short-term receivables | 19,662,068,640,316 | 19,652,984,670,130 | +9,083,970,186 | 0.046200% |
| Code 310 current liabilities | 76,146,303,967,243 | 76,137,215,001,801 | +9,088,965,442 | 0.011936% |

Both source subtotal mismatches remain physically present in issuer original, and 133/317 are not printed. No phantom numerical line is created. The source financial data retain 34 independent exact-VND identities and total assets = liabilities + equity 0 residual; cash opening (FY2025 audited to Q1) was previously explained by signed Note 16, never part of Q1 CFO/CFI/CFF.

## Independent public display comparisons (all consistent at published precision)

- Signed issuer PDF primary source, original VND: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/PLX_Baocaotaichinh_Q1_2026_Hopnhat.pdf
- Stockbiz https://web.stockbiz.vn/Stocks/PLX/FinancialStatements.aspx; correct consolidated Q1/2026 column, displayed units **million VND integer**: code 130 19,662,069; code 310 76,146,304.
- Cophieu68 https://cophieu68.vn/quote/financial_detail.php?hideIC=1&id=plx; Q1/2026 second column, **million VND integer**: 19,662,069; 76,146,304.
- iWinStock https://www.iwinstock.com/stock/PLX/financial-reports/; Q1/2026 third column, **billion VND to one decimal**: 19,662.1 and 76,146.3.
- Rounded values from issuer exact originals agree with all 3 provider displays. **Do not claim those platforms establish exact VND accuracy**; sources may share upstream records.
- Official HOSE direct source https://staticfile.hsx.vn/Uploads/UploadDocuments/2459340/20260504%20-%20PLX%20-%20BCTC%20hop%20nhat%20Quy%201%20nam%202026.pdf is still not fully downloaded. 206 HTTP partial 64 KB worked; 2 MB range calls timed out; do not claim full HOSE-vs-Vietstock SHA equality.
- No signed issuer erratum resolving 130/310 proven. These remain **issuer-original subcomponent arithmetic exceptions**, but acceptable for data USE under user's new 0.1% policy after matching three secondary public displays.

## Code changes and exact test gate

- New `reports/source-audits/PLX-2026Q1-B01-cross-source-tolerance.json` stores source URL, period, scope, displayed units, published amounts, residuals, caveats.
- `reports/validation-tolerance-policy-0p1percent.md` documents conditions, exceptions and future-ticker policy.
- `scripts/verify_plx_q1_2026_b01_tolerance.py` verifies original exact source values, same-period comparison, display rounding (Decimal), both residual percentages, three named secondary platforms, and negative tests (tampered total or missing sources).
- Existing `scripts/verify_plx_q1_2026_b01_forensic.py` still verifies original arithmetic mismatch and notes but now enforces the 0.1% boundary instead of previous 0.01%; impossible to mark source component arithmetic exact.
- `scripts/verify_plx_q1_2026_original.py` still protects 34 exact identities, original VND and cash reclassification; `.github/workflows/validate.yml` includes the added tolerance verification.
- `data/financials-PLX.json` changes only the Q1 consolidated verification status, tolerance metadata, reviewed status and source flags; 82 original VND fields, 55 B01 detail fields and other periods untouched.

## Meaning of status

`PASS_WITH_TOLERANCE` = **usable for published B01 subtotal values**, after the source-consistency gate. `full_b01_component_arithmetic_passed=false` = **the issuer-signed subtotal discrepancy still has no exact correction**. Both statements must remain true; do not mask historical exceptions.

## Checkpoint and gate

This document is created on a feature branch as an implementation record; do NOT infer final merge/CI/production success from this checkpoint alone. Before declaring the PLX Q1/2026 period completed **WITH TOLERANCE**, require (1) PR financial validation CI PASS, including old tests and new tamper-negative-tests; (2) merge; (3) main validation PASS; (4) production read-only smoke test and deploy verification. Save the final commit SHA and checkpoint. Do not reprocess older passing periods or unrelated tickers.
