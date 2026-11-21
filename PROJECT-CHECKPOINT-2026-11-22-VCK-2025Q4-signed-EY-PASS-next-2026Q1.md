# CHECKPOINT — VPS/VCK Q4/2025 nguồn ký gốc và kiểm toán EY, tiếp Q1/2026 (22/11/2026)

Repo `kiemtimem12345/solieutaichinh`, PR **#131**. VCK Q1 và Q3/2025 đã PASS; không làm lại các kỳ này. Người dùng yêu cầu tự làm tiếp, queue ngoại lệ nội bộ, **không hiển thị danh sách thiếu/ngoại lệ trừ khi hỏi**.

## Nguồn gốc đúng
- Q4/2025 ký 19/01/2026 ZIP HOSE/Vietstock `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/VCK_Baocaotaichinh_Q4_2025.zip`, 5.095.521 byte, SHA-256 `6b8623b993d35eb43f04ee6feb8583b3cafc29f3a7dc8ea4449da8af10c37e43`. ZIP có bản công bố, bản Anh và bản Việt; chọn **bản Việt** `m88_20260119_20260116___vck___baocaotaichinh_quy41768821647959duedxzl4.pdf`, 2.427.951 byte, 43 trang, SHA-256 `3c3c95bace73bd3c880f77bc299bd61f3e4a887e43dd0f65c6280aff01c2f265`. Source GitHub Action `44933535018` **PASS**, artifact JPEG `14718995174` cho 24 trang đầu, giữ 1 ngày. `scripts/inspect_vck_2025q4_original_source.py` chọn bản Việt ưu tiên. B01 PDF pp5–7, B02 pp9–12 (cột Q4 năm 2025 riêng), B03 pp13–14 (lũy kế 12M). B03 riêng doanh nghiệp, không cộng tiền khách hàng môi giới.
- FY2025 kiểm toán EY ký 30/01/2026 HNX bản chính xác: `https://owa.hnx.vn/ftp/cims/2026/2_W1/000000015836998_VI_Baocaotaichinh_Kiemtoan_2025__signed.pdf`. Có bản text bảng gốc; B01 tài sản 48.402.380.273.658, lợi nhuận năm 3.578.662.786.915, CFO -6.386.814.845.213, CFI -188.923.073.932, CFF +13.524.586.405.812, tiền cuối 8.680.990.313.016 VND **khớp bản Q4 gốc**.
- Báo cáo Q4 gốc FY doanh thu hoạt động 8.267.314.897.952 VND, chi phí hoạt động 3.328.406.063.393 VND; báo cáo EY kiểm toán FY doanh thu 8.260.714.445.897 VND, chi phí 3.321.805.611.338 VND. Phần tái phân loại bằng nhau **6.600.452.055 VND**, lợi nhuận hoạt động, PBT, PAT và dòng tiền năm **không đổi**. Ghi riêng so sánh hai nguồn trong ledger, không trộn cách trình bày/điền chênh vào Q4. Cột Q4 gốc là nguồn chính cho riêng quý.
- Scope VCK công ty VPS chứng khoán đã bán công ty con năm Q1/2025 nên BCTC doanh nghiệp phát hành là nguồn, không giả báo cáo hợp nhất ký gốc.

## Số liệu B01/B02 Q4 ký gốc VND
| Chỉ tiêu | VND |
|---|---:|
| Tổng tài sản | 48.402.380.273.658 |
| Nợ phải trả | 19.567.271.018.191 |
| Vốn chủ sở hữu | 28.835.109.255.467 |
| Tiền và tương đương tiền cuối Q4 | 8.680.990.313.016 |
| Doanh thu hoạt động riêng Q4 | 2.366.904.499.271 |
| Chi phí hoạt động riêng Q4 | 889.576.769.117 |
| Lợi nhuận trước thuế Q4 | 1.279.411.027.421 |
| Lợi nhuận sau thuế Q4 | 1.014.257.104.149 |

## B03 doanh nghiệp riêng Q4 theo 12M trừ 9M ký gốc (VND)
| Chỉ tiêu | FY12M | Q3 9M | Q4 độc lập |
|---|---:|---:|---:|
| CFO | -6.386.814.845.213 | +1.009.497.441.021 | **-7.396.312.286.234** |
| CFI | -188.923.073.932 | -108.139.216.091 | **-80.783.857.841** |
| CFF | +13.524.586.405.812 | +6.044.751.583.047 | **+7.479.834.822.765** |
| Thay đổi tiền thuần | +6.948.848.486.667 | +6.946.109.807.977 | **+2.738.678.690** |
| Tiền đầu quý | | | **8.678.251.634.326** |
| Tiền cuối quý | | | **8.680.990.313.016** |
CFO+CFI+CFF = thay đổi tiền; tiền đầu + biến động = tiền cuối **dư 0 VND**.

## Code/QA
- `reports/source-audits/VCK-2025Q4-original-EY-FY2025-exact-vnd.json`: 80 trường nguồn ký VND, 32 phương trình chính xác, báo cáo EY riêng và thông tin điều chỉnh trình bày năm.
- `data/financials-VCK.json`: chỉ Q4/2025, giá trị VND/1e6 để hiển thị triệu đồng, B01 B02 quý gốc, B03 FY và quý riêng; không sửa các hàng PASS Q1/Q3, không đụng queue nội bộ.
- `scripts/verify_vck_2025q4_original_EY_FY_bridge.py`: 32 phương trình tính lại, xác thực nguồn, FY EY 18 giá trị đối chiếu, 4 kiểm thử dữ liệu sai; gắn `.github/workflows/validate.yml`.
- Chờ CI PASS ở SHA cuối, sau đó merge PR #131, đọc lại main và lưu checkpoint.

## Tiếp tục
- VCK Q1/2026 → Q2/2026 → Q3/2026 đúng thứ tự, không hỏi xác nhận. Sau đó ticker kế tiếp từ checkpoint, không lặp mã đã PASS. Không đưa năm 2024 vào lưu trữ.
- Nếu phát hiện vấn đề bất khả giải ở bất kỳ kỳ nào: tạo/update `reports/financial-exception-queue.json` kèm source, cờ production_eligible=false, tiếp tục kỳ khác, không liệt kê riêng trừ khi user hỏi “còn thiếu mã nào”.
