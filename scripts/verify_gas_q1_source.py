#!/usr/bin/env python3
"""Regression on GAS Q1/2025 issuer B01/B02/B03, after segment disclosure correction.

Numerical fields are stored as million VND, while PDF shows raw VND.
Do NOT imply visual screenshot verification: this is PDF-text + exact arithmetic.
"""
import json
from decimal import Decimal
from pathlib import Path

path=Path(__file__).resolve().parents[1]/"data/financials-GAS.json"
obj=json.loads(path.read_text(encoding="utf-8"))
r=next(x for x in obj["items"] if x["period"]=="2025-Q1")
assert "hợp nhất" in r["report_type"].lower()
assert r["unit"]=="triệu VND"
assert r["source_validation"]["manually_visual_reviewed"] is False
assert "source_amendment_url" in r["source_validation"]
assert "Thuyết minh 37" in r["source_validation"]["source_amendment_scope"]
assert all(v=="0" for v in r["source_validation"]["exact_identity_residuals_vnd"].values())
assert len(r["source_validation"]["exact_identity_residuals_vnd"]) == 15

def n(field): return Decimal(str(r[field]))*Decimal(1000000)
def eq(left,right,title): assert left==right,(title,left-right)

eq(n("current_assets")+n("non_current_assets"),n("total_assets"),"B01 assets")
eq(n("total_liabilities")+n("equity"),n("total_assets"),"B01 sources")
eq(n("current_liabilities")+n("long_term_liabilities"),n("total_liabilities"),"B01 liabilities")
eq(n("revenue")-n("cost_of_goods_sold"),n("gross_profit"),"B02 gross")
eq(n("gross_profit")+n("financial_income")-n("financial_expense")+n("share_of_profit_in_associates")-n("selling_expense")-n("admin_expense"),n("operating_profit"),"B02 operating")
eq(n("other_income")-n("other_expense"),n("other_profit"),"B02 other")
eq(n("operating_profit")+n("other_profit"),n("pretax_profit"),"B02 pretax")
eq(n("income_tax_current")+n("income_tax_deferred"),n("income_tax"),"B02 taxes")
eq(n("pretax_profit")-n("income_tax"),n("net_profit"),"B02 net")
eq(n("net_profit_attributable")+n("non_controlling_interest_profit"),n("net_profit"),"B02 parent NCI")
eq(n("operating_cash_flow")+n("investing_cash_flow")+n("financing_cash_flow"),n("net_cash_change"),"B03 cash flows")
eq(n("cash_beginning")+n("net_cash_change")+n("foreign_exchange_effect"),n("cash_ending"),"B03 cash bridge")
eq(n("cash_and_equivalents"),n("cash_ending"),"B01 closing cash vs B03")
assert r["eps"]==1177 and r["cashflow_period_basis"]=="year_to_date"
assert r["source_validation"]["exact_identity_residuals_vnd"]["B03 investing components"]=="0"
assert r["source_validation"]["exact_identity_residuals_vnd"]["B03 finance components"]=="0"
assert all(r[name] < 0 for name in ("income_tax_deferred","investing_cash_flow","capital_expenditure","foreign_exchange_effect"))
assert "financial_line_items_manually_verified_fields" not in r, "No visual check: do not mark manually verified"
print("PASS: GAS Q1 2025 consolidated B01/B02/B03, 42 source fields, 15/15 exact VND identities, original correction scoped to note 37.")
