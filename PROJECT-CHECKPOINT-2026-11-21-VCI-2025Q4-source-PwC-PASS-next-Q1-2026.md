# CHECKPOINT — VCI Q4/2025 ký gốc và kiểm toán PwC, tiếp Q1/2026

**Ngày:** 21/11/2026. **Repo:** kiemtimem12345/solieutaichinh. **PR #125**. Chỉ tác động dữ liệu Q4/2025; giữ Q1/Q2/Q3 2025 và Q3/2026 PASS, không chạy lại.

## Chứng cứ xác minh
- Báo cáo Q4/2025 phát hành công ty ký ngày 19/01/2026, PDF 48 trang, 8.046.323 byte, SHA-256 `eacfd66b3e90cb64f197a2b3c6a353adb6781793f00bef7038c04b7445bbea5f`. URL `https://www.vietcap.com.vn/api/cms-api/uploads/froala/files/20260119%20%20-%20VCI%20-%20CBTT%20Bao%20cao%20tai%20chinh%20Q4.2025.pdf`.
- Báo cáo kiểm toán FY2025 PwC công bố 13/02/2026, PDF 101 trang, 33.936.991 byte, SHA-256 `9035205081b85170e7fbf71aa1bdb8fb7052f6461b6feacffa989788d08c12ee`. URL `https://www.vietcap.com.vn/api/cms-api/uploads/froala/files/20260213%20-%20VCI%20-%20BCTC%202025%20-%20CBTT.pdf`.
- GitHub nguồn run `44923331586` **SUCCESS**, artifact `14714577893`, JPEG trích xuất 23 trang đầu từng báo cáo, không commit PDF gốc. B01/B02/B03 gốc, cùng B01/B02/B03 kiểm toán, đã kiểm tra hình. 19 trường cốt lõi B01 B02 B03 FY 2025 bản kiểm toán khớp số bản Q4 phát hành đầu tiên **từng VND**. Không kết luận các thuyết minh chưa xem không có thay đổi.
- Q4 B01/B02 thuộc phạm vi công ty chứng khoán **không có công ty con**, xác nhận tại Note 1 bản ký gốc PDF trang 19. Phạm vi tương đương nhóm để tổng hợp dashboard, không phải báo cáo hợp nhất có ký. Tiền khách hàng môi giới không được cộng vào B01/B03 doanh nghiệp.
- `reports/source-audits/VCI-2025Q4-asfiled-PwC-audited-2025-source-vnd.json`: **73 trường nguồn VND**; **26 phương trình kế toán/cầu dòng tiền**, dư đều 0 VND. `scripts/verify_vci_2025q4_original_vs_audited.py` kiểm chứng 19 trường kiểm toán và 4 negative controls. CI tài chính **`44924021204` PASS** trên nhánh thay đổi này.

## B01 B02 Q4/2025, VND
| Chỉ tiêu | Kết quả |
|---|---:|
| Tổng tài sản 31/12 | 36.005.864.835.815 |
| Nợ phải trả | 17.995.968.295.866 |
| Vốn chủ sở hữu | 18.009.896.539.949 |
| Tiền và tương đương tiền | 3.213.693.581.406 |
| Doanh thu hoạt động riêng Q4 | 1.526.308.619.569 |
| Chi phí hoạt động riêng Q4 | 619.386.029.157 |
| KQKD hoạt động riêng Q4 | 543.524.398.145 |
| Lợi nhuận trước thuế riêng Q4 | 543.679.284.091 |
| Lợi nhuận sau thuế riêng Q4 | 442.924.081.840 |
| Doanh thu năm 2025 | 4.980.201.525.108 |
| LNST năm 2025 | 1.341.954.506.958 |

## B03 riêng Q4/2025, chính xác VND
Cùng cơ sở nguồn 12M FY 2025 của công ty đã ký/PwC và 9M công ty đã ký:
| Dòng | 12M | 9M | Q4 riêng |
|---|---:|---:|---:|
| CFO | -8.790.735.982.232 | -5.239.067.626.738 | **-3.551.668.355.494** |
| CFI | -57.062.669.357 | -35.548.742.835 | **-21.513.926.522** |
| CFF | +7.317.720.300.250 | +3.167.896.300.250 | **+4.149.824.000.000** |
| Net cash | -1.530.078.351.339 | -2.106.720.069.323 | **+576.641.717.984** |
| Tiền đầu quý | | | **2.637.051.863.422** |
| Tiền cuối quý | | | **3.213.693.581.406** |
CFO+CFI+CFF = Net, tiền đầu + net = tiền cuối, cả hai phương trình **0 VND sai số**. Năm 2025 đã kiểm toán và bản Q4 gốc có 6 B03 nguồn chính xác cùng số.

## Thay đổi triển khai
- `data/financials-VCI.json`: cập nhật duy nhất Q4/2025, các giá trị VND/1.000.000 theo đơn vị website triệu VND; lưu CFO/CFI/CFF/net riêng quý, mở/đóng quý, các dòng 12M lũy kế và nhãn năm; không tạo dữ liệu sai đơn vị.
- `scripts/verify_vci_2025q4_original_vs_audited.py` và `.github/workflows/validate.yml`: regression nguồn/PwC/26 phương trình/4 lỗi giả lập.
- `scripts/inspect_vci_2025q4_original_and_audited_sources.py` + workflow đọc nguồn ký và kiểm toán.
- PR #125: chỉ được merge sau financial CI PASS. Chưa mặc định khẳng định website 45/45 SHA hay Pages production PASS trừ khi kiểm tra riêng.

## Điểm tiếp theo
1. Xác minh PR #125 merge main, checkpoint và production CI/status.
2. **VCI Q1/2026** nguồn ký gốc, rồi **VCI Q2/2026**. Q3/2026 đã PASS từ PR #121. Khi xong 7/7 VCI → VCK → các mã thiếu Q3.
3. MBB/VIX/GAS/VDS 7/7 PASS; GEG IDC hoàn tất nguồn với ngoại lệ B03 quý II theo quyết định người dùng (chờ BCTC kiểm toán FY2026), PLX mẹ Q3/2026 CFF bất thường +87.654.015.000 VND chưa có đính chính, để BLOCKED. Không làm lại kỳ PASS, không tải 2024, giữ tối đa 20 kỳ.
