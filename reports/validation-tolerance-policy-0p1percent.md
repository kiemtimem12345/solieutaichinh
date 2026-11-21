# Quy tắc chuẩn hóa sai lệch không quá 0,1% — có đối chiếu nguồn (21/11/2026)

Áp dụng cho các **chênh lệch cộng trừ của các chỉ tiêu báo cáo** được công bố trên báo cáo gốc, khi tất cả điều kiện sau được đáp ứng:

1. Bản gốc của đúng mã, kỳ, loại báo cáo (riêng lẻ/hợp nhất), ngày, đơn vị và dấu đã được kiểm chứng. Ưu tiên bản công bố có chữ ký, sao lưu SHA-256 nguồn.
2. Giá trị **tổng công bố** phải được đối chiếu với **ít nhất hai nguồn dữ liệu công khai bổ sung**. Mỗi nguồn ghi rõ URL, kỳ, đơn vị, độ chính xác hiển thị; không giả định số làm tròn trùng là giống tuyệt đối VND. Không sử dụng nhiều tên miền sao chép cùng một giá trị làm chứng cứ pháp lý độc lập.
3. Không có bất nhất **ở độ chính xác từng nguồn thực sự công bố**. Nếu có số khác nhau, cần điều tra phiên bản/kỳ/phạm vi; không PASS tự động.
4. Với mỗi tổng phụ, tính `100 * ABS(tổng in - tổng cấu phần) / ABS(tổng in)` ở VND chính xác, không làm tròn sớm, điều kiện `<=0.1%`. Không áp dụng nếu mẫu số bằng 0, số nguồn không truy xuất được, sai dấu hoặc sai kỳ, hay vi phạm nguyên tắc số liệu kế toán cốt lõi.
5. Giữ **số gốc đã công bố**; không điều chỉnh để ép khớp; không thêm số tưởng tượng vào các dòng không in (ví dụ mã 133/317). Lưu sai lệch tuyệt đối, tỷ lệ, nguồn và cờ nhận diện.
6. Kết quả `PASS_WITH_TOLERANCE` **không có nghĩa nguồn gốc cộng đúng**. Trường `full_b01_component_arithmetic_passed` vẫn false; nếu có công bố đính chính sau này, phải đối chiếu lại và đổi kết quả.
7. Bảng cân đối tổng tài sản/nợ/vốn, B03 CFO/CFI/CFF, đối chiếu tiền đầu-cuối, đúng đơn vị, đúng phạm vi và các rủi ro trọng yếu không tự động được bỏ qua bằng ngưỡng 0,1%.
8. Chỉ đánh dấu hoàn tất bước khi CI, regression, test phát hiện nguồn chênh và smoke-test website thành công; checkpoint sau mỗi mã và không tái xử lý mã/kỳ đã nghiệm thu.

**Phạm vi áp dụng đã được xác minh trong code:** PLX B01 hợp nhất 2026-Q1; không tự thay hàng loạt trạng thái mã khác hay hạ các bộ kiểm tra kế toán nghiêm ngặt hiện có. Các mã khác phải đủ điều kiện đối chiếu nêu trên trước khi nhận quy tắc mới.

**Lưu ý quan trọng:** Hai sai lệch PLX (9.083.970.186 VND mã 130; 9.088.965.442 VND mã 310) vẫn tồn tại trong PDF. Chỉ được chấp nhận dùng **tổng số in gốc** sau khi xác nhận các bên thứ ba hiện thị giá trị phù hợp ở độ phân giải đã công bố.
