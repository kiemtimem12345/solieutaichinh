# CHECKPOINT — GEG hợp nhất Q3/2025 từ PDF gốc, hoàn thành dòng tiền riêng Q4/2025 (19/11/2026)

## Chỉ đọc điểm dừng mới nhất
- VDS 7/7 kỳ hợp nhất 2025Q1–2026Q3 đã PASS và giữ nguyên; GEG 2026Q3 hợp nhất & công ty mẹ PASS, GEG 2026Q1 gốc 90 trường PR #70 PASS, 2026Q2 gốc 101 trường PR #69 PASS. Không reprocess các kỳ đạt chuẩn.
- GEG 2025Q4 original đã được xác minh 96 trường và 29 identity chính xác đến VND trong PR #71 merge `62a0145c6fc0c47fdf902018be1a5c7b6e75caa5`, checkpoint `PROJECT-CHECKPOINT-2026-11-19-GEG-2025Q4-original-and-opening-cash-vintage.md`.
- Hostinger staging bug từ ZIP 18/11 đã khắc phục PR #72 merge `bdb85cb78c729765bcee440cb8ee32886967cf70`; staged 41 tracked JSON source, SHA byte-equal. Website vẫn có thể lag GitHub JSON, tuyệt đối không claim 45/45 khi không có run thành công.

## GEG 2025Q3 original signed consolidated source
- Original HOSE-published GEG PDF hosted unchanged by Vietstock `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/GEG_Baocaotaichinh_Q3_2025_Hopnhat.pdf`.
- 83 pages, signed **28/10/2025**, source pages visually reviewed **PDF p5 B01 assets**, **p6 B01 liabilities/equity**, **p7 B02 quarterly and 9M**, **p8 B03 9M**, **p9 B03 closing cash**. Original 30 Oct 2025 issuer management explanation independently describes Q3 consolidated net profit about 80.06bn. Report source amounts VND, JSON normalized `triệu VND` except EPS.
- Source PDF hash unknown (not downloaded into local container); don't invent SHA. Page screenshots + exact issuer accounting checks used; no OCR-only financial assertion.

## Source numbers GEG Q3/2025 (VND)
- **B01 30/09/2025**: assets **15,247,952,050,819**, liabilities **8,674,761,966,494**, equity **6,573,190,084,325**; parent equity **5,008,341,099,594**, NCI equity **1,564,848,984,731**. Corporate cash **406,053,297,053** VND; distinct from any funds held on behalf of customers.
- **B02 standalone Q3/Năm nay**: revenue **671,328,091,438**, COGS **348,638,552,595**, gross **322,689,538,843**, pretax **98,726,289,378**, current tax **18,340,054,977**, deferred **323,314,089**, after-tax consolidated **80,062,920,312**, parent net **74,645,813,663**, NCI **5,417,106,649** VND. EPS basic/diluted **198 VND/share**.
- **B02 9M cumulative**: revenue **2,408,423,088,592**, PBT **888,112,383,635**, net **850,723,788,298**, parent net **618,707,408,600** VND.
- **B03 9M 2025 cumulative**: CFO **+856,209,015,015**, CFI **+244,031,897,120**, CFF **-857,979,656,903**, net **+242,261,255,232**. FY beginning cash **163,717,707,072**, FX **+74,334,749**, ending **406,053,297,053** VND; balance bridge exact.
- **96 source fields**, 29 original signed B01/B02/B03 numeric identities residual **0 VND**.
- Original GEG 2025Q3 period-only CFO/CFI/CFF **not yet computed**, because original Q2 2025 H1 B03 remains old auto unverified, pending next step.

## GEG Q4/2025 standalone cash from FY 12M minus original Q3 9M
| B03 (VND) | FY2025/12M original | 2025Q3/9M original | Q4 standalone exact |
|---|---:|---:|---:|
| CFO | +932,884,327,033 | +856,209,015,015 | **+76,675,312,018** |
| CFI | +1,921,143,888 | +244,031,897,120 | **-242,110,753,232** |
| CFF | -1,012,240,268,026 | -857,979,656,903 | **-154,260,611,123** |
| Net change | -77,434,797,105 | +242,261,255,232 | **-319,696,052,337** |
| FX | +81,753,281 | +74,334,749 | +7,418,532 |
| Corporate cash opening Q4 | — | 406,053,297,053 | 406,053,297,053 |
| Corporate cash closing Q4 | 86,364,663,248 | — | 86,364,663,248 |

- Exact Q4 bridge: 406,053,297,053 -319,696,052,337 +7,418,532 = **86,364,663,248** VND, zero residual.
- Capex standalone Q4 **-288,511,522,757 VND** (FY -408,566,559,815 minus 9M -120,055,037,058).
- Independently, **18** B02 source FY2025-minus-Q3/9M comparisons reproduce original Q4 *standalone* B02 exactly (revenue 590,444,253,989, net 96,055,064,822, etc). Residual 0 VND.
- Status 2025Q4 upgrades to `issuer_signed_original_visual_verified_B01_B02_B03_FY_and_Q4_standalone_cash`, 103 source/derived fields. Original FY cumulative B03 unchanged; no multiplication or unit confusion.

## Changed files and tests
- `data/financials-GEG.json` updates only 2025Q3 and 2025Q4: archives old auto Q3 values in prior/rejected metadata, populates FY-minus-9M standalone Q4. GEG 2026 previously PASS original figures unchanged.
- `scripts/verify_geg_q3_2025_original.py` asserts 29 exact-VND Q3 source identities, Q4 standalone 3 cash identities and 18 B02 12M–9M crosschecks.
- `scripts/verify_geg_q4_2025_original.py` updated to require FY/9M standalone Q4 CFO/CFI/CFF, source hashes unknown but URLs preserved; `.github/workflows/validate.yml` new CI gate.
- Merge only on CI PASS, verify HTTPS production JSON SHA after successful sync; do not claim deployment success from CI alone.

## Remaining priority
1. GEG consolidated **2025Q2 signed original H1 B01/B02/B03**, then derive standalone 2025Q3 B03 from 9M–6M, and 2025Q1 original to derive Q2 standalone. Preserve 2026Q3 two scopes PASS.
2. Review full FY2025 audited and H1 2026 reviewed original notes for the 11,422,218,903 VND **cash equivalents** initial comparator discrepancy. Already isolated: original 2025Q4/2026Q1 cash-only 46,702,358,323 unchanged; equivalents original 39,662,304,925 versus Q2 comparator 28,240,086,022 (difference 11,422,218,903). Causes/transfer destination unproven.
3. IDC 2026Q3 after GEG source periods. GAS H1 2026 cost of goods discrepancy 10,160,150,278 VND and PLX parent Q3 2026 cash CFF discrepancy 87,654,015,000 VND remain separate open checkpoints.
4. Rules: >=2025Q1, max20 distinct quarters, tolerance <=0.01%, preserve original source vintages, avoid speculative values; save checkpoint after every validated ticker, no revisiting accepted periods.
