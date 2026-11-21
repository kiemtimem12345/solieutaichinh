# CHECKPOINT — VCI 2025-Q3 đã xác minh báo cáo gốc, tiếp Q4/2025

Ngày 21/11/2026. Repository kiemtimem12345/solieutaichinh; PR #124.

## Nguồn chính thức
- PDF gốc VCI ký/công bố 15/10/2025: https://www.vietcap.com.vn/api/cms-api/uploads/froala/files/20251015%20-%20VCI%20-%20CBTT%20BCTC%20Q3.2025.pdf
- 48 trang, 15.472.278 bytes, SHA-256 8a2cb804555583a1b7a9a4ae235fe220f2e050a38f1e10117172dec52a69ef68; source GitHub workflow 44922406049 SUCCESS, artifact ảnh nguồn 14713704732.
- PDF scan pdftotext chỉ 48 ký tự; đọc bằng hình B02 PDF p11, B03 pp13–14. Chứng từ gốc xác nhận công ty không có công ty con, không gọi là BCTC hợp nhất đã phát hành. Tiền của khách hàng môi giới tách khỏi tiền doanh nghiệp.

## Dữ liệu VND ký gốc
- B01 tài sản 29.717.532.042.853, nợ 17.047.567.491.881, vốn chủ 12.669.964.550.972, tiền cuối 2.637.051.863.422.
- B02 doanh thu quý 1.443.289.075.867, LNST quý 420.260.805.822, tài chính quý 5.716.520.412, tài chính lũy kế 18.846.616.831. Không nhầm cột quý/lũy kế trên trang B02 in ngang.
- B03 9M CFO -5.239.067.626.738, CFI -35.548.742.835, CFF +3.167.896.300.250, tiền thuần -2.106.720.069.323, tiền mở 4.743.771.932.745, tiền cuối 2.637.051.863.422.
- Đối chiếu PwC soát xét H1 2025 đã PASS: Q3 riêng CFO -5.129.888.190.051, CFI -8.269.114.883, CFF +7.302.932.240.000, net +2.164.774.935.066; tiền đầu quý 472.276.928.356, cuối quý 2.637.051.863.422. Tổng dòng tiền/cầu nối sai số 0 VND.

## Code thay đổi
- data/financials-VCI.json: chỉ cập nhật Q3/2025 (66 trường gốc, riêng quý, đơn vị triệu VND); Q1 và Q2 2025, Q3 2026 giữ nguyên.
- reports/source-audits/VCI-2025Q3-issuer-signed-9M-minus-H1-vnd.json: nguồn ký, hash, các đối chiếu VND.
- scripts/verify_vci_2025q3_signed_original.py: 23 phương trình nguồn và cầu tiền, 4 lỗi giả lập phải bị chặn.
- scripts/inspect_vci_2025q3_original_source.py và .github/workflows/inspect-vci-2025q3-original.yml: nguồn PDF, ảnh bằng chứng giới hạn.
- .github/workflows/validate.yml: bắt buộc test chứng cứ mới.

## Tiếp tục
- Chỉ merge PR #124 khi kiểm thử tài chính PASS và nguồn đã kiểm tra. Sau đó kiểm tra main và nếu có thể kiểm tra production; không nhận đã deploy khi chưa có bằng chứng.
- Tiếp theo VCI Q4/2025 → Q1/2026 → Q2/2026; Q3/2026 đã PASS, không load lại. Sau VCI tới VCK.
- GEG, IDC đã đóng theo nguồn công bố có ngoại lệ Q2 chờ kiểm toán FY2026; PLX Q3/2026 mẹ B03 CFF lệch 87.654.015.000 VND còn chặn. MBB, GAS, VDS, VIX đã PASS 7/7.
