# PROJECT CHECKPOINT — 21/11/2026: PLX signed parent B03 external blocker reconfirmed; VCI 2026Q3 signed source recovered

## Ordering / task rule
Requested user processing sequence: **PLX → VCI → VCK → 18 missing Q3 2026 → KBC/TCB/VPB/TCX/VND**.
Recheck actual completed tickers from checkpoints: MBB, VIX, GAS, VDS, GEG, IDC. Do not redo their already PASS periods.
Continue processing **VCI** next; PLX is source-correction dependent and must remain correctly flagged, NOT promoted to PASS.

## PLX Q3/2026 parent — held terminal manual review
Original signed parent B03 code40 prints 5,966,101,543,718 VND; signed six finance component sum = 6,053,755,558,718 VND. Unexplained 87,654,015,000 VND (1.4692% of printed code40) is far outside 0.1% rule. The original source on **Petrolimex own file server** was again found and code40 still printed unchanged. Investor-relations site shows original parent report; 02/11 explanatory letter 2779/PLX-TCKT does not explicitly address code40. No independent signed correction located in this search. Screenshots of issuer PDF from web timed out, original 39/39 screenshot verification and hashes were recorded at older checkpoint. No production financial data changed for PLX. NEW PATH: `PROJECT-CHECKPOINT-2026-11-21-PLX-parent-CFF-issuer-site-rechecked-advance-VCI.md`. Reopen only with issuer-signed correction.

## VCI Q3/2026 — source new progress
Original issuer signed HOSE 20/10/2026:
https://staticfile.hsx.vn/Uploads/UploadDocuments/2506191/20261020%20-%20VCI%20-%20BCTC%20Q3.2026%20va%20Giai%20trinh%20chenh%20lech%20loi%20nhuan.pdf

Source PDF original text tables + spot-check page screenshot B01 p3/B02 p8; note policy p17 states **“Công ty không có công ty con”**. Thus the issuer does not issue a separate formal **consolidated** report; its single entity is economically equivalent in reporting perimeter, not mislabeled as issuer-signed consolidated. The old source extraction failed for three attempts because it could not establish a consolidated label. Distinguish this from VIX separate/no-subsidiary acceptance: a single-company source can be accepted with explicit no-subs evidence.

New `reports/source-audits/VCI-2026Q3-issuer-HOSE-original-special-broker-no-subs-vnd.json` holds **64 source fields in exact VND strings**. Main financial JSON `data/financials-VCI.json` Q3 row now has 64 corresponding entries in **triệu VND**, source URL changed to original HOSE, signed no-subs classification added, source old failures retained for provenance. All previous six VCI period records unchanged. No misleading claims of full 48-page PDF visual review or a file hash: the original PDF bytes and B03 all-page screenshots could not be retrieved in this session, but issuer source text for B03 was available; B01/B02 have selected page screenshots.

### Selected source Q3 numeric checks (VND)
- B01 total assets **40,401,402,835,579**, liabilities **23,453,347,651,288**, equity **16,948,055,184,291**; exact balance 0.
- B02 Q3 revenue operating **1,304,683,609,187**, operating expenses **402,848,651,935**, PBT **426,808,479,055**, PAT **367,407,505,316**; 9M PAT **958,726,199,269**; all arithmetic identities exact.
- Broker B03 9M issuer company cash: CFO **−6,185,243,120,130**, CFI **−76,957,830,177**, CFF **+6,058,038,109,500**, net **−204,162,840,807**, cash opening **3,213,693,581,406**, ending **3,009,530,740,599**; zero VND residual.
- **Customer brokerage cash OUTSIDE issuer B01**: opening **3,009,844,681,587**, movement **+2,057,277,771,704**, closing **5,067,122,453,291**; do not mix with company cash. Source Note 2 policy requires this.
- Specialist securities regime TT210/2014, TT334/2016 and relevant guidance; don't map brokerage customer deposits to corporate liquidity.
- **Quarter-only Q3 CFO/CFI/CFF remain NULL** until H1 2026 signed same-entity B03 verified, then 9M−6M exact cash bridge.

### CI and next
- `scripts/verify_vci_2026q3_issuer_no_subs_source.py` verifies 64 rows, signed scope evidence, 16 exact VND statement/custody identities and negative controls.
- New workflow step `.github/workflows/validate.yml` runs verifier with old independent PLX/GEG/IDC/etc tests.
- Wait for PR CI / merge and main CI; if failure, fix test and rerun before marking Q3 source step PASS.
- Then continue **VCI Q2/2026 signed original** to establish H1 B03 and Q3 standalone, followed by earlier VCI 2025+ signed sources. Do not switch to VCK until VCI ticker complete or genuinely externally blocked with checkpoint.
