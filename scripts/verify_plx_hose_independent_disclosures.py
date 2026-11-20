#!/usr/bin/env python3
"""Independent HOSE issuer disclosure vs signed-source original cross-check.

Reads only local production JSON. Both HOSE explanatory letters are *separate*
official filings, distinct from signed BCTC PDF image verification.
PLX parent signed Q3 CFF anomaly must remain blocked even if income is PASS.
HNX IDC is a different issuer/exchange, not a PLX or GAS substitute.
"""
import json
from decimal import Decimal
from pathlib import Path
base=Path(__file__).resolve().parents[1]
obj=json.loads((base/"data/financials-PLX.json").read_text("utf-8"))
rows=[r for r in obj["items"] if r["period"]=="2026-Q3"]
assert len(rows)==2
def source(scope):return next(r for r in rows if r["source_validation"]["scope"]==scope)
con,par=source("consolidated"),source("parent_company")
def v(r,k):
 n=Decimal(str(r[k]))*Decimal(1000000)
 assert n==n.to_integral_value(),(k,n)
 return int(n)
xc=con["source_validation"]["hose_exchange_independent_explanations"]
xp=par["source_validation"]["hose_exchange_independent_explanations"]
assert xc["exchange"]==xp["exchange"]=="HOSE / HSX"
assert xc["q3_issuer_official_explanation_doc_number"]==xp["q3_issuer_official_explanation_doc_number"]=="2779/PLX-TCKT"
assert xc["h1_issuer_official_explanation_doc_number"]==xp["h1_issuer_official_explanation_doc_number"]=="2143/PLX-TCKT"
assert xc["q3_official_explanation_pdf"].startswith("https://staticfile.hsx.vn/Uploads/UploadDocuments/2510766/")
assert xc["h1_official_explanation_pdf"].startswith("https://staticfile.hsx.vn/Uploads/UploadDocuments/2493883/")
assert xc["q3_original_issuer_parent_hose_url"]==xp["q3_original_issuer_parent_hose_url"]
assert "/2510747/" in xc["q3_original_issuer_parent_hose_url"] and "/2510747/" in xc["q3_original_issuer_consolidated_hose_url"]
assert "Cong%20ty%20me" in xc["q3_original_issuer_parent_hose_url"]
assert "Hop%20nhat" in xc["q3_original_issuer_consolidated_hose_url"]
assert xc["hose_original_parent_source_http_content_length_bytes"]==14241486
assert xc["issuer_parent_source_pdf_previous_verified_bytes"]==14198075
assert xc["hose_parent_byte_difference_not_proof_of_restatement"] is True
assert xc["hose_parent_original_pdf_visual_comparison_pending"] is True
assert xc["h1_hose_explanation_does_not_address_q3_cff"] is True
assert xc["q3_hose_explanation_does_not_address_q3_cff"] is True
assert v(con,"net_profit")==int(xc["q3_aftertax_reported_exact_vnd"])==1363096640781
assert v(par,"net_profit")==int(xp["q3_parent_aftertax_reported_exact_vnd"])==1315029909162
assert int(xc["q3_aftertax_prior_year_reported_exact_vnd"])==705970238434
assert int(xp["q3_parent_aftertax_prior_year_reported_exact_vnd"])==527524735210
h1=v(con,"net_profit_ytd")-v(con,"net_profit")
assert h1==int(xc["h1_aftertax_from_9m_less_q3_original_exact_vnd"])==2389769308768
assert h1//1000000==int(xc["h1_aftertax_reported_rounded_million_vnd"])==2389769
assert h1-int(xc["h1_aftertax_reported_rounded_million_vnd"])*1000000==int(xc["h1_reported_rounding_difference_vnd"])==308768
assert xp["h1_parent_aftertax_reported_rounded_million_vnd"]=="678943"
assert con["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_q3_standalone_cash"
assert par["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_printed_cff_arithmetic_anomaly_blocked"
assert xp["q3_parent_cf_reported_subtotal_source_problem_vnd"]=="87654015000"
assert xp["q3_parent_cf_source_error_remains_blocked"] is True
assert xp["q3_parent_cf_original_hose_pdf_not_bytewise_comparison_verified"] is True
assert par["source_validation"]["b03_error_confirmed_on_signed_original"] is True
# Independent 2026 Vietstock issuer document archive is a PDF with DIFFERENT
# wrapper/cover metadata, but every original scanned issuer statement page is
# identical at embedded JPEG/PNG source-image byte level across 39/39 pages.
mirror=par["source_validation"]["vietstock_alternate_signed_original_source_comparison"]
assert mirror["source_url"].startswith("https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/PLX_Baocaotaichinh_Q3_2026_Congtyme.pdf")
assert mirror["source_pdf_sha256"]=="ab13686742234d95930b6c16e51300f7b2a2600e07919eb4b0a3464c820a6b6d"
assert mirror["source_pdf_bytes"]==14241486
assert mirror["source_pdf_pages"]==39
assert mirror["issuer_original_pdf_sha256"]=="a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef"
assert mirror["issuer_original_pdf_bytes"]==14198075
assert mirror["source_pdf_bytes_difference"]==43411
assert mirror["source_original_embedded_images_identical_count"]==mirror["source_original_embedded_images_total"]==39
assert mirror["signed_issuer_and_mirror_embedded_images_identical"] is True
assert mirror["original_b03_page_7_embedded_image_sha256"]=="2087fb122a23d4d850ed05498acbc7b1434f543ceb53998336f4943f98138296"
assert mirror["original_b03_page_8_embedded_image_sha256"]=="f8dddc318d103c0750b12eb922355696fdd0b9213786c3591dd4abc6f5d2cd6e"
assert mirror["original_b03_embedded_scan_images_identical"] is True
assert int(mirror["original_b03_sum_financing_detail_vnd"])-int(mirror["original_b03_printed_cff_subtotal_vnd"])==87654015000
assert mirror["q3_parent_b03_visual_validation_still_blocked"] is True
assert mirror["byte_length_matches_hose_content_length_header"] is True
assert mirror["hose_pdf_bytewise_sha256_still_unverified"] is True
assert mirror["github_actions_source_mirror_run"]==44676432848
assert mirror["github_actions_source_mirror_artifact_id"]==14602178653

assert all(par.get(k) is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_ending"))
print("PASS: PLX HOSE 2779 Q3 exact aftertax parent & consolidated; HOSE 2143 reviewed-H1 rounded profit agrees with signed 9M-minus-Q3 within 308768 VND; preserve issuer Q3 parent CFF 87654015000 VND source error and unreviewed exchange PDF.")
