#!/usr/bin/env python3
"""Original VDS consolidated 2025-Q4 B01/B02/FY B03, exact-VND source gate.

Issuer signed FY PDF 28 Jan 2026, 50 pages, SHA256 below. Standalone Q4
CFO, CFI and CFF are FY2025 12M minus verified Q3 2025 9M, same scope.
"""
import json
from decimal import Decimal
from pathlib import Path

doc=json.loads((Path(__file__).resolve().parents[1]/"data/financials-VDS.json").read_text("utf-8"))
rows={x["period"]:x for x in doc["items"]}
q=rows["2025-Q4"]
nextq=rows["2026-Q1"]
def v(key): return int((Decimal(str(q[key]))*Decimal(1000000)).to_integral_exact())
def s(*keys):return sum(v(k) for k in keys)

assert q["unit"]=="triệu VND" and q["eps"]==q["diluted_eps"]==51
assert q["roa"] is None and q["roe"] is None
assert "hợp nhất" in q["report_type"].lower()
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["original_pdf_sha256"]=="eba8fa6cde5e7325a8ab6fef5d2776807e81e6e3e17da24ed7a116f191baab95"
assert q["source_validation"]["original_pdf_bytes"]==10387010
assert q["source_validation"]["original_pdf_pages"]==[6,7,8,11,12,13,14,15,16]
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_fy_and_q4_standalone_cash"
assert q["cashflow_period_basis"]=="year_to_date"
assert len(q["financial_line_items_extracted_fields"])==118
assert set(q["financial_line_items_extracted_fields"])==set(q["financial_line_items_manually_verified_fields"])
assert v("operating_cash_flow")==-59940474075
assert v("investing_cash_flow")==40439803532
assert v("financing_cash_flow")==428224000000
assert v("net_cash_change")==408723329457
assert v("cash_beginning")==588252269795
assert v("capital_expenditure")==-3650969550
assert v("foreign_exchange_effect")==0
assert v("cash_beginning")+v("net_cash_change")==v("cash_ending")
assert v("operating_cash_flow")+v("investing_cash_flow")+v("financing_cash_flow")==v("net_cash_change")
assert q["source_validation"]["q4_standalone_cashflow_status"]=="derived_from_verified_original_FY_12M_minus_original_Q3_9M"
assert all(x=="0" for x in q["source_validation"]["q4_standalone_cashflow_residuals_vnd"].values())
assert q["selling_expense"] is None

SOURCE={
 "total_assets":8121452969623,"total_liabilities":5022323459557,"equity":3099129510066,
 "current_assets":6925802937636,"non_current_assets":1195650031987,
 "financial_current_assets":6910970948034,"other_current_assets":14831989602,
 "financial_noncurrent_assets":1091869660940,"fixed_assets":61495440050,
 "construction_in_progress":653595750,"other_noncurrent_assets":41631335247,
 "current_liabilities":4998480395596,"long_term_liabilities":23843063961,
 "cash_and_equivalents":996975599252,"cash_only":846975599252,"cash_equivalents_only":150000000000,
 "broker_fvtpl_assets":1353534452184,"broker_lending_assets":4003532443009,
 "broker_afs_assets":495850260000,"broker_financial_assets_impairment":-44212240217,
 "broker_receivables":79386427835,"broker_noncurrent_held_to_maturity_assets":800000000000,
 "broker_noncurrent_other_investments":291869660940,"non_control_interest_equity":67544853295,
 "parent_equity":3031584656771,"revenue":221975460374,"revenue_ytd":1041834370118,
 "broker_fvtpl_gain":23061221276,"broker_fvtpl_trade_profit":167677087732,
 "broker_fvtpl_revaluation_gain":-148005854370,
 "broker_fvtpl_interest_dividend_income":3389987914,
 "broker_total_operating_expenses":162390566550,
 "broker_fvtpl_loss":37413271337,
 "financial_income":15085954900,"financial_expense":11665136606,"admin_expense":47290771609,
 "operating_profit":15714940509,"other_profit":29216612,"pretax_profit":15744157121,
 "income_tax":5651950112,"income_tax_current":37119111184,
 "income_tax_deferred":-31467161072,"net_profit":10092207009,
 "net_profit_attributable":13821476572,"non_controlling_interest_profit":-3729269563,
 "operating_profit_ytd":346750206454,"pretax_profit_ytd":346792272212,
 "net_profit_ytd":282167739885,
 "operating_cash_flow_ytd":-850325354079,
 "investing_cash_flow_ytd":-824472465903,
 "financing_cash_flow_ytd":1464636000000,
 "net_cash_change_ytd":-210161819982,
 "cash_beginning_reported_ytd":1207137419234,
 "cash_ending":996975599252,
 "foreign_exchange_effect_ytd":0,"capital_expenditure_ytd":-10395248615,
 "client_brokerage_cash_ending_ytd":1748126020118,
}
for k,amount in SOURCE.items():
    assert v(k)==amount,(k,v(k),amount)

