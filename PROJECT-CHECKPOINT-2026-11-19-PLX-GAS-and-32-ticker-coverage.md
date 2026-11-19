# CHECKPOINT — BCTC 32 mã: PLX Q3/2026 và GAS Q1/2025 — 19/11/2026

## Kết quả đã hoàn thành và lưu lên production (không làm lại nếu không có mâu thuẫn mới)

### PLX Q3/2026
- PR #40: Hai bản ghi Q3/2026, **hợp nhất** và **công ty mẹ**. Số LNST quý từ văn bản giải trình chính thức số 2779/PLX-TCKT ngày 02/11/2026: hợp nhất **1.363.096.640.781 VND**; công ty mẹ **1.315.029.909.162 VND**.
- PR #42: Bổ sung **31 trường B01/B02** Q3/2026 **công ty mẹ** từ PDF BCTC gốc phát hành 30/10/2026, các phương trình cân đối kiểm tra đến từng VND. B01 tại 30/09; B02 dùng cột phát sinh riêng **Quý 3/Năm nay**, không dùng 9 tháng.
- B01 mẹ: tổng tài sản 73.735.716.400.522 VND, nợ 49.645.102.958.279 VND, VCSH 24.090.613.442.243 VND.
- B02 mẹ: doanh thu thuần 84.352.714.995.460 VND, lợi nhuận trước thuế 1.529.964.370.494 VND, LNST 1.315.029.909.162 VND.
- **B03 mẹ vẫn CHẶN**: CFF in báo cáo 5.966.101.543.718 VND; tổng các dòng CFF = 6.053.755.558.718 VND; sai lệch **87.654.015.000 VND**. CFO + CFI + CFF từ các thành phần mới khớp dòng tiền thuần in. Không công bố B03 quý riêng, không tự sửa số in; tìm H1/2026 cùng phạm vi và lời giải thích chính thức.
- B01/B02 mẹ được đối chiếu **văn bản PDF + phép tính**, nhưng **ảnh trang PDF chưa xem được do Cache miss**; không ghi nhãn visual PASS.
- B01/B02/B03 **hợp nhất** Q3 vẫn thiếu PDF gốc truy xuất được; mới xác minh LNST hợp nhất từ văn bản giải trình, không suy đoán các chỉ tiêu còn lại.
- BCTC hợp nhất Q2/2026 PLX trong JSON cũ dựa OCR chưa rà ảnh; nếu số liệu từ nguồn soát xét H1 khác bản gốc cần kiểm tra phân loại lại và nguồn chính thức, **không** dùng ước tính bên thứ ba để ghi đè.
- Kiểm thử: PR #40 `44464968412` (attempt 2) 45/45 site PASS; PR #42 `44466078779` CI PASS và `44466078741` website 45/45 PASS.

Nguồn:
- https://files.petrolimex.com.vn/files/6783dc1271ff449e95b74a9520964169/application%3Dpdf/041ce27107d94176a4c6a3356a250824/20261102%20-%20PLX%20-%20Van%20ban%20giai%20trinh%20BCTC%20Quy%203%20nam%202026.pdf
- https://files.petrolimex.com.vn/files/6783dc1271ff449e95b74a9520964169/application%3Dpdf/5011693c3c5240a0833bfaea0e7983a5/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20m%E1%BA%B9%20Q3%20nam%202026.pdf

### GAS Q1/2025 hợp nhất
- PR #43: Khôi phục từ *PDF công bố chính thức của GAS 29/04/2025* (bản Vietstock mirror) **42 chỉ tiêu B01/B02/B03** trong JSON; đơn vị lưu triệu VND, EPS đồng/cổ phiếu.
- Báo cáo công bố đính chính 16/06/2025 là **thuyết minh số 37 theo bộ phận thiếu cột Các hoạt động khác**; không phải thay số tổng B01/B02/B03. Nguồn đính chính đã liên kết riêng.
- B01: tài sản 82.020.779.538.795 VND; nợ 17.693.590.948.680 VND; VCSH 64.327.188.590.115 VND. B02 Q1: doanh thu thuần 25.675.428.574.505 VND, LNTT 3.428.885.485.800 VND, LNST 2.762.782.490.472 VND.
- B03 Q1: CFO 4.148.471.083.342 VND, CFI -1.694.772.666.608 VND, CFF +145.909.966.728 VND, net +2.599.608.383.462 VND; tiền đầu kỳ 5.567.998.965.715, FX -952.781.220, cuối kỳ 8.166.654.567.957. Q1 lũy kế = phát sinh quý.
- **15/15 phép số học khớp từng đồng**, gồm cân đối tài sản, B02, B03, cấu phần CFI/CFF và cầu tiền cuối kỳ. B03 đầu kỳ khác so sánh B01 ngày 01/01/2025 khoảng 15.534.247 VND; giữ đúng hai nguồn theo báo cáo, không tự chỉnh.
- **PDF screenshot Cache miss**, đánh dấu `original_issuer_disclosure_text_reconciled_visual_pending`, tuyệt đối không ghi visual PASS.
- GAS 2025-Q2 đến 2026-Q2 vẫn thiếu nhiều chỉ tiêu; GAS Q3/2026 hai phạm vi đã được kiểm chứng trước, không làm lại.
- PR #43 CI `44467091046` PASS, web smoke `44467091030` PASS 45/45 sau merge.

