# CHECKPOINT — GEG hợp nhất Q2/2026 B01/B02/B03 gốc — 19/11/2026

## Tiến độ và nguyên tắc
- VDS 2025-Q1 đến 2026-Q3 hợp nhất đã kiểm chứng **7/7 kỳ**, PR #66 merge `0423fb7323a461e9c01a16574c8153cbda97f817`, PR #67 merge `aadd57d6a28fc8c377eb999b23a80b6c9bee8b2a`; website CI+SHA 45/45 PASS. Không làm lại VDS. H1/2025 VDS lệch phân bổ parent/NCI 1,117,693,283 VND đã đối chiếu 3 báo cáo và được giữ làm ngoại lệ chứ không sửa ép.
- GEG Q3/2026 **cả riêng lẻ và hợp nhất** đã đạt `verified_manual_visual_reconciliation`; không chạy lại kỳ Q3. GEG 2025Q1–2026Q2 (6 kỳ) cũ đang `auto_extracted_pending_visual_review`, cần xử lý lần lượt; kỳ này tập trung **GEG Q2/2026 hợp nhất**.
- GitHub main nguồn gốc website; tài chính từ Q1/2025, tối đa 20 kỳ/mã, đơn vị VND PDF → `triệu VND` JSON trừ EPS, chênh <=0.01% cho phép bỏ qua nhưng đẳng thức gốc yêu cầu chính xác đến đồng khi có đầy đủ cấu phần. B03 YTD không đồng nhất với số riêng quý.

## Nguồn gốc PDF và lỗi tải chính thức
- HOSE công bố ngày 29/07/2026 file `20260729 - GEG - BCTC hop nhat Q2.2026 & giai trinh.pdf`: https://staticfile.hsx.vn/Uploads/UploadDocuments/2484429/20260729%20-%20GEG%20-%20BCTC%20hop%20nhat%20Q2.2026%20%26%20giai%20trinh.pdf .
- Truy xuất HOSE trực tiếp từ web và GitHub Actions thường trả **timeout**, không suy ra PDF thiếu. Đã chuyển qua bản sao **PDF gốc có chữ ký và dấu của công ty**, đúng biểu mẫu hợp nhất, từ Vietstock: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/GEG_Baocaotaichinh_Q2_2026_Hopnhat.pdf .
- GitHub Actions read-only `44520387543`: `SOURCE_UNAVAILABLE HOSE TimeoutError` rồi `SOURCE_OK VIETSTOCK`, `PDF_OK` **43 trang**, **2,341,291 bytes**, SHA256 `e5c84e9cb42b1698481b12f426544cfad517894d46d3d0f37a1e9e53575f00d5`, artifact PNG `14526818741` (24 trang đầu); `SOURCE_RENDER_PASS`. Original page images visually reviewed p4–5 B01-DN/HN; p6 B02-DN/HN; p7–8 B03-DN/HN, report signed 28/07/2026. **Không dùng tài liệu B01a-DN công ty mẹ** lẫn với bản hợp nhất vì từ năm 2026 báo cáo theo Thông tư 43/2026/TT-BTC.
- `scripts/inspect_geg_q2_2026_pdf.py` and `.github/workflows/inspect-geg-q2-2026-pdf.yml` are read-only ephemeral image render and HTTP-domain restricted. OCR fallback unverified until PNG review.

## B01 GEG hợp nhất 30/06/2026 (VND chính xác)
- Total assets **15,481,663,386,076**, current assets 1,795,327,105,425, non-current assets 13,686,336,280,651.
- Liabilities **8,730,633,735,292** = short 1,073,912,833,438 + long 7,656,720,901,854; equity **6,751,029,650,784** includes non-controlling interest 1,570,575,747,143 and parent equity 5,180,453,903,641 (sum equals B01 equity).
- Cash + equivalents **100,327,178,533**, short investments 399,347,389,553, receivables 1,089,342,589,419, inventory 59,335,951,480, other short assets 146,973,996,440; fixed assets 12,889,071,805,876. Cash matches B03 closing exactly.

