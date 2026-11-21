# Quy trình đối chiếu BCTC theo chuẩn mực kế toán, chế độ chuyên ngành và pháp luật Việt Nam
*Áp dụng từ 21/11/2026; kiểm tra dữ liệu và hồ sơ nguồn, không thay thế ý kiến kiểm toán hay tư vấn pháp lý*

## 1. Phân tầng quy định theo năm và ngành
- Luật Kế toán số 88/2015/QH13 (cùng sửa đổi) và **VAS 01**: trung thực, khách quan, đầy đủ, nhất quán và thận trọng; số liệu kỳ sau phải kế tiếp kỳ trước hoặc phải có thuyết minh về thay đổi chính sách/trình bày lại.
- **VAS 21**: tính nhất quán, phạm vi riêng/hợp nhất, cách trình bày kỳ so sánh. **VAS 24**: phân loại CFO, CFI, CFF và đối chiếu biến động tiền, không nhầm LNTT với CFO.
- **Công ty chứng khoán (CTCK): Thông tư 210/2014/TT-BTC và Thông tư 334/2016/TT-BTC** hướng dẫn mẫu chuyên ngành; doanh thu FVTPL/cho vay/môi giới, tài sản tài chính, dự phòng và tiền khách hàng ngoài B01 được ghi theo báo cáo nguồn chuyên ngành. Không ép sang mẫu doanh nghiệp công nghiệp hoặc ghi tiền khách hàng vào tài sản của CTCK.
- Từ **năm tài chính bắt đầu 01/01/2026**, **Thông tư 99/2025/TT-BTC** thay Thông tư 200/2014 cho chế độ kế toán doanh nghiệp nói chung; **KHÔNG kết luận thay thế máy móc** các phụ lục kế toán chuyên ngành CTCK. Với hồ sơ CTCK 2026 phải kiểm tra tiêu đề/mẫu/thuyết minh kế toán của bản ký thực tế và văn bản áp dụng, đánh dấu `NEEDS_FORM_AND_EFFECTIVE_SCOPE_REVIEW` nếu chưa rõ. Với ngân hàng hoặc ngành đặc thù khác phải tra chế độ riêng.
- **Luật Doanh nghiệp 59/2020/QH14, sửa đổi Luật 76/2025/QH15, VBHN 67/VBHN-VPQH**: lập, thông qua/cung cấp hồ sơ báo cáo theo trách nhiệm của doanh nghiệp, không tự sửa báo cáo gốc; lưu phiên bản đính chính, trách nhiệm báo cáo.
- **Thông tư 96/2020/TT-BTC, được sửa đổi bởi 68/2024 và 18/2025** về công bố thông tin chứng khoán: cần ghi URL công bố, ngày nguồn, ngày ký, kỳ và loại báo cáo, bản kiểm toán/soát xét và bản sửa đổi. Tình trạng đúng hạn/đúng trách nhiệm *không được kết luận bằng máy* khi chưa có bằng chứng sự kiện.

Nguồn chính thức:
- Luật Kế toán: https://congbao.chinhphu.vn/van-ban/luat-so-88-2015-qh13-18393.htm
- VAS 01 (tài liệu Bộ Tài chính): https://nif.mof.gov.vn/webcenter/contentattachfile/idcplg?dDocName=MOFUCM313484&dID=318048&filename=CD4+-+Ke+toan+final.pdf
- TT210/2014: https://congbao.chinhphu.vn/van-ban/thong-tu-so-210-2014-tt-btc-12804/8207.htm
- TT334/2016: https://congbao.chinhphu.vn/van-ban/thong-tu-so-334-2016-tt-btc-22357.htm
- TT99/2025: https://congbao.chinhphu.vn/van-ban/thong-tu-so-99-2025-tt-btc-46529/59652.htm
- Luật Doanh nghiệp hợp nhất 2025: https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-67-vbhn-vpqh-45865.htm
- TT18/2025 sửa TT96: https://congbao.chinhphu.vn/van-ban/thong-tu-so-18-2025-tt-btc-44783.htm

## 2. Quy tắc kiểm thử và mức độ chứng cứ