Nguồn:
- https://static2.vietstock.vn/vietstock/2025/4/29/20250429_20240429___gas___cbtt_bctc_q1_2025_hop_nhat.pdf
- https://static2.vietstock.vn/vietstock/2025/6/17/20250616___gas___cbtt_dinh_chinh_bctc_quy_1_2025_hop_nhat.pdf

## Kiểm kê hiện trạng 32 mã × 7 kỳ Q1/2025–Q3/2026
- PR #39: tạo `scripts/audit_all_statement_coverage.py` + GitHub Actions. PR #40 sửa phân loại để **không gọi báo cáo riêng lẻ/chưa rõ phạm vi là mất dữ liệu**.
- Run `44464968336`: 164/224 cặp mã-kỳ hợp nhất được nhận diện; **21 cặp không có bản ghi**, **28 có bản ghi nhưng phạm vi chưa xác nhận**, **11 chỉ có bản ghi riêng lẻ**. Chỉ có 7/32 mã có ghi nhận đủ bảy kỳ hợp nhất; không có nghĩa đủ chi tiết hoặc được kiểm chứng.
- **MBB** Q1/2025–Q2/2026 KQKD hợp nhất đã PASS 48/48 phương trình (PR #38), không trích xuất lại; Q3/2026 vẫn chưa cập nhật.
- **VDS Q3/2026** chưa có bản ghi hợp nhất trên site; **IDC Q3/2026** chưa có bản ghi; GEG Q3/2026 cả hai phạm vi đã PASS, nên ưu tiên các kỳ trước còn thiếu thay vì làm lại Q3.
- Các báo cáo SHS/VIX/VND/TCX/VCK phải được phân loại đúng công ty mẹ/hợp nhất/không rõ trước khi điền dữ liệu.

## Điểm tiếp tục
1. **PLX**: tìm BCTC Q3/2026 hợp nhất gốc và soát xét H1/2026 đúng phạm vi; xác minh bất nhất CFF mẹ 87.654.015.000 VND trước khi đăng B03 hoặc trừ ra quý riêng.
2. **GAS**: từ Q2/2025 (đã khôi phục Q1/2025), tìm báo cáo hợp nhất gốc và rà B01/B02/B03, bảo toàn Q3/2026 đã xác nhận.
3. **VDS Q3/2026** → **GEG các kỳ cũ còn thiếu** → **IDC Q3/2026**, từng mã/kỳ/phạm vi đến khi số nguồn đạt chuẩn.
4. Các nhóm ngân hàng (ACB/BID/CTG...) và CTCK còn các dòng KQKD trống: áp dụng SOP MBB nhưng không tự điền giá trị thiếu bằng 0.

## Nguyên tắc bất biến
- GitHub `kiemtimem12345/solieutaichinh` nhánh `main` là nguồn production; không upload data riêng SFTP vào public_html vì Git auto-deploy có thể xóa.
- BCTC từ Q1/2025, tối đa 20 kỳ/mã. Dung sai số liệu <=0,01%. Giữ dấu âm, đúng VND/triệu/tỷ; phân biệt quý và YTD. Không gộp công ty mẹ với hợp nhất. Không suy đoán EPS từ mã chỉ tiêu 70.
- Checkpoint ngay phần hoàn tất; không xử lý lại đã được xác minh trừ khi có nguồn mâu thuẫn sau này.
- Website nguyên bản không được đổi bố cục. Smoke 45/45 URL/SHA256 và CI phải PASS sau thay đổi.
