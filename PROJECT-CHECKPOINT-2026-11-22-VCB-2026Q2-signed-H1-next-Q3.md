# CHECKPOINT — VCB consolidated issuer signed 2026Q2 H1 and quarter B04, 22 Nov 2026

Repository `kiemtimem12345/solieutaichinh`; PR #141 branch `work/vcb-2026q2-signed-H1-consolidated-20261122`, target main. **Do not mark as merged until CI PASS on newest head, merge and re-read main.** Already source-verified VCB Q1/2025–Q4/2025 PR #136–139 and 2026Q1 PR #140; don't reload completed periods. Only process 2025+ dashboard periods (FY2025 comparator from audited can be retained as opening source only), up to newest 20 periods.

## Source and reporting entity
- Signed VCB issuer original Q2 H1 consolidated `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCB_Baocaotaichinh_Q2_2026_Hopnhat.pdf` signed **30/07/2026**, 55 scanned pages, 6,028,106 bytes, SHA256 **`fb0bc8ebbad76c175e61f7c2a7b78ae67608623a8d715d5470a08dbac00ff223`** verified source Actions `45011853335` SUCCESS, visual artifact `14750210893` retained 1 day. Original B02/TCTD-HN consolidated balance pp7–8, B03/TCTD-HN Q2 direct and H1 earnings pp10–11, B04/TCTD-HN 6M cash pp12–13, reporting currency **triệu VND**, exact integer million source precision (do not claim 1 VND).
- Audit ledger `reports/source-audits/VCB-2026Q2-issuer-signed-H1-sixmonth-million-vnd.json`: **141 original source million-VND fields**, **40 recomputed source accounting identities zero**. QA `scripts/verify_vcb_2026q2_signed_original_H1.py` independently recomputes 40 source equations, 24 independent signed Q2 B03-direct vs H1-sixmonth minus verified Q1 source earnings fields (all zero million differences), Q2-only B04 6M−Q1 cashflow, 4 negative mutation tests. Mandatory added to `.github/workflows/validate.yml`.
- `data/financials-VCB.json`: only 2026Q2 row updated, other PASS untouched. The old provisional OCR mistakenly put H1 gross cash interest **67.450.619** as CFO, and capex **-680.065** as CFI. Correct source H1 consolidated B04: CFO **+130.996.443**, CFI **-645.581**; no CFF. Corporate bank cash-and-equivalents is different from B02 vault cash.
- Report H1 2026 B04 opening **541.688.802** is the same audited FY2025 source vintage as verified Q1 2026, **not** first-issued 2025 Q4 B04. Do not force previous editions across audit vintages to balance, do not reprocess signed periods.
- Private queue `reports/financial-exception-queue.json` is never displayed or enumerated proactively, including stock ticker lists, unless user specifically asks what remains. Continue sequentially without questions.

## Signed B02 bank consolidated balance at 30/06/2026, TRIỆU VND
| Field | Value |
|---|---:|
| Assets | 2.657.440.573 |
| Liabilities | 2.408.950.067 |
| Equity | 248.490.506 |
| Vault cash | 14.602.141 |
| Deposits with State Bank | 73.064.279 |
| Other interbank deposits and loans | 620.660.670 |
| Loans to bank customers net | 1.728.183.370 |
| Customer deposit liabilities | 1.728.820.567 |

## B03 direct Q2 and cumulative H1 2026, TRIỆU VND
| Field | Signed Q2 current | H1 signed 6M |
|---|---:|---:|
| Net interest income | 19.141.761 | 36.792.844 |
| Net service income | 859.682 | 1.803.097 |
| Total operating income (dashboard revenue) | **26.371.601** | 47.551.411 |
| Operating expenses | -8.449.251 | -15.333.306 |
| Pre-provision operating profit | 17.922.350 | 32.218.105 |
| Credit provision | -502.625 | -2.995.727 |
| Pretax profit | **17.419.725** | 29.222.378 |
| Corporate tax | 2.868.766 | 5.209.324 |
| PAT consolidated | **14.550.959** | 24.013.054 |
| PAT parent bank shareholders | 14.542.276 | 23.998.842 |

**24/24 Q2 direct source income figures = signed H1 6M minus signed Q1 3M, exact million VND.**

## Bank B04 cash exact Q2 2026, TRIỆU VND
| Field | Signed H1 six months | Signed Q1 | Standalone Q2 |
|---|---:|---:|---:|
| CFO | **+130.996.443** | +35.398.194 | **+95.598.249** |
| CFI | **-645.581** | -294.108 | **-351.473** |
| CFF | 0 | 0 | **0** |
| Bank net cash change | **+130.350.862** | +35.104.086 | **+95.246.776** |
| Company bank cash/equiv opening | 541.688.802 | 541.688.802 | **576.792.888** |
| Company bank cash/equiv closing | **672.039.664** | 576.792.888 | **672.039.664** |

H1 CFO+CFI+CFF=net; H1 opening+net=ending; Q2 CFO+CFI+CFF=net, Q2 opening+net=ending, all residual **0 million**. B04 bank cash 672.039.664 is different from B02 on-hand cash 14.602.141. No invented financing cash.

## Resume next, uninterrupted
1. Wait only for actual CI and original source workflow results of newest PR #141. Merge PR only on PASS, read back main `data/financials-VCB.json` and checkpoint before marking complete. Avoid claiming actual deployment without observed deployment.
2. Advance to VCB **2026Q3** signed consolidated issuer original. Inspect B02/B03/B04 9M, Q3 direct income and 9M minus source signed H1 B04 cash; preserve Q1/H1 audited vintage, unit million, bank reporting scope and signed cash signs. Source catalogue `https://finance.vietstock.vn/VCB/tai-tai-lieu.htm?doctype=1`; actual original PDF link must be verified rather than fabricated.
3. After VCB Q3, continue the next ticker in latest approved sequence, one at a time, never rerun previously verified PASS data, keep queued cases internal unless specifically asked.
