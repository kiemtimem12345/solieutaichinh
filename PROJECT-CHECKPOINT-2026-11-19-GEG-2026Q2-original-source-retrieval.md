# CHECKPOINT — GEG Q2/2026 issuer original source retrieval (19/11/2026)

## Completed upstream (do not redo)
- VDS 7/7 consolidated issuer-original quarters 2025Q1–2026Q3, B01/B02/B03 and standalone quarterly cash flows, from PR #66 merge `0423fb7323a461e9c01a16574c8153cbda97f817`.
- Separate VDS reviewed H1/2025 consolidation check PR #67 merge `aadd57d6a28fc8c377eb999b23a80b6c9bee8b2a`, 84-page reviewed issuer PDF with exact B02 parent H1 8,071,151,977 and NCI -252,715,388 VND, confirms a **1,117,693,283 VND** opposite parent/NCI cross-quarter allocation inconsistency. Source lines original and reviewed match, preserving documented exception. Do not rewrite Q1/Q2 individual issuer columns. CI and site 45/45 PASS after PR #67.
- GEG 2026Q3 has **both parent and consolidated separately PASS**; never redo.

## Next ticker GEG
- `data/financials-GEG.json` currently has 8 records, of which consolidated Q1–Q4/2025 and Q1–Q2/2026 are all `auto_extracted_pending_visual_review`; 2026Q3 2 scope variants validated, must preserve.
- GEG Q2/2026 HOSE official original disclosure dated 29/07/2026:
  https://staticfile.hsx.vn/Uploads/UploadDocuments/2484429/20260729%20-%20GEG%20-%20BCTC%20hop%20nhat%20Q2.2026%20%26%20giai%20trinh.pdf
- HOSE original path independently indexed at https://stock.hoana.vn/bao-cao-tai-chinh/GEG and https://nmquan.vn/data/ma/GEG/cong-bo/28060409-bctc-hop-nhat-q2-2026-giai-trinh . File fallback catalog VietstockFinance links:
  https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/GEG_Baocaotaichinh_Q2_2026_Hopnhat.pdf (URL constructed from existing project auto archive; **unconfirmed direct availability**).
- Read-only GitHub Actions original source capture `scripts/inspect_geg_q2_2026_pdf.py` with workflow `.github/workflows/inspect-geg-q2-2026-pdf.yml`, runs ephemeral with cap 45MB and redirect guard, renders original pages 1–21. Q2 source run `44520357617` started. **At this checkpoint no new canonical GEG financial data has been accepted.** Do not substitute guessed Q2 amounts, OCR-only values or parent/cons scope.

## Verification and resume procedure
1. Inspect run results, including source bytes SHA256 and page images. If HOSE access fails, try issuer GEC original at https://geccom.vn plus official HOSE mirrored disclosure. Render original B01/B02/B03 and visually verify all entered numbers.
2. Keep GEG 2026Q2 original B01 assets = liabilities + equity, Q2 B02 profit and cumulative H1, B03 6M source and cash bridge and B01 cash, signs/units VND. Derive stand-alone Q2 cash only after GEG 2026Q1 source B03 3M verified from same consolidated scope.
3. Add source provenance and rejected parser originals for changed fields; exact-VND regression; PR+CI; site 45/45 and durable checkpoint; proceed next 2026Q1, 2025Q4… then IDC.
4. Preserve GEG 2026Q3 two already complete scope records and don't alter website UI. Source main GitHub tracked 41 JSON + index/assets; never edit Hostinger checkout outside Git.
5. Independent unresolved issues: GAS 2026H1 cost classification 10,160,150,278 VND; PLX parent Q3/2026 financing 87,654,015,000 VND. All changes maintain cutoff 2025Q1, max 20 periods, tolerated <=0.01%, million VND JSON except EPS.
