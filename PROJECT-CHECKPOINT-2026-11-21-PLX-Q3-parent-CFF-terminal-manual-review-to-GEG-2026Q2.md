# CHECKPOINT — PLX Q3/2026 công ty mẹ B03 terminal manual review; tiếp tục GEG Q2/2026

Ngày 21/11/2026. Repository `kiemtimem12345/solieutaichinh`. Trước đó VIX 2025Q1→2026Q3 7/7 kỳ RIÊNG đã hoàn thành (main SHA f347b305d5f38f083469d0aff5259371a89b68da).

## Không thực hiện lại dữ liệu PLX đã đạt
- PLX Q3/2026 **hợp nhất** B01/B02/B03, cùng báo cáo hợp nhất bán niên 2026 soát xét, đã nghiệm thu đầy đủ và triển khai thành công; giữ nguyên.
- PLX Q3/2026 **công ty mẹ** B01/B02 đã đối chiếu nguồn ký gốc, cân đối 0 VND; riêng dòng B03 CFF bị bất nhất **trên bản PDF ký gốc**; không phát hành dòng tiền Q3 riêng công ty mẹ.

## Chứng cứ bất nhất nguyên gốc (riêng công ty mẹ)
- PLX original Petrolimex signed PDF 39 trang SHA256 `a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef`.
- Vietstock mirror same signed 39 scanned page images bytewise all 39/39 identical but PDF container sha khác `ab13686742234d95930b6c16e51300f7b2a2600e07919eb4b0a3464c820a6b6d`; **không có bản đính chính** trong hai nguồn này.
- B03 lũy kế 9M: mã 31 +844,158,780,900; 32 -1,134,759,693; 33 +71,733,162,995,138; 34 -65,128,441,186,058; 35 0; 36 -1,393,990,271,569; tổng **+6,053,755,558,718 VND**. Mã 40 in trên chính B03 **+5,966,101,543,718 VND**, sai **87,654,015,000 VND = 1.469200856835821%** của mã 40 in, vượt xa quy tắc tối đa 0.1%.
- CFO mã20 -3,435,516,597,061, CFI mã30 -2,575,747,123,895. Tổng CFO+CFI+**tổng cấu phần CFF** = mã 50 công bố +42,491,837,762 VND. CFO+CFI+**CFF in mã40** = -45,162,177,238 VND, khác mã50 bởi 87,654,015,000. Không được tự ý sửa mã 40 thành tổng thành phần dù phép tính gợi ý đó là lỗi in, vì chưa có bản sửa chính thức.
- Bán niên 2026 **công ty mẹ** KPMG soát xét cùng phạm vi đã xác minh PDF SHA256 `a7929fbbc64f8f7fd201c33df9d09f32098ea1829ead9d6ea39c434f8821cd2c`, B03 6M pp10–11; không giải quyết được mâu thuẫn mã 40 của báo cáo 9M.
- Văn bản giải trình BCTC Q3 số 2779/PLX-TCKT ngày 02/11/2026 trên HOSE không giải thích chênh CFF. Kiểm tra các từ khóa đính chính PLX Q3/2026 trên Petrolimex/HOSE đến 21/11/2026 chưa có nguồn sửa được xác minh; không khẳng định sẽ không bao giờ có.
- Dữ liệu PLX Q3 công ty mẹ B03 vẫn `issuer_original_visual_verified_b01_b02_b03_printed_cff_arithmetic_anomaly_blocked`. Cờ `automatic_extraction_exhausted` + `terminal_manual_review` chỉ áp dụng **ngoại lệ này**; tắt việc tự tải lại cùng hai PDF đã khớp 39 ảnh. Chỉ mở lại nếu doanh nghiệp có **bản B03 đính chính ký và xác minh SHA/page**, hay thuyết minh pháp lý làm rõ 87.654.015.000.
- CI `scripts/verify_plx_issuer_q3.py` yêu cầu tỉ lệ >0,1%, hai PDF giống ảnh, nguồn chưa đính chính, ngăn nâng trạng thái hoặc tự đưa CFO/CFI/CFF mẹ quý riêng lên site. Không được đánh dấu PLX Q3 mẹ B03 đã hoàn thành.

## Xác định hạng mục tiếp theo thực sự thiếu
- Đọc `data/financials-GAS.json`: GAS hợp nhất từ 2025Q1 đến 2026Q3 **7/7 các kỳ đã visual source PASS**, Q3 có thêm báo cáo riêng; KHÔNG làm lại.
- Đọc `data/financials-VDS.json`: VDS hợp nhất **7/7 các kỳ đã visual source PASS**, KHÔNG làm lại.
- Đọc `data/financials-GEG.json`: GEG 2026Q2 hợp nhất B01/B02/B03 lũy kế H1 source visual PASS, nhưng **CFO/CFI/CFF riêng Q2 vẫn null** bởi chênh đối chiếu tiền đầu năm Q1 bản đầu và H1 bản sau **11,422,218,903 VND**; cần giải thích chuyển phân loại tiền gửi/tài sản đảm bảo trên thuyết minh trước khi xuất dòng tiền quý riêng.
- Nguồn mới hữu ích phát hiện: chính **thuyết minh 11 GEG H1/2026** (báo cáo Q2 signed gốc) ghi **11,422,218,903 VND** tiền gửi có kỳ hạn dùng làm bảo lãnh, hạch toán **tài sản ngắn hạn khác (mã165)** tại số so sánh 01/01/2026; khớp chính xác chênh tiền tương đương đầu năm giữa nguồn Q1 và H1. Cần kiểm tra BCTC năm 2025 đã kiểm toán và lý do trình bày lại, phân biệt dòng tiền thực với phân loại phi tiền mặt, không chuyển số 11.422 tỷ vào CFO/CFI/CFF nếu không có bằng chứng.
- IDC 2026Q2 hợp nhất cũng có dòng tiền riêng quý null (vintage opening discrepancy) sau GEG; các kỳ Q3 được xác minh, không xử lý lại.

## Nguyên tắc tiếp tục
- Mã/kỳ đã PASS không tải xử lý lại. Chỉ xử lý GEG 2026Q2 cùng phạm vi hợp nhất, TT99/2025 và chế độ thực tế công bố; số liệu từ BCTC ký gốc, kiểm tra từng dòng và thuyết minh. Dung sai chỉ cho tổng phụ có nhiều nguồn chấp thuận <=0,1%, **không dùng** cho sai phân loại, phạm vi, tiền đầu kỳ hoặc cầu B03.
- Sau chỉnh sửa phải chạy CI nhánh, merge, kiểm thử website 45/45 SHA và Pages; lưu checkpoint bền vững.
