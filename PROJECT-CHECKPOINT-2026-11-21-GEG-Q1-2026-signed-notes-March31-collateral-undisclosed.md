# GEG 2026 Q1 B09 signed original extended notes QA — 21 Nov 2026

## Evidence since last checkpoint PR #109
- Original signed GEG consolidated Q1 2026 **82-page PDF**: SHA256 d8dade2f270452432a190bedddb46736523cc3a74b783ae1a2f82b76a5e74d5b. Public original: https://static2.vietstock.vn/vietstock/2026/4/29/20260429___geg___bao_cao_tai_chinh_hop_nhat_q1_2026___giai_trinh__song_ngu_.pdf
- Newly recovered original pages 15 to 42; complete SHA confirmed, source-only GitHub Actions 44869922268, image artifact 14693117139.
- **Q1 B01 PDF page 6**: bank cash 31/03/2026 46,625,510,309 VND, bank equivalents 59,231,282,740, total 105,856,793,049; code160 other current assets 65,558,815,530. Original Q1 B01 lists only code161/162/163 beneath 160, **no separately displayed code165**. That does **not** prove a restricted deposit had a zero balance.
- **Q1 B09 note5 PDF page 22**: repeats cash 46,625,510,309 and equivalents 59,231,282,740; initial maturity of bank equivalents <=3 months; does **not** separately disclose the amount pledged or restricted as at 31 March.
- **Q1 B09 note16a PDF page 27**: prepaid expenses at 31/03/2026 20,606,764,369; no pledged-deposit note or balance.
- Prior verified **Q2 signed B09 note11 PDF page24**: restricted bank guarantee deposits Jan1 11,422,218,903 VND and Jun30 54,079,653,068 VND (code165 other current assets). Opening B01 representation decreased cash equivalents code112 and increased other current assets code160 by equal 11,422,218,903 VND, total current assets unchanged.
- Original Q1 and H1 2026 B03 both internally balance exact VND, but computing Q2 as H1−Q1 crosses source vintage and leaves Q2 cash bridge residual -11,422,218,903 VND; the Jan1 collateral deposit figure does **not** establish Mar31 restated cash. Do NOT publish standalone Q2 CFO/CFI/CFF; keep NULL. No arithmetic 0.1% waiver for source version/classification.
- New JSON audit: reports/source-audits/GEG-2026Q1-B09-note5-and-16a-no-March31-pledged-balance.json. Add metadata flags to 2026Q1/Q2 only. CI regression: scripts/verify_geg_2026q1_note5_march31_restricted_cash.py. No signed source financial numbers altered.

## Next
After CI and website smoke merge, GEG Q2 remains blocked only for standalone B03; reopen if an issuer-signed 31/03/2026 restricted-cash balance/restated B03 is provided. Move to IDC 2026Q2 next: +890,796,892 VND original-vs-reviewed opening cash reclassification confirmed in H1 Note41, but Q2 standalone quarter cash basis needs independent source-validation. Do not revisit any previously PASS quarters/tickers.
