# Checkpoint production — 19/11/2026, GAS consolidated 2025-Q1 through 2026-Q2

## Production validation / latest commit
- Current main after PR #55: `17da6f35a3f8c24b25bb4c5b58db7d73fce32355`.
- GAS Q4/2025 finished PR #50; GAS Q1/Q2 2026 finished PR #52. 2025 Q1-Q3 earlier, 2026-Q3 consolidated+parent earlier; never reprocess already verified values.
- GAS Q4: 52 fields, 23 source arithmetic checks PASS. GAS Q1/Q2: 49+50 fields, 18+18 source arithmetic checks PASS. Original issuer signed PDF pages were visually inspected, never OCR-only.
- GAS audit/review comparisons (PR #53 source inspector, PR #54 metadata), original quarter data retained; audit 2025 and H1 reviewed 2026 are separately recorded and cross-checked by `scripts/verify_gas_reviewed_h1_versions.py`.
- GitHub Actions production after PR #54: CI `44494683084` PASS; smoke `44494683125` attempt 2 PASS. PR #55 fixed a transient Git/Hostinger deployment race (per-commit cache busting and bounded HTTP retry), no data or UI change.
- After PR #55: CI `44495138557` PASS; site smoke `44495138507` **45/45 HTTPS HTTP200 + SHA256 PASS**. Preserve UI and 41 tracked JSON including 32 financial files.
- Latest checkpoint explains source version differences: `PROJECT-CHECKPOINT-2026-11-19-GAS-reviewed-audited-cross-version.md`.

## Source-vintage and anomalies
- 2025 original unaudited closing balance assets `93.531.511.866.676` VND; audited 2025 published 04/03/2026 `93.568.198.109.790` VND, +`36.686.243.114` VND. 2026 opening B01 uses audited source (difference between vintages confirmed; audit-specific adjusting journal still not established).
- Original Q2/2026 H1 vs signed Deloitte-reviewed H1/2026 (14/08): revised B01 total assets `102.853.960.066.179` vs original `102.869.897.500.506` VND, −`15.937.434.327`. Reviewed B03 CFO `6.455.378.093.715` vs original `7.038.604.357.979`, CFI reviewed `−2.234.588.471.909` vs original `−2.828.965.984.641`; end cash same `11.055.638.145.352`.
- H1 reviewed B03 pretax equals reviewed B02 pretax, fixing B03/B02 original mismatch `11.034.262.367` VND; H1 reviewed opening cash equals audited 2025 close, fixing `15.534.247` VND opening discrepancy in reviewed version.
- **Still blocked:** H1 reviewed B02 COGS/pretax/net differs from Q1 original + Q2 original by `10.160.150.278` VND. Reviewed H1 B02 agrees with initial H1; only stand-alone Q1/Q2 sums differ. No evidence yet how this is allocated to quarterly history; do not silently force Q1/Q2 to sum H1.
- **Still blocked:** May not replace Q2 standalone cash flow with 6M reviewed less unreviewed Q1 without same accounting basis. The latest reviewed 6M is stored as `source_validation.reviewed_h1_version_comparison` alongside unreviewed Q2 source; original per-quarter fields unchanged. Full GAS ticker remains pending source-vintage adjudication.
- PLX parent Q3 B03 has unresolved `87.654.015.000` VND difference, remains blocked.

## Next action
1. Focus GAS H1 reviewed detailed footnotes for the exact retrospective 10.160.150.278 COGS/profit adjustment and B03 CFO/CFI classification. Ensure valid revised Q1 basis before allocating to Q2.
2. Do not alter already PASS periods absent explicit source contradiction and verified accounting trail. Source original vs audited/reviewed are distinct evidence vintages; scope remains consolidated.
3. When cross-period GAS validated under 0.01%, mark GAS complete and proceed VDS Q3/2026, then GEG historical missing periods, IDC Q3/2026.
4. GitHub main production source, website existing UI immutable. 2025-Q1 onward, max 20 quarters, millions VND except EPS, 0.01% tolerance.
