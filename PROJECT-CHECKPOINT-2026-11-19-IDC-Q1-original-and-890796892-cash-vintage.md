# CHECKPOINT — IDC hợp nhất Q1/2026 original 22 VND identities; Q1 vs H1 opening cash discrepancy — 19/11/2026

## Resume from latest production, do not reprocess verified quarters
- Main commit `d04a51fd104376a5e47f4321aa910929203233f5`, IDC 2026Q2 signed original and Q3 standalone verified from Q3 9M minus H1 6M, PR #77. Main CI `44544289584` PASS and site smoke `44544289617` 45/45 URLs SHA256 PASS.
- VDS 7/7, GEG 7/7, IDC Q3 original and IDC Q2 H1 original already source validated. **Do not reload prior validated data**, only source-version exceptions.
- IDC Q1/2026 original consolidated record was auto-extracted rounded to whole millions, EPS 902 from comparative column; prior auto ROA/ROE relied on unverified annualized average balances.

## Official original IDC Q1 2026 report and visual review
- Public HNX-linked original Vietnamese issuer-signed consolidated PDF: https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%201/IDC_Baocaotaichinh_Q1_2026_Hopnhat.pdf
- HNX disclosure on 06/05/2026; signed 28/04/2026. PDF 66 pages, 16,372,834 bytes, SHA256 `229a1ff9af9d3e1bffd777a0c9b92b4bd5cbee5bc02765f02bee5778c2b2085b`. Original visual render GitHub Actions `44544841284` PASS; actual PDF pages **8–11 B01-DN/HN, 12 B02-DN/HN, 13–14 B03-DN/HN** independently reviewed; web PDF viewer screenshot refused large source, GitHub ephemeral JPEG SHA-locked renderer succeeded.
- PDF is explicitly consolidated, not company-parent. Source unit VND; JSON normalizes to `triệu VND` except EPS in VND/share.
- `data/financials-IDC.json` 2026Q1 original **88 source and derived fields, 22 exact VND accounting identities all residual zero**.

## Correct Q1 issuer core (VND)
| Original source item | Q1 2026 |
|---|---:|
| B01 assets 31/03/2026 | 23,539,502,630,420 |
| B01 liabilities | 14,689,764,458,605 |
| B01 equity | 8,849,738,171,815 |
| B01 cash / equivalents ending | 800,729,495,703 |
| B02 standalone Q1 net revenue | 1,485,524,640,421 |
| B02 standalone Q1 pretax profit | 420,297,126,978 |
| B02 standalone Q1 net | 337,907,181,059 |
| B02 standalone Q1 parent attributable | 270,595,917,639 |
| B02 standalone Q1 EPS | **713 VND/share**, **NOT 902**; old 902 was prior-year comparison Q1/2025 |
| B03 CFO 3M/Q1 | +197,524,137,001 |
| B03 CFI 3M/Q1 | -68,608,251,477 |
| B03 CFF 3M/Q1 | +118,757,627,185 |
| B03 net change Q1 | +247,673,512,709 |
| B03 opening cash Q1 version | 553,052,678,239 |
| B03 FX effect Q1 | +3,304,755 |
| B03 ending cash Q1 | 800,729,495,703 |

- Q1 exact internal bridge: **553,052,678,239 + 247,673,512,709 + 3,304,755 = 800,729,495,703 VND**.
- Q1+original Q2 standalone **B02 revenue, pretax, consolidated net, parent-attributable net** each equal original H1 cumulative B02 exactly. This isolates the unresolved discrepancy to **B01/B03 opening cash source version** rather than income statements.

## Material unresolved cross-vintage 31/12/2025 Q1 vs H1 opening-cash discrepancy
| Source source version | VND |
|---|---:|
| IDC Q1/2026 original B01 comparative Dec 2025 and B03 initial cash | **553,052,678,239** |
| IDC H1/2026 original B01 comparative Dec 2025 and B03 initial cash | **553,943,475,131** |
| Difference H1 minus Q1 opening cash | **+890,796,892** |

