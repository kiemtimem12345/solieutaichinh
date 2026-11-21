# CHECKPOINT VCI — B03 Q3/2026 quý riêng từ báo cáo 9M trừ H1 soát xét, đúng từng VND

**Ngày:** 21/11/2026 (ICT). **Repo:** `kiemtimem12345/solieutaichinh`. **PR:** #121. **Nhiệm vụ tiếp:** VCI các kỳ còn thiếu, xong mới VCK.

## Chứng cứ nguồn đã trực tiếp đọc ảnh scan (không OCR)
- H1/2026 BCTC giữa niên độ VCI, báo cáo soát xét có PwC trên ảnh, PDF mirror nguồn Vietstock liên kết từ công bố VCI: 98 trang, **15.650.240 bytes**, **SHA256 `1ea814d02563a136d11d718c62c1ffc3c08463ffaf12369c517111cd26f6b9af`**. Ảnh scan `H1_reviewed-16.jpg` và `H1_reviewed-17.jpg` (PDF trang 16–17, báo cáo in 12–13) là B03b-CTCK 6 tháng.
- BCTC Q2/2026 VCI theo nguồn HOSE mirror Vietstock: 48 trang, **17.064.259 bytes**, **SHA256 `a8fec422bac195c1b4d9743a995da35ec5066fa6dc0f951e6fbb36f2218823b5`**. Ảnh scan `Q2_as_filed-13.jpg` và `Q2_as_filed-14.jpg` (PDF trang 13–14, báo cáo in 11–12) là B03 lũy kế 6 tháng.
- Cả hai file hợp lệ `%PDF-`, `pdfinfo` xác nhận trang; `pdftotext` chỉ 194/144 ký tự nên phần B03 phải đọc hình. Không nhận dạng OCR giả làm xác minh. Ảnh kiểm tra lưu ngắn hạn trong artifact 14712970890, run https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44918419435. Không commit bản PDF hay ảnh đầy đủ vào repo.
- **Hai phiên bản Q2 gốc và H1 có soát xét hoàn toàn khớp** 6 dòng B03 sau đây, không có sai số vintage trong kỳ H1; phạm vi đúng CTCK VCI, **không có công ty con theo ghi chú đã xác minh ở Q3**, không gọi báo cáo này là PDF hợp nhất chính thức.
- Hai URL mirror: https://static2.vietstock.vn/vietstock/2026/8/14/20260813___vci___bctc_6t_nam_2026___cbtt_2.pdf ; https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCI_Baocaotaichinh_Q2_2026_1.pdf
- Nguồn gốc Q3 đã ký, 64 dòng B01/B02/B03 9M kiểm chứng PR #119: `reports/source-audits/VCI-2026Q3-issuer-HOSE-original-special-broker-no-subs-vnd.json`. B03 riêng Q3 trước đây NULL nay có thể tính đúng nguồn.

## B03 doanh nghiệp VCI, số chính xác VND
| Dòng | Nguồn H1 (6M) | Nguồn Q3 (9M) | Q3 riêng = 9M − H1 |
|---|---:|---:|---:|
| CFO kinh doanh | -4.539.879.183.965 | -6.185.243.120.130 | **-1.645.363.936.165** |
| CFI đầu tư | -26.547.106.493 | -76.957.830.177 | **-50.410.723.684** |
| CFF tài chính | +5.001.663.109.500 | +6.058.038.109.500 | **+1.056.375.000.000** |
| Thay đổi tiền thuần | +435.236.819.042 | -204.162.840.807 | **-639.399.659.849** |
| Tiền đầu kỳ | 3.213.693.581.406 | 3.213.693.581.406 | **3.648.930.400.448** |
| Tiền cuối kỳ | 3.648.930.400.448 | 3.009.530.740.599 | **3.009.530.740.599** |

Các phương trình doanh nghiệp:
- H1 CFO+CFI+CFF = +435.236.819.042 VND; tiền mở + biến động = 3.648.930.400.448 VND, dư 0.
- Q3 riêng CFO+CFI+CFF = -639.399.659.849 VND; tiền cuối H1 3.648.930.400.448 −639.399.659.849 = tiền cuối Q3 3.009.530.740.599 VND, dư **0 VND**.
- Dòng tiền chứng khoán của khách hàng nằm ngoài B03 tiền doanh nghiệp, không cộng vào tiền mặt VCI.

## Thay đổi code trên PR #121
- `data/financials-VCI.json`: thêm đúng **5 dòng dòng tiền quý riêng** và tiền đầu Q3, giữ tiền cuối Q3 và 64 dòng nguồn cũ, đơn vị website **triệu đồng** (exact six decimal precision from VND). Dòng `*_ytd` 9M giữ nguyên, `cashflow_period_basis` giữ `year_to_date` để bảng chọn lũy kế vẫn hoạt động. Metadata nguồn rõ.
- `reports/source-audits/VCI-2026Q3-reviewed-H1-signed-Q2-quarter-cash-vnd.json` lưu hash, đường nguồn, trang PDF, hai phiên bản H1/Q2, phép tính tại đơn vị VND. Không lưu toàn văn PDF.
- `scripts/verify_vci_2026q3_h1_reviewed_cash_bridge.py`: kiểm chứng VND chính xác, đối chiếu báo cáo nguồn Q3 cũ, so sánh H1/Q2, test 3 lỗi cố ý, bảo vệ việc Q2 standalone chưa có nguồn, không lẫn tiền khách hàng.
- `scripts/verify_vci_2026q3_issuer_no_subs_source.py`: cập nhật assertion Q3 quý thay vì còn null, giữ các 64 kiểm chứng nguồn cũ.
- `.github/workflows/validate.yml`: thêm regression, cấm publish nếu lệch.
- `scripts/inspect_vci_2026h1_signed_pdf_sources.py` và workflow `inspect-vci-2026h1-original.yml`: tải có giới hạn thời gian, check SHA và số trang exact, render ảnh PDF có giới hạn, artifact retention 1 ngày, phát hiện bản scan, không nhận nhầm là searchable PDF.
- **Lưu ý:** Q2/2026 standalone CFO/CFI/CFF còn NULL vì cần Q1/2026 ký gốc cùng phạm vi; H1 6M có ký đã dùng làm chứng cứ cho Q3, không phải số Q2 riêng.

## Điều kiện hoàn thành và bước tiếp
- [x] Đã kiểm tra báo cáo ký Q2 6M và H1 soát xét 6M bằng ảnh B03
- [x] 6M hai phiên bản đúng VND; Q3 9M trừ 6M và cầu tiền dư 0
- [x] Có báo cáo kiểm chứng máy bằng Python và 3 phép kiểm âm; dữ liệu Q3 JSON cập nhật trên nhánh PR
- [ ] Chỉ coi hoàn tất **merge và production** khi PR financial CI, nguồn kiểm tra, website smoke và Pages xác nhận PASS; ghi mã run/commit sau khi hoàn tất
- [ ] VCI Q1/2025–Q2/2026 B01/B02/B03 riêng kỳ chưa hoàn thành; tiếp tục từng kỳ, không lặp Q3; sau khi VCI xong xử lý VCK.

## Không mở lại ngoài phạm vi
- MBB/VIX/GAS/VDS đã PASS 7 kỳ. GEG và IDC đã hoàn thành xử lý nguồn 7/7 có ngoại lệ B03 quý II, chờ kiểm toán năm 2026 (PR #117/#118), không tái xử lý.
- PLX Q3/2026 công ty mẹ B03 CFF lệch 87.654.015.000 VND (1,4692% > 0,1%) chưa có đính chính nguồn ký, giữ `terminal_manual_review`.
