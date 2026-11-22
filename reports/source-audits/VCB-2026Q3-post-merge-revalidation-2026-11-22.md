# VCB 2026-Q3 — Revalidation after consolidated publication

Checked 2026-11-22, repository `kiemtimem12345/solieutaichinh`, branch `main`.

## Evidence and scope
- Production data: `data/financials-VCB.json` Q3/2026, **consolidated**, million VND.
- Original signed-source audit: `reports/source-audits/VCB-2026Q3-original-signed-consolidated-9M-million-vnd.json` (PDF SHA-256 `9c69b62c629e7c4d586535c99277bbc6c4ba785d04ff765371fea07ece5daa08`, 66 pages, 2026-10-30).
- Prior H1 source ledger exists at `reports/source-audits/VCB-2026Q2-issuer-signed-H1-sixmonth-million-vnd.json`.
- This revalidation compared the existing repository's data and audit records. The signed PDF was **not downloaded or visually re-read in this session** because HOSE and Vietstock remote endpoints returned errors. Prior signed original PDF review and original source SHA are assertions supported by the repository source audit, not newly verified by download.

## Automated consistency checks in this session
- Source audit contains **148 numeric source fields**, all **148/148 exactly equal** to consolidated production Q3 JSON, zero mismatches.
- Source audit holds **43 recorded accounting residuals**; all 43 equal zero.
- Independently recomputed **11 accounting identities/bridges**, all equal exactly **0 million VND**:
  1. Balance: assets - liabilities - equity.
  2. Pre-tax: profit before provisions + provision expense - pretax profit.
  3. Post-tax: pretax profit - income tax - net profit.
  4. Cash 9M: CFO + CFI + CFF - net change.
  5. Cash 9M: opening + net change - ending.
  6. Cash Q3: CFO + CFI + CFF - net change.
  7. Cash Q3: opening + net change - ending.
  8. CFO Q3 = CFO 9M - CFO H1.
  9. CFI Q3 = CFI 9M - CFI H1.
  10. CFF Q3 = CFF 9M - CFF H1.
  11. Profit attributable = net profit + signed NCI adjustment.
- Quarter beginning cash **672,039,664** equals Q2 ending cash; quarter ending cash **618,002,538**, million VND.
- Q3 standalone cash flow (million VND): CFO **-49,547,933**, CFI **-729,139**, CFF **-3,760,054**, delta **-54,037,126**.
- Balance 30/09/2026: assets **2,682,408,935** = liabilities **2,428,647,789** + equity **253,761,146** million VND.
- Original audit reports direct Q3 B03 P&L matches 9M less H1 across 24 source fields; this session did not independently re-scan PDF.

## Restated comparative vintage (do not mutate existing 2025 records)
- The signed Q3 source audit states comparative 31/12/2025 assets **2,442,324,081** million VND; prior Q2 published vintage **2,442,279,166** million VND.
- Difference **+44,915 million VND** = **44.915 billion VND**; treat Q3 comparative as explicitly restated, keep both vintages attributed to source, not as an error in first published FY2025. See source audit notes and signed comparative disclosure.
- For quarter Q3 use only 2026 9M and 2026 H1 figures of the same consolidated scope.

## Result
- **PASS — repository data-to-audit consistency**, and prior original signed-source audit documents PASS.
- No production data change required, no duplicated `2026-Q3` row, no reprocessing already PASS periods.
- This is not evidence of deployment to Hostinger; live UI and server endpoints remain unconfirmed in this session.
