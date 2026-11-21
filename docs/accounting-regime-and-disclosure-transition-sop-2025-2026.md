# SOP — Áp dụng chế độ kế toán và công bố BCTC theo giai đoạn (2025–2026)

**Ngày rà soát:** 21/11/2026. **Phạm vi dự án:** BCTC doanh nghiệp niêm yết Việt Nam từ Q1/2025 đến Q3/2026; tách riêng công ty mẹ/hợp nhất, ngân hàng/chứng khoán/doanh nghiệp chung. **Tài liệu kỹ thuật, không phải chứng nhận doanh nghiệp tuân thủ pháp luật.**

## 1. Bốn mốc pháp lý luôn phải lưu riêng

Mỗi tệp nguồn phải có metadata:
- `fiscal_year_start`, `report_period_end`, `report_signed_at`, `disclosed_at`.
- `report_scope`: consolidated / separate / parent; `industry_framework`: general / banking / securities / other-special.
- `accounting_regime_id` và `consolidation_regime_id`: gắn theo **năm tài chính, phạm vi áp dụng và điều khoản chuyển tiếp**, KHÔNG suy đoán chỉ từ ngày ban hành thông tư.
- `disclosure_regime_id`: hệ thống luật chứng khoán riêng với chế độ lập kế toán.
- `source_version_id`: original_interim / reviewed_H1 / audited_FY / restated / correction, kèm nguồn, hash, trang chú thích.
- `transition_basis`: mandated_retrospective / simplified_retrospective / prospective / reclassified_comparative / unknown; chỉ kết luận khi có điều khoản pháp lý và xác nhận từ BCTC gốc.
- `comparative_basis`: original_as_filed vs re-presented; `cash_classification`: free cash / restricted deposits / noncash classification.

## 2. Văn bản nền tảng: hiệu lực phải đối chiếu theo năm tài chính

- **TT200/2014/TT-BTC**: chế độ kế toán doanh nghiệp chung trước năm tài chính 2026, với ngoại lệ chuyên ngành. 
- **TT99/2025/TT-BTC**: ban hành 27/10/2025, hiệu lực 01/01/2026 và áp dụng cho **năm tài chính bắt đầu từ hoặc sau 01/01/2026**, thay thế đa số quy định TT200. Điều 30 phân biệt điều chỉnh hồi tố, hồi tố đơn giản, phi hồi tố, theo hướng dẫn chuyển tiếp cụ thể; nếu áp dụng lần đầu quy định pháp luật không bắt buộc hồi tố thì có thể phi hồi tố. Ngân hàng/TCTD có chế độ theo NHNN, không tự gán TT99.
  Official MOF: https://www.mof.gov.vn/tin-tuc-tai-chinh/tin-chinh-sach-tai-chinh/quy-dinh-moi-ve-che-do-ke-toan-doanh-nghiep
  Full reference: https://luatminhkhue.vn/van-ban/thong-tu-so-99-2025-tt-btc.aspx (Điều 30, 31).
- **TT202/2014/TT-BTC + TT43/2026/TT-BTC** cho báo cáo hợp nhất: TT43 ký 20/04/2026, **hiệu lực 20/04/2026** nhưng **áp dụng khi lập báo cáo hợp nhất cho năm tài chính bắt đầu từ hoặc sau 01/01/2026** (Điều 3). Bộ Tài chính xác nhận TT43 được áp dụng kịp cho **BCTC hợp nhất Q1/2026**. Không gán máy móc Q1/2026=chế độ hợp nhất cũ; ngược lại, không coi thiếu chữ “TT43” trong thuyết minh là chứng cứ vi phạm hoặc đủ chứng cứ số Q1 đã trình bày lại. Điều 3(2) cho phép phi hồi tố trong một số trường hợp áp dụng quy định lần đầu nếu không bắt buộc hồi tố.
  Official MOF: https://www.mof.gov.vn/tin-tuc-tai-chinh/tin-chinh-sach-tai-chinh/quy-dinh-moi-ve-phuong-phap-lap-va-trinh-bay-bao-cao-tai-chinh-hop-nhat
  Full TT43: https://thuvienphapluat.vn/van-ban/Tai-chinh-nha-nuoc/Thong-tu-43-2026-TT-BTC-sua-doi-Thong-tu-202-2014-TT-BTC-trinh-bay-Bao-cao-tai-chinh-hop-nhat-703170.aspx
- **TT96/2020/TT-BTC** công bố thông tin niêm yết/đại chúng quy mô lớn và sửa đổi bởi TT68/2024, TT18/2025, TT08/2026. Đây là lớp nghĩa vụ công bố, **không tự động đòi hỏi doanh nghiệp nộp lại mọi báo cáo quý trước khi có thông tư kế toán mới**. Điều 14 quy định, tùy đối tượng: quý 20 ngày từ quý kết thúc, công ty mẹ/đơn vị kế toán cấp trên 30 ngày; bán niên đã soát xét 5 ngày kể từ ngày ký (giới hạn 45/60 ngày theo đối tượng); kèm toàn văn và giải trình khi cần. Điều 14 phải kiểm tra bản đã sửa đổi đang có hiệu lực tại thời điểm công bố. Có dự thảo tháng 10/2026 để thay TT96 nhưng dự thảo **không có hiệu lực pháp luật**.
  Text Điều 14: https://vanban.vcci.com.vn/thong-tu-962020tt-btc-huong-dan-cong-bo-thong-tin-tren-thi-truong-chung-khoan
  2026 amendment SSC: https://ssc.gov.vn/webcenter/portal/ubck/pages_r/l/chitit?dDocName=APPSSCGOVVN1620163824
  Draft status SSC: https://ssc.gov.vn/webcenter/portal/ubck/pages_r/l/chitit?dDocName=APPSSCGOVVN1620172383&dID=182819

