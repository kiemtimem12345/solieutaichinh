# CHECKPOINT — VIX 2025-Q4 signed original RIÊNG, 2026-11-21 (premerge)

## Source anchors — do not repeat PASS VIX Q1–Q3
- Production repo `kiemtimem12345/solieutaichinh` main; PR #103 last complete signed separate Q3/2025 (commit `5e59eff95778a996fed22d7eee9f0c0749fadd64`), all CI / website / Pages PASS.
- Original Q4 separate financials signed 12 Jan 2026:
  https://vixs.vn/wp-content/uploads/2026/01/20260112-VIX-Baocaotaichinh-Quy-4-2025.pdf
  **43 pages, 1,743,460 bytes, SHA256 `d5a6e87eeac220951bcbe35c5359940092f58e4080d40f94c6bbd2ab99717408`**. GitHub Actions full PDF recovery `44863016591` SUCCESS; issuer-signed scan B01 p8–11, off-B01 client money p11, B02 p13–15, B03 p16–17 reviewed visually. No accidental use of unrelated consolidated data.
- **Separate source vintage, NOT rewriting original Q4:** 10 Feb 2026 VIX corrected FY2025 self-prepared report:
  https://vixs.vn/wp-content/uploads/2026/02/20260210-VIX-Dinh-chinh-BCTC-NAM-2025-tu-lap-Phat-hanh-lai.pdf
  42 pages, 9,386,876 bytes SHA256 `74d89731ce8efbb393f5f94a39cec377d9031c8889568a49aaaa8176133e22d8`. Original FY2025 as published on 04 Feb code 312 loan line showed typo **1,332,000,000,000 VND** instead of **11,332,000,000,000 VND**, repaired; code311 and original signed Q4 12-Jan code312 already show **11,332,000,000,000 VND**. Other FY2025 self-prepared cells stated unchanged. This is not FY audited, nor a revision of Q4 original.
- User agreement: <=0.1% only after multiple-source agreement, not for wrong units, sign, quarter/YTD; all listed Q4 source identities EXACT 0 VND.

## Q4 source original (signed exact VND)

| Code / field | Original Q4 2025 signed |
|---|---:|
| B01 270 Assets | 34,167,047,236,850 |
| B01 300 Liabilities | 12,712,284,159,210 |
| B01 400 Equity | 21,454,763,077,640 |
| B01 Current | 34,112,186,395,621 |
| B01 Noncurrent | 54,860,841,229 |
| B01 Cash | 2,049,092,199,336 |
| B01 Short-term borrowings (not the FY typo) | 11,332,000,000,000 |
| B02 Quarter revenue | 2,101,485,787,083 |
| B02 Quarter operating expenses | 314,710,715,590 |
| B02 Quarter PBT | 1,601,368,040,701 |
| B02 Quarter total income tax | 314,657,117,481 |
| B02 Quarter PAT | 1,286,710,923,220 |
| B02 12M PAT | 5,410,022,178,202 |
| B03 12M CFO | -7,119,094,558,676 |
| B03 12M CFI | -12,341,070,000 |
| B03 12M CFF | 8,487,000,000,000 |
| B03 12M net | +1,355,564,371,324 |
| B03 12M opening/closing | 693,527,828,012 / 2,049,092,199,336 |
| Off-balance client cash code026 (NOT company B01 cash) | 3,020,481,537,835 |

Quarterly original cash must derive from original Q4 **12M minus signed Q3 9M same RIÊNG scope**:
- **Q4 standalone CFO +102,816,912,722; CFI -12,627,320,000; CFF +1,049,000,000,000; net +1,139,189,592,722; opening 909,902,606,614 and ending 2,049,092,199,336 VND**. Every CFO+CFI+CFF, source cash bridge and B01 cash matches zero VND difference.
- Original signed B02 12M revenue 8,279,145,384,688, pretax 6,717,012,326,793, net 5,410,022,178,202 VND equals verified 9M Q3 source plus original standalone Q4 to exact VND.
- EPS full-year 3,533 VND/share; Q4 quarter EPS cell **blank**; keep quarterly EPS NULL (not extrapolated). B01 company short term borrowings 11.332e12, customer money outside statement.
- PDF 17 source identities B01/B02/B03 exact VND 0; original Q4 no numerical tolerance exceptions.

## Implementation pending final QA
- Source ledger `reports/source-audits/VIX-2025Q4-original-B01-B02-B03-exact-vnd.json`, original PDF hash + erratum hash (no copyrighted full source checked into Git).
- `data/financials-VIX.json`: Q4 exact signed source fields converted to million VND, proper scope, provenance and standalone cash quarterization, no other VIX period touched.
- `scripts/verify_vix_2025q4_signed_original.py` checks 17 exact source identities, field exactness, original 9M+Q4=12M bridge, original signed Q4 vs FY self-filed correction distinction, quarantine customer cash and EPS. Includes two tamper-negative tests.
- `.github/workflows/validate.yml` now tests Q4 and previous Q3/Q1/Q2 plus other tickers.
- **Checkpoint written pre-PR merge.** Only say Q4 complete after financial CI branch + main PASS, postmerge site 45/45 exact SHA PASS and Pages PASS, save final merge SHA. Remain within VIX after Q4 to Q1/Q2/Q3 2026 unverified.
