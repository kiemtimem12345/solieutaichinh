# CHECKPOINT — VCB 2026Q3 original consolidated 9M and standalone Q3 B04, 22/11/2026

**Repository** `kiemtimem12345/solieutaichinh`, PR #142, branch `work/vcb-2026q3-HOSE-signed-original-20261122`, target `main`. This checkpoint is pending final PR CI and main verification before marking merged. All earlier signed VCB 2025Q1–2026Q2 quarters PASS and must not be reloaded without later contradictory evidence. 2024 quarters excluded from all dashboards.

## Source
- Bank issuer signed 30/10/2026, official HOSE `https://staticfile.hsx.vn/Uploads/UploadDocuments/2510515/20261030%20-%20VCB%20-%20BCTC%20Hop%20nhat%20Q3%202026.pdf`. Independently downloaded original signed consolidated 9M filing via Vietstock `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VCB_Baocaotaichinh_Q3_2026_Hopnhat.pdf`, **66 scanned pages**, **9,988,936 bytes**, SHA256 **`9c69b62c629e7c4d586535c99277bbc6c4ba785d04ff765371fea07ece5daa08`** from source Actions **45012503358 SUCCESS**, artifact **14749929820** retained one day. B02a/TCTD-HN consolidated balance PDF pp16–17, B03a/TCTD-HN signed Q3 and 9M earnings pp19–20, B04a/TCTD-HN 9M bank cash pp21–22.
- Source reporting unit **triệu VND**, exact as printed integers. Preserve source entity as consolidated bank, not parent-only. Never use 1VND numerical precision claims on million-scaling sources. Do not confuse bank B04 bank cash/equiv vs B02 vault cash on hand.
- `reports/source-audits/VCB-2026Q3-original-signed-consolidated-9M-million-vnd.json` has **148 signed exact original million-VND cells**, **43 independently recomputed source account equations zero**, standalone Q3 B04 9M−verified H1 6M, and signed source FY2025 comparative. `scripts/verify_vcb_2026q3_signed_9m_h1.py` checks 43 fresh equations, 24 exact Q3 direct vs 9M-minus-6M earnings lines, four corrupted-source/data controls, bank cash 9M and Q3 zero residuals. CI is mandatory in `.github/workflows/validate.yml`.
- Data `data/financials-VCB.json`: append just 2026Q3 as seventh period, preserve earlier completed Q1/2025 to Q2/2026 rows. Source-signed status, 155 accepted fields. ROA/ROE remain null pending correct ratio methodology, do not invent. No 2024 row.

## Signed bank B02 at 30/09/2026 (TRIỆU VND)
| Field | Source |
|---|---:|
| Assets | **2.682.408.935** |
| Liabilities | 2.428.647.789 |
| Equity | 253.761.146 |
| Vault cash | 13.375.646 |
| Deposits at State Bank | 63.237.158 |
| Interbank deposits/loans | 582.805.066 |
| Customer loans net | 1.784.925.179 |
| Investment securities | 173.844.631 |
| Customer deposits liability | 1.781.703.044 |

## B03 Q3 current and 9M, TRIỆU VND
| Field | Q3 direct signed | 9M signed |
|---|---:|---:|
| Net interest income | 20.385.955 | 57.178.799 |
| Net service income | 904.260 | 2.707.357 |
| Total operating income | **25.431.117** | 72.982.528 |
| Operating expenses | -8.029.332 | -23.362.638 |
| Profit before credit provision | 17.401.785 | 49.619.890 |
| Credit provision | -6.184.109 | -9.179.836 |
| Pretax profit | **11.217.676** | 40.440.054 |
| CIT | 2.176.555 | 7.385.879 |
| Consolidated PAT | **9.041.121** | 33.054.175 |
| PAT attributable parent | 9.033.302 | 33.032.144 |

**24/24 current Q3 issuer B03 signed direct fields exactly equal signed 9M minus signed H1 2026 same-scope figures at million precision.** Q3 9M pretax and PAT exact; NCI separate.

## B04 9M, signed H1 and standalone Q3, TRIỆU VND
| Field | 9M signed | H1 signed | Q3 standalone |
|---|---:|---:|---:|
| CFO | **+81.448.510** | +130.996.443 | **-49.547.933** |
| CFI | **-1.374.720** | -645.581 | **-729.139** |
| CFF | **-3.760.054** | 0 | **-3.760.054** |
| Net change | **+76.313.736** | +130.350.862 | **-54.037.126** |
| Bank cash/equiv opening | 541.688.802 | 541.688.802 | **672.039.664** |
| Bank cash/equiv closing | **618.002.538** | 672.039.664 | **618.002.538** |

9M CFO+CFI+CFF=net; 9M opening+net=closing; standalone Q3 CFO+CFI+CFF=net and Q3 opening+net=closing, **0 million VND residual**. Signed B04 nine months **interest receipts +106.822.239 are not CFO +81.448.510**, and capex is not full CFI. Q3 CFF is signed cash dividends paid, not fabricated balancing outflow.

## Private source version comparison
The original Q3 B02 31/12/2025 comparator explicitly marked `trình bày lại` is not identical to the FY2025 audited comparison in issuer H1 2026. Preserve original 2025, audited H1, and Q3 re-presented vintages. Internal nonblocking evidence record `VCB-2026Q3-2025FY-comparative-trinh-bay-lai-vs-2026H1` in `reports/financial-exception-queue.json`. NEVER display queued ticker/period list to the user unless user explicitly asks. Do not change previously PASS quarters, do not use tolerance to plug cash.

## Next uninterrupted steps
1. Confirm latest PR #142 financial CI and source-run PASS, merge with correct expected head SHA, re-read main JSON, checkpoint and signed source audit; only then mark VCB 2026Q3 complete. Do not claim site production/deployment success without separate test.
2. VCB Q1/2025–Q3/2026 source series now covers seven quarters once merged. Proceed immediately to **next ticker per newest project queue/checkpoint**, one ticker at a time, avoiding already completed periods, and save PASS after each. Private exceptions remain silent, process rest of queue.
3. If later new FY2025 audit note clarifies comparative restatement, update private exception source ledger only, without redoing completed VCB source financial Q3 data.
