# Checkpoint — GEG / IDC H1 2026 reviewed sources: GitHub Actions recovery (21/11/2026)

## Resume target
Only unresolved quarterly standalone 2026-Q2 **consolidated** B03 for GEG and IDC. Existing Q1 and Q2 original signed B01/B02 and YTD B03 PASS; other 7/7 period source audits remain. No numbers or production JSON modified by this retrieval effort.

## Signed filing routes verified
GEG H1 2026 reviewed **consolidated**, HOSE filing date 25/08/2026:
`https://staticfile.hsx.vn/Uploads/UploadDocuments/2491976/20260825%20-%20GEG%20-%20Bao%20cao%20tai%20chinh%20hop%20nhat%20ban%20nien%20soat%20xet%202026%20%2B%20giai%20trinh.pdf`.
GEG separate:
`https://staticfile.hsx.vn/Uploads/UploadDocuments/2491976/20260825%20-%20GEG%20-%20Bao%20cao%20tai%20chinh%20rieng%20le%20ban%20nien%20soat%20xet%202026%20%2B%20giai%20trinh.pdf`.
IDC H1 2026 consolidated HNX filing date 07/09/2026:
`https://owa.hnx.vn/ftp///cims/2026/9_W1/000000016828159_VI_BaoCaoTaiChinh_KiemToan_HN_T6.2026_s.pdf`.
IDC BSC alternate signed source:
`https://www.bsc.com.vn/News/NewsAttachedFile/1599258-1`, previously SHA `f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944`.
HOSE/HNX PDF reader timed out; BSC returned octet-stream to web reader. Do NOT treat URL identification as signed page QA.

## New source-recovery branch, source-only
Branch `work/geg-idc-review-source-20261121` created from production main.
- `scripts/inspect_geg_idc_h1_2026_reviewed_retrieval.py`: attempts exact HOSE/HNX/BSC originals, validates `%PDF-` and SHA, uses `pdfinfo` and `pdftotext`, emits short source note excerpts only, no PDFs archived, no financial JSON writes.
- `.github/workflows/inspect-geg-idc-h1-2026-review.yml`: runs only on dedicated investigation branch pushes.
- First job `44884447439` FAILED environmental guard `poppler-utils missing` on Ubuntu 26 runner; no source bytes read. Fixed by adding `sudo apt-get install poppler-utils`, commit `48e6b0b82943ee7d2d923a9030354b150324f26b`.
- Second job `44884496727`: poppler setup + syntax PASS, source download/extraction was still running at last check.
- Third optimized source job `44884906277` on commit `472d2b680e3de7b0b68af7a40c1985b1c4ab6a6a`: changes expensive per-page pdf reopen to one whole-file `pdftotext`; running at last check.
- The last two runs were not completed at checkpoint time; inspect actual job conclusion and source log before claiming any PDF retrieved or source note verified. This status is intentionally **nonfinal** for retrieval, not financial data.

## Unresolved evidence gates
**GEG:** Q2 signed note11 year-opening bank guarantee reclassification `11,422,218,903 VND` verified. Q1 31/03/2026 restricted deposit balance or signed same-basis restated Q1 B03 still **not found**. Q2 standalone provisional cash bridge residual `-11,422,218,903 VND`; no cash quarter numbers promoted.
**IDC:** H1 signed policy note TT43 and Note41 reclassified *2025 comparative*, not signed 2026 Q1 current B03. Q1/H1 apparent opening cash mismatch `+890,796,892 VND`; no signed same-vintage 2026 Q1 quarter cash mapping found. Q2 standalone remains NULL.
Do not transfer the noncash or prior-period difference into CFO/CFI/CFF. No 0.1% tolerance for cash bridge.

## Next action
1. Read latest GitHub Actions run results `44884906277` first and `44884496727` if useful; inspect source identity, PDF hash/pages/notes.
2. If GEG original H1 binary recovered, inspect signed auditor report / note restricted deposits, 31 Mar balance, same-vintage Q1 B03. If no March figure, keep exception.
3. If IDC HNX or BSC source recovered, compare existing reviewed 72page SHA and note41; seek formal signed 2026 Q1 current-period restatement from issuer. Preserve original YTD.
4. Only then enable controlled quarterization and rerun existing `scripts/verify_reporting_regime_transitions.py` plus global CI, smoke test, Pages, checkpoint. Do not reprocess verified source periods.