## 3. Quy trình xử lý khi có thông tư mới

1. **Xác định phạm vi:** doanh nghiệp, ngành/chế độ đặc thù, phạm vi mẹ/hợp nhất, năm tài chính bắt đầu ngày nào.
2. **Phân lớp pháp lý:** lập BCTC (TT99/TT202+TT43 hoặc NHNN/UBCK chuyên ngành) khác với công bố thông tin (TT96 và sửa đổi).
3. **Đọc điều khoản hiệu lực/chuyển tiếp:** hiệu lực ngày ký != năm tài chính áp dụng; phân loại hồi tố, hồi tố đơn giản, phi hồi tố theo điều khoản + thuyết minh phát hành.
4. **Lưu bản gốc độc lập:** `original_Q1_as_filed` không bị ghi đè bởi `H1_reviewed_represented`; ngày ký/công bố và SHA riêng.
5. **Lập bảng cầu nối thay đổi:** chi tiết từng chỉ tiêu, bản gốc, bản trình bày lại, lý do, số dư mở/đóng, dòng tiền vs phân loại phi tiền tệ, nguồn + trang.
6. **Công nhận nguồn gốc:** nếu B01/B02/B03 **bản gốc** cân chính xác thì từng báo cáo vẫn source PASS dù phiên bản so sánh khác. Không gọi khác phiên bản là lỗi doanh nghiệp.
7. **Tính B03 quý độc lập** khi H1(6M) và Q1(3M) cùng phạm vi và cùng cơ sở hiện hành; nếu khác bản trình bày, phải có chứng cứ đối chiếu cùng-basis cả CFO/CFI/CFF **và** cầu tiền mặt quý trước khi đưa vào production. Không chuyển chênh lệch phân loại phi tiền tệ thành CFO/CFI/CFF.
8. **Chặn những kỳ không đủ bằng chứng:** để B03 quý độc lập null, vẫn hiển thị B03 lũy kế có ghi nguồn, công khai trạng thái “khác phiên bản trình bày/chưa có cầu nối”. Sai số <=0.1% chỉ áp dụng với tổng phụ đủ đối chứng đa nguồn, **không áp dụng** cho sai phạm vi/chế độ/dấu/đơn vị hay cash bridge.
9. **Kiểm thử và checkpoint:** chạy validator của mã + global, thực hiện CI, sau merge xác nhận website 45/45, giữ lịch sử nguồn. Không tự xóa/chỉnh báo cáo đã hợp lệ.

## 4. Áp dụng đặc biệt GEG và IDC 2026-Q2

**GEG** (hợp nhất): Q1/H1 nguồn signed PASS. Báo cáo Q2 B09 thuyết minh 11 có 11,422,218,903 VND tiền gửi bảo lãnh tại 01/01/2026, được chuyển từ B01 code112 sang code165 so với bản quý I. **Đây là phân loại lại số dư đầu năm**; chưa có số bảo lãnh 31/03/2026 đã ký hoặc B03 Q1 cùng basis. Không được xem chênh lệch cầu tiền quý II -11,422,218,903 VND là luồng tiền chi ra, hoặc tự cộng trừ vào CFO/CFI/CFF. Giữ quarterly Q2 B03 NULL.

**IDC** (hợp nhất): Q1 thuyết minh TT99, H1 thuyết minh TT99+TT43 và Note41 so sánh 2025, có chênh lệch tiền mở kỳ 890,796,892 VND. Do TT43 có hiệu lực áp dụng cho năm 2026 **bao gồm Q1**, việc Q1 không *nhắc* TT43 không đủ để gán Q1 sai luật hay tự buộc doanh nghiệp tái công bố; cần phân tích thay đổi **các dòng thực tế 2026** và bản restated/bridge nếu tồn tại. H1 Note41 tái phân loại B03 kỳ so sánh 2025 không thể thay thế dòng 2026. Giữ quarterly Q2 B03 NULL tới khi có signed same-basis reconciliation.

Nguồn kiểm toán nội bộ:
- `reports/source-audits/GEG-2026Q2-note11-pledged-cash-opening-reclassification-vnd.json`
- `reports/source-audits/IDC-2026Q1-vs-H1-TT43-source-policy-and-Note41-B03-comparatives.json`
- `scripts/verify_geg_q2_2026_pledged_deposit_note11.py`
- `scripts/verify_idc_q2_2026_tt43_signed_current_period_vintage.py`

### Decision rule
**Thiếu điều chỉnh Q1 không mặc nhiên vi phạm nghĩa vụ công bố; thay đổi chế độ kế toán được xử lý theo điều khoản chuyển tiếp và báo cáo gốc, không hồi tố máy móc.** Cho phép giữ bản gốc và ghi riêng “chưa xác định cùng phiên bản để quarterize”; không ép phát sinh số quý II khi B03 tiền không cân.
