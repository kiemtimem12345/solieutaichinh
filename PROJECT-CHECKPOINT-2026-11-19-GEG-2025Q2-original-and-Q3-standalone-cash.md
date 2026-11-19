# CHECKPOINT — GEG 2025 Q2 issuer original consolidated and Q3 standalone cash — 19/11/2026

## Exact resume pointer
- GitHub main pre-update latest commit: `7a6bc1d14a5feb83591f63165d899676e387abf4` PR #73, GEG signed original 2025 Q3 B01 B02 9M B03 and Q4 FY-minus-9M standalone CFO/CFI/CFF validated; see `PROJECT-CHECKPOINT-2026-11-19-GEG-2025Q3-original-Q4-quarterly-cash.md`.
- VDS all 7 consolidated periods 2025Q1–2026Q3 source-verified, **do not reprocess**. GEG 2025Q3,Q4 and 2026Q1,Q2 plus 2026Q3 both scopes source-verified. GEG 2025Q1 remains auto-extracted pending manual verification and is the next period.
- **Production website is not up-to-date** at this checkpoint: site smoke run `44530634005` 44/45, `data/financials-GEG.json` production 114,448 bytes vs tracked 127,582 bytes. Main financial CI PASS. Do not label website 45/45 until new run passes; do not stage November 18 archive ZIP over newer Git data. Manual guarded deploy workflow needs authorized execution and FTPS/SFTP credentials, not available via GitHub connector workflow dispatch.

## PDF original and scope proof
- Original consolidated **GEG Q2/2025 85-page signed PDF**: https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/GEG_Baocaotaichinh_Q2_2025_Hopnhat.pdf
- Original issuer signed **24/07/2025**, disclosure released 29/07/2025. Original screenshot PDF **pages 7–8 B01**, **page 9 B02**, **pages 10–11 B03** (PDF 1-based); report title explicitly `BÁO CÁO TÀI CHÍNH HỢP NHẤT QUÝ II/2025`, original tables `B01-DN/HN`, `B02-DN/HN`, `B03-DN/HN`.
- SHA256 not computed: preserve original fixed URL and screenshots, do not invent hash. Source amounts VND; normalized JSON `triệu VND` except EPS VND/share. Q2 B02 uses **Quý II/2025** column, not H1 cumulative.

## Source verified GEG 2025-Q2
| Indicator (VND) | Source original |
|---|---:|
| B01 total assets 30/06/2025 | 15,185,463,396,529 |
| B01 liabilities | 8,688,615,254,343 |
| B01 equity | 6,496,848,142,186 |
| B01 cash equivalents | 473,549,350,030 |
| B02 standalone Q2 revenue | 624,339,137,173 |
| B02 standalone Q2 cost of goods sold | 351,447,828,104 |
| B02 standalone Q2 gross profit | 272,891,309,069 |
| B02 standalone Q2 pretax profit | 184,091,358,827 |
| B02 standalone Q2 income-tax expense | 26,376,499,388 |
| B02 standalone Q2 consolidated net | 157,714,859,439 |
| B02 standalone Q2 parent net | 165,820,759,376 |
| B02 standalone Q2 NCI net | -8,105,899,937 |
| B02 EPS | 356 VND/share |
| B02 H1 revenue | 1,737,094,997,154 |
| B02 H1 PBT | 789,386,094,257 |
| B02 H1 net | 770,660,867,986 |
| B03 H1 CFO | 555,421,075,993 |
| B03 H1 CFI | 476,067,298,075 |
| B03 H1 CFF | -721,712,954,268 |
| B03 H1 net movement | 309,775,419,800 |
| B03 H1 cash beginning | 163,717,707,072 |
| B03 H1 FX | 56,223,158 |
| B03 H1 cash ending | 473,549,350,030 |

- B03 H1 cash bridge: 163,717,707,072 +309,775,419,800 +56,223,158 = **473,549,350,030**, B01 cash matches. 96 manually reviewed source fields, **35 exact VND identities** including B01/B02/B03, and 9M Q3 source less standalone Q3 reproduces H1 B02 revenue, COGS, gross, PBT, net and parent net, zero residual.
- Older 2025Q2 auto values archived in `financial_line_items_prior_values` and `financial_line_items_rejected_values`. Q2 `selling_expense=0` due issuer B02 dash; old parser -135 million is not a valid Q2 source figure. Q2 standalone CFO/CFI/CFF intentionally null until GEG Q1 2025 B03 source verified.

## GEG 2025-Q3 standalone cash newly derived (issuer original 9M minus H1)
| B03 VND | 2025 Q3 YTD 9M | 2025 Q2 YTD H1 | Q3 stand-alone |
|---|---:|---:|---:|
| CFO | 856,209,015,015 | 555,421,075,993 | **+300,787,939,022** |
| CFI | +244,031,897,120 | +476,067,298,075 | **-232,035,400,955** |
| CFF | -857,979,656,903 | -721,712,954,268 | **-136,266,702,635** |
| Net movement | +242,261,255,232 | +309,775,419,800 | **-67,514,164,568** |
| FX | +74,334,749 | +56,223,158 | +18,111,591 |
| Opening corporate cash | — | 473,549,350,030 | 473,549,350,030 |
| Closing corporate cash | 406,053,297,053 | 473,549,350,030 | 406,053,297,053 |

- Exact quarterly cash bridge: 473,549,350,030 -67,514,164,568 +18,111,591 = 406,053,297,053 VND. Q3 capex -103,386,144,231 VND; Q3 standalone cash section and capex checks residual **0 VND**. No scope mixing, original YTD source values untouched.
- GEG Q3/2025 status updated to `issuer_signed_original_visual_verified_B01_B02_B03_9m_ytd_and_Q3_standalone_cash`; 104 total issuer/derived fields.

## Files / QA / next
- `data/financials-GEG.json`: only 2025Q2 original source and 2025Q3 newly derived standalone cash updated; all accepted 2025Q4/2026 periods untouched.
- `scripts/verify_geg_q2_2025_original.py`: exact VND source fixtures, 35 original identities, Q3 9M-minus-H1 cash bridge and source provenance.
- `scripts/verify_geg_q3_2025_original.py`: now requires derived Q3 flows and updated field count; `.github/workflows/validate.yml` includes new gate.
- Merge only **CI PASS**; run production SHA smoke, report site sync as separate status. If production remains 44/45 due older GEG JSON, stop falsely reporting deployed, don't roll back finance data by old ZIP. No remote deletions; prefer guarded validated JSON-only deploy when workflow invocation is explicitly available/authorized.
- **Next GEG 2025-Q1** original signed B01/B02/3M B03, then compute GEG 2025Q2 standalone cash from H1–Q1. Once verified all 7 consolidated periods + 2026Q3 parent, mark GEG complete with permanent backup/checkpoint, proceed IDC 2026Q3. Keep GEG 2026 cash opening comparator discrepancy 11,422,218,903 VND under source version review, not silently corrected.
- Existing GAS H1 cost-of-goods gap 10,160,150,278 VND and PLX Q3 parent B03 CFF gap 87,654,015,000 VND remain separately documented.
- Project rules: only >=2025-Q1, max 20 periods per ticker, <=0.01% discrepancy tolerance, one ticker at a time, company parent and consolidated scopes isolated, VND vs million VND, no repeats of PASS data.
