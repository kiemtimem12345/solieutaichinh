# CHECKPOINT — VCI Q2/2026 nguồn ký gốc + PwC H1, chốt đủ 7/7 — 22/11/2026

## Điểm tiếp tục
- Repository: `kiemtimem12345/solieutaichinh`; PR #127; nhánh `work/vci-2026q2-original-reviewed-h1-bridge-20261121`.
- 2025Q1/Q2/Q3/Q4, 2026Q1, 2026Q3 đã merge PASS (PR #121–126); kỳ cuối **2026Q2** vừa được kiểm toán nguồn. KHÔNG trích xuất lại các kỳ đã hoàn thành.
- Financial CI PR #127 trước checkpoint commit 5d68ba47ab6b8623029c6bd544e5c86ef1e2e344, workflow **44925460124**, kết quả **success**. Sau chỉnh metadata cần kiểm tra CI ở commit cuối, chỉ merge khi PASS.
- Data `data/financials-VCI.json`, row 2026-Q2 đã cập nhật 69 trường B01 B02 B03 nguồn VND + trường quý riêng thành đơn vị triệu VND. Không cập nhật các hàng Q1–Q4 2025, Q1/Q3 2026.
- Source ledger `reports/source-audits/VCI-2026Q2-original-reviewed-H1-and-Q1-cash-bridge-vnd.json`; 69 trường nguyên bản VND, **31 phương trình** sai số 0 VND; regression `scripts/verify_vci_2026q2_signed_h1_q1_bridge.py` gồm 4 negative controls. Regression Q3 trước đây có giả định Q2 B03 quý riêng NULL, đã sửa `scripts/verify_vci_2026q3_h1_reviewed_cash_bridge.py` để kiểm tra Q2 giờ đã có nguồn signed Q1 kết hợp signed/reviewed H1.

## Nguồn đã xác nhận trước đó
- BCTC CTCK VCI Q2/2026 bản phát hành nguồn gốc (48 trang/17.064.259 byte), SHA256 `a8fec422bac195c1b4d9743a995da35ec5066fa6dc0f951e6fbb36f2218823b5`, Vietstock `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCI_Baocaotaichinh_Q2_2026_1.pdf`; bản HOSE `https://staticfile.hsx.vn/Uploads/UploadDocuments/2480835/20260720%20-%20VCI%20-%20BCTC%20Q2.2026-CBTT.pdf`. B01 p5–7, B02 p10–12, B03 p13–14, Note1 p19 không có công ty con.
- H1/2026 được PwC soát xét (98 trang/15.650.240 byte), SHA256 `1ea814d02563a136d11d718c62c1ffc3c08463ffaf12369c517111cd26f6b9af`, `https://static2.vietstock.vn/vietstock/2026/8/14/20260813___vci___bctc_6t_nam_2026___cbtt_2.pdf`, B03 p16–17. B03 6M hai nguồn khớp từng VND. Nguồn hình PDF trong Actions run `44918419435`, artifact `14712970890`.
- Q1/2026 VCI ký gốc đã xác minh PR #126; source audit `reports/source-audits/VCI-2026Q1-issuer-signed-original-B01-B02-B03-vnd.json`. Phạm vi báo cáo công ty không có công ty con; không tự đặt là báo cáo hợp nhất đã phát hành. Không bao gồm tiền khách hàng môi giới vào tiền doanh nghiệp.

## Số B03 riêng Q2/2026, VND
| Chỉ tiêu | 6M/H1/2026 | 3M Q1/2026 | Riêng Q2/2026 |
|---|---:|---:|---:|
| CFO | -4.539.879.183.965 | -2.900.034.543.773 | **-1.639.844.640.192** |
| CFI | -26.547.106.493 | -19.436.706.493 | **-7.110.400.000** |
| CFF | +5.001.663.109.500 | +1.754.026.860.500 | **+3.247.636.249.000** |
| Thay đổi tiền thuần | +435.236.819.042 | -1.165.444.389.766 | **+1.600.681.208.808** |
| Tiền đầu Q2 | | | **2.048.249.191.640** |
| Tiền cuối Q2 | | | **3.648.930.400.448** |
- CFO+CFI+CFF − net = **0 VND**; Tiền đầu Q2 + net − Tiền cuối Q2 = **0 VND**; nguyên tắc kỳ, đơn vị VND/triệu đồng và dấu được kiểm chứng nguồn.
- B01 Q2: tài sản **39.727.391.134.343 VND**, nợ **22.589.496.145.882 VND**, vốn CSH **17.137.894.988.461 VND**. B02: doanh thu quý **1.175.848.817.294 VND**, LNST quý **250.588.812.865 VND**; 6M PAT 591.318.693.953 VND = Q1 + Q2.
- CI toàn bộ kiểm thử tài chính ở nhánh PASS sau khi thêm dữ liệu và sửa assertion lỗi lịch sử, rồi cập nhật metadata để bỏ cờ lỗi 'not Q2 standalone', cần xác nhận CI commit cuối.

## Bước tiếp theo bắt buộc
1. Chạy PASS toàn bộ PR #127 tại SHA cuối; merge PR #127 vào main, kiểm tra dữ liệu 7 kỳ và checkpoint. Đừng gộp nếu CI lỗi.
2. Chuyển **VCK** (ưu tiên Q1/2025–Q3/2026, không nạp 2024; đọc checkpoint VCK gần nhất trong repo/Library và không lặp kỳ đã PASS).
3. Sau VCK: các mã còn thiếu, kiểm thử dashboard và trạng thái deploy khi có đủ chứng cứ. GEG/IDC giữ đóng hồ sơ có ngoại lệ Q2 2026 theo quyết định người dùng, PLX Q3/2026 công ty mẹ B03 CFF chênh 87.654.015.000 VND > 0,1%, chờ nguồn đính chính ký.
