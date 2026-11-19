# CHECKPOINT — IDC consolidated Q3/2026 original report recovered, B01/B02/B03 29 exact-VND checks (19 Nov 2026)

## Starting point and no rework
- `main` after GEG source-verification 7/7 consolidated commit `a8f899d57dcc591c462f5f3e7db603e27c6bdd8f` has financial CI PASS `44535532371` and site SHA256 45/45 PASS `44535532376`.
- VDS already issuer-original verified consolidated 7/7 periods 2025Q1–2026Q3; **do not revisit** its completed quarters.
- IDC `data/financials-IDC.json` previously had only 2025Q1–2026Q2, mostly auto-extracted and visual QA pending. **2026-Q3 consolidated was absent**.
- Important: IDC signed Q3 PDF source scope must be explicitly **B01a-DN/HN, B02a-DN/HN, B03a-DN/HN**; do not copy separately reported company-parent Q3 into consolidated.

## Official original source retrieval
- HNX IDC disclosure: https://www.hnx.vn/vi-vn/cophieu-etfs/chi-tiet-chung-khoan-ny-IDC.html?_des_tab=1, "Báo cáo tài chính quý 3/2026" posted 02 Nov 2026, separate issuer company-parent posted 30 Oct 2026.
- Original issuer signed report dated **28 October 2026**, 70 PDF pages: BSC-hosted original https://www.bsc.com.vn/News/NewsAttachedFile/1632697-1 ; downloaded bytes **17,424,887**, SHA256 `dde75e3efe8a569a0d264b27f7d7a0d8a4edb4abdf22a56144e0847f2c8dc790`.
- Other BSC original English copy 70 pages SHA256 `d445c78a7ae7ad6aeb5363296dc5ad22b611bcd89274a3f2d4200228ed2b3554`. Both PDF hashes duplicated exactly by two entries in Vietstock-sourced ZIP downloaded from https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%203/IDC_Baocaotaichinh_Q3_2026_Hopnhat.zip ; archive bytes 30,595,278, SHA256 `1c01afa02529fff7d88b8a3a953e7b75dfb5307789b80d67af0193533d67e574`.
- HNX direct `https://owa.hnx.vn/ftp///cims/2026/10_W5/000000016989520_VI_BaoCaoTaiChinhHN_Q3_2026_signed.pdf` still errors `CERTIFICATE_VERIFY_FAILED` on GitHub ephemeral Linux runner; **do not disable TLS verification** or silently invent a source. BSC and hash-identical Vietstock original are grounded alternative.
- Read-only source-recovery GitHub Actions run `44536828720` PASS (artifact `14536542839`), original screenshot renderer run `44541188764` original signed PDF pages **8–11** B01, **12–13** B02, **14–15** B03 displayed and independently reviewed. The text layer had incorrect reading order, so **financial fields were read from images**, not OCR-only unsorted text. PDF source unit VND.

## IDC Q3/2026 consolidated — original exact VND
| Statement item | Q3 2026 standalone or period-end (VND) |
|---|---:|
| B01 total assets 30/09/2026 | 23,631,671,909,723 |
| B01 total liabilities | 14,273,143,387,664 |
| B01 equity | 9,358,528,522,059 |
| B01 current assets | 16,599,453,089,891 |
| B01 noncurrent assets | 7,032,218,819,832 |
| B01 corporate cash/equivalents | 469,934,018,621 |
| B02 standalone Q3 net revenue | 2,075,575,029,891 |
| B02 standalone Q3 cost of goods sold | 1,403,796,161,144 |
| B02 standalone Q3 pretax profit | 673,834,389,916 |
| B02 standalone Q3 after-tax profit | 540,374,922,785 |
| B02 standalone Q3 parent-attributable net | 492,839,952,222 |
| B02 standalone Q3 NCI profit | 47,534,970,563 |
| B02 EPS standalone Q3 | 1,181 VND/share |

- B02 **9M cumulative** separately preserved as `*_ytd`: revenue **5,831,589,049,869**, pretax **1,927,066,885,420**, consolidated net **1,541,615,910,123**, parent net **1,373,246,282,153** VND; 9M EPS 3,290 VND/share. Do not substitute 9M into Q3-only income columns.
- B03 **9M cumulative**: CFO **+211,600,221,432**, CFI **+505,984,662,907**, CFF **-801,577,203,462**, net **-83,992,319,123**, beginning **553,943,475,131**, FX effect **-17,137,387**, ending **469,934,018,621** VND. B01 cash = B03 ending exact.
- 9M capex **-357,115,441,830** and financing dividends paid **-710,532,693,375** VND; B03 constituent-flow signs validated.
- Source image rows yield **105 numeric fields**, normalized to `triệu VND` except EPS, and **29 independent VND-level accounting identities all residual 0** across B01/B02 quarter, B02 9M, B03 9M constituent sums and cash bridges. ROA/ROE null until validated average denominators.
- **Q3-alone CFO/CFI/CFF intentionally null**: IDC 2026Q2 legacy record B03 H1 6M has not passed original visual QA. Cannot derive 9M-minus-6M from unverified text.

## Implementation
- `data/financials-IDC.json` adds a single `2026-Q3` consolidated snapshot, retaining 2025Q1–2026Q2 original rows unmodified and source/period cutoff >=2025Q1.
- `scripts/inspect_idc_q3_2026_pdf.py` & `.github/workflows/inspect-idc-q3-2026-pdf.yml`: bounded source fetch from BSC/Vietstock ZIP and independent SHA checks.
- `scripts/emit_idc_q3_2026_visual_jpeg.py` & `.github/workflows/visual-idc-q3-2026-pages.yml`: small hash-locked original screenshots to verify amounts despite malformed PDF text order; no production data write.
- `scripts/verify_idc_q3_2026_original.py`: assert original source PDF hash, 105 fields, 29 identities, scope, cashflow period basis, and absence of fabricated Q3-only CFO/CFI/CFF.
- `.github/workflows/validate.yml` includes new IDC Q3 source gate. Merge only **CI PASS**, verify website 45/45 HTTPS URL and byte-for-byte SHA256 when deployed.

## Resume instructions
1. Verify/merge IDC 2026Q3 PR when CI PASS; record production SHA after 45/45 site gate.
2. Continue **IDC 2026-Q2 consolidated original B03 H1** from previously linked Vietstock/issuer PDF, reconfirm period and unit; derive standalone Q3 CFO/CFI/CFF with **same-scope 9M-6M**. Only after H1 B03 original confirmed can remove cashflow-deferred flag.
3. IDC earlier 2026Q1/2025Q1–2025Q4 legacy auto-extracted rows remain incomplete; process one at a time from signed issuer PDFs, preserve raw amounts and reject misaligned OCR fields. Do not claim ticker fully done.
4. GEG source-vintage opening cash **11,422,218,903 VND** unresolved, GAS H1 2026 B02 cost re-presentation **10,160,150,278 VND**, PLX parent Q3 B03 component discrepancy **87,654,015,000 VND** remain separate source-vintage / blocked exceptions.
5. Principles: only Q1/2025 onwards, at most 20 report periods/ticker, <=0.01% tolerance except hard exact source checks, keep parent and consolidated separate, do not erase verified records, GitHub main only production source. Avoid guarded FTPS/SFTP overwrite of finance JSON with stale restore ZIP.
