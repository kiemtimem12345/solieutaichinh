# CHECKPOINT — Rà soát tất cả nguồn dữ liệu tài chính đã bổ sung (Vietstock/WiData/HOSE/HNX/SSC/doanh nghiệp), 20/11/2026

## Nguồn và kiểm kê kết quả thử trực tiếp
- Main checkpoint trước khi bắt đầu: `e89e4f68300fd4c94ba4e7d4848ce504147c97b9` (PR #89 HOSE/HNX độc lập, website 45/45 SHA PASS).
- GitHub Actions source-audit `44675803871` PASS (JSON artifact `14602347195`); `scripts/audit_previous_financial_sources_20261120.py` chạy GET/HEAD đúng ngữ nghĩa, phân nhóm nguồn, lưu response/timeout, không thay đổi bất kỳ BCTC nào.
- 22 URL nguồn đầu mối, **19 HEAD/GET trực tiếp phản hồi HTTP 200**. Các trường hợp không trả 200:
  1. `congbothongtin.ssc.gov.vn` (UBCKNN): **DNS resolution failure (curl 6)** trong runner; không kết luận không có hồ sơ.
  2. `www.hnx.vn` trang công bố IDC: lỗi chuỗi chứng chỉ OpenSSL (curl 60), không hạ bảo mật; vẫn dùng bản ghi HNX/BSC nguồn gốc đã xác minh.
  3. Một đường danh mục PV GAS `www.pvgas.com.vn/sanpham-dich-vu/category/bao-cao-tai-chinh` trong runner HEAD + GET đều 404, dù bản cache web tìm kiếm có lưu trước đó. Dùng **đường trực tiếp báo cáo** /DesktopModules... hoặc **trang tài liệu cổ đông** trả 200, không coi PDF gốc mất.
- Năm trang WiData `widata.vn/{PLX,GAS,VDS,GEG,IDC}?tab=documents`: 5/5 HTTP 200, **chỉ đối chiếu thứ cấp**; HTTP 200 không chứng minh dữ liệu bảng đầy đủ, cập nhật hay giống số báo cáo ký gốc. Không dùng làm nguồn thay thế B01/B02/B03.
- Trang Vietstock eDocuments `finance.vietstock.vn/<ticker>/tai-tai-lieu.htm?doctype=1`: **5/5 GET 200**, dù **HEAD trả 404** ở chính các URL đó. Lỗi HEAD-only đã được sửa bằng GET có giới hạn dung lượng. Không được ghi sai `source unavailable` chỉ vì HEAD.
- **Vietstock public eDocuments POST `/data/getdocument` + CSRF cookie phiên**: 5/5 mã có 2 năm 2025/2026 đọc thành công, **101 ứng viên liên kết tài liệu**:
  - PLX: 2025 **12**, 2026 **8**;
  - GAS: 2025 **13**, 2026 **8**;
  - VDS: 2025 **12**, 2026 **8**;
  - GEG: 2025 **12**, 2026 **8**;
  - IDC: 2025 **12**, 2026 **8**.
  Đây là 101 **document URLs** (gồm mẹ, hợp nhất, soát xét, kiểm toán), không phải 101 kỳ hợp nhất PASS. Danh mục xác nhận link, **không thay thế nguồn gốc PDF issuer ký**.
- Nhà phát hành: `plx.petrolimex.com.vn/quan-he-nha-dau-tu.html` HEAD 200, `www.petrolimex.com.vn/nha-dau-tu.html` 200; `www.vdsc.com.vn` 200; `idico.com.vn` 200; `www.pvgas.com.vn/quan-he-co-%C4%91ong/tai-lieu-co-%C4%91ong` 200; PV GAS Q2/2026 **PDF issuer trực tiếp** `https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14585&documentid=3358&moduleid=648&portalid=0` trả HTTP 200, **Content-Length 8,755,462 bytes**. Ngưỡng nguồn nếu tải phải có đúng bytes, SHA256, visual B01/B02/B03.
- IDC HNX filing original mirrored via BSC `https://www.bsc.com.vn/News/NewsAttachedFile/1632697-1`: 200; hồ sơ IDC Q3/2026 đã PASS từ checkpoint cũ, không tải/làm lại.
- HOSE original PLX parent Q3 `https://staticfile.hsx.vn/Uploads/UploadDocuments/2510747/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20me%20Q3%20nam%202026.pdf`: 200 Content-Length **14,241,486** bytes; phiên bản Petrolimex `https://files.petrolimex.com.vn/files/.../20261030 ...pdf` đã ký, SHA `a8073e...`, dung lượng **14,198,075** bytes. Chênh **43,411 bytes** chưa chứng minh CFF được sửa.
- **MỚI: HOSE range probe trên chính tệp Q3 mẹ** thành công HTTP `206 Content-Range: bytes 0-4095/14241486`, nhận **4,096/4,096 byte**, bắt đầu `%PDF`. Source audit `44675803871`. Bằng chứng hỗ trợ tải PDF thành từng đoạn, nhưng **không có quyền nâng PASS trước khi mọi đoạn hợp lệ và xem ảnh B03**.
- Đã thử `scripts/recover_plx_hose_parent_q3_by_ranges.py` workflow `44675990309`: **kết quả cancelled** do từng 256KiB HTTP 206 quá chậm, nhiều segment timeout sau 44s dù Content-Range đúng; chỉ 2–3/55 segment thành công trước khi hết thời gian. **KHÔNG** ghép bản PDF thiếu và KHÔNG ghi HOSE visual PASS. Không tự động chạy lại khi nguồn vẫn chậm; chỉ thử lại nếu thay đổi cách truyền hoặc có văn bản đính chính.
- **ĐÃ KHẮC PHỤC ĐỐI CHIẾU BẢN THỨ HAI Q3 CÔNG TY MẸ QUA VIETSTOCK**: `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/PLX_Baocaotaichinh_Q3_2026_Congtyme.pdf?ver=35b831da`. API eDocuments xác nhận FileInfoID **566125**; workflow `44676432848` PASS, artifact `14602178653`, file **14,241,486 bytes, 39 trang**, SHA256 `ab13686742234d95930b6c16e51300f7b2a2600e07919eb4b0a3464c820a6b6d`.
- Bản signed Petrolimex trước: **14,198,075 bytes**, 39 trang, SHA256 `a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef`.
- Đã mở **hai file PDF trọn vẹn trong PyMuPDF**; **cả 39/39 embedded original scanned page images có cùng SHA256 từng ảnh** (không chỉ so bản tóm tắt hoặc OCR); khi render grayscale đến 0.8×, 38/39 trang từ 2 đến 39 giống **100% pixels**, trang 1 khác biệt nhỏ phần chữ bao/cách đóng gói. **Hai ảnh B03 trang PDF 7 và 8 source-image hash tuyệt đối giống nhau**:
  - p7 `2087fb122a23d4d850ed05498acbc7b1434f543ceb53998336f4943f98138296`;
  - p8 `f8dddc318d103c0750b12eb922355696fdd0b9213786c3591dd4abc6f5d2cd6e`.
- Vì ảnh ký gốc B03 giống, **không có thay đổi CFF trong Vietstock mirror**: source printed 5,966,101,543,718 so sum components 6,053,755,558,718 = **87,654,015,000 VND discrepancy**. Không suy luận HOSE PDF identical chỉ từ trùng Content-Length 14,241,486: **chưa có HOSE SHA256**. B03 PLX Q3 parent vẫn **BLOCKED**, không publish CFO/CFI/CFF riêng Q3 mẹ.
- Đã lưu `source_validation.vietstock_alternate_signed_original_source_comparison` trong **PLX parent 2026-Q3** với đủ 2 source SHA, source image hashes, 39/39 pixel/source matching, sai lệch original CFF, và trạng thái HOSE byte comparison chưa xác minh. `scripts/verify_plx_hose_independent_disclosures.py` mở rộng regression khóa nguồn và duy trì parent B03 blocked.


## Kết quả đối chiếu trạng thái ticker production main
- GAS có 7 kỳ hợp nhất Q1/2025–Q3/2026 PDF gốc visual PASS (một số kỳ có exception về comparative cash), thêm Q3 2026 mẹ riêng đã PASS; GEG 7 kỳ hợp nhất source B01/B02/B03 visual đã xác minh, **Q2/2026 standalone cash deferred** do mismatch vintage. VDS 7 kỳ hợp nhất original visual, IDC 7 kỳ original visual (Q2/2026 quarter cash deferred do TT99). Không xử lý lại.
- PLX Q3/2026 **hợp nhất** PDF original 36 trang và H1 soát xét 83 trang, 111 fields + 40 exact-VND checks, PASS; bản Q3/2026 **công ty mẹ** B03 đóng băng vì dòng CFF 40 in +5,966,101,543,718 nhưng tổng 31–36 +6,053,755,558,718 VND, chênh **87,654,015,000** VND. HOSE document byte comparison still pending.
- PLX Q1/Q3/Q4 2025 và Q1/Q2 2026 chưa full source B01/B02/B03 verified; đây là nhóm cần đối chiếu tiếp, không trùng các mã đã hoàn tất.

## Sàng lọc nhầm nguồn
- Kết quả web `files.petrolimex.com.vn/pdfs/.../EN_FinancialStatements_Q3_2026_Separated_signed.pdf` từng có dòng tiền 87,745,880,634 VND là **Petrolimex Petrochemical Corporation - PLC**, không phải `PLX` Tập đoàn Xăng dầu Việt Nam; tuyệt đối **không** lấy PDF PLC để lấp PLX.
- `stockbiz.vn/ma-chung-khoan/PLX/tai-chinh` CFO Q3 2026 hợp nhất khoảng -3,432 tỷ; có thể đối chiếu xu hướng nhưng số đã làm tròn không phải chứng cứ chính xác đến VND. Các báo cáo phân tích, dự phóng 2026F cũng không dùng làm BCTC gốc.

## Nguyên tắc thực thi tiếp
- Mọi nguồn có cấp độ xác nhận: (A) full signed issuer/exchange original PDF SHA+image+B01/B02/B03; (B) issuer official listing or same-document mirror URL; (C) secondary aggregator WiData/Stockbiz; (D) unavailable or transient error. Chỉ cấp A nâng `manually_visual_reviewed` / financial PASS.
- Nguồn HOSE/HNX/UBCKNN luôn được xác thực đúng mã/sở và phạm vi hợp nhất/công ty mẹ; không bỏ HTTPS verification hoặc bịa source link.
- Chỉ giữ Q1/2025+, tối đa 20 kỳ, VND source, triệu VND normalized, dấu âm B03; chênh ≤0.01% chấp nhận, các cấu phần tiền vẫn phải cân nguồn/tổng.
- Sau khi HOSE range PDF complete, so ảnh trang B03 7–8 với issuer PDF ký và rà lại CFF. Nếu HOSE cũng in sai, giữ 87.654.015.000 bị chặn và chỉ tìm bản đính chính chính thức.

## Các đường tài liệu PLX ưu tiên từ Vietstock API 2025/2026 (không nhập lại dữ liệu đã PASS)
- Năm 2025 Vietstock public `/data/getdocument` trả 12 tài liệu: 4 quý × (mẹ+hợp nhất), H1 soát xét 2 phạm vi, năm kiểm toán 2 phạm vi.
- PLX hợp nhất Q1 2025: `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY 1/PLX_Baocaotaichinh_Q1_2025_Hopnhat.pdf`.
- PLX hợp nhất Q3 2025: `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY 3/PLX_Baocaotaichinh_Q3_2025_Hopnhat.pdf`.
- PLX hợp nhất Q4 2025: `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY 4/PLX_Baocaotaichinh_Q4_2025_Hopnhat.pdf`.
- PLX hợp nhất Q1 2026: `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY 1/PLX_Baocaotaichinh_Q1_2026_Hopnhat.pdf`.
- PLX hợp nhất Q2 2026: `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY 2/PLX_Baocaotaichinh_Q2_2026_Hopnhat.pdf`.
- PLX soát xét H1 2025 hợp nhất: `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY 2/PLX_Baocaotaichinh_6T_2025_Soatxet_Hopnhat.pdf`.
- PLX năm 2025 hợp nhất kiểm toán: `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/NAM/PLX_Baocaotaichinh_2025_Kiemtoan_Hopnhat.pdf`.
- Các URL trên là **link nguồn từ catalog verified**, không có full-source exact-VND PASS mới. Tiếp tục từng kỳ PLX chưa đủ đã audit, tải PDF gốc và lưu checkpoint, không mở lại 5 ticker vốn đã PASS.
