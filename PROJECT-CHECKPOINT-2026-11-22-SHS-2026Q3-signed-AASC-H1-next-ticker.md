# CHECKPOINT — SHS 2026Q3 signed issuer and independently AASC reviewed H1, 2026-11-22

**Repo:** `kiemtimem12345/solieutaichinh`; **PR #143**; branch `work/shs-2026q3-signed-original-reviewed-h1-20261122`, base `main`. **Before claiming completion**, verify final financial and source CI on latest PR head SUCCESS, merge PR, and re-read `main` row/checkpoint. VCB 7/7 was already PASS/merged PR #142; SHS 2025Q1–2026Q2 rows unchanged. Do not reload previous completed periods; never include 2024 dashboard periods.

## Exact independent source originals and scope
- Company SHS issuer signed report dated 20/10/2026, official `https://s3-storage.shs.com.vn/shs-website/VI_SHS_Bao_Cao_Tai_Chinh_Q3_2026_UB_94d6052636.pdf`, **40 pages**, 29,580,249 bytes, SHA256 **`78622b1eb767b4cbefa53836bde45ece8f8feb6baa55d6bac1d155667f80acc8`**. Signed Q3 issuer B01a-CTCK pp6–8, off-company broker client cash p9, B02a-CTCK direct Q3 and 9M pp10–12, B03b-CTCK corporate cash pp13–14, broker client cashflow p15.
- Independently AASC-reviewed H1 original `https://s3-storage.shs.com.vn/shs-website/VI_SHS_Bannien_BCTC_2026_f1d999d678.pdf`; signed 13/08/2026; **56 pages**, 37,951,575 bytes, SHA256 **`6511a79ba024ffa3070b2739c634c9a88f45236ec7d716de0a7fe932a4d2c2f0`**. H1 B01 pp10–11, B02 pp14–15, B03 corporate pp17–18, broker customer p19. Both official full sources independently hashed original GitHub workflow **45013391624 SUCCESS**, visual JPEG artifact **14750393671** retained 1 day, original copyrighted PDFs never committed.
- Accounting scope is SHS **issuer company CTCK statement**. Do not label consolidated without explicit issuer source. **VND source exact** (unlike VCB triệu VND), only convert to triệu VND in dashboard by dividing by 1,000,000. Broker client cash in source B01 off-statement code026 is **1,211,124,622,076 VND**, not SHS own cash **3,392,364,033,103 VND**; they cannot be added.
- `reports/source-audits/SHS-2026Q3-issuer-signed-AASC-reviewed-H1-exact-vnd.json`: 62 signed/reviewed **exact VND values**, **24 source accounting identities all exactly 0 VND**, including statement B01 balance, B02 Q3 direct income vs 9M−H1, B03 corporate cash and broker-client segregation, independently reviewed H1 balance and company cash.
- `scripts/verify_shs_2026q3_signed_reviewed_h1.py`: 62 value checks, 24 recomputed equations, 4 corruption controls, correct source-verified Q3 annualized ROA/ROE; included in mandatory `.github/workflows/validate.yml`. No changes to 2025 or 2026Q1/Q2 SHS entries. Newly appended only SHS 2026Q3 in `data/financials-SHS.json`, 7 periods total.

## SHS original Q3/2026 financial position (VND)
| Indicator | As printed |
|---|---:|
| Total assets 30/09 | 29.053.827.666.847 |
| Current assets | 28.883.331.945.178 |
| Long-term assets | 170.495.721.669 |
| Liabilities | 16.532.398.788.107 |
| Equity | 12.521.428.878.740 |
| SHS own cash / equivalents | 3.392.364.033.103 |
| FVTPL assets | 8.357.765.086.899 |
| HTM assets | 1.429.173.437.325 |
| Margin/other financial loans | 12.435.414.017.252 |
| AFS assets | 2.494.862.250.450 |

Independently AASC-reviewed prior June30 SHS assets **27,566,961,471,493 VND** and equity **12,544,246,462,810 VND**, balances exact, suitable for Q3 annualized ROA **2.87%** and ROE **6.49%** (4× quarter PAT divided by two-point average balance). Calculated ratios may remain qualified as annualized simple quarterly ratios, not TTM.

## SHS direct issuer B02a Q3 vs 9M−AASC H1 (VND)
| Indicator | Signed direct Q3 |
|---|---:|
| Total operating revenue | 1.001.990.396.188 |
| Operating expenses | 370.115.926.821 |
| Finance income | 981.981.572 |
| Finance expenses | 352.361.500.605 |
| Administration expenses | 29.685.108.052 |
| Profit before tax | **250.810.082.215** |
| Corporate tax | 47.556.157.510 |
| PAT | **203.253.924.705** |

Signed 9M operating revenue **2,017,028,302,710**, reviewed H1 **1,015,037,906,522**; signed 9M PBT **620,521,717,151**, reviewed H1 **369,711,634,936**; signed 9M PAT **510,853,071,094**, reviewed H1 **307,599,146,389**. All differences match signed Q3 **0 VND residual**.

## B03b company cash exact Q3 standalone from 9M−reviewed 6M (VND)
| Corporate cash | Signed 9M Q3 | Reviewed H1 | Derived Q3 |
|---|---:|---:|---:|
| CFO | -4.051.046.844.037 | -5.061.133.441.373 | **+1.010.086.597.336** |
| CFI | -29.454.293.791 | -13.790.864.563 | **-15.663.429.228** |
| CFF | +6.585.250.814.265 | +5.145.670.000.000 | **+1.439.580.814.265** |
| Net cash change | +2.504.749.676.437 | +70.745.694.064 | **+2.434.003.982.373** |
| Cash opening | 887.614.356.666 | 887.614.356.666 | **958.360.050.730** |
| Cash ending | 3.392.364.033.103 | 958.360.050.730 | **3.392.364.033.103** |

All three CFO+CFI+CFF=net, opening+net=ending, and B01 company cash=B03 company ending, exact **0 VND** residual. Preserve original signs and same issuer scope. H1 AASC audit report has source-original cash not same as custody money.

## Next steps without asking
1. Confirm newest PR #143 financial CI and source CI SUCCESS, merge expected head, re-read main and checkpoint. **Do not** claim website production deployed without deploy validation.
2. Follow current sequence to next unverified ticker/period; don't reprocess previously verified VCK/VIX/VDS/VCI/VCB and SHS completed rows, instead advance to next newly missing period or next ticker from latest checkpoint. For unresolved variance append private `reports/financial-exception-queue.json`, NEVER list pending tickers/periods to user unless explicitly asked.
3. New sources signed BCTC from issuer/Vietstock/HNX/HOSE, respect original report scope, accounting laws/TT334/CTCK, exact VND, 0.1% accepted limited to immaterial line-vintage only (not bank cashflow section balances). Save checkpoint after each PASS.
