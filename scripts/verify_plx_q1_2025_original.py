#!/usr/bin/env python3
"""Regress PLX consolidated Q1/2025 from signed 53-page source at exact VND.

Visual originals B01 PDF pp2–5, B02 pp6–7 and B03 pp8–10 inspected.
All source currency values are VND, stored as *exact* million VND decimals.
Q1 standalone B03 equals source 3M YTD. Never mix PLX parent scope or other
report vintages. Original SHA256 and GitHub source recovery are immutable.
"""
import json
from decimal import Decimal
from pathlib import Path
obj=json.loads((Path(__file__).resolve().parents[1]/"data/financials-PLX.json").read_text("utf-8"))
q=next(x for x in obj["items"] if x["period"]=="2025-Q1" and "hợp nhất" in x["report_type"])
vld=q["source_validation"]
assert q["unit"]=="triệu VND" and q["symbol"]=="PLX"
assert q["verification_status"]=="issuer_original_signed_visual_verified_b01_b02_b03_q1_2025_exact_VND"
assert vld["manually_visual_reviewed"] is True and vld["source_scope_verified"] is True
assert vld["source_scope"]=="consolidated" and vld["original_source_figures_unit"]=="VND"
assert vld["original_issuer_signed_pdf_sha256"]=="8ebe33f1a2757507aa2db8421fa261a93d6a765a0de9e2e5aee60b1a56460b97"
assert (vld["original_issuer_signed_pdf_bytes"],vld["original_issuer_signed_pdf_pages"])==(1050763,53)
assert vld["original_signed_pdf_recovery_workflow"]==44678708402
assert vld["original_signed_pdf_artifact_id"]==14603706432
assert vld["visually_reviewed_signed_pdf_pages"]==[2,3,4,5,6,7,8,9,10]
assert q["cashflow_period_basis"]=="quarter" and q["cashflow_ytd_period_basis"]=="three_months"
assert len(q["financial_line_items_extracted_fields"])==96
assert q["financial_line_items_manually_verified_fields"]==q["financial_line_items_extracted_fields"]
assert vld["original_source_financial_fields_count"]==96
assert len(vld["statement_vnd_original_exact_checks"])==40
assert all(x=="0" for x in vld["statement_vnd_original_exact_checks"].values())

def v(k):
    assert k in q and isinstance(q[k],(float,int)),k
    x=Decimal(str(q[k]))*Decimal(1000000)
    assert x==x.to_integral_exact(),(k,x)
    return int(x)