| Nhóm | Kiểm tra kỹ thuật | Nếu sai hoặc chưa có bằng chứng |
|---|---|---|
| Nhận diện nguồn | Mã, kỳ, năm, riêng/hợp nhất, đơn vị, chữ ký/nguồn, SHA-256, bản gốc-vs-đính chính | BLOCK, không nhập số sai phạm vi |
| B01 | Tổng tài sản = nợ + vốn; từng nhóm/nợ ngắn/dài; tài sản tài chính; chính xác theo báo cáo nguồn | FAIL nếu mất cân đối |
| B02 | Doanh thu − chi phí theo mẫu chuyên ngành; lợi nhuận khác; LNTT − thuế = LNST | FAIL nếu khác dấu/dòng hoặc đơn vị |
| B03 | CFO + CFI + CFF = dòng tiền thuần; đầu + biến động = cuối; tiền B03 cuối = B01 | FAIL nếu không khớp |
| Tính quý | Q2 = 6M − Q1; Q3 = 9M − H1; Q4 = 12M − 9M **cùng phạm vi và vintage** | BLOCK nếu trộn phiên bản hoặc YTD |
| CTCK | Tiền nhà đầu tư ngoài B01 tách khỏi tiền và nợ công ty; EPS theo đúng cột quý/YTD | BLOCK nếu gộp sai hoặc suy EPS |
| Thuyết minh/đính chính | Lưu phiên bản nguồn ban đầu, ngày đính chính, giá trị cũ/mới, khoản phân loại lại | REVIEW hoặc FAIL nếu số cũ bị ghi đè không dấu vết |
| So sánh cùng ngành | Cùng mẫu kế toán, đúng quý/năm, phạm vi và đơn vị; không so ngân hàng như doanh nghiệp sản xuất | CẢNH BÁO/không xếp hạng |
| Công bố theo luật | Kiểm tra URL, ngày ký/ngày công bố, loại kiểm toán và người chịu trách nhiệm | MANUAL_LEGAL_REVIEW; không tự kết luận đã tuân thủ luật |

## 3. Điều kiện đặc biệt đối với ngưỡng sai lệch 0,1%
- Chỉ dùng cho **chênh lệch cộng số của tổng phụ trên báo cáo gốc**, khi có đối chiếu ít nhất hai nguồn bổ sung, cùng kỳ, phạm vi, độ phân giải; xác nhận đúng mã, đơn vị, dấu.
- Không được dùng cho sai báo cáo riêng/hợp nhất, nhầm đơn vị triệu/tỷ/VND, sai dấu hoặc tiền trong B03, EPS, phiên bản, tổng tài sản=nợ+vốn, hay công thức dòng tiền.
- **PASS_WITH_TOLERANCE không đồng nghĩa báo cáo nguồn cộng đúng.** Luôn lưu số tổng công bố, tổng chi tiết, chênh tuyệt đối/tỷ lệ, đường dẫn gốc, nguồn bổ sung và cờ ngoại lệ.
- Khi có bản đính chính, phải mở lại ngoại lệ tương ứng, không tự sửa các kỳ PASS chưa có mâu thuẫn nguồn.

## 4. Áp dụng hiện tại và kết quả kiểm tra
- Mã **VIX**, phạm vi **BCTC RIÊNG năm 2025**: Q1–Q4 đã kiểm tra chính xác từ PDF ký gốc và được giữ nguyên. Mẫu CTCK theo 210/334; tiền khách hàng ngoài B01 được tách; CFO/CFI/CFF và B02 riêng quý/YTD khớp nguồn.
- **VIX Q1–Q3/2026**: dữ liệu `manual_review_required_pending_extraction`; chưa có bằng chứng ký gốc B01/B02/B03 đầy đủ trong bộ kiểm thử hiện tại, nên chưa đủ điều kiện hoàn thành. Ngoài dữ liệu còn phải rà tương tác TT99 2025 và chế độ CTCK trong tài liệu gốc.
- **PLX Q1/2026**: giữ tình trạng `PASS_WITH_TOLERANCE` cho đúng hai tổng phụ đã được kiểm tra đa nguồn. Không đổi thành exact component PASS hoặc xem đây là giấy chứng nhận tuân thủ pháp luật.
- Kiểm thử tự động: `scripts/verify_accounting_legal_framework.py` (đi kèm năm phép kiểm thử âm), manifest nguồn luật/hiệu lực: `reports/accounting-legal-validation-framework.json`, GitHub Actions validate bắt buộc.
- Những yếu tố như phát hành/đăng ký vốn, nghĩa vụ công bố, thông qua BCTC ở ĐHĐCĐ, quyết định kiểm toán, điều chỉnh thuế, thuyết minh giá trị hợp lý **cần bằng chứng tài liệu**. Tình trạng `PASS_ACCOUNTING_SOURCE_CHECKS` chỉ phản ánh các phép đối chiếu đã triển khai, **không phải xác nhận tuân thủ mọi chuẩn mực và luật**.

