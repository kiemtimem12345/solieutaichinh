# CHECKPOINT — PLX Q2/2026 consolidated signed original 36p with KPMG-reviewed H1 source vintage isolated

Date 20 Nov 2026. Production repo `kiemtimem12345/solieutaichinh`; main base `70f6fe029cbb266f40c84751f1c2c833cb2ab966` after PR #96 PLX Q1/2026 source original with 34 VND arithmetic identities and 3 caveats. Production 45/45 SHA256 PASS run `44710519484`. Do not reprocess prior PLX Q1 2026 or Q1–Q3 2025 PASS, Q4 2025 source audited-vintage conflict, GAS/VDS/GEG/IDC PASS. PLX Q3 2026 consolidated PASS, parent B03 issuer CFF 87,654,015,000 VND remains BLOCKED.

## Original Q2 issuer vs reviewed H1
1. **Original PLX Q2/2026 consolidated signed 30 July 2026** 36 PDF pages, **15,936,693 bytes**, SHA256 `925339daf7038fe2adf0ac3ac8277246992ebd00011d90cd1a1b82c079940cc6`. Original source `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/PLX_Baocaotaichinh_Q2_2026_Hopnhat.pdf`. Recovery GitHub Actions `44710991488`, artifact `14617376536`. Manually viewed B01 pp2–4 B02 p5 (quarter + H1 columns) B03 pp6–7 (six months). Scanned PDF, all currency VND. Source exact ledger `reports/source-audits/PLX-2026Q2-consolidated-signed-original-vnd.txt` contains **104 signed original financial fields** and 37 B01 source details.
2. **KPMG-reviewed H1/2026 signed 28 Aug 2026** 83 pages, SHA256 `e26c0d58e991895d3704c6b2417953b2fd962255af5197a33e24ed944bf3ccd6`, previously recovered with issuer Q3 project workflow; NOT new re-extraction. Full previous reviewed original is locally available in `/mnt/data/PLX-2026-Q3-H1-issuer-original-visual-pages.zip`. B02 reviewed PDF p10, B03 pp12–13 visually checked. Another accounting source vintage: use separately for Q3 standalone 9M-minus-reviewed H1, **do not overwrite Q2 as-filed**.
3. PLX original Q1 signed 29 Apr 2026 PDF 36p SHA `158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f9` is full source Q1, already PR #96; Q1 and Q2 original 6M B03 both use 01 Jan 2026 opening cash `7,588,239,730,231` VND and Q1 original ending `10,034,406,335,760`, enabling same source-vintage quarterly cash calculations. Q1 notes explicit reclassification opening vs FY2025 audited remain pending from #96.

## Financial original B01, B02, B03 and standalone Q2, VND
- B01 30/06/2026: total assets **87,876,314,405,848**; liabilities **58,722,729,974,402**; equity **29,153,584,431,446**; original B01 cash+equiv **6,323,957,202,057**. All 41 source B01/B02/B03 ledger arithmetic identities **0 VND** (unlike the two signed-source subgroup exceptions in Q1).
- B02 Q2 **standalone quarter**: net revenue **136,218,133,725,344**, gross profit **7,691,714,817,215**, pretax **3,364,152,276,032**, net profit **3,044,722,624,008**, attributable parent **2,808,812,523,261**, basic EPS **2,329 VND/share**. Six-month reported as-filed PAT **2,382,245,498,101**; Q1 PAT -662,477,125,907 + Q2 PAT 3,044,722,624,008 = 6M source PAT exact.
- B03 Q2 original **six-month YTD**: CFO **+1,224,204,547,047**, CFI **+5,536,623,100,159**, CFF **-8,019,953,358,007**, net **-1,259,125,710,801**, FX **-5,156,817,373**, opening **7,588,239,730,231**, closing **6,323,957,202,057** VND. All original 6M CFO/CFI/CFF detail sums, net and cash bridge PASS 0 VND.
- **Q2 standalone cash** = original Q2 signed 6M minus original signed Q1 3M, same beginning cash/vintage:
  - CFO **-8,151,521,210,218 VND**
  - CFI **+4,771,932,657,800 VND**
  - CFF **-330,860,581,285 VND**
  - Net **-3,710,449,133,703 VND**
  - FX **0 VND**
  - Capex **-591,073,777,428 VND**
  - Dividends paid **-112,351,369 VND**
  - Beginning **10,034,406,335,760 VND**
  - Closing **6,323,957,202,057 VND**.
  - Nine independent quarterly source/cash-flow identities 0 VND.
- ROA annualized **12.56%**, ROE **41.97%**, calculated source original Q1/Q2 B01 balances and Q2 standalone PAT, no OCR approximations.
- Database `data/financials-PLX.json` Q2 now stores 104 raw fields plus eight Q2 derived cash amounts in million VND exact, sourced to original signed PDF and values to one VND. Q1 prior, Q3 consolidated and parent not modified.

## Reviewed H1 2026 differences vs original Q2 as-filed (reviewed MINUS original in VND)
| Item | Signed KPMG reviewed − Q2 original |
|---|---:|
| H1 net revenue | **-171,838,220,315** |
| H1 PAT | **+7,523,810,667** |
| H1 pretax | **+30,021,263,981** |
| H1 CFO | **-279,661,291,608** |
| H1 CFI | **+442,210,624,980** |
| H1 CFF | **-157,699,639,254** |
| Net cash change | **+4,849,694,118** |
| H1 FX | **+13,981,777,234** |
| H1 beginning cash | **+3,192,126,575** |
| H1 ending cash | **+22,023,597,927** |

Reviewed H1 B03 signed: CFO +944,543,255,439; CFI +5,978,833,725,139; CFF -8,177,652,997,261; net -1,254,276,016,683; opening 7,591,431,856,806, FX +8,824,959,861; closing 6,345,980,799,984 VND. Its B03 net and cash bridge also self-balance to VND. It is not an issuer correction to quarterly Q2 standalone under as-filed vintage, but distinct reviewed H1 source. Source `source_validation.KPMG_reviewed_H1_minus_original_6M_source_vintage_vnd` keeps every difference, not allocate differences to Q2/Q3 by assumption.

## Validation, deployment and resume
- `scripts/verify_plx_q2_2026_original.py` independently validates signed source 104 VND fields, **41 source accounting identities** all 0, nine original Q2 derived standalone cashflow checks, independently signed reviewed H1 cash bridge, +22,023,597,927 difference and previous issuer CFF problem unaffected.
- CI `.github/workflows/validate.yml` includes this regression. Require CI PASS before PR merge; then production **45/45 SHA256** read-only smoke plus deployment, save checkpoint / issuer original PDF to Library.
- **Next**: review remaining PLX discrepancies (Q1/2026 printed B01 short receivables +9,083,970,186 VND, current liabilities +9,088,965,442 VND; prior audited annual starting cash reclassification -3,087,558,817,574 VND) with notes and official HOSE/issuer explanations without redoing PASS data. PLX Q3/2026 consolidated already PASS; *do not reprocess*. PLX Q3/2026 parent B03 CFF discrepancy remains blocked pending official errata.
