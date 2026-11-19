# CHECKPOINT — IDC Q1/2025 nguồn ký và hoàn tất dòng tiền riêng Q2/2025 — 19/11/2026

## Source original Q1 2025
- HNX original mirrored at https://static2.vietstock.vn/data/HNX/2025/BCTC/VN/QUY%201/IDC_Baocaotaichinh_Q1_2025_Hopnhat.pdf
- Consolidated issuer-signed PDF **62 pages, 15,532,917 bytes**, SHA256 `5b3809b3492cb8ac96900d41e9410bbec4155500dd1ecc315485f044e0cbc322`, signed 28/04/2025.
- Github Actions original-page download and render run `44565988985`, artifact `14549884840`. Visually checked original image pages 8–11 B01, page 12 B02 rotated to upright, pages 13–14 B03.
- `data/financials-IDC.json` Q1: **98 signed original numeric fields**, **24 independent exact-VND accounting identities residual 0**. Replaced unverified rounded OCR. No unsupported ROA/ROE.
- B01 Q1 assets **19,410,468,097,703**, liabilities **12,280,835,294,709**, equity **7,129,632,802,994 VND**. Source B02 Q1 revenue **1,793,484,296,130**, PBT **520,708,647,205**, PAT **416,984,544,604 VND**, EPS **1,040 VND/share**.
- B03 Q1 CFO **+593,194,330,719**, CFI **-745,138,695,014**, CFF **+256,704,039,546**, net **+104,759,675,251**, FX **+2,753,952**, cash opening **2,188,037,806,317**, cash ending **2,292,800,235,520 VND**. All signed-source checks 0 VND.
- A **60,000 VND** transcription discrepancy in Q1 B01 short-term receivables was caught by accounting check and corrected to source-printed **1,530,965,913,962 VND** (not 1,530,965,973,962); identity 0.

## IDC Q2/2025 standalone cash flow, signed H1 minus signed Q1
- Q2/2025 H1 original 6M signed 29/07/2025 (63-page PDF, hash `04ced780ca282517bc28399e59d1a08dda0338cdda6a523403139a821674003f`) had already PASS: 100 fields, 30 exact-VND identities.
- Standalone **Q2**, same *consolidated* scope, source-basis signed interim 6M minus signed 3M, amounts VND:
  - CFO **+809,015,066,804**
  - CFI **-1,693,078,122,700**
  - CFF **-545,521,959,637**
  - Net cash change **-1,429,585,015,533**
  - FX **+38,713,120**
  - Cash at Q2 beginning **2,292,800,235,520**, ending **863,253,933,107**
  - Capex **-746,582,157,511** and dividends paid **-568,281,373,470**
- **6 exact-VND Q2 standalone cash checks 0**, including 6M-3M reconciliation, CFO+CFI+CFF net, and beginning + net + FX = ending.
- Source comparison: original Q2/2025 B03 cash components differ in classification from reviewed EY H1/2025 28/08, e.g. code05 by 47,357,863,919 VND, but CFO/CFI/CFF totals unchanged. Keep original interim and EY-reviewed H1 provenance separately.

## Repo and checkpoints
- PR #82 and #83 merged to main; PR #84 https://github.com/kiemtimem12345/solieutaichinh/pull/84 carries original Q1 and completed Q2 standalone, dedicated source recovery and regression.
- `scripts/verify_idc_q1_2025_original.py` source-exact 98 fields and 24 checks; `scripts/verify_idc_q2_2025_original.py` 100 fields and 30 identities plus 6 cash checks; `scripts/verify_idc_q3_2025_original.py` remains regression for prior verified Q3 and Q4.
- Merge only when financial-snapshot validation and original-page recovery workflows PASS. No website layout change; verify production smoke separately. Git main not modified until PR merge.
- After merge IDC **all seven consolidated 2025-Q1 through 2026-Q3 periods** now have signed-original source validation for B01/B02/B03, with **2026-Q2 cash opening vintage exception of +890,796,892 VND** preserved; Q3/2026 and Q3/2025 completed states preserved.
- Next action: verify deployment website JSON endpoints and resume other outstanding symbols/scope according to latest global audit (PLX parent Q3 printed CFF mismatch remains quarantined; etc.). All periods 2025-Q1+, max 20 per symbol, no unsupported 0 or source mixing, tolerance <=0.01%.