def s(*ks):return sum(v(k) for k in ks)
expected={
 "total_assets":80035874441574,
 "current_assets":58986937922224,"non_current_assets":21048936519350,
 "total_liabilities":50515699095191,"current_liabilities":49731701032965,
 "long_term_liabilities":783998062226,"equity":29520175346383,
 "cash_and_equivalents":10446733576792,"cash_only":6918908801180,
 "cash_equivalents_only":3527824775612,"short_term_investments":20016387716915,
 "short_term_receivables":11896134250401,"inventory":15677477473291,
 "fixed_assets":13248957528011,"retained_earnings":4049415332826,
 "gross_revenue":67890171339647,"revenue_deductions":29140851991,
 "revenue":67861030487656,"cost_of_goods_sold":64149128072879,
 "gross_profit":3711902414777,"profit_from_associates":114290656351,
 "financial_income":421762522293,"financial_expense":293602592566,
 "selling_expense":3353223304063,"admin_expense":263607670164,
 "operating_profit":337522026628,"other_profit":20861624931,
 "pretax_profit":358383651559,"income_tax_current":101717149134,
 "income_tax_deferred":45897701886,"income_tax":147614851020,
 "net_profit":210768800539,"net_profit_attributable":133414809920,
 "non_controlling_interest_profit":77353990619,
 "cf_operating_before_working_capital_ytd":1029076382168,
 "operating_cash_flow_ytd":-2549784370445,
 "investing_cash_flow_ytd":-4577483497115,
 "financing_cash_flow_ytd":2647070139831,
 "net_cash_change_ytd":-4480197727729,
 "cash_beginning_reported_ytd":14933068792315,
 "foreign_exchange_effect_ytd":-6137487794,
 "cash_ending":10446733576792,"capital_expenditure_ytd":-190316844600,
 "dividends_paid_ytd":-10079500,
}
for k,e in expected.items():assert v(k)==e,(k,v(k),e)
assert q["eps"]==q["eps_ytd"]==86
checks={
 "assets_minus_classes":v("total_assets")-s("current_assets","non_current_assets"),
 "assets_minus_liabilities_equity":v("total_assets")-s("total_liabilities","equity"),
 "liabilities_minus_classes":v("total_liabilities")-s("current_liabilities","long_term_liabilities"),
 "current_assets_minus_groups":v("current_assets")-s("cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
 "noncurrent_assets_minus_groups":v("non_current_assets")-s("long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
 "cash_split":v("cash_and_equivalents")-s("cash_only","cash_equivalents_only"),
 "short_investments":v("short_term_investments")-(6691022742-2102399521+20011799093694),
 "receivables":v("short_term_receivables")-(11631122792742+383849823679+739787829720-858998819526+372623786),
 "inventory":v("inventory")-(16011682679299-334205206008),
 "fixed_assets":v("fixed_assets")-(10864936586875+2384020941136),
 "long_term_investments":v("long_term_financial_investments")-(1578404696537+260411708977-118798709247+1253400000000),
 "other_long_term_assets":v("other_non_current_assets")-(3156124377783+148076942148+4138239105),
 "equity_parent_NCI":v("equity")-(26147041967064+v("non_controlling_interest_equity")),
 "gross_revenue":v("gross_revenue")-s("revenue_deductions","revenue"),
 "gross_profit":v("revenue")-s("cost_of_goods_sold","gross_profit"),
 "operating_profit":v("gross_profit")+v("financial_income")-s("financial_expense","selling_expense","admin_expense")+v("profit_from_associates")-v("operating_profit"),
 "other_profit":v("other_income")-s("other_expense","other_profit"),
 "pretax_profit":v("operating_profit")+v("other_profit")-v("pretax_profit"),
 "income_tax":s("income_tax_current","income_tax_deferred")-v("income_tax"),
 "after_tax_profit":v("pretax_profit")-s("income_tax","net_profit"),
 "PAT_parent_NCI":v("net_profit")-s("net_profit_attributable","non_controlling_interest_profit"),
 "q1_revenue_equals_ytd":v("revenue")-v("revenue_ytd"),
 "q1_profit_equals_ytd":v("net_profit")-v("net_profit_ytd"),
 "cashflow_pretax_matches_b02":v("pretax_profit")-v("cf_pretax_profit_ytd"),
 "cashflow_profit_before_wc":s("cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v("cf_operating_before_working_capital_ytd"),
 "cashflow_operating":s("cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_trading_securities_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_receipts_ytd","cf_other_operating_payments_ytd")-v("operating_cash_flow_ytd"),
 "cashflow_investing":s("capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_other_longterm_investment_ytd","cf_other_investment_recovery_ytd","cf_interest_dividends_received_ytd")-v("investing_cash_flow_ytd"),
 "cashflow_financing":s("cf_share_issue_proceeds_ytd","cf_repurchase_shares_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","cf_finance_lease_repayments_ytd","dividends_paid_ytd")-v("financing_cash_flow_ytd"),
 "cashflow_total":s("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v("net_cash_change_ytd"),
 "cashflow_begin_fx_end":s("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v("cash_ending"),
 "cashflow_end_equals_B01":v("cash_and_equivalents")-v("cash_ending"),
 "q1_operating_equals_ytd":v("operating_cash_flow")-v("operating_cash_flow_ytd"),
 "q1_investing_equals_ytd":v("investing_cash_flow")-v("investing_cash_flow_ytd"),
 "q1_financing_equals_ytd":v("financing_cash_flow")-v("financing_cash_flow_ytd"),
 "q1_net_cash_equals_ytd":v("net_cash_change")-v("net_cash_change_ytd"),
 "q1_fx_equals_ytd":v("foreign_exchange_effect")-v("foreign_exchange_effect_ytd"),
 "q1_capex_equals_ytd":v("capital_expenditure")-v("capital_expenditure_ytd"),
 "q1_dividends_equals_ytd":v("dividends_paid")-v("dividends_paid_ytd"),
 "q1_cash_begin_equals_reported":v("cash_beginning")-v("cash_beginning_reported_ytd"),
 "q1_cash_bridge":s("cash_beginning","net_cash_change","foreign_exchange_effect")-v("cash_ending"),
}
assert len(checks)==40
assert all(x==0 for x in checks.values()),{k:x for k,x in checks.items() if x}
assert {k:str(x) for k,x in checks.items()}==vld["statement_vnd_original_exact_checks"]
opening_assets=81274634873472
opening_equity=29307974443473
roa=Decimal(4*v("net_profit"))/(Decimal(opening_assets+v("total_assets"))/Decimal(2))*100
roe=Decimal(4*v("net_profit"))/(Decimal(opening_equity+v("equity"))/Decimal(2))*100
assert round(roa,2)==Decimal("1.05") and round(roe,2)==Decimal("2.87")
assert (q["roa"],q["roe"])==(1.05,2.87)
parent=next(r for r in obj["items"] if r["period"]=="2026-Q3" and r["source_validation"].get("scope")=="parent_company")
assert parent["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_printed_cff_arithmetic_anomaly_blocked"
assert parent["source_validation"]["b03_cashflow_discrepancy_vnd"]=="87654015000"
assert parent.get("operating_cash_flow") is None and parent.get("financing_cash_flow") is None
print("PASS: PLX Q1 2025 signed original 53p B01 pp2-5 B02 pp6-7 B03 pp8-10 visual; 96 VND fields and 40 original accounting identities exactly zero VND, ROA 1.05%, parent Q3 CFF still quarantined.")
