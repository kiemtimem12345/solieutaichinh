# Checkpoint — website data recovery and continued BCTC work
Date: 17/11/2026, 21:12 Asia/Ho_Chi_Minh

## Current live diagnosis
- Live site search result currently reports 32 tickers but 0/0 quarterly periods and 32 tickers unable to load snapshots. It also reports `data/category-data.json` unavailable and the category panels empty.
- Direct web open of the website JSON endpoints did not expose their bodies (cache/internal error), so server file presence cannot be confirmed.
- GitHub API for repo `kiemtimem123/so-lieu` still returns 403 account suspended. No GitHub write possible. No authenticated Hostinger file manager connection is available.

## New exact data updates in this continuation
- NCB transfer OFFER rates updated to 17/11/2026 from the official NCB exchange-rate page: USD 26,000; EUR 29,503; GBP 34,646; JPY 166.92; CHF 31,333; CAD 18,438; AUD 17,807; SGD 20,403; KRW 23.29; THB 802.59 VND per unit.
- Free-market USD indicative buy value updated to 25,957 VND/USD from a survey of exchange points at 08:40 on 17/11/2026 (Vietnam.vn); not an official rate.
- OMO panels remain at 16/11/2026 because the NHNN-derived series source last updated at 17:02 on 16/11. Interbank rates remain at 13/11, the latest observation currently exposed by the source.
- Vietnam government yield curve remains at 16/11 (1Y 3.683%, 2Y 3.784%, 10Y 4.573%, 20Y 4.806%); 15Y/20Y source last update is 13/11.
- Category-data has 42 non-empty series and covers all 24 keys used by the existing app.js target map; no interpolation added. `global-rice` remains a single dated quote (refreshed 17/11), not a full historical series.
- Category snapshot consistency fix: 21 series had valid historical observations but null latest summary `value/date`; build now syncs those fields from the maximum dated existing observation. No new observation points were fabricated.
- Brent observation refreshed to Reuters' later 17/11 intraday quote of USD 93.71/bbl at 1340 GMT (+about 1.4%); this is not a closing/settlement value.

## KBC Q3/2026 consolidated — provisional numeric reconciliation, visual gate pending
- Official KBC issuer page confirms Q3 consolidated report date 12/10/2026 and Q3 separate report was also published that day. Q3 consolidated issuer page: https://kinhbaccity.vn/kbc-cbtt-bao-cao-tai-chinh-hop-nhat-quy-iii-nam-2026.htm. Signed disclosure no. 1210/2026/KBC-CK. Q3 PDF retrieval copy: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/KBC_Baocaotaichinh_Q3_2026_Hopnhat.pdf.
- Official Q2 consolidated comparator PDF was opened directly from KBC and B03 pages 7-8 visually inspected: https://kinhbaccity.vn/pic/FileLibrary/20260730-kbc-cbtt-bao-cao-tai-chinh-hop-nhat-quy-2-nam-2026_2039.pdf.
- Q3 B01 values (million VND): current assets 61,353,409.009; total assets 76,673,779.294; total liabilities 48,750,802.708; equity 27,922,976.586; balance check exact.
- Q3 B02 (million VND): revenue 3,187,288.760; gross profit 1,722,680.788; operating profit 1,214,071.099; PBT 1,220,726.477; PAT 937,236.264; parent PAT 911,255.360; NCI 25,980.904; EPS 968 VND/share. Tax-deferred line is a benefit, not expense; the investment-property-sale line is a printed dash. Formula checks and parent+NCI = PAT pass.
- Q3 B03 9M YTD (million VND): CFO -7,265,926.403; CFI -515,402.271; CFF +4,557,285.001; net -3,224,043.673; opening cash 8,368,534.552; closing 5,144,490.879.
- Q2 B03 6M same scope visually inspected (million VND): CFO -7,268,641.879; CFI +322,296.362; CFF +4,100,251.982; net -2,846,093.535; opening 8,368,534.552; closing 5,522,441.017.
- Derived Q3 B03 (million VND): CFO +2,715.476; capex -101,027.905; CFI -837,698.633; CFF +457,033.020; net -377,950.138; opening 5,522,441.017; closing 5,144,490.879. Components and cash bridge pass. FX/dividends-paid are not separately presented.
- Q3 screenshots still return Cache miss. Provisional JSON is stored outside production at `provisional/KBC-Q3-2026-consolidated-provisional.json`; `production_eligible=false`. Do not merge into `data/financials-KBC.json` until Q3 visual QA passes.

## BCTC status and corrections
- GAS Q3/2026 parent and consolidated PDF pages B01/B02/B03 were rechecked from Library originals. Both B01 are 13/13 and all UI B02 fields are either numeric, dash, or N/A. B03 Q3 report values are 9M YTD; Q3 standalone is still pending Q2 same-scope PDFs (consolidated attachment ID 3359, parent ID 3357).
- Important correction: a zoomed visual reread of GAS consolidated B02 page 5 corrected admin expense from 353,776.534967 to 353,776.354967 million VND. With the corrected extraction, the printed operating-profit subtotal exactly equals gross profit + financial income - financial expense + share of profit from associates - selling expense - admin expense. A temporary mismatch caused by low-resolution reading was removed and the equality is recorded in source validation.
- GEG Q3/2026 both scopes have B01/B02/B03 fully populated for the fields presented by the applicable statement forms. Parent-only fields absent/not applicable are marked separately, not as missing or zero.
- Other 30 financial snapshots are preserved from the last complete site bundle (27/10/2026), generally latest Q2/2026; audit records missing fields and status, no unsupported values added.

## Package created
- Full recovery package: all 32 `financials-*.json` files plus all nine ancillary JSON snapshots and the patched `assets/app.js`.
- It intentionally excludes `index.html`, CSS, PHP, and database files. Merge files into `public_html/data/` and replace only `public_html/assets/app.js` after backing up current site data.
- Package remains NOT deployed. Verify JSON endpoints and visible panels after manual upload.

## Deferred blockers to resume
1. GAS Q2/2026 parent and consolidated original PDFs: official page attachments IDs 3357/3359; still cache/transport blocked unless user uploads the downloaded PDFs.
2. PLX H1/2026 reviewed parent and consolidated source PDFs: HOSE files exceed the current reader size cap; Petrolimex file host times out. Parent Q3 printed CFF difference 87,654,015,000 VND remains preserved.
3. VDS Q3/2026 consolidated numeric Q3 standalone B03 PASS; visual QA Q3 remains blocked.
4. IDC Q3/2026 consolidated numeric pass, visual source blocked; parent source/visual pending.
5. Continue the other ticker B01/B02/B03 gaps listed in audit CSV; do not redo already-PASS calculations.
6. Hostinger deployment remains blocked until authenticated access/user upload; GitHub API 403 remains a separate blocker.

## Next priority
- First resolve GAS Q2/2026 comparator if user uploads/downloads the two official PDFs.
- Then PLX H1 and Q3 parent CFF source/visual review; next VDS/IDC; meanwhile process any available original PDFs and update only confirmed rows.
