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

## 5. Triển khai bằng chương trình (bổ sung ngày 21/11/2026)

Quy trình này có **cổng kiểm tra tự động**, không chỉ mô tả bằng văn bản:

- `config/reporting-regime-rules-2025-2026.json`: dữ liệu quy phạm và ngày hiệu lực, gồm **ngưỡng năm tài chính** (01/01/2026), **ngày ký/hiệu lực** TT43 (20/04/2026), thông tư công bố độc lập, và nhánh ngành đặc thù cần xác minh riêng.
- `scripts/verify_reporting_regime_transitions.py`: đánh giá năm tài chính và phạm vi báo cáo, kiểm tra GEG/IDC Q2 dòng tiền quý độc lập với nguồn ký gốc + cầu nối tiền VND chính xác; chặn mọi khoản CFO/CFI/CFF hoặc số 0 giả khi thiếu cầu nối.
- `.github/workflows/validate.yml` chạy verifier này **bắt buộc** cùng toàn bộ kiểm thử kế toán cũ. Cơ chế này không thay thế BCTC gốc và không thay số liệu B01/B02/B03 lũy kế.

**Phương pháp có thể tái sử dụng ở kỳ mới:** khi ghi nhận báo cáo, lưu các trường `fiscal_year_start`, `period_end`, `scope`, `industry`, `signed_at`, `disclosed_at`, `source_sha256`, `source_version_id`, `accounting_regime`, `consolidation_regime`, `disclosure_regime`, `transition_basis`. Dùng `accounting_basis(policy, fiscal_year_start, consolidated, industry)` trong verifier để xác định khung pháp lý **có thể áp dụng**, rồi tra thuyết minh ký gốc trước khi xác nhận chế độ **thực tế được doanh nghiệp áp dụng**. Với bank/chứng khoán trả về cần kiểm tra chế độ chuyên ngành, không gán TT99/TT43 máy móc.

**Điều kiện nâng Q2/2026 từ BLOCKED lên PASS:** phải đồng thời có chứng cứ ký gốc về cách trình bày lại Q1 hiện hành, cùng phạm vi, số dư cuối Q1 đã điều chỉnh, kiểm tra từng dòng CFO/CFI/CFF, và cầu tiền Q2 khớp **0 VND**. Ngoại lệ được ghi trong ledger vẫn được theo dõi độc lập; phép dung sai 0,1% không vượt qua cổng này. Khi xuất hiện báo cáo điều chỉnh, bổ sung file gốc/sha/trang, thay đổi chứng cứ và kiểm thử có chủ đích, không tự sửa giá trị thành số 0.

**Kết luận hiện tại:** quy tắc chuyển tiếp theo thông tư hợp lệ để bổ sung vào SOP. Nó giải thích *vì sao* cần lưu nhiều phiên bản, **không tự làm mất** hai ngoại lệ GEG/IDC Q2 do thiếu bằng chứng signed same-basis; B01/B02 và B03 lũy kế được giữ PASS.

## 6. Ngoại lệ GEG: cùng số dư điều chỉnh, khác mã B01 giữa các phiên bản

Tài liệu ký gốc GEG Q1/2026, bản quý II công bố ban đầu và bản bán niên EY soát xét cho thấy **11.422.218.903 VND** được loại khỏi tổng tiền và tương đương tiền đầu năm và chuyển vào mã 165. **Nhưng dòng tiền bị điều chỉnh không đồng nhất**:

- Q1 bản gốc: B01 mã 111 tiền `46.702.358.323`, mã 112 tương đương tiền `39.662.304.925`, tổng `86.364.663.248`.
- Q2 bản gốc (số đầu năm): mã 111 `46.702.358.323`, mã 112 `28.240.086.022`, tổng `74.942.444.345`.
- H1 soát xét EY (số đầu năm, **cùng tổng**): mã 111 `35.280.139.420`, mã 112 `39.662.304.925`, tổng `74.942.444.345`.

Do đó **không được coi hai phiên bản Q2/H1 là cùng bản chất mã 111/112** chỉ vì tổng tiền và mã 165 khớp. Đối chiếu tới cấp chỉ tiêu và phiên bản phải làm trước khi thay số B01 trên website.

