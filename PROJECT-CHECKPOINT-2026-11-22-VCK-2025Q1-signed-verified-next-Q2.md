# CHECKPOINT — VCK (VPS/VPSS) Q1/2025 đã đối chiếu nguồn ký

Ngày 22/11/2026 (ICT). Repo `kiemtimem12345/solieutaichinh`, PR #128. Thứ tự: **VCK Q1/2025 xong → Q2/2025 → Q3/2025 → Q4/2025 → Q1/2026 → Q2/2026 → Q3/2026**. Không mở lại VCI 7/7 hay kỳ VCK đã PASS.

## Chứng cứ
- Nguồn PDF VPS nguyên bản ký 17/04/2025: `https://static2.vietstock.vn/data/OTC/2025/BCTC/VN/QUY%201/VPSS_Baocaotaichinh_Q1_2025.pdf`. Tên công ty **Công ty Cổ phần Chứng khoán VPS**, mã hồ sơ cũ VPSS, mã niêm yết mới VCK. B01 PDF trang 5–6, B02 trang 8–11, B03 trang 12–13, riêng tiền hoạt động môi giới của khách hàng tách trang tiếp. Tất cả số lưu đúng VND; giao diện triệu VND. Không xác nhận hash binary vì chưa tải/hash trực tiếp; nguồn hình và bảng PDF đã đọc trực quan.
- Bản cáo bạch VCK ký `https://cmsv5.fiingroup.vn/medialib/FG/2025/2025-12/2025-12-09/VCK/20251208--VCK--Ban-cao-bach-niem-yet_signed.pdf` trang cáo bạch 45 (và các trang khác), xác nhận VPS đã thoái hoàn toàn công ty con VPBS Myanmar trong Q1/2025; **không phải lập BCTC hợp nhất kể từ Q1/2025**. Vì vậy không tự ghi BCTC này là “BCTC hợp nhất”, dùng BCTC công ty phát hành với cờ phạm vi rõ. Không lấy nhầm báo cáo thuốc sát trùng “VPS” cùng chữ mã.
- `reports/source-audits/VCK-2025Q1-VPSS-issuer-signed-standalone-vnd.json`: 65 trường VND gốc từ B01/B02/B03, **19 phương trình chính xác VND sai số 0**, giữ URL và trang. `scripts/verify_vck_2025q1_signed_vps_issuer.py`: CI 19 phương trình, 4 phép kiểm thử hỏng dữ liệu chủ ý.
- `data/financials-VCK.json`: chỉ cập nhật 2025Q1, giữ 2025Q2–2026Q3 nguyên trạng. Đã bỏ 4 hồ sơ `pre_listing_legacy_reports` từ 2024, áp dụng quy tắc chỉ lưu Q1/2025+. Tách tiền khách hàng khỏi tiền doanh nghiệp.
- CI workflow `44931917659` cho commit chứa dữ liệu/ledger/test trước checkpoint **PASS**. Kiểm tra lại workflow sau commit checkpoint, merge PR #128 chỉ khi PASS. Production Pages/smoke cần theo dõi riêng nếu có công cụ.

## Số liệu ký gốc 2025Q1 (VND)
| Chỉ tiêu | VND |
|---|---:|
| Tài sản | 36.130.495.941.257 |
| Nợ phải trả | 24.032.801.434.855 |
| Vốn CSH | 12.097.694.506.402 |
| Doanh thu hoạt động | 1.468.456.997.200 |
| Chi phí hoạt động | 536.490.028.663 |
| Doanh thu tài chính | 274.622.985.436 |
| Chi phí tài chính | 203.397.310.816 |
| Lợi nhuận trước thuế | 918.473.136.361 |
| Chi phí thuế TNDN | 183.698.911.256 |
| Lợi nhuận sau thuế | 734.774.225.105 |
| CFO | -5.192.088.224.222 |
| CFI | -18.460.375.168 |
| CFF | +5.101.821.666.666 |
| Thay đổi tiền thuần | -108.726.932.724 |
| Tiền đầu kỳ | 1.732.141.826.349 |
| Tiền cuối kỳ | 1.623.414.893.625 |

Kết quả: CFO+CFI+CFF=biến động tiền, tiền đầu+biến động=tiền cuối; tài sản=nợ+vốn; B02 cơ cấu chi phí, thu nhập và thuế khớp **0 VND**.

## Bước tiếp theo không cần hỏi
1. Xác nhận CI PR #128 SHA cuối, merge, đọc lại main và lưu checkpoint.
2. **VCK Q2/2025**: bản ký gốc `https://static2.vietstock.vn/data/OTC/2025/BCTC/VN/QUY%202/VPSS_Baocaotaichinh_Q2_2025.pdf` (39 trang, scan), B01 p5–6, B02 p8–11, B03 6M p12–13. Xem thêm bản H1/2025 đã soát xét trên website VPS công bố 14/08/2025; so sánh 6M theo đúng kỳ/phạm vi rồi trừ Q1 CFO/CFI/CFF để có quý II. Nếu có sai lệch nguồn thì đưa ngoại lệ vào hàng chờ nội bộ và tiếp tục mã/kỳ theo trình tự, chỉ hiển thị danh sách tồn đọng khi người dùng hỏi.
3. Sau khi toàn bộ VCK hoàn thành, tiếp các mã theo danh sách ưu tiên đã checkpoint, không xử lý lại mã PASS. Không đưa 2024 vào chuỗi.
