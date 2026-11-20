# CHECKPOINT — PLX consolidated Q2/2025 signed original + H1 cash minus signed Q1, 20/11/2026

## Safe resume state
- Production repo `kiemtimem12345/solieutaichinh`. Main before this task **`a684821cd42f736c47697dfc80e4b249c3a70086`** (PR #91 Q1/2025 completed, postmerge live 45/45 SHA run `44679928726` PASS).
- This PR processes **only PLX Q2/2025 consolidated**. PLX Q1/2025 source original 53p full B01/B02/B03 already PASS; PLX Q3/2026 consolidated and all GAS/VDS/GEG/IDC certified periods not touched. PLX 2026Q3 parent B03 CFF 87,654,015,000 VND issuer error quarantined.
- Existing Q2 only B02 page5 visually verified from user-supplied image; B01 subtotal/current assets, retained earnings and H1 B03 source OCR were incomplete or improperly rounded. This checkpoint replaces them from original.

## New signed original source evidence
- `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/PLX_Baocaotaichinh_Q2_2025_Hopnhat.pdf` — issuer signed **29 July 2025** (Petrolimex), **31 PDF pages, 13,678,870 bytes**, SHA256 `90195e13c974fbadf90004ec9817b9e356c2b9203c2308a8a40c313110b29ec3`.
- Source recovery script `scripts/recover_plx_q2_2025_consolidated_original.py`, GitHub Actions `44680177934` PASS, source artifact `14602749723` holds whole original and images. Scanned PDF has **no selectable text on statement pages**; copied by manual source image reading, not trusting old OCR.
- B01 original **PDF pp2–4**; B02 original **p5** has columns Q2 current year and H1 6M YTD, which must never be confused; B03 original **pp6–7** is six-month YTD cumulative. All these signed source images have been inspected visually with legible VND and CEO signature.

## Exact consolidated source VND
- B01 30 Jun 2025: assets **87,410,971,055,479**, liabilities **59,232,773,172,200**, equity **28,178,197,883,279**; current assets 66,274,987,488,379; noncurrent assets 21,135,983,567,100; cash and equivalents **10,765,084,811,049**; retained earnings 2,796,932,634,102.
- B02 **standalone Q2**: net sales **77,054,375,574,284**, COGS **71,919,641,393,348**, gross profit **5,134,734,180,936**, pretax profit **1,637,975,909,016**, income tax total 269,657,265,137 (current 323,685,620,958, deferred -54,028,355,821), PAT **1,368,318,643,879**, parent-attributable 1,283,730,540,279, EPS **899** VND/share.
- B02 **H1 six-month cumulative**: net revenue **144,915,406,061,940**, PAT **1,579,087,444,418**, EPS 926 VND/share. Signed Q1 PAT 210,768,800,539 + signed Q2 PAT 1,368,318,643,879 = H1 source to exact VND.
- B03 **H1 six-month YTD**: CFO **-442,992,517,070**, CFI **-5,598,916,341,260**, CFF **+1,855,066,395,925**, net **-4,186,842,462,405**, FX +18,858,481,139, year-opening 14,933,068,792,315, ending **10,765,084,811,049**. YTD source CFO/CFI/CFF detail rows sum to printed subtotal exactly and B03 ending equals B01 cash.
- **Q2 standalone = source H1 6M minus signed source Q1 3M, same scope, source VND**:
  - CFO **+2,106,791,853,375**
  - CFI **-1,021,432,844,145**
  - CFF **-792,003,743,906**
  - net cash **+293,355,265,324**
  - FX **+24,995,968,933**
  - beginning **10,446,733,576,792**
  - ending **10,765,084,811,049**
  - capex **-358,908,217,763**, dividends paid **-1,514,365,622,917** VND.
- Cash bridge Q2: 10,446,733,576,792 +293,355,265,324 +24,995,968,933 =10,765,084,811,049 VND (**0 VND residual**).
- `reports/source-audits/PLX-2025Q2-consolidated-original-vnd.txt`: **104 manually transcribed original VND source fields**, no original PDF body copied. Derived **8 Q2 monetary fields** (plus closing equal existing original) -> `data/financials-PLX.json` Q2 has **112 exact fields**, EPS recorded in VND/cp.
- **43 independently validated exact-VND accounting/source equations, 0 VND differences**, including B01 subtotals, B02 quarter and H1, B03 signed H1 CFO/CFI/CFF component sums, H1 cash, Q1→Q2 income bridges and standalone quarter cash bridge. Tested locally against originals and enforced by `scripts/verify_plx_q2_2025_original.py` in `.github/workflows/validate.yml`.
- ROA **6.54%**, ROE **18.97%** checked again from source-exact Q1/Q2 B01 opening/closing and standalone Q2 PAT; values remain unchanged. Other periods untouched.

## Following actions
1. CI financial validation must PASS; merge PR with source SHA and checkpoint; require live website **45/45 HTTPS/SHA256** PASS after merge; save Library checkpoint and source PDF.
2. Next **PLX 2025-Q3 consolidated** (currently partially verified from archived OCR). Its signed source B03 9M minus **verified H1 2025 source (this checkpoint)** determines standalone Q3 CFO/CFI/CFF. Do not reprocess already PASS Q1 or Q2. Check source interim comparative vintages and debit/credit signs.
3. PLX 2025Q4 and 2026Q1/Q2 remain visual pending, handle one period at a time; parent PLX 2026Q3 genuine original CFF 87,654,015,000 VND source discrepancy remains blocked until official issuer correction.
