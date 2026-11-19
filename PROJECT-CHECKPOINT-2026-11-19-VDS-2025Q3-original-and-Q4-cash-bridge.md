# CHECKPOINT — VDS consolidated 2025 Q3 issuer original and Q4 standalone cash bridge, 19/11/2026

## Exact starting point
- Main commit before this change `637d7ac2b2073e881426d0e80dd82eedc3db795a`, PR #64 VDS 2025Q4 visually inspected consolidated B01/B02/12M B03; pre/main CI PASS; website smoke 45/45 PASS; previous checkpoint `PROJECT-CHECKPOINT-2026-11-19-VDS-2025Q4-original-B01B02B03.md`.
- VDS 2026Q1/Q2/Q3 consolidated rows PASS; do not rerun previously validated quarters. VDS 2025Q1/Q2 remain unverified.
- Latest task: 2025Q3 original VDS Cty Chứng khoán Rồng Việt, PDF from issuer, not legacy Vietstock parser. Same company and consolidated scope as Q4.

## Original source and visual verification
- Issuer announcement (28/10/2025): https://www.vdsc.com.vn/quan-he-co-dong/cong-bo-thong-tin/rong-viet-cong-bo-bao-cao-tai-chinh-hop-nhat-quy-3-2025-va-giai-trinh-chenh-lech-loi-nhuan-i963
- Signed original PDF 24/10/2025: https://www.vdsc.com.vn/data/api/app/file-storage/8656c204-2255-4ed2-0bbf-08de15b97c34/VDSC_Cong%20bo%20BCTC%20HN%20Quy%203%20nam%202025%20va%20giai%20trinh%20chenh%20lech%20loi%20nhuan.pdf?downloadFrom=ManagementDocument-963
- SHA256 `93580147a2c34adb8118a83ed3d9348360355b0660bdd5a47871c60f2403dc3b`; 10,076,199 bytes, 50 scanned pages. GitHub Actions read-only inspector run `44510814492` PASS, image artifact `14523530888` used for primary visual verification. Pages 6–8 B01, 11–13 B02, 14–17 B03 and separate client-brokerage cash. **OCR is not sole evidence.**
- Source VND, JSON normalized `triệu VND`; EPS in VND/share.

## Correct VDS consolidated Q3/2025 issuer figures
- B01 at 30/09/2025: assets **7,732,966,527,561**, liabilities **4,578,708,861,227**, equity **3,154,257,666,334**, corporate cash **588,252,269,795** VND.
- B02 **standalone Quý III/Năm nay**: CTCK operating revenue **469,935,413,540**, operating expenses **106,328,748,769**, PBT **325,846,951,359**, corporate income tax **61,589,855,072**, consolidated net **264,257,096,287**, parent net **261,233,437,741**, NCI **3,023,658,546** VND; EPS **960 VND/share**.
- B02 9M cumulative: operating revenue 819,858,909,744; PBT 331,048,115,091; net 272,075,532,876; parent net 269,304,589,718 VND. These are source 9M columns, not standalone Q3.
- B03 **9M cumulative**: CFO **-790,384,880,004**, CFI **-864,912,269,435**, CFF **+1,036,412,000,000**, net **-618,885,149,439**, beginning **1,207,137,419,234**, ending **588,252,269,795** VND.
- Client brokerage cash outside corporate B01: 2,589,483,189,435 VND, separate from issuer corporate cash.
- Legacy parser errors quarantined: previously `operating_cash_flow_ytd=+331048 triệu` was actually 9M pretax profit, `foreign_exchange_effect_ytd=588252 triệu` was ending corporate cash; FVTPL 259.287bn was read as total operating revenue, but actual standalone Q3 CTCK revenue 469.935bn. Original legacy values retained in `financial_line_items_prior_values` and `financial_line_items_rejected_values`.
- 117 new/reverified fields; **30 source exact-VND B01/B02/B03 accounting checks residual zero**. Q3 standalone cashflow still null until independent 2025Q2 H1 source validated.

## Q4 standalone cash now provable from verified 12M-9M same scope
| B03 (VND) | Source 2025 FY 12M | Source 2025 Q3 9M | Q4 standalone |
|---|---:|---:|---:|
| CFO | -850,325,354,079 | -790,384,880,004 | **-59,940,474,075** |
| CFI | -824,472,465,903 | -864,912,269,435 | **+40,439,803,532** |
| CFF | +1,464,636,000,000 | +1,036,412,000,000 | **+428,224,000,000** |
| Net change | -210,161,819,982 | -618,885,149,439 | **+408,723,329,457** |
| Corporate cash end | 996,975,599,252 | 588,252,269,795 | 996,975,599,252 |

- FY-minus-9M also exactly reproduces original Q4 quarterly B02 revenue 221,975,460,374, pretax 15,744,157,121, net 10,092,207,009, parent 13,821,476,572 and NCI -3,729,269,563 VND (7 independent quarterly B02 comparisons = zero).
- Q4 begins at Q3 ending 588,252,269,795, and +408,723,329,457 net ends FY 996,975,599,252. 3 Q4 quarterly cash checks residual zero, capex Q4 -3,650,969,550 VND. No assumptions or invented cash flows.

## Changed files and QA gate
- `data/financials-VDS.json`: only records 2025-Q3 and Q4 updated. 2025-Q3 sourced exact, 2025-Q4 now has valid source-derived standalone CFO/CFI/CFF/net/capex/cash opening, with original 12M values unchanged.
- `scripts/inspect_vds_q3_2025_pdf.py`, `.github/workflows/inspect-vds-q3-2025-pdf.yml`: read-only original issuer PDF download (size and redirect guarded) with 3-day PNG images.
- `scripts/verify_vds_q3_2025_source.py`: 30 original source exact-VND identities + original file SHA + 12M-minus-9M and Q4 B02 cross-report proofs.
- `scripts/verify_vds_q4_2025_source.py` now checks 118 verified Q4 fields, exact Q4 standalone cash instead of pending-null.
- `.github/workflows/validate.yml` runs expanded gate on every snapshot push. Merge only if CI PASS, check site SHA 45/45.
- Do not mark VDS ticker complete: 2025-Q1 and Q2 still legacy auto extraction. Next original review VDS consolidated **2025-Q2 → 2025-Q1**, derive Q3 quarterly B03 from 9M-6M, then Q2 quarterly 6M-3M.

## Business rules
- All quarters starting Q1/2025 only; at most 20 periods/ticker; numeric tolerance <=0.01%; preserve VND-to-million-VND provenance and sign. Check issuer originals and keep off-balance client funds separate from corporate cash.
- GAS H1 2026 COGS +10,160,150,278 VND allocation pending, PLX Q3/2026 parent CFF +87,654,015,000 VND discrepancy pending; don't fabricate fixes.
- GitHub `main` is production source; no SFTP edits, 45/45 website smoke on each accepted change. Keep finished periods immutable unless source contradiction is proved.
