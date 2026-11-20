# CHECKPOINT — PLX Q1/2025 consolidated issuer original signed B01/B02/B03, 20/11/2026

## Project and latest safe restore
- Production repo `kiemtimem12345/solieutaichinh`; main starting point **`81022c51c63faab8dc044740fca9cca271d8e7df`** after PR #90, postmerge site 45/45 HTTPS SHA256 PASS run `44677039798`.
- This branch processes **PLX consolidated 2025-Q1 only**, following latest saved source audit. GAS, VDS, GEG, IDC previously PASS periods untouched; PLX consolidated Q3/2026 and parent Q3/2026 unchanged. Parent Q3 issuer B03 printed CFF contradiction **87,654,015,000 VND** remains quarantined. No request to redo other periods.
- Previous PLX 2025-Q1 data had rounded million-VND and fields `partially_verified_from_archived_source_text`, explicit manual visual pending. Existing raw archive `reports/raw/PLX/auto-plx-20261021/8ebe33f1a2757507.pdf` SHA prefix matches new original signed source, independently re-downloaded.

## Signed original complete source, not OCR
- Vietstock original document catalogue `https://finance.vietstock.vn/PLX/tai-tai-lieu.htm?doctype=1`, document ID **504658**; original PDF exact:
  `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/PLX_Baocaotaichinh_Q1_2025_Hopnhat.pdf`
- Recovery script `scripts/recover_plx_q1_2025_consolidated_original.py`, GitHub Actions run **`44678708402`** succeeded, artifact **`14603706432`**.
- Issuer original **53 PDF pages, 1,050,763 bytes, SHA256 `8ebe33f1a2757507aa2db8421fa261a93d6a765a0de9e2e5aee60b1a56460b97`**. Signed by Petrolimex CEO on 29 Apr 2025, public source linked. PDF has original selectable text and signature/stamp images, no OCR approximations needed.
- B01 PDF pages **2–5**, B02 pages **6–7**, B03 pages **8–10** have been **visually inspected from original images** and corroborated with original text. Source explicitly shows consolidated B01/B02/B03, currency VND; do not mistake parent source or 2024 comparative.

## Original financial data checked in VND, unrounded
- B01 31/03/2025: assets **80,035,874,441,574**, current assets 58,986,937,922,224, noncurrent assets 21,048,936,519,350; liabilities **50,515,699,095,191**, equity **29,520,175,346,383**, cash+equivalents **10,446,733,576,792**.
- Original B01 opening 01/01/2025 assets **81,274,634,873,472**, equity **29,307,974,443,473**. Correct Q1 ROA annualized from exact source opening + closing and quarter net PAT **1.05%** (old stored 1.04 from mismatched/rounded opening); ROE **2.87%**.
- B02 standalone Q1 = 3M YTD: gross sales **67,890,171,339,647**, deductions 29,140,851,991, net revenue **67,861,030,487,656**, COGS **64,149,128,072,879**, gross profit **3,711,902,414,777**, operating profit 337,522,026,628, pretax profit **358,383,651,559**, tax **147,614,851,020**, PAT **210,768,800,539**, parent-attributable PAT **133,414,809,920**, noncontrolling PAT 77,353,990,619, EPS **86 VND/share**.
- B03 Q1 signed 3M: CFO **-2,549,784,370,445**, CFI **-4,577,483,497,115**, CFF **+2,647,070,139,831**, net **-4,480,197,727,729**, opening cash **14,933,068,792,315**, FX **-6,137,487,794**, closing cash **10,446,733,576,792** VND; quarter Q1 equals YTD. Signed B03 detail component CFO (before WC, interest, taxes), CFI (capex and investments), CFF (borrowings and dividend) sums all reconcile exactly; B03 ending cash equals B01 cash exactly.
- **96 exact source VND monetary fields** normalized to **triệu VND** without early rounding and EPS separately. `data/financials-PLX.json` `2025-Q1` upgraded to issuer original visual PASS with 40 source-exact VND checks (all difference **0 VND**). `financial_line_items_extracted_fields` and `...manually_verified_fields` updated, original SHA/pages/recovery run embedded. Never modify other PLX periods in this PR.
- `scripts/verify_plx_q1_2025_original.py` independently checks 40 original VND identities from numeric fields (not just trusting metadata), selected signed source exact amounts, signed original PDF hash, Q1 quarter-vs-YTD, EPS & ROA, and asserts 2026Q3 parent source B03 blocked.
- `.github/workflows/validate.yml` updated with Q1 test. Before merge demand financial CI PASS; after merge demand production `45/45` SHA256 HTTP and pages deployment. If CI reports a discrepancy, fix test/data only from source before merge.

## Next task after PR
- Next unverified **PLX 2025-Q2 consolidated B01/B02/B03**, older row `manually_visual_verified_user_image` applies only B02 user image p5; B01 and B03 source needed. Preserve B02 already verified, recover issuer original complete PDF and compare same-scope H1 YTD B03 minus this newly signed Q1, run exact-VND identity checks. Do not treat old Q2 rounded/partially mismatched cashflows as PASS.
- Later PLX Q3–Q4 2025 and Q1–Q2 2026 one period at a time. Checkpoint after each verified period. Q3 2026 parent CFF remains blocked absent correction.
