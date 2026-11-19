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
 assert not r["source_validation"]["full_b01_b02_b03_visual_reviewed"]
 assert not any(isinstance(r.get(k),(int,float)) for k in (
  "operating_cash_flow","investing_cash_flow","financing_cash_flow",
  "net_cash_change","cash_ending","dividends_paid")), "B03 must stay blocked"
 if scope=="consolidated":
  assert r["financial_line_items_extracted_fields"]==["net_profit"]
  assert not any(isinstance(r.get(k),(int,float)) for k in
    ("revenue","gross_profit","total_assets","pretax_profit","net_profit_attributable"))
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
  assert r["source_validation"]["b03_component_cfo_cfi_cff_reconciles_net_change"]
assert {r["source_validation"]["scope"] for r in q}==set(expected)
previous=next(r for r in obj["items"] if r["period"]=="2025-Q3" and "hợp nhất" in r["report_type"].lower())
prev_issuer=Decimal("705970.238434")
assert abs(Decimal(str(previous["net_profit"]))-prev_issuer)/prev_issuer*100<=Decimal("0.01")
print("PASS: PLX Q3 consolidated issuer LNST; parent B01/B02 31 numeric fields and 8 exact reconciliations; B03 discrepancy blocked")
