#!/usr/bin/env python3
"""Exact-VND IDC consolidated 2026-Q3 issuer signed B01/B02 and 9M B03.

70-page original BSC-distributed HNX PDF, hashed exactly against Vietstock
archived PDF. Original screenshots of PDF pages 8-15 independently checked.
All financial calculations work in integer VND, never rounded million VND.
"""
import json
from decimal import Decimal
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "data" / "financials-IDC.json"
doc = json.loads(p.read_text("utf-8"))
items = [r for r in doc["items"] if r["period"] == "2026-Q3" and "hợp nhất" in r["report_type"].lower()]
assert len(items) == 1, ("IDC Q3 consolidated unique",len(items))
q = items[0]
def v(k):
    return int((Decimal(str(q[k])) * Decimal(1000000)).to_integral_exact())
def s(*keys):
    return sum(v(k) for k in keys)

assert q["symbol"] == "IDC"
assert q["unit"] == "triệu VND"
assert q["eps"] == 1181 and q["diluted_eps"] == 1181
assert q["eps_ytd"] == 3290
assert q["roa"] is None and q["roe"] is None
assert q["cashflow_period_basis"] == "year_to_date"
assert q["verification_status"] == "issuer_original_visual_verified_b01_b02_b03_9m_ytd_q3_standalone_cash_deferred"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["source_scope"].startswith("consolidated only")
assert q["source_validation"]["issuer_pdf_sha256"] == "dde75e3efe8a569a0d264b27f7d7a0d8a4edb4abdf22a56144e0847f2c8dc790"
assert q["source_validation"]["issuer_pdf_pages"] == 70
assert q["source_validation"]["reviewed_page_numbers"] == [8,9,10,11,12,13,14,15]
assert q["source_validation"]["mirrored_consolidated_pdf_matches_issuer_sha256"] is True
assert q["q3_standalone_cashflow_status"].startswith("deferred")
assert all(q.get(k) is None for k in (
    "operating_cash_flow", "investing_cash_flow", "financing_cash_flow",
    "net_cash_change", "cash_beginning", "foreign_exchange_effect",
    "capital_expenditure", "dividends_paid"))
assert len(q["financial_line_items_extracted_fields"]) == 105
assert set(q["financial_line_items_extracted_fields"]) == set(q["financial_line_items_manually_verified_fields"])
assert len(doc["items"]) == 7
assert not any(r["period"] < "2025-Q1" for r in doc["items"])

EXPECTED = {
    "total_assets": 23631671909723,
    "current_assets": 16599453089891,
    "non_current_assets": 7032218819832,
    "total_liabilities": 14273143387664,
    "current_liabilities": 5159493652033,
    "long_term_liabilities": 9113649735631,
    "equity": 9358528522059,
    "cash_and_equivalents": 469934018621,
    "cash_only": 176602664768,
    "cash_equivalents_only": 293331353853,
    "short_term_investments": 6574446666848,
    "short_term_receivables": 1306232213691,
    "inventory": 8160746512715,
    "investment_property": 2623257353393,
    "fixed_assets": 2785732914155,
    "non_controlling_interest_equity": 2103161758828,
    "gross_revenue": 2075622272669,
    "revenue_deductions": 47242778,
    "revenue": 2075575029891,
    "cost_of_goods_sold": 1403796161144,
    "gross_profit": 671778868747,
    "financial_income": 154229863294,
    "financial_expense": 52840083513,
    "selling_expense": 19889816498,
    "admin_expense": 85810249675,
    "operating_profit": 667187222079,
    "pretax_profit": 673834389916,
    "net_profit": 540374922785,
    "net_profit_attributable": 492839952222,
    "non_controlling_interest_profit": 47534970563,
    "revenue_ytd": 5831589049869,
    "cost_of_goods_sold_ytd": 3922065492542,
    "pretax_profit_ytd": 1927066885420,
    "net_profit_ytd": 1541615910123,
    "net_profit_attributable_ytd": 1373246282153,
    "operating_cash_flow_ytd": 211600221432,
    "investing_cash_flow_ytd": 505984662907,
    "financing_cash_flow_ytd": -801577203462,
    "net_cash_change_ytd": -83992319123,
    "cash_beginning_reported_ytd": 553943475131,
    "foreign_exchange_effect_ytd": -17137387,
    "cash_ending": 469934018621,
    "capital_expenditure_ytd": -357115441830,
    "dividends_paid_ytd": -710532693375,
}
for key,amount in EXPECTED.items():
    assert v(key) == amount, (key,v(key),amount)

