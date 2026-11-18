SO-LIEU / SOLIEUTAICHINH.ONLINE — FULL DATA RECOVERY PACKAGE
Build date: 17/11/2026 (Asia/Ho_Chi_Minh)

WHAT THIS PACKAGE CONTAINS
- 32 financials-<TICKER>.json snapshots (the latest archived full set from 27/10/2026, overlaid with the verified GAS and GEG Q3/2026 snapshots).
- 9 category / market / rate / report snapshots, including 42 economic series in category-data.json.
- assets/app.js with same-origin-first loading via absolute /data/ URLs (works on nested routes) and JSON-body validation.
- BCTC-gap-audit-2026-11-17.csv and project checkpoint.
- No index.html, CSS, PHP, database schema, or visual layout files are included.

IMPORTANT DATA CUTOFFS
- GAS Q3/2026 B01/B02 both scopes visually verified. B03 is reported 9M YTD only; do not display it as Q3 standalone. Need same-scope Q2 B03 PDFs (official attachment IDs: consolidated 3359; parent 3357) before quarterization.
- KBC Q3/2026 consolidated text-extracted B01/B02/B03 reconciles numerically; official same-scope Q2 comparator B03 was visually inspected. Q3 page-image review remains Cache miss. A provisional JSON is stored at `provisional/KBC-Q3-2026-consolidated-provisional.json`, outside `data/`; do not publish until visual QA passes.
- GEG Q3/2026 parent and consolidated B01/B02/B03 visually verified and quarterized. The statement rows not present in the applicable forms are marked N/A/not presented, not zero.
- Other financials-*.json files are preserved from the latest complete site archive (27/10/2026), mostly Q2/2026 snapshots. They are a recovery base, not a statement that all 32 tickers have Q3/2026 data. See the audit CSV for exact missing fields and source/visual status.
- Category data contains 42 series; observation dates vary. The most recent available dates are stored per series; no gaps are interpolated. DOJI/BTMC gold, CBOT rough rice and Brent intraday quote were refreshed to 17/11/2026. A consistency repair also fills top-level `value/date` from the latest existing dated observation in every series; it adds no observations and performs no interpolation. Brent uses Reuters' later 17/11/2026 intraday observation, USD 93.71/bbl at 1340 GMT (+about 1.4%), not a settlement price.
- NCB currency rates are transfer OFFER/SELL rates effective 17/11/2026. Black-market USD is a surveyed indicative buy price, not an official exchange rate. OMO latest confirmed observation remains 16/11/2026; interbank latest remains 13/11/2026.

SAFE UPLOAD
1. Download/back up the current Hostinger public_html/data and public_html/assets folders first.
2. Upload the contents of this package's data/ folder into public_html/data/ (merge by filename; do not delete unrelated files).
3. Upload assets/app.js over public_html/assets/app.js. Keep index.html, CSS, PHP and folders unchanged.
4. Clear Hostinger cache if enabled and hard-refresh the browser.
5. Verify these URLs return JSON, not HTML/404:
   https://solieutaichinh.online/data/financials-MBB.json
   https://solieutaichinh.online/data/financials-GAS.json
   https://solieutaichinh.online/data/financials-GEG.json
   https://solieutaichinh.online/data/category-data.json
   https://solieutaichinh.online/data/currency-rates.json
6. Confirm site counters show 32 ticker snapshots (some periods still need extraction), and category widgets no longer say category-data.json unavailable.

DO NOT
- Do not interpret the old 27/10 financials as Q3/2026; most have latest Q2/2026.
- Do not mark incomplete/visual-pending values as verified.
- Do not replace any HTML or CSS from the live website with files from the old archive.
- Do not call this deployed until the JSON endpoints and the visible website have been tested after upload.

LIVE ACCESS LIMITATION
This session can prepare/validate files but has no authenticated Hostinger file-manager connection. The GitHub API for kiemtimem123/so-lieu has returned HTTP 403 (account suspended). No remote upload, commit, or deploy has occurred.

DIAGNOSTICS
- SNAPSHOT-DIAGNOSTIC.js probes all 41 data endpoints from the live website origin and reports HTTP status, content type, JSON validity, financial snapshot schema, and latest period.
- Paste it into browser DevTools Console after upload. Do not send credentials or cookies.
