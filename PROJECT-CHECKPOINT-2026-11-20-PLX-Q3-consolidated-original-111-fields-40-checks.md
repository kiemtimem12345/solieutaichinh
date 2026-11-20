# CHECKPOINT — PLX Q3/2026 hợp nhất B01/B02/B03 nguyên bản, dòng tiền Q3 từ H1 soát xét — 20/11/2026

## Nguồn gốc, phạm vi và trạng thái
- Repository production: `kiemtimem12345/solieutaichinh`, main trước PR `0deae0df49ef850d43ae7312643bb82c8b29f55d`, PR #87: https://github.com/kiemtimem12345/solieutaichinh/pull/87 .
- **Chỉ hợp nhất PLX Q3/2026**: hoàn tất xác minh B01/B02/B03 từ PDF issuer có chữ ký; không dùng nhầm công ty mẹ. Bản PLX **công ty mẹ** Q3/2026 vẫn B03 BLOCKED vì sai lệch CFF 87,654,015,000 VND trên ảnh gốc, được giữ nguyên theo PR #86.
- Đã có báo cáo H1/2026 hợp nhất KPMG cùng phạm vi, soát xét ngày 28/08/2026; dùng riêng B03 H1 để trừ khỏi B03 9 tháng Q3.
- Trước khi merge, chỉ nhánh PR thay đổi; **không xác nhận production đến khi CI và site smoke sau merge PASS**. Phạm vi Q1/2025+, tối đa 20 kỳ, normalized triệu VND từ số VND gốc, EPS VND/cổ phiếu. Giữ nguyên UI.

## Khắc phục nghẽn nguồn
- Tìm nguyên nhân dữ liệu Vietstock eDocuments tải động: `/bundles/company/document/jsx` gọi public `POST /data/getdocument` cùng CSRF token và cookie phiên của trang tài liệu. Tạo `scripts/discover_plx_2026_vietstock_document_api.py` và workflow `discover-plx-2026-vietstock-docs.yml`. Run `44665859456` PASS và trả 8 PDF PLX năm 2026, bao gồm 4 tài liệu Q3/H1 đúng phạm vi.
- Dò nguồn HOSE official trước từ disclosure listings, nhưng `staticfile.hsx.vn` trả chưa hết tệp (80,618/18,543,309 byte trong 28 giây); đã sửa extractor loại tệp tải dở, không cho SHA256 trên prefix. Public HTTP source timeout không đồng nghĩa thiếu báo cáo.
- `scripts/recover_plx_2026_consolidated_and_reviewed_h1.py` + workflow `recover-plx-2026-consolidated-and-reviewed-h1.yml`, run **44666024791** PASS **3/3 full issuer PDFs**; artifact **14596614646** với PDF đầy đủ và ảnh trang.
- PDF Q3 hợp nhất issuer signed 30/10/2026: `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/PLX_Baocaotaichinh_Q3_2026_Hopnhat.pdf`, **36 trang, 16,084,820 byte, SHA256 `e0b6cfd9463c211970d0172aa8d258b8983b84ea472d59e0a242aed9ddf5c587`**. Đã xem ảnh B01 trang PDF 2–4, B02 trang 5, B03 trang 6–7.
- PDF H1 hợp nhất KPMG reviewed 28/08/2026: `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/PLX_Baocaotaichinh_6T_2026_Soatxet_Hopnhat.pdf?ver=39c44c02`, **83 trang, 23,713,656 byte, SHA256 `e26c0d58e991895d3704c6b2417953b2fd962255af5197a33e24ed944bf3ccd6`**. Đã xem B03 trang PDF 12–13.
- PDF H1 công ty mẹ riêng 28/08/2026, cũng tải được (63 trang, 18,543,309 byte, SHA256 `a7929fbbc64f8f7fd201c33df9d09f32098ea1829ead9d6ea39c434f8821cd2c`). Chỉ lưu làm nguồn cùng phạm vi cho *parent*, không dùng để tính dòng tiền *consolidated* Q3. Parent Q3 B03 cần bản đính chính chính thức.

