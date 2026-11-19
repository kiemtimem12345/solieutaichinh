#!/usr/bin/env python3
"""Regression for visual signed IDC 2025-Q2 HNX consolidated B01/B02/B03.

The original 63-page PDF source is independently archived by HNX/Vietstock,
rendered by the recovery workflow, and has been manually checked at pages 8–14.
Store numeric values in million VND, but assertions always use exact integer VND.
Original H1 6M minus visually verified signed Q1 3M yields exact standalone Q2 cashflow.
"""
from decimal import Decimal
import json
from pathlib import Path

doc=json.loads((Path(__file__).resolve().parents[1]/"data/financials-IDC.json").read_text("utf-8"))
rows={r["period"]:r for r in doc["items"]}
q=rows["2025-Q2"]
s=q["source_validation"]
assert len(doc["items"])==7 and all(r["period"]>="2025-Q1" for r in doc["items"])
assert q["symbol"]=="IDC" and "hợp nhất" in q["report_type"].lower()
assert q["unit"]=="triệu VND" and q["cashflow_period_basis"]=="year_to_date"
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_6m_and_q2_standalone_cash"
assert q["financial_line_items_status"]=="issuer_original_visual_B01_B02_B03_6m_plus_Q2_standalone_cash_verified"
assert s["manually_visual_reviewed"] is True
assert s["source_scope"].startswith("consolidated only")
assert s["reviewed_pdf_pages"]==[8,9,10,11,12,13,14]
assert s["original_pdf_pages"]==63 and s["original_pdf_bytes"]==15956738
assert s["original_issuer_signed_pdf_sha256"]=="04ced780ca282517bc28399e59d1a08dda0338cdda6a523403139a821674003f"
assert s["original_hnx_zip_sha256"]=="48616c2bb9d17c9937590f0f1332ff7e9b75e160385860b61fcc1c2e2a9e6614"
assert s["original_pdf_member"]=="4_idc_2025_7_30_caaaf64_vi_baocaotaichinhhn_q2_2025_s.pdf"
assert s["source_recovery_actions_run"]==44562677282
assert q["eps"]==902 and q["diluted_eps"]==902 and q["eps_ytd"]==1942
assert q["roa"] is None and q["roe"] is None
assert q["q2_standalone_cashflow_status"]=="verified_original_h1_6m_minus_original_q1_3m_same_consolidated_scope"
assert "q2_standalone_B03_blocker" not in s
assert s["q2_standalone_B03_original_q1_pdf_sha256"]=="5b3809b3492cb8ac96900d41e9410bbec4155500dd1ecc315485f044e0cbc322"
expected_q2={
"operating_cash_flow":809015066804,"investing_cash_flow":-1693078122700,
"financing_cash_flow":-545521959637,"net_cash_change":-1429585015533,
"capital_expenditure":-746582157511,"foreign_exchange_effect":38713120,
"dividends_paid":-568281373470,"cash_beginning":2292800235520}
for key,amount in expected_q2.items():
    assert int(s["q2_standalone_B03_verified_vnd"][key])==amount
    assert int((Decimal(str(q[key]))*Decimal(1000000)).to_integral_exact())==amount
    if key!="cash_beginning":
        src_q1=rows["2025-Q1"]
        assert amount==int((Decimal(str(q[key+"_ytd"]))-Decimal(str(src_q1[key+"_ytd"])))*Decimal(1000000))
assert all(int(v)==0 for v in s["q2_standalone_B03_identity_residuals_vnd"].values())
assert len(s["q2_standalone_B03_identity_residuals_vnd"])==6
def V(k):return int((Decimal(str(q[k]))*Decimal(1000000)).to_integral_exact())
def S(*ks):return sum(V(k) for k in ks)
fixture={
"total_assets":19606417044848,"total_liabilities":12150945318805,"equity":7455471726043,
"current_assets":7811294674643,"non_current_assets":11795122370205,
"cash_and_equivalents":863253933107,"current_liabilities":3669554755411,
"long_term_liabilities":8481390563394,"retained_earnings":1603390908975,
"revenue":1763197891011,"cost_of_goods_sold":1218680135812,
"gross_profit":544517755199,"financial_income":62954887826,"financial_expense":29939147355,
"operating_profit":491284811691,"pretax_profit":519324437238,"income_tax":103360530018,
"net_profit":415963907220,"net_profit_attributable":297573101125,
"non_controlling_interest_profit":118390806095,
"gross_profit_ytd":1095908591782,"operating_profit_ytd":966843161800,
"pretax_profit_ytd":1040033084443,"net_profit_ytd":832948451824,
"cf_investment_gains_ytd":-128028360752,"cf_operating_before_working_capital_ytd":1351845045068,
"cf_receivables_ytd":-113079215676,"cf_payables_ytd":650923124092,
"operating_cash_flow_ytd":1402209397523,"investing_cash_flow_ytd":-2438216817714,
"financing_cash_flow_ytd":-288817920091,"net_cash_change_ytd":-1324825340282,
"cash_beginning_reported_ytd":2188037806317,"foreign_exchange_effect_ytd":41467072,
"cash_ending":863253933107,"capital_expenditure_ytd":-909344214214,
"dividends_paid_ytd":-588587063470}
for k,expected in fixture.items():assert V(k)==expected,(k,V(k),expected)
source=s["original_source_exact_vnd_fields"]
assert len(source)==100 and len(q["financial_line_items_extracted_fields"])==100
assert q["financial_line_items_extracted_fields"]==q["financial_line_items_manually_verified_fields"]
assert set(source)==set(q["financial_line_items_extracted_fields"])
for k,expected in source.items():
    assert V(k)==int(expected),(k,V(k),expected)
