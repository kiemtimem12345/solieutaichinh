#!/usr/bin/env python3
"""Issuer GEG consolidated 2025Q2 B01/B02/H1 B03 and Q3 standalone VND gate.

Original 85-page signed GEG PDF from HOSE/Vietstock, 24 July 2025.
PDF pages 7-8 B01, page 9 B02, pages 10-11 B03.
Do not accept an unverified 2025Q1 auto-derived Q2 standalone cash.
"""
import json
from decimal import Decimal
from pathlib import Path

doc=json.loads((Path(__file__).resolve().parents[1]/"data"/"financials-GEG.json").read_text("utf-8"))
rows={r["period"]:r for r in doc["items"] if "hợp nhất" in r.get("report_type","").lower()}
q,n=rows["2025-Q2"],rows["2025-Q3"]
def v(r,k):return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
def s(r,*keys):return sum(v(r,k) for k in keys)
source={
 "total_assets":15185463396529,"total_liabilities":8688615254343,
 "equity":6496848142186,"current_assets":1751807765411,
 "non_current_assets":13433655631118,"current_liabilities":689069127083,
 "long_term_liabilities":7999546127260,"parent_equity":4937387820688,
 "non_control_interest_equity":1559460321498,"cash_and_equivalents":473549350030,
 "cash_only":75431237865,"cash_equivalents_only":398118112165,
 "short_term_investments":236500000000,"short_term_receivables":914018215370,
 "inventory":105104270467,"other_current_assets":22635929544,
 "long_term_receivables":168557946073,"fixed_assets":12897652730850,
 "construction_in_progress":278924634105,"long_term_investments":53658442225,
 "other_non_current_assets":34861877865,"revenue":624339137173,
 "cost_of_goods_sold":351447828104,"gross_profit":272891309069,
 "financial_income":119441275360,"financial_expense":172262962873,
 "share_of_profit_in_associates":709366343,"admin_expense":37254702429,
 "operating_profit":183524285470,"other_profit":567073357,
 "pretax_profit":184091358827,"income_tax_current":28569111623,
 "income_tax_deferred":-2192612235,"income_tax":26376499388,
 "net_profit":157714859439,"net_profit_attributable":165820759376,
 "non_controlling_interest_profit":-8105899937,
 "revenue_ytd":1737094997154,"cost_of_goods_sold_ytd":638116324079,
 "gross_profit_ytd":1098978673075,"pretax_profit_ytd":789386094257,
 "net_profit_ytd":770660867986,"net_profit_attributable_ytd":544061594937,
 "operating_cash_flow_ytd":555421075993,"investing_cash_flow_ytd":476067298075,
 "financing_cash_flow_ytd":-721712954268,"net_cash_change_ytd":309775419800,
 "cash_beginning_reported_ytd":163717707072,
 "foreign_exchange_effect_ytd":56223158,"cash_ending":473549350030,
 "capital_expenditure_ytd":-16668892827,"dividends_paid_ytd":-296857300
}
for k,amount in source.items():assert v(q,k)==amount,(k,v(q,k),amount)
assert q["unit"]=="triệu VND" and q["eps"]==356 and q["diluted_eps"]==356
assert q["cashflow_period_basis"]=="year_to_date"
assert q["verification_status"]=="issuer_signed_original_visual_verified_B01_B02_B03_H1_ytd_and_Q2_standalone_cash"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["original_pdf_total_pages"]==85
assert q["source_validation"]["original_visual_page_numbers"]==[7,8,9,10,11]
assert q["source_validation"]["signed_report_date"]=="2025-07-24"
assert q["source_validation"]["original_pdf_sha256"]=="not_computed_source_url_and_images_verified"
assert len(q["financial_line_items_extracted_fields"])==104
assert q["financial_line_items_extracted_fields"]==q["financial_line_items_manually_verified_fields"]
assert v(q,"operating_cash_flow")==493110540478
assert v(q,"investing_cash_flow")==399539538641
assert v(q,"financing_cash_flow")==-594553494740
assert v(q,"net_cash_change")==298096584379
assert v(q,"cash_beginning")==175400032558
assert v(q,"capital_expenditure")==-15469177804
assert v(q,"foreign_exchange_effect")==52733093
assert v(q,"dividends_paid")==-75482900
assert q["source_validation"]["q2_standalone_cashflow_status"]=="derived_from_verified_original_H1_6m_minus_Q1_3m"
assert all(x=="0" for x in q["source_validation"]["q2_standalone_residuals_vnd"].values())
assert v(q,"cash_beginning")+v(q,"net_cash_change")+v(q,"foreign_exchange_effect")==v(q,"cash_ending")
assert v(q,"net_cash_change")==s(q,"operating_cash_flow","investing_cash_flow","financing_cash_flow")
assert q["roa"] is None and q["roe"] is None
assert q["financial_line_items_rejected_values"]["auto_eps_prior_vnd"]==70
assert q["financial_line_items_prior_values"]["prior_auto_2025Q2_unverified_before_original_20261119"]["operating_cash_flow_ytd"]==555421

