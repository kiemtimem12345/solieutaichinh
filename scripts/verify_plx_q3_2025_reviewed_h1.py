#!/usr/bin/env python3
"""Validate PLX consolidated Q3 2025 signed original with KPMG reviewed H1 vintage.

Q3 standalone B02 source printed vs 9M source; cash Q3 only from source 9M
minus signed KPMG-reviewed H1 (29-Aug-2025), NOT first-issued Q2 H1.
Two B02 source lines of other income and expense differ equally by VND
858,475,922 between 9M minus reviewed H1 and printed Q3 quarter; they cancel
net profit. Do NOT silently rewrite printed source amounts. Dividend quarter
is withheld because signed 9M less reviewed H1 is positive for "cash paid".
"""
import json
from decimal import Decimal
from pathlib import Path
root=Path(__file__).resolve().parents[1]
obj=json.loads((root/"data/financials-PLX.json").read_text(encoding="utf-8"))
q=next(r for r in obj["items"] if r["period"]=="2025-Q3" and "hợp nhất" in r["report_type"].lower())
p=next(r for r in obj["items"] if r["period"]=="2025-Q2" and "hợp nhất" in r["report_type"].lower())
parent=next(r for r in obj["items"] if r["period"]=="2026-Q3" and r["source_validation"].get("scope")=="parent_company")
s=q["source_validation"]
def raw(filename):
 d={}
 for line in (root/"reports/source-audits"/filename).read_text(encoding="utf-8").splitlines():
  if not line or line.startswith("#"):continue
  k,n=line.split()
  assert k not in d and n.lstrip("-").isdigit(),line
  d[k]=int(n)
 return d
V=raw("PLX-2025Q3-consolidated-original-vnd.txt")
H=raw("PLX-2025H1-reviewed-consolidated-original-vnd.txt")
assert len(V)==104 and len(H)==59
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_reviewed_h1_q3cash_with_other_income_expense_and_dividend_vintage_exceptions"
assert s["manually_visual_reviewed"] is True and s["full_b01_b02_b03_visual_reviewed"] is True
assert s["source_scope"]=="consolidated" and s["normalized_to"]=="triệu VND"
assert s["original_issuer_signed_pdf_sha256"]=="012d34a3166e67ca61de8c7442bb7474479853b55f105b30c60347ee4e40453c"
assert s["original_issuer_signed_pdf_bytes"]==13678774 and s["original_issuer_signed_pdf_pages"]==31
assert s["original_signed_pdf_recovery_run"]==44681702136 and s["original_signed_pdf_artifact_id"]==14604826033
assert s["original_visually_reviewed_pdf_pages"]==[2,3,4,5,6,7]
assert s["reviewed_h1_original_sha256"]=="c44c230d3eb53b832bb5393cce4cabe9d491980e1b016201823b0e9e4f733bb5"
assert s["reviewed_h1_original_bytes"]==16596635 and s["reviewed_h1_original_pages"]==75
assert s["reviewed_h1_signed_on"]=="2025-08-29"
assert s["reviewed_h1_recovery_run"]==44682724580 and s["reviewed_h1_recovery_artifact_id"]==14605067414
assert s["reviewed_h1_original_B02_visual_pages"]==[10,11]
assert s["reviewed_h1_original_B03_visual_pages"]==[12,13,14]
assert s["q3_quarter_cashflow_uses_reviewed_h1_not_prior_q2"] is True
assert s["q2_source_original_remains_unchanged"] is True
assert q["eps"]==369 and q["eps_ytd"]==1330
assert q["cashflow_period_basis"]=="quarter" and q["cashflow_ytd_period_basis"]=="nine_months"
assert set(q["financial_line_items_manually_verified_fields"])==set(q["financial_line_items_extracted_fields"])
assert len(q["financial_line_items_extracted_fields"])==111
def money(row,k):
 val=Decimal(str(row[k]))*Decimal(1000000)
 assert val==val.to_integral_value(),(row["period"],k,val)
 return int(val)
