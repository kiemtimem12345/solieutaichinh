#!/usr/bin/env python3
"""Regression: VDS issuer original 2025 Q1/Q2 B01 B02 B03 and Q2/Q3 cash.

Do not accept prior auto parser numbers or confuse Q1/Q2 standalone with YTD.
Original scans: Q1 issuer 48 pp SHA 632be553... and Q2 issuer 50 pp
SHA 48934ed...; business data stored in exact VND via Decimal(million).
"""
import json
from decimal import Decimal
from pathlib import Path

p=Path(__file__).resolve().parents[1]/"data/financials-VDS.json"
d=json.loads(p.read_text("utf-8"))
rows={r["period"]:r for r in d["items"]}
q,h,n=[rows[k] for k in ("2025-Q1","2025-Q2","2025-Q3")]
def v(x,k):
    return int((Decimal(str(x[k]))*Decimal(1000000)).to_integral_exact())
def s(x,*keys):return sum(v(x,k) for k in keys)
fixtures={
 "2025-Q1":{
 "total_assets":6348196110824,"total_liabilities":3502234864743,"equity":2845961246081,
 "current_assets":6089638598532,"non_current_assets":258557512292,
 "cash_and_equivalents":663750989889,"financial_current_assets":6075238554604,
 "financial_noncurrent_assets":144185817777,"fixed_assets":70844617599,
 "non_control_interest_equity":48412169777,"parent_equity":2797549076304,
 "revenue":168952311087,"broker_fvtpl_gain":33896814431,
 "broker_total_operating_expenses":112661705215,
 "financial_income":6742408779,"financial_expense":3769643835,
 "admin_expense":36619982450,"operating_profit":22643388366,
 "pretax_profit":22643851018,"income_tax":3631508762,
 "net_profit":19012342256,"net_profit_attributable":19089097924,
 "non_controlling_interest_profit":-76755668,
 "operating_cash_flow_ytd":-553201398548,
 "investing_cash_flow_ytd":78014969203,
 "financing_cash_flow_ytd":-68200000000,
 "net_cash_change_ytd":-543386429345,
 "cash_beginning_reported_ytd":1207137419234,
 "cash_ending":663750989889,"capital_expenditure_ytd":-959310000,
 "client_brokerage_cash_ending_ytd":1727897394701
 },
 "2025-Q2":{
 "total_assets":6856334146952,"total_liabilities":4022130711905,"equity":2834203435047,
 "current_assets":5746624022451,"non_current_assets":1109710124501,
 "cash_and_equivalents":1289345078324,"financial_current_assets":5731629921182,
 "financial_noncurrent_assets":999942873410,"fixed_assets":69267687690,
 "non_control_interest_equity":47250464312,"parent_equity":2786952970735,
 "revenue":180998605171,"revenue_ytd":349950141337,
 "broker_fvtpl_gain":27506294771,"broker_lending_income":93923645308,
 "broker_total_operating_expenses":160666996283,
 "financial_income":13265014557,"financial_expense":8468353872,
 "admin_expense":42582594403,"operating_profit":-17454324830,
 "pretax_profit":-17442687286,"income_tax":-6248781619,
 "net_profit":-11193905667,"net_profit_attributable":-9900252664,
 "non_controlling_interest_profit":-1293653003,
 "operating_cash_flow_ytd":423813880703,
 "investing_cash_flow_ytd":-766006221613,
 "financing_cash_flow_ytd":424400000000,
 "net_cash_change_ytd":82207659090,
 "cash_beginning_reported_ytd":1207137419234,
 "cash_ending":1289345078324,"capital_expenditure_ytd":-5045412431,
 "client_brokerage_cash_ending_ytd":1944403214851
 }}
for period,r in (("2025-Q1",q),("2025-Q2",h)):
    for k,expected in fixtures[period].items():
        assert v(r,k)==expected,(period,k,v(r,k),expected)
    assert r["unit"]=="triệu VND"
    assert r["source_validation"]["manually_visual_reviewed"] is True
    assert r["roa"] is None and r["roe"] is None
    assert r["selling_expense"] is None
    assert r["cashflow_period_basis"]=="year_to_date"
    assert len(r["financial_line_items_extracted_fields"])==120
    assert set(r["financial_line_items_extracted_fields"])==set(r["financial_line_items_manually_verified_fields"])

