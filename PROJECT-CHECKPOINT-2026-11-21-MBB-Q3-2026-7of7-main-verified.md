# CHECKPOINT — MBB Q3/2026 signed original verified, all 7 quarters Q1/2025–Q3/2026 COMPLETE (21 Nov 2026)

## Production PASS
- Production GitHub repo `kiemtimem12345/solieutaichinh`, main PR [#112](https://github.com/kiemtimem12345/solieutaichinh/pull/112) merged commit **`2de47613fa79da863d48d05fde64d35a322123c5`**.
- Finance CI PR `44871772598` **SUCCESS** (27 exact MBB Q3 original source B02a/B03a/B04a identities, five negative tests, 56/56 bank P&L checks all seven quarters; prior six unchanged).
- **Post-merge main finance CI** https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44871836608 **SUCCESS**.
- **Production HTTPS 45/45 SHA256** https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44871836618 **SUCCESS**.
- **GitHub Pages** https://github.com/kiemtimem12345/solieutaichinh/actions/runs/44871836525 **SUCCESS**.

## Signed 61-page source PDFs; currency signed = triệu VND
- Q3/2026 61p, 3,862,536B, SHA256 `bd5b2bad6c4c0669f16e9673c9a076d100fa6eb51bc7085bf66db89053d618ce`, issuer signed 20 Oct 2026, publicly filed 30 Oct: https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/MBB_Baocaotaichinh_Q3_2026_Hopnhat.pdf.
- Q2/2026 61p, 3,683,597B, SHA256 `a86757a4499953264ca22dd57ae2e3257057631107742e1d04ad1ecd0e2c23d1`, source https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/MBB_Baocaotaichinh_Q2_2026_Hopnhat.pdf?ver=8b5fd9ba.
- Full source GH recovery and original p3–4 bank balance B02a/TCTD-HN, p6 bank income B03a/TCTD-HN, p7–8 direct-method cash B04a/TCTD-HN evidence: run `44871203134`, artifact `14693223647`. No mixing with industrial B01/B02/B03 or bank separate statements.

## Signed exact 2026 Q3 million VND
| Item | Q3 original |
|---|---:|
| B02a assets / liabilities / equity | 1,837,857,452 / 1,673,715,844 / 164,141,608 |
| B03a quarter operating income / pretax / PAT / parent PAT | 21,091,443 / 10,330,100 / 8,251,873 / 8,039,497 |
| B04a standalone Q3 CFO / CFI / CFF | -12,063,094 / -789,880 / +5,047,866 |
| B04a Q3 net cash / beginning / ending | -7,805,108 / 187,350,187 / 179,545,079 |

B04a original Q2 H1 CFO -53,201,811 CFI -731,882 CFF 2,023,891 net -51,909,802, begin 239,259,989 end 187,350,187. Q3 original 9M CFO -65,264,905 CFI -1,521,762 CFF 7,071,757 net -59,714,910 begin 239,259,989 end 179,545,079. Q3 standalone = signed 9M − same-scope signed H1; cash start and end exact; net and component identities all zero million VND. Reported 9M net profit 24,400,066 equals Q1+Q2+Q3 signed quarter PAT; EPS current quarter blank (NULL), 9M EPS 2,563 VND/share.

Code source ledger `reports/source-audits/MBB-2026Q3-signed-consolidated-B02a-B03a-B04a-million-vnd.json`, new data row only in `data/financials-MBB.json`, validation `scripts/verify_mbb_2026q3_signed_original.py`, seven period bank income `scripts/verify_mbb_income.py`. No previous six quarter data changed. 0.1% allowance not used.

## Remaining blocked source caveats; do not redo PASS
- PLX Q3/2026 **parent B03 printed financing CFF error** 87,654,015,000 VND =1.4692% >0.1%, original Petrolimex and Vietstock scanned pages all 39/39 identical; terminal manual review until authenticated issuer correction. PLX Q3 consolidated + parent B01/B02 PASS.
- GEG Q2/2026 **standalone B03** opening cash equivalent reclassification 11,422,218,903 VND into bank guarantee deposits code165 in later signed note11 confirmed; Q1 note5 original p22 does not disclose restricted bank deposits as of 31 March; quarter cash fields must remain NULL. GEG Q1/Q2 sources and other quarters PASS.
- IDC Q2/2026 **standalone B03** opening noncash reclassification +890,796,892 VND signed H1 Note41 TT99, but Q1 original signed TT99 and H1 reviewed consolidated TT43 and 2025 comparative cash-flow reclass 5 rows net zero; 2026 Q1 same reporting-basis restatement not yet signed-source verified, retain quarter CFO/CFI/CFF NULL. IDC Q3 standalone PASS.
- VIX, GAS, VDS, MBB in-scope seven quarters source-verified; no reprocessing unless authenticated amendment directly contradicts prior source.
- Resume: run current 32×7 quarter coverage audit; prioritize a genuinely missing other ticker/quarter, while leaving existing blocked source-unavailable tasks in manual review. Maintain signed original VND versus stored million VND, scope, accounting model, cash signs, and quarter-vs-YTD. Checkpoint after each ticker period.
