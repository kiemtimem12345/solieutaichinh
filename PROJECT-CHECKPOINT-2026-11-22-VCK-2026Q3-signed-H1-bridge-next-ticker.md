# CHECKPOINT — VCK 2026-Q3 original HOSE signed, 9M minus H1 reviewed, 22/11/2026

Repository: `kiemtimem12345/solieutaichinh`; PR **#135**, source-validation branch `work/vck-2026q3-HOSE-original-9M-reviewed-H1-20261122`, target `main`. This checkpoint is written after the signed source and accounting work. Do **not** declare merged/deployed until final CI success and main read.

## Rules applying to future processing
1. Process periods/tickers **sequentially**, no questions/confirmation between steps, resume newest verified checkpoint rather than stale prompt.
2. Exclude all 2024 records; preserve verified periods and never re-download already validated originals unless later error proven.
3. Company securities cash B01/B03 is **not broker client-custody cash**; issuer VPS has no required consolidated statements since divestment in Q1/2025. Don't label standalone as consolidated.
4. Check 9M-minus-6M company cashflow using exact VND and same-scope, same-vintage source. Allow signed source-level differences **up to newest user 0.1% tolerance** only if individually explained/recorded. Do not make balancing plugs.
5. All exception details and outstanding ticker/period lists stay in private `reports/financial-exception-queue.json`; **do not enumerate or display until user asks which tickers or periods remain**. Keep work moving to next quarter/ticker.

## Signed Q3 2026 source
- Issuer signed VPS report dated **19/10/2026**, published on HOSE 20/10/2026 at `https://staticfile.hsx.vn/Uploads/UploadDocuments/2505926/20261020%20-%20VCK%20-%20Bao%20cao%20tai%20chinh%20Quy%203.2026%20-%20signed.pdf`. Original official HOSE PDF rendered/inspected B01 B02 B03, including customer custody table.
- Confirmed signed original full PDF mirror `https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VCK_Baocaotaichinh_Q3_2026.pdf` verified GitHub source workflow **44969525235 SUCCESS**, 61 pages, **3,680,290 bytes**, SHA-256 **`faa3a568d8aac84e4104c234196355b985d4aa17417cb6adffe2fd4dc22dc7b6`**, artifact **14733320500**, selected page images retained one day. Don't assert mirror and HOSE URL bytewise identical; both have matching source statement content and page comparison.
- The HOSE source is **Công ty Cổ phần Chứng khoán VPS**, not similarly named pesticide issuer. B01 signed company statement, B02 quarter and 9M, B03 company 9M signed. Customer custody B03 separately recorded.
- Exact audit ledger `reports/source-audits/VCK-2026Q3-issuer-signed-9M-reviewed-H1-exact-vnd.json`: **89 original VND fields**, 38 formula checks; 36 zero VND, two signed source subcomponent-to-subtotal differences retained in private queue (0.0241% revenue, 0.000067% operating expense, both under 0.1% accepted threshold). Never alter signed subtotals or use sum-to-balance plugs.
- Verification regression `scripts/verify_vck_2026q3_signed_9m_h1.py`: 38 dynamic equations, 4 corruption negative controls and source hash proof, independent reviewed H1, client cash separation. Registered in `.github/workflows/validate.yml`.

## B01 B02 signed Q3 2026 (VND)
| Source item | Exact VND |
|---|---:|
| Total assets at 30/09 | 48.808.808.409.666 |
| Liabilities | 16.734.412.314.197 |
| Equity | 32.074.396.095.469 |
| Company cash at 30/09 | 4.409.472.183.292 |
| Q3 signed direct revenue | 2.076.361.607.668 |
| Q3 signed direct operating expense | 596.682.815.711 |
| Q3 profit before tax | 1.118.639.309.926 |
| Q3 income tax | 225.110.922.184 |
| Q3 profit after tax | 893.528.387.742 |
| Signed 9M revenue | 6.949.389.621.212 |
| Signed 9M profit after tax | 3.233.129.599.948 |
| Brokerage clients' cash (NOT company cash) | 12.833.629.335.057 |

## B03 VND quarter bridge (9M signed − reviewed 6M, verified)
| Cashflow | 9M Q3 source | 6M H1 reviewed source | Q3 standalone |
|---|---:|---:|---:|
| CFO | -1.871.642.954.652 | -2.969.984.185.501 | +1.098.341.230.849 |
| CFI | -183.759.495.068 | -66.449.390.863 | -117.310.104.205 |
| CFF | -2.216.115.680.004 | -2.284.931.680.002 | +68.815.999.998 |
| Net cash change | -4.271.518.129.724 | -5.321.365.256.366 | +1.049.847.126.642 |
| Cash opening for Q3 | | | 3.359.625.056.650 |
| Cash ending for Q3 | | | 4.409.472.183.292 |

Checks 9M CFO+CFI+CFF=net; Q3 CFO+CFI+CFF=Q3 net, Q3 cash opening+change=cash ending, B01 company cash=B03 company ending: **all residual 0 VND**.
- H1 source ledger from already source-verified `reports/source-audits/VCK-2026Q2-issuer-signed-original-and-Q1-quarter-vnd.json`, audited independent reviewed H1 Q2 corporate B03.
- Original B02 current-quarter source and 9M-minus-reviewed-6M cross-check exact zero for income statement primary subtotals; preserve tiny detail differences in source audit and private queue rather than rewriting source.

## Commit, CI and continuation
- Data `data/financials-VCK.json`: only 2026-Q3 row newly corrected with 89 exact VND source fields / 1,000,000, standalone quarter cash and 9M source, date/notes/metadata. Prior PASS 2025Q1, 2025Q3, 2025Q4, 2026Q1, 2026Q2 untouched; separately queued source version remains hidden.
- After CI on PR #135 PASS, merge PR and read main JSON/ledger and checkpoint. Do not mark website production deployment without actual deploy proof.
- Then follow **the next ticker in latest project-approved sequence**, one ticker/period at a time. Do not reprocess VCI 7/7 or VCK completed periods.
