# CHECKPOINT — GEG Q1 2026 vs EY-reviewed H1 2026: four uploaded signed PDFs (21/11/2026)

## Four user-uploaded original PDFs inspected (read-only)
- Q1 2026 **consolidated**: `GEG_Baocaotaichinh_Q1_2026_Hopnhat.pdf`, 82 pages, SHA256 `d8dade2f270452432a190bedddb46736523cc3a74b783ae1a2f82b76a5e74d5b`. Exactly matches previously verified original original-Vietstock source and same Q1 B03; original 31 March cash and equivalents `105,856,793,049 VND`. B03 PDF pp9-10.
- Q1 2026 **parent/separate**: `GEG_Baocaotaichinh_Q1_2026_Congtyme.pdf`, 70 pages, SHA256 `5532ce20cf729600ed20cb7fcb326c9ac5af7deaa394a7d868da76a27aefc707`.
- H1 2026 **consolidated reviewed**: `GEG_Baocaotaichinh_6T_2026_Soatxet_Hopnhat.pdf`, 74 pages, SHA256 `c5fcba1374cea2e2fc6e82eb66ccd4cf49320bd4a412c4c3f834d60c16ba700e`. Contains EY H1 review, auditor signed 24 August 2026 (PDF pp9-10), issuer signed disclosure 25 August 2026, consolidated B01 pp11-13, B03 pp16-17, Note 3.1.2 TT43 p23, Note5 cash p35, Note22 restricted deposits p44, Note37 reclassification p73.
- H1 2026 **parent/separate reviewed**: `GEG_Baocaotaichinh_6T_2026_Soatxet_Congtyme.pdf`, 57 pages, SHA256 `3cd06d6acddd1fc23787e06e7cf9d7973e7809f9f4c0ba180704875d616ae495`, signed issuer 25 August, EY 24 August, B03 pp14-15. Do not merge parent with consolidated.

## NEW signed reviewed H1 source facts — exact VND
Signed reviewed consolidated B03 PDF pp16–17:
- CFO `707905751019` VND
- CFI `-734466295121` VND
- CFF `51927115815` VND
- H1 net increase `25366571713` VND
- H1 cash opening `74942444345` VND
- FX `13217270` VND
- Cash end `100322233328` VND (matches reviewed B01 p11 and Note5 p35)
- Entire B03 CFO+CFI+CFF = net; opening+net+FX=end exactly **0 VND residual**.

Previously validated original quarterly Q2 filing (same consolidated scope, **different signed source version**) currently in production:
- CFO `722160976132`, CFI `-732448267884`, CFF `35658808670`, net `25371516918`, opening `74942444345`, FX `13217270`, end `100327178533` VND.
- Reviewed-minus-original changes: CFO `-14255225113`, CFI `-2018027237`, CFF `+16268307145`, net and cash end `-4945205` VND. The signed reviewed version supersedes no financial values automatically; version migration must reconcile Q3 signed standalone B03 previously PASS.

## Signed TT99/TT43 evidence, critical distinction
- Reviewed consolidated **Note 3.1.2, PDF p23** explicitly says TT43/2026 adopted for 2026 consolidated financials, together with 2025 comparatives re-presented.
- Reviewed consolidated **Note37, PDF p73**, is titled “PHÂN LOẠI DỮ LIỆU TƯƠNG ỨNG THEO HƯỚNG DẪN CỦA THÔNG TƯ 99”. Original year-open cash and equivalents `86364663248` minus `11422218903` = reviewed year-open `74942444345` VND; code165 other current assets increases exactly `11422218903` VND. Note37 cashflow reclassification in remainder refers to **2025 comparative**, not newly signed 2026 Q1 line items.
- **Note22, PDF p44**: short-term other assets include deposits restricted by loan agreement/collateral and releasable upon terms. Reviewed B01 p11 shows code165 pledged restricted deposits `54079653068` at 30 June and `11422218903` at opening. There is NO signed amount on 31 March in those pages.
- Q1 signed original PDF does not report a separate March 31 pledged deposit balance and has no 2026 Q1 B03 restatement in the four supplied PDFs.
- *Review report* is limited assurance, not a full annual audit; no claim that embedded digital signatures were cryptographically validated.

## Quarter cashflow control
Using reviewed H1 and original Q1:
- Arithmetic-only Q2 CFO `494578607554`, CFI `-707727120080`, CFF `219048746426`, net `5900233900`, FX `-12574718` VND.
- Original Q1 cash end `105856793049`, reviewed H1 cash end `100322233328`; quarter cash bridge residual `-11422218903` VND. **Still BLOCKED**, cannot publish quarter-only B03.
- User-uploaded reviewed H1 adds real source and changes 2026 current H1 numbers; TT99 year-opening reclassification proven, 31 March cash-vintage restatement NOT proven. Do not infer every CFO/CFI/CFF delta solely due to TT43 and do not accuse issuer of reporting violation.

## Implementation
- Evidence `reports/source-audits/GEG-2026H1-user-uploaded-reviewed-note37-current-cashflow-version.json` includes SHA of all four PDFs, signed H1 vs original period line amounts, Note37 2025 comparison and year-open, and exact residual.
- Regression `scripts/verify_geg_2026_h1_uploaded_reviewed_version.py` checks signed-source-ledger accounting identities, production original Q2 preserved, Q1 same SHA, 2025 comparative transformations, falsification negatives, and BLOCKED quarter.
- `.github/workflows/validate.yml` includes regression step. Run whole CI, merge only on PASS.
- Source PDFs were uploaded in chat and not committed or distributed. When later reopening them use attached file paths in this chat or independently source original URL; SHA record is source identifier, not guarantee of public URL identical binary.

## Next evidence
- Obtain issuer-signed restricted bank deposits as of 31 March 2026, or issuer-signed 2026 Q1 B03 restated under the reviewed H1 cash classification with detailed CFO/CFI/CFF row mapping.
- If switching production FY2026 H1 B03 from original Q2 to reviewed H1, first examine signed Q3 9M reconciled with updated H1 version; preserve Q3 existing PASS until verified and test every identity. No quarter-only promotion from current figures.
