# IDC HOÀN TẤT — chuẩn hóa nguồn Q1/2025–Q3/2026; ngoại lệ B03 Q2/2026 chờ kiểm toán FY2026

**Ngày hoàn thành:** 21/11/2026 (Asia/Ho_Chi_Minh)  
**Repository:** kiemtimem12345/solieutaichinh  
**Phương pháp:** áp dụng quy trình chấp nhận số doanh nghiệp đã công bố theo bản có ký, như trường hợp GEG mà người dùng đã duyệt; người dùng tiếp tục yêu cầu xử lý IDC. Quyết định ở cấp hồ sơ nguồn, không tự suy ra rằng người dùng chấp nhận biến số quý chưa có bằng chứng thành số đã kiểm toán.

## Đã đạt nguồn 7/7, không làm lại
Các báo cáo hợp nhất IDC Q1/2025 đến Q3/2026 đã xác minh B01/B02 và B03 lũy kế có ký. B03 Q3/2026 quý độc lập từ 9M−6M cùng phạm vi PASS, cash bridge chênh 0 VND. Các mốc tiền:
- Q1/2026 B03 3M (ký nguyên gốc, SHA256 `229a1ff9af9d3e1bffd777a0c9b92b4bd5cbee5bc02765f02bee5778c2b2085b`): CFO `197.524.137.001`, CFI `-68.608.251.477`, CFF `118.757.627.185`, net `247.673.512.709`, mở `553.052.678.239`, FX `3.304.755`, đóng `800.729.495.703` VND.
- Q2/2026 bản gốc B03 6M (SHA256 PDF `f0bee9c4554b166380098034650b09c0e45f85da55fd016086f0ef08a596354c`): CFO `-5.019.037.910`, CFI `412.225.133.057`, CFF `-352.471.108.238`, net `54.734.986.909`, mở `553.943.475.131`, FX `6.117.592`, đóng `608.684.579.632` VND.
- H1/2026 soát xét nguồn ký HNX 7/9 và BSC `https://www.bsc.com.vn/News/NewsAttachedFile/1599258-1` SHA256 `f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944`, PDF 72 trang: TM 3.1 p21 xác nhận TT99/TT43, TM 41 p71 giải thích điều chỉnh số mở `890.796.892` VND, dòng B03 **kỳ trước 2025** điều chỉnh tổng `0` VND.
- Q3/2026 B03 9M (SHA256 `dde75e3efe8a569a0d264b27f7d7a0d8a4edb4abdf22a56144e0847f2c8dc790`): CFO `211.600.221.432`, CFI `505.984.662.907`, CFF `-801.577.203.462`, net `-83.992.319.123`, mở `553.943.475.131`, đóng `469.934.018.621` VND. Quý III riêng đã xác thực từ 9M−6M CFO `216.619.259.342`, CFI `93.759.529.850`, CFF `-449.106.095.224`, net `-138.727.306.032`, cầu tiền đúng 0 VND.

## Ngoại lệ Q2/2026 kết thúc ở cấp công việc, không xác minh giả
Chênh lệch B03 mở năm: **+890.796.892 VND**, là **phân loại lại phi tiền tệ** được thể hiện trong TM41, không được tính thành khoản thu tài chính/quý II. Nếu 6M−3M, dòng quý II tạm tính CFO `-202.543.174.911`, CFI `480.833.384.534`, CFF `-471.228.735.423`, net `-192.938.525.800`, FX `2.812.837`; chênh lệch cầu tiền `890.796.892` vì hai phiên bản có đầu năm khác nhau. Chưa có **B03 quý I/2026 ký lại theo chính sách hợp nhất H1** và không thể lấy thay đổi dòng so sánh năm 2025 làm căn cứ xác nhận từng dòng CFO/CFI/CFF hiện hành.

Do vậy, **giữ các trường B03 quý II riêng là NULL**, không gán 0 hoặc số tạm tính như đã kiểm chứng. Các số B01/B02/B03 lũy kế nguồn phát hành giữ chính xác theo bản đã ký; không giả định vi phạm TT43/2026.

## Trạng thái cuối
`completed_issuer_source_verified_with_accounting_vintage_exception_pending_audited_fy2026`.

- **IDC đã hoàn tất việc chuẩn hóa nguồn theo quy trình đã chấp nhận**, không còn nằm trong vòng lặp tải PDF / OCR và tìm bản Q1 kỳ hiện hành liên tục.
- **Chỉ mở lại** khi IDICO công bố BCTC **kiểm toán hợp nhất năm 2026**, có công bố chỉnh sửa có ký, hoặc có số liệu cùng cơ sở TT43 trực tiếp chứng minh thay đổi.
- Kiểm toán năm 2026 thường công bố trong 2027; cần kiểm tra B01/B02/B03 12M và thuyết minh reclass, đối chiếu với 9M/6M đã ký, sửa chỉ tiêu liên quan nếu có nguồn và kiểm thử.

## Implementation links
- `data/financials-IDC.json`: `ticker_processing_completion`, thêm metadata Q1/Q2/Q3, giữ mọi giá trị numeric đã xác minh.
- `reports/source-audits/IDC-2026Q2-issuer-source-accepted-closure-pending-audited-FY2026.json`: báo cáo nguồn và số đối chiếu chính xác.
- `scripts/verify_idc_issuer_source_accepted_completion.py`: hồi quy VND, kiểm tra nguồn và cấm số quý II tự suy diễn.
- `scripts/audit_all_statement_coverage.py`: IDC và GEG được phân loại hoàn thành với ngoại lệ, không còn trong hàng đợi ưu tiên.
- `docs/accounting-regime-and-disclosure-transition-sop-2025-2026.md`: SOP cập nhật mục 8.
- `.github/workflows/validate.yml`: chạy verifier mới cạnh các kiểm thử cũ.
