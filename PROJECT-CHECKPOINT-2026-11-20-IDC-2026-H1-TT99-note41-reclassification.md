# CHECKPOINT — IDC H1/2026 cash opening TT99 restatement source resolved — 20/11/2026

## Resume context
- Repo: `kiemtimem12345/solieutaichinh`, main prior `f1c542372b8616ab2cd17d5110e63d5149cefa1c`, PR #85 source diagnostic. Prior successful PRs #82/#83/#84 preserve all signed IDC consolidated 2025-Q1 through 2026-Q3 B01/B02/B03.
- User instructed continue, do not re-read completed periods. A quarter is not fully PASS if source, scope, unit or original cash bridge cannot be validated.

## Authoritative original now recovered
- 07/09/2026 HNX filing, IDICO 2026 reviewed consolidated H1 signed 27/08/2026, original 72-page VI PDF retrieved via BSC HNX archive:
  https://www.bsc.com.vn/News/NewsAttachedFile/1599258-1
- Filename per HNX disclosure: `IDC_2026.9.7_2931d0c_VI_BaoCaoTaiChinh_KiemToan_HN_T6.2026_s.pdf`.
- Original SHA256: `f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944`; 10,086,230 bytes, PDF 72 pages.
- Visual source page 10 (H1 B01): 2025 comparative opening cash + equivalents **553,943,475,131 VND**; page 17 (H1 B03): line 60 opening cash **553,943,475,131 VND**, line 70 closing cash 608,684,579,632; page 34 note 4 components initial opening: 11,422,258,523 cash + 67,138,991,311 bank + 475,382,225,297 equivalents.
- Source page 21 Note 3.1: 2026 first adoption of **Thông tư 99/2025/TT-BTC** and **Thông tư 43/2026/TT-BTC**; comparative figures reclassified and details disclosed in **Note 41**.
- Original source PDF page 71, Note 41 'PHÂN LOẠI DỮ LIỆU TƯƠNG ỨNG THEO HƯỚNG DẪN CỦA THÔNG TƯ 99' explicitly reconciles earlier period opening balances:
  - Cash equivalents **474,491,428,405 + 890,796,892 = 475,382,225,297 VND**.
  - Short-term held-to-maturity investments: 6,807,014,517,859 **+ 106,831,646,770** = 6,913,846,164,629 VND.
  - Other short-term receivables: 393,049,146,108 **- 107,722,443,662** = 285,326,702,446 VND.
  - Sum of the three reclassifications **0 VND**; no cash receipt.
  - Also inventory **+6,093,936,851,316**, long-term work in progress **-6,091,082,770,286**, investment property **-2,854,081,030**, net **0 VND**. This also explains large reclassification between B01 current and noncurrent assets.
- Conclusion: cash difference +890,796,892 is **explicit noncash opening cash equivalent reclassification** under TT99; not a Q2 financing/operating cash flow, not OCR, not 2025 FY audit contradiction.
- Original 2025 FY/Q4 and 2026 Q1 cash opening/closing **553,052,678,239 VND** remain true as *previous presentation version*. H1 revised comparative **553,943,475,131 VND** is true as *reclassified presentation*. Preserve both original vintages.

## Q2/2026 provisional bridge diagnosed at exact VND
- H1 2026 6M minus Q1 2026 3M source-level raw arithmetic, not yet approved for same-vintage standalone publication:
  - Q2 CFO -202,543,174,911 VND; CFI +480,833,384,534; CFF -471,228,735,423; net -192,938,525,800; FX +2,812,837.
  - Q1 original cash closing 800,729,495,703. Q2 reported H1 closing 608,684,579,632.
  - Raw bridge residual (Q1 ending + Q2 net + Q2 FX - H1 ending) **-890,796,892** VND.
  - Add *separate issuer-disclosed NONCASH opening reclassification* +890,796,892 VND => adjusted bridge **0 VND**.
- Crucial: **do not add this noncash reclassification to CFO/CFI/CFF, do not override original Q1 cash, and do not silently publish Q2 quarter values while Q1/2026 current-year B03 has not been re-presented under the H1 current-period basis**. Q2 standalone fields in `financials-IDC.json` remain null; provisional values archived in `source_validation` with the new exact-vintage evidence. All signed original B01/B02 and H1 B03 remain PASS. Q3/2026 standalone 9M-minus-6M unchanged and PASS.

## Implementation and checks
- PR #85 https://github.com/kiemtimem12345/solieutaichinh/pull/85 contains source downloader/rendered page audit, adds validated issuer Note41 fields to `data/financials-IDC.json` and `scripts/verify_idc_2026_h1_note41_reclassification.py` to global CI.
- New recorded identity checks: opening FY+noncash=H1 revised (0); current asset reclassification net 0; inventory/long-term net 0; Q2 quarterly cash bridge after **separately flagged noncash reclassification** 0. Compare specific original PDF SHA256 and original page numbers.
- Website production after previous PR #84 main commit `f1c5423`: GitHub read-only live smoke run **44567710214** PASS 45/45 original homepage HTML, JS, CSS, 41 JSON SHA256. Do not claim new PR #85 is deployed before merge and renewed smoke.
- After CI PASS merge PR #85; verify main source and website 45/45 (main data change triggers existing `verify-live-site.yml`). Save a new Library checkpoint, leave original data and website layout unchanged.

## Next source action
- Look for an issuer-signed revised Q1 2026 consolidated B03 with the TT99/TT43 presentation basis used in H1 2026; absent this, keep Q2 standalone deferred with explicit reason, no blind Q1 recast.
- Next processable pending ticker: PLX parent Q3 CFF source mismatch 87,654,015,000 VND remains quarantined, H1 reviewed same-scope still pending; VDS / GEG / GAS follow coverage audit. Do not redo already-PASS IDC quarters.
- Rules: original issuer/exchange BCTC only; VND exact accounting checks, normalized in triệu VND, negative signs preserved, no fabricated numbers; 2025-Q1 onward and max 20 quarters, <=0.01% tolerance, exact visual source gate and checkpoint on PASS.
