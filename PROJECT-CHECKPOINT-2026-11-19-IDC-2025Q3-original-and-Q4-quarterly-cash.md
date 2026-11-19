# CHECKPOINT — IDC hợp nhất Q3/2025 signed HNX original; riêng Q4/2025 từ FY 12M − 9M — 19/11/2026

## Điểm tiếp tục — không làm lại số đã đạt
- Main sau PR #79, commit `c5a27a4a8298549ead5d897536403552d98fdf94`, đã xác minh IDC hợp nhất Q4/2025 B01/B02 và FY 12M B03 (101 fields, 29 exact-VND checks); dữ liệu kiểm toán FY2025, Q1/2026 đồng thuận cuối năm 2025 tiền **553,052,678,239 VND**. H1/2026 dùng 553,943,475,131 VND, chênh **+890,796,892 VND** chưa tìm thấy chứng cứ phân loại lại, Q2/2026 cashflow riêng tiếp tục blocked. IDC 2026Q1/Q2/Q3 và GAS/VDS/GEG đã xác minh giữ nguyên.
- CI production sau PR79 run `44550194480` PASS; website run `44550194303` **45/45 URLs SHA256 PASS**; no website UI or direct SFTP edits.

## Nguồn IDC hợp nhất Q3/2025 đã phục hồi đúng PDF có chữ ký
- Đường PDF máy chủ IDICO `https://admin.idico.com.vn/uploads/VIE_BCTC_HOP_NHAT_Q3_2025_506ed62acb.pdf` hiện **404**, đã xử lý bằng **ZIP công bố HNX** lưu tại Vietstock (không sử dụng nhầm báo cáo riêng lẻ):
  https://static2.vietstock.vn/data/HNX/2025/BCTC/VN/QUY%203/IDC_Baocaotaichinh_Q3_2025_Hopnhat.zip
- ZIP size 28,276,931 bytes SHA256 `04ff7104fec1b3fd47c3567570c862072bc1bebde48968e4249b06e0b5650394`, chứa bản báo cáo hợp nhất gốc tiếng Việt ký ngày **29/10/2025** `3_idc_2025_10_30_d9319de_vi_baocaotaichinhhn_q3_2025_s.pdf`, 16,173,434 bytes, SHA256 **`80c1b3dcb2e5469d4fb84c3a0cbd46c51f664ce7e07a2a0946e10b691ca92ce3`**, 64 PDF pages; bản tiếng Anh trong ZIP không dùng thay thế.
- GitHub Actions `44550845936` PASS, short-lived original visual artifact `14543736426`. Page images manually inspected **B01 PDF pages 8–11, B02 page 12, B03 pages 13–14**. Exact original unit **VND**.

## Chỉ tiêu gốc IDC hợp nhất Q3/2025
| Original verified | Source VND |
|---|---:|
| B01 tài sản ngày 30/09/2025 | 21,293,030,253,931 |
| B01 nợ phải trả | 12,926,247,964,300 |
| B01 vốn chủ sở hữu | 8,366,782,289,631 |
| B01 tiền và tương đương tiền | 791,686,559,919 |
| B02 **riêng Q3** doanh thu thuần | 2,871,329,472,687 |
| B02 riêng Q3 LNTT | 1,218,492,728,027 |
| B02 riêng Q3 LNST | 981,137,501,988 |
| B02 riêng Q3 LNST cổ đông mẹ | 841,835,881,584 |
| B02 EPS Q3 | 2,218 VND/cổ phiếu |
| B02 **lũy kế 9 tháng** doanh thu | 6,428,011,659,828 |
| B02 9M LNTT | 2,258,525,812,470 |
| B02 9M LNST | 1,814,085,953,812 |
| B03 **lũy kế 9 tháng** CFO | +2,943,740,801,880 |
| B03 CFI 9M | -4,680,519,162,668 |
| B03 CFF 9M | +340,361,746,335 |
| B03 biến động tiền thuần 9M | -1,396,416,614,453 |
| B03 đầu năm | 2,188,037,806,317 |
| B03 tỷ giá 9M | +65,368,055 |
| B03 cuối Q3 | 791,686,559,919 |