checks={
"balance":V("total_assets")-S("total_liabilities","equity"),
"assets":V("total_assets")-S("current_assets","non_current_assets"),
"liability":V("total_liabilities")-S("current_liabilities","long_term_liabilities"),
"cash_split":V("cash_and_equivalents")-S("cash_only","cash_equivalents_only"),
"current_assets":V("current_assets")-S("cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"noncurrent_assets":V("non_current_assets")-S("long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
"equity":V("equity")-S("share_capital","share_premium","other_owner_capital","asset_revaluation_difference","development_investment_fund","retained_earnings","non_controlling_interest_equity"),
"q2_revenue":V("gross_revenue")-V("revenue_deductions")-V("revenue"),
"q2_gross":V("revenue")-V("cost_of_goods_sold")-V("gross_profit"),
"q2_operating":V("gross_profit")+V("financial_income")-V("financial_expense")+V("profit_from_associates")-V("selling_expense")-V("admin_expense")-V("operating_profit"),
"q2_other":V("other_income")-V("other_expense")-V("other_profit"),
"q2_pretax":V("operating_profit")+V("other_profit")-V("pretax_profit"),
"q2_tax":V("income_tax")-S("income_tax_current","income_tax_deferred"),
"q2_net":V("pretax_profit")-V("income_tax")-V("net_profit"),
"q2_profit_split":V("net_profit")-S("net_profit_attributable","non_controlling_interest_profit"),
"h1_revenue":V("gross_revenue_ytd")-V("revenue_deductions_ytd")-V("revenue_ytd"),
"h1_gross":V("revenue_ytd")-V("cost_of_goods_sold_ytd")-V("gross_profit_ytd"),
"h1_operating":V("gross_profit_ytd")+V("financial_income_ytd")-V("financial_expense_ytd")+V("profit_from_associates_ytd")-V("selling_expense_ytd")-V("admin_expense_ytd")-V("operating_profit_ytd"),
"h1_other":V("other_income_ytd")-V("other_expense_ytd")-V("other_profit_ytd"),
"h1_pretax":V("operating_profit_ytd")+V("other_profit_ytd")-V("pretax_profit_ytd"),
"h1_tax":V("income_tax_ytd")-S("income_tax_current_ytd","income_tax_deferred_ytd"),
"h1_net":V("pretax_profit_ytd")-V("income_tax_ytd")-V("net_profit_ytd"),
"h1_profit_split":V("net_profit_ytd")-S("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
"cf_pre_wc":S("cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd")-V("cf_operating_before_working_capital_ytd"),
"cf_operating":S("cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_payments_ytd")-V("operating_cash_flow_ytd"),
"cf_investing":S("capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_interest_dividends_received_ytd")-V("investing_cash_flow_ytd"),
"cf_financing":S("cf_share_issue_proceeds_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","dividends_paid_ytd")-V("financing_cash_flow_ytd"),
"cf_net":S("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-V("net_cash_change_ytd"),
"cf_cash":S("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-V("cash_ending"),
"b01_b03_cash":V("cash_and_equivalents")-V("cash_ending")
}
assert len(checks)==30 and set(checks)==set(s["source_identity_residuals_vnd"])
assert all(value==0 for value in checks.values()),checks
assert all(int(v)==0 for v in s["source_identity_residuals_vnd"].values())
vintage=s["source_vintage_comparison"]
assert vintage["original_minus_reviewed_vnd"]=="47357863919"
assert int(vintage["original_b03_investment_gains_vnd"])-int(vintage["reviewed_h1_b03_investment_gains_vnd"])==47357863919
assert int(vintage["receivables_original_vnd"])-int(vintage["receivables_reviewed_vnd"])==-16695796978
assert int(vintage["payables_original_vnd"])-int(vintage["payables_reviewed_vnd"])==-30662066941
assert vintage["cashflow_totals_same_vnd"] is True
assert s["reviewed_h1_2025_consolidated_b03_visual"]["line_items_exact_vnd"]["operating_cash_flow_ytd"]==str(V("operating_cash_flow_ytd"))
print("PASS IDC Q2 2025 100 signed-source fields + 30 exact-VND identities; Q2 standalone signed H1 minus signed Q1 cashflow 6 checks; reviewed version difference retained")
