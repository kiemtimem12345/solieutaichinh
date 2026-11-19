# CHECKPOINT — IDC consolidated Q2/2025 source and Q3 cash (19/11/2026, night ICT)

This checkpoint supersedes the Q2/2025 partial-source state of `PROJECT-CHECKPOINT-2026-11-19-IDC-Q3-2025-reviewed-H1-bridge.md`; it does not supersede the completed Q3/2025 or Q3/2026 results.

## IDC Q2/2025 original source recovered and verified
- HNX disclosure mirror: https://static2.vietstock.vn/data/HNX/2025/BCTC/VN/QUY%202/IDC_Baocaotaichinh_Q2_2025_Hopnhat.zip
- ZIP exactly 26,491,458 bytes, SHA256 `48616c2bb9d17c9937590f0f1332ff7e9b75e160385860b61fcc1c2e2a9e6614`.
- Signed consolidated original PDF member `4_idc_2025_7_30_caaaf64_vi_baocaotaichinhhn_q2_2025_s.pdf`; 15,956,738 bytes, 63 pages, SHA256 `04ced780ca282517bc28399e59d1a08dda0338cdda6a523403139a821674003f`; signed 29/07/2025.
- Github Actions recovery `44562677282` succeeded and generated 14 page images, artifact `14549641653`. Manually visually inspected **PDF pages 8–14**: B01 8–11, B02 page 12 (landscape), B03 pages 13–14.
- Added **100 exact-VND B01/B02/B03 source data fields** to `data/financials-IDC.json`. **30/30 independently computed accounting identities = 0 VND residual**. Original B01 assets **19,606,417,044,848 VND** = liabilities 12,150,945,318,805 + equity 7,455,471,726,043.
- Q2-only B02 revenue **1,763,197,891,011**, pretax 519,324,437,238, after-tax **415,963,907,220 VND**, EPS 902 VND/share. 6M operating profit **966,843,161,800 VND** (not 968,843,161,800; validated from original page image and exact equations). 6M PAT 832,948,451,824 VND.
- Original Q2 interim 6M B03 CFO **+1,402,209,397,523**, CFI **-2,438,216,817,714**, CFF **-288,817,920,091**, net **-1,324,825,340,282**, opening 2,188,037,806,317, FX +41,467,072, closing 863,253,933,107 VND, arithmetic to 1 VND.

## Reporting version classification in original Q2 29/07 vs EY-reviewed H1 28/08
- Exact B03 total CFO/CFI/CFF, cash opening/FX/closing agree.
- B03 investment profit adjustment original **-128,028,360,752** versus reviewed **-175,386,224,671**: difference +47,357,863,919 VND original minus reviewed.
- Cash operating before working capital original **1,351,845,045,068** versus reviewed **1,304,487,181,149**: difference +47,357,863,919.
- Receivables working-capital original **-113,079,215,676** vs reviewed **-96,383,418,698**: difference -16,695,796,978.
- Payables working-capital original **+650,923,124,092** vs reviewed **+681,585,191,033**: difference -30,662,066,941. Offsetting -47,357,863,919, hence CFO unchanged.
- Do not speculate why classification differs, do not overwrite an original source subtotal with a recalculation, and retain versions separately.

## Deferred and data-quality treatment
- IDC Q2/2025 `verification_status=issuer_original_visual_verified_b01_b02_b03_6m_ytd_q2_standalone_cash_deferred`; original B01/B02/B03 6M verified. **Standalone Q2 CFO/CFI/CFF remains null** until signed Q1 2025 original visuals and exact-VND 3M B03 are verified. Old Q2 standalone amounts and old unverified ROA/ROE preserved as `legacy_q2_unverified_values` for provenance only.
- IDC Q3/2025 standalone B03 had previously been computed from 9M minus EY-reviewed 6M: because top-level H1 CFO/CFI/CFF agree between originals, Q3 derivation is unaffected.
- IDC Q3/2026 remains PASS, not reprocessed; seven quarterly consolidated records remain from Q1/2025 through Q3/2026. Do not mix parent/consolidated.

## CI and next steps
- GitHub PR #83 https://github.com/kiemtimem12345/solieutaichinh/pull/83 adds recovery workflow and original Q2 source fields/verification script. `scripts/verify_idc_q2_2025_original.py` tests 100 fields, exact VND, 30 identities, original hashes, version differences.
- Verify PR CI and recovery workflow PASS before merge; verify deployment/site smoke after merge; no website layout changes.
- Next **IDC Q1/2025 consolidated** signed original PDF pages B01/B02/B03 from HNX/Vietstock, recover as bounded page images, exact-VND verify, then quarterize Q2/2025 B03 with Q1 exact same-scope source. Do not repeat Q3/2025/2026 passed work.
