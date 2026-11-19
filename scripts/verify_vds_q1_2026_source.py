#!/usr/bin/env python3
"""Exact-VND regression for VDS issuer consolidated 2026 Q1 B01/B02/B03.

The issuer's Q1 statement columns are authoritative for Q1 stand-alone figures.
H1/2026 later cumulative netted identical 6,063,861,335 VND out of FVTPL
revenues and expenses, leaving operating profit unchanged. Preserve both source
vintages and the 141,501,685 VND owner/NCI H1 allocation discrepancy.
"""
import json
from decimal import Decimal
from pathlib import Path
p = Path(__file__).resolve().parents[1] / "data" / "financials-VDS.json"
rows = {r["period"]: r for r in json.loads(p.read_text("utf-8"))["items"]}
q,h = rows["2026-Q1"],rows["2026-Q2"]
def v(row,key):
    return int((Decimal(str(row[key]))*Decimal(1000000)).to_integral_exact())
def s(row,*keys):
    return sum(v(row,k) for k in keys)
assert q["unit"]=="triệu VND"
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_q1_and_ytd"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["b03_q1_issuer_original_visual_verified"] is True
assert q["source_validation"]["issuer_report_signed_on"]=="2026-04-24"
assert q["source_validation"]["original_issuer_pdf_sha256"]=="f48b349d51f0158185764b8862648386b9560c271fdb11c65c8bb5710b8e90ec"
assert q["source_validation"]["issuer_pdf_pages"]==list(range(6,17))
assert q["eps"] == q["diluted_eps"] == -105
assert q["roa"] is None and q["roe"] is None and q["selling_expense"] is None
assert q["financial_line_items_status"]=="issuer_original_visual_B01_B02_B03_q1_verified"
assert len(q["financial_line_items_manually_verified_fields"])==88
assert set(q["financial_line_items_manually_verified_fields"])==set(q["financial_line_items_extracted_fields"])

source = {
 "total_assets":7868505982599,"total_liabilities":4839432932978,"equity":3029073049621,
 "current_assets":6417238249041,"non_current_assets":1451267733558,
 "financial_current_assets":6401952024611,"other_current_assets":15286224430,
 "financial_noncurrent_assets":1353238800940,"fixed_assets":55943385496,
 "construction_in_progress":653595750,"other_noncurrent_assets":41431951372,
 "current_liabilities":4831645599511,"long_term_liabilities":7787333467,
 "cash_and_equivalents":858161024619,"cash_only":399661024619,"cash_equivalents_only":458500000000,
 "broker_fvtpl_assets":1272891059150,"broker_held_to_maturity_assets":0,
 "broker_lending_assets":3842280764261,"broker_afs_assets":412758448000,
 "broker_financial_assets_impairment":-44212240217,"broker_receivables":45939812590,
 "broker_supplier_advances":790685923,"broker_service_receivables":12615666398,
 "broker_other_receivables":2705012365,"broker_receivable_impairment":-1978208478,
 "broker_noncurrent_held_to_maturity_assets":1100000000000,
 "broker_noncurrent_other_investments":253238800940,
 "non_control_interest_equity":59719114955,
 "broker_customer_deposits":1220638114499,
 "revenue":202757306990,"broker_fvtpl_gain":-21364334330,
 "broker_htm_income":14427123290,"broker_lending_income":118422852421,
 "broker_afs_interest_income":33685939300,"broker_brokerage_revenue":54605098960,
 "broker_custody_revenue":1959949420,"broker_financial_advisory_revenue":414090909,
 "broker_other_operating_income":606587020,
 "broker_fvtpl_trade_profit":42214526347,
 "broker_fvtpl_revaluation_gain":-69029299725,
 "broker_fvtpl_interest_dividend_income":5450439048,
 "broker_total_operating_expenses":190545800755,
 "broker_fvtpl_loss":59694895497,
 "broker_afs_reclassification_loss":5326029300,
 "broker_loan_loss_and_borrowing_provision":77138419416,
 "broker_trading_expense":917509818,
 "broker_brokerage_expense":41445982285,
 "broker_custody_expense":2143640576,
 "broker_advisory_expense":3260790859,
 "broker_other_service_expense":618533004,
 "financial_income":9984544961,"financial_expense":12726612033,
 "interest_expense":12546575343,"broker_financial_fx_loss":180036690,
 "admin_expense":45505054316,"operating_profit":-36035615153,
 "other_income":545454,"other_expense":0,"other_profit":545454,
 "pretax_profit":-36035069699,"income_tax":-6544269253,
 "income_tax_current":7851910907,"income_tax_deferred":-14396180160,
 "net_profit":-29490800446,"net_profit_attributable":-28526203886,
 "non_controlling_interest_profit":-964596560,
 "operating_cash_flow_ytd":248423817918,
 "investing_cash_flow_ytd":-270538392551,
 "financing_cash_flow_ytd":-116700000000,
 "net_cash_change_ytd":-138814574633,
 "cash_beginning_reported_ytd":996975599252,
 "cash_ending":858161024619,
 "capital_expenditure_ytd":-1035060800,
}
for k,amount in source.items():
    assert v(q,k)==amount,(k,v(q,k),amount)
