# CHECKPOINT — PLX Q1/2026 B01 original signed: source-confirmed opening cash reclassification; two source subtotals remain BLOCKED

Date: 2026-11-20 (ICT). Source original signed PLX consolidated Q1/2026, 29/04/2026, 36 pages, SHA256 158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f4bc5f9.
Production repository: kiemtimem12345/solieutaichinh. Previous checkpoint: PROJECT-CHECKPOINT-2026-11-20-PLX-2026Q1-signed-34-checks-B01-3-exceptions.md, PR #96; Q2 2026 original already separately completed. Do not redo the 34 source identities or unrelated ticker data.

## Signed-primary-source + official annual report, 0 VND reclassification bridge

Source Q1: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/PLX_Baocaotaichinh_Q1_2026_Hopnhat.pdf
- B01 PDF page 2: Q1 01/01/2026 comparative cash code 110 = 7,588,239,730,231 VND, other current assets code 160 = 4,283,789,584,061 VND, code 165 = 3,088,367,068,202 VND.
- **Note 16 original signed PDF page 21**: 01/01/2026 'Tiền gửi tại Quỹ Bình ổn giá' 3,087,558,817,574 VND, included in other current assets (code 165).
Official issuer 2025 audited B01: https://www.petrolimex.com.vn/~plxpublic/bctn-2025-baocaotaichinh.html
- 31/12/2025 audited cash code 110 = 10,675,798,547,805 VND, other current assets = 1,196,230,766,487 VND, 'other' component = 808,250,628 VND.

Exact independent bridges:
1. 10,675,798,547,805 - 7,588,239,730,231 = **3,087,558,817,574** VND.
2. 4,283,789,584,061 - 1,196,230,766,487 = **3,087,558,817,574** VND.
3. 3,088,367,068,202 - 808,250,628 = **3,087,558,817,574** VND.
4. Combined audited vs reclassified comparative (cash + other current assets) changes by exactly **0 VND**.
5. Source Q1 Note 16 price-stabilization-fund opening deposit **3,087,558,817,574 VND** exactly explains the destination.

**Conclusion:** B01 original 2026 opening cash is a presentation reclassification of funds at price-stabilization account, not Q1 operating, investing or financing cash flow. Keep both as-filed Q1 cash and FY2025 audited source versions, never overwrite one vintage with the other and never add to CFO/CFI/CFF.

## Two remaining B01 issuer-original subtotal discrepancies, no artificial PASS
- Short-term receivables B01 row 130 printed 19,662,068,640,316; line details total 19,652,984,670,130: +9,083,970,186 VND, **0.04620%**, exceeds 0.01%.
- Short-term liabilities B01 row 310 printed 76,146,303,967,243; listed line items total 76,137,215,001,801: +9,088,965,442 VND, **0.01194%**, exceeds 0.01%.
- Direct signed visual PDF p2 and p3 and source ledger confirm these are not solved by cash reclassification. Never allocate either amount to an invented detail row, never claim B01 component PASS without signed corrected disclosure / independent supporting evidence.
- The source retains high-level assets=liabilities+equity exact VND, and other original 34 identities 0 VND; source-reported figures remain intact.
- Status remains **B01 partial (two groups BLOCKED)**; B02/B03 exact-source PASS; cash comparative reclassification VERIFIED.
- For move-on gate: require both B01 residuals <=0.01% or formally documented issuer amendment correcting each source number. A test that confirms proper quarantine is a successful guard test, not a B01 financial PASS.

## Code changed on isolated branch
- reports/source-audits/PLX-2026Q1-consolidated-signed-original-vnd.txt: 7 exact source comparator values + signed Note16 source evidence.
- data/financials-PLX.json: source_validation now records confirmed Note16 destination and strict remaining B01 unresolved source flags; no top-level financial value modified.
- scripts/verify_plx_q1_2026_original.py: independent 0-VND reclassification checks and guard against false full-B01 PASS, still validates existing 34 checks and previous quarantines.
- CI workflow .github/workflows/validate.yml already invokes that verifier, no workflow modification required.
- CI / merge status: pending until explicitly verified; do not mark main deployed without the run's result.

## Resume gate
1. Verify GitHub Actions checks for PR branch, Python validator and full financial regression.
2. Search official issuer/HOSE documents for B01 issuer correction / 2026 Q1 explanations. If no official repair, leave two exceptions explicitly BLOCKED and do NOT proceed to another incomplete financial subsection under user's latest strict condition.
3. After full B01 PASS from properly supported numbers, save exact source+commit and only then proceed to the next incomplete PLX item; preserve all prior completed tickers.
