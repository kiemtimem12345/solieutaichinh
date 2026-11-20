# CHECKPOINT — PLX Q1/2026 hợp nhất: bản gốc ký, B01/B02/B03 đến VND, 3 điểm khác biệt được khoanh vùng

Ngày 20/11/2026. Repository production `kiemtimem12345/solieutaichinh`. Main cơ sở trước cập nhật `e8d6de4676e2969bf611161272480238e908fd05` sau PR #95 PLX Q4/2025. Source partial Q1/2026 chưa xác minh ảnh trước phiên này. Q1–Q3/2025 đã PASS, Q4/2025 có phân loại khác phiên bản FY audited và 8 trường quý bị khóa, PLX Q3/2026 công ty mẹ có CFF sai trên PDF gốc (87.654.015.000 VND) vẫn bị khóa. Không xử lý lại các kỳ đã hoàn thành.

## Bản gốc issuer signed 29/04/2026
- Vietstock original public eDocuments: `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/PLX_Baocaotaichinh_Q1_2026_Hopnhat.pdf`, document ID `545469`.
- **36 trang, 7.990.499 byte, SHA256 `158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f4bc5f9`**, ký 29/04/2026; URL source catalog `https://finance.vietstock.vn/PLX/tai-tai-lieu.htm?doctype=1`.
- GitHub Actions recovery `44687366816` PASS, artifact `14606503712` chứa PDF đầy đủ, ảnh 19 trang đầu; **đã xem ảnh gốc B01 PDF trang 2–4, B02 trang 5, B03 trang 6–7** (dấu, chữ ký). PDF quét, không có văn bản tài chính selectable nên dùng ảnh gốc; số gốc VND, lưu số triệu VND đầy đủ thập phân 6 số.
- Ledger nguồn nguyên VND lưu `reports/source-audits/PLX-2026Q1-consolidated-signed-original-vnd.txt`: 82 số B01/B02/B03 và 55 dòng chi tiết B01, plus số so sánh đầu kỳ.
- `scripts/verify_plx_q1_2026_original.py` kiểm tra **34 phương trình số học 0 VND**, 3 khác biệt được khoanh vùng, EPS cơ bản để null, tỷ suất annualized, và PLX Q3/2026 mẹ vẫn khóa. CI thêm test trong `.github/workflows/validate.yml`.

## Tóm tắt tài chính xác minh từ PDF gốc — VND
| Chỉ tiêu hợp nhất Q1/2026 | Số in |
|---|---:|
| Tài sản 31/03/2026 | 106.072.582.121.188 |
| Nợ phải trả | 77.188.587.290.317 |
| Vốn chủ sở hữu | 28.883.994.830.871 |
| Tiền và tương đương tiền cuối Q1 | 10.034.406.335.760 |
| Doanh thu thuần | 98.697.936.100.129 |
| Lợi nhuận gộp | 3.700.744.454.398 |
| Lợi nhuận hoạt động | -493.347.203.011 |
| LNTT | -495.815.051.996 |
| LNST | -662.477.125.907 |
| LNST thuộc cổ đông mẹ | -762.973.681.188 |
| CFO (3 tháng/riêng Q1) | +9.375.725.757.265 |
| CFI | +764.690.442.359 |
| CFF | -7.689.092.776.722 |
| Tiền thuần | +2.451.323.422.902 |
| Ảnh hưởng FX | -5.156.817.373 |
| Tiền đầu kỳ (số Q1 đã phân loại lại) | 7.588.239.730.231 |
| Tiền cuối kỳ | 10.034.406.335.760 |