## Chỉ tiêu PLX hợp nhất Q3/2026 đã kiểm tra từ ảnh PDF gốc (VND)
- B01 ngày 30/09/2026: tài sản **109,008,605,779,427**, nợ **77,649,612,814,671**, VCSH **31,358,992,964,756**, các nhóm tài sản 82,061,675,824,229 ngắn hạn và 26,946,929,955,198 dài hạn. Tiền + tương đương **6,121,677,239,224**.
- B02 **riêng Q3**: doanh thu thuần **138,481,753,151,156**, giá vốn **131,178,675,012,184**, lãi gộp **7,303,078,138,972**, LNTT **1,790,008,444,119**, LNST **1,363,096,640,781**, cổ đông công ty mẹ **1,240,939,185,012**, NCI **122,157,455,769**, EPS **835 VND/cp**.
- B02 **lũy kế 9 tháng**: doanh thu thuần **373,225,984,756,314**, LNST **3,752,865,949,549**.
- B03 **9 tháng**: CFO **-2,487,945,351,739**, CFI **-6,928,744,654,125**, CFF **+7,960,585,978,080**, dòng tiền thuần **-1,456,104,027,784**, tiền đầu 2026 **7,591,431,856,806**, FX **-13,650,589,798**, tiền cuối **6,121,677,239,224**. 6 dòng cấu phần CFF cộng đúng dòng in 40 (0 VND lệch); khác với bản *công ty mẹ*.
- B03 H1 hợp nhất 6 tháng **đã soát xét**: CFO **+944,543,255,439**, CFI **+5,978,833,725,139**, CFF **-8,177,652,997,261**, net **-1,254,276,016,683**, đầu năm **7,591,431,856,806**, FX **+8,824,959,861**, tiền cuối 30/06 **6,345,980,799,984**.
- B03 **riêng Q3 = 9M ký − H1 đã soát xét, cùng scope**: CFO **-3,432,488,607,178**, CFI **-12,907,578,379,264**, CFF **+16,138,238,975,341**, net **-201,828,011,101**, FX **-22,475,549,659**, tiền đầu Q3 **6,345,980,799,984**, cuối Q3 **6,121,677,239,224**, capex **-773,959,104,832**, dividends **-1,227,987,400,207** VND.
- **40 phương trình kiểm thử độc lập đều dư sai số 0 VND**: B01 tổng và nhóm, B02 Q3 và 9M, B03 9M dòng CFO/CFI/CFF cấu phần, net và cash bridge; H1 net & bridge; quý riêng Q3 CFO/CFI/CFF/FX/capex/dividends/net, beginning cash, ending cash.
- Dòng tiền Q3 hợp nhất PASS; **KHÔNG** bỏ khóa dòng tiền Q3 công ty mẹ sai tổng CFF 87,654,015,000 VND.

## Triển khai và điểm tiếp tục
- `data/financials-PLX.json` chỉ chỉnh bản Q3 **hợp nhất**: **108 trường VND + 3 EPS**, 40 source checks, bản PDF SHA và URL, 9M B03 và riêng Q3, danh sách trường đối chiếu. Dữ liệu Q2/2026 cũ còn `partially_reconstructed_from_archived_source_text` **không sửa** vì chưa rà B01/B02 các kỳ Q2; chỉ dùng **B03 H1 PDF gốc** để tính Q3, không dùng JSON Q2 cũ.
- `scripts/verify_plx_q3_2026_consolidated_original.py` kiểm tra 40 phương trình VND & bằng chứng, `scripts/verify_plx_issuer_q3.py` sửa để tách PASS hợp nhất và blocked parent. `.github/workflows/validate.yml` thêm regression. Chỉ merge PR #87 sau CI PASS và xác minh site 45/45 sau merge.
- Checkpoint sau hoàn tất PR nên ưu tiên **PLX công ty mẹ Q3 B03**: tìm văn bản đính chính CFF hoặc xác nhận rõ nguyên nhân từ issuer, vì B03 dòng 40 in 5,966,101,543,718 khác tổng dòng 31-36 là 6,053,755,558,718. Có nguồn H1 parent đã tải thành công để đối chiếu, nhưng không tự sửa CFF. Sau PLX đi GAS Q2/2025 rồi VDS/GEG dựa audit.