**Có thể xác minh và lưu song song cách tính quý III** trên cùng cơ sở H1 soát xét và B03 9 tháng Q3 ký gốc (đơn vị VND, kết quả đã qua regression CI):
- CFO `448.662.906.453`, CFI `-639.871.926.621`, CFF `186.959.810.890`, net `-4.249.209.278`, FX `-15.900.229`.
- Cầu tiền tháng 7–9: `100.322.233.328 - 4.249.209.278 - 15.900.229 = 96.057.123.821`, **sai số 0 VND**.
- Bản quý III đang lưu trên website có thể thuộc nhánh quý II ban đầu; **không đổi sản xuất một phần** nếu chưa cập nhật đồng bộ B01/B03 quý II, xác nhận dữ liệu trang hiển thị và chạy các kiểm thử liên kỳ. Hai cách tính không được lẫn trong một phép kiểm tra mà thiếu nhãn version.

**Q2 standalone vẫn NULL**: chưa có số tiền bị hạn chế đã ký tại 31/03/2026 hoặc B03 Q1 cùng phiên bản lập lại để nối tiền quý II. Không tự lấy chênh lệch đầu năm làm dòng tiền giao dịch. Có thể kết thúc lượt tìm kiếm định kỳ bằng trạng thái `terminal_manual_review_pending_issuer_signed_same_basis_q1`, nhưng **không đánh dấu B03 quý II đã hoàn thành/PASS**.

Nguồn audit thực thi: `reports/source-audits/GEG-2026Q3-H1-reviewed-reconciliation.md`, `scripts/verify_geg_2026q3_reviewed_h1_bridge.py`, H1 EY ký gốc người dùng tải lên 74 trang, B03 p16–17 và thuyết minh 37 p73; Q3 bản gốc doanh nghiệp đã được xác minh tại repo.

## 7. Đóng hồ sơ theo nguồn do doanh nghiệp công bố (người dùng chấp thuận ngày 21/11/2026)

Trường hợp có **hai phiên bản ký hợp lệ nhưng không đồng nhất phân loại** (ví dụ B03 GEG Q2/2026 và bản EY soát xét H1/2026), được phép **kết thúc giai đoạn xử lý của mã** khi người dùng chấp nhận dùng số liệu nguồn phát hành chính thức làm chuẩn tạm thời. Điều này có nghĩa:

1. B01/B02/B03 **gốc đã ký** và **bản soát xét bán niên** đều được lưu theo đúng `source_version_id`; bản soát xét là mốc tham chiếu ưu tiên cho **lũy kế sáu tháng**. Không ghi đè, không trộn mã B01 111 và 112 giữa các phiên bản.
2. Trạng thái nghiệp vụ `completed_issuer_accepted_exception_pending_fy2026_audited_recheck` nghĩa là **đóng hồ sơ truy nguồn**, không đồng nghĩa tất cả số liệu quý độc lập đã kiểm toán hay được doanh nghiệp công bố trực tiếp.
3. Nếu bản gốc không có B03 riêng quý II và trừ số liệu từ các phiên bản khác nhau gây sai cầu tiền, để **`null`** các trường CFO/CFI/CFF quý độc lập. Không đặt 0, không giả định số dư tiền bị hạn chế 31/03 bằng số 01/01. Được phép lưu phép trừ lũy kế dưới nhãn *chưa công nhận quý độc lập*, không đưa như số thực tế.
4. Không thay các kỳ đã kiểm tra PASS; đóng ngoại lệ thì **loại mã khỏi hàng đợi xử lý thường xuyên**. Đánh dấu rõ ngoại lệ trong báo cáo kiểm kê và hồ sơ checkpoint. Nếu công ty phát hành đính chính có ký, hoặc xuất hiện BCTC **kiểm toán năm tài chính 2026** (không gọi nhầm báo cáo năm là bán niên “soát xét”), mới kích hoạt đối chiếu lại; nếu không có bất nhất thì giữ nguyên.
5. Khi kiểm tra báo cáo kiểm toán FY2026, đối chiếu 12M/9M, B01/B02/B03, nguồn áp dụng Thông tư 99/43, thuyết minh tài sản bảo đảm và tiền gửi hạn chế; sửa dữ liệu chỉ khi có căn cứ và kiểm thử VND chính xác. Luôn lưu lại lịch sử phiên bản.

