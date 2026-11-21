# CHECKPOINT — VCK/VPS Q3/2025 signed source passed (2026-11-22)

**Repository:** kiemtimem12345/solieutaichinh. **Priority:** VCK Q1/2025 already signed PASS PR #128; VCK Q2 evidence internally queued per PR #129, not displayed to user unless asked; now signed Q3 B01/B02/B03 verified. Next work VCK Q4/2025, then 2026Q1–Q3 sequentially.

## Exact original source
- VCK Q3 issuer VPS filing (VPSS former filing ID) Vietstock signed ZIP: `https://static2.vietstock.vn/data/OTC/2025/BCTC/VN/QUY%203/VPSS_Baocaotaichinh_Q3_2025.zip`
- ZIP SHA256 `1eb8c56340d1006d5818eaf69bb415c627ea5339c47c6e435404c0ef89cbfdf4`, 4,772,801 bytes.
- **Correct issuer-signed PDF ZIP member:** `VI_Baocaotaichinh_Quy 317604385128323NQH1ueK.pdf`, SHA256 `f266a63e92f12c97e84c34d93e549e94eb1b0e26cc40ba7c3002a4548efefd4f`, 2,235,421 bytes, 39 pages, statement signed 08/10/2025. Do NOT use `EN_ExplanationRelatingToFS` ZIP member instead. GitHub source workflow `44932687219` PASS, artifact 14718411957 has 24 visually inspected JPEG pages; text layer only 199 characters.
- Original PDF B01 pages5–6, B02 pages8–11, B03 company pages12–13, client brokerage cash separate page14. Independent readable mirror `https://financialfilings.com/filings/cong-ty-co-phan-chung-khoan-vps/interim-quarterly-report/2025/49186302/` matches original images/values.
- Reporting entity VPS Securities, company issuer standalone after sole subsidiary exited Q1/2025, **do not mislabel consolidated**.

## Source exact VND
- B01 total assets **39.177.958.193.814**, liabilities **25.250.632.229.751**, equity **13.927.325.964.063**, company cash end **8.678.251.634.326**.
- B02 Q3 operating revenue **2.708.413.906.220**, operating expenses **1.232.969.450.534**, PBT **1.394.617.853.844**, CIT **268.114.197.672**, PAT **1.126.503.656.172**.
- B02 9M cumulative revenue **5.900.410.398.681**, PBT **3.191.995.387.087**, PAT **2.564.405.682.766**; all 9M − EY audited H1 6M equal source Q3 current figures VND exact.
- B03 9M CFO **1.009.497.441.021**, CFI **-108.139.216.091**, CFF **6.044.751.583.047**, cash net **6.946.109.807.977**, cash open **1.732.141.826.349**, cash end **8.678.251.634.326**.
- EY audited VPS H1 B03 same accounting dividend classification as 9M: CFO **3.301.435.800.315**, CFI **-82.372.806.368**, CFF **202.716.749.534**, cash net **3.421.779.743.481**, cash end **5.153.921.569.830**.
- Q3 standalone from 9M−EY H1: CFO **-2.291.938.359.294**, CFI **-25.766.409.723**, CFF **+5.842.034.833.513**, net **+3.524.330.064.496**, cash open **5.153.921.569.830**, end **8.678.251.634.326**. All cash equations **0 VND residual**. Broker client money **30.168.163.229.832** separate.
- `reports/source-audits/VCK-2025Q3-VPS-original-signed-EY-H1-vnd.json`: original 63 signed VND fields, 25 exact identities. `scripts/verify_vck_2025q3_signed_original_ey_h1.py`: 3 negative tests, ensure Q2 pending numbers never published. `data/financials-VCK.json`: only 2025Q3 normalized million VND; other PASS unchanged.
- CI `.github/workflows/validate.yml` includes new Q3 verifier. Before merge confirm CI PASS and re-read main. No automatic repeat of prior PASS periods or 2024 data.

## Next steps
1. Finish CI/merge for current PR, main verification and checkpoint.
2. VCK **Q4/2025** signed ZIP `https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/VCK_Baocaotaichinh_Q4_2025.zip`, issuer FY2025 audited 31/01/2026 (VPS investor relations), determine different reporting vintages, calculate Q4 cash 12M−9M only if same scope/statement.
3. VCK Q1/2026, Q2/2026, Q3/2026, then next ticker. Exception queue internal only; no list displayed unless user requests.
