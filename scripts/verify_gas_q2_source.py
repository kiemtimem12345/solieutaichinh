#!/usr/bin/env python3
"""Source-anchored validation for GAS consolidated Q2/2025 B01/B02/B03.

B03 original H1 is year-to-date; public quarterly Q2 values equal H1 less
Q1 same-scope source-verified YTD. Checks exact VND. Does not imply visual
PDF screenshot review, which is pending because cached PDF image unavailable.
"""
import json
from decimal import Decimal
from pathlib import Path

o=json.loads((Path(__file__).resolve().parents[1]/"data/financials-GAS.json").read_text("utf-8"))
q1=next(x for x in o["items"] if x["period"]=="2025-Q1")
q2=next(x for x in o["items"] if x["period"]=="2025-Q2")
assert "hợp nhất" in q2["report_type"].lower()
assert q1["source_validation"]["manually_visual_reviewed"] is True
assert q2["source_validation"]["manually_visual_reviewed"] is True
assert q2["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_h1_ytd_and_q2_standalone_cash"
assert q2["source_validation"]["source_original_issuer_pdf_sha256"]=="c21bc4e88e2ce3d8331fa518df619d50086de50feed8691e48f653b825a4f31d"
assert q2["source_validation"]["source_original_issuer_pdf_bytes"]==14166457
assert q2["source_validation"]["source_original_issuer_pdf_pages"]==75
assert q2["source_validation"]["visually_reviewed_original_pdf_pages"]==[4,5,6,7]
assert q2["source_validation"]["source_original_pdf_recovery_workflow_run"]==44668684322
assert q2["source_validation"]["source_original_pdf_artifact_id"]==14599102084
assert q2["financial_line_items_manually_verified_fields"]==q2["financial_line_items_extracted_fields"]
assert len(q2["financial_line_items_manually_verified_fields"])==49
assert q2["source_validation"]["quarter_columns"]=="B02 current year quarter (not prior year or H1 YTD)"
assert q2["eps"]==1985 and q2["unit"]=="triệu VND"
assert q2["financial_line_items_manually_verified_fields"]==q2["financial_line_items_extracted_fields"]
assert len(q2["source_validation"]["exact_checks"])==23
assert all(x=="0" for x in q2["source_validation"]["exact_checks"].values())

def v(row, key):
    assert isinstance(row.get(key), (int,float)) and not isinstance(row[key],bool),(row["period"],key)
    n=Decimal(str(row[key]))*Decimal(1000000)
    assert n==n.to_integral_value(),(key,"not whole VND",n)
    return int(n)

count=0
def eq(title, left, right):
    global count
    assert left==right,(title,left,right,left-right)
    count+=1

eq("assets",v(q2,"current_assets")+v(q2,"non_current_assets"),v(q2,"total_assets"))
eq("sources",v(q2,"total_liabilities")+v(q2,"equity"),v(q2,"total_assets"))
eq("debt classes",v(q2,"current_liabilities")+v(q2,"long_term_liabilities"),v(q2,"total_liabilities"))
eq("current asset components",sum(v(q2,k) for k in ("cash_and_equivalents","short_term_investments","short_term_receivables","inventory"))+746080597465,v(q2,"current_assets"))
eq("gross",v(q2,"revenue")-v(q2,"cost_of_goods_sold"),v(q2,"gross_profit"))
eq("operating",v(q2,"gross_profit")+v(q2,"financial_income")-v(q2,"financial_expense")+v(q2,"share_of_profit_in_associates")-v(q2,"selling_expense")-v(q2,"admin_expense"),v(q2,"operating_profit"))
eq("other",v(q2,"other_income")-v(q2,"other_expense"),v(q2,"other_profit"))
eq("pretax",v(q2,"operating_profit")+v(q2,"other_profit"),v(q2,"pretax_profit"))
eq("taxes",v(q2,"income_tax_current")+v(q2,"income_tax_deferred"),v(q2,"income_tax"))
eq("after tax",v(q2,"pretax_profit")-v(q2,"income_tax"),v(q2,"net_profit"))
eq("noncontrolling",v(q2,"net_profit_attributable")+v(q2,"non_controlling_interest_profit"),v(q2,"net_profit"))
eq("H1 revenue",v(q1,"revenue")+v(q2,"revenue"),55755849819168)
eq("H1 gross",v(q1,"gross_profit")+v(q2,"gross_profit"),9043463237162)
eq("H1 pretax",v(q1,"pretax_profit")+v(q2,"pretax_profit"),9410488006623)
eq("H1 net",v(q1,"net_profit")+v(q2,"net_profit"),7571381524975)
eq("H1 cashflows",sum(v(q2,k) for k in ("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")),v(q2,"net_cash_change_ytd"))
eq("quarter cashflows",sum(v(q2,k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow")),v(q2,"net_cash_change"))
eq("H1 cash bridge",v(q2,"cash_beginning_reported_ytd")+v(q2,"net_cash_change_ytd")+v(q2,"foreign_exchange_effect_ytd"),v(q2,"cash_ending"))
eq("Q2 cash bridge",v(q2,"cash_beginning")+v(q2,"net_cash_change")+v(q2,"foreign_exchange_effect"),v(q2,"cash_ending"))
eq("H1 CFI components",-1025956642702-432200000000-17803047858253+14965776433351-10167798761+16000000000+428273527982,v(q2,"investing_cash_flow_ytd"))
eq("H1 CFF components",10167798761+380771869008-611765142445,v(q2,"financing_cash_flow_ytd"))
eq("quarter capex",v(q2,"capital_expenditure_ytd")-v(q1,"capital_expenditure_ytd"),v(q2,"capital_expenditure"))
eq("Q2 begins at Q1 closing cash",v(q1,"cash_ending"),v(q2,"cash_beginning"))
for field in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure"):
    eq(field+" Q2=H1 less Q1",v(q2,field+"_ytd")-v(q1,field+"_ytd"),v(q2,field))
assert v(q2,"admin_expense")==-1282797122580
assert v(q2,"foreign_exchange_effect")==1848437942
assert v(q2,"cash_beginning")==8166654567957 and v(q2,"cash_ending")==10597445910363
assert v(q2,"net_profit")==4808599034503
print(f"PASS: GAS consolidated Q2/2025 signed original 75-page PDF B01/B02/B03 visually checked pp4–7; 49 fields, {count} exact VND financial and Q2 YTD-minus-Q1 identities")