def identities(r):
    return {
      "b01_balance":v(r,"total_assets")-s(r,"total_liabilities","equity"),
      "b01_assets_classes":v(r,"total_assets")-s(r,"current_assets","non_current_assets"),
      "b01_liab_classes":v(r,"total_liabilities")-s(r,"current_liabilities","long_term_liabilities"),
      "b01_current_classes":v(r,"current_assets")-s(r,"financial_current_assets","other_current_assets"),
      "b01_noncurrent_classes":v(r,"non_current_assets")-s(r,"financial_noncurrent_assets","fixed_assets","construction_in_progress","other_noncurrent_assets"),
      "b01_cash_split":v(r,"cash_and_equivalents")-s(r,"cash_only","cash_equivalents_only"),
      "b01_equity_owners":v(r,"equity")-s(r,"parent_equity","non_control_interest_equity"),
      "b01_financial_longterm":v(r,"financial_noncurrent_assets")-s(r,"broker_noncurrent_held_to_maturity_assets","broker_noncurrent_other_investments"),
      "b01_financial_current":v(r,"financial_current_assets")-s(r,"cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets","broker_lending_assets","broker_afs_assets","broker_financial_assets_impairment","broker_receivables","broker_supplier_advances","broker_service_receivables","broker_other_receivables","broker_receivable_impairment"),
      "b02_revenue":v(r,"revenue")-s(r,"broker_fvtpl_gain","broker_htm_income","broker_lending_income","broker_afs_interest_income","broker_brokerage_revenue","broker_investment_advisory_revenue","broker_custody_revenue","broker_financial_advisory_revenue","broker_other_operating_income"),
      "b02_fvtpl":v(r,"broker_fvtpl_gain")-s(r,"broker_fvtpl_trade_profit","broker_fvtpl_revaluation_gain","broker_fvtpl_interest_dividend_income"),
      "b02_fvtpl_loss":v(r,"broker_fvtpl_loss")-s(r,"broker_fvtpl_trade_loss","broker_fvtpl_revaluation_loss","broker_fvtpl_trading_expense"),
      "b02_expenses":v(r,"broker_total_operating_expenses")-s(r,"broker_fvtpl_loss","broker_loan_loss_and_borrowing_provision","broker_trading_expense","broker_brokerage_expense","broker_custody_expense","broker_advisory_expense","broker_other_service_expense"),
      "b02_financial_expenses":v(r,"financial_expense")-s(r,"interest_expense","broker_financial_fx_loss"),
      "b02_operating":v(r,"operating_profit")-v(r,"revenue")-v(r,"financial_income")+s(r,"broker_total_operating_expenses","financial_expense","admin_expense"),
      "b02_other":v(r,"other_profit")-v(r,"other_income")+v(r,"other_expense"),
      "b02_pretax":v(r,"pretax_profit")-s(r,"operating_profit","other_profit"),
      "b02_tax":v(r,"income_tax")-s(r,"income_tax_current","income_tax_deferred"),
      "b02_net":v(r,"net_profit")-v(r,"pretax_profit")+v(r,"income_tax"),
      "b02_parent_nci":v(r,"net_profit")-s(r,"net_profit_attributable","non_controlling_interest_profit"),
      "b03_sections":v(r,"net_cash_change_ytd")-s(r,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"),
      "b03_bridge":v(r,"cash_ending")-s(r,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd"),
      "b03_B01_cash":v(r,"cash_and_equivalents")-v(r,"cash_ending"),
      "b03_investing":v(r,"investing_cash_flow_ytd")-s(r,"capital_expenditure_ytd","investing_capital_contributions_ytd","investing_recovery_of_capital_ytd","investing_dividends_received_ytd"),
      "b03_financing":v(r,"financing_cash_flow_ytd")-s(r,"financing_share_issue_ytd","financing_share_repurchase_ytd","financing_borrowing_proceeds_ytd","financing_debt_repayments_ytd"),
      "b03_client_cash":v(r,"client_brokerage_cash_ending_ytd")-s(r,"client_brokerage_cash_beginning_ytd","client_brokerage_cash_change_ytd"),
    }
for r,sha,status,extra in (
   (q,"632be5538c0b2b29c975f311388a2b33e97046e0cafc6a609e78b786771fbc86","issuer_original_visual_verified_b01_b02_b03_2025q1",{"b02_q1_ytd":v(q,"revenue_ytd")-v(q,"revenue")}),
   (h,"48934ed3df3d6b47271c563448fc908ecf68533a990dd205397f87dd78525a36","issuer_original_visual_verified_b01_b02_b03_h1_and_q2_standalone_cash",{
      "b02_h1_operating":v(h,"operating_profit_ytd")-v(h,"revenue_ytd")-v(h,"financial_income_ytd")+s(h,"securities_operating_expense_ytd","financial_expense_ytd","admin_expense_ytd"),
      "b02_h1_pretax":v(h,"pretax_profit_ytd")-s(h,"operating_profit_ytd","other_profit_ytd"),
      "b02_h1_net":v(h,"net_profit_ytd")-v(h,"pretax_profit_ytd")+v(h,"income_tax_ytd"),
      "b02_h1_parent_nci":v(h,"net_profit_ytd")-s(h,"net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
   })
):
    assert r["source_validation"]["original_pdf_sha256"]==sha
    assert r["verification_status"]==status
    calc={**identities(r),**extra}
    count=27 if r is q else 30
    assert len(calc)==count,(r["period"],len(calc))
    assert all(x==0 for x in calc.values()),calc
    assert set(calc)==set(r["source_validation"]["statement_identity_residuals_vnd"])
    assert all(x=="0" for x in r["source_validation"]["statement_identity_residuals_vnd"].values())

assert q["eps"]==79 and h["eps"]==-41
assert v(q,"operating_cash_flow")==v(q,"operating_cash_flow_ytd")
assert v(q,"cash_ending")==v(h,"cash_beginning")
assert v(h,"operating_cash_flow")==977015279251
assert v(h,"investing_cash_flow")==-844021190816
assert v(h,"financing_cash_flow")==492600000000
assert v(h,"net_cash_change")==625594088435
assert v(h,"cash_beginning")==663750989889
assert v(h,"capital_expenditure")==-4086102431
assert v(h,"cash_beginning")+v(h,"net_cash_change")==v(h,"cash_ending")
assert v(h,"net_cash_change")==s(h,"operating_cash_flow","investing_cash_flow","financing_cash_flow")
assert h["source_validation"]["q2_standalone_Q1_source_sha256"]==q["source_validation"]["original_pdf_sha256"]
assert all(x=="0" for x in h["source_validation"]["q2_standalone_residuals_vnd"].values())
assert v(n,"operating_cash_flow")==-1214198760707
assert v(n,"investing_cash_flow")==-98906047822
assert v(n,"financing_cash_flow")==612012000000
assert v(n,"net_cash_change")==-701092808529
assert v(n,"cash_beginning")==v(h,"cash_ending")
assert v(n,"cash_beginning")+v(n,"net_cash_change")==v(n,"cash_ending")
assert v(h,"pretax_profit_ytd")==v(q,"pretax_profit")+v(h,"pretax_profit")
assert v(h,"net_profit_ytd")==v(q,"net_profit")+v(h,"net_profit")
assert v(h,"revenue_ytd")-v(h,"revenue")-v(q,"revenue")==-774921
assert v(h,"securities_operating_expense_ytd")-v(h,"broker_total_operating_expenses")-v(q,"broker_total_operating_expenses")==-774921
assert v(h,"net_profit_attributable_ytd")-v(h,"net_profit_attributable")-v(q,"net_profit_attributable")==-1117693283
assert v(h,"non_controlling_interest_profit_ytd")-v(h,"non_controlling_interest_profit")-v(q,"non_controlling_interest_profit")==1117693283
print("PASS: original issuer VDS 2025-Q1 27 identities and Q2 30 identities in VND, exact Q2/Q3 standalone cash bridges, small H1 revenue netting and owner/NCI source-vintage difference preserved")
