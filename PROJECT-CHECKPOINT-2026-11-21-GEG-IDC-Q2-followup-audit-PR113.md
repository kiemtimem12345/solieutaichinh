# Checkpoint — 2026-11-21 GEG / IDC Q2 consolidated standalone B03 follow-up (PR #113)

## Repo and scope
- Active production repo: `kiemtimem12345/solieutaichinh`, `main`. This checkpoint belongs to PR #113 branch `audit-geg-idc-2026q2-policy-20261121`, NOT yet merged.
- In-scope 2025-Q1 through 2026-Q3. GEG and IDC each have 7/7 original consolidated period/source files with B01/B02 and B03 current YTD verified; Q3 standalone B03 already PASS. Do not redo signed-source arithmetic.
- Only open gates are the 2026-Q2 quarter-only B03 CFO/CFI/CFF and cash bridge of GEG and IDC; both remain NULL in production. Other ticker data untouched.

## 1. GEG 2026-Q2
- Signed Q1 consolidated source: `https://static2.vietstock.vn/vietstock/2026/4/29/20260429___geg___bao_cao_tai_chinh_hop_nhat_q1_2026___giai_trinh__song_ngu_.pdf`.
- Signed Q2 consolidated source: `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/GEG_Baocaotaichinh_Q2_2026_Hopnhat.pdf`.
- Verified original note11 Q2 source PDF p24: 11,422,218,903 VND pledged deposits year-open, 54,079,653,068 VND at June 30. Year-open B01 code112 decrease precisely 11,422,218,903 VND, other current assets code165 increase same, current assets unchanged.
- Re-checked Q1 public PDF indexed body as of 2026-11-21: Q1 notes cash 105,856,793,049 at March31 (cash bank 46,625,510,309; cash equivalents 59,231,282,740); Q1 short-term fixed deposits 288,087,676,704 under 6–12mo; Q1 B01 code160 65,558,815,530 at March31, not a separately stated guarantee deposit balance. Q2 pledged deposit line does not establish how much remained restricted March31, and Q1 signed Q1 B03 version was not re-presented.
- Provisional H1-Q1 Q2 B03 residual against Q1 end and H1 end cash remains -11,422,218,903 VND. Do not assume this exact opening-balance reclassification was unchanged at March31. Do not publish provisional Q2 quarter figures.
- Source evidence: `reports/source-audits/GEG-2026Q2-note11-pledged-cash-opening-reclassification-vnd.json`, existing fail-closed regression `scripts/verify_geg_q2_2026_pledged_deposit_note11.py`.

## 2. IDC 2026-Q2
- Signed Q1 consolidated source `https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%201/IDC_Baocaotaichinh_Q1_2026_Hopnhat.pdf`, Q1 original policy note2.5 TT99/2025.
- Reviewed H1 consolidated `https://www.bsc.com.vn/News/NewsAttachedFile/1599258-1`, signed original B09a note3.1 applies TT43/2026 and note41 changes previous-period 2025 B03 comparatives. No signed restated current 2026 Q1 B03 under TT43 found in targeted issuer/HNX search this turn.
- Opening cash discrepancy +890,796,892 VND persists. 2025 comparative reclasses cannot be added to current 2026 CFO/CFI/CFF. Q2 quarter B03 fields must remain NULL.
- Existing source audit `reports/source-audits/IDC-2026Q1-vs-H1-TT43-source-policy-and-Note41-B03-comparatives.json`, fail-closed regression `scripts/verify_idc_q2_2026_tt43_signed_current_period_vintage.py`.

## 3. Improvement in PR #113
- Changed ONLY `scripts/audit_all_statement_coverage.py`: adds an explicit GEG/IDC Q2 quarter-only B03 missing-data table and fails the audit if a report now shows a complete Q2 B03 without exception re-review.
- Corrected obsolete 0.01% report-policy text to the newly approved up-to-0.1% **only for independently corroborated small subtotals**, never for scope/version, sign/unit/period, or cash bridge.
- PR: `https://github.com/kiemtimem12345/solieutaichinh/pull/113`, branch commit before this checkpoint `134989e3de5db791a01554d728ef3e3f15308ab9`.
- As of checkpoint creation, PR CI did NOT return a new run; no CI PASS claim, no merge or production deployment. Main remains unchanged.
- Next: await/inspect GitHub financial validation run for PR #113; merge only on PASS and postmerge verify. Reopen GEG/IDC Q2 B03 only upon new signed same-vintage quarter source evidence.
