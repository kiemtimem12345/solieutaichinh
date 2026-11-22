# CHECKPOINT — VCB consolidated Q1/2025 signed original and corrected banking B04 — 22/11/2026

## Current position
- Repository `kiemtimem12345/solieutaichinh`, PR **#136**, branch `work/vcb-2025q1-consolidated-signed-source-20261122`, target main. Continue one ticker and one quarter at a time. Prior VCI complete and signed VCK periods validated, DO NOT reprocess. No 2024 data rows.
- Current VCB Q1/2025 banking signed source recovered and visually inspected. Final CI/merge needs PASS before declaring Q1 complete. Next processing VCB **2025-Q2** consolidated signed 6M report, calculate standalone Q2 B04 as signed H1 6M minus signed Q1 (same consolidated scope), then successive VCB quarters and next ticker in approved order.
- Source signed issuer Vietcombank original `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/VCB_Baocaotaichinh_Q1_2025_Hopnhat.pdf`, 53 pages, 14,951,723 bytes, SHA256 `f25bf036ad962541961817d80b49fba2119881d75cbf7abd5c98854a8fad5321`, issued/signed **29/04/2025**. GitHub Actions read-only source worker **44969925241 SUCCESS**, visual artifact **14733132694** has only 32 selected JPEG pages retained 1 day. PDF has no meaningful text layer, direct page-image review performed.
- **Important bank legal-form names:** B02/TCTD-HN balance statement pp4–5, off-balance p6, B03/TCTD-HN income pp7–8, B04/TCTD-HN cashflow pp9–10, in original **triệu VND**. Do not mistake source unit million for exact underlying one-VND precision. The dashboard stores integer million VND (converted 1e6 only for inter-report totals).
- `reports/source-audits/VCB-2025Q1-original-signed-consolidated-million-vnd.json`: **110 source fields** exactly as printed, **28 independently recomputable accounting identities** all 0 million VND residual. `scripts/verify_vcb_2025q1_consolidated_signed_original.py` checks 28 source equations, source SHA/page count, signed scope, unit, NCI, bank-specific B04, 4 negative controls.
- `.github/workflows/validate.yml` requires new QA. `data/financials-VCB.json` Q1/2025 only has original-source unit, correct B04 company cash (not cash-on-hand). All later VCB periods unchanged provisional.
- User's exception rule: `reports/financial-exception-queue.json` is **internal only**; never show or enumerate missing stock/quarter records or queued cases until explicitly asked; continue processing without requesting permission.

## Verified issuer original B02 balance Q1/2025 (TRIỆU VND)
| Item | Signed original |
|---|---:|
| Assets | 2.109.260.616 |
| Liabilities | 1.904.318.782 |
| Equity including noncontrolling | 204.941.834 |
| Vault cash on hand | 13.713.225 |
| Deposits at SBV | 28.020.997 |
| Deposits and loans to credit institutions | 410.587.576 |
| Net loans to customers | 1.433.896.493 |
| Securities investments | 176.979.243 |
| Customer deposits (bank liabilities) | 1.509.113.389 |

## Verified issuer original B03 income Q1/2025 (TRIỆU VND)
| Item | Signed original |
|---|---:|
| Interest income | 24.574.904 |
| Interest expense | -10.887.751 |
| Net interest income | 13.687.153 |
| Net service income | 805.964 |
| FX net gain | 2.023.940 |
| Total operating income (dashboard revenue) | 17.264.726 |
| Operating costs | -5.652.437 |
| Pre-provision operating profit | 11.612.289 |
| Credit provision | -752.356 |
| PBT | 10.859.933 |
| CIT total | 2.158.207 |
| PAT consolidated | 8.701.726 |
| Noncontrolling profit (signed negative allocation) | -5.497 |
| PAT attributable to parent | 8.696.229 |

## Verified B04 cash Q1/2025 (TRIỆU VND)
| Item | Signed source |
|---|---:|
| **CFO** | **-13.180.595** |
| **CFI** | **-174.898** |
| **CFF** | **0** |
| Net cash movement | -13.355.493 |
| Cash and equivalents beginning | 430.614.185 |
| Cash and equivalents closing | 417.258.692 |

**Major repair:** Previous OCR had CFO = +23,692,971 million, which is **just gross interest receipts**, not bank B04 aggregate CFO. It also incorrectly used CFI = -186,147 million (gross capex only) whereas signed investing section subtotal = -174,898 million. CFF zero explicitly from bank B04. Cash sections and bridge 0 million residual. B04 corporate cash+equivalents 417,258,692 million should NOT be equated to B02 on-hand vault cash 13,713,225 million; cash definition includes interbank equivalents.
- Q1 ROA and ROE calculations may use 31/12/2024 opening balance from the source **as comparators only**; never retain 2024 as an independent dashboard period. EPS issuer signed 1,041 VND per share.
- Only claim GitHub main/production status when actually verified; commit source and QA first, await PASS.

## Next sequential actions, no questions
1. Confirm CI source and financial tests PASS for PR #136 at newest SHA, merge PR, re-fetch main Q1 verified row and checkpoint.
2. Start **VCB consolidated 2025Q2 signed original** `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/VCB_Baocaotaichinh_Q2_2025_Hopnhat.pdf` (bank accounting source **triệu VND**, B02/B03/B04). Reconcile Q2 signed direct income vs 6M minus signed Q1; for B04 calculate cashflow Q2 as signed/reviewed 6M minus Q1, verify net and quarterly cash bridge exactly at printed source precision. Source hierarchy issuer/HOSE/Vietstock signed PDF, other providers only corroboration. Do not use previous auto-extraction values without original signed page verification.
3. Then Q3/Q4 2025 and Q1/Q2/Q3 2026 VCB, preserving each PASS checkpoint and private exception queue without pauses or user confirmation.