**Đã áp dụng riêng cho GEG:** `data/financials-GEG.json` lưu `ticker_processing_completion` và `source_validation.case_closure_status`; hồ sơ quyết định:
`reports/source-audits/GEG-2026Q2-accepted-issuer-vintage-closure-pending-audited-FY2026.json`. Chứng cứ H1 EY soát xét (PDF 74 trang, B03 trang 16–17, TM37 trang 73) là mốc đối chiếu ưu tiên, nhưng bản quý II công bố trước đó được giữ nguyên tại cột nguồn gốc. Hai phiên bản B03 lũy kế đã cân chính xác; chênh lệch riêng Q2 do cơ sở báo cáo được chấp nhận ở cấp xử lý chứ không bị biến thành một luồng tiền thực tế.

**Phạm vi:** chỉ áp dụng khi có quyết định chấp nhận ngoại lệ rõ ràng và nguồn hợp lệ, **không tự áp dụng cho IDC hoặc mã khác**. Không coi ngưỡng 0,1% là lý do bỏ qua sai cầu tiền.

## 8. IDC — đã xử lý theo nguồn doanh nghiệp có ký, ngoại lệ chuyển tiếp TT99/TT43 (21/11/2026)

Sau khi người dùng chỉ dẫn tiếp tục xử lý mã IDC theo quy trình đã xác lập, hồ sơ nguồn IDC **7/7 kỳ hợp nhất Q1/2025–Q3/2026** được kết thúc ở trạng thái **hoàn thành chuẩn hóa nguồn và bảo lưu ngoại lệ chuyển tiếp**, không đánh đồng với B03 **quý II riêng độc lập đã kiểm chứng**.

- IDC Q1 2026 đã ký, B03 3M: mở đầu `553.052.678.239 VND`, cuối `800.729.495.703 VND`; thuyết minh 2.5 nêu TT99/2025.
- BCTC H1 soát xét nguồn đã ký, HNX/BSC SHA256 `f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944`: thuyết minh 3.1.2 nêu TT43/2026, thuyết minh 41 (PDF p71) điều chỉnh tiền tương đương tiền số dư mở `+890.796.892 VND` và các dòng so sánh **2025** (cộng biến động B03 2025 bằng 0). Việc này **không phải** luồng tiền thu quý II/2026.
- B03 6M của IDC theo báo cáo doanh nghiệp công bố: CFO `-5.019.037.910`; CFI `412.225.133.057`; CFF `-352.471.108.238`; net `54.734.986.909`; mở `553.943.475.131`; FX `6.117.592`; cuối `608.684.579.632 VND`. Từng bản gốc có cầu tiền chính xác.
- B03 9M Q3/2026 có số đầu năm giống H1 `553.943.475.131 VND`; quý III riêng `9M−6M` đã kiểm tra chính xác CFO `216.619.259.342`, CFI `93.759.529.850`, CFF `-449.106.095.224`, net `-138.727.306.032 VND`.
- Quý II riêng từ B03 6M trừ B03 3M chỉ là **phép tính liên phiên bản nguồn**; cầu tiền có sai khác `890.796.892 VND` được giải thích về **phân loại lại tiền đầu kỳ**, nhưng vẫn chưa có báo cáo quý I/2026 cùng cơ sở TT43 ký lại. **Không đưa phép trừ vào trường CFO/CFI/CFF quý độc lập như số thực tế**; trường đó phải tiếp tục `null`.
- Mã IDC được loại khỏi danh sách rà soát điểm nghẽn **thường xuyên**, chuyển ngoại lệ sang **chờ kiểm toán hợp nhất năm 2026**. Chỉ mở lại trên báo cáo năm đã kiểm toán/đính chính ký gốc có số liệu mới hoặc mâu thuẫn. Cách này **không tuyên bố doanh nghiệp sai luật** và không tự động áp dụng cho mã khác.

Mã hóa tại: `data/financials-IDC.json` → `ticker_processing_completion`, `2026-Q2.source_validation.case_closure_status`; hồ sơ `reports/source-audits/IDC-2026Q2-issuer-source-accepted-closure-pending-audited-FY2026.json`; kiểm thử `scripts/verify_idc_issuer_source_accepted_completion.py`; tích hợp `validate.yml` và kiểm kê 32 mã.

**Điểm phân biệt pháp lý:** ngày ký/hiệu lực TT43 khác kỳ kế toán phải áp dụng; sự vắng mặt tên TT43 trên bản Q1 không đủ kết luận sai quy định, cũng không chứng minh Q1 cùng phiên bản như H1. Trạng thái đã hoàn thành **là trạng thái quản lý tiến độ dùng nguồn có công bố**, không phải chứng nhận kiểm toán cho số chưa hề được báo cáo riêng.
