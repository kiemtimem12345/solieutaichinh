# CHECKPOINT — VCI Q2/H1 2026, truy hồi PDF giới hạn thời gian (21/11/2026)

## Điểm tiếp tục chính xác
- Nhánh main trước sửa: commit `80d8e13beebbab7403935774f7f635a30cc9c29a`, PR #120 merged. PR #119 đã xác thực 64 trường VCI Q3/2026 B01/B02 và B03 **lũy kế 9M** từ nguồn HOSE, không tái trích xuất.
- Các kỳ VCI 2025Q1–2026Q2 còn chờ đọc nguồn ký gốc. Riêng B03 Q3/2026 quý độc lập còn NULL vì thiếu B03 6M cùng phạm vi/kỳ theo nguồn gốc.
- Runner PR #120 workflow `44914776784`, job `136877918125` khởi chạy tải HOSE Q2; lần đầu gặp `TimeoutError: The read operation timed out` lúc 14:41:02 UTC (21/11), job bị **cancelled** 14:48:20 UTC. Không có xác minh B03 H1/Q2 thành công, không được nâng kết quả thành PASS.
- Công cụ trình đọc web tải bản HOSE / Vietstock 17MB–15MB bị chặn do dung lượng; bản tin/báo cáo phân tích thứ ba chỉ cho dữ liệu làm **đối chiếu định hướng**, không thay số ký gốc.

## Thử thay thế (nguồn ký gốc, không sửa dữ liệu)
- Sửa `scripts/inspect_vci_2026h1_signed_pdf_sources.py`: curl có tường thời gian **80s/source**, connect 12s, rate-stall 16s, subprocess max 92s; chỉ có 3 đầu nguồn, không retry vô hạn; thử nguồn H1 HOSE, sau đó Q2 Vietstock, sau đó Q2 HOSE.
- Chỉ công bố kết quả tìm thấy nếu kiểm tra `%PDF-`, byte size <= 45MB, SHA256, `pdfinfo` và `pdftotext` hàng dữ liệu thành công. File PDF tạm xóa theo runner, không commit nguyên văn.
- `.github/workflows/inspect-vci-2026h1-original.yml` chạy khi mở PR để thực thi trong runner Linux, timeout 8 phút. Job **FAIL CLOSED** nếu thiếu H1 hoặc Q2 có hàng dữ liệu đọc được; không coi lỗi tải là thành công hay điền 0.
- Dù job thành công đọc text, vẫn cần kiểm tra đơn vị VND/triệu VND, B03 CFO/CFI/CFF/net và đầu/cuối, xác thực hình và phiên bản soát xét trước khi cập nhật các trường VCI. Cầu tiền Q3 phải bằng 0 VND sau 9M−6M đúng phạm vi.
- Các báo cáo VCI nguồn gốc: HOSE H1 13/08/2026 `https://staticfile.hsx.vn/Uploads/UploadDocuments/2488911/20260813%20-%20VCI%20-%20BCTC%206T%20nam%202026%20-%20CBTT.pdf`; HOSE Q2 20/07/2026 `https://staticfile.hsx.vn/Uploads/UploadDocuments/2480835/20260720%20-%20VCI%20-%20BCTC%20Q2.2026-CBTT.pdf`; Vietstock Q2 `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCI_Baocaotaichinh_Q2_2026_1.pdf`.

## Giữ nguyên các kết quả đã đóng
- MBB, VIX, GAS, VDS: 7/7 kỳ đã PASS theo checkpoints.
- GEG: case hoàn thành theo nguồn ký, PR #117; Q2 B03 quý riêng NULL, chỉ xét lại khi kiểm toán FY2026 / nguồn đính chính.
- IDC: case hoàn thành 7/7 theo nguồn ký, PR #118; Q2 B03 quý riêng NULL do TT99/TT43, chỉ xét lại khi kiểm toán FY2026 / đính chính.
- PLX Q3/2026 **công ty mẹ B03** ngoại lệ CFF 87.654.015.000 VND (1,4692%), > ngưỡng 0,1%; chờ đính chính công ty có ký, không sửa đoán.
- Kế tiếp sau VCI: VCK, rồi các mã thiếu Q3/2026; mỗi mã xong mới cập nhật checkpoint. Không hợp thức số quý độc lập khi thiếu bản cùng cơ sở.

## Nguyên tắc QA
- 32 mã × 7 quý (Q1/2025–Q3/2026); tối đa lưu 20 kỳ, không giữ 2024.
- Sai số ≤ 0,1% chỉ áp dụng cho tổng phụ có nguồn đối chiếu độc lập, **không áp dụng** cầu tiền, dấu, phạm vi, kỳ và đơn vị.
- Chỉ merge dữ liệu numeric sau B01/B02/B03, phép kiểm toán, financial CI, smoke website và Pages đạt. Nhánh sửa công cụ này chỉ đụng công cụ/triggers/checkpoint, không sửa `data/financials-*.json`.
