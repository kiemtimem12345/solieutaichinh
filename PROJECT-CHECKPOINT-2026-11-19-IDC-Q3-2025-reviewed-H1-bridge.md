# CHECKPOINT — IDC Q3/2025 hợp nhất — B03 riêng quý, 19/11/2026 (sau 22:30 ICT)

## Điểm xuất phát
- Tiếp tục từ `PROJECT-CHECKPOINT-2026-11-19-IDC-Q3-data-directory-audit.md` sau commit main `cbbd664dd9cc8dc4e96bfd5ff9faee75e8fb0442`.
- Không sửa IDC Q3/2026 đã PASS, không thay đổi bất kỳ kỳ nào trước 2025-Q1, không gộp công ty mẹ và hợp nhất.

## Chứng cứ mới — H1/2025 đã soát xét, cùng phạm vi
- Báo cáo BCTC **hợp nhất** giữa niên độ 6 tháng, 30/06/2025; EY soát xét, ký 28/08/2025; công bố HNX 04/09/2025.
- Tệp công bố HNX: `IDC_2025.9.4_32903a4_VI_BaoCaoTaiChinh_KiemToan_HN_T6.2025.pdf`.
- Truy xuất bản sao báo cáo ký: https://cafef1.mediacdn.vn/download/040925/idc-bao-cao-tai-chinh-ban-nien-nam-2025-0-579208.pdf
- Trang PDF zero-based 14–15, B03a-DN/HN, đã xem trực quan. Trên trang 14: CFO 1.402.209.397.523, CFI -2.438.216.817.714, CFF -288.817.920.091 VND; trang 15: biến động tiền -1.324.825.340.282, đầu kỳ 2.188.037.806.317, FX +41.467.072, cuối kỳ 863.253.933.107 VND.
- H1 tổng ba luồng -1.324.825.340.282, khớp biến động tiền; cầu tiền đầu + biến động + FX - cuối = **0 VND**.
- H1: capex -909.344.214.214, cổ tức/lợi nhuận trả -588.587.063.470 VND (trang 14).
- Chỉ đánh dấu **B03 H1 trực quan đạt**, KHÔNG đánh dấu B01/B02 Q2/2025 đạt. Bản quý II gốc ngày 30/07/2025 vẫn hơn giới hạn tải 15MB tại CafeF; giữ Q2/2025 trạng thái partial cho đến khi rà toàn báo cáo.

## IDC Q3/2025 — B03 riêng quý hợp nhất
- PDF Q3 2025 HNX ký 29/10/2025, hash SHA256 `80c1b3dcb2e5469d4fb84c3a0cbd46c51f664ce7e07a2a0946e10b691ca92ce3`, bản đã xác minh 9M tại checkpoint trước (30 source identities residual 0).
- Phép tính: **9M Q3 nguồn gốc trừ 6M H1 soát xét cùng phạm vi**, ở độ chính xác VND, không trừ bản OCR làm tròn.
- CFO Q3 **+1.541.531.404.357 VND**.
- CFI Q3 **-2.242.302.344.954 VND**.
- CFF Q3 **+629.179.666.426 VND**.
- Dòng tiền thuần Q3 **-71.591.274.171 VND**.
- FX riêng quý **+23.900.983 VND**.
- Tiền đầu Q3 **863.253.933.107 VND**; cuối Q3 **791.686.559.919 VND**.
- Chi mua TSCĐ/BĐSĐT riêng quý **-893.695.067.506 VND**; cổ tức/lợi nhuận đã trả **-57.513.573.250 VND**.
- **5 phép kiểm tra VND residual 0**: H1 ba luồng, H1 cầu tiền, Q3 ba luồng, Q3 cầu tiền, B01= B03 tiền cuối.
- Giữ `cashflow_period_basis=year_to_date` cho trường lũy kế, các trường `operating_cash_flow` v.v. là quý riêng. Đơn vị trong JSON `triệu VND`, EPS VND/cổ phần.
- Chỉ cập nhật `data/financials-IDC.json` (Q2 thêm bằng chứng B03 riêng, Q3 thêm dòng tiền quý) và `scripts/verify_idc_q3_2025_original.py`; số 9M đã xác minh không sửa, IDC Q3/2026 không thay đổi.

## Điểm tiếp tục
1. CI chạy `scripts/verify_idc_q3_2025_original.py`, script Q3/2026 và smoke 45/45 sau khi tạo PR. Chỉ merge khi PASS.
2. IDC Q2/2025 original dated 30/07/2025: PDF VI HNX file `IDC_2025.7.30_caaaf64_VI_BaoCaoTaiChinhHN_Q2_2025_s.pdf`, mirror https://cafef1.mediacdn.vn/download/300725/idc-bao-cao-tai-chinh-quy-2-2025-3-573470.pdf (15,956,738 bytes; web tool content cap). Tìm đường tải/split nhỏ rồi kiểm tra ảnh B01/B02/B03, đối chiếu bản soát xét cùng phạm vi.
3. IDC Q1/2025: nguồn PDF hợp nhất Vietstock hiện trạng OCR, cần visual QA B01/B02/B03; không làm lại trường đã kiểm số học nếu không mâu thuẫn.
4. Các phần khác của PLX/GAS/VDS/GEG giữ trạng thái và ưu tiên theo checkpoint mới nhất. PLX công ty mẹ Q3 CFF lệch 87.654.015.000 VND, không sửa/không công bố B03 khi chưa có bằng chứng.

## Quy tắc
Sai lệch <=0,01%, không bịa số; chỉ từ 2025-Q1; mỗi mã tối đa 20 kỳ; không thay bố cục web. Bản `main` mới là production, nhánh làm việc không phải deploy.
