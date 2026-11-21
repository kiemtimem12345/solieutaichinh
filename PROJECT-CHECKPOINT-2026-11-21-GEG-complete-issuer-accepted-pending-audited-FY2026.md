# CHECKPOINT GEG — hoàn thành theo nguồn phát hành, ngoại lệ được chấp nhận (21/11/2026)

## Quyết định
Người dùng trực tiếp chấp thuận ngày 21/11/2026: dùng số liệu **đã công bố và ký** của Công ty CP Điện Gia Lai làm chuẩn theo từng phiên bản, **đóng trường hợp GEG** và **đánh dấu hoàn thành**, chỉ rà soát/hiệu chỉnh khi doanh nghiệp công bố BCTC **kiểm toán hợp nhất năm 2026** hoặc đính chính có ký. Không lặp lại truy tìm số dư 31/03 trước thời điểm đó.

### Kết quả đã hoàn thành
- 7/7 kỳ hợp nhất Q1/2025–Q3/2026 đã có báo cáo nguồn và kiểm chứng riêng; các số B01/B02 và B03 lũy kế chính xác với bản phát hành tương ứng.
- BCTC H1/2026 EY soát xét bản doanh nghiệp ký, 74 trang (SHA256 `c5fcba1374cea2e2fc6e82eb66ccd4cf49320bd4a412c4c3f834d60c16ba700e`), B03 PDF trang 16–17: CFO **707.905.751.019 VND**, CFI **−734.466.295.121 VND**, CFF **51.927.115.815 VND**, net **25.366.571.713 VND**, số dư đầu **74.942.444.345 VND**, FX **13.217.270 VND**, cuối **100.322.233.328 VND**. Cân 0 VND.
- Thuyết minh 37 PDF trang 73: tái phân loại đầu kỳ **11.422.218.903 VND** khỏi tiền và tương đương tiền sang tài sản ngắn hạn khác. TM22 và TM25 xác nhận tiền gửi có ràng buộc theo các hợp đồng tín dụng. Bản quý II ban đầu và EY H1 khác chi tiết mã 111/112, lưu theo phiên bản riêng.
- Bản Q2 ban đầu 6M (CFO **722.160.976.132**, CFI **−732.448.267.884**, CFF **35.658.808.670**, cuối **100.327.178.533 VND**) vẫn được giữ trong các trường nguồn production **đúng với phiên bản báo cáo ký ban đầu**. Bản EY đã soát xét được lưu làm tham số chuẩn **6M ưu tiên đối chiếu**, chưa thay giá trị của phiên bản ban đầu một cách thiếu nhãn.
- Q3/2026 signed 9M và EY H1 cùng cơ sở cho số quý III đã kiểm tra: CFO **448.662.906.453 VND**, CFI **−639.871.926.621 VND**, CFF **186.959.810.890 VND**, net **−4.249.209.278 VND**, FX **−15.900.229 VND**, opening **100.322.233.328 VND**, closing **96.057.123.821 VND** — residual **0 VND**; lưu bảng cầu nối riêng, không ghi đè số quý III gốc khi chưa chuyển đồng bộ phiên bản.

## Ngoại lệ được phép đóng ở cấp công việc, không giả nhận số chưa công bố
B03 **riêng quý II/2026** của GEG không được phát hành độc lập cùng phương pháp soát xét. Phép trừ H1−Q1 gốc có sai khác cầu tiền đúng **−11.422.218.903 VND**, do thiếu số dư tiền bị hạn chế tại 31/03/2026; người dùng đã chấp thuận **nguồn số thực tế** và chấp nhận hồ sơ nguồn này là **hoàn thành có ngoại lệ**. Không ghi số 0 hay số Q2 độc lập thiếu chứng cứ. Các trường `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow`, `net_cash_change` riêng Q2 vẫn `null`; không biến sai khác trình bày thành giao dịch tiền.

**Trạng thái cuối:** `completed_issuer_accepted_exception_pending_fy2026_audited_recheck`. Không đưa mã GEG vào hàng đợi tìm lỗi hàng ngày nữa. Ngoại lệ chỉ kích hoạt lại nếu nguồn kiểm toán năm 2026/đính chính có ký mâu thuẫn số liệu hiện lưu hoặc bổ sung bảng cầu nối Q1 cùng cơ sở.

## Hệ thống hóa
- `data/financials-GEG.json`: `ticker_processing_completion`; `2026-Q2.source_validation.case_closure_status` và mốc bản EY; `2026-Q3.source_validation.reviewed_h1_comparator_accepted_under_geg_completion`.
- `reports/source-audits/GEG-2026Q2-accepted-issuer-vintage-closure-pending-audited-FY2026.json`: nguồn chính thức, số đối chiếu và quyết định người dùng.
- `scripts/verify_geg_issuer_accepted_completion.py`: kiểm tra nguồn, 6M EY, 9M GEG và trạng thái chốt.
- `scripts/audit_all_statement_coverage.py`: GEG được báo đã đóng, không còn liệt kê như việc phải xử lý; IDC vẫn mở.
- `docs/accounting-regime-and-disclosure-transition-sop-2025-2026.md`: quy tắc nghiệp vụ mới; chỉ áp dụng từng mã có user consent rõ ràng.

## Nhiệm vụ sau khi công bố kiểm toán FY2026
Khi GEG công bố **BCTC hợp nhất kiểm toán năm 2026** (thường vào năm 2027), truy xuất báo cáo từ nguồn doanh nghiệp/HOSE, kiểm tra B01/B02/B03 12 tháng, khoản tiền gửi bảo đảm, số đầu kỳ và các thuyết minh trình bày lại; đối chiếu 12M với 9M và 6M EY theo cùng version. Nếu điều chỉnh, lưu nguồn SHA/trang, sửa cặp kỳ liên quan, chạy CI + web smoke, checkpoint mới. Không mở lại riêng vì số dư tháng 3 vẫn không có trong báo cáo cũ.
