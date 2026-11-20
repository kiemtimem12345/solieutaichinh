# CHECKPOINT — PLX Q4/2025 hợp nhất: bản gốc Q4 và KPMG FY2025 khác phiên bản, khóa dòng tiền riêng quý IV

Ngày 20/11/2026. Repository `kiemtimem12345/solieutaichinh`, main nền tảng `7a5613060c306e9e4a48a199bc97b0d6a3dac857` sau PR #93: PLX Q1/Q2/Q3 2025 hợp nhất PASS, GAS/VDS/GEG/IDC các kỳ đã PASS không làm lại, PLX Q3/2026 hợp nhất PASS. PLX Q3/2026 công ty mẹ B03 dòng 40 gốc sai tổng cấu phần **87.654.015.000 VND**, tiếp tục BLOCKED.

## Đã khôi phục tài liệu gốc, không OCR làm nguồn chính
- PLX Q4/2025 hợp nhất ký 29/01/2026, `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/PLX_Baocaotaichinh_Q4_2025_Hopnhat.pdf`. **31 trang PDF, 13.759.900 byte, SHA256 `35a0f637ffbb0ecf5161337f5289e5e2572dc5655ff865d2d5c8eca592187e61`**. Xem B01 PDF trang 2–4, B02 trang 5 (Q4 và lũy kế năm), B03 trang 6–7 (lũy kế 12 tháng), dấu/ chữ ký gốc.
- PLX hợp nhất năm 2025 được KPMG kiểm toán ký 31/03/2026, `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/NAM/PLX_Baocaotaichinh_2025_Kiemtoan_Hopnhat.pdf`. **85 trang PDF, 12.190.357 byte, SHA256 `5570d8cdb64de8f7978f6ef0a753afd08311a08e0dceb7f10a85b90e744b1735`**. Xem B01 PDF trang 6–9, B02 10–11, B03 12–14.
- Cả hai PDF đã khôi phục **đầy đủ, SHA256** từ Vietstock original tài liệu công khai, không trộn báo cáo mẹ; GitHub Actions recovery `44684657529` PASS, artifact `14606265504` lưu hai bản nguồn gốc và ảnh.
- Bản 9M Q3/2025 hợp nhất đã PASS từ PR #93: `reports/source-audits/PLX-2025Q3-consolidated-original-vnd.txt`, PDF SHA `012d34a3166e67ca61de8c7442bb7474479853b55f105b30c60347ee4e40453c`. Không xử lý lại.

## Đối chiếu giữa hai kỳ báo cáo gốc (đơn vị VND)
| Chỉ tiêu | Q4/2025 công bố lần đầu (31 trang) | FY2025 sau kiểm toán (85 trang) | Kiểm toán trừ Q4 gốc |
|---|---:|---:|---:|
| Tài sản | 86.116.520.697.256 | 85.855.397.411.812 | -261.123.285.444 |
| Nợ phải trả | 56.640.123.798.180 | 56.293.654.583.191 | -346.469.214.989 |
| Vốn chủ | 29.476.396.899.076 | 29.561.742.828.621 | +85.345.929.545 |
| Doanh thu thuần 12M | 309.924.230.750.513 | 309.874.515.169.939 | -49.715.580.574 |
| LNST 12M | 3.038.078.002.060 | 3.026.744.562.818 | -11.333.439.242 |
| CFO 12M | +4.254.126.280.969 | +3.990.368.093.758 | -263.758.187.211 |
| CFI 12M | -7.693.713.011.502 | -7.318.982.155.223 | +374.730.856.279 |
| CFF 12M | -701.839.793.706 | -928.898.351.454 | -227.058.557.748 |
| Biến động tiền 12M | -4.141.426.524.239 | -4.257.512.412.919 | -116.085.888.680 |
| Ảnh hưởng tỷ giá | +11.511.581.307 | +242.168.409 | -11.269.412.898 |
| Tiền cuối năm | 10.803.153.849.383 | 10.675.798.547.805 | **-127.355.301.578** |