c={
 "b01_assets":v(q,"total_assets")-s(q,"current_assets","non_current_assets"),
 "b01_balance":v(q,"total_assets")-s(q,"total_liabilities","equity"),
 "b01_liabilities":v(q,"total_liabilities")-s(q,"current_liabilities","long_term_liabilities"),
 "b01_owner_equity":v(q,"equity")-s(q,"parent_equity","non_control_interest_equity"),
 "b01_current_assets":v(q,"current_assets")-s(q,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
 "b01_noncurrent_assets":v(q,"non_current_assets")-s(q,"long_term_receivables","fixed_assets","construction_in_progress","long_term_investments","other_non_current_assets"),
 "b01_cash":v(q,"cash_and_equivalents")-s(q,"cash_only","cash_equivalents_only"),
 "b02_gross":v(q,"revenue")-v(q,"cost_of_goods_sold")-v(q,"gross_profit"),
 "b02_operating":v(q,"gross_profit")+v(q,"financial_income")-v(q,"financial_expense")+v(q,"share_of_profit_in_associates")-v(q,"selling_expense")-v(q,"admin_expense")-v(q,"operating_profit"),
 "b02_other":v(q,"other_income")-v(q,"other_expense")-v(q,"other_profit"),
 "b02_pretax":v(q,"operating_profit")+v(q,"other_profit")-v(q,"pretax_profit"),
 "b02_tax":v(q,"income_tax_current")+v(q,"income_tax_deferred")-v(q,"income_tax"),
 "b02_net":v(q,"pretax_profit")-v(q,"income_tax")-v(q,"net_profit"),
 "b02_nci":v(q,"net_profit_attributable")+v(q,"non_controlling_interest_profit")-v(q,"net_profit"),
 "ytd_gross":v(q,"revenue_ytd")-v(q,"cost_of_goods_sold_ytd")-v(q,"gross_profit_ytd"),
 "ytd_operating":v(q,"gross_profit_ytd")+v(q,"financial_income_ytd")-v(q,"financial_expense_ytd")+v(q,"share_of_profit_in_associates_ytd")-v(q,"selling_expense_ytd")-v(q,"admin_expense_ytd")-v(q,"operating_profit_ytd"),
 "ytd_other":v(q,"other_income_ytd")-v(q,"other_expense_ytd")-v(q,"other_profit_ytd"),
 "ytd_pretax":v(q,"operating_profit_ytd")+v(q,"other_profit_ytd")-v(q,"pretax_profit_ytd"),
 "ytd_tax":v(q,"income_tax_current_ytd")+v(q,"income_tax_deferred_ytd")-v(q,"income_tax_ytd"),
 "ytd_net":v(q,"pretax_profit_ytd")-v(q,"income_tax_ytd")-v(q,"net_profit_ytd"),
 "ytd_owner_split":v(q,"net_profit_attributable_ytd")+v(q,"non_controlling_interest_profit_ytd")-v(q,"net_profit_ytd"),
 "b03_before_wc":s(q,"cf_pretax_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investing_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v(q,"cf_before_working_capital_ytd"),
 "b03_cfo":s(q,"cf_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_taxes_paid_ytd","cf_other_paid_ytd")-v(q,"operating_cash_flow_ytd"),
 "b03_cfi":s(q,"capital_expenditure_ytd","cf_disposal_proceeds_ytd","cf_loans_issued_ytd","cf_loans_recovered_ytd","cf_equity_investments_ytd","cf_equity_recovery_ytd","cf_investment_income_received_ytd")-v(q,"investing_cash_flow_ytd"),
 "b03_cff":s(q,"cf_borrowings_ytd","cf_debt_repayments_ytd","cf_finance_leases_paid_ytd","dividends_paid_ytd")-v(q,"financing_cash_flow_ytd"),
 "b03_net":s(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v(q,"net_cash_change_ytd"),
 "b03_cash_bridge":s(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v(q,"cash_ending"),
 "b03_B01_cash":v(q,"cash_ending")-v(q,"cash_and_equivalents"),
 "same_fy_beginning":v(q,"cash_beginning_reported_ytd")-v(n,"cash_beginning_reported_ytd"),
 "ytd_Q3_revenue":v(n,"revenue_ytd")-v(n,"revenue")-v(q,"revenue_ytd"),
 "ytd_Q3_cogs":v(n,"cost_of_goods_sold_ytd")-v(n,"cost_of_goods_sold")-v(q,"cost_of_goods_sold_ytd"),
 "ytd_Q3_gross":v(n,"gross_profit_ytd")-v(n,"gross_profit")-v(q,"gross_profit_ytd"),
 "ytd_Q3_pretax":v(n,"pretax_profit_ytd")-v(n,"pretax_profit")-v(q,"pretax_profit_ytd"),
 "ytd_Q3_net":v(n,"net_profit_ytd")-v(n,"net_profit")-v(q,"net_profit_ytd"),
 "ytd_Q3_parent":v(n,"net_profit_attributable_ytd")-v(n,"net_profit_attributable")-v(q,"net_profit_attributable_ytd"),
}
assert len(c)==35 and all(x==0 for x in c.values()),c
assert set(c)==set(q["source_validation"]["statement_identity_residuals_vnd"])
assert all(x=="0" for x in q["source_validation"]["statement_identity_residuals_vnd"].values())

assert n["verification_status"]=="issuer_signed_original_visual_verified_B01_B02_B03_9m_ytd_and_Q3_standalone_cash"
assert len(n["financial_line_items_extracted_fields"])==104
assert n["source_validation"]["q3_standalone_cashflow_status"]=="derived_from_verified_original_9m_minus_H1_6m"
expectedQ3={
 "operating_cash_flow":300787939022,
 "investing_cash_flow":-232035400955,
 "financing_cash_flow":-136266702635,
 "net_cash_change":-67514164568,
 "capital_expenditure":-103386144231,
 "foreign_exchange_effect":18111591,
 "dividends_paid":-49677200,
 "cash_beginning":473549350030,
}
for k,amount in expectedQ3.items():
    assert v(n,k)==amount,(k,v(n,k),amount)
    if k!="cash_beginning":
        assert v(n,k)==v(n,k+"_ytd")-v(q,k+"_ytd"),k
    else: assert v(n,k)==v(q,"cash_ending")
assert v(n,"cash_beginning")+v(n,"net_cash_change")+v(n,"foreign_exchange_effect")==v(n,"cash_ending")
assert v(n,"net_cash_change")==s(n,"operating_cash_flow","investing_cash_flow","financing_cash_flow")
assert all(x=="0" for x in n["source_validation"]["q3_standalone_residuals_vnd"].values())
assert n["source_validation"]["source_q2_2025_original_pdf"]==q["source_url"]
print("PASS: GEG 2025Q2 original B01 B02 H1 B03 35 exact-VND identities; original 9M minus verified H1 Q3 standalone CFO/CFI/CFF and cash bridge exact")