## B02 riêng Q2 và H1 lũy kế
| VND | Quý II 2026 riêng | 6 tháng 2026 YTD |
|---|---:|---:|
| Doanh thu thuần | 580,335,207,100 | 1,347,714,407,034 |
| Giá vốn | 342,819,635,918 | 623,234,271,697 |
| Lãi gộp | 237,515,571,182 | 724,480,135,337 |
| Lợi nhuận kinh doanh | 18,662,838,595 | 303,878,676,169 |
| LNTT | 18,568,717,509 | 304,983,996,509 |
| Thuế TNDN (hiện hành + hoãn lại) | 10,416,711,695 | 33,178,017,299 |
| LNST hợp nhất | **8,152,005,814** | 271,805,979,210 |
| LNST cổ đông công ty mẹ | 28,179,986,219 | 234,855,487,782 |
| LNST lợi ích không kiểm soát | -20,027,980,405 | 36,950,491,428 |
- EPS gốc **22 VND/cp**, diluted EPS **21 VND/cp** (bản auto ghi EPS 70, diluted -14956 là lấy sai chỉ tiêu, đã cách ly giá trị cũ).

## B03 6 tháng 2026 gốc (YTD, VND)
- CFO **+722,160,976,132**, CFI **-732,448,267,884**, CFF **+35,658,808,670**, net cash **+25,371,516,918**; FX +13,217,270; cash opening **74,942,444,345** → closing **100,327,178,533**. Bridge exact zero VND.
- Capex -653,270,670,725; debt proceeds +751,518,963,283, repayments -710,817,288,298; finance lease repayments -4,991,802,915. **Dividends paid only -71,063,400 VND**, not -4,991,802,915 as old parser mistakenly mapped. Preserve rejected figure.
- 101 source fields stored in `data/financials-GEG.json` Q2 consolidated, 31 independent B01/B02/B03 identity residuals all **0 VND**. Original pre-verification values archived under `financial_line_items_prior_values` and `financial_line_items_rejected_values`.
- **Q2 standalone CFO/CFI/CFF not yet calculated**: 2026-Q1 consolidated B03 remains old auto extraction; don't subtract invalid YTD. Q3/2026 previously PASS not reprocessed.
- `scripts/verify_geg_q2_2026_source.py` checks exact original SHA, page count, Q2/H1 source figures, 31 balance identities, EPS and lease-vs-dividend signs, ensures no invented standalone cash. Workflow `.github/workflows/validate.yml` runs gate before accepting PR.

## Next
1. CI PASS → merge GEG Q2 source verification; production website Git main deploy + read-only 45/45 URL and SHA. Save merged commit to this checkpoint.
2. Verify **GEG Q1/2026 hợp nhất** original B01 B02 B03 before calculating Q2 quarter cash (6M minus 3M), then GEG 2025Q4, 2025Q3, 2025Q2, 2025Q1 one quarter at a time. Source original first; no automatic parser numbers marked PASS.
3. When all GEG periods pass, move to IDC 2026 Q3; do not redo already verified GEG 2026Q3 two scopes.
4. Open independent exceptions: VDS 2025 H1 owner/NCI attribution 1,117,693,283 VND, GAS 2026 H1 COGS 10,160,150,278 VND, PLX parent 2026 Q3 CFF 87,654,015,000 VND. Keep provenance and never guess resolution.

## PR #69 / CI and production verified
- Merged GitHub PR #69 to main, commit `0da1635d0c846b45208f5cc35a64d71f25880bd0`.
- Pre-merge financial CI run `44522227655` **success**; post-merge main financial CI `44522371719` **success**, with 31 exact-VND GEG Q2 source/identity checks.
- Read-only production smoke run `44522371752` **success**, log explicitly `PASS: 45/45 HTTPS URLs serve exact tracked Git content (SHA256).`
- Redundant source-only PR #68 (failing direct HOSE PDF fetch) closed as superseded by successful original signed-PDF Vietstock mirror fallback in PR #69. Do not merge PR #68.
- GEG consolidated 2026-Q2 now **issuer_original_visual_verified** with B03 6M YTD. Do **not** calculate standalone 2026-Q2 cash until GEG 2026-Q1 original B03 same scope is verified.
- Next resume: GEG **2026-Q1** issuer consolidated original B01/B02/B03. After Q1 source validated, derive Q2 standalone = 6M–3M and retain Q3/2026 original already PASS; then historical GEG 2025-Q4 → Q1.
