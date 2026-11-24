# Nhật ký dự án — 24/11/2026

## Quy tắc bắt buộc khi mở cuộc trò chuyện mới
Đọc file này trên main và kiểm tra commit mới nhất trước khi tiếp tục. Chỉ xử lý bước chưa đạt; mỗi mã/kỳ đạt phải ghi nhật ký, nguồn, kiểm thử, commit và điểm tiếp theo. Không coi OCR hoặc dữ liệu có sẵn là PASS nếu chưa đủ chứng cứ. Ngoại lệ đưa vào hàng chờ và tiếp tục mã khác theo yêu cầu. Phạm vi Q1/2025–Q3/2026, tối đa 20 kỳ, không nhập 2024. Biểu đồ cột xanh bo góc và đường, đơn vị rõ ràng, trục quý.

## Trạng thái kiểm tra thực tế
- CTG: commit dd9f6adb3085539f08765e504d8dcb6b1ab0cf53 ghi đóng 7 kỳ; chưa kiểm tra lại CI trong lượt này.
- BID: 7/7 bản ghi có trạng thái nguồn ký gốc đã xác minh B01/B03/B04; không làm lại các kỳ này nếu không có mâu thuẫn.
- TCB: 7/7 bản ghi; chưa sửa lỗi OCR được báo cáo ở lượt trước (Q3 cho vay khách hàng 656641278 và số dư tiền cuối kỳ bị loại); cần xác minh lại PDF gốc trước khi sửa. Thiếu B04 các kỳ 2025; không đánh dấu hoàn thành.
- MBB: Q3/2026 đã có trạng thái xác minh ảnh nguồn ký gốc và 27 phép đối chiếu; giữ nguyên. Sáu kỳ Q1/2025–Q2/2026 thiếu CFF riêng quý và tiền đầu/cuối kỳ; Q3/Q4 2025 thiếu CFI riêng quý. Chuyển xử lý MBB, bắt đầu Q1/2025 B04, sau đó lần lượt các kỳ còn thiếu.
- ACB và SHB: mỗi mã có 6/7 bản ghi, thiếu Q3/2026; xử lý sau MBB.

## Điểm tiếp tục
MBB Q1/2025 B04: https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/MBB_Baocaotaichinh_Q1_2025_Hopnhat.pdf . Đối chiếu PDF ký gốc, đơn vị triệu VND, CFO/CFI/CFF và cầu tiền bao gồm FX nếu có. Chỉ ghi dữ liệu khi đủ nguồn; kiểm thử trước khi đóng kỳ.

Lượt này đã đọc snapshot main, kiểm kê thiếu trường. Chưa thay đổi số liệu, chưa chạy CI/CD.

## MBB Q1/2025 — B04 nguồn gốc đã xác minh
PDF 60 trang, ký 24/04/2025, ảnh PDF trang 7–8 (đếm từ 1), B04a/TCTD-HN. Nguồn URL ở trên. Triệu VND: CFO -26075011; CFI -176955; CFF 2198563; net -24053403; opening 97040275; closing 72986872. Hai đẳng thức dòng tiền dư 0. CFO cũ 18186686 là thu lãi nhận được; CFI cũ -105882 cũng sai. Chưa sửa production vì Q2 trở đi phụ thuộc lũy kế Q1 sai. Điểm tiếp theo: đọc H1/2025 soát xét và Q2/2025 ký gốc B04, chuẩn hóa Q1+Q2 đồng bộ, kiểm thử rồi cập nhật. Không đọc lại B04 Q1 trừ khi mâu thuẫn. Chưa chạy CI/CD.