checks = {
"balance": v("total_assets") - s("total_liabilities","equity"),
"assets_classes": v("total_assets") - s("current_assets","non_current_assets"),
"debt_classes": v("total_liabilities") - s("current_liabilities","long_term_liabilities"),
"cash_split": v("cash_and_equivalents") - s("cash_only","cash_equivalents_only"),
"current_asset_classes": v("current_assets") - s("cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"noncurrent_asset_classes": v("non_current_assets") - s("long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
"equity_classes": v("equity") - s("share_capital","share_premium","other_owner_capital","asset_revaluation_difference","development_investment_fund","retained_earnings","non_controlling_interest_equity"),
"net_revenue": v("gross_revenue") - v("revenue_deductions") - v("revenue"),
"gross_profit": v("revenue") - v("cost_of_goods_sold") - v("gross_profit"),
"operating_profit": v("gross_profit") + v("financial_income") - v("financial_expense") - v("selling_expense") - v("admin_expense") + v("profit_from_associates") - v("operating_profit"),
"other_profit": v("other_income") - v("other_expense") - v("other_profit"),
"pretax_profit": v("operating_profit") + v("other_profit") - v("pretax_profit"),
"tax_components": v("income_tax") - s("income_tax_current","income_tax_deferred"),
"net_profit": v("pretax_profit") - v("income_tax") - v("net_profit"),
"net_parent_nci": v("net_profit") - s("net_profit_attributable","non_controlling_interest_profit"),
"net_revenue_ytd": v("gross_revenue_ytd") - v("revenue_deductions_ytd") - v("revenue_ytd"),
"gross_profit_ytd": v("revenue_ytd") - v("cost_of_goods_sold_ytd") - v("gross_profit_ytd"),
"operating_profit_ytd": v("gross_profit_ytd") + v("financial_income_ytd") - v("financial_expense_ytd") - v("selling_expense_ytd") - v("admin_expense_ytd") + v("profit_from_associates_ytd") - v("operating_profit_ytd"),
"other_profit_ytd": v("other_income_ytd") - v("other_expense_ytd") - v("other_profit_ytd"),
"pretax_profit_ytd": v("operating_profit_ytd") + v("other_profit_ytd") - v("pretax_profit_ytd"),
"net_profit_ytd": v("pretax_profit_ytd") - v("income_tax_ytd") - v("net_profit_ytd"),
"net_parent_nci_ytd": v("net_profit_ytd") - s("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
"cash_flow_9m_sections": s("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd") - v("net_cash_change_ytd"),
"cash_flow_9m_open_fx_close": s("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd") - v("cash_ending"),
"b01_b03_cash": v("cash_and_equivalents") - v("cash_ending"),
"cash_operating_before_wc": s("cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd") - v("cf_operating_before_working_capital_ytd"),
"cash_operating": s("cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_payments_ytd") - v("operating_cash_flow_ytd"),
"cash_investing": s("capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_interest_dividends_received_ytd") - v("investing_cash_flow_ytd"),
"cash_financing": s("cf_share_issue_proceeds_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","dividends_paid_ytd") - v("financing_cash_flow_ytd"),
}
assert len(checks) == 29
assert all(residual == 0 for residual in checks.values()), checks
assert set(checks) == set(q["source_validation"]["source_identity_residuals_vnd"])
assert all(v == "0" for v in q["source_validation"]["source_identity_residuals_vnd"].values())
assert v("cash_ending") == v("cash_and_equivalents")
print("PASS IDC 2026-Q3 signed original consolidated B01/B02/B03: 105 numeric fields; 29 exact-VND accounting identities, separate Q3 B02 vs 9M B03 and no fabricated Q3-only CFO/CFI/CFF")
