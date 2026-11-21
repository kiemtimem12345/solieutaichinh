# CHECKPOINT — VCI Q1/2025 ký gốc B01 B02 B03 xác minh — 21/11/2026

Repo `kiemtimem12345/solieutaichinh`. PR #122. Chỉ tiến độ VCI Q1/2025, **không** tuyên bố VCI đủ 7/7.

## Nguồn gốc và phạm vi
- PDF ký gốc `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/VCI_Baocaotaichinh_Q1_2025.pdf` công bố/ký 18/04/2025; **34 trang**, 13.356.823 bytes, SHA256 `7be015c6a66aee0387047aa80535da1bf8133ad9d9872c43285847b531dfd69f`.
- Tệp quét hầu như không tìm kiếm được (`pdftotext` 130 ký tự). Run GitHub Actions `44919423302` **PASS**, artifact `14713441571` (ảnh PDF pp1–24, giữ 1 ngày). Ảnh đã đọc trực quan, không lấy số liệu OCR chưa soát xét.
- Trang PDF 5–7 (B01), 10–12 (B02 in ngang), 13–14 (B03 doanh nghiệp), trang PDF 19 / trang báo cáo in 17, ghi rõ *“Công ty không có công ty con.”* Phạm vi công ty không có công ty con, tương đương phạm vi hợp nhất khi tổng hợp dashboard, nhưng **không gọi là PDF BCTC hợp nhất đã phát hành**. Dòng tiền khách hàng môi giới được tách.
- Ledger `reports/source-audits/VCI-2025Q1-signed-original-visual-vnd.json`; 48 giá trị VND chính xác; 11 identity B01 B02 B03 dư bằng 0.
- Script `scripts/verify_vci_2025q1_signed_original.py`, 3 phép kiểm âm làm sai từng dòng, vào CI `.github/workflows/validate.yml`.
- PR financial validate run `44920055069` **PASS**, nguồn scan run `44920055005` **PASS**; các run đã PASS trước khi chèn checkpoint này. Không tự nhận postmerge Pages / live smoke nếu chưa có kiểm chứng.

## B01 B02 B03 Q1/2025, VND từ nguồn đã ký
| Chỉ tiêu | Giá trị |
|---|---:|
| Tổng tài sản | 23.727.625.262.449 |
| Nợ phải trả | 11.147.502.674.864 |
| Vốn chủ sở hữu | 12.580.122.587.585 |
| Tài sản ngắn hạn | 23.620.977.742.780 |
| Tài sản dài hạn | 106.647.519.669 |
| Tiền và tương đương tiền | 2.302.263.974.886 |
| Doanh thu hoạt động | 850.928.963.332 |
| Chi phí hoạt động | 313.821.357.598 |
| Lợi nhuận hoạt động | 340.064.867.627 |
| Lợi nhuận trước thuế | 355.107.020.678 |
| Tổng chi phí TNDN (gồm hoãn lại) | 60.239.238.272 |
| Lợi nhuận sau thuế | 294.867.782.406 |
| CFO | +10.325.858.831 |
| CFI | -9.337.876.940 |
| CFF | -2.442.495.939.750 |
| Thay đổi tiền thuần | -2.441.507.957.859 |
| Tiền đầu kỳ | 4.743.771.932.745 |
| Tiền cuối kỳ | 2.302.263.974.886 |

- Cân đối = nợ + vốn CSH đúng VND.
- B02 doanh thu - chi phí + doanh thu tài chính - chi phí tài chính - quản lý = lợi nhuận hoạt động, đúng VND.
- TNDN hiện hành + hoãn lại = tổng chi phí TNDN, đúng VND.
- CFO+CFI+CFF = biến động tiền; tiền đầu+biến động = tiền cuối, cả hai dư 0 VND.

## Lỗi cũ đã được sửa bằng nguồn ký
- `cash_ending` OCR/auto trước = **0**, thật = **2.302.263.974.886 VND**; nghiêm trọng, đã thay số nguồn.
- `broker_afs_assets` cũ = **8 triệu VND**, thật = **7.523.915.401.233 VND**.
- `broker_custody_revenue` cũ = **1.940 triệu VND**, thật = **2.650.375.165 VND**.
- `fixed_assets` cũ = **36.514 triệu VND**, thật = **42.697.960.952 VND**.
- `income_tax` cũ = **72.883 triệu VND** (nhầm khoản hiện hành), thật **60.239.238.272 VND** sau thuế hoãn lại.
- Số tiền đầu kỳ/doanh thu/dòng tiền trước từng làm tròn, nay dùng chính xác VND/1.000.000 ở bảng triệu đồng.
- Không xóa bản ghi lịch sử lỗi auto extraction, nhưng thay status `issuer_signed_original_2025Q1_B01_B02_B03_core_verified_no_subs`; không re-OCR kỳ PASS.

## Điểm tiếp tục
1. **VCI Q2/2025**: tìm BCTC ký gốc 6 tháng, đối chiếu B01 B02 và tính B03 riêng quý II = 6M−Q1 ký gốc (vintage cùng phạm vi). Lưu ledger, exact VND, CI; chỉ đánh dấu xong kỳ khi đạt.
2. VCI Q3/2025, Q4/2025, Q1/2026, Q2/2026. Q3/2026 **đã chuẩn hóa, PR #121 merge**, không xử lý lại.
3. Khi VCI đủ 7 kỳ, tiếp VCK → các mã còn thiếu Q3. Các mã MBB/VIX/GAS/VDS PASS và GEG/IDC hoàn thành nguồn có ngoại lệ B03 Q2 không xử lý lại. PLX mẹ B03 Q3/2026 chưa đính chính CFF 87.654.015.000 VND, vẫn BLOCKED.
