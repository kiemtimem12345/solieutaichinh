# CHECKPOINT — áp dụng chuẩn mực kế toán trực tiếp cho VIX 2026-Q1, nguồn doanh nghiệp, 21/11/2026

## Điểm đã xác minh
- Quy trình kiểm soát pháp luật/chế độ kế toán đã merge ở PR #105, commit `deae9190737f9dea495abe1103cd294d54c4cc3f`; không làm lại 2025 Q1–Q4 VIX PASS.
- Tra cứu trực tiếp tệp báo cáo trên website công ty `https://vixs.vn/wp-content/uploads/2026/04/20260417-VIX-BAO-CAO-TAI-CHINH-QUY-I-2026.pdf` ngày ký 17/04/2026.
- Trang B01 B02 B03b và B09 ghi mẫu CTCK theo **Thông tư 334/2016/TT-BTC**. Thuyết minh 2.1 dẫn **Thông tư 210/2014/TT-BTC**, Thông tư 334 và VAS 27. Xác nhận phạm vi **báo cáo RIÊNG** theo danh mục `https://vixs.vn/bao-cao`; chưa có chứng cứ để tuyên bố báo cáo tuân thủ mọi luật định.
- Bản PDF chưa có full-file SHA256 trong phiên này (tải trực tiếp ở runtime thất bại, dù tài liệu được truy xuất qua cổng web), vì vậy phải tiếp tục tải/chụp ảnh, không dùng trạng thái PASS đầy đủ.

## Số gốc đã đối chiếu được, đơn vị chính xác VND
| Nguồn và mã | Số Q1/2026 |
|---|---:|
| B01 tổng tài sản (270) | 29,598,210,995,041 |
| B01 nợ phải trả | 8,005,077,648,346 |
| B01 vốn chủ sở hữu | 21,593,133,346,695 |
| B02 LNTT | 156,353,886,858 |
| B02 Thuế TNDN tổng | 17,983,617,803 |
| B02 Thuế hiện hành | +44,096,616,869 |
| B02 Thuế hoãn lại | **-26,112,999,066** |
| B02 LNST | 138,370,269,055 |
| B03 CFO | +3,243,431,300,446 |
| B03 CFI | -529,478,618 |
| B03 CFF | -4,321,000,000,000 |
| B03 biến động tiền | -1,078,098,178,172 |
| B03 tiền đầu kỳ | 2,049,092,199,336 |
| B03 tiền cuối kỳ | 970,994,021,164 |
| B01 tiền cuối kỳ, thuyết minh số 5 | 970,994,021,164 |

- Các phương trình tổng B01, B02, B03 bằng VND **khớp đúng 0 VND**. B03 mở đầu 2026 trùng **VIX Q4/2025 tiền cuối kỳ đã nghiệm thu**, không lẫn phiên bản năm.
- Nguyên tắc VAS 24 giữ CFO khác hoàn toàn LNTT; trường CFO cũ của Q1/2026 `156354` triệu thực chất là gần LNTT — đã thay bằng CFO gốc `3.243.431.300.446 VND`.
- Dòng thuế hoãn lại là số âm, không được sửa dấu theo ngưỡng 0,1%.
- EPS Q1/2026 cột riêng quý không in giá trị, cột lũy kế ghi 90 VND/cp; không tự suy diễn EPS quý (lưu riêng YTD).

## File thay đổi ở nhánh
- `reports/source-audits/VIX-2026Q1-issuer-TT334-legal-form-and-headline-vnd.json`: số nguồn, mẫu, liên kết issuer, cờ chưa có SHA và danh mục thiếu cần QA.
- `data/financials-VIX.json`: sửa duy nhất Q1/2026 các trường cốt lõi đã có nguồn, giữ đơn vị triệu VND; cập nhật phạm vi RIÊNG và `verification_status=issuer_signed_2026Q1_partial_core_B01_B02_B03_verified_FULL_DETAIL_PENDING`. Các dòng B01/B02/B03 chưa xác minh vẫn là pending, không công nhận toàn kỳ.
- `scripts/verify_vix_2026q1_issuer_tt334_core.py`: kiểm tra công thức tổng B01 B02 B03, thuế âm đúng, cầu tiền Q4/2025 đến Q1/2026, note 5, đầy đủ xuất xứ một phần và fail-closed.
- `scripts/verify_accounting_legal_framework.py`: đổi cờ cho VIX Q1/2026 là form/đầu mục đã xác minh **nhưng vẫn cần rà đầy đủ**; Q2–Q3/2026 tiếp tục pending. Không đổi dữ liệu PLX hoặc các kỳ 2025 đã hoàn tất.
- `.github/workflows/validate.yml` chạy kiểm thử mới trước legal test tổng.
- `reports/accounting-legal-validation-framework.json` và SOP bổ sung chứng cứ TT334 từ chính VIX.
- Chưa claim merged/CI/deploy khi tài liệu nhánh này chưa nghiệm thu.

## Điểm tiếp tục chính xác
1. Chạy CI PR, merge khi PASS; check main CI, website production 45/45, Pages; lưu final checkpoint.
2. Truy xuất đầy đủ PDF gốc VIX Q1/2026 để lấy SHA256 và kiểm từng dòng B01/B02/B03, thuyết minh FVTPL/lãi vay/phải thu/thuế, tiền khách hàng ngoài B01; đối chiếu nguồn sở giao dịch và công ty. Chỉ FULL PASS sau QA từng dòng, không dùng ngưỡng sai 0,1% cho sai đơn vị/dấu/phạm vi.
3. Sau Q1/2026 hoàn thành, tiếp tục Q2/2026 rồi Q3/2026; không khởi động lại VIX 2025 đã xong.
