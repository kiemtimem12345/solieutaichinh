#!/usr/bin/env python3
"""Verify VDS securities consolidated 2026 Q3 from issuer B01/B02/B03 scans.

VDS B02 is securities revenue/expenses, not manufacturing turnover or COGS.
B03 year-to-date and client brokerage cash are separate from company cash.
Nothing in this test invents stand-alone Q3 cash flows.
"""
import json
from decimal import Decimal
from pathlib import Path

data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-VDS.json").read_text("utf-8"))
records=[x for x in data["items"] if x["period"]=="2026-Q3"]
assert len(records)==1, records
q=records[0]
def v(k):
    return int((Decimal(str(q[k]))*Decimal(1000000)).to_integral_exact())
def s(*names):
    return sum(v(k) for k in names)
assert q["symbol"]=="VDS" and "hợp nhất" in q["report_type"].lower()
assert q["unit"]=="triệu VND" and q["eps"]==-382 and q["diluted_eps"]==-382
assert q["roa"] is None and q["roe"] is None
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["source_unit"]=="VND"
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_ytd_standalone_cash_deferred"
assert q["cashflow_period_basis"]=="year_to_date"
assert q["q3_standalone_cashflow_status"].startswith("deferred")
assert q.get("operating_cash_flow") is None and q.get("financing_cash_flow") is None and q.get("investing_cash_flow") is None
assert len(q["financial_line_items_extracted_fields"])==90
assert set(q["financial_line_items_extracted_fields"])==set(q["financial_line_items_manually_verified_fields"])
assert not any(x["period"] < "2025-Q1" for x in data["items"])
assert len(data["items"])==7

source_values={
 "total_assets":7424891063002,"total_liabilities":4612624799039,"equity":2812266263963,
 "current_assets":6161151738346,"non_current_assets":1263739324656,
 "current_liabilities":4611870220727,"long_term_liabilities":754578312,
 "cash_and_equivalents":871526568802,"cash_only":539526568802,"cash_equivalents_only":332000000000,
 "financial_current_assets":6119959710849,"other_current_assets":41192027497,
 "financial_noncurrent_assets":1173156281212,"fixed_assets":43416435592,
 "construction_in_progress":653595750,"other_noncurrent_assets":46513012102,
 "revenue":192250618894,"revenue_ytd":651097043132,
 "securities_operating_expense":260004749624,"securities_operating_expense_ytd":601673487827,
 "financial_income":2045269763,"financial_expense":20886146850,"admin_expense":46615307188,
 "operating_profit":-133210315005,"other_profit":-711398719,"pretax_profit":-133921713724,
 "income_tax":-21812358624,"income_tax_current":-20068023340,
 "income_tax_deferred":-1744335284,"net_profit":-112109355100,
 "net_profit_attributable":-103872007558,"non_controlling_interest_profit":-8237347542,
 "pretax_profit_ytd":-127244377917,"net_profit_ytd":-108501210335,
 "operating_cash_flow_ytd":284201617114,"investing_cash_flow_ytd":-89200647564,
 "financing_cash_flow_ytd":-320450000000,"net_cash_change_ytd":-125449030450,
 "cash_beginning_reported_ytd":996975599252,"cash_ending":871526568802,
 "capital_expenditure_ytd":-1517717300,"financing_borrowing_proceeds_ytd":6824000000000,
 "financing_debt_repayments_ytd":-7144450000000,
 "client_brokerage_cash_change_ytd":-1112807615606,
 "client_brokerage_cash_beginning_ytd":1748126020118,
 "client_brokerage_cash_ending_ytd":635318404512
}
for k,amount in source_values.items():
    assert v(k)==amount,(k,v(k),amount)
checks={
 "b01_assets":v("total_assets")-s("total_liabilities","equity"),
 "b01_assets_classes":v("total_assets")-s("current_assets","non_current_assets"),
 "b01_liability_classes":v("total_liabilities")-s("current_liabilities","long_term_liabilities"),
 "b01_current_assets":v("current_assets")-s("financial_current_assets","other_current_assets"),
 "b01_noncurrent_assets":v("non_current_assets")-s("financial_noncurrent_assets","fixed_assets","construction_in_progress","other_noncurrent_assets"),
 "b01_cash_components":v("cash_and_equivalents")-s("cash_only","cash_equivalents_only"),
 "b02_operating":v("operating_profit")-(v("revenue")+v("financial_income")-s("securities_operating_expense","financial_expense","admin_expense")),
 "b02_other":v("other_profit")-v("other_income")+v("other_expense"),
 "b02_pretax":v("pretax_profit")-s("operating_profit","other_profit"),
 "b02_tax":v("income_tax")-s("income_tax_current","income_tax_deferred"),
 "b02_net":v("net_profit")-v("pretax_profit")+v("income_tax"),
 "b02_attributable":v("net_profit")-s("net_profit_attributable","non_controlling_interest_profit"),
 "b02_ytd_other":v("pretax_profit_ytd")-v("operating_profit_ytd")-(-705379319),
 "b02_ytd_net":v("net_profit_ytd")-v("pretax_profit_ytd")+v("income_tax_ytd"),
 "b02_ytd_attributable":v("net_profit_ytd")-s("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
 "b03_net":v("net_cash_change_ytd")-s("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"),
 "b03_cash":v("cash_ending")-s("cash_beginning_reported_ytd","net_cash_change_ytd"),
 "b03_b01_cash":v("cash_ending")-v("cash_and_equivalents"),
 "b03_cfi":v("investing_cash_flow_ytd")-s("capital_expenditure_ytd","investing_asset_disposal_proceeds_ytd","investing_capital_contributions_ytd","investing_recovery_of_capital_ytd","investing_dividends_received_ytd"),
 "b03_cff":v("financing_cash_flow_ytd")-s("financing_borrowing_proceeds_ytd","financing_debt_repayments_ytd"),
 "client_cash_is_separate":v("client_brokerage_cash_ending_ytd")-s("client_brokerage_cash_beginning_ytd","client_brokerage_cash_change_ytd"),
}
assert len(checks)==21
assert all(value==0 for value in checks.values()),checks
assert set(checks)==set(q["source_validation"]["statement_identity_residuals_vnd"])
assert all(raw=="0" for raw in q["source_validation"]["statement_identity_residuals_vnd"].values())
assert v("client_brokerage_cash_ending_ytd") != v("cash_ending")
assert v("net_profit") < 0 and v("income_tax") < 0
print("PASS VDS 2026Q3 consolidated issuer B01/B02/B03: 90 fields, 21 exact-VND identities, separate off-balance client cash, no invented Q3 standalone cash")