def v(k):return V[k]
def h(k):return H[k]
def sumv(*keys):return sum(v(k) for k in keys)
def sumh(*keys):return sum(h(k) for k in keys)
for k,value in V.items():
 assert money(q,k)==value,(k,money(q,k),value)
assert s["original_financial_source_fields_count"]==104
assert p["verification_status"]=="issuer_original_signed_visual_verified_b01_b02_b03_h1_2025_and_q2_standalone_cash"
assert p["source_validation"]["original_issuer_signed_pdf_sha256"]=="90195e13c974fbadf90004ec9817b9e356c2b9203c2308a8a40c313110b29ec3"
# Original signed Q3 internal B01/B02/B03 source equations independent of
# reviewed H1 or previously published Q2 values.
c={
 "b01_assets":v("total_assets")-sumv("current_assets","non_current_assets"),
 "b01_sources":v("total_assets")-sumv("total_liabilities","equity"),
 "b01_liabilities":v("total_liabilities")-sumv("current_liabilities","long_term_liabilities"),
 "b01_current_components":v("current_assets")-sumv("cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
 "b01_noncurrent_components":v("non_current_assets")-sumv("long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
 "b01_cash_split":v("cash_and_equivalents")-sumv("cash_only","cash_equivalents_only"),
 "b02_q3_sales":v("gross_revenue")-sumv("revenue_deductions","revenue"),
 "b02_q3_gross":v("revenue")-sumv("cost_of_goods_sold","gross_profit"),
 "b02_q3_operating":v("gross_profit")+v("financial_income")+v("profit_from_associates")-sumv("financial_expense","selling_expense","admin_expense","operating_profit"),
 "b02_q3_other":v("other_income")-sumv("other_expense","other_profit"),
 "b02_q3_pretax":sumv("operating_profit","other_profit")-v("pretax_profit"),
 "b02_q3_tax":sumv("income_tax_current","income_tax_deferred")-v("income_tax"),
 "b02_q3_pat":v("pretax_profit")-sumv("income_tax","net_profit"),
 "b02_q3_attr":v("net_profit")-sumv("net_profit_attributable","non_controlling_interest_profit"),
 "b02_9m_sales":v("gross_revenue_ytd")-sumv("revenue_deductions_ytd","revenue_ytd"),
 "b02_9m_gross":v("revenue_ytd")-sumv("cost_of_goods_sold_ytd","gross_profit_ytd"),
 "b02_9m_operating":v("gross_profit_ytd")+v("financial_income_ytd")+v("profit_from_associates_ytd")-sumv("financial_expense_ytd","selling_expense_ytd","admin_expense_ytd","operating_profit_ytd"),
 "b02_9m_other":v("other_income_ytd")-sumv("other_expense_ytd","other_profit_ytd"),
 "b02_9m_pretax":sumv("operating_profit_ytd","other_profit_ytd")-v("pretax_profit_ytd"),
 "b02_9m_tax":sumv("income_tax_current_ytd","income_tax_deferred_ytd")-v("income_tax_ytd"),
 "b02_9m_pat":v("pretax_profit_ytd")-sumv("income_tax_ytd","net_profit_ytd"),
 "b02_9m_attr":v("net_profit_ytd")-sumv("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
 "b03_b02_pretax":v("cf_pretax_profit_ytd")-v("pretax_profit_ytd"),
 "b03_before_wc":sumv("cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v("cf_operating_before_working_capital_ytd"),
 "b03_cfo":sumv("cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_trading_securities_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_receipts_ytd","cf_other_operating_payments_ytd")-v("operating_cash_flow_ytd"),
 "b03_cfi":sumv("capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_other_longterm_investment_ytd","cf_other_investment_recovery_ytd","cf_interest_dividends_received_ytd")-v("investing_cash_flow_ytd"),
 "b03_cff":sumv("cf_share_issue_proceeds_ytd","cf_repurchase_shares_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","cf_finance_lease_repayments_ytd","dividends_paid_ytd")-v("financing_cash_flow_ytd"),
 "b03_net":sumv("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v("net_cash_change_ytd"),
 "b03_fx_bridge":sumv("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v("cash_ending"),
 "b03_end_B01":v("cash_and_equivalents")-v("cash_ending")
}
assert len(c)==30
assert all(x==0 for x in c.values()),{k:x for k,x in c.items() if x}
assert {k:str(x) for k,x in c.items()}==s["signed_original_vnd_checks"]
# Independently verify KPMG-reviewed H1 source before use as a comparator.
checks={
 "h1_revenue":h("gross_revenue_ytd")-sumh("revenue_deductions_ytd","revenue_ytd"),
 "h1_gross":h("revenue_ytd")-sumh("cost_of_goods_sold_ytd","gross_profit_ytd"),
 "h1_operating":sumh("gross_profit_ytd","financial_income_ytd","profit_from_associates_ytd")-sumh("financial_expense_ytd","selling_expense_ytd","admin_expense_ytd","operating_profit_ytd"),
 "h1_other":h("other_income_ytd")-sumh("other_expense_ytd","other_profit_ytd"),
 "h1_pretax":sumh("operating_profit_ytd","other_profit_ytd")-h("pretax_profit_ytd"),
 "h1_tax":sumh("income_tax_current_ytd","income_tax_deferred_ytd")-h("income_tax_ytd"),
 "h1_net":h("pretax_profit_ytd")-sumh("income_tax_ytd","net_profit_ytd"),
 "h1_pat_attr":h("net_profit_ytd")-sumh("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
 "h1_b03_pretax":h("pretax_profit_ytd")-h("cf_pretax_profit_ytd"),
 "h1_b03_pre_wc":sumh("cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-h("cf_operating_before_working_capital_ytd"),
 "h1_b03_cfo":sumh("cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_trading_securities_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_receipts_ytd","cf_other_operating_payments_ytd")-h("operating_cash_flow_ytd"),
 "h1_b03_cfi":sumh("capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_other_longterm_investment_ytd","cf_other_investment_recovery_ytd","cf_interest_dividends_received_ytd")-h("investing_cash_flow_ytd"),
 "h1_b03_cff":sumh("cf_share_issue_proceeds_ytd","cf_repurchase_shares_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","cf_finance_lease_repayments_ytd","dividends_paid_ytd")-h("financing_cash_flow_ytd"),
 "h1_b03_net":sumh("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-h("net_cash_change_ytd"),
 "h1_b03_bridge":sumh("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-h("cash_ending")
}
assert len(checks)==15
assert all(x==0 for x in checks.values()),{k:x for k,x in checks.items() if x}
assert {k:str(x) for k,x in checks.items()}==s["reviewed_h1_b02_b03_vnd_checks"]
period_fields=["operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure"]
d={k:v(k+"_ytd")-h(k+"_ytd") for k in period_fields}
d["cash_beginning"]=h("cash_ending")
d["cash_ending"]=v("cash_ending")
for k,val in d.items():assert money(q,k)==val,(k,money(q,k),val)
quarter={
 "q3_cfo":v("operating_cash_flow_ytd")-h("operating_cash_flow_ytd")-d["operating_cash_flow"],
 "q3_cfi":v("investing_cash_flow_ytd")-h("investing_cash_flow_ytd")-d["investing_cash_flow"],
 "q3_cff":v("financing_cash_flow_ytd")-h("financing_cash_flow_ytd")-d["financing_cash_flow"],
 "q3_net":v("net_cash_change_ytd")-h("net_cash_change_ytd")-d["net_cash_change"],
 "q3_fx":v("foreign_exchange_effect_ytd")-h("foreign_exchange_effect_ytd")-d["foreign_exchange_effect"],
 "q3_capex":v("capital_expenditure_ytd")-h("capital_expenditure_ytd")-d["capital_expenditure"],
 "q3_start":d["cash_beginning"]-h("cash_ending"),
 "q3_net_components":d["operating_cash_flow"]+d["investing_cash_flow"]+d["financing_cash_flow"]-d["net_cash_change"],
 "q3_cash_bridge":d["cash_beginning"]+d["net_cash_change"]+d["foreign_exchange_effect"]-d["cash_ending"]
}
assert len(quarter)==9 and all(x==0 for x in quarter.values())
assert {k:str(x) for k,x in quarter.items()}==s["q3_standalone_cashflow_exact_checks"]
assert d=={"operating_cash_flow":-799826559974,"investing_cash_flow":-1434662126272,
 "financing_cash_flow":4058999584829,"net_cash_change":1824510898583,
 "foreign_exchange_effect":21409869707,"capital_expenditure":-209747902082,
 "cash_beginning":10770637171668,"cash_ending":12616557939958}
B02=["gross_revenue","revenue_deductions","revenue","cost_of_goods_sold","gross_profit",
 "financial_income","financial_expense","interest_expense","profit_from_associates",
 "selling_expense","admin_expense","operating_profit","other_income","other_expense",
 "other_profit","pretax_profit","income_tax_current","income_tax_deferred",
 "income_tax","net_profit","net_profit_attributable","non_controlling_interest_profit"]
diffs={k:v(k+"_ytd")-h(k+"_ytd")-v(k) for k in B02}
assert len(diffs)==22
assert {k:val for k,val in diffs.items() if val}=={"other_income":-858475922,"other_expense":-858475922}
assert {k:str(val) for k,val in diffs.items()}==s["original_q3_B02_quarter_vs_9m_minus_reviewed_h1_differences_vnd"]
assert diffs["other_income"]-diffs["other_expense"]==0
assert diffs["other_profit"]==diffs["net_profit"]==diffs["revenue"]==0
def previous(key):return money(p,key)
historical={
 "revenue":h("revenue_ytd")-previous("revenue_ytd"),
 "net_profit":h("net_profit_ytd")-previous("net_profit_ytd"),
 "operating_cash_flow":h("operating_cash_flow_ytd")-previous("operating_cash_flow_ytd"),
 "investing_cash_flow":h("investing_cash_flow_ytd")-previous("investing_cash_flow_ytd"),
 "financing_cash_flow":h("financing_cash_flow_ytd")-previous("financing_cash_flow_ytd"),
 "net_cash_change":h("net_cash_change_ytd")-previous("net_cash_change_ytd"),
 "foreign_exchange_effect":h("foreign_exchange_effect_ytd")-previous("foreign_exchange_effect_ytd"),
 "cash_ending":h("cash_ending")-previous("cash_ending")
}
assert {k:str(val) for k,val in historical.items()}==s["original_q2_H1_2025_vs_reviewed_H1_2025_source_vintage_differences_vnd"]
assert historical["revenue"]==-515395599706 and historical["net_profit"]==56092433583
assert historical["cash_ending"]==5552360619
dividends=v("dividends_paid_ytd")-h("dividends_paid_ytd")
assert dividends==42990997073 and dividends>0
assert int(s["dividends_paid_q3_ytd_minus_reviewed_h1_vnd"])==dividends
assert q.get("dividends_paid") is None
assert s["dividends_paid_q3_quarter_status"].startswith("UNVERIFIED:")
assert s["q3_source_accounting_reconciliation_status"].startswith("PASS signed Q3")
assert (q["roa"],q["roe"])==(3.16,9.89)
assert parent["source_validation"]["b03_cashflow_discrepancy_vnd"]=="87654015000"
assert parent.get("financing_cash_flow") is None
print("PASS: PLX Q3 2025 signed 31p original B01 B02 B03, 104 exact source VND fields and 30 identities; KPMG-reviewed signed H1 75p source 59 exact fields 15 identities; Q3 cash 9/9 standalone identities zero VND, PAT/revenue reviewed H1 vintage reconciles, other-income/expense 858475922 VND dual exception isolated, Q3 dividend detail withheld; parent PLX Q3 2026 remains blocked.")
