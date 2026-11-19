#!/usr/bin/env python3
"""IDC 2025-Q1 signed HNX original consolidated B01 B02 B03, exact VND.

The signed 62-page scanned original (28 April 2025) was rendered and manually
checked at PDF pages 8-14; see recovery workflow. No OCR rounded figures.
Q1 B03 is 3M YTD and Q1 standalone simultaneously.
"""
from decimal import Decimal
from pathlib import Path
import json
d=json.loads((Path(__file__).resolve().parents[1]/"data/financials-IDC.json").read_text("utf8"))
rows={row["period"]:row for row in d["items"]}
q,h=rows["2025-Q1"],rows["2025-Q2"]
s=q["source_validation"]
assert len(d["items"])==7 and all(row["period"]>="2025-Q1" for row in d["items"])
assert q["symbol"]=="IDC" and "hợp nhất" in q["report_type"].lower() and q["unit"]=="triệu VND"
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_q1_2025_and_q2_comparator"
assert q["cashflow_period_basis"]=="year_to_date"
assert s["manually_visual_reviewed"] is True
assert s["source_scope"].startswith("consolidated only")
assert s["reviewed_pdf_pages"]==[8,9,10,11,12,13,14]
assert s["issuer_pdf_sha256"]=="5b3809b3492cb8ac96900d41e9410bbec4155500dd1ecc315485f044e0cbc322"
assert s["issuer_pdf_bytes"]==15532917 and s["issuer_pdf_pages"]==62
assert s["source_recovery_actions_run"]==44565988985
assert q["eps"]==1040 and q["diluted_eps"]==1040 and q["eps_ytd"]==1040
assert q["roa"] is None and q["roe"] is None
def V(key):return int((Decimal(str(q[key]))*1000000).to_integral_exact())
def S(*ks):return sum(V(k) for k in ks)
fix={
"total_assets":19410468097703,"current_assets":8117308377501,
"non_current_assets":11293159720202,"total_liabilities":12280835294709,
"current_liabilities":5348738935759,"long_term_liabilities":6932096358950,
"equity":7129632802994,"cash_and_equivalents":2292800235520,
"short_term_receivables":1530965913962,"retained_earnings":1326003016864,
"revenue":1793484296130,"cost_of_goods_sold":1242093459547,
"gross_profit":551390836583,"operating_profit":475558350109,
"pretax_profit":520708647205,"income_tax_current":108547172018,
"income_tax_deferred":-4823069417,"net_profit":416984544604,
"net_profit_attributable":343278910627,
"cf_operating_before_working_capital_ytd":717333801107,
"operating_cash_flow_ytd":593194330719,"investing_cash_flow_ytd":-745138695014,
"financing_cash_flow_ytd":256704039546,
"net_cash_change_ytd":104759675251,"cash_beginning_reported_ytd":2188037806317,
"foreign_exchange_effect_ytd":2753952,"cash_ending":2292800235520,
"capital_expenditure_ytd":-162762056703,"dividends_paid_ytd":-20305690000}
for k,expected in fix.items():assert V(k)==expected,(k,V(k),expected)
src=s["source_exact_vnd_fields"]
assert len(src)==98 and len(q["financial_line_items_extracted_fields"])==98
assert set(src)==set(q["financial_line_items_extracted_fields"])==set(q["financial_line_items_manually_verified_fields"])
for k,expected in src.items():assert V(k)==int(expected),(k,V(k),expected)
assert all(V(k)==V(k+"_ytd") for k in (
"gross_revenue","revenue","cost_of_goods_sold","gross_profit",
"financial_income","financial_expense","operating_profit","pretax_profit","net_profit",
"net_profit_attributable","non_controlling_interest_profit"
))
assert all(V(k)==V(k+"_ytd") for k in (
"operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change",
"capital_expenditure","dividends_paid","foreign_exchange_effect"
))
checks={
"balance":V("total_assets")-S("total_liabilities","equity"),
"assets":V("total_assets")-S("current_assets","non_current_assets"),
"liability":V("total_liabilities")-S("current_liabilities","long_term_liabilities"),
"cash_split":V("cash_and_equivalents")-S("cash_only","cash_equivalents_only"),
"current_assets":V("current_assets")-S("cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"noncurrent_assets":V("non_current_assets")-S("long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
"equity":V("equity")-S("share_capital","share_premium","other_owner_capital","asset_revaluation_difference","development_investment_fund","retained_earnings","non_controlling_interest_equity"),
"revenue":V("gross_revenue")-V("revenue_deductions")-V("revenue"),
"gross":V("revenue")-V("cost_of_goods_sold")-V("gross_profit"),
"operating":V("gross_profit")+V("financial_income")-V("financial_expense")+V("profit_from_associates")-V("selling_expense")-V("admin_expense")-V("operating_profit"),
"other":V("other_income")-V("other_expense")-V("other_profit"),
"pretax":V("operating_profit")+V("other_profit")-V("pretax_profit"),
"tax":V("income_tax")-S("income_tax_current","income_tax_deferred"),
"net":V("pretax_profit")-V("income_tax")-V("net_profit"),
"split":V("net_profit")-S("net_profit_attributable","non_controlling_interest_profit"),
"cf_pre_wc":S("cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd")-V("cf_operating_before_working_capital_ytd"),
"cf_operating":S("cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_payments_ytd")-V("operating_cash_flow_ytd"),
"cf_investing":S("capital_expenditure_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_interest_dividends_received_ytd")-V("investing_cash_flow_ytd"),
"cf_financing":S("cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","dividends_paid_ytd")-V("financing_cash_flow_ytd"),
"cf_net":S("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-V("net_cash_change_ytd"),
"cf_bridge":S("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-V("cash_ending"),
"b01_cash":V("cash_and_equivalents")-V("cash_ending"),
"cf_pretax_match":V("cf_pretax_profit_ytd")-V("pretax_profit"),
"cf_interest_match":V("cf_interest_expense_ytd")-V("interest_expense")
}
assert len(checks)==24 and set(checks)==set(s["source_identity_residuals_vnd"])
assert all(a==0 for a in checks.values()),checks
assert all(int(a)==0 for a in s["source_identity_residuals_vnd"].values())
assert h["q2_standalone_cashflow_status"]=="verified_original_h1_6m_minus_original_q1_3m_same_consolidated_scope"
assert h["source_validation"]["q2_standalone_B03_original_q1_pdf_sha256"]==s["issuer_pdf_sha256"]
assert len(h["source_validation"]["q2_standalone_B03_identity_residuals_vnd"])==6
assert all(int(a)==0 for a in h["source_validation"]["q2_standalone_B03_identity_residuals_vnd"].values())
print("PASS IDC 2025 Q1 original signed 98 fields, 24 exact-VND checks, Q2 verified cashflow comparator source")
