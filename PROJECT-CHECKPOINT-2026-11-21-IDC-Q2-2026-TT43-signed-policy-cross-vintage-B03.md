# CHECKPOINT — IDC 2026-Q2 Q1 vs reviewed H1 TT99/TT43 signed current-period B03 comparability (21 Nov 2026)

## Unchanged financial values and source work
IDC consolidated 2025-Q1 through 2026-Q3 original signed B01/B02/B03 is already verified at the statements' original current period. Standalone Q3 2026 9M-minus-6M B03 0-VND bridge PASS, **do not redo**. Q2 2026 quarter-only B03 CFO/CFI/CFF remains NULL because original 3M and reviewed 6M reporting vintages differ: early 2026 original B03 cash beginning 553,052,678,239 versus reviewed H1 original 553,943,475,131, delta **+890,796,892 VND**. Signed H1 Note41 independently proves this is an opening **noncash restatement**; Q2 inferred CFO=-202,543,174,911, CFI=+480,833,384,534, CFF=-471,228,735,423 VND remains provisional, not site data. Raw quarter cash bridge -890,796,892 and adjusted bridge including separate noncash opening +890,796,892 equals 0; a valid arithmetic adjustment alone does **not** prove same-current-period policy and quarter revenue/cash B03.

## New signed source comparison
Original Q1 consolidated issuer PDF: https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%201/IDC_Baocaotaichinh_Q1_2026_Hopnhat.pdf — 66 pages SHA256 `229a1ff9af9d3e1bffd777a0c9b92b4bd5cbee5bc02765f02bee5778c2b2085b`.
- **Original Q1 B09-DN/HN PDF page17, section 2.5** explicitly says adopted TT99/2025 for financial period to 31/03/2026. It **does not declare TT43/2026** in that original note (absence is not a statement that the issuer violated law).
- Q1 current-period B03 p13/p14 already validated in prior checkpoint; no signed restated Q1 current-period TT43 B03 has been retrieved.

Reviewed H1 signed issuer filed HNX, original preserved at https://www.bsc.com.vn/News/NewsAttachedFile/1599258-1 — 72 pages SHA256 `f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944`.
- **Reviewed H1 B09a-DN/HN PDF page21, notes 3.1.1/3.1.2**: TT99/2025 and new **TT43/2026** consolidations policy formally adopted; 2025 comparative financial information re-presented with sources in note41.
- **H1 PDF page71 Note41**: B01 2025 opening cash equivalents +890,796,892 VND. **Five additional 2025 comparative B03 rows** presented as revised amounts: depreciation -141,514,712,612; inventory change -25,335,127,650; receivables change -331,959,067,818; interest paid -27,028,341,934; capex cash payment +525,837,250,014. Arithmetic sum of these five reclassifications **0 VND**. The table expressly labels this B03 as **prior period (kỳ trước)**, NOT 2026 current period.
- TT43/2026 signed 20/04/2026 revises TT202/2014 consolidated financial statement methods. MOF official description: https://www.mof.gov.vn/tin-tuc-tai-chinh/tin-chinh-sach-tai-chinh/quy-dinh-moi-ve-phuong-phap-lap-va-trinh-bay-bao-cao-tai-chinh-hop-nhat
- The two source PDFs were re-fetched and full-file SHA reverified by GitHub Actions `44870445628`, original page-image evidence artifact `14694155870` (27 selected Q1+H1 pages). No OCR necessary to validate notes.
- The known 2025 comparative B03 changes cannot be transferred into Q1 2026 or Q2 2026 actual cash. The revised H1 note does not itself provide a signed re-presented Q1 2026 B03/current-period line map. **Unresolved: same-current-period TT43 Q1 restatement**, not merely opening cash difference.

## Code changes only source evidence
- `reports/source-audits/IDC-2026Q1-vs-H1-TT43-source-policy-and-Note41-B03-comparatives.json`: signed sources, notes page refs, exact 2025 comparative B03 delta, no 2026 inference.
- `data/financials-IDC.json`: metadata only on 2026Q1/Q2 (TT43 evidence flags, Q2 source-comparison reason); no signed numeric source values modified, Q2 standalone cashflow remains NULL; signed source Q3 not touched.
- `scripts/verify_idc_q2_2026_tt43_signed_current_period_vintage.py`: signed evidence QA, source math and fail-closed no-quarter-cash check; `.github/workflows/validate.yml` includes regression.
- The 0.1% numeric tolerance not relevant to signed source policy/version or B03 closing cash, nor a legal-compliance certification.

## Next
After PR financial CI PASS and post-merge main CI / website 45/45 SHA / GitHub Pages PASS, leave IDC Q2 quarter-only B03 source version MANUAL REVIEW, with Q1 and H1 original data PASS and Q3 verified. Reopen when issuer publishes signed Q1 2026 consolidated B03 re-presented under TT43 or a detailed current 2026 cash-flow mapping Q1-to-H1. Advance to next objectively missing in-scope ticker/period, e.g. **MBB Q3 2026 consolidated** if not already confirmed, and preserve all previously completed ticker-period checkpoints.
