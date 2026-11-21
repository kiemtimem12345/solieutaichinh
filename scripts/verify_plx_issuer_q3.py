#!/usr/bin/env python3
"""Verify PLX Q3/2026 issuer profit; parent B01/B02 source-PDF arithmetic.

The original B03 is blocked: a printed CFF differs from components by
87,654,015,000 VND. Never publish inferred Q3 cash flow on this evidence.
"""
import json
from decimal import Decimal
from pathlib import Path
obj=json.loads((Path(__file__).resolve().parents[1]/"data/financials-PLX.json").read_text(encoding="utf-8"))
q=[r for r in obj["items"] if r["period"]=="2026-Q3"]
assert len(q)==2,"Missing or duplicate PLX Q3 report scope"
expected={"consolidated":Decimal("1363096.640781"),"parent_company":Decimal("1315029.909162")}
signed_source={"consolidated":1363096640781,"parent_company":1315029909162}
required_parent=[
 "total_assets","total_liabilities","equity","current_assets","non_current_assets",
 "cash_and_equivalents","short_term_investments","short_term_receivables","inventory","fixed_assets",
 "revenue","cost_of_goods_sold","gross_profit","financial_income","financial_expense",
 "selling_expense","admin_expense","operating_profit","other_income","other_expense","other_profit",
 "pretax_profit","income_tax_current","income_tax_deferred","income_tax","net_profit"
]
def n(x,key): return Decimal(str(x[key]))
def exact(x,y): assert x==y,(x,y)
for r in q:
 scope=r["source_validation"]["scope"]
 assert scope in expected and Decimal(str(r["net_profit"]))==expected[scope]
 assert r["source_validation"]["reported_vnd"]==signed_source[scope]
 assert int(expected[scope]*Decimal(1000000))==signed_source[scope]
 assert r["source_validation"]["full_b01_b02_b03_visual_reviewed"] is (scope=="consolidated")
 if scope=="parent_company":
  assert not any(isinstance(r.get(k),(int,float)) for k in (
   "operating_cash_flow","investing_cash_flow","financing_cash_flow",
   "net_cash_change","cash_ending","dividends_paid")), "Parent B03 must stay blocked"
 if scope=="consolidated":
  assert r["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_q3_standalone_cash"
  assert r["source_validation"]["manually_visual_reviewed"] is True
  assert len(r["financial_line_items_extracted_fields"])==108
  assert r["financial_line_items_extracted_fields"]==r["financial_line_items_manually_verified_fields"]
  assert r["source_validation"]["q3_standalone_cashflow_status"]=="verified_signed_9m_minus_reviewed_signed_h1_same_consolidated_scope_and_cash_bridge_exact"
  links=r["source_validation"]["hose_source_links_discovered"]
  assert links["url_listing_verified"] is True
  assert links["issuer_pdf_bytes_recovered"] is True and links["issuer_pdf_visual_reviewed"] is True
  assert links["cashflow_quarterization_allowed"] is True
  assert links["original_q3_consolidated_pdf_url"]=="https://staticfile.hsx.vn/Uploads/UploadDocuments/2510747/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Hop%20nhat%20Q3%20nam%202026.pdf"
  assert "/2494321/" in links["reviewed_h1_consolidated_comparator_url"]
  assert "/2493840/" in links["reviewed_h1_parent_other_scope_url"]
  assert links["reviewed_h1_consolidated_comparator_url"]!=links["reviewed_h1_parent_other_scope_url"]

  assert all(isinstance(r.get(k),(int,float)) for k in
    ("revenue","gross_profit","total_assets","pretax_profit","net_profit_attributable",
     "operating_cash_flow","investing_cash_flow","financing_cash_flow",
     "net_cash_change","cash_beginning","cash_ending"))
 else:
  assert r["source_validation"]["source_document_url"].startswith("https://files.petrolimex.com.vn/")
  for key in required_parent:
   assert isinstance(r.get(key),(int,float)) and key in r["financial_line_items_extracted_fields"],key
  exact(n(r,"total_assets"),n(r,"total_liabilities")+n(r,"equity"))
  exact(n(r,"total_assets"),n(r,"current_assets")+n(r,"non_current_assets"))
  exact(n(r,"revenue"),n(r,"cost_of_goods_sold")+n(r,"gross_profit"))
  exact(n(r,"operating_profit"),n(r,"gross_profit")+n(r,"financial_income")-
        n(r,"financial_expense")-n(r,"selling_expense")-n(r,"admin_expense")+
        n(r,"investment_property_disposal_gain"))
  exact(n(r,"other_profit"),n(r,"other_income")-n(r,"other_expense"))
  exact(n(r,"pretax_profit"),n(r,"operating_profit")+n(r,"other_profit"))
  exact(n(r,"income_tax"),n(r,"income_tax_current")+n(r,"income_tax_deferred"))
  exact(n(r,"net_profit"),n(r,"pretax_profit")-n(r,"income_tax"))
  assert r["source_validation"]["b03_cashflow_discrepancy_vnd"]=="87654015000"
  assert r["source_validation"]["b03_cff_components_vnd"]=="6053755558718"
  assert r["source_validation"]["b03_cff_printed_vnd"]=="5966101543718"
  # Preserve the original nine-month B03 anomaly, without publishing a
  # guessed financing subtotal. Detailed signed-source rows 31..36 from PDF.
  financing_rows_vnd=(844158780900,-1134759693,71733162995138,
                       -65128441186058,0,-1393990271569)
  sum_cff=sum(financing_rows_vnd)
  printed_cff=5966101543718
  original_cfo=-3435516597061
  original_cfi=-2575747123895
  reported_net=42491837762
  assert sum_cff==6053755558718
  assert sum_cff-printed_cff==87654015000
  assert original_cfo+original_cfi+sum_cff==reported_net
  assert original_cfo+original_cfi+printed_cff==reported_net-87654015000
  assert r["source_validation"]["b03_net_cashflow_reported_vnd"]==str(reported_net)
  src=r["source_validation"]
  assert r["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_printed_cff_arithmetic_anomaly_blocked"
  assert src["issuer_original_signed_pdf_sha256"]=="a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef"
  assert src["issuer_original_signed_pdf_bytes"]==14198075 and src["issuer_original_signed_pdf_pages"]==39
  assert src["visually_reviewed_pdf_pages"]==[2,3,4,5,6,7,8]
  assert src["b01_b02_visual_reviewed"] and src["b03_original_visual_reviewed"]
  assert src["b03_error_confirmed_on_signed_original"] and src["b03_source_text_ocr_error_ruled_out"]
  assert sum(int(v) for v in src["b03_financing_detail_lines_vnd"].values())==sum_cff
  assert src["b03_source_identity_checks_vnd"]["net_using_components_minus_printed_net"]=="0"
  assert src["b03_source_identity_checks_vnd"]["net_using_printed_cff_minus_printed_net"]=="-87654015000"
  assert src["full_b01_b02_b03_visual_reviewed"] is False
  assert src["separate_parent_h1_2026_reviewed_pdf_still_pending"] is False
  assert src["reviewed_parent_h1_original_complete"] is True
  assert src["reviewed_parent_h1_b03_original_source_page_visual_verified"] is True
  assert src["reviewed_parent_h1_pdf_sha256"]=="a7929fbbc64f8f7fd201c33df9d09f32098ea1829ead9d6ea39c434f8821cd2c"
  assert src["reviewed_parent_h1_pdf_bytes"]==18543309 and src["reviewed_parent_h1_pdf_pages"]==63
  assert src["reviewed_parent_h1_b03_verified_pdf_pages"]==[10,11]
  reviewed_h1={k:int(v) for k,v in src["reviewed_parent_h1_original_b03_vnd"].items()}
  assert reviewed_h1["operating_cash_flow_ytd"]==990932483405
  assert reviewed_h1["investing_cash_flow_ytd"]==8086220870542
  assert reviewed_h1["financing_cash_flow_ytd"]==-9071667387469
  assert (reviewed_h1["operating_cash_flow_ytd"]+reviewed_h1["investing_cash_flow_ytd"]+reviewed_h1["financing_cash_flow_ytd"])==reviewed_h1["net_cash_change_ytd"]==5485966478
  assert (reviewed_h1["cash_beginning_reported_ytd"]+reviewed_h1["net_cash_change_ytd"]+reviewed_h1["foreign_exchange_effect_ytd"])==reviewed_h1["cash_ending"]==1416006359296
  assert src["q3_parent_cashflow_quarter_still_blocked_by_signed_original_cff_discrepancy"] is True
  from decimal import Decimal as _D
  relative_error = _D(src["b03_cashflow_discrepancy_vnd"])/_D(src["b03_cff_printed_vnd"])*_D(100)
  assert relative_error > _D("0.1") # User-approved subtotal tolerance cannot rescue this.
  assert abs(relative_error-_D(src["b03_arithmetic_difference_percent_of_printed_cff"])) < _D("1e-22")
  assert src["b03_exceeds_user_approved_0p1percent_subtotal_threshold"] is True
  assert src["automatic_extraction_exhausted"] is True
  assert src["terminal_manual_review"] is True
  assert src["issuer_q3_parent_b03_official_correction_verified"] is False
  assert src["no_automatic_repeat_same_signed_pdf_for_b03"] is True
  assert src["terminal_manual_review_scope"].startswith("ONLY PLX Q3/2026 PARENT B03")
  assert "87,654,015,000" in src["terminal_manual_review_reason"]
  assert "Authenticated issuer-signed amended B03" in src["reopen_condition"]
  assert src["next_processable_target"].startswith("GEG consolidated 2026-Q2")
  assert src["vietstock_alternate_signed_original_source_comparison"]["signed_issuer_and_mirror_embedded_images_identical"] is True
  assert src["vietstock_alternate_signed_original_source_comparison"]["source_original_embedded_images_identical_count"] == 39
  assert src["vietstock_alternate_signed_original_source_comparison"]["original_b03_embedded_scan_images_identical"] is True



  assert r["source_validation"]["b03_component_cfo_cfi_cff_reconciles_net_change"]
assert {r["source_validation"]["scope"] for r in q}==set(expected)
previous=next(r for r in obj["items"] if r["period"]=="2025-Q3" and "hợp nhất" in r["report_type"].lower())
prev_issuer=Decimal("705970.238434")
assert abs(Decimal(str(previous["net_profit"]))-prev_issuer)/prev_issuer*100<=Decimal("0.01")
print("PASS: PLX Q3 consolidated B01/B02/B03 and reviewed-H1 standalone cash source-verified; PLX parent Q3 source-printed CFF 87,654,015,000 VND discrepancy independently quarantined")
