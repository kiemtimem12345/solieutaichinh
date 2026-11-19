# CHECKPOINT — GEG hợp nhất Q1/2026 đã xác minh; Q2/2026 nguồn tiền đầu năm bất nhất (19/11/2026)

## Điểm tiếp tục và các kỳ đã hoàn tất
- VDS **7/7 kỳ hợp nhất từ Q1/2025 đến Q3/2026** đã xác minh gốc B01/B02/B03, không làm lại. VDS H1/2025 phân bổ lợi nhuận công ty mẹ/NCI lệch **1,117,693,283 VND** đã chứng minh trên 3 phiên bản, lưu ngoại lệ PR #67 merge `aadd57d6a28fc8c377eb999b23a80b6c9bee8b2a`.
- GEG **Q3/2026 công ty mẹ và hợp nhất** đã PASS gốc, không làm lại.
- GEG **Q2/2026 hợp nhất** original B01 B02 B03 6M from signed PDF Vietstock mirror, 101 trường, 31 exact-VND source checks, PR #69 merge `0da1635d0c846b45208f5cc35a64d71f25880bd0`, CI PASS and website smoke 45/45 PASS run `44522371752`. Postmerge checkpoint commit `4c8cda9e6cbd4186adffc1208430d469ccd15c1d`.
- This checkpoint adds **GEG consolidated Q1/2026** source-verification and records **significant cross-vintage cash opening difference** blocking Q2 standalone B03. Follow source integrity; do not guess, do not overwrite signed Q1/Q2.

## Q1/2026 original signed issuer evidence
- HOSE official disclosure (PDF server sometimes timeout): https://staticfile.hsx.vn/Uploads/UploadDocuments/2458785/20260429%20-%20GEG%20-%20Bao%20cao%20tai%20chinh%20hop%20nhat%20Q1.2026%20%2B%20giai%20trinh%20%28song%20ngu%29.pdf
- Signed GEG original bilingual 82-page PDF mirror (published 29/04/2026): https://static2.vietstock.vn/vietstock/2026/4/29/20260429___geg___bao_cao_tai_chinh_hop_nhat_q1_2026___giai_trinh__song_ngu_.pdf
- SHA256 original **`d8dade2f270452432a190bedddb46736523cc3a74b783ae1a2f82b76a5e74d5b`**, 4,082,692 bytes, signature dated **24/04/2026**. GitHub Actions run `44523692326` PASS with `SOURCE_OK VIETSTOCK_PUBLISHED` and `PDF_OK total_pages=82`; artifact `14529945476`, screenshots directly reviewed: PDF **p6 B01 assets**, **p7 B01 debt/equity**, **p8 B02**, **p9–10 B03 3M**. Uses consolidated B01-DN/HN not parent B01a-DN, original source VND, JSON million VND, EPS VND/share.
- Original GEG first-release Q1 was recorded according to TT43 and notes. No OCR-only figures marked verified.

## Original Q1 B01/B02/B03 source values
| Source original signed (VND) | Q1/2026 |
|---|---:|
| B01 assets at 31/03/2026 | **15,135,066,404,510** |
| Liabilities | 8,374,006,488,064 |
| Equity | 6,761,059,916,446 |
| Cash & equivalents ending (B01/B03) | 105,856,793,049 |
| B02 revenue standalone Q1 | **767,379,199,934** |
| Cost of goods sold | 280,414,635,779 |
| Gross profit | 486,964,564,155 |
| Pre-tax profit | 286,415,279,000 |
| Current corporate income tax | +23,323,328,690 |
| Deferred tax | -562,023,086 |
| After-tax net consolidated | **263,653,973,396** |
| After-tax parent owners | 206,675,501,563 |
| Non-controlling owner share | 56,978,471,833 |
| EPS basic / diluted | **577 / 550 VND/cp** |
| 3M B03 CFO | **+213,327,143,465** |
| 3M B03 CFI | **-26,739,175,041** |
| 3M B03 CFF | **-167,121,630,611** |
| 3M B03 cash movement | **+19,466,337,813** |
| FX effect | +25,791,988 |
| B03 beginning cash | **86,364,663,248** |
| B03 ending cash | **105,856,793,049** |
- Standalone Q1 B03 3M = Q1 quarter. CFO constituent components and asset/debt/equity etc reconciled to **23 original signed PDF accounting identities exact-VND 0**; B03 cash bridge 86,364,663,248 + 19,466,337,813 + 25,791,988 = 105,856,793,049 exactly.
- `data/financials-GEG.json` 2026-Q1 now has **90 issuer original/derived fields** and corrected EPS basic **577 vs auto 70**, diluted **550**; prior auto values retained under `financial_line_items_prior_values` + `financial_line_items_rejected_values`.
- GEG H1/2026 Q2 B02 cumulative revenue 1,347,714,407,034 = Q1 767,379,199,934 + Q2 standalone 580,335,207,100, and net H1 271,805,979,210 = Q1 263,653,973,396 + Q2 8,152,005,814, owner profits also exact. **No Q1/Q2 P&L mismatch**.

