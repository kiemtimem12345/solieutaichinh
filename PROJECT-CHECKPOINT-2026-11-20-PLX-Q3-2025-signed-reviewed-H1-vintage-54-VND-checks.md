# CHECKPOINT — PLX hợp nhất Q3/2025: bản gốc ký + H1 2025 KPMG soát xét, xử lý khác biệt phiên bản — 20/11/2026

## Điểm tiếp tục chính xác
- Repo production `kiemtimem12345/solieutaichinh`, main ban đầu **`0a30602734bdc8936e215e22e5cd1bc240658f2f`** sau PR #92 (PLX Q1/Q2 hợp nhất 2025 đã PASS; site smoke 45/45 run `44681397314` PASS).
- Chỉ cập nhật **PLX hợp nhất 2025-Q3**. Không mở lại PLX 2025-Q1/Q2 đã PASS; chỉ đọc B03 H1 trước để lập phép so. GAS, VDS, GEG, IDC, PLX 2026-Q3 hợp nhất không đụng tới. PLX **2026-Q3 công ty mẹ** B03 CFF nguồn in lệch 87,654,015,000 VND vẫn bị chặn.
- Bản 2025-Q3 cũ chỉ OCR một phần, EPS 369, PAT 705,970 triệu VND đã làm tròn, capex YTD OCR cắt thiếu, và dòng tiền quý dùng bản H1 **trước soát xét**. Khôi phục gốc cả Q3 và bản H1 KPMG soát xét làm rõ thay đổi và tính lại kỳ quý.

## Nguồn gốc PDF Q3/2025 signed
- PDF phát hành `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/PLX_Baocaotaichinh_Q3_2025_Hopnhat.pdf`, **31 trang**, **13,678,774 byte**, SHA256 **`012d34a3166e67ca61de8c7442bb7474479853b55f105b30c60347ee4e40453c`**, doanh nghiệp ký **29/10/2025**.
- Workflow nguồn **`44681702136`** PASS, artifact **`14604826033`** gồm PDF và các trang ảnh. Đã xem ảnh gốc ký: B01 pp2–4, B02 p5 (cột quý III riêng và cột lũy kế 9M), B03 pp6–7 (9M YTD). PDF là scan, bảng không có text layer, dùng ảnh trực tiếp và bản ghi VND từng dòng, không suy đoán OCR.
- B01 30/09/2025: tài sản **91,574,911,377,304**, nợ **62,675,251,687,942**, vốn CSH **28,899,659,689,362**, cash và tương đương **12,616,557,939,958** VND.
- B02 **Quý III (Năm nay) in trên PDF**: doanh thu thuần **83,631,407,329,088**, lợi nhuận trước thuế **807,127,310,124**, LNST **705,970,238,434**, LNST thuộc cổ đông mẹ **610,701,186,200**, EPS **369** VND/cổ phiếu. B02 **9M YTD**: doanh thu thuần **228,031,417,791,322**, LNST **2,341,150,116,435**, EPS YTD 1330.
- B03 **9M** CFO **-1,156,503,980,511**, CFI **-6,956,810,447,853**, CFF **+5,767,818,280,823**, thuần **-2,345,496,147,541**, đầu năm **14,933,068,792,315**, FX **+28,985,295,184**, cuối **12,616,557,939,958** VND. Tổng dòng chi tiết CFO/CFI/CFF và cầu tiền trong PDF khớp 0 VND.
- `reports/source-audits/PLX-2025Q3-consolidated-original-vnd.txt` có **104 trường tiền gốc VND**, `scripts/verify_plx_q3_2025_reviewed_h1.py` kiểm 30 phương trình Q3 original VND = 0.

