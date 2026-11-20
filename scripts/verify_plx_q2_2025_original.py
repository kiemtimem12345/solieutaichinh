#!/usr/bin/env python3
"""PLX consolidated Q2/2025 issuer signed original QA at source-exact VND.

Scanned B01 PDF pp2–4, B02 p5 and 6M/YTD B03 pp6–7 manually reviewed
in full 31-page source. Validate independently against exact VND numeric
transcription and earlier signed Q1/2025 same-scope source. Q2 standalone
B03 cashflow = issuer H1 cumulative less issuer Q1 cumulative, not OCR.
"""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
obj=json.loads((ROOT/"data/financials-PLX.json").read_text("utf-8"))
raw=(ROOT/"reports/source-audits/PLX-2025Q2-consolidated-original-vnd.txt").read_text("utf-8")
V={}
for line in raw.splitlines():
    if not line or line.startswith("#"):continue
    k,val=line.split()
    assert k not in V and val.lstrip("-").isdigit(),line
    V[k]=int(val)
assert len(V)==104
q1=next(x for x in obj["items"] if x["period"]=="2025-Q1" and "hợp nhất" in x["report_type"])
q2=next(x for x in obj["items"] if x["period"]=="2025-Q2" and "hợp nhất" in x["report_type"])
s=q2["source_validation"]
assert q1["verification_status"]=="issuer_original_signed_visual_verified_b01_b02_b03_q1_2025_exact_VND"
assert q2["verification_status"]=="issuer_original_signed_visual_verified_b01_b02_b03_h1_2025_and_q2_standalone_cash"
assert q1["unit"]==q2["unit"]=="triệu VND"
assert s["manually_visual_reviewed"] and s["source_scope_verified"] and s["source_scope"]=="consolidated"
assert s["original_source_figures_unit"]=="VND" and s["normalized_unit"]=="triệu VND"
assert s["original_issuer_signed_pdf_sha256"]=="90195e13c974fbadf90004ec9817b9e356c2b9203c2308a8a40c313110b29ec3"
assert (s["original_issuer_signed_pdf_bytes"],s["original_issuer_signed_pdf_pages"])==(13678870,31)
assert (s["original_signed_pdf_recovery_workflow"],s["original_signed_pdf_artifact_id"])==(44680177934,14602749723)
assert s["visually_reviewed_signed_pdf_pages"]==[2,3,4,5,6,7]
assert s["source_6m_cashflow_ytd_subtract_signed_q1"] is True
assert s["source_q1_2025_original_sha256"]==q1["source_validation"]["original_issuer_signed_pdf_sha256"]
assert q2["cashflow_period_basis"]=="quarter" and q2["cashflow_ytd_period_basis"]=="six_months"
assert q2["eps"]==899 and q2["eps_ytd"]==926
assert s["original_B02_current_year_quarter_vs_6m_column_validated"] is True
assert s["source_vnd_exact_checks_count"]==43
assert q2["financial_line_items_extracted_fields"]==q2["financial_line_items_manually_verified_fields"]
assert len(q2["financial_line_items_extracted_fields"])==112
assert set(q2["financial_line_items_extracted_fields"])>=set(V)

def money(row,key):
    assert isinstance(row.get(key),(int,float)),(row["period"],key)
    x=Decimal(str(row[key]))*Decimal(1000000)
    assert x==x.to_integral_value(),(key,x)
    return int(x)
def v(key):return money(q2,key)
def p(key):return money(q1,key)
def vs(*keys):return sum(v(x) for x in keys)
for k,val in V.items():assert v(k)==val,(k,v(k),val)
for key in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure","dividends_paid"):
    V[key]=V[key+"_ytd"]-p(key+"_ytd")
