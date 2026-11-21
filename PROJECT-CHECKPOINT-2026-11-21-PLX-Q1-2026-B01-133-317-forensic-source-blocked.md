# CHECKPOINT — PLX consolidated B01 Q1/2026, 2026-11-21, source-origin forensic verification

**Do not mark B01 fully complete. Do not move to another ticker/period until B01 full arithmetic PASS or issuer's signed correction is documented and verified.** This is a source anomaly, not a remaining coding or OCR arithmetic correction. Prior verified data must not be reprocessed.

## Source provenance
- Signed issuer original (29/04/2026) 36p, 7,990,499 bytes; SHA256 158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f4bc5f9:
  https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/PLX_Baocaotaichinh_Q1_2026_Hopnhat.pdf
- B01 signed PDF pages 2–3 (1-based) visually inspected. Codes 133 and 317 are **not printed** in the consolidated B01, and their value cannot be deduced. There are no cells claiming a 9-billion value. The absence of the row cannot be treated as a verified zero, nor as proof the missing residual belongs to that row.
- Notes signed PDF page 20: Note 3 customer receivables = 19,245,177,718,970 VND incl. 275,000,000 VND long-term; current 19,244,902,718,970 VND exactly agrees with B01 code 131. Note 4 other current receivables 893,190,840,519 agrees with B01 code 135; note 5 assets awaiting treatment 1,429,637,192 agrees with code 137.
- Notes PDF pages 21–22: note 18 supplier payables 58,702,436,241,952 = code 311; note 21 accrued 652,922,698,316 = code 316; note 22 other payable 935,848,354,785 = code 320; note 23 unearned 13,603,182,893 = code 319; note 26 provision 276,453,109,103 = code 322.
- FY2025 audited comparative cash / Q1 opening price stabilization deposit Note16 correction already resolved in PR #98; do not reopen or allocate any of that cash reclassification to Q1 cashflows.

## Two signed B01 printed-subtotal discrepancies (Q1 current end)
1) B01 code 130 printed **19,662,068,640,316 VND** but sum of code 131,132,135,136,137 displayed detail is **19,652,984,670,130 VND**, residual **+9,083,970,186 VND**, 0.04620% (>0.01%).
2) B01 code 310 printed **76,146,303,967,243 VND** but sum of code 311,312,313,314,315,316,319,320,321,322,323,324 displayed detail is **76,137,215,001,801 VND**, residual **+9,088,965,442 VND**, 0.01194% (>0.01%).
3) Differences differ **4,995,256 VND**; do not assume a symmetric internal receivable/payable elimination.

## Original comparative opening column Q1/2026 confirms no error at opening
- 01/01/2026 code 130 printed **15,969,900,845,614 VND**, matches visible detailed codes 131/132/135/136/137 exactly, residual **0 VND**.
- 01/01/2026 code 310 printed **55,354,328,118,906 VND**, matches 12 visibly printed codes 311/312/313/314/315/316/319/320/321/322/323/324 exactly, residual **0 VND**.
- Therefore mismatch is only in 31/03/2026 end column, not general parser sign/unit rules.

## Secondary source / amendment investigation
- Checked issuer website IR listing, 2026 HOSE disclosure references and major report aggregators. Located Q1 as-filed disclosure and Q1 profit variance explanation, but no *verified official signed Q1 B01 revised amount/erratum* explaining either ~9-billion difference in accessible results. This is a **limited-source finding**, not proof there can be no issuer amendment anywhere.
- B01 overall assets=liabilities+equity and 34 existing exact VND identities from Q1 original remain untouched. Q2 2026 original 41 checks PASS already; Q2 is another reporting date and cannot cure original Q1 mismatch.

## Code/CI changes
- Added original 01/01/2026 printed detail ledger and independent source-notes values in `reports/source-audits/PLX-2026Q1-consolidated-signed-original-vnd.txt` under B01_FORENSIC_OPENING_AND_SIGNED_NOTES; original 82 financial values and 55 existing closing B01 details untouched.
- Added `scripts/verify_plx_q1_2026_b01_forensic.py`: verifies opening sums, notes crosschecks, end residuals >0.01%, independent note3 current/long split, no fictional 133/317, and fail-closed status against false financial approval.
- Added mandatory verification step in `.github/workflows/validate.yml`.
- Added forensic source metadata and status to Q1 record inside `data/financials-PLX.json`. No top-level numerical values changed, other periods untouched.
- **PASS from GitHub CI means forensic guard passed, not full B01 PASS**. Only upgrade to financially complete when exact source-correction evidence/verified subtotal arithmetic meets 0.01%, together with full CI, site check and checkpoint.

## Resume point
Seek signed official company/HOSE corrected Q1/2026 consolidated B01, detailed ledger/appendix explicitly accounting for codes 133/317 or authoritative reconciliation. If none, retain source report printed amounts, evidence, and **BLOCKED**. Do not manufacture numbers, move to other items, or mark Q1 financially complete.
