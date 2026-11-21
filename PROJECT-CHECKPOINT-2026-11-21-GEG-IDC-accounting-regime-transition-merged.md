# CHECKPOINT — GEG / IDC Q2/2026 — statutory accounting-regime transition and B03 guard integrated

**Date:** 2026-11-21 (Asia/Ho_Chi_Minh)  
**Production repo:** `kiemtimem12345/solieutaichinh` / `main`  
**PR:** https://github.com/kiemtimem12345/solieutaichinh/pull/114 — **merged**  
**Merge commit:** `208828fcbed967c0baa6c7322da5cad6542af21d`.

## Completed changes
1. Added `config/reporting-regime-rules-2025-2026.json`, which distinguishes (a) fiscal-year accounting applicability, (b) actual effective/signature date, (c) parent vs consolidated scope, (d) specialized industry exceptions, (e) securities disclosure law separately. TT99 begins FY 2026; TT43 is dated/effective 20 April 2026 but applies to consolidated FY starting 1 January 2026 and later; do **not** automatically classify Q1 2026 as pre-TT43 or claim noncompliance based on note wording.
2. Added `scripts/verify_reporting_regime_transitions.py`, which reads verified issuer audit ledgers and both GEG/IDC production financial JSON files, enforces exact VND cash bridges and blocks invented/zero Q2 CFO/CFI/CFF. Sector-specific frameworks must be validated separately.
3. Wired this verifier into `.github/workflows/validate.yml`.
4. Updated `docs/accounting-regime-and-disclosure-transition-sop-2025-2026.md` with implementable metadata and the mandatory cashflow quarterization gate. The new law-to-reports versioning model is reusable for subsequent ticker quarters.

## Financial evidence retained without numeric changes
- **GEG** 2026Q2 consolidated: original Q1 and H1 source B01/B02 and B03 YTD PASS; restricted/pledged deposits of 11,422,218,903 VND were reclassified out of year-opening cash equivalents, original Q1 31 March restricted amount unverified. Provisional H1-Q1 Q2 cash bridge residual **-11,422,218,903 VND**. No legal justification to book noncash classification as operating/investing/financing cash.
- **IDC** 2026Q2 consolidated: original Q1 and reviewed H1 sources PASS; signed H1 Note41 contains 2025 comparison reclassifications, not a signed same-basis 2026Q1 current cashflow restatement. Provisional quarter cash bridge residual **+890,796,892 VND**. Cannot move prior-year comparative entries to 2026 current quarter cashflow.
- For **both**, `data/financials-GEG.json` and `data/financials-IDC.json` signed source figures unchanged; `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow` and other Q2-only cash fields remain NULL; B03 signed H1 YTD remains available. Previously completed 7/7 source periods and Q3 standalone work remain PASS and are not reprocessed.

## Validations on merged code
- PR #114 run https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44875217192 — PASS; new statutory policy/evidence test PASS.
- Main financial validate https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44875263478 — PASS.
- GitHub Pages run https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44875263414 — build and deploy jobs PASS.
- Checkpoint commit is documentation-only and may produce an additional main validation run. No numerical site modifications or new quarter PASS are asserted.

## Next evidence-only action
- **GEG**: signed evidence of March 31 2026 pledged bank deposits and issuer/current-period Q1 2026 restated B03 (or signed same-policy reconciliation) to resolve cash bridge.
- **IDC**: issuer-certified Q1 2026 current-period B03 presented on the H1 TT43 policy or signed line-by-line 2026 current-year mapping plus revised cash position at March31.
- Only upon acquiring evidence: update source hashes/pages in ledger, verify exact VND balance, explicitly modify case tests to reflect same-basis source, then update production financial fields and run CI, web smoke, and checkpoint. Do not re-download already verified originals repeatedly.
