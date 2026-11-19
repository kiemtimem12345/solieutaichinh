#!/usr/bin/env python3
"""Issuer-original consolidated VDS Q3/2025 exact-VND statement regression.

Full B01 B02 and 9M B03 from 24 Oct 2025 signed issuer PDF; Q4/2025
standalone quarter cash is original FY 12M minus original Q3 9M, never OCR.
"""
import json
from decimal import Decimal
from pathlib import Path
doc=json.loads((Path(__file__).resolve().parents[1]/"data/financials-VDS.json").read_text("utf-8"))
r={x["period"]:x for x in doc["items"]}
q,f=r["2025-Q3"],r["2025-Q4"]
def v(row,key):
    return int((Decimal(str(row[key]))*Decimal(1000000)).to_integral_exact())
def s(row,*ks): return sum(v(row,k) for k in ks)
assert q["unit"]=="triệu VND" and "hợp nhất" in q["report_type"].lower()
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_q3_standalone_cash"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["original_pdf_sha256"]=="93580147a2c34adb8118a83ed3d9348360355b0660bdd5a47871c60f2403dc3b"
assert q["source_validation"]["original_pdf_bytes"]==10076199
assert q["source_validation"]["original_pdf_pages"]==[6,7,8,11,12,13,14,15,16,17]
assert q["eps"]==q["diluted_eps"]==960
assert q["roa"] is None and q["roe"] is None and q["selling_expense"] is None
assert len(q["financial_line_items_extracted_fields"])==124
assert set(q["financial_line_items_extracted_fields"])==set(q["financial_line_items_manually_verified_fields"])
assert v(q,"operating_cash_flow")==-1214198760707
assert v(q,"investing_cash_flow")==-98906047822
assert v(q,"financing_cash_flow")==612012000000
assert v(q,"net_cash_change")==-701092808529
assert v(q,"cash_beginning")==1289345078324
assert v(q,"cash_beginning")+v(q,"net_cash_change")==v(q,"cash_ending")
assert v(q,"operating_cash_flow")+v(q,"investing_cash_flow")+v(q,"financing_cash_flow")==v(q,"net_cash_change")
assert q["source_validation"]["q3_standalone_source_Q2_sha256"]=="48934ed3df3d6b47271c563448fc908ecf68533a990dd205397f87dd78525a36"
assert all(x=="0" for x in q["source_validation"]["q3_standalone_residuals_vnd"].values())
original={
 "total_assets":7732966527561,"total_liabilities":4578708861227,"equity":3154257666334,
 "current_assets":6530500802868,"non_current_assets":1202465724693,
 "financial_current_assets":6515004521376,"other_current_assets":15496281492,
 "financial_noncurrent_assets":1095875463410,"fixed_assets":64985477513,
 "construction_in_progress":0,"other_noncurrent_assets":41604783770,
 "current_liabilities":4522612518725,"long_term_liabilities":56096342502,
 "cash_and_equivalents":588252269795,"cash_only":435252269795,"cash_equivalents_only":153000000000,
 "broker_fvtpl_assets":1448355116236,"broker_lending_assets":4005047840003,
 "broker_afs_assets":408781530000,"broker_financial_assets_impairment":-44222315258,
 "broker_receivables":89891998441,"broker_noncurrent_held_to_maturity_assets":800000000000,
 "broker_noncurrent_other_investments":295875463410,
 "broker_short_term_borrowings":1561426000000,"broker_short_term_bonds":2859100000000,
 "non_control_interest_equity":71274122857,"parent_equity":3082983543477,
 "revenue":469935413540,"revenue_ytd":819858909744,
 "broker_fvtpl_gain":259287392878,"broker_fvtpl_trade_profit":63339547879,
 "broker_fvtpl_revaluation_gain":189408165547,
 "broker_fvtpl_interest_dividend_income":6539679452,
 "broker_total_operating_expenses":106328748769,"broker_fvtpl_loss":-29733185559,
 "broker_fvtpl_trade_loss":15258944903,"broker_fvtpl_revaluation_loss":-45253873700,
 "broker_fvtpl_trading_expense":261743238,
 "financial_income":19292895989,"financial_expense":9560904110,"admin_expense":47492454241,
 "operating_profit":325846202409,"other_profit":748950,"pretax_profit":325846951359,
 "income_tax":61589855072,"income_tax_current":26295285720,"income_tax_deferred":35294569352,
 "net_profit":264257096287,"net_profit_attributable":261233437741,
 "non_controlling_interest_profit":3023658546,"operating_profit_ytd":331035265945,
 "pretax_profit_ytd":331048115091,"net_profit_ytd":272075532876,
 "net_profit_attributable_ytd":269304589718,
 "non_controlling_interest_profit_ytd":2770943158,
 "operating_cash_flow_ytd":-790384880004,
 "investing_cash_flow_ytd":-864912269435,
 "financing_cash_flow_ytd":1036412000000,
 "net_cash_change_ytd":-618885149439,
 "cash_beginning_reported_ytd":1207137419234,
 "cash_ending":588252269795,"foreign_exchange_effect_ytd":0,
 "capital_expenditure_ytd":-6744279065,
 "client_brokerage_cash_beginning_ytd":835549380874,
 "client_brokerage_cash_ending_ytd":2589483189435,
 "client_brokerage_cash_change_ytd":1753933808561,
}
for k,expected in original.items():
    assert v(q,k)==expected,(k,v(q,k),expected)