## 5. Quy trình tiến độ
1. Đọc checkpoint mới nhất; không tái kiểm tra số liệu đã PASS nếu không có nguồn mâu thuẫn.
2. Với kỳ chưa hoàn thành: lấy nguồn doanh nghiệp + sở giao dịch + ít nhất một nguồn đối chiếu, lưu SHA và ngày nguồn.
3. Nhận diện mẫu chế độ kế toán theo năm, ngành, thuyết minh; tách riêng/hợp nhất và bản báo cáo gốc/soát xét/kiểm toán/đính chính.
4. Nhập số VND chính xác, kiểm tra B01/B02/B03 và YTD→riêng quý; kiểm tra ngoại lệ 0,1% chỉ đúng đối tượng.
5. Chạy CI nhánh; merge sau PASS; chạy CI main, website smoke, deploy; lưu checkpoint khi hoàn tất từng kỳ.
6. Nếu thiếu chứng cứ pháp lý hoặc hồ sơ ký gốc, ghi `REVIEW_REQUIRED` và chuyển sang tìm nguồn, không tạo số ảo/không nâng trạng thái.

*Tài liệu này là SOP quản trị chất lượng dữ liệu dựa trên các quy định trích dẫn; không phải đánh giá pháp lý chính thức hoặc kết luận rằng doanh nghiệp đã thực hiện đầy đủ mọi nghĩa vụ.*

## 6. Bổ sung bằng chứng trực tiếp VIX 2026-Q1 (chỉ kiểm thử một phần)
- Bản PDF gốc trên trang VIX: https://vixs.vn/wp-content/uploads/2026/04/20260417-VIX-BAO-CAO-TAI-CHINH-QUY-I-2026.pdf; ngày ký 17/04/2026, mẫu B01/B02/B03b/B09 **CTCK theo TT334/2016**; thuyết minh 2.1 dẫn TT210/2014, TT334/2016 và VAS27. Đây là nguồn xác nhận **mẫu áp dụng thực tế của VIX Q1/2026**, không phải khẳng định TT99/2025 vô hiệu cho mọi vấn đề kế toán CTCK.
- Đã xác minh **chỉ tiêu tổng từ PDF gốc**: B01 tổng tài sản 29.598.210.995.041, tổng nợ 8.005.077.648.346, vốn CSH 21.593.133.346.695 VND; B02 LNTT 156.353.886.858, thuế tổng 17.983.617.803 (thuế hiện hành 44.096.616.869; thuế hoãn lại -26.112.999.066), LNST 138.370.269.055; B03 CFO +3.243.431.300.446, CFI -529.478.618, CFF -4.321.000.000.000; biến động -1.078.098.178.172 VND.
- B03 tiền đầu 2.049.092.199.336 VND khớp **số cuối Q4/2025 ký gốc đã nghiệm thu**, B03 cuối = B01 cuối = Thuyết minh 5 = 970.994.021.164 VND, tất cả kiểm tra 0 VND.
- Lưu bằng chứng trong `reports/source-audits/VIX-2026Q1-issuer-TT334-legal-form-and-headline-vnd.json`. Vì chưa có SHA-256 của **toàn tệp PDF gốc Q1/2026** và chưa kiểm hết từng dòng B01/B02/B03, trạng thái kỳ vẫn **FULL_DETAIL_PENDING**, không nhận PASS toàn phần và không chứng nhận tuân thủ pháp luật. Các nguồn so sánh năm 2025 đã nghiệm thu vẫn được giữ nguyên.