source_checks={
 "b01_balance":v(q,"total_assets")-s(q,"total_liabilities","equity"),
 "b01_total_assets":v(q,"total_assets")-s(q,"current_assets","non_current_assets"),
 "b01_liabilities":v(q,"total_liabilities")-s(q,"current_liabilities","long_term_liabilities"),
 "b01_current_classes":v(q,"current_assets")-s(q,"financial_current_assets","other_current_assets"),
 "b01_longterm_classes":v(q,"non_current_assets")-s(q,"financial_noncurrent_assets","fixed_assets","construction_in_progress","other_noncurrent_assets"),
 "b01_cash":v(q,"cash_and_equivalents")-s(q,"cash_only","cash_equivalents_only"),
 "b01_financial_noncurrent":v(q,"financial_noncurrent_assets")-s(q,"broker_noncurrent_held_to_maturity_assets","broker_noncurrent_other_investments"),
 "b01_financial_current":v(q,"financial_current_assets")-s(q,"cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets","broker_lending_assets","broker_afs_assets","broker_financial_assets_impairment","broker_receivables","broker_supplier_advances","broker_service_receivables","broker_other_receivables","broker_receivable_impairment"),
 "b02_revenue":v(q,"revenue")-s(q,"broker_fvtpl_gain","broker_htm_income","broker_lending_income","broker_afs_interest_income","broker_brokerage_revenue","broker_custody_revenue","broker_financial_advisory_revenue","broker_other_operating_income"),
 "b02_fvtpl":v(q,"broker_fvtpl_gain")-s(q,"broker_fvtpl_trade_profit","broker_fvtpl_revaluation_gain","broker_fvtpl_interest_dividend_income"),
 "b02_operating_expenses":v(q,"broker_total_operating_expenses")-s(q,"broker_fvtpl_loss","broker_afs_reclassification_loss","broker_loan_loss_and_borrowing_provision","broker_trading_expense","broker_brokerage_expense","broker_custody_expense","broker_advisory_expense","broker_other_service_expense"),
 "b02_financial_expenses":v(q,"financial_expense")-s(q,"interest_expense","broker_financial_fx_loss"),
 "b02_operating":v(q,"operating_profit")-v(q,"revenue")-v(q,"financial_income")+s(q,"broker_total_operating_expenses","financial_expense","admin_expense"),
 "b02_other":v(q,"other_profit")-v(q,"other_income")+v(q,"other_expense"),
 "b02_pretax":v(q,"pretax_profit")-s(q,"operating_profit","other_profit"),
 "b02_tax":v(q,"income_tax")-s(q,"income_tax_current","income_tax_deferred"),
 "b02_net":v(q,"net_profit")-v(q,"pretax_profit")+v(q,"income_tax"),
 "b02_attributable":v(q,"net_profit")-s(q,"net_profit_attributable","non_controlling_interest_profit"),
 "b02_q1_ytd":v(q,"revenue_ytd")-v(q,"revenue"),
 "b01_b03_cash":v(q,"cash_and_equivalents")-v(q,"cash_ending"),
}
assert len(source_checks)==20 and all(n==0 for n in source_checks.values()),source_checks
assert source_checks.keys()==q["source_validation"]["b01_b02_exact_identity_residuals_vnd"].keys()
assert all(val=="0" for val in q["source_validation"]["b01_b02_exact_identity_residuals_vnd"].values())
b03={
 "q1_b03_sections":v(q,"net_cash_change_ytd")-s(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"),
 "q1_b03_bridge":v(q,"cash_ending")-s(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd"),
 "q1_b03_investing":v(q,"investing_cash_flow_ytd")-s(q,"capital_expenditure_ytd","investing_capital_contributions_ytd","investing_recovery_of_capital_ytd","investing_dividends_received_ytd"),
 "q1_b03_financing":v(q,"financing_cash_flow_ytd")-s(q,"financing_borrowing_proceeds_ytd","financing_debt_repayments_ytd"),
 "q1_b03_b01_cash":v(q,"cash_ending")-v(q,"cash_and_equivalents"),
}
assert len(b03)==5 and all(val==0 for val in b03.values()),b03
assert set(b03)==set(q["source_validation"]["b03_exact_identity_residuals_vnd"])
assert all(val=="0" for val in q["source_validation"]["b03_exact_identity_residuals_vnd"].values())

# Q2 6M issuer B03 minus Q1 3M same scope is now authoritative for Q2.
expected_q2={
 "operating_cash_flow":-251044721598,
 "investing_cash_flow":179751455631,
 "financing_cash_flow":14750000000,
 "net_cash_change":-56543265967,
 "capital_expenditure":-23746500,
 "cash_beginning":858161024619
}
for k,amount in expected_q2.items():assert v(h,k)==amount,(k,v(h,k),amount)
assert h["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_and_q2_standalone_cash"
assert v(h,"cash_beginning")+v(h,"net_cash_change")==v(h,"cash_ending")
assert v(h,"equity")-v(h,"non_control_interest_equity")-v(h,"parent_equity")==0
assert v(h,"non_control_interest_equity")==56506662501
assert v(h,"parent_equity")==2957968452602
assert h["source_validation"]["equity_split_exact_residual_vnd"]=="0"
assert q["financial_line_items_rejected_values"]["prior_auto_eps_vnd"]==501

# H1 2026 report code20 and code40 differ from the sum of the two separately
# released quarters by the same re-presentation amount: profit remains exact.
netting=6063861335
assert v(h,"revenue_ytd")-v(h,"revenue")-v(q,"revenue")==-netting
assert 341668738203-v(h,"broker_total_operating_expenses")-v(q,"broker_total_operating_expenses")==-netting
assert 47357244675-v(h,"broker_fvtpl_gain")-v(q,"broker_fvtpl_gain")==-netting
assert 94797348788-v(h,"broker_fvtpl_loss")-v(q,"broker_fvtpl_loss")==-netting
assert v(h,"operating_profit_ytd")==v(h,"operating_profit")+v(q,"operating_profit")
assert v(h,"pretax_profit_ytd")==v(h,"pretax_profit")+v(q,"pretax_profit")
assert v(h,"net_profit_ytd")==v(h,"net_profit")+v(q,"net_profit")
assert v(h,"net_profit_attributable_ytd")-v(h,"net_profit_attributable")-v(q,"net_profit_attributable")==141501685
assert v(h,"non_controlling_interest_profit_ytd")-v(h,"non_controlling_interest_profit")-v(q,"non_controlling_interest_profit")==-141501685
assert q["source_validation"]["h1_FVTPL_revenue_and_operating_expense_netting_difference_vnd"]=="-6063861335"
assert q["source_validation"]["h1_parent_nci_profit_allocation_difference_vnd"]=="141501685"
print("PASS: VDS 2026 Q1 20 B01/B02 and 5 B03 original exact VND checks; Q2 cash bridge verified; H1 FVTPL symmetric -6.064bn presentation and NCI split flagged without rewriting Q1")