V["cash_beginning"]=p("cash_ending")
for k in V:assert v(k)==V[k],(k,v(k),V[k])
assert len(V)==112
checks={
"b01 total assets":v("total_assets")-vs("current_assets","non_current_assets"),
"b01 liabilities and equity":v("total_assets")-vs("total_liabilities","equity"),
"b01 liability split":v("total_liabilities")-vs("current_liabilities","long_term_liabilities"),
"b01 cash split":v("cash_and_equivalents")-vs("cash_only","cash_equivalents_only"),
"b01 current assets":v("current_assets")-vs("cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"b01 non current assets":v("non_current_assets")-vs("long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
"b01 receivables":v("short_term_receivables")-(16047855471224+407942921553+795275395222-1006289922462+603537767),
"b01 investments":v("short_term_investments")-(6691022742-2044654919+21235939425782),
"b01 inventory":v("inventory")-(17005741331830-215834711606),
"b01 fixed assets":v("fixed_assets")-(10679134654700+2413791144464),
"b01 long-term investments":v("long_term_financial_investments")-(1630205998696+260411708977-118818967382+1000000000000),
"b01 other noncurrent":v("other_non_current_assets")-(3209877246093+172321198704+3967696111),
"b01 equity parent-nci":v("equity")-(25017642033313+v("non_controlling_interest_equity")),
"b02 Q2 gross sales":v("gross_revenue")-vs("revenue_deductions","revenue"),
"b02 Q2 gross profit":v("revenue")-vs("cost_of_goods_sold","gross_profit"),
"b02 Q2 operating":v("gross_profit")+v("financial_income")-vs("financial_expense","selling_expense","admin_expense")+v("profit_from_associates")-v("operating_profit"),
"b02 Q2 other":v("other_income")-vs("other_expense","other_profit"),
"b02 Q2 pretax":vs("operating_profit","other_profit")-v("pretax_profit"),
"b02 Q2 income tax":vs("income_tax_current","income_tax_deferred")-v("income_tax"),
"b02 Q2 net":v("pretax_profit")-vs("income_tax","net_profit"),
"b02 Q2 attribution":v("net_profit")-vs("net_profit_attributable","non_controlling_interest_profit"),
"b02 H1 gross revenue":v("gross_revenue_ytd")-vs("revenue_deductions_ytd","revenue_ytd"),
"b02 H1 gross profit":v("revenue_ytd")-vs("cost_of_goods_sold_ytd","gross_profit_ytd"),
"b02 H1 operating":v("gross_profit_ytd")+v("financial_income_ytd")-vs("financial_expense_ytd","selling_expense_ytd","admin_expense_ytd")+v("profit_from_associates_ytd")-v("operating_profit_ytd"),
"b02 H1 other":v("other_income_ytd")-vs("other_expense_ytd","other_profit_ytd"),
"b02 H1 pretax":vs("operating_profit_ytd","other_profit_ytd")-v("pretax_profit_ytd"),
"b02 H1 income tax":vs("income_tax_current_ytd","income_tax_deferred_ytd")-v("income_tax_ytd"),
"b02 H1 net":v("pretax_profit_ytd")-vs("income_tax_ytd","net_profit_ytd"),
"b02 H1 attribution":v("net_profit_ytd")-vs("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
"b03 pretax equals B02":v("cf_pretax_profit_ytd")-v("pretax_profit_ytd"),
"b03 pre WC":vs("cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v("cf_operating_before_working_capital_ytd"),
"b03 CFO":vs("cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_trading_securities_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_receipts_ytd","cf_other_operating_payments_ytd")-v("operating_cash_flow_ytd"),
"b03 CFI":vs("capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_other_longterm_investment_ytd","cf_other_investment_recovery_ytd","cf_interest_dividends_received_ytd")-v("investing_cash_flow_ytd"),
"b03 CFF":vs("cf_share_issue_proceeds_ytd","cf_repurchase_shares_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","cf_finance_lease_repayments_ytd","dividends_paid_ytd")-v("financing_cash_flow_ytd"),
"b03 6m net":vs("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v("net_cash_change_ytd"),
"b03 6m bridge":vs("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v("cash_ending"),
"b03 closing B01":v("cash_and_equivalents")-v("cash_ending"),
}
for key in ("revenue","net_profit","gross_profit","pretax_profit"):
    checks["Q2+Q1 equals H1 "+key]=v(key)+p(key)-v(key+"_ytd")
checks["q2 quarterly cash sum"]=vs("operating_cash_flow","investing_cash_flow","financing_cash_flow")-v("net_cash_change")
checks["q2 quarterly cash bridge"]=vs("cash_beginning","net_cash_change","foreign_exchange_effect")-v("cash_ending")
assert len(checks)==43,len(checks)
assert all(not difference for difference in checks.values()),{k:n for k,n in checks.items() if n}
assert s["source_financial_fields_count"]==112
assert all(int(s["q2_standalone_cashflow_exact_vnd"][k])==v({
"operating":"operating_cash_flow","investing":"investing_cash_flow","financing":"financing_cash_flow",
"net":"net_cash_change","fx":"foreign_exchange_effect","beginning":"cash_beginning",
"ending":"cash_ending","capex":"capital_expenditure","dividends":"dividends_paid"}[k]) for k in s["q2_standalone_cashflow_exact_vnd"])
assert v("operating_cash_flow")==2106791853375
assert v("investing_cash_flow")==-1021432844145
assert v("financing_cash_flow")==-792003743906
assert v("net_cash_change")==293355265324
assert v("foreign_exchange_effect")==24995968933
assert v("cash_beginning")==10446733576792
assert v("cash_ending")==10765084811049
assert (q2["roa"],q2["roe"])==(6.54,18.97)
parent=next(x for x in obj["items"] if x["period"]=="2026-Q3" and x["source_validation"].get("scope")=="parent_company")
assert parent["source_validation"]["b03_cashflow_discrepancy_vnd"]=="87654015000"
assert parent.get("financing_cash_flow") is None
print("PASS: PLX consolidated Q2 2025 signed source 31p B01 pp2-4 B02 p5 6M B03 pp6-7, 104 original VND + 8 Q2 derived =112 fields, 43 exact source identities zero VND; PLX parent Q3 issuer anomaly still blocked.")
