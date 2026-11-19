# CHECKPOINT — Kiểm tra thư mục dữ liệu IDC Q3 (19/11/2026, 22:30 ICT)

## Kết quả kiểm tra hiện trạng trước sửa metadata
- GitHub: `kiemtimem12345/solieutaichinh`, nhánh `main` commit `7a5b75405a123004e9c4edb91ae886a57b10f577`, PR #80 đã merge.
- Tệp **duy nhất** chứa IDC trong thư mục `data/`: `data/financials-IDC.json` (129975 bytes trước khi sửa metadata), **7 bản ghi hợp nhất từ Q1/2025 đến Q3/2026**, không có `data/IDC/Q3/` và không lưu PDF gốc bên trong `data/`. PDF nguồn nằm ở BSC/HNX hoặc bản HNX sao chép trên Vietstock, kèm URL/hash/chuỗi bằng chứng trong JSON.
- Phần mềm repo có các script `scripts/verify_idc_q3_2025_original.py`, `scripts/verify_idc_q3_2026_original.py`, các luồng `.github/workflows/inspect-idc-q3-2025-original.yml`, `.github/workflows/inspect-idc-q3-2026-pdf.yml`, và checkpoint chi tiết.
- Library `/Projects/so-lieu` (đã kiểm tra tên tài liệu ở cấp thư mục): chỉ có các ghi chú về IDC Q3 ngày 14/11 và binary retrieval 16/11, **chậm hơn** checkpoint đã merge trong GitHub ngày 19/11. Không được lấy các ghi chú Library cũ làm trạng thái cuối.

## IDC hợp nhất 2026-Q3 — PASS
- Tài sản 30/09/2026 **23,631,671,909,723 VND**; nợ **14,273,143,387,664**, vốn chủ **9,358,528,522,059** (B01).
- Doanh thu thuần riêng Q3 **2,075,575,029,891 VND**, LNTT **673,834,389,916**, LNST **540,374,922,785** (B02).
- B03 lũy kế **9 tháng**: CFO **211,600,221,432**, CFI **505,984,662,907**, CFF **-801,577,203,462** VND.
- **Riêng Q3** sau khi lấy 9M trừ H1 cùng phạm vi đã ký: CFO **216,619,259,342**, CFI **93,759,529,850**, CFF **-449,106,095,224**, dòng tiền thuần **-138,727,306,032 VND**.
- 113 fields trong JSON, **29** original-statement identity checks tại VND residual 0; standalone Q3 có **4** identity checks residual 0; `scripts/verify_idc_q3_2026_original.py` CI PASS.
- PDF gốc 70 trang, ký 28/10/2026; BSC issuer distribution https://www.bsc.com.vn/News/NewsAttachedFile/1632697-1 , SHA256 `dde75e3efe8a569a0d264b27f7d7a0d8a4edb4abdf22a56144e0847f2c8dc790`. HNX công bố 02/11/2026, xem phạm vi *hợp nhất*, **không phải công ty mẹ**. Q3 2026 hợp nhất đã hoàn thành, không chạy lại số gốc.

## IDC hợp nhất 2025-Q3 — đã xác minh B01/B02/9M B03, còn B03 riêng quý
- Tài sản **21,293,030,253,931 VND**, doanh thu thuần riêng Q3 **2,871,329,472,687**, LNST riêng Q3 **981,137,501,988** VND.
- PDF gốc HNX sao chép trong ZIP https://static2.vietstock.vn/data/HNX/2025/BCTC/VN/QUY%203/IDC_Baocaotaichinh_Q3_2025_Hopnhat.zip , 64 trang, ký 29/10/2025, PDF SHA256 `80c1b3dcb2e5469d4fb84c3a0cbd46c51f664ce7e07a2a0946e10b691ca92ce3`.
- 102 fields, **30** identity checks VND residual 0. CFO/CFI/CFF riêng Q3 **null** đúng nguyên tắc vì **Q2/2025 H1** chưa qua visual QA nguồn ký, không lấy 9M trừ bản auto chưa kiểm tra.
- 2025-Q4 standalone B03 đã PASS từ FY2025 minus 2025Q3 signed 9M, không cần kiểm tra lại.

## Phát hiện lỗi metadata và sửa
- Trong 2026-Q3 `source_validation.q3_standalone_cashflow_blocker` vẫn ghi “Q2 legacy chưa xác minh, không thể tính Q3”, trái với dữ liệu/số học 2026Q3 đã PASS sau PR #77.
- Lưu nguyên văn trạng thái chặn cũ ở `q3_standalone_cashflow_prior_blocker_resolved`; loại trường blocker đã lỗi thời; thêm `q3_standalone_cashflow_current_status` đồng bộ với status chính và chứng cứ PDF H1/Q3 4 exact checks.
- Thêm regression vào `scripts/verify_idc_q3_2026_original.py` để không xuất hiện lại sự mâu thuẫn trạng thái này. **Không sửa bất cứ số tài chính nào**, không thay website UI hoặc phạm vi báo cáo.

## Hệ thống và điểm tiếp tục
- CI trên main commit 7a5b754 đã PASS: validation run `44553341626`, website smoke `44553341725` **45/45 URL + SHA256 match** HTML/CSS/JS và 41 JSON (32 tài chính + 9 khác).
- Merge metadata repair PR chỉ sau khi CI PASS; sau merge xác minh website 45/45 lần nữa.
- **Điểm tiếp tục thật:** IDC Q2/2025 hợp nhất từ PDF/ZIP gốc, rồi Q1/2025; sau đó tính riêng Q3/2025 = 9M minus H1 signed. Ngoại lệ khác: IDC Q2/2026 standalone cash bridge **890,796,892 VND** do số tiền đầu năm H1 khác Q1/FY audited. Không được tự cân đối hay viết đè số gốc chỉ để tạo PASS.
- Chỉ từ Q1/2025, tối đa 20 kỳ mỗi mã, source unit VND normalized `triệu VND` (EPS VND/share), sai lệch tối đa 0,01%; tất cả số đạt chuẩn phải giữ checkpoint.
