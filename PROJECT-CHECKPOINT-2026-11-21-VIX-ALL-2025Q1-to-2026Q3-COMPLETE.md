# FINAL CHECKPOINT — VIX all 2025-Q1 through 2026-Q3 separate-source B01/B02/B03 complete, 21 Nov 2026

## Production acceptance verified
GitHub repo: `kiemtimem12345/solieutaichinh`. VIX specialist **RIÊNG/company parent** statements (TT210/2014 and TT334/2016) all seven in-scope quarters now verified using signed originals exact VND, not unsupported consolidated data.

- 2025-Q1, Q2: signed source RIÊNG B01/B02/B03 passed PRs #101/#102, checkpoint `PROJECT-CHECKPOINT-2026-11-21-VIX-through-2025Q4-main-verified.md`.
- 2025-Q3 PR #103, 2025-Q4 PR #104 same source evidence, accepted and preserved without reprocessing.
- **2026-Q1/Q2/Q3 PR #107 merged**: https://github.com/kiemtimem12345/solieutaichinh/pull/107. Merge commit **`990eb784ffea00155a81647d226d871d7b0d2407`**. 18 exact original B01/B02/B03 identities per quarter (**54 checked, 0 VND arithmetic difference**), plus B02 Q1+Q2=H1, H1+Q3=9M and B03 Q2=6M-Q1, Q3=9M-H1 same source scope and vintage; seven negative tests reject wrong values/scope/units/EPS/customer money.
- Branch financial CI `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44866950760` SUCCESS.
- **Post-merge main financial CI** `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44867023803` SUCCESS, including all old 2025 VIX, PLX and other ticker tests.
- **Production read-only HTTPS smoke** `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44867023849` SUCCESS: **45/45 URL/SHA256 exact match**, 32 financial JSON +9 auxiliary JSON, homepage JS/CSS.
- **GitHub Pages deployment** `https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44867023393` SUCCESS.
- All 2025 previously accepted data untouched. No use of the conditional 0.1% tolerance (all 2026 source arithmetic checked exact).

## Exact signed VND 2026 evidence
| | Q1 | Q2 | Q3 |
|---|---:|---:|---:|
| B01 assets | 29,598,210,995,041 | 38,592,337,487,368 | 39,860,148,439,643 |
| B02 quarter PAT | 138,370,269,055 | 75,882,025,127 | 173,835,663,136 |
| Quarter CFO | +3,243,431,300,446 | -6,932,367,903,529 | -1,441,172,047,997 |
| B01/B03 quarter-ending cash | 970,994,021,164 | 2,615,847,191,635 | 2,263,801,259,952 |
| YTD EPS VND/share (quarter EPS cells blank) | 90 | 114 | 177 |

- Q1 issuer signed 17/04/2026 `https://vixs.vn/wp-content/uploads/2026/04/20260417-VIX-BAO-CAO-TAI-CHINH-QUY-I-2026.pdf`, 43 pages SHA256 `90845a76928739230468c0f8ea3f3890e29475fe91239cbb51c5e9b28aab852f`.
- Q2 issuer signed 17/07/2026 `https://vixs.vn/wp-content/uploads/2026/07/20260717-VIX-Bao-cao-tai-chinh-Quy-2-nam-2026.pdf`, 43 pages SHA256 `41ea9b8482afff88b81297139afac8fd9c2075aa01ecea350992beda23e622c0`.
- Q3 signed Vietnamese **company-parent** report from Vietstock disclosure ZIP `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VIX_Baocaotaichinh_Q3_2026.zip?ver=8c766727`, ZIP SHA256 `2ff2a874c70297e284946105ccc0143c72c92a29ff330112ce7736eb9fb2dbee`. Member `VIX_Baocaotaichinh_Q3_2026_Congtyme.pdf` 44 pages SHA `088c2fed91cee527f33e898f43b67b94ca4db404636841fbc963cb8c0c6acfbd`; second member 47-page English **translation of same RIÊNG statement** SHA `64ef26327d91aea75f699337efe86e7c3580701fa3dd66cbd6025e1e20d847f4`. The direct issuer Q3 URL was blocked, successful regulatory disclosure mirror with fully validated PDF used; do not claim English translation is a separate consolidated statement or independent data source.
- `reports/source-audits/VIX-2026Q1Q2Q3-original-signed-VND.json` exact source ledger and PDF provenance.
- `scripts/verify_vix_2026q1q2q3_signed_original.py` 54 exact VND identities + seven fail-closed tamper tests; original 2025/TT334 legal framework CI preserved.
- Q3 and Q2 source quarterly EPS cells blank: leave null, YTD EPS source separate. Client brokerage money is OFF firm B01, always kept separate from company cash/liabilities. Cash opening 2026-Q1 agrees with verified signed Q4/2025 year end 2,049,092,199,336 VND. Same-scope B02/B03 quarterly YTD bridges fully reconciled.
- Legal and disclosure timeliness certification separate and **NOT claimed**; source/arithmetical completion is a data QA result only.

## Status transition
Mark **VIX financial-source task COMPLETE, all 7/7 quarter periods Q1/2025→Q3/2026**. No more reprocessing unless a later contradictory issuer amendment is found. 2026Q3 is **RIÊNG**, not a claim that a hypothetical consolidated report exists. Global rule ≤0.1% for multiple-source-confirmed eligible subtotals unchanged and not needed for VIX.

## Next checkpoint
Per user's latest instruction, **leave VIX and select next incomplete independent workstream/ticker** from current checkpoint and `scripts/audit_all_statement_coverage.py`. Preserve existing verified tickers and statuses. Existing known PLX 2026Q3 **parent** B03 CFF exception >0.1% is not resolved by VIX and must remain blocked if encountered; source alternative/issuer correction required.
