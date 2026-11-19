# CHECKPOINT — GAS hợp nhất Q1–Q2/2026 (19/11/2026)

## Nguồn, điểm đã hoàn thành, trạng thái
- Duy trì GAS hợp nhất 2025 Q1–Q4 đã xác minh; Q4 merged PR #50 commit `322bf572`, 52 fields, 23 checks, site 45/45 PASS.
- Nguồn 2026 Q1 PV GAS gốc: https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14496&documentid=3276&moduleid=648&portalid=0 ; PDF 17.616.647 bytes, SHA-256 `853ad22dfe045d2477d9e027fa3d161a9eb2bed37c2a37bec8942fa815008deb`.
- Nguồn 2026 Q2 PV GAS gốc: https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14585&documentid=3358&moduleid=648&portalid=0 ; PDF 8.755.462 bytes, SHA-256 `118f3b092ddce271d87051734c4c789d18b82a65dc7ace39ce83beedeea46e56`.
- Công cụ trích ảnh nguồn tại `scripts/inspect_gas_2026_q1_q2_pdf.py`, workflow `inspect-gas-2026-q1-q2.yml`, PR #51 đã merge; GitHub Actions run `44490692134` hai matrix PASS. Artifacts Q1 `14512856021`; Q2 `14513325099`. Đã xem trực quan ảnh B01/B02/B03 Q1 PDF trang 4–7, Q2 trang 3–6. Không ghi số chỉ từ OCR chưa xem ảnh.
- Dữ liệu bổ sung `data/financials-GAS.json` **2026-Q1/Q2 hợp nhất**, 49 + 50 trường công khai đã kiểm tra từng nguồn, cộng các cấu phần B03 hỗ trợ tái tính. **36 đẳng thức số học nội bộ** (18 mỗi kỳ) residual **0 VND**.
- Q1 B01: tài sản `92.923.423.491.919`, nợ `22.333.645.606.660`, VCSH `70.589.777.885.259` VND. Q1 B02 phát sinh doanh thu thuần `38.019.609.031.268`, LNTT `3.754.683.655.851`, LNST `2.994.115.272.577`, EPS 1.220 đồng/cp. Q1 B03 CFO `-468.939.629.618`, CFI `599.484.606.752`, CFF `314.542.385.295`; net `445.087.362.429` VND.
- Q2 B01: tài sản `102.869.897.500.506`, nợ `32.615.256.063.103`, VCSH `70.254.641.437.403`. Q2 B02 cột riêng Quý II/Năm nay: doanh thu thuần `43.249.135.951.689`, LNTT `7.443.056.154.493`, LNST `6.021.399.337.485`, EPS 2.385 đồng/cp. Q2 B03 phát sinh quý = H1 YTD trừ Q1 YTD cùng phạm vi: CFO `7.507.543.987.597`, CFI `-3.428.450.591.393`, CFF `-356.759.006.640`, net `3.722.334.389.564` VND. Q2 tiền đầu kỳ `7.321.907.295.672`, FX `11.396.460.116`, cuối `11.055.638.145.352` khớp exact.
- Q1 B03 cổ tức trả dòng 36 là gạch ngang, **không** tự coi bằng 0, nên chưa suy ra cổ tức riêng Q2 từ tổng H1.

## Các mâu thuẫn nguồn bắt buộc giữ cảnh báo, không tự sửa
1. B01 cột 01/01/2026 ghi tổng tài sản `93.568.198.109.790` VND trong cả báo cáo Q1 và Q2, khác tổng tài sản 31/12/2025 của BCTC gốc cuối năm đã PASS `93.531.511.866.676` VND: **+36.686.243.114 VND**, ~0,0392% > ngưỡng 0,01%. Nợ mở đầu cũng có chênh lệch tương ứng; có thể do trình bày/điều chỉnh so sánh, chưa khẳng định nguyên nhân.
2. Báo cáo Q2/2026 cột lũy kế H1 cho giá vốn `68.967.158.848.778` VND, trong khi tổng giá vốn Q1 + Q2 từ hai cột quý là `68.977.318.999.056` VND. Chênh **10.160.150.278 VND**. Gross, PBT, net và parent attributable H1 cùng lệch +10.160.150.278 so với tổng hai quý gốc. Nguồn H1 có khả năng trình bày lại số cũ: chưa xác nhận chính thức; **giữ B02 từng quý như bản gốc**, không ép sum khớp H1. Doanh thu H1 khớp chính xác tổng hai quý.
3. B03 6 tháng dòng LNTT đầu nguồn ghi `11.218.934.222.989` VND, khác B02 H1 LNTT `11.207.899.960.622` VND **11.034.262.367 VND**, >0,01%. B03 CFO và bridge nội bộ vẫn khớp số học; chưa có thuyết minh giải thích.
4. B03 2026 đầu năm tiền `6.876.452.747.838` VND, khác B03/B01 31/12/2025 `6.876.468.282.085` VND **-15.534.247 VND**; kế thừa dấu vết chênh lệch số đầu kỳ được ghi ở báo cáo 2025; không sửa tay dữ liệu nguồn.
5. Đây là **nguồn mới có mâu thuẫn** nên xem xét lại riêng các cột so sánh/hồi tố khi tìm được thuyết minh. Không tuyên bố cross-period PASS; chỉ 36 internal statement checks PASS.

## Triển khai và điểm tiếp
- Tệp dữ liệu `data/financials-GAS.json` Q1–Q2/2026; script `scripts/verify_gas_2026_q1_q2_visual.py`; `.github/workflows/validate.yml` có gate tự kiểm, kiểm toán chính xác 36 phép và chặn đảo chiều dấu.
- Merge PR dữ liệu chỉ khi Validate financial snapshots PASS; sau merge xác minh website production **45/45 HTTP/SHA-256 PASS**. Ghi checkpoint commit.
- GAS Q3/2026 hợp nhất và công ty mẹ đã kiểm chứng từ trước **không làm lại**. Ticker tiếp theo theo thứ tự VDS Q3/2026, GEG các kỳ cũ, IDC Q3/2026. PLX Q3/2026 mẹ B03 vẫn chặn 87.654.015.000 VND, không bịa hoặc tự cân đối.
- Lưu tối đa 20 kỳ từ Q1/2025, đơn vị triệu VND ngoài EPS, bảo toàn báo cáo riêng/hợp nhất, giữ giao diện website.
