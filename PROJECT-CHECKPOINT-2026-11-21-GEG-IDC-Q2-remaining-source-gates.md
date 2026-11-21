# Checkpoint 2026-11-21 — GEG and IDC Q2/2026 standalone B03 exceptions

Scope: source-evidence-only follow-up; repository kiemtimem12345/solieutaichinh, main. Do not redo already PASS GEG/IDC Q1/2025–Q3/2026 B01/B02 and source YTD B03, nor GEG/IDC Q3 standalone verified amounts.

## GEG consolidated 2026-Q2
Original signed Q1 and Q2 and source audit already proved that 11,422,218,903 VND pledged bank deposits were reclassified out of Jan 1 2026 cash equivalents into other current assets (Q2 note 11, PDF p24). Total current assets did not change. Q1 signed cash at Mar 31 105,856,793,049; Q2 signed cash at Jun 30 100,327,178,533. Straight H1−Q1 cash flow YTD leaves −11,422,218,903 VND cash bridge discrepancy. Q1 notes did not prove restricted balance at 31 March, so NO Q2 standalone CFO/CFI/CFF and no invented bridge. Continue to use metadata and fail-closed tests in prior checkpoint PROJECT-CHECKPOINT-2026-11-21-GEG-Q2-2026-note11-cash-reclassification-exact-bridge.md.

## IDC consolidated 2026-Q2
Q1 original says TT99/2025, H1 signed reviewed says TT99 and TT43/2026, H1 note41 documents 2025 comparative changes, not an official restated Q1 2026 B03. The 2026 opening-cash vintage difference is +890,796,892 VND. H1−Q1 provisional quarter totals CFO −202,543,174,911; CFI +480,833,384,534; CFF −471,228,735,423 VND are NOT production-ready; Q2 standalone cashflow stays NULL. Source regression and metadata already documented in PROJECT-CHECKPOINT-2026-11-21-IDC-Q2-2026-TT43-signed-policy-cross-vintage-B03.md.

## 2026-11-21 follow-up search
Targeted external search for GEG 31/03/2026 pledged/blocked deposits and IDC restated signed Q1/2026 B03 under TT43 found no qualifying signed current-period restatement. Third-party aggregate quarterly cash-flow tables are not valid to replace originals. No source-version blocker was removed. Existing source validation/checkpoints remain controlling.

## Required proof to close
GEG: issuer signed evidence of restricted deposits and cash-classification amounts at 31 March 2026 and explicit re-presented Q1 current-period cashflow (or signed reconciliation).
IDC: issuer signed Q1 2026 current-period B03 on same TT43 H1 reporting basis, or explicit signed current-year mapping of changed line items.
Upon recovery: rerun existing two ticker-specific validators plus global .github/workflows/validate.yml, verify production website checks, and only then mark quarter standalone B03 PASS. Until then do not change financials-GEG.json or financials-IDC.json numerical fields; preserve original B01/B02 and YTD B03 PASS.

This checkpoint records a still-open evidence gate; it does NOT claim new numerical PASS, CI, deployment or a resolved financial statement.
