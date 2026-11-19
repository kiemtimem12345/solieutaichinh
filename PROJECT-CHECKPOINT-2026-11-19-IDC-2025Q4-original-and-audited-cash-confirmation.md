# CHECKPOINT — IDC consolidated Q4/2025 source B01/B02 and FY B03; FY audit cash versus 2026 H1 opening — 19/11/2026

## Resume: no reprocessing already validated
- Previous main commit `29074bf923976ce91abc57f8ad7d5a5f60a49bea`, PR #78; IDC Q1/2026 B01/B02/B03 **22** exact-VND checks, IDC Q2/2026 H1 **29** checks, IDC Q3/2026 B01/B02/9M B03 **29** checks and standalone Q3 cash sourced 9M less H1. All previously verified records remain intact.
- VDS consolidated 7/7 2025Q1–2026Q3 source verified; GEG consolidated 7/7. No duplicated VDS Q1/Q2 work — PR #66 already merged, website 45/45 PASS.
- Primary outstanding IDC 2026Q2 cash source-vintage mismatch **890,796,892 VND**; investigate Q4/2025 independently rather than guessing Q2 cash.

## Sources recovered and directly checked
1. Issuer official **consolidated Q4/2025** original PDF, signed **26 Jan 2026**: https://admin.idico.com.vn/uploads/VIE_BCTC_HOP_NHAT_Q4_2025_170f9f2fa3.pdf
   - 67 pages, 17,108,337 bytes, SHA-256 `1ca45cd909f038d6b5a54123280b2e92b9d7dab92c52ba3c85fac5f9b0483d5f`.
   - B01 pages **8–11**, B02 page **12** (Quý 4 / Năm nay, distinct from full-year columns), B03 FY 2025 pages **13–14**; inspected original rendered PNG images.
2. Independent **FY2025 audited consolidated financial statements** within IDICO official 2025 annual report, audited **27 Mar 2026**: https://admin.idico.com.vn/uploads/VI_Annual_Report_2025_942f6f68b7.pdf
   - 138 PDF pages, 11,994,136 bytes, SHA-256 `8eae4129eef2e3ae88b4f9ff1559a6d4cb3fd03a7a893e9030439eac9055e25b`. Audited B01, B03 and note 5 both confirm 31 Dec 2025 closing cash **553,052,678,239 VND** (official searchable text); does **not** include the alternative H1 opening cash.
3. Source recovery GitHub Actions `44548468214` both jobs PASS, short-lived original page artifacts Q4 ID `14541019188` and FY audited ID `14540714622`. Original source hashes recorded in `data/financials-IDC.json`. The issuer pages were reviewed on 19/11/2026.
4. Q1/2026 source is original consolidated signed 28 Apr 2026; FY original 2025 consolidated sources above are same scope (not parent report).

## Verified 2025-Q4 issuer source (VND)
| Metric | Source |
|---|---:|
| B01 total assets at 31 Dec | 23,201,490,679,523 |
| B01 total liabilities | 14,938,459,787,767 |
| B01 equity | 8,263,030,891,756 |
| B01 cash/equivalents | **553,052,678,239** |
| B02 stand-alone Q4 net revenue | 2,160,138,111,718 |
| B02 stand-alone Q4 pretax | 659,219,588,033 |
| B02 stand-alone Q4 net | 539,995,121,238 |
| B02 stand-alone Q4 parent net | 449,103,567,116 |
| B02 Q4 EPS | 1,183 VND/share |
| FY2025 B03 CFO | **+3,913,940,809,873** |
| FY2025 B03 CFI | **-7,009,893,958,684** |
| FY2025 B03 CFF | **+1,460,905,190,082** |
| FY2025 B03 net cash | **-1,635,047,958,729** |
| FY2025 B03 beginning cash | 2,188,037,806,317 |
| FY2025 B03 FX | +62,830,651 |
| FY2025 B03 ending cash | **553,052,678,239** |