## QUAN TRỌNG: cùng phạm vi nhưng 2 phiên bản BCTC H1/2025 KHÁC số
- **Bản Q2 lần đầu**: source original PDF 29/07/2025, PR #92 Q2 43/43 accounting checks PASS **đúng theo báo cáo đó**, không làm sai số gốc. H1 (Q2) trước soát xét net revenue **144,915,406,061,940**, PAT **1,579,087,444,418**, B03 H1 CFO **-442,992,517,070**, CFI **-5,598,916,341,260**, CFF **+1,855,066,395,925**, cash end **10,765,084,811,049** VND. Đây là **vintage đầu**, không dùng trực tiếp cho Q3 9M sau khi đã có H1 soát xét.
- **MỚI H1 KPMG reviewed**: issuer PDF `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/PLX_Baocaotaichinh_6T_2025_Soatxet_Hopnhat.pdf`, **75 trang**, **16,596,635 bytes**, SHA256 **`c44c230d3eb53b832bb5393cce4cabe9d491980e1b016201823b0e9e4f733bb5`**, ký **29/08/2025**, KPMG reviewed. Source recovery run **`44682724580`** PASS, artifact **`14605067414`**. Đã xem ảnh PDF B02 pp10–11 và B03 pp12–14. `reports/source-audits/PLX-2025H1-reviewed-consolidated-original-vnd.txt`: **59 trường nguồn VND**, 15/15 phương trình H1 B02/B03 = 0 VND.
- H1 reviewed B02 net revenue **144,400,010,462,234**, PAT **1,635,179,878,001**. So với H1 trước soát xét: doanh thu **-515,395,599,706**, PAT **+56,092,433,583 VND**. **H1 reviewed net revenue + Q3 printed revenue = Q3 9M source** và PAT cũng **trùng từng VND**. Như vậy lỗi tính 9M−H1 trước đó là lỗi **trộn phiên bản**, không phải phép trừ Q3 sai. Giữ nguyên bản Q2 cũ với nhãn version, dùng H1 reviewed cho kỳ Q3.
- Có **ngoại lệ hai dòng B02** thỏa `9M−reviewed H1−printed Q3 = -858,475,922 VND` cho **thu nhập khác** và **chi phí khác**; cả hai lệch cùng số nên lợi nhuận khác và PAT **không chênh**. Không sửa dòng gốc, chưa khẳng định nguyên nhân thuyết minh, ghi rõ flagged.
- H1 reviewed B03 nguồn: CFO **-356,677,420,537**, CFI **-5,522,148,321,581**, CFF **+1,708,818,695,994**, net **-4,170,007,046,124**, FX **+7,575,425,477**, đầu 2025 **14,933,068,792,315**, tiền 30/06 cuối **10,770,637,171,668**. Chênh cuối kỳ với H1 Q2 ban đầu **+5,552,360,619 VND**.
- B03 **quý III riêng theo bản cùng vintage** = 9M original signed − H1 reviewed signed:
  - CFO **-799,826,559,974**;
  - CFI **-1,434,662,126,272**;
  - CFF **+4,058,999,584,829**;
  - thuần **+1,824,510,898,583**;
  - FX **+21,409,869,707**;
  - đầu quý **10,770,637,171,668**;
  - cuối quý **12,616,557,939,958** VND;
  - capex **-209,747,902,082 VND**.
- **9/9 phương trình riêng quý III bằng 0 VND**, gồm tổng CFO/CFI/CFF và cash bridge. `cashflow_period_basis=quarter`; `cashflow_ytd_period_basis=nine_months`.
- **QUARANTINE dòng cổ tức riêng quý III**: B03 9M khoản "tiền chi trả cổ tức" `-1,577,888,831,500` trừ bản H1 reviewed `-1,620,879,828,573` = **+42,990,997,073 VND**, *dấu dương bất thường với dòng tiền trả cổ tức*. Ghi `dividends_paid_ytd` nguồn đầy đủ nhưng `dividends_paid` Q3 riêng **không công bố (null/absent)** đến khi xác minh thuyết minh/đính chính. Không biến dương thành dòng chi âm tự đoán.

## Scope, schema và kiểm thử
- Chỉ `data/financials-PLX.json` bản `2025-Q3`: 104 trường original VND + 7 quý riêng (CFO/CFI/CFF/net/FX/capex/cash_beginning) = **111 numerical monetary fields**, EPS Q3 369, YTD 1330, nguyên ảnh nguồn.
- `scripts/verify_plx_q3_2025_reviewed_h1.py` chạy 30 nguồn Q3 exact-VND + 15 nguồn H1 reviewed exact-VND + 9 kỳ Q3 exact-VND, tái chứng minh 22 dòng B02 9M−reviewed H1−quý III có đúng 2 ngoại lệ, chênh khác so bản Q2 cũ, khóa dòng dividends_paid Q3 và PLX parent Q3/2026 BLOCKED.
- `.github/workflows/validate.yml` thêm test; chỉ merge sau CI PASS và xác minh postmerge production 45/45 URLs SHA256. No UI change; không load dữ liệu các kỳ đã PASS khác.

## Điểm tiếp theo
1. Sau khi main + site PASS, Library `/Projects/so-lieu` lưu checkpoint cùng PDF original Q3 và reviewed H1, và không reprocess quý Q1/Q2 đã ký PASS.
2. Tiếp tục **PLX 2025-Q4 hợp nhất**, source gốc FY 12M, derive Q4 standalone B03 FY−Q3 9M đã verified, so B02 quý riêng vs bản năm FY audited 2025 (có thể thay đổi vintage). Đặc biệt nếu nguồn năm kiểm toán thay đổi, không trộn khi trừ dòng tiền, giữ exception.
3. PLX 2026-Q1/Q2 mới làm sau PLX Q4; Q3/2026 hợp nhất PASS, Q3/2026 mẹ 87,654,015,000 VND CFF signed original error remains quarantine.
