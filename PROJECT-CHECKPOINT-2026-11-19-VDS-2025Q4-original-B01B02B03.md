# CHECKPOINT — VDS hợp nhất Q4/2025, PDF gốc Rồng Việt — 19/11/2026

## Điểm xuất phát
- Main checkpoint `PROJECT-CHECKPOINT-2026-11-19-VDS-2026Q1-original-Q2-cash-and-H1-FVTPL.md` updated commit `0ec5131064cb68772b97e1e3523050d8659acdb0`; PR #63 consolidated Q1/2026 merged commit `d1587e4216358e1d4997abfd10701bbacadd82df`, CI PASS, website 45/45 PASS.
- Verified GAS 2025Q1–2026Q3 and VDS 2026Q1–Q3 must not be reprocessed; VDS 2025Q1–2025Q4 legacy auto figures need issuer QA.
- This update addresses **VDS consolidated 2025-Q4**, preserving all other quarters and original invalid parser values.

## Official original source
- Issuer listing published **30/01/2026**: https://www.vdsc.com.vn/quan-he-co-dong/cong-bo-thong-tin/rong-viet-cong-bo-bao-cao-tai-chinh-hop-nhat-quy-4-2025-va-giai-trinh-chenh-lech-loi-nhuan-i983
- Issuer signed PDF (dated 28/01/2026): https://www.vdsc.com.vn/data/api/app/file-storage/8308ae9d-cdf4-47da-21e6-08de5fe7b04e/VDSC_Cong%20bo%20BCTC%20HN%20Quy%204%20nam%202025.pdf?downloadFrom=ManagementDocument-983
- 50-page 10,387,010-byte original; SHA256 `eba8fa6cde5e7325a8ab6fef5d2776807e81e6e3e17da24ed7a116f191baab95`. Original source GitHub Actions run `44509101362` PASS, rendered artifact `14520538548` visual pages 6–8 B01, 11–13 B02, 14–16 B03; separate official VDSC announcement and explanation documents independently corroborate Q4 profit.
- PDF scans manually reviewed, not OCR-only. All financial amounts in source are **VND**; JSON normalized to **million VND**, EPS remains VND/share.

## Original issuer verified numbers
| Q4/2025 consolidated | Original VND |
|---|---:|
| Assets 31/12/2025 B01 | 8,121,452,969,623 |
| Liabilities B01 | 5,022,323,459,557 |
| Equity B01 | 3,099,129,510,066 |
| Corporate cash B01/B03 | 996,975,599,252 |
| Stand-alone Q4 operating revenue (CTCK code 20) | 221,975,460,374 |
| Stand-alone Q4 operating expense code40 | 162,390,566,550 |
| Stand-alone Q4 PBT | 15,744,157,121 |
| Stand-alone Q4 tax expense | 5,651,950,112 |
| Stand-alone Q4 net profit | **10,092,207,009** |
| Stand-alone Q4 parent profit | 13,821,476,572 |
| Stand-alone Q4 NCI profit | -3,729,269,563 |
| Stand-alone Q4 EPS | 51 VND/share |
| FY2025 12M CFO from B03 | **-850,325,354,079** |
| FY2025 12M CFI B03 | -824,472,465,903 |
| FY2025 12M CFF B03 | +1,464,636,000,000 |
| FY2025 12M net cash movement | -210,161,819,982 |
| FY B03 beginning cash | 1,207,137,419,234 |
| FY B03 ending cash | 996,975,599,252 |

- Corporate cash ending FY2025 matches beginning of verified VDS 2026-Q1 B03 *exactly*; customer brokerage cash `1,748,126,020,118` VND remains separate, not included in company cash.
- B01/B02/B03 28 independently checked source accounting identities residual **0 VND**; 111 verified issuer fields, including 12M YTD.
- Prior auto values were **wrong**: Q4 `revenue=23,061 triệu` was FVTPL gain, not total revenue; `net_profit=15,744 triệu` mistakenly copied PBT, correct Q4 net is 10,092,207,009 VND; `operating_cash_flow_ytd=346,792 triệu` was **FY2025 pretax profit**, not operating CFO; actual FY CFO is **negative 850,325,354,079 VND**. The prior `foreign_exchange_effect_ytd=996,976 triệu` was closing cash, not FX. Old values saved in `financial_line_items_prior_values` and `financial_line_items_rejected_values`.
- **Do not infer Q4 stand-alone CFO, CFI, CFF** until VDS Q3/2025 consolidated 9M original B03 is visually verified. JSON 12M YTD valid; quarter-only cash fields intentionally null, `verification_status` explicitly deferred.

## Changes
- Data `data/financials-VDS.json` 2025-Q4 only, no changes to validated VDS 2026Q1–Q3 or untouched VDS 2025Q1–Q3.
- `scripts/inspect_vds_q4_2025_pdf.py` and `.github/workflows/inspect-vds-q4-2025-pdf.yml`: short-lived read-only official original PDF page render (no web writes).
- `scripts/verify_vds_q4_2025_source.py`: 28 exact-VND regressions, source hash, historical false parser check, separate brokerage cash, Q1/2026 opening cash equality, no fabricated Q4 quarter cash.
- `.github/workflows/validate.yml` runs this gate on every snapshot change.
- Open PR, verify CI PASS then merge and run 45/45 production web SHA check, save final commit to this checkpoint.

## Next priority (same VDS ticker)
1. **VDS consolidated 2025-Q3** issuer original B01/B02/9M B03; then recompute stand-alone Q4 B03 **12M minus 9M same scope** and certify.
2. Continue VDS 2025-Q2 → 2025-Q1 source QA and cross-period bridges. Don't leave ticker unless fully completed or explicit documented exception.
3. GEG historical gaps → IDC Q3/2026; don't redo GEG Q3 PASS. GAS 2026H1 COGS 10,160,150,278 VND allocation pending, PLX Q3 parent CFF 87,654,015,000 VND discrepancy still blocked.
4. Rules: period >=2025-Q1, at most 20, VND source to million-VND JSON, EPS VND/share, acceptable residual <=0.01%; original screenshots + precise source-vintage, main GitHub only deployment.
