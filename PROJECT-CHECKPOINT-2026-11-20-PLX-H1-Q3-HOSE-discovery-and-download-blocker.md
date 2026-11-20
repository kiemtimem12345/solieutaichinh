# CHECKPOINT — PLX 2026 H1 reviewed/Q3 consolidated exact HOSE source links, 20/11/2026

## Current protected state
- Production repository: `kiemtimem12345/solieutaichinh`, main base `0deae0df49ef850d43ae7312643bb82c8b29f55d` (PR #86 merged), post-merge website smoke `44588774101` **45/45 HTTP/SHA256** PASS.
- Q3/2026 PLX parent original signed PDF SHA256 `a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef` 39p: B01/B02 verified visually, **B03 issuer-printed financing line40 +5,966,101,543,718 VND contradicts six components +6,053,755,558,718 VND**, difference 87,654,015,000. Original signed image pages 7–8 visually checked. Still BLOCKED. Do not substitute computed amount into production.
- Consolidated PLX Q3/2026 still only issuer-disclosed Q3 after-tax profit **1,363,096,640,781 VND** as PASS; full consolidated B01/B02/B03 not source visual verified and not to be invented.
- IDC periods already PASS in prior checkpoints; do not rerun.

## NEW exact official HOSE document locators (links verified in public disclosure listing 20 Nov 2026)
1. **PLX consolidated Q3/2026, signed issuer original, disclosed 30 Oct 2026**:
   https://staticfile.hsx.vn/Uploads/UploadDocuments/2510747/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Hop%20nhat%20Q3%20nam%202026.pdf
   Linked via https://nmquan.vn/data/ma/PLX/cong-bo/245179924-bao-cao-tai-chinh-hop-nhat-q3-nam-2026
2. **PLX parent H1/2026 reviewed, disclosed 28 Aug 2026**:
   https://staticfile.hsx.vn/Uploads/UploadDocuments/2493840/20260828%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20me%206%20thang%20nam%202026%20sau%20soat%20xet.pdf
   Linked via https://nmquan.vn/data/ma/PLX/cong-bo/50884368-bao-cao-tai-chinh-cong-ty-me-6-thang-nam-2026-sau-soat-xet
3. **PLX consolidated H1/2026 reviewed, disclosed 28 Aug 2026**:
   https://staticfile.hsx.vn/Uploads/UploadDocuments/2494321/20260828%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20hop%20nhat%206%20thang%20nam%202026%20sau%20soat%20xet.pdf
   Linked via https://nmquan.vn/data/ma/PLX/cong-bo/52619791-bao-cao-tai-chinh-hop-nhat-6-thang-nam-2026-sau-soat-xet
- Listing URLs are verified, but **original PDF bytes for these new sources NOT recovered or visually inspected**. Do not misclassify link discovery as B01/B02/B03 source QA PASS.

## Reproducible source-delivery diagnostics
- Original issuer IR pages `www.petrolimex.com.vn/quan-he-nha-dau-tu.html`, `plx.petrolimex.com.vn`, `w.petrolimex.com.vn`: repeated GitHub curl **timeout after 28s, 0 bytes**.
- `https://www.petrolimex.com.vn/ndi/thong_tin_co_dong/` and `https://www.petrolimex.com.vn/nha-dau-tu.html` GET 200 but current HTML anchors do not contain direct target Q3/H1 source PDF.
- `https://finance.vietstock.vn/PLX/tai-tai-lieu.htm?doctype=1` accessible GET 200 (~241 KB) but documents table is loaded dynamically from `/bundles/company/document/jsx` and no direct target PDF appeared in initial HTML. Investigate this supported mirror path rather than invent a storage name.
- 2026 H1 parent HOSE PDF request returned HTTP 200 headers, declared 18,543,309 bytes, but GitHub download timed out after 28s with **only 80,618 bytes**. A prefix `%PDF` is NOT sufficient proof of full source. The extractor was corrected to **reject timeout/partial PDFs and never publish their SHA256 as original evidence**. Web tool rejects 18.5MB file as over size; container network cannot resolve staticfile.hsx.vn. This is a *delivery blocker*, not missing report.
- On GitHub workflow 44665240329, original three links from disclosure indexes were independently verified; ongoing diagnostic JS bundle can potentially reveal Vietstock's document API. Artifact 14597267647 contains issuer/vietstock HTML source and detection output, no complete original financial PDFs.
- Source discovery script `scripts/discover_plx_2026_h1_q3_ir_links.py` runs URLs concurrently using curl `--connect-timeout 10 --max-time 28`; workflow `.github/workflows/discover-plx-2026-h1-q3-ir-links.yml`. Do not automatically re-fetch slow PDF on every code change once confirmed accessible via listing.

## Working tree and checks
- This branch adds `data/financials-PLX.json` Q3 *consolidated* `source_validation.hose_source_links_discovered` with all three exact source links, scope and flags `issuer_pdf_bytes_recovered=false`, `issuer_pdf_visual_reviewed=false`, `cashflow_quarterization_allowed=false`; no amounts changed, no scope mixing. A regression in `scripts/verify_plx_issuer_q3.py` enforces links and that numeric fields beyond independently verified PAT remain absent.
- After source discovery results and CI success, merge PR and confirm live 45/45 HTTPS SHA. Save checkpoint to Library `/Projects/so-lieu`. Site UI unchanged.
- Next attempt: from verified Vietstock document list or official file.petrolimex service recover the same issuer original *complete signed PDF*, verify SHA256, visually review B01/B02/B03 and Q3 H1 cash bridge. Parent B03 original CFF error remains quarantined absent issuer correction. If paths still blocked, retain terminal manual-review status and move to next unprocessed GAS Q2/2025, then VDS/GEG according to global audit.

## Rules
One ticker at a time; no unverified numeric OCR, no zeroing blanks, 2025-Q1 onwards <=20 periods, correct parent vs consolidated, exactly preserve YTD vs quarter and signs, original source VND normalized to million VND, numerical tolerance <=0.01%, checkpoints after PASS.