- **102 fields original** and **30 source exact-VND accounting identities residual zero** including both B02 period and cumulative columns, B01/B03 cash balance, CFO 9M components, CFI and CFF constituent sums.
- Legacy IDC Q3 rounded auto B01/B02 and missing original cash flow quarantined, source original signed PDF used for validation.
- **Q3 riêng CFO/CFI/CFF** still intentionally null: need issuer-confirmed IDC H1/2025 6M B03 same consolidated scope, do not compute from an unverified ZIP/PDF.

## IDC Q4/2025: riêng B03 = FY 12M − Q3 9M, both signed originals same scope
| Source | FY2025 12M VND | IDC Q3 9M VND | **Q4 riêng VND** |
|---|---:|---:|---:|
| CFO | +3,913,940,809,873 | +2,943,740,801,880 | **+970,200,007,993** |
| CFI | -7,009,893,958,684 | -4,680,519,162,668 | **-2,329,374,796,016** |
| CFF | +1,460,905,190,082 | +340,361,746,335 | **+1,120,543,443,747** |
| Tiền thuần | -1,635,047,958,729 | -1,396,416,614,453 | **-238,631,344,276** |
| FX | +62,830,651 | +65,368,055 | **-2,537,404** |
| Tiền cuối | 553,052,678,239 | 791,686,559,919 | 553,052,678,239 |
- 2025 Q4 beginning cash **791,686,559,919** and net change **−238,631,344,276**, FX **−2,537,404**, ending **553,052,678,239** VND; exact bridge 0 residual. Standalone Q4 capex **−1,300,428,928,495** and cash dividends **−654,131,953,577** VND.
- Also **9 Q4 B02 metrics** match FY reported YTD minus Q3 9M **exactly**: revenue, gross profit, COGS, operating, other, pretax, after-tax, parent and minority net. Added **5 independent exact-VND cash checks**.
- Q4 source FY source assets, earnings, 12M B03 remain unchanged; only newly authenticated standalone-quarter B03 fields are appended.

## Technical modifications
- `data/financials-IDC.json` 2025Q3 now full verified B01/B02/9M B03; 2025Q4 now standalone FY-minus-9M cash. 2025Q1/Q2 and 2026 records untouched; 2026Q2 source-vintage missing cash remains null.
- `scripts/inspect_idc_q3_2025_original.py` with `.github/workflows/inspect-idc-q3-2025-original.yml`: protects ZIP size/host and extracts only signed consolidated PDF after issuer URL returned 404.
- `scripts/verify_idc_q3_2025_original.py` validates 102 fields and 30 exact VND identities, source hashes, Q4 FY-minus-9M. `scripts/verify_idc_q4_2025_original.py` expanded to validate 8 standalone quarter cash fields and 9 Q4 B02 crosschecks. `.github/workflows/validate.yml` new CI gate.
- PR merge **only after CI PASS**, run website 45/45 URL/SHA verification, record production merge here.

## Next pending tasks
1. Same ticker IDC **2025-Q2 original consolidated H1** B01/B02 6M B03, then derive Q3 standalone 9M − H1 and independently verify its cash bridge.
2. Then IDC **2025-Q1 original 3M** B01/B02/B03 to derive Q2 standalone 6M − 3M. Mark ticker complete only once 7/7 consolidated periods source-validated with source-vintage conflicts explicitly tracked.
3. Independent 2026Q2 opening-cash +890,796,892 VND remains quarantined; other blockers GEG +11,422,218,903 cash, GAS H1 +10,160,150,278 COGS, PLX parent Q3 cash financing 87,654,015,000. Do not write fiction to canonical values.
4. Source VND → JSON million VND (EPS VND/share), periods Q1/2025 onward, max 20, tolerated difference <=0.01%, segregate original source versions, do not overwrite passing data or website UI.
