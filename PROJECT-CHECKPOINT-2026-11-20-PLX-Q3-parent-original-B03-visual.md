# CHECKPOINT — PLX Q3/2026 công ty mẹ: xác minh trực quan bất nhất B03, 20/11/2026

## Continuation anchor
- Repo `kiemtimem12345/solieutaichinh`, production branch `main` base `86049d287ca98ef47bbe80d0c272f3e064aeba52` (IDC 2026 H1 TT99 Note41 PR #85 merged, live website 45/45 PASS run 44583682247).
- PLX Q3/2026 parent B01/B02 numeric PDF-text verification from earlier PR #42; original parent B03 still blocked for CFF difference 87,654,015,000 VND. User requested continue and diagnose; do NOT process already-PASS IDC.

## Exact authentic PLX parent Q3 source retrieved
- Official Petrolimex source:
  https://files.petrolimex.com.vn/files/6783dc1271ff449e95b74a9520964169/application%3Dpdf/5011693c3c5240a0833bfaea0e7983a5/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20m%E1%BA%B9%20Q3%20nam%202026.pdf
- Successfully downloaded by GitHub Action `44584975199` before other HOSE source requests stalled and its 9-minute timeout cancelled workflow.
- Exact signed PDF **39 pages**, **14,198,075 bytes**, SHA256 **`a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef`**.
- Original PDF and 19 page images persisted as GH Actions artifact **`14559633962`**, downloaded and visually inspected: PDF pages **2-5 B01**, **6 B02**, **7-8 B03** (signed page 8).
- Prior B01/B02 numeric values confirmed visually on original: total assets **73,735,716,400,522**, liabilities **49,645,102,958,279**, equity **24,090,613,442,243** VND, Q3 parent net revenue **84,352,714,995,460**, PAT **1,315,029,909,162** VND. Existing arithmetic exact-VND PASS, and original page signatures visible; do not redo remaining 31 proven fields.

## Proven signed-original B03 financing subtotal contradiction
- On signed original PDF pages 7–8, line 31 issuance/owner capital **+844,158,780,900** VND; line 32 owner capital returned **-1,134,759,693**; line 33 loans received **+71,733,162,995,138**; line 34 principal repayment **-65,128,441,186,058**; line 35 lease repayment **0**; line 36 dividends **-1,393,990,271,569**.
- Sum of lines 31–36 **+6,053,755,558,718 VND**, but **source-printed line 40 CFF +5,966,101,543,718 VND**. Difference **+87,654,015,000 VND**.
- Original CFO line 20 **-3,435,516,597,061**, CFI line 30 **-2,575,747,123,895**, net cash line 50 **+42,491,837,762** VND.
- CFO+CFI+sum(CFF components) = **+42,491,837,762** (exactly equals signed source line 50). CFO+CFI+printed line40 = **-45,162,177,238**, unequal to original line50 by **-87,654,015,000**.
- **Source was read from original PDF signed pages, not OCR**, so the numeric inconsistency is **on the disclosed original**. Do not call this a verified financial restatement or assume which source value issuer intended. No issuer correction explaining it was located in official searches on 20/11/2026.
- Full B03 validation remains **BLOCKED** and quarter-only cashflow values are **NOT added to production**. Original printed CFF must be preserved separately from computed row sum with metadata identifying both, original PDF SHA/page.
- `data/financials-PLX.json` Q3 parent now includes exact original source hash, visual pages and detailed anomaly proof; `full_b01_b02_b03_visual_reviewed=false` intentionally, as a fully verified cash-flow section must reconcile to original source or signed issuer correction.

## CI / deployment and next actions
- PR #86: https://github.com/kiemtimem12345/solieutaichinh/pull/86 .
- Read-only retriever `scripts/recover_plx_q3_2026_original_sources.py` now fetches only original PLX Q3 parent to avoid serial HOSE download timeouts; workflow `.github/workflows/recover-plx-q3-2026-original-sources.yml`. Dedicated numeric assertions extended `scripts/verify_plx_issuer_q3.py`, plus source metadata in `data/financials-PLX.json`.
- Before merge require both validation and isolated source recovery successful, then verify production 45/45 URL+SHA. Do not change website layout.
- **Next PLX**: retrieve **parent H1/2026 reviewed** same scope from official HOSE `https://staticfile.hsx.vn/Uploads/UploadDocuments/2493840/20260828%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20me%206%20thang%20nam%202026%20sau%20soat%20xet.pdf` in independent bounded source job; search for a signed issuer correction of Q3 parent B03 CFF before publishing Q3 cash. Also retrieve separate **consolidated Q3/2026** original, not same as parent. Do not use subsidiary PLC/PJT financial statements as PLX source.
- If corrected source remains unavailable, preserve blocker and move to next processable GAS/VDS/GEG source according to audit. 2025-Q1 onwards, at most 20 periods/mã, exact VND arithmetic, <=0.01% tolerance, no invented numbers and source scope identity.
