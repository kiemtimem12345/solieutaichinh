# CHECKPOINT — GAS Q1/Q2 2025 source originals visual checked, 20/11/2026

## Entry point
- Production repo `kiemtimem12345/solieutaichinh`, main base `1cb195e910f74aa40c78bbdb03f77a16daf6542c` (PLX consolidated Q3/2026 completed; 45/45 HTTPS/SHA run `44668217349` PASS). Keep previous PASS periods untouched.
- Prior GAS Q1/Q2 data only PDF-text and VND arithmetic PASS but screenshot cache miss, state `visual_pending`; this checkpoint **performs visual QA** of **already saved fields**, no re-extraction from start, no arbitrary source corrections.

## Original signed issuer source PDF evidence
- GAS 2025-Q1 consolidated original `https://static2.vietstock.vn/vietstock/2025/4/29/20250429_20240429___gas___cbtt_bctc_q1_2025_hop_nhat.pdf`; 76 pages, **18,836,716 bytes**, SHA256 `b86f8fa9f26731955d41cff2866d68aa9f1fd8692a78ff25b228447a51710d15`. Signed 21/04/2025 GAS original; issuer disclosure cover 29/04/2025. Visual PDF pages 4–5 B01, 6 B02, 7 B03.
- GAS 2025-Q2 consolidated original `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/GAS_Baocaotaichinh_Q2_2025_Hopnhat.pdf`; 75 pages, **14,166,457 bytes**, SHA256 `c21bc4e88e2ce3d8331fa518df619d50086de50feed8691e48f653b825a4f31d`. Signed 21/07/2025 GAS original; visual PDF pages 4–5 B01, 6 B02 (current quarter vs six-month YTD columns), 7 B03 6M YTD.
- GitHub Actions `44668684322`: source recovery **2/2 full PDFs** and first 23 original page PNGs, artifact `14599102084`. No OCR needed; manually inspected page source images (scanned text).
- Existing note37 Q1 disclosure correction is only segment disclosure, **not B01/B02/B03**. Preserve original and amendment provenance.

## Verified figures and reconciliation
- GAS Q1/2025 (VND): assets `82,020,779,538,795`, liabilities `17,693,590,948,680`, equity `64,327,188,590,115`; Q1 aftertax `2,762,782,490,472`; CFO `+4,148,471,083,342`, CFI `-1,694,772,666,608`, CFF `+145,909,966,728`; cash closing `8,166,654,567,957`. Existing 48 numeric fields, 15 exact-VND checks all residual 0. B03 original cash beginning `5,567,998,965,715` differs from 01/01 B01 comparator `5,567,983,431,468` by `15,534,247` VND; preserve vintage difference, do not blindly correct.
- GAS Q2/2025 (VND): total assets `88,634,139,110,702`, liabilities `19,860,792,028,126`, equity `68,773,347,082,576`; Q2 B02 net sales `30,080,421,244,663`; Q2 PAT `4,808,599,034,503`; PDF B03 H1 CFO `9,110,699,100,985`, CFI `-3,861,322,338,383`, CFF `-220,825,474,676`, net `+5,028,551,287,926`, FX `+895,656,722`, opening `5,567,998,965,715`, closing `10,597,445,910,363`.
- Q2 standalone H1 minus Q1 verified same-scope signed B03: CFO `+4,962,228,017,643`; CFI `-2,166,549,671,775`; CFF `-366,735,441,404`; net `+2,428,942,904,464`; Q2 begins at Q1 closing `8,166,654,567,957` and ending `10,597,445,910,363`. H1 FX less Q1 FX = +1,848,437,942 VND, quarter cash bridge residual 0.
- Existing source numerical validations: 15/15 Q1, 23 metadata exact Q2 identities and 29 dynamic source/quarter statements, all residual 0 VND. Do not infer missing accounting keys as zero.
- Two records in `data/financials-GAS.json` upgraded to original issuer source visual PASS with signed PDF hashes, page numbers, artifact and original scope. Existing original source figures unchanged; regression scripts `verify_gas_q1_source.py`, `verify_gas_q2_source.py` enforce original hashes and visual QA.

## Next
- New PR source visual recovery script `scripts/recover_gas_2025_q1_q2_original_images.py` and workflow `.github/workflows/recover-gas-2025-q1-q2-original-images.yml`. Require finance CI PASS and post-merge live smoke 45/45 SHA256.
- GAS Q3/2025 already source visual verified; **do not redo**. Next remaining work: GAS Q4/2025 or 2026 periods with missing source comparatives; then VDS/GEG. PLX Q3/2026 consolidated finished, parent B03 CFF signed original mismatch 87,654,015,000 VND remains quarantined pending corrected issuer source.
- Standard rules: Q1/2025 onwards max 20 periods, exact VND sources and million-VND normalization, quarterly vs YTD and parent vs consolidated separated, 0.01% tolerance, save checkpoint after verified ticker/period, no site layout change.
