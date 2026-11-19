# CHECKPOINT — VDS hợp nhất 2026 Q1, dòng tiền riêng Q2 và chênh lệch trình bày H1 (19/11/2026)

## Điểm tiếp tục
- Trước phiên: main commit `42ec2ae0c8eec9c144af258e11a9a0367672a383`, PR #62 đã merge và CI + production 45/45 PASS: VDS 2026Q2 hợp nhất B01/B02 + B03 6M, 24 issuer exact-VND identities.
- `data/financials-VDS.json` 2026Q3 hợp nhất B01/B02/B03 9M và standalone Q3 đã PASS; **không reprocess**.
- VDS 2026Q1 chỉ có legacy auto parser: sai revenue, LNST, EPS, CFO, FX. Mục tiêu xử lý Q1 issuer original và lấy B03 Q1 để hoàn thành tiền riêng Q2 cùng phạm vi.

## Nguồn chính thức, PDF ký 24/04/2026
- Trang công bố: https://www.vdsc.com.vn/quan-he-co-dong/cong-bo-thong-tin/rong-viet-cong-bo-bao-cao-tai-chinh-hop-nhat-quy-1-2026-va-giai-trinh-chenh-lech-loi-nhuan-i1019
- PDF gốc: https://www.vdsc.com.vn/data/api/app/file-storage/a22de0e9-c1c8-49fe-d79a-08dea20313d6/VDSC_Cong%20bo%20BCTC%20HN%20Quy%201.2026.pdf?downloadFrom=ManagementDocument-1019
- Original 50-page signed issuer PDF, 5,424,585 bytes, SHA256 `f48b349d51f0158185764b8862648386b9560c271fdb11c65c8bb5710b8e90ec`.
- GitHub Actions inspect run `44506806233` PASS, artifact `14519881822` page images 3–18 reviewed visually; PDF pages 6–10 B01, 11–13 B02, 14–16 B03. Screenshot official PDF also available in this chat.
- B01 source unit VND; JSON unit `triệu VND` except EPS (VND/cổ phiếu). B02 uses securities company revenue code 20, NOT FVTPL gain code 01.

## Q1 2026 dữ liệu gốc
- **B01 31/03/2026:** tài sản **7.868.505.982.599**, nợ **4.839.432.932.978**, vốn chủ **3.029.073.049.621**, cash **858.161.024.619**, current assets 6.417.238.249.041, noncurrent assets 1.451.267.733.558 VND. NCI equity POSITIVE 59.719.114.955 VND; client-brokerage cash outside corporate B01: 1.220.638.114.499 VND, not added to balance-sheet cash.
- **B02 Quý I/Năm nay:** doanh thu hoạt động 202.757.306.990, chi phí hoạt động 190.545.800.755, finance income 9.984.544.961, finance cost 12.726.612.033, admin cost 45.505.054.316, operating P/L -36.035.615.153, PBT **-36.035.069.699**, tax expense **-6.544.269.253** (current +7.851.910.907, deferred -14.396.180.160), consolidated after-tax **-29.490.800.446**, parent -28.526.203.886, NCI -964.596.560 VND; EPS -105 VND/share. Old auto `revenue=-21.364 triệu` was FVTPL component, `net_profit=0` incorrect, EPS 501 incorrect; legacy values quarantined in `financial_line_items_prior_values` and `financial_line_items_rejected_values`.
- **B03 3M/YTD Q1:** CFO +248.423.817.918, CFI -270.538.392.551, CFF -116.700.000.000, net cash -138.814.574.633, beginning cash 996.975.599.252, ending 858.161.024.619 VND; issuer exact 5 source checks residual zero. Earlier auto CFO -36.035 triệu and FX = ending cash were wrong; originals retained in rejected metadata.
- Q1 B01/B02 independent 20 exact-VND checks residual zero; Q1 B03 5 checks zero. All primary lines verified visually.

