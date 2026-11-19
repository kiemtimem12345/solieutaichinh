# CHECKPOINT — GAS hợp nhất Q4/2025, nguồn PDF gốc (19/11/2026)

## Điểm xuất phát
- Commit production trước lượt: `9bc27bd`, đã hoàn tất GAS hợp nhất Q1–Q3/2025, không xử lý lại.
- File JSON thực: `data/financials-GAS.json` (không phải `data/GAS.json`).
- BCTC gốc công bố PV GAS 30/01/2026: https://www.pvgas.com.vn/sanpham-dich-vu/bao-cao-tai-chinh-hop-nhat-nam-2025
- PDF gốc: https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14435&documentid=3245&moduleid=648&portalid=0
- Nguồn PDF scan 17.491.783 bytes, SHA-256 `0bc837f3df86ca06affc9b5547feb37905beac567ab93778210bc9671db10c09`.
- PR #49 đã merge: `scripts/inspect_gas_q4_pdf.py`, workflow `inspect-gas-q4-pdf.yml`; Actions run `44488704353` PASS, artifact `14511712651` chứa ảnh trang 3–11; ảnh trang 4,5,6,7 đã kiểm tra trực quan.

## Bộ dữ liệu GAS hợp nhất Q4/2025 đã khôi phục
- B01 31/12/2025: tài sản `93.531.511.866.676` VND, nợ `25.878.122.748.740` VND, VCSH `67.653.389.117.936` VND. Tiền và tương đương tiền `6.876.468.282.085` VND.
- B02 **cột Quý IV/Năm nay**: doanh thu thuần `43.683.070.609.001`, giá vốn `39.890.266.518.331`, lợi nhuận gộp `3.792.804.090.670`, LNTT `1.742.972.889.113`, LNST `1.387.429.975.481`, LNST cổ đông mẹ `1.361.084.899.485` VND; EPS 558 VND/cổ phiếu.
- B03 **12 tháng**: CFO `13.378.374.377.362`, CFI `-6.718.543.866.192`, CFF `-5.352.162.410.986`, dòng tiền thuần `1.307.668.100.184` VND.
- B03 **riêng Q4 = 12 tháng trừ 9 tháng hợp nhất đã kiểm tra**: CFO `829.207.541.688`, CFI `-1.145.686.907.823`, CFF `-4.447.363.676.194`, dòng tiền thuần `-4.763.843.042.329` VND.
- Q4 tiền đầu kỳ lấy B03 cuối Q3 `11.641.062.000.554`; biến động tỷ giá Q4 `-750.676.140`; cuối kỳ `6.876.468.282.085` VND. Cầu tiền khớp chính xác.
- 52 trường từ trang 4–7 được kiểm tra ảnh và nguồn; **23 đẳng thức số học ở VND có residual 0**. Đơn vị JSON là triệu VND trừ EPS, ROA/ROE vẫn null nếu chưa đủ mẫu số.
- B03 9M/2025 tiền đầu kỳ thấp hơn H1/2025 `15.534.247` VND: giữ cảnh báo lịch sử Q3, không tự chỉnh hay dùng để làm sai Q4.

## Thay đổi và kiểm thử
- Data: `data/financials-GAS.json` 2025-Q4.
- Regression: `scripts/verify_gas_q4_visual.py` gồm xác nhận số nguồn, 23 identity số học, đối chiếu Q1–Q4 = năm và Q4 B03 = 12M trừ 9M.
- `.github/workflows/validate.yml` chạy kiểm thử mới.
- Chỉ công bố là production PASS sau khi PR merge và CI PASS; không suy đoán/cộng gộp phạm vi công ty mẹ.

## Điểm tiếp tục
1. Mở PR dữ liệu GAS Q4, đợi/check CI, chỉ merge khi PASS, kiểm tra website 45/45 URL sau merge.
2. GAS hợp nhất Q1/2026 → Q2/2026 (đang trống), ưu tiên PDF gốc và từng kỳ; **GAS Q3/2026 công ty mẹ/hợp nhất đã PASS, không làm lại**.
3. Sau GAS: VDS Q3/2026 → GEG các quý cũ còn thiếu → IDC Q3/2026.
4. Song song PLX Q3/2026 B03 công ty mẹ chặn sai lệch 87.654.015.000 VND, không tự sửa.
5. Giữ branch main làm nguồn triển khai website. Không đổi giao diện, không upload dữ liệu riêng vào Hostinger checkout.