- **Hai bản B01/B02/B03 mỗi bản tự cân đối đến từng VND**, 24 source checks trong `scripts/verify_plx_q4_2025_original_vs_audited_vintage.py` đều 0 VND; không có căn cứ ghi đè bản gốc Q4 với bản kiểm toán cùng lúc.
- B02 **riêng Q4** như in nguồn ký đầu tiên: doanh thu thuần 81.892.812.959.191; LNTT 886.090.899.162; LNST 696.927.885.625; EPS 350 VND/cp. B02 12M như in nguồn Q4 và B02 12M kiểm toán được lưu riêng.
- Từ **Q4 bản công bố 12M trừ 9M signed Q3 cùng scope**, candidate CFO +5.410.630.261.480; CFI -736.902.563.649; CFF -6.469.658.074.529, net -1.795.930.376.698, FX -17.473.713.877; từ B03 FY **kiểm toán 12M trừ 9M** candidate CFO +5.146.872.074.269; CFI -362.171.707.370; CFF -6.696.716.632.277, net -1.912.016.265.378, FX -28.743.126.775. Mỗi candidate tự khớp cầu tiền, **nhưng khác nguồn phiên bản rất lớn**. Không có cơ sở chọn một candidate mà không ghi vintage.
- **Dấu cổ tức:** theo bản Q4 lần đầu trừ Q3 9M ra dòng `dividends_paid` riêng Q4 **+53.608.752.723 VND** (dương bất thường cho dòng chi), bản audited 12M trừ 9M lại ra **-146.879.152.932 VND**. Cần nguồn thuyết minh điều chỉnh trước khi công bố.
- Bản nguồn **Q4 chính thức** trong `data/financials-PLX.json` giữ **31 chỉ tiêu B01/B02/12M B03** nguyên giá trị VND chuyển thành triệu chính xác (không tròn trước), EPS VND/cp; `source_validation` lưu 2 SHA, 2 phiên bản, 2 cầu tiền candidate, mọi chênh lệch. Các trường dòng tiền **riêng quý IV** `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow`, `net_cash_change`, `foreign_exchange_effect`, `cash_beginning`, `capital_expenditure`, `dividends_paid` được để **null**, không công bố số quý giả. Số tiền cuối năm `cash_ending` giữ theo bản gốc 31p, đúng B01 bản đó.
- Bằng chứng nguồn chữ ký sẵn trong `reports/source-audits/PLX-2025Q4-original-vs-audited-FY2025-exact-vnd.txt`; không đưa toàn bộ PDF sang Git.

## Văn bản HOSE đối chiếu chính thức 01/04/2026
- Petrolimex gửi UBCKNN/HOSE **0677/PLX-TCKT**, bản PDF chính thức:
  `https://staticfile.hsx.vn/Uploads/UploadDocuments/2449947/20260401%20-%20PLX%20-%20Giai%20trinh%20bao%20cao%20tai%20chinh%20nam%202025.pdf`
- Xác nhận LNST **hợp nhất FY2025 sau kiểm toán 3.026.744.562.818 VND**, đúng bản kiểm toán trích số, và nhận định chênh lệch *kết quả kinh doanh* trước/sau kiểm toán dưới 5% nên không cần giải trình kết quả. **KHÔNG** giải thích các điều chỉnh B03 chi tiết (CFO/CFI/CFF), không được lấy văn bản này để tự coi 127.355.301.578 VND tiền cuối năm chênh là hợp lệ không cần chú thích.

## Kiểm tra trước/sau merge và bước tiếp tục
- `scripts/verify_plx_q4_2025_original_vs_audited_vintage.py` độc lập so 31 trường tài chính, 24 kế toán/cash source identities VND 0, hai candidate cash bridge, phân biệt 2 SHA, xác nhận 8 trường quý null, không đụng PASS Q3/2025 hay PLX Q3/2026 parent CFF; `.github/workflows/validate.yml` có regression. **Chỉ PR merge sau CI financial PASS.** Sau merge xác minh production smoke **45/45 HTTP(S) SHA256** và pages build. Lưu checkpoint Library.
- Nếu có văn bản đính chính/thuyết minh báo cáo kiểm toán để đối chiếu từng dòng, giải quyết Q4 từ source 12M đúng phiên bản với 9M, tránh lặp thử tải hai PDF đã có. Nếu không có, Q4 riêng cash **deferred**, tiếp sang PLX Q1/2026 hợp nhất chưa visual PASS, rồi Q2/2026, lần lượt từng kỳ. Không hỏi người dùng.