- **101 issuer visual-verified fields** (source VND converted to `triệu VND`, except EPS). **29 original B01/B02/FY B03 source accounting identities, residual zero VND**; original images cover all three signed statements. ROA/ROE reset to null pending proper denominator.
- Prior auto `IDC 2025-Q4 operating_cash_flow_ytd=836,453,742 triệu VND` and `financing_cash_flow_ytd=371,657,217 triệu VND` **not supported by source**, replaced with original above. Original auto values archived with reason under `financial_line_items_prior_values` / `financial_line_items_rejected_values`.
- B02 PDF line explicitly **prints Q4 interest expense 43,891,490,863 VND**, exceeding total financial expense of 42,472,227,098 VND (possible net offsets); this is source fact confirmed visually, not a reason to silently null/OCR-correct the line. No unsupported decomposition of total financial expense.
- **Q4 standalone B03 not derived**: 12M original cash figures cannot become Q4 alone before independently verified 2025-Q3 original 9M. Keep `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow`, etc. **null**; preserve 12M values in `*_ytd` fields and `cashflow_period_basis=year_to_date`.

## Audited cash resolves *which historical comparative is supported*, not Q2 bridge
| Original source version | 31 Dec 2025 / beginning 2026 cash (VND) |
|---|---:|
| IDC signed Q4/2025 B01/B03 | **553,052,678,239** |
| IDC FY2025 **audited** B01/B03 and note 5 | **553,052,678,239** |
| IDC original Q1/2026 B01 comparative + B03 opening | **553,052,678,239** |
| IDC original H1/2026 B01 comparative + B03 opening | **553,943,475,131** |
| H1 original minus both FY sources | **+890,796,892** |

- Independent FY audited and pre-audit Q4 issuer converge exactly on **553,052,678,239 VND**, as does Q1 original. The H1 original number is the only deviant source vintage; **do not call it incorrect until an issuer correction, accounting reclassification or restatement note is traced**.
- Main B01 FY2025 total assets 23,201,490,679,523 VND also matches H1 2026 B01 2025 comparative *total*; difference may be a reclassification among items inside assets but exact item/issuer note **not yet identified**.
- Difference 890,796,892 / 553,052,678,239 = approx 0.161%, above tolerance 0.01%. Consequently, 2026-Q2 standalone cashflow derived from H1 less Q1 remains blocked: implied start+section changes+FX misses Q2 close by **-890,796,892 VND**. Do not move provisional figures into canonical quarter fields.
- `source_validation.audited_year_end_comparative` in IDC 2025Q4 and linked cross-vintage metadata in IDC 2026Q1/Q2 hold source URLs, hashes and exact deltas, **no fabricated Q2 adjustment**.

## Code and next workflow
- `data/financials-IDC.json`: 2025-Q4 core + FY cash verified and corrected, 2026Q1/Q2 only append linked audited comparative metadata; Q3 and 2025Q1–Q3 untouched.
- `scripts/inspect_idc_fy2025_original_pdf.py` and `.github/workflows/inspect-idc-fy2025-original.yml`: read-only parallel original PDF source checks + image artifacts.
- `scripts/verify_idc_q4_2025_original.py`: verify 101 fields / 29 exact-VND source identities, signed and audited SHA, audit/Q1/H1 890,796,892 VND comparison, archival of erroneous auto values and intentionally null Q4 standalone cash.
- `.github/workflows/validate.yml` CI gate; merge only on PASS, production website SHA 45/45 after merge, save commit and run IDs here.

### Exact next checkpoint after Q4 accepted
1. IDC **2025-Q3** issuer consolidated original B01/B02/9M B03 and source identity checks; compute Q4 stand-alone CFO/CFI/CFF = 12M-9M **only with same source scope and cash bridge exact**.
2. Then IDC 2025Q2 H1 and Q1 original; derive Q3/Q2 stand-alone only from verified cumulative predecessors.
3. Investigate 2026 H1 historical cash comparative 890,796,892 VND via specific notes and comparative financial position classifications. If no clear source evidence keep exception; do not block unrelated periods indefinitely.
4. Other open source exceptions: GEG 11,422,218,903 VND 2025 cash-vintage, GAS H1 10,160,150,278 VND COGS source-vintage, PLX Q3 company-parent B03 87,654,015,000 VND. Maintain separate scope and artifacts.
5. Original values VND→million VND JSON except EPS; periods Q1/2025 onward; max 20; <=0.01% tolerance; avoid SFTP modifications to Git-tracked Hostinger checkout.
