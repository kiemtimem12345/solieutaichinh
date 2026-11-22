# VCB Q3/2026 — kiểm định nguồn báo cáo RIÊNG (chưa ghi production)

Ngày rà soát: 2026-11-22. Mã VCB. Đơn vị nguyên gốc: **triệu VND**. Phạm vi: **RIÊNG**, không phải hợp nhất.

## Nguồn ký gốc và định vị
- Bản PDF: https://static2.vietstock.vn/vietstock/2026/11/2/20261030___vcb___bctc_rieng_q3_2026.pdf
- Trang PDF 16 (0-based 15): B02a/TCTD — tài sản, trang in số 3.
- Trang PDF 17 (0-based 16): B02a/TCTD — nguồn vốn, trang in số 4.
- Trang PDF 19–20 (0-based 18–19): B03a/TCTD — KQKD, trang in 6–7.
- Trang PDF 21–22 (0-based 20–21): B04a/TCTD — dòng tiền trực tiếp 9 tháng, trang in 8–9.
- Văn bản có chữ ký/dấu 30/10/2026; PHS công bố đường dẫn ngày 02/11/2026: https://www.phs.vn/tin-tuc/vcb-bctc-quy-3-nam-2026/6445219

## Chỉ tiêu đã nhìn trực tiếp (triệu VND)
| Chỉ tiêu | Giá trị |
|---|---:|
| Tổng tài sản 30/09/2026 | 2665192498 |
| Tổng nợ phải trả | 2418995508 |
| Vốn chủ sở hữu | 246196990 |
| Cho vay khách hàng sau dự phòng | 1759717056 |
| Tiền gửi khách hàng | 1785765282 |
| Lãi thuần Q3 | 19935563 |
| Lãi thuần 9 tháng | 56146959 |
| Lợi nhuận trước dự phòng Q3 | 17008055 |
| Chi phí dự phòng Q3 (âm) | -6145289 |
| Lợi nhuận trước thuế Q3 | 10862766 |
| Chi phí thuế TNDN Q3 (âm) | -2100332 |
| Lợi nhuận sau thuế Q3 | 8762434 |
| Lợi nhuận trước thuế 9 tháng | 36431003 |
| Lợi nhuận sau thuế 9 tháng | 29222820 |
| CFO 9 tháng | 87194048 |
| CFI 9 tháng | -8510796 |
| CFF 9 tháng | -3760054 |
| Biến động tiền 9 tháng | 74923198 |
| Tiền đầu năm theo B04a | 542513577 |
| Tiền cuối kỳ theo B04a | 617436775 |

## Phép kiểm định đạt chính xác
- 2,418,995,508 + 246,196,990 = 2,665,192,498; sai lệch 0.
- 17,008,055 - 6,145,289 = 10,862,766; sai lệch 0.
- 10,862,766 - 2,100,332 = 8,762,434; sai lệch 0.
- 87,194,048 - 8,510,796 - 3,760,054 = 74,923,198; sai lệch 0.
- 542,513,577 + 74,923,198 = 617,436,775; sai lệch 0.

## Gate tiếp theo
1. Lấy và xem PDF **HỢP NHẤT** Q3/2026, xác minh nguồn và toàn bộ bảng B02/B03/B04 theo TCTD-HN; tuyệt đối không đưa trị số báo cáo riêng sang snapshot hợp nhất.
2. Đối chiếu B04 lũy kế Q3 với H1/2026 cùng phạm vi để xác định riêng quý III, xét các số so sánh trình bày lại.
3. Ghi `data/financials-VCB.json` chỉ sau khi bản hợp nhất đạt đầy đủ kiểm định. Không sửa các kỳ đã PASS.
4. Số liệu phân tích hợp nhất từ TCBS/Vietcap chỉ phục vụ đối chiếu làm tròn; không coi là số liệu nguồn ký gốc.

Trạng thái: `VCB_2026Q3_PARENT_SOURCE_VISUAL_CORE_PASS_CONSOLIDATED_PENDING`; `production_eligible=false`.

## Đã định danh PDF hợp nhất Q3/2026
- HOSE: https://staticfile.hsx.vn/Uploads/UploadDocuments/2510515/20261030%20-%20VCB%20-%20BCTC%20Hop%20nhat%20Q3%202026.pdf
- Tên tệp gốc: `20261030 - VCB - BCTC Hop nhat Q3 2026.pdf`; công bố 30/10/2026, xác nhận qua https://nmquan.vn/data/ma/VCB/cong-bo/244413491-bctc-hop-nhat-q3-2026
- Thử đọc trực tiếp qua web ngày 22/11/2026: timeout khi fetch; **chưa xem được ảnh gốc hợp nhất**. Các trị số hợp nhất làm tròn ở nguồn phân tích không đủ điều kiện để ghi production.