c={
"b01_balance":v(q,"total_assets")-s(q,"total_liabilities","equity"),
"b01_assets_classes":v(q,"total_assets")-s(q,"current_assets","non_current_assets"),
"b01_liab_classes":v(q,"total_liabilities")-s(q,"current_liabilities","long_term_liabilities"),
"b01_current_classes":v(q,"current_assets")-s(q,"financial_current_assets","other_current_assets"),
"b01_noncurrent_classes":v(q,"non_current_assets")-s(q,"financial_noncurrent_assets","fixed_assets","construction_in_progress","other_noncurrent_assets"),
"b01_cash_split":v(q,"cash_and_equivalents")-s(q,"cash_only","cash_equivalents_only"),
"b01_equity_owners":v(q,"equity")-s(q,"parent_equity","non_control_interest_equity"),
"b01_financial_longterm":v(q,"financial_noncurrent_assets")-s(q,"broker_noncurrent_held_to_maturity_assets","broker_noncurrent_other_investments"),
"b01_financial_current":v(q,"financial_current_assets")-s(q,"cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets","broker_lending_assets","broker_afs_assets","broker_financial_assets_impairment","broker_receivables","broker_supplier_advances","broker_service_receivables","broker_other_receivables","broker_receivable_impairment"),
"b02_revenue":v(q,"revenue")-s(q,"broker_fvtpl_gain","broker_htm_income","broker_lending_income","broker_afs_interest_income","broker_brokerage_revenue","broker_custody_revenue","broker_financial_advisory_revenue","broker_other_operating_income"),
"b02_fvtpl":v(q,"broker_fvtpl_gain")-s(q,"broker_fvtpl_trade_profit","broker_fvtpl_revaluation_gain","broker_fvtpl_interest_dividend_income"),
"b02_fvtpl_loss":v(q,"broker_fvtpl_loss")-s(q,"broker_fvtpl_trade_loss","broker_fvtpl_revaluation_loss","broker_fvtpl_trading_expense"),
"b02_expenses":v(q,"broker_total_operating_expenses")-s(q,"broker_fvtpl_loss","broker_afs_reclassification_loss","broker_loan_loss_and_borrowing_provision","broker_trading_expense","broker_brokerage_expense","broker_advisory_expense_from_securities","broker_custody_expense","broker_advisory_expense","broker_other_service_expense"),
"b02_financial_expense":v(q,"financial_expense")-s(q,"interest_expense","broker_financial_fx_loss"),
"b02_operating":v(q,"operating_profit")-v(q,"revenue")-v(q,"financial_income")+s(q,"broker_total_operating_expenses","financial_expense","admin_expense"),
"b02_other":v(q,"other_profit")-v(q,"other_income")+v(q,"other_expense"),
"b02_pretax":v(q,"pretax_profit")-s(q,"operating_profit","other_profit"),
"b02_tax":v(q,"income_tax")-s(q,"income_tax_current","income_tax_deferred"),
"b02_net":v(q,"net_profit")-v(q,"pretax_profit")+v(q,"income_tax"),
"b02_parent_nci":v(q,"net_profit")-s(q,"net_profit_attributable","non_controlling_interest_profit"),
"b02_nine_month_operating":v(q,"operating_profit_ytd")-v(q,"revenue_ytd")-v(q,"financial_income_ytd")+s(q,"securities_operating_expense_ytd","financial_expense_ytd","admin_expense_ytd"),
"b02_nine_month_pretax":v(q,"pretax_profit_ytd")-s(q,"operating_profit_ytd","other_profit_ytd"),
"b02_nine_month_net":v(q,"net_profit_ytd")-v(q,"pretax_profit_ytd")+v(q,"income_tax_ytd"),
"b02_nine_month_parent_nci":v(q,"net_profit_ytd")-s(q,"net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
"b03_sections":v(q,"net_cash_change_ytd")-s(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"),
"b03_cash_bridge":v(q,"cash_ending")-s(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd"),
"b03_B01_cash":v(q,"cash_and_equivalents")-v(q,"cash_ending"),
"b03_investing":v(q,"investing_cash_flow_ytd")-s(q,"capital_expenditure_ytd","investing_capital_contributions_ytd","investing_recovery_of_capital_ytd","investing_dividends_received_ytd"),
"b03_financing":v(q,"financing_cash_flow_ytd")-s(q,"financing_share_issue_ytd","financing_share_repurchase_ytd","financing_borrowing_proceeds_ytd","financing_debt_repayments_ytd"),
"b03_client_cash":v(q,"client_brokerage_cash_ending_ytd")-s(q,"client_brokerage_cash_beginning_ytd","client_brokerage_cash_change_ytd"),
}
assert len(c)==30 and all(val==0 for val in c.values()),c
assert set(c)==set(q["source_validation"]["statement_identity_residuals_vnd"])
assert all(val=="0" for val in q["source_validation"]["statement_identity_residuals_vnd"].values())
assert v(q,"client_brokerage_cash_ending_ytd") != v(q,"cash_ending")
assert q["financial_line_items_prior_values"]["prior_unverified_auto_before_issuer_20251119"]["operating_cash_flow_ytd"]==331048
assert q["financial_line_items_rejected_values"]["auto_fx_ytd_million_vnd"]==588252

assert f["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_fy_and_q4_standalone_cash"
assert f["source_validation"]["q4_standalone_cashflow_q3_source_pdf_sha256"]=="93580147a2c34adb8118a83ed3d9348360355b0660bdd5a47871c60f2403dc3b"
assert f["source_validation"]["q4_standalone_cashflow_status"]=="derived_from_verified_original_FY_12M_minus_original_Q3_9M"
expected={
 "operating_cash_flow":-59940474075,
 "investing_cash_flow":40439803532,
 "financing_cash_flow":428224000000,
 "net_cash_change":408723329457,
 "capital_expenditure":-3650969550,
 "foreign_exchange_effect":0,
 "cash_beginning":588252269795,
}
for k,amount in expected.items():
    assert v(f,k)==amount,(k,v(f,k),amount)
    assert v(f,k)==v(f,k+"_ytd")-v(q,k+"_ytd") if k!="cash_beginning" else v(f,k)==v(q,"cash_ending")
assert v(f,"cash_ending")==v(q,"cash_ending")+v(f,"net_cash_change")
assert v(f,"net_cash_change")==s(f,"operating_cash_flow","investing_cash_flow","financing_cash_flow")
assert all(str(val)=="0" for val in f["source_validation"]["q4_standalone_cashflow_residuals_vnd"].values())
for k in ("revenue","pretax_profit","net_profit","net_profit_attributable","non_controlling_interest_profit","operating_profit","other_profit"):
    assert v(f,k)==v(f,k+"_ytd")-v(q,k+"_ytd"),k
assert all(str(x)=="0" for x in f["source_validation"]["q4_quarterly_B02_equals_FY_minus_9M_vnd"].values())
print("PASS: VDS Q3 2025 original B01 B02 9M B03 30 identities; Q4 FY-minus-9M standalone B03 and B02 exact at VND")
