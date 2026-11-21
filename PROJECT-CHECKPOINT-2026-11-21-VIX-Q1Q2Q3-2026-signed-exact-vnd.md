# CHECKPOINT — VIX 2026 Q1/Q2/Q3 RIÊNG signed original (pre-merge, 21 Nov 2026)

Scope: VIX securities company, signed SEPARATE company-parent B01-CTCK/B02-CTCK/B03b-CTCK under TT210/2014 and TT334/2016, currency source VND; stored in millions VND. Do not conflate translation with consolidated. No use of 0.1% tolerance, all verified original arithmetical identities exact.

## Signed primary originals and SHA
- Q1 issuer https://vixs.vn/wp-content/uploads/2026/04/20260417-VIX-BAO-CAO-TAI-CHINH-QUY-I-2026.pdf, 43 pages, 8,667,531 bytes, SHA256 90845a76928739230468c0f8ea3f3890e29475fe91239cbb51c5e9b28aab852f.
- Q2 issuer https://vixs.vn/wp-content/uploads/2026/07/20260717-VIX-Bao-cao-tai-chinh-Quy-2-nam-2026.pdf, 43 pages, 5,734,803 bytes, SHA256 41ea9b8482afff88b81297139afac8fd9c2075aa01ecea350992beda23e622c0.
- Q3 issuer direct host unavailable even with 64 KB range; signed VIX parent PDF recovered from Vietstock disclosure ZIP https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VIX_Baocaotaichinh_Q3_2026.zip?ver=8c766727. ZIP SHA256 2ff2a874c70297e284946105ccc0143c72c92a29ff330112ce7736eb9fb2dbee. Original Vietnamese member VIX_Baocaotaichinh_Q3_2026_Congtyme.pdf, 44 pages, 6,286,791 bytes, SHA256 088c2fed91cee527f33e898f43b67b94ca4db404636841fbc963cb8c0c6acfbd. English member VIX_Baocaotaichinh_2026.pdf, 47 pages, SHA256 64ef26327d91aea75f699337efe86e7c3580701fa3dd66cbd6025e1e20d847f4 is a TRANSLATION of same parent scope, not consolidated nor independent corroboration.
- Recovery GitHub Actions 44865446595 failed due direct Q3 timeout but Q1/Q2 source downloads succeeded; alternate Q3 ZIP job 44865947377 PASS.

## Key original signed VND (Q1 | Q2 | Q3)
- Assets B01: 29,598,210,995,041 | 38,592,337,487,368 | 39,860,148,439,643
- Net profit B02 quarter: 138,370,269,055 | 75,882,025,127 | 173,835,663,136
- Standalone CFO B03: +3,243,431,300,446 | -6,932,367,903,529 | -1,441,172,047,997
- Cash end B01=B03: 970,994,021,164 | 2,615,847,191,635 | 2,263,801,259,952
- EPS signed year-to-date 3M/6M/9M: 90 | 114 | 177 VND/share; standalone quarter EPS cells blank, must stay null.
- **18 original exact VND B01/B02/B03 arithmetic identities per period = 54, all 0 VND residual**; B02 quarter + signed previous YTD = current YTD; B03 Q2 6M−Q1 3M, Q3 9M−Q2 6M; cash continuity begins with VIX 2025Q4 signed closing 2,049,092,199,336 VND. Off-B01 customer money kept separate from firm cash/liabilities.
- Repaired severe 2026 Q1 stale CFO=pretax proxy, 2026 Q2 CFO=YTD confusion, 2026 Q3 VND vs million, and 2026 B02 turnover/tax/expense mapping; no fake consolidated numbers.

## Source files and CI
- reports/source-audits/VIX-2026Q1Q2Q3-original-signed-VND.json — signed original VND ledger + PDF sha/period/scope.
- data/financials-VIX.json — only 2026 Q1 Q2 Q3 updated, 2025 Q1–Q4 untouched.
- scripts/verify_vix_2026q1q2q3_signed_original.py — all mapped original amounts, 54 exact identities, B02 3M/6M/9M, B03 independent quarterly bridges, 7 negative guards.
- Historic Q1 partial-source guard now requires completed signed original, legal framework updated; legal filing compliance still unassessed, financial source arithmetic not legal certification.
- .github/workflows/validate.yml adds independent new regression along existing 2025 regressions.

## Required next gate
This checkpoint is created on a feature branch, NOT YET CLAIMING MERGED OR DEPLOYED. Open PR and merge only after passing financial CI, then require main financial CI, live website read-only 45/45 SHA256 and Pages deployment PASS. Save final checkpoint with merge hash and run URLs. After all seven VIX RIÊNG Q1/2025–Q3/2026 pass, leave VIX and select next unfinished ticker according to source coverage checkpoint, never reprocess verified statements.
