# CHECKPOINT — VDS Q2/2026 hợp nhất, B01/B02 source visually reconciled 19/11/2026

## Starting point
- GAS H1 discrepancy well documented, PR #57 PASS, do not redo GAS verified periods.
- VDS Q3 2026 consolidated source B01/B02/B03 original 90 fields restored PR #59, then standalone CFO/CFI/CFF from Q2 6M original + Q3 9M original PR #60 merged commit `35af4bd560d42f1eeb9cb8ca0571d1a4655c08de`. CI and website 45/45 PASS.
- PR #61 implemented ephemeral source image rendering for VDS Q2 original, CI PASS, issuer PDF SHA-256 `d16188e1e63da279e5214af46271dfd67dab4d26c20c2d77c78cb1db56200410`, workflow run `44503781640`, artifact `14518217295`, 16 source page images. Original PDF https://www.vdsc.com.vn/data/api/app/file-storage/b0d720b4-5481-47f3-a9ad-08deed64b48e/VDSC_Cong_bo_BCTC_HN_Q2.2026.pdf?downloadFrom=ManagementDocument-1034 .
- Issuer signed 29/07/2026, published 30/07/2026, B01 PDF pages 6–8, B02 PDF pages 11–13 and B03 PDF pages 14–16. All core B01/B02 visually inspected, including original page 11 B02 revenue/expense items and original page 12 B02 profit; no use of unverified OCR numbers alone.

## New exact-VND issuer figures for VDS consolidated Q2/2026
- B01 total assets **7.906.589.387.452 VND**, liabilities **4.892.114.272.349**, equity **3.014.475.115.103**. Current assets **6.637.898.183.061**, noncurrent **1.268.691.204.391**. Cash **801.617.758.652** already matched B03 earlier. Verified multiple B01 class decompositions with exact residual 0.
- B02 **Quý II, Năm nay** revenue from CTCK form **262.152.978.583 VND**, operating cost **157.186.798.783**, financial income **5.473.235.995**, financial expense **21.800.613.791**, administrative expense **45.931.870.444**, operating result **42.706.931.560**, other result **5.473.946**, pretax profit **42.712.405.506**, tax expense **9.613.460.295**, net profit **33.098.945.211**, controlling net profit **36.516.641.493**, noncontrolling profit **-3.417.696.282**, EPS **134 VND/share**.
- B02 6M YTD revenue **458.846.424.238**, pretax **6.677.335.807**, net profit **3.608.144.765** VND, consistent with H1 B03 pretax. Q3 9M minus Q3 isolated also validates H1 revenue.
- The prior auto parser falsely stored Q2 revenue **74.785 million VND** (a component of FVTPL gain rather than overall CTCK revenue code 20) and EPS **501 VND** rather than 134 VND. Prior erroneous values and other changed automatic fields were saved in `financial_line_items_prior_values` / `financial_line_items_rejected_values`; 29 previous fields were updated to exact VND after source comparison.
- 87 source fields B01/B02/B03 validated with **24 exact-VND identities residual 0** for B01/B02 (plus independent 5 source identities from B03 H1). Q2 cash **standalone** (rather than 6M YTD) remains null pending verified Q1 same-scope B03, so **do not label VDS ticker fully finished**.
- Current VDS Q3 source and standalone quarterly cash were previously PASS; do not re-read or recompute. Existing 2025 quarterly VDS and Q1/2026 are auto-extracted pending source validation, not PASS.

## Added CI and checkpoint
- `data/financials-VDS.json` updates only VDS 2026-Q2 B01/B02 source values and retained original B03 (no other periods modified).
- `scripts/verify_vds_q2_2026_source.py` asserts 24 exact-VND source identities, previously misparsed fields quarantined, 87 verified financial values, and blocked Q2 standalone B03 status.
- `.github/workflows/validate.yml` runs this as CI gate. New source inspection workflow from PR #61 (original PDF page previews).
- Merge only after CI PASS, then verify 45/45 HTTPS / SHA-256 production.

## Next
1. VDS 2026-Q1 original consolidated B01/B02/B03 PDF; calculate standalone Q2 B03 as Q2 H1 less verified Q1; preserve already PASS VDS Q3.
2. VDS 2025Q1–Q4 remaining auto-extracted pending source verification, one quarter at a time. Never assume already validated if only `auto_extracted_pending_visual_review`.
3. Proceed GEG old gaps then IDC Q3/2026 when VDS really done. Do not redo GEG Q3/2026 or GAS verified records.
4. PLX parent Q3/2026 B03 CFF discrepancy 87,654,015,000 VND stays unresolved, no forced correction.
5. Store checkpoints on GitHub main; data from 2025Q1, maximum 20 periods, numeric tolerance 0.01%, source VND to `triệu VND` with EPS VND/cp, bank/broker/industrial statement formats distinct.
