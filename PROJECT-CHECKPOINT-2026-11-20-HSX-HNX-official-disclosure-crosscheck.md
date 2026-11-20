# CHECKPOINT — HOSE (HSX) vs HNX: source exchange independent cross-check — 20/11/2026

## Baseline
- Main before this audit: `4d30c09d69b3158676a2a9b1f75f2b731efdfb27` (PR #88 GAS Q1–Q2 signed issuer originals visual QA PASS). Production smoke `44669469566` PASS 45/45 HTTPS SHA256.
- Never redo IDC or GAS 2025 periods already PASS; PLX Q3/2026 *consolidated* finished 111 source fields, 40 exact-VND checks (PR #87). PLX Q3/2026 *parent* B03 **BLOCKED** signed PDF CFF discrepancy 87,654,015,000 VND.

## Exchange-specific policy
- PLX (Petrolimex) and GAS (PV GAS) **listed HOSE**: Sở GDCK TP.HCM `hsx.vn` and signed document service `staticfile.hsx.vn` as exchange-original disclosure provenance. HNX filings for similarly named subsidiaries (e.g., PLC) cannot substitute issuer PLX/GAS.
- IDC (IDICO) **listed HNX**: official `https://www.hnx.vn/vi-vn/cophieu-etfs/chi-tiet-chung-khoan-ny-IDC.html?_des_tab=1`. HNX visible announcement rows **02/11/2026 08:55 Q3 consolidated**, **30/10/2026 17:08 Q3 parent**, **07/09/2026 13:35 H1 reviewed consolidated**, **28/08/2026 17:29 H1 parent**, **31/07/2026 16:37 Q2 consolidated**. Prior signed originals manually verified, no repeat. Official HNX listing confirms filing existence and scope/date, not exact PDF byte identity until direct exchange attachment fetched.
- Public HNX attached source example from previously validated repository: IDC Q3/2026 signed 2026 original PDF recovered via BSC HNX filing attachment `https://www.bsc.com.vn/News/NewsAttachedFile/1632697-1`; original SHA256 verified and stored under `data/financials-IDC.json`. No data rewrite.

## Independent official HOSE issuer disclosures for PLX
1. Signed parent and consolidated Q3 issuer 2779/PLX-TCKT dated 02/11/2026:
   `https://staticfile.hsx.vn/Uploads/UploadDocuments/2510766/20261102%20-%20PLX%20-%20Van%20ban%20giai%20trinh%20BCTC%20Quy%203%20nam%202026.pdf`.
   Official source exact Q3 PAT **parent 1,315,029,909,162 VND** and **consolidated 1,363,096,640,781 VND**; these values **identical VND** to the two distinct PLX Q3 records already verified. Q3 prior year parent 527,524,735,210; consolidated 705,970,238,434 VND. This **narrative explanation discusses profit, not B03 CFF source subtotal**. Do NOT use to lift parent B03 block.
2. Reviewed H1 issuer 2143/PLX-TCKT dated 28/08/2026:
   `https://staticfile.hsx.vn/Uploads/UploadDocuments/2493883/20260828%20-%20PLX%20-%20Giai%20trinh%20bao%20cao%20tai%20chinh%206%20thang%20nam%202026.pdf`.
   HOSE explanation shows H1/2026 PAT **parent 678,943 triệu VND**, **consolidated 2,389,769 triệu VND** (rounded in millions).
   Q3 original signed 9M consolidated PAT **3,752,865,949,549** minus Q3 consolidated PAT **1,363,096,640,781** = H1 **2,389,769,308,768 VND**. HOSE explanatory **2,389,769 triệu** = 2,389,769,000,000 VND; rounding residue **308,768 VND**, within a million-VND display roundoff and 0.01% project tolerance. Independent accounting and scope verification PASS.
3. Official HOSE original Q3 parent document locator confirmed via public disclosure entry `https://nmquan.vn/data/ma/PLX/cong-bo/245179923-bao-cao-tai-chinh-cong-ty-me-q3-nam-2026`:
   `https://staticfile.hsx.vn/Uploads/UploadDocuments/2510747/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20me%20Q3%20nam%202026.pdf`.
   Web source reports source PDF content length **14,241,486 bytes**, exceeding web PDF parser supported size. Previously visually verified **signed issuer-hosted** parent PDF has **14,198,075 bytes**, SHA256 `a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef`. Size difference **43,411 bytes** may be PDF packing/signature/revision, **NOT proof a number was changed**. Exact HOSE PDF pages and original issuer PDF must be compared visually before asserting any CFF correction or byte identity. Remains **UNVERIFIED**.
4. Official HOSE Q3 consolidated original:
   `https://staticfile.hsx.vn/Uploads/UploadDocuments/2510747/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Hop%20nhat%20Q3%20nam%202026.pdf`. Already verified issuer signed original via exact public Vietstock eDocument link, 36 pages SHA256 `e0b6cfd9463c211970d0172aa8d258b8983b84ea472d59e0a242aed9ddf5c587`. Do not assume byte identity with HOSE without full exchange download.
5. Same-scope H1 reviewed HOSE originals:
   - Parent `https://staticfile.hsx.vn/Uploads/UploadDocuments/2493840/20260828%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20me%206%20thang%20nam%202026%20sau%20soat%20xet.pdf`.
   - Consolidated `https://staticfile.hsx.vn/Uploads/UploadDocuments/2494321/20260828%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20hop%20nhat%206%20thang%20nam%202026%20sau%20soat%20xet.pdf`.
   - Existing original issuer PDF mirrors (KPMG reviewed) signed SHA256 separately verified; the exchange URL is a **locator**, direct HOSE bytes remain blocked or incomplete due timeouts and size limits.

## GAS exchange source boundaries
- GAS is HOSE-listed and has issuer original signed Q1/Q2 consolidated 2025 PDFs, visually checked in latest PR #88: Q1 PDF 76 pages SHA256 `b86f8fa9f26731955d41cff2866d68aa9f1fd8692a78ff25b228447a51710d15`, Q2 75 pages SHA256 `c21bc4e88e2ce3d8331fa518df619d50086de50feed8691e48f653b825a4f31d`.
- Direct **separately downloadable** HOSE-hosted GAS Q1/Q2 2025 PDFs not yet verified, so classify `HOSE-specific independent PDF bytes: pending`, not "PASS". Do not replace issuer signed originals or run the same already-PASS calculations.

## Changes and verification
- This PR updates **source_validation metadata only** for PLX parent and consolidated Q3, adding exact official HOSE issuer explanation URLs, proven scope/profit, H1 disclosure rounded-figure comparison, and pending direct official parent PDF byte comparison. No financial quantities, normalization, cashflow, or UI changes.
- Regression `scripts/verify_plx_hose_independent_disclosures.py` checks exact-VND issuer Q3 profit in both scopes, rounded H1 difference 308,768 VND, original official exchange source URLs, and retains original parent Q3 signed B03 87,654,015,000 VND quarantine. CI workflow `.github/workflows/validate.yml` must PASS before merge; live 45/45 SHA256 after merge.
- HNX IDC information is a source locator corroboration, not a need to reprocess completed ticker.
- Next source priority: obtain whole HOSE parent Q3 PDF at /2510747/ via permitted byte-range or a reliable official mirror to **visually compare CFF printed row40** with issuer-hosted signed original; search issuer/HOSE correction. If source remains inaccessible, leave B03 blocked; continue remaining GAS quarters and VDS/GEG without repetitions.
