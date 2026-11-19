# CHECKPOINT — GAS audited FY2025 B03 and reviewed H1 2026 B01 versions — 19/11/2026

## Earlier verified progress
- Main production GAS 2025Q1–2025Q4 and 2026Q1–2026Q2 original B01/B02/B03 quarter snapshots remain verified; 2026Q3 parent and consolidated previously PASSED and must not be reprocessed.
- PR #52 merged GAS 2026Q1/Q2; PR #53 source PDF renderer for audited 2025/H1 reviewed 2026; PR #54 stored source vintage differences; PR #55 corrected temporary smoke failures due mismatched cache while Git deploy propagated.
- Original GAS 2025Q4 report and 2026Q2 report are still the sources of **standalone quarterly** figures. Audited 2025 and reviewed H1 2026 are subsequent, distinct **report versions**.

## Exact source evidence
- GAS FY2025 **audited report**, PV GAS official original, released 04/03/2026: https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14454&documentid=3253&moduleid=648&portalid=0
  - SHA256 `b1cfb676ad81cabb6a0ebcd4b9955f33c9644964ef894c985228694a2d5aef6c`, GitHub Actions run 44493346638 artifact 14514061182; original PDF scan pages 9–13 visually inspected.
- GAS H1/2026 **reviewed report**, PV GAS official original, published 14/08/2026: https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14606&documentid=3375&moduleid=648&portalid=0
  - SHA256 `a90c4b06b6fa67215ee83247c8f2ea7b5cf8bdba8cc968b226e52c55ce568886`, same run reviewed artifact 14512709329; PDF pages 8–12 visually inspected.

## New 2025 audited B03 comparison in data/financials-GAS.json source_validation.audit_version_comparison
| B03 (VND) | 2025 Q4 original 12M | FY2025 audited | Audited less original |
|---|---:|---:|---:|
| CFO | 13,378,374,377,362 | 13,040,237,870,138 | -338,136,507,224 |
| CFI | -6,718,543,866,192 | -6,468,619,501,015 | +249,924,365,177 |
| CFF | -5,352,162,410,986 | -5,264,541,765,224 | +87,620,645,762 |
| Net cash | 1,307,668,100,184 | 1,307,076,603,899 | -591,496,285 |
| FX | 816,750,433 | 1,408,246,718 | +591,496,285 |
| Beginning cash | 5,567,983,431,468 | 5,567,983,431,468 | 0 |
| Ending cash | 6,876,468,282,085 | 6,876,468,282,085 | 0 |
- Audited investment expenditures -2,314,735,009,692; original Q4 12M -2,330,869,042,369.
- Audited cash dividends -5,011,650,250,256; original Q4 12M -5,109,438,694,779.
- 6 independent exact-VND identity/delta checks = zero. Audited FY B02 annual revenue 135,129,055,328,395, PBT 14,359,435,183,859, net 11,571,631,226,008 VND **unchanged** from original Q4 annual totals. Original quarterly period values remain intact.

## Audited balance sheet and H1 reviewed class checks
- FY2025 audited B01 assets +36,686,243,114 VND versus Q4 B01; liabilities +36,686,243,113 VND, equity +1 VND; cash remains unchanged.
- Increase of FY2025 current assets +41,048,624,111 VND decomposes as short-term receivables +40,109,533,369, inventory +34,827,618,390, other current -33,888,527,648 VND; noncurrent assets -4,362,380,997 VND.
- H1 2026 reviewed B01 assets 102,853,960,066,179, liabilities 32,568,229,020,837, equity 70,285,731,045,342 VND; B01 class and current-asset component checks each residual 0.
- H1 reviewed B03 CFO 6,455,378,093,715; CFI -2,234,588,471,909; CFF -42,021,936,897; cash closing 11,055,638,145,352 VND. These are in the previous PR #54 metadata.
- H1 reviewed YTD pre-tax profit 11,207,899,960,622 VND and net 9,025,674,760,340 VND. Sum original Q1+Q2 quarterly pre-tax/net remains 10,160,150,278 VND lower. **No authoritative source attributes the delta to Q1 vs Q2**, so do not rewrite either stand-alone B02.

## Principles / next step
1. Keep source version metadata under `source_validation`; do not silently overwrite previously verified original quarterly statements by FY-audited/H1-reviewed values from a different vintage.
2. `scripts/verify_gas_reviewed_h1_versions.py` CI now validates additional audited B03 and reviewed H1 B01 classes, source-version identities and original observations.
3. Determine whether full audited 2025 and reviewed H1 2026 statement notes explicitly explain reclassification; if no allocation of 10.160bn to Q1/Q2, keep cross-quarter reconciliation as *open* with source notes, not fabricated corrections.
4. Keep GAS 2026Q3 both scopes PASS. After final GAS verification move in order VDS Q3/2026 → GEG historical gaps → IDC Q3/2026. PLX Q3 parent B03 87,654,015,000 VND unresolved and must not be released.
5. GitHub main is website production; CI + SHA/HTTPS 45/45 after merge; 2025-Q1 onward, at most 20 periods, tolerance <=0.01%, million VND except EPS.
