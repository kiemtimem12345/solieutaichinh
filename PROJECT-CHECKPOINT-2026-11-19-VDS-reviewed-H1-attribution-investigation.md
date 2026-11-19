# VDS H1/2025 reviewed report — attribution investigation checkpoint (2026-11-19)

## Baseline: main completed issuer quarters 7/7
- `data/financials-VDS.json` Q1/2025–Q3/2026 all seven consolidated quarter source originals verified for B01/B02/B03, with exact-VND accounting identity regression, Q2–Q4 2025 standalone B03 derived from successive source YTD. Last data PR #66 merged `0423fb7323a461e9c01a16574c8153cbda97f817`; read-only site smoke run `44518228001` confirmed 45/45 HTTPS URLs exactly match Git SHA-256 and main CI `44518227512` PASS.
- Merge checkpoint `PROJECT-CHECKPOINT-2026-11-19-VDS-2025Q1Q2-verified-and-quarterly-cash.md` commit `74f1321b2f063daff5bfdfb314048e7457a3c13b`. Do not repeat completed issuer source QA for each quarter.

## Original B02 2025 H1 parent/NCI difference is not parser error
- Q1 official B02 signed source PDF 28/04/2025 p13 standalone net attributable to parent `19,089,097,924` and NCI `-76,755,668` VND.
- Q2 official B02 signed source PDF 30/07/2025 p14 standalone net attributable to parent `-9,900,252,664` and NCI `-1,293,653,003` VND.
- Q1+Q2 parent standalone sum = `9,188,845,260`; H1 cumulative reported in original Q2 PDF p14 parent `8,071,151,977`. Difference cumulative minus quarterly sum **`-1,117,693,283` VND**. NCI H1 cumulative reported `-252,715,388` vs quarter sum `-1,370,408,671`, opposite difference `+1,117,693,283`. Consolidated H1 net `7,818,436,589` equals quarterly Q1+Q2 consolidated net exactly.
- Q3/2025 original issuer B02 9M cumulative parent `269,304,589,718` less Q3 standalone parent `261,233,437,741` reproduces the same H1 cumulative parent `8,071,151,977`; parent/NCI split persists into Q3.
- Original quarter sources cannot be altered or a delta assigned to Q1/Q2 without issuer-authenticated restatement. 2025 H1 quarter netting revenue and operating expense difference `-774,921` VND is separate, below 0.01% tolerance and offsets in profit.

## New official reviewed source
- VDS issuer report publication 13/08/2025: https://www.vdsc.com.vn/quan-he-co-dong/cong-bo-thong-tin/rong-viet-cong-bo-bao-cao-tai-chinh-rieng-bao-cao-tai-chinh-hop-nhat-va-bao-cao-ty-le-attc-ban-nien-2025-da-duoc-soat-xet-i921
- Issuer original 84 page **reviewed consolidated** PDF: https://www.vdsc.com.vn/data/api/app/file-storage/6d34c594-a07c-4fc9-88a1-08ddd9f82764/VDSC_Cong%20bo%20BCTC%20hop%20nhat%20ban%20nien%202025%20da%20soat%20xet.pdf?downloadFrom=ManagementDocument-921
- The web PDF original opened, but web screenshot returned timeout/conflict; container direct download failed. To avoid blocking, `scripts/inspect_vds_h1_2025_reviewed_pdf.py` and `.github/workflows/inspect-vds-h1-2025-reviewed.yml` run read-only from an ephemeral GitHub Actions runner, capture source SHA256/metadata, text as unverified aid, and original PNG images for visual inspection. On this work branch, run `44519001636`; do not claim the figures reconciled before visual confirmation.
- This is SOURCE-DISCOVERY / QA-only work. No canonical quarter or website data changed.

## Next decision
1. Inspect original reviewed H1 2025 B02 columns parent / noncontrolling profit and relevant notes of consolidation/reclassification; compare against original Q2 issuer and Q3 source 9M.
2. If reviewed H1 explicitly allocates the 1,117,693,283 VND difference to a quarter or explains it, save audited source-vintage values as provenance and implement an explicit adjustment policy only if consistent with original quarter source integrity.
3. Otherwise record `cross_period_parent_nci_attribution_unresolved` in validation and mark the seven original source quarter rows verified but harmonization exception open. Continue next ticker GEG historical Q1/2025→Q2/2026 after preserved checkpoint, do not redo GEG Q3/2026 both scopes verified.
4. GAS H1 2026 10,160,150,278 VND cost-of-goods quarterly/YTD mismatch, PLX Q3 parent cashflow financing 87,654,015,000 VND discrepancy remain separate open cases.


## Original reviewed H1 PDF visual QA result (19 Nov 2026)
- Original reviewed H1 consolidated VDS PDF **successfully retrieved on ephemeral GitHub runner**, source bytes **9,476,053**, 84 pages, SHA256 `75de6381cdb92812422c264f9d4729e69e5bf7c31c852b77d60c0052140ac57f`. Run `44519001636` PASS, PNG artifact `14527516340`.
- Source original PDF p20 B02 H1 revenue **349,950,141,337 VND**, operating expense **273,327,926,577**. Page 21 B02 H1 PBT **5,201,163,732**, tax income **2,617,272,857** (negative tax expense), consolidated net **7,818,436,589**, parent-attributable net **8,071,151,977**, noncontrolling net **-252,715,388** VND. Page 22 EPS **33 VND/share**. All visually inspected from original PNG, no OCR-only amounts accepted.
- **Reviewed H1 has exactly the same H1 cumulative parent/NCI figures as original Q2/2025 report**. Thus the 1,117,693,283 VND discrepancy between the original standalone Q1+Q2 parent/NCI splits and published H1 is reproducible across **original Q2, later reviewed H1, and Q3 9M less standalone Q3**. It is not explained by OCR or unit conversion, and the review does not identify which standalone quarter must be reallocated.
- `data/financials-VDS.json` 2025Q2 `source_validation.reviewed_h1_2025_consolidated_vintage` records reviewed original, source SHA, source YTD values, 10 exact-VND checks and explicit `no_quarterly_adjustment_without_issuer_evidence=true`. The original Q1/Q2 canonical financial figures remain unchanged.
- `scripts/verify_vds_h1_2025_reviewed_attribution.py` CI gate checks the owner/NCI exactly opposite +/-1,117,693,283 VND offset and consolidated net 0 residual; `.github/workflows/validate.yml` runs this on each snapshot update.
- **Final VDS classification:** `7/7 issuer_original_quarters_verified; cross_period_parent_nci_allocation_2025H1_unresolved`. A defensible *documented exception* has been established with all three original source vintages. Advance to **GEG historical periods** per user-approved order while preserving this exception and automatically investigate only when a new official issuer correction or note supplies a quarter-specific attribution.
