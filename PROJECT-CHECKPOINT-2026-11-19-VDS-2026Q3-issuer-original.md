# CHECKPOINT — VDS 2026-Q3 hợp nhất từ báo cáo gốc 30/10/2026

## Nguồn và trạng thái
- Tiếp tục sau GAS Q3/2026 B02 9M xác minh chênh lệch H1 10.160.150.278 VND; PR #57 merged commit `778ecc8`; website 45/45 PASS. Không lặp GAS Q1–Q3 các kỳ đã kiểm tra.
- Nguồn **Rồng Việt Securities** chính thức, BCTC hợp nhất Quý III năm 2026, ngày ký 29/10/2026, công bố 30/10: https://www.vdsc.com.vn/data/api/app/file-storage/0a48e73d-8e80-4aeb-52c9-08df35c2eb9d/VDSC_Cong%20bo%20BCTC%20HN%20Quy%203.2026.pdf?downloadFrom=ManagementDocument-1061
- Nguồn HOSE độc lập (công bố kèm giải trình): https://staticfile.hsx.vn/Uploads/UploadDocuments/2510196/20261030%20-%20VDS%20-%20BCTC%20HN%20Quy%203%20nam%202026%20va%20Giai%20trinh%20CLLN.pdf
- PDF gốc có trang thông báo và trang scan. Kiểm tra ảnh nguồn PDF trang 6–10 (B01), 11–13 (B02), 14–16 (B03). Dữ liệu text HOSE hỗ trợ đối chiếu, không thay nguồn gốc bằng OCR chưa kiểm chứng.
- Trước thay đổi: `data/financials-VDS.json` chỉ có sáu kỳ 2025Q1–2026Q2; nhiều kỳ cũ còn `auto_extracted_pending_visual_review`, **không coi là PASS**.

## Mới khôi phục VDS hợp nhất Q3/2026 (đơn vị VND từ PDF gốc)
- **B01 30/09/2026**: tổng tài sản `7.424.891.063.002`; tổng nợ `4.612.624.799.039`; vốn chủ `2.812.266.263.963`; tiền và tương đương `871.526.568.802`.
- **B02 riêng Quý III/Năm nay** theo biểu mẫu CTCK (không dùng doanh thu công nghiệp): doanh thu hoạt động `192.250.618.894`; chi phí hoạt động `260.004.749.624`; doanh thu tài chính `2.045.269.763`; chi phí tài chính `20.886.146.850`; chi phí quản lý `46.615.307.188`; lỗ trước thuế `-133.921.713.724`; chi phí thuế âm `-21.812.358.624`; lỗ sau thuế `-112.109.355.100`; LNST cổ đông mẹ `-103.872.007.558`; LNST cổ đông thiểu số `-8.237.347.542`; EPS âm `-382` VND/cp.
- **B03 9 tháng lũy kế:** CFO `284.201.617.114`, CFI `-89.200.647.564`, CFF `-320.450.000.000`; dòng tiền thuần `-125.449.030.450`; tiền đầu năm `996.975.599.252`, cuối kỳ `871.526.568.802` VND.
- **Đặc biệt CTCK:** tiền khách hàng tại ngân hàng **ngoài B01** `635.318.404.512` VND và biến động tiền khách hàng `-1.112.807.615.606` VND được lưu trong các trường độc lập có tiền tố `client_brokerage_`; không cộng chung vào cash_and_equivalents hay CFO công ty.
- **Dòng tiền riêng Q3** chưa tính vì cần B03 H1/2026 hợp nhất đã xác minh và quy đổi YTD 9M-6M. Không dùng Q2 auto-extracted chưa qua QA để suy diễn; để trạng thái `deferred`.
- Chính xác 90 trường mới được nhập vào một record `2026-Q3`, `unit=triệu VND` trừ EPS; 21 đẳng thức kế toán tới đồng VND có residual 0.
- `scripts/verify_vds_q3_2026_source.py` regression 90 trường/21 đẳng thức, kiểm tra dấu âm thuế và cách tách tiền khách hàng, `.github/workflows/validate.yml` chạy test mới.
- Các kỳ VDS cũ 2025-Q1–2026-Q2 **không bị chỉnh**, do đang cần kiểm tra từ nguồn gốc. Dữ liệu Q3 không bị trộn phạm vi riêng lẻ.

## Lịch trình tiếp
1. Merge PR data mới khi CI PASS; website 45/45 byte-for-byte SHA PASS sau merge, lưu commit sản xuất.
2. Kiểm tra/chuẩn hóa tiếp VDS Q2/2026 hợp nhất B03 H1 (hiện auto-extracted pending visual QA) để tính B03 riêng Q3. Sau đó kiểm tra các kỳ VDS cũ 2025Q1–2026Q1 lần lượt (người dùng yêu cầu từng mã hoàn tất trước khi qua mã khác).
3. Chỉ chuyển sang GEG các khoảng trống (không làm lại GEG Q3/2026 PASS) và IDC Q3/2026 sau khi VDS hoàn thành/có checkpoint quy định ngoại lệ rõ ràng.
4. PLX công ty mẹ Q3/2026 B03 chênh 87.654.015.000 VND vẫn chưa giải quyết; không ghi sửa giả.
5. Tuân thủ 2025-Q1 trở đi; tối đa 20 kỳ; chấp nhận lệch <=0,01%; sao lưu checkpoint; GitHub main là nguồn deploy trang web Hostinger.