## Open material Q1 versus Q2 source-vintage cash comparatives — do not hide
Two independently signed **consolidated** GEG original PDF sources have different Jan 1, 2026 *cash and cash equivalents* comparatives, despite both reporting the same FY opening total assets 15,110,888,031,702 VND:
- Q1 original signed 24/04/2026, B01 p6 opening cash and B03 p10 beginning cash **86,364,663,248 VND**.
- Q2 original signed 28/07/2026, B01 p4 opening cash and B03 p8 beginning cash **74,942,444,345 VND**. Q3 later original uses this same 74,942,444,345 VND opening comparator.
- Difference **Q1 minus Q2 opening 11,422,218,903 VND**, not zero and above 0.01% material threshold.
- 6M Q2 B03 reported net cash change 25,371,516,918; Q1 3M net change 19,466,337,813; hypothetical quarter-only net change **+5,905,179,105**; FX hypothetically H1 13,217,270 minus Q1 25,791,988 = **-12,574,718** VND. Q1 closing cash **105,856,793,049**, Q2 closing **100,327,178,533**, actual quarter cash change **-5,529,614,516**. Candidate quarter-only net +5,905,179,105 + FX -12,574,718 = +5,892,604,387 VND, differing from actual cash change by **11,422,218,903 VND** exactly. This is a **cross-vintage comparative cash opening/restatement discrepancy**, not arithmetic fault in either individual B03.
- Section-wise purely algebraic H1−Q1 source values (provisional, **NOT canonical Q2**): CFO +508,833,832,667; CFI -705,709,092,843; CFF +202,780,439,281 VND. They sum to provisional net +5,905,179,105, but do **not bridge to reported Q2 B01 cash**. Store only in `source_validation.q2_cash_flow_year_to_date_subtraction_unreconciled_provisional_vnd`; keep GEG Q2 `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow`, `net_cash_change`, `cash_beginning` etc **null** and status `blocked_cross_source_year_opening_cash_difference_11422218903_vnd` pending validated issuer restatement or revised comparator.
- Cross-report root cause not yet determined; possible reclassification of beginning cash equivalents requires **issuer notes**, cannot be inferred as fact. Review official audited H1 2026 (GEG semiannual consolidated, released late August 2026), 2025 FY audited cash note, and 2026 Q2 thuyết minh 5 carefully. Preserve both original baselines.

## Code and next action
- `scripts/inspect_geg_q1_2026_pdf.py` and `.github/workflows/inspect-geg-q1-2026-pdf.yml`: bounded original source reader now prioritizes known reachable issuer signed Vietstock publication copy, saves original page PNG artifact, skips slow OCR, never writes canonical data. Run `44523692326` PASS.
- `scripts/verify_geg_q1_2026_source.py`: independent issuer source 23 exact VND B01/B02/B03 checks; exact cross-report Q1+Q2 H1 B02; protects material comparative difference and forbids silently populating invalid Q2 standalone B03 fields.
- `.github/workflows/validate.yml` new GEG Q1 gate. Merge only when CI PASS; deploy unchanged website and smoke 45/45 SHA. Save final merge commit as checkpoint append.
- Once GEG 2026Q1 source passes, next investigate **official GEG H1/2026 audited/reviewed** to reconcile Jan1 cash comparative, otherwise keep explicit exception and continue one ticker **GEG 2025-Q4, Q3, Q2, Q1** original validation. DO NOT redo GEG 2026-Q3 both scopes PASS; do not move to IDC before GEG historical periods validated.
- Independent open cases: VDS H1 2025 owner/NCI 1,117,693,283 VND documented; GAS 2026H1 cost of goods 10,160,150,278 VND unresolved allocation; PLX parent 2026Q3 B03 CFF 87,654,015,000 VND unresolved. Original source only; do not fabricate.
