#!/usr/bin/env python3
"""Independent exact-VND GAS Q4/2025 source and cross-quarter verifier.

Original scanned PV GAS consolidated 2025 report, PDF pages 4–7.
B02 Q4 = separate Quý IV/Năm nay, B03 Q4 = 12M YTD minus verified 9M YTD.
No automated OCR number is accepted without source-image + arithmetic checks.
"""
import json
from decimal import Decimal
from pathlib import Path

doc = json.loads((Path(__file__).resolve().parents[1] / "data" / "financials-GAS.json").read_text("utf-8"))
rows = {item["period"]: item for item in doc["items"] if item["period"] in ("2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4")}
a, h, n, q = [rows[k] for k in ("2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4")]
def V(r, k):
    return int((Decimal(str(r[k])) * Decimal(1000000)).to_integral_exact())
def b(k):
    return V(q, k)

assert q["unit"] == "triệu VND" and q["eps"] == 558
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["reviewed_pages"] == [4, 5, 6, 7]
assert q["source_validation"]["issuer_pdf_sha256"] == "0bc837f3df86ca06affc9b5547feb37905beac567ab93778210bc9671db10c09"
assert q["roa"] is None and q["roe"] is None
assert q["verification_status"] == "issuer_original_pdf_visual_verified_b01_b02_b03_q4_ytd_derived"

EXPECTED = {
    "total_assets": 93531511866676, "total_liabilities": 25878122748740,
    "equity": 67653389117936, "current_assets": 69861417011215,
    "non_current_assets": 23670094855461, "current_liabilities": 20537033146305,
    "long_term_liabilities": 5341089602435, "cash_and_equivalents": 6876468282085,
    "revenue": 43683070609001, "cost_of_goods_sold": 39890266518331,
    "gross_profit": 3792804090670, "operating_profit": 1763597883667,
    "pretax_profit": 1742972889113, "net_profit": 1387429975481,
    "net_profit_attributable": 1361084899485, "non_controlling_interest_profit": 26345075996,
    "operating_cash_flow_ytd": 13378374377362, "investing_cash_flow_ytd": -6718543866192,
    "financing_cash_flow_ytd": -5352162410986, "net_cash_change_ytd": 1307668100184,
    "cash_beginning_reported_ytd": 5567983431468, "foreign_exchange_effect_ytd": 816750433,
    "cash_ending": 6876468282085,
}
for k, raw_vnd in EXPECTED.items():
    assert b(k) == raw_vnd, (k, b(k), raw_vnd)

checks = {
  "balance": b("total_assets")-b("total_liabilities")-b("equity"),
  "assets_classes": b("total_assets")-b("current_assets")-b("non_current_assets"),
  "current_assets": b("current_assets")-sum((b(k) for k in ("cash_and_equivalents","short_term_investments","short_term_receivables","inventory")))-889281613049,
  "liabilities": b("total_liabilities")-b("current_liabilities")-b("long_term_liabilities"),
  "net_revenue": 43706104716897-23034107896-b("revenue"),
  "gross": b("revenue")-b("cost_of_goods_sold")-b("gross_profit"),
  "operating": b("gross_profit")+b("financial_income")-b("financial_expense")+b("share_of_profit_in_associates")-b("selling_expense")-b("admin_expense")-b("operating_profit"),
  "other": b("other_income")-b("other_expense")-b("other_profit"),
  "pretax": b("operating_profit")+b("other_profit")-b("pretax_profit"),
  "income_tax": b("income_tax_current")+b("income_tax_deferred")-b("income_tax"),
  "net": b("pretax_profit")-b("income_tax")-b("net_profit"),
  "nci": b("net_profit_attributable")+b("non_controlling_interest_profit")-b("net_profit"),
  "cashflow_ytd": b("operating_cash_flow_ytd")+b("investing_cash_flow_ytd")+b("financing_cash_flow_ytd")-b("net_cash_change_ytd"),
  "cashbridge_ytd": b("cash_beginning_reported_ytd")+b("net_cash_change_ytd")+b("foreign_exchange_effect_ytd")-b("cash_ending"),
  "cashflow_q4": b("operating_cash_flow")+b("investing_cash_flow")+b("financing_cash_flow")-b("net_cash_change"),
  "cashbridge_q4": b("cash_beginning")+b("net_cash_change")+b("foreign_exchange_effect")-b("cash_ending"),
  "cash_b01_b03": b("cash_and_equivalents")-b("cash_ending"),
  "annual_revenue": sum(V(row,"revenue") for row in (a,h,n,q))-135129055328395,
  "annual_pretax": sum(V(row,"pretax_profit") for row in (a,h,n,q))-14359435183859,
  "annual_net": sum(V(row,"net_profit") for row in (a,h,n,q))-11571631226008,
  "financing_components": 10167798761+1108894654657-1361786169625-5109438694779-b("financing_cash_flow_ytd"),
  "investing_components": -2330869042369+5480-47754759986135+42042139868239-30167798761+16000000000+1339113087354-b("investing_cash_flow_ytd"),
  "operating_components": 15816182705447-4648819133898+139664400700+4450049887145+354254106806-220449662891-2402735413734-16879604762-92892907451-b("operating_cash_flow_ytd"),
}
assert len(checks) == 23 and all(v == 0 for v in checks.values()), checks
assert set(checks) == set(q["source_validation"]["statement_identity_residuals_vnd"])
assert all(int(x) == 0 for x in q["source_validation"]["statement_identity_residuals_vnd"].values())
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure","dividends_paid"):
    assert b(k) == b(k+"_ytd") - V(n,k+"_ytd"), k
assert b("cash_beginning") == V(n,"cash_ending")
assert b("cash_ending") == V(n,"cash_ending") + b("net_cash_change") + b("foreign_exchange_effect")
assert b("cash_beginning_reported_ytd") == V(n,"cash_beginning_reported_ytd")
assert b("capital_expenditure_ytd") == -2330869042369
assert b("dividends_paid_ytd") == -5109438694779
fields = set(q["financial_line_items_extracted_fields"])
assert len(fields) == 52 and fields == set(q["financial_line_items_manually_verified_fields"])
assert fields == set(EXPECTED) | (fields - set(EXPECTED))
print("PASS: GAS consolidated Q4/2025 original images B01/B02/B03; 52 fields, 23 exact VND accounting checks; FY minus verified 9M quarterly cash-flow")
