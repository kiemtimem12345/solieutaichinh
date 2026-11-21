# CHECKPOINT — VCI Q2/H1 2026 signed HOSE PDF recovery (21/11/2026)

## Location in sequence
User directed PLX -> VCI -> VCK -> missing Q3 tickers. PLX parent Q3 financing residual external issuer-correction blocker, checkpoint at `PROJECT-CHECKPOINT-2026-11-21-PLX-parent-CFF-issuer-site-rechecked-advance-VCI.md`. VCI Q3 64 signed-source B01 B02 B03 9M numbers were merged PR #119 (main commit `b0e6d524ae04988f9bbafb4e26ae12ec4102ac12`), CI, 41-JSON HTTPS smoke, Pages all SUCCESS. Do not redo verified VCI Q3 signed numbers.

## Q2/H1 official original sources identified, numbers NOT YET read
- **VCI Q2 2026 report**, HOSE publication 20/07/2026 (PDF HTTP Content-Length 17,064,259 bytes):
  https://staticfile.hsx.vn/Uploads/UploadDocuments/2480835/20260720%20-%20VCI%20-%20BCTC%20Q2.2026-CBTT.pdf
- **VCI reviewed H1 2026 report**, HOSE publication 13/08/2026 (PDF HTTP Content-Length 15,650,240 bytes):
  https://staticfile.hsx.vn/Uploads/UploadDocuments/2488911/20260813%20-%20VCI%20-%20BCTC%206T%20nam%202026%20-%20CBTT.pdf
- Alternate Vietstock Q2 mirrored PDF:
  https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCI_Baocaotaichinh_Q2_2026_1.pdf
- Another issuer IR site `https://www.vietcap.com.vn/quan-he-co-dong/bao-cao-tai-chinh-sau-thang-dau-nam-2026`, direct CMS file link observed redirecting to maintenance.

The interactive web PDF reader confirmed size errors on both HOSE originals and cannot parse the PDF directly. This proves URL existence/source response size, **NOT the PDF content, hash or accounting numbers**. Do not fabricate Q2 numeric fields or derive Q3 independent quarter CFO/CFI/CFF from third-party rounded feeds.

## New source-only GitHub worker
Branch `work/vci-h1-2026-signed-PDF-source-recovery`:
- `scripts/inspect_vci_2026h1_signed_pdf_sources.py`: download signed PDF originals to disposable runner temp directory, verify PDF magic, SHA256 and page count, extract only cashflow headings/text, log short source excerpts. No PDF binaries committed, no financial production cells changed.
- `.github/workflows/inspect-vci-2026h1-original.yml`: run only on investigation branch via push or manual dispatch; installs poppler-utils.
- First run **`44914776784`**, job `136877918125`, Python syntax and poppler setup success; source-retrieval step was **still in progress** at checkpoint creation. DO NOT claim source retrieved or run success without reading completion log.
- If source inaccessible: record source-specific HTTP/timeout, avoid excessive retries or a misleading "pass". If retrieved: confirm same-company/specialist securities scope, B03 6M CFO/CFI/CFF/net/open/end, accounting policy, note no subsidiaries; compare 9M Q3 original signed current period, only publish Q3 standalone on exact VND cash bridge. Then process all earlier VCI Q1/2025–Q2/2026 one at a time and leave VCK for after VCI.

## Safety and scope
VCI issuer signed Q3 note "Công ty không có công ty con", so its single-entity specialist brokerage report is economically equivalent to group perimeter but **not** a formally issued consolidated PDF. Never call it an issuer-signed consolidated report. Brokerage customer custody cash must not be added into company B01 cash. Signed Q3 9M had zero residual in own B03 and 64 mapped fields PR #119; only Q3 standalone deferred. Existing GEG/IDC, VIX, GAS, VDS, MBB source PASSES untouched.