- B03 Q1 3 tháng tự cân: CFO+CFI+CFF=2.451.323.422.902 VND; 7.588.239.730.231 +2.451.323.422.902 -5.156.817.373=10.034.406.335.760 VND đúng B01. Các cấu phần tiền chính và B02 P&L khớp số in gốc đến VND; 34 checks 0 VND.
- B01 đầu năm Q1 2026 tổng tài sản **85.855.397.411.812**, equity **29.561.742.828.621**, đúng bản FY2025 audited tổng khoản; ROA annualized **-2,76%**, ROE **-9,07%** từ LNST âm, số dư đầu/cuối kỳ B01 có chữ ký.
- **EPS cơ bản** B02 PDF p5 dòng **mã 70** cột 2026 in **trống**; giá trị cũ `eps=70` là OCR nhầm mã chỉ tiêu. Để `eps=null`, `eps_ytd=null`; dòng **EPS suy giảm mã 71** cột 2026 là **(521) VND/cổ phiếu**, lưu `diluted_eps=-521`.

## Ba ngoại lệ, không được âm thầm ép cho khớp
1. **B01 phải thu ngắn hạn**: tổng phụ in `19.662.068.640.316`, nhưng cộng các dòng được liệt kê trên đúng ảnh nguồn p2 = `19.652.984.670.130`, thiếu **9.083.970.186 VND**, khoảng **0,04620%**, vượt 0,01%. Để nguyên tổng in, nêu nguồn chưa giải thích khoản thiếu, không đánh dấu toàn bộ B01 component PASS.
2. **B01 nợ ngắn hạn**: tổng phụ in `76.146.303.967.243`, tổng các khoản con liệt kê p3 = `76.137.215.001.801`, thiếu **9.088.965.442 VND**, **0,01194%**, cũng vượt 0,01%. Nợ tổng, tài sản/vốn chủ vẫn cân đúng VND. Không suy luận khoản 9 tỷ này thành số bất kỳ ở dòng con.
3. **Số dư tiền đầu kỳ khác phiên bản**: B01 và B03 Q1/2026 gốc ký in `7.588.239.730.231` VND, còn bản hợp nhất FY2025 kiểm toán ngày 31/03/2026 in **10.675.798.547.805** VND cuối năm. Chênh **-3.087.558.817.574 VND**. Nguồn Q1/2026 đánh dấu **“phân loại lại”** ở cột so sánh B01 và B03; chưa xác minh tài khoản đích và thuyết minh chi tiết điều chỉnh. Đây **không** phải dòng tiền riêng Q1 và không ép vào CFO/CFI/CFF.
- Kết quả: B01 **đã xem PDF gốc** và cân đối cấp cao đúng, nhưng hai tổng phụ bị cảnh báo; B02/B03 đã xem nguồn có chữ ký và kiểm tra đúng. Trạng thái `signed_original_visual_B01_B02_B03_Q1_2026_34_exact_vnd_checks_with_B01_subgroup_and_opening_cash_vintage_exceptions`, không tự ghi PASS toàn bộ chi tiết bảng cân đối.

## Triển khai/tiếp tục
- Cần PR và CI `scripts/verify_plx_q1_2026_original.py` PASS trước khi merge, sau merge smoke **45/45 exact SHA256** website. Lưu checkpoint & PDF gốc Library `/Projects/so-lieu`.
- Nếu tìm thấy thuyết minh cụ thể cho 2 subtotal ~9 tỷ hoặc phân loại lại cash, cập nhật `source_validation` và làm rõ theo văn bản gốc; không sửa số in để ép khớp.
- Kỳ tiếp **PLX Q2/2026 hợp nhất**: dùng PDF Q2/2026 ký gốc B01/B02 và B03 sáu tháng; đối chiếu với BCTC H1/2026 soát xét và **số Q1/2026 cùng phiên bản so sánh tiền**. Không dùng kết quả báo cáo năm kiểm toán để thay số đầu năm Q1 có phân loại lại. Chuyển sang Q3/2026 chỉ sau khi Q2 đã đối chiếu, không làm lại Q3 hợp nhất đã PASS. Các ticker GAS/VDS/GEG/IDC đã PASS giữ nguyên.