- Both original B03s each reconcile internally exactly, same company consolidated scope; Q2 source's B01 2025 comparative **total assets stays the same 23,201,490,679,523 VND** while cash is reclassified. **No reliable issuer note allocating the difference to quarter Q2 has been confirmed yet.**
- Pure **arithmetic** (H1 YTD minus Q1 YTD, not a validated Q2 standalone cash bridge): CFO **-202,543,174,911**, CFI **+480,833,384,534**, CFF **-471,228,735,423**, total net **-192,938,525,800**, FX **+2,812,837**, Q1 ending **800,729,495,703** VND.
- These provisional sections add to net exactly, but opening Q1 cash + derived Q2 net + derived FX reaches **607,793,782,740 VND**, while H1/Q2 B01 ends at **608,684,579,632 VND**, leaving residual **-890,796,892 VND**. This mismatch precisely equals the opposite of the 31/12/2025 opening-cash source-version shift.
- Therefore **canonical `IDC 2026-Q2 operating_cash_flow/investing_cash_flow/financing_cash_flow/net_cash_change/cash_beginning/foreign_exchange_effect` remain `null`**, not silently fabricated. Provisional H1−Q1 section values stored only under `source_validation.q2_arithmetic_only_cash_flow_provisional_vnd`; `q2_cashflow_quarter_status` explicitly deferred, paired with `q2_cashflow_quarter_bridge_error_vnd=-890796892`. Q1 source and Q2 H1 source both remain unchanged.
- Q1 legacy *rounded* values, incorrect EPS 902 and unverified ROA/ROE are archived under `financial_line_items_prior_values`/`financial_line_items_rejected_values`, and ratio fields null.

## Implemented changes and quality gate
- `data/financials-IDC.json`: Q1 original exact B01/B02/B03 + Q2 cross-vintage metadata, **no changes to fully validated Q3** or any prior 2025 rows.
- `scripts/emit_idc_q1_2026_visual_jpeg.py` and `.github/workflows/visual-idc-q1-2026-pages.yml`: SHA-logged temporary original PDF imaging; read-only, no production writes.
- `scripts/verify_idc_q1_2026_original.py`: 22 exact source identities, Q1 EPS corrected, original hash and page QA, H1 income consistency, **strictly verifies nonzero -890,796,892 VND source-vintage Q2 cash bridge**, asserts canonical Q2 quarterly cash stays null; regression catches accidental override.
- `.github/workflows/validate.yml` includes exact VND source and exception gate; no UI changes.
- Merge only CI PASS and check website 45/45 HTTPS+SHA256. After merge append production run IDs to checkpoint.

## Next best steps
1. Investigate original audited FY2025 consolidated IDC closing-cash Dec 31 and H1/2026 notes about restatement `trình bày lại` or `phân loại lại` to identify source of **890,796,892 VND** comparative cash reclassification. If issuer note confirms treatment and Q2 stand-alone bridge can be built reliably, update Q2 canonical Q2 CFO/CFI/CFF *only with provenance and exact cash bridge*; else leave flagged open and continue validated quarters.
2. Continue **IDC consolidated 2025-Q4 → 2025-Q3 → 2025-Q2 → 2025-Q1** original issuer visuals; never mix 9M/FY cumulative B03 with standalone.
3. Other exceptions stay open: GEG cash comparator 11,422,218,903 VND; GAS H1 2026 B02 COGS quarterly allocation 10,160,150,278 VND; PLX Q3 parent B03 CFF constituent difference 87,654,015,000 VND.
4. Only periods Q1/2025 onward, max 20/ticker, exact VND checks, <=0.01% tolerance for acceptable comparison, keep issuer parent/consolidated and source vintages isolated, GitHub main source of production, no stale Hostinger restore ZIP.