c={
"b01_balance":v("total_assets")-s("total_liabilities","equity"),
"b01_assets_classes":v("total_assets")-s("current_assets","non_current_assets"),
"b01_liab_classes":v("total_liabilities")-s("current_liabilities","long_term_liabilities"),
"b01_current_classes":v("current_assets")-s("financial_current_assets","other_current_assets"),
"b01_noncurrent_classes":v("non_current_assets")-s("financial_noncurrent_assets","fixed_assets","construction_in_progress","other_noncurrent_assets"),
"b01_cash_split":v("cash_and_equivalents")-s("cash_only","cash_equivalents_only"),
"b01_equity_owners":v("equity")-s("parent_equity","non_control_interest_equity"),
"b01_financial_longterm":v("financial_noncurrent_assets")-s("broker_noncurrent_held_to_maturity_assets","broker_noncurrent_other_investments"),
"b01_financial_current":v("financial_current_assets")-s("cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets","broker_lending_assets","broker_afs_assets","broker_financial_assets_impairment","broker_receivables","broker_supplier_advances","broker_service_receivables","broker_other_receivables","broker_receivable_impairment"),
"b02_revenue_components":v("revenue")-s("broker_fvtpl_gain","broker_htm_income","broker_lending_income","broker_afs_interest_income","broker_brokerage_revenue","broker_custody_revenue","broker_financial_advisory_revenue","broker_other_operating_income"),
"b02_fvtpl_components":v("broker_fvtpl_gain")-s("broker_fvtpl_trade_profit","broker_fvtpl_revaluation_gain","broker_fvtpl_interest_dividend_income"),
"b02_expense_components":v("broker_total_operating_expenses")-s("broker_fvtpl_loss","broker_afs_reclassification_loss","broker_loan_loss_and_borrowing_provision","broker_trading_expense","broker_brokerage_expense","broker_custody_expense","broker_advisory_expense","broker_other_service_expense"),
"b02_finance_cost":v("financial_expense")-s("interest_expense","broker_financial_fx_loss"),
"b02_operating":v("operating_profit")-v("revenue")-v("financial_income")+s("broker_total_operating_expenses","financial_expense","admin_expense"),
"b02_other":v("other_profit")-v("other_income")+v("other_expense"),
"b02_pretax":v("pretax_profit")-s("operating_profit","other_profit"),
"b02_tax":v("income_tax")-s("income_tax_current","income_tax_deferred"),
"b02_net":v("net_profit")-v("pretax_profit")+v("income_tax"),
"b02_parent_nci":v("net_profit")-s("net_profit_attributable","non_controlling_interest_profit"),
"b02_annual_operating":v("operating_profit_ytd")-v("revenue_ytd")-v("financial_income_ytd")+s("securities_operating_expense_ytd","financial_expense_ytd","admin_expense_ytd"),
"b02_annual_pretax":v("pretax_profit_ytd")-s("operating_profit_ytd","other_profit_ytd"),
"b02_annual_net":v("net_profit_ytd")-v("pretax_profit_ytd")+v("income_tax_ytd"),
"b02_annual_parent_nci":v("net_profit_ytd")-s("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
"b03_sections":v("net_cash_change_ytd")-s("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"),
"b03_cash_bridge":v("cash_ending")-s("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd"),
"b03_B01cash":v("cash_and_equivalents")-v("cash_ending"),
"b03_investing_components":v("investing_cash_flow_ytd")-s("capital_expenditure_ytd","investing_asset_disposal_proceeds_ytd","investing_capital_contributions_ytd","investing_recovery_of_capital_ytd","investing_dividends_received_ytd"),
"b03_finance_components":v("financing_cash_flow_ytd")-s("financing_share_issue_ytd","financing_share_repurchase_ytd","financing_borrowing_proceeds_ytd","financing_debt_repayments_ytd"),
}
assert len(c)==28 and all(x==0 for x in c.values()),c
assert set(c)==set(q["source_validation"]["statement_identity_residuals_vnd"])
assert all(x=="0" for x in q["source_validation"]["statement_identity_residuals_vnd"].values())
assert v("cash_ending")==int(Decimal(str(nextq["cash_beginning_reported_ytd"]))*1000000)
assert q["source_validation"]["opening_2026Q1_cash_residual_vnd"]=="0"
assert v("client_brokerage_cash_ending_ytd") != v("cash_ending")
prior=q["financial_line_items_prior_values"]["prior_unverified_auto_core_b03_before_20261119"]
assert prior["revenue"]==23061 and prior["net_profit"]==15744
assert prior["operating_cash_flow_ytd"]==346792
assert q["financial_line_items_rejected_values"]["auto_eps_vnd"]==501
assert v("net_profit")==v("pretax_profit")-v("income_tax")
print("PASS VDS 2025Q4 issuer signed consolidated 28 exact-VND B01/B02/B03 identities, 118 fields, original Q4 net P/L, FY CFO and exact 12M less verified 9M standalone Q4 flows")
