# CHECKPOINT — MBB 2026 Q3 signed bank consolidated B02a / B03a / B04a exact-source recovery and quarterization

Date 21/11/2026; repository `kiemtimem12345/solieutaichinh`. Transition after completing VIX 7/7, GAS 7/7, VDS 7/7; PLX parent Q3 2026 B03 quarantined issuer 1.469% subtotal defect; GEG Q2 2026 signed source note11 proved opening deposit reclassification but Q2 standalone cash needs 31/03 pledge balance; IDC Q2 2026 signed TT43 current-quarter comparator absent. Previously completed records must remain untouched.

## Current missing period found and signed originals
MBB consolidated periods in production 2025 Q1 through 2026 Q2, only **6/7**. New 2026 Q3 report located through Vietstock issuer disclosure and MB official IR. Source original identical bank model, currency **triệu VND**:
- Q3/2026 Q3 original 61-page signed PDF (signed 20 October, publicly released 30 October), SHA256 `bd5b2bad6c4c0669f16e9673c9a076d100fa6eb51bc7085bf66db89053d618ce`, 3,862,536 bytes: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/MBB_Baocaotaichinh_Q3_2026_Hopnhat.pdf. Official announcement: https://www.mbbank.com.vn/nha-dau-tu/thong-bao/bao-cao-tai-chinh-hop-nhat-va-rieng-le-quy-3-nam-2026
- Q2/2026 original 61-page signed PDF, 3,683,597 bytes, SHA256 `a86757a4499953264ca22dd57ae2e3257057631107742e1d04ad1ecd0e2c23d1`: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/MBB_Baocaotaichinh_Q2_2026_Hopnhat.pdf?ver=8b5fd9ba . Q2 already in canonical dataset, only used as 6M cashflow comparator without modifying old values.
- GitHub Actions `44871203134` SUCCESS recovered original both PDF SHA values and visual pages **p3–4 balance B02a/TCTD-HN**, **p6 bank income B03a/TCTD-HN**, **p7–8 cash B04a/TCTD-HN direct cash flows**; artifact `14693223647`. Signed page renders and page 6/7/8 physically inspected, original source NOT OCR guess.

## Exact values bank source (triệu VND)
- Q3 30/09 B02a: total assets **1,837,857,452**, liabilities **1,673,715,844**, equity **164,141,608**. Balance and 11 main asset groups + 7 liabilities groups + capital components = exact.
- Q3 current quarter B03a: bank interest revenue 37,792,619, expense -19,956,645, net 17,835,974; service net 1,677,762; all operating income **21,091,443**; before provision 15,571,390; provision -5,241,290; pretax **10,330,100**; current tax -2,074,288, deferred -3,939, total tax 2,078,227; after-tax **8,251,873**, noncontrolling 212,376, parent 8,039,497. Current-quarter EPS cell not provided; 9M EPS source 2563 VND/share kept separately.
- Q2 original B04a 6M YTD: CFO -53,201,811; CFI -731,882; CFF +2,023,891; net -51,909,802; beginning 239,259,989; ending **187,350,187**.
- Q3 original B04a 9M YTD: CFO -65,264,905; CFI -1,521,762; CFF +7,071,757; net -59,714,910; beginning **239,259,989** (same Q2 source); ending **179,545,079**.
- **Q3 cashflow standalone** = Q3 9M−Q2 H1 6M: CFO **-12,063,094**, CFI **-789,880**, CFF **+5,047,866**, net **-7,805,108**, cash opening **187,350,187**, cash ending **179,545,079**; quarter CFO+CFI+CFF=net and beginning+net=ending EXACT 0 triệu. Capex Q3 standalone -796,582, cash dividends Q3 standalone -8,557,134.
- 9M B03a profit 24,400,066 = Q1 7,702,720 + Q2 8,445,473 + Q3 8,251,873; 9M operating income 58,955,963=Q1 17,430,206 + Q2 20,434,314 + Q3 21,091,443.
- All source accounting checks in `reports/source-audits/MBB-2026Q3-signed-consolidated-B02a-B03a-B04a-million-vnd.json`: **27/27 exact million-VND identity zero residual**, including same year-start and B02a net loans/investment/trading provisions. No 0.1% tolerance invoked; source unit original million VND not VND.

## Code branch acceptance gate
- `data/financials-MBB.json`: append only MBB Q3 2026 consolidated verified original 64 source fields; Q1/2025-Q2/2026 unchanged. Seven periods Q1/2025 to Q3/2026. B01/02/03 nomenclature mapped to actual bank **B02a/B03a/B04a**, no industrial model substitution.
- `scripts/verify_mbb_income.py`: increase roster to 7 and all bank signed quarterly P&L 8 checks each ->56; previous six quarters untouched.
- `scripts/verify_mbb_2026q3_signed_original.py`: independently read signed ledger, compare all mapped keys and new Q3 source, exact quarter B04a cashflow, 27 math tests and five negative tamper guards rejecting YTD as quarter, wrong unit, parent-vs-consolidated, invented quarterly EPS and wrong cash opening.
- `.github/workflows/validate.yml` requires both tests.
- **Do NOT claim main/production complete on unmerged feature branch**. Open PR, monitor CI, merge only if SUCCESS; check post-merge main finance CI, live web smoke 45/45 SHA, Pages, then final checkpoint. Do not touch other completed tickers or quarters.

## Next
After seven MBB quarters complete and production PASS, update latest checkpoint, move on to objectively still missing records in 32 ticker coverage audit, not old solved GAS/VDS/GEG/IDC or VIX historical quarters. Preserve source-original version metadata and sign.