## Q2 tiền riêng từ 6M trừ Q1 cùng phạm vi
- H1 B03 original Q2 pre-verified (from PR #60) CFO -2.620.903.680, CFI -90.786.936.920, CFF -101.950.000.000, net -195.357.840.600 VND.
- **Q2 standalone**, 6M–3M: CFO **-251.044.721.598**, CFI **+179.751.455.631**, CFF **+14.750.000.000**, net **-56.543.265.967** VND. Q2 begins at Q1 B01 cash 858.161.024.619, ends 801.617.758.652: exact bridge, quarterly capex -23.746.500 VND.
- Status `2026-Q2` advanced to `issuer_original_visual_verified_b01_b02_b03_and_q2_standalone_cash`.
- **Q2 original B01 sign fix**: NCI equity B01 item 418 must be **+56.506.662.501** VND; previous JSON incorrectly carried `-56.506.662.501`. Separate parent equity 2.957.968.452.602, total equity 3.014.475.115.103 VND, source exact split 0 residual; maintain wrong original sign in prior-values metadata.

## H1 cross-quarter exception — not a license to edit original published quarters
- Q1 standalone operating revenue 202.757.306.990 + Q2 standalone 262.152.978.583 = **464.910.285.573**, but Q2 H1 YTD reported revenue **458.846.424.238**; **-6.063.861.335 VND** difference.
- Q1 standalone expenses 190.545.800.755 + Q2 standalone 157.186.798.783 = 347.732.599.538; H1 YTD expense 341.668.738.203; **-6.063.861.335** difference exactly. Both concentrated in FVTPL revenue and FVTPL losses, so net operating profit/PBT/net income H1 equals Q1+Q2 exactly.
- H1 parent-attributable vs Q1+Q2 parent net differs **+141.501.685 VND**; NCI difference `-141.501.685` VND. Consolidated total net reconciles, no isolated quarter attribution confirmed. Preserve source vintage and both quarter-original columns.
- No inference/adjustment of quarterly Q1/Q2 to force revenue/expense sums. Classify as **report-vintage FVTPL netting and attribution exceptions**, not PDF OCR corruption.

## Code, checkpoints, and next
- `data/financials-VDS.json`: Q1 B01/B02/B03 exact and Q2 standalone B03 and NCI equity sign fixed; only periods 2026Q1, Q2 altered, 2026Q3 and historical 2025 rows unchanged.
- `scripts/inspect_vds_q1_2026_pdf.py` + `.github/workflows/inspect-vds-q1-2026-pdf.yml`: ephemeral official original render (read-only).
- `scripts/verify_vds_q1_2026_source.py`: 20 Q1 B01/B02 identities, 5 Q1 B03, Q2 bridge, controlled H1 re-presentation checks, source hash.
- `scripts/verify_vds_q2_2026_source.py` and `scripts/verify_vds_q2h1_q3cash_bridge.py` updated to expect Q2 standalone and positive NCI equity; CI gate in `.github/workflows/validate.yml`.
- **Merge only CI PASS**, then verify production website 45/45 URLs and byte-level SHA against main. Save merged commit in this checkpoint.
- Next within **same ticker VDS**, validate 2025Q1–Q4 B01/B02/B03 from issuer originals one quarter at a time; do not mark old auto-extracted values as PASS. After full VDS, GEG gaps → IDC Q3; skip already complete GEG Q3.
- GAS H1 2026 COGS 10.160.150.278 VND assignment unresolved, retain checkpoint; PLX parent Q3 B03 mismatch 87.654.015.000 VND unresolved; never fabricate.

## Merge / production status — verified
- PR #63 merged `main`, commit `d1587e4216358e1d4997abfd10701bbacadd82df`.
- GitHub Actions pre-merge CI run `44508369760` PASS; main CI run `44508444594` PASS.
- GitHub Actions read-only issuer original Q1 50-page PDF run `44506806233` PASS (artifact 14519881822; SHA256 documented above); duplicate reruns not required for financial verification.
- Production website read-only SHA-256 verification `44508444014` PASS **45/45 HTTPS URLs**, including original HTML/CSS/JS and all 41 tracked JSON assets (32 financial + 9 support). No direct SFTP changes.
- VDS 2026Q1 and 2026Q2 consolidated original B01/B02/B03 and Q2/Q3 standalone cash-flow now have source+exact-VND checks. **VDS ticker NOT fully finished**: older 2025Q1–Q4 remain auto-extracted/unverified; do not revisit completed 2026Q1–Q3 unless a later explicit contradiction.
- Resume next from **VDS 2025-Q4 original B01/B02/B03** (then Q3→Q1 2025, one quarter at a time). Preserve 2025Q1 cutoff, max 20 periods, and <=0.01% tolerance.
