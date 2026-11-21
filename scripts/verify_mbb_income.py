#!/usr/bin/env python3
"""Validate MBB consolidated B03a quarterly P&L against exact accounting identities."""
import json
from pathlib import Path
data = json.loads((Path(__file__).resolve().parents[1] / "data/financials-MBB.json").read_text(encoding="utf-8"))
periods = ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
rows = {x["period"]:x for x in data["items"]}
assert sorted(rows) == periods, "Unexpected MBB periods"
required = ["bank_interest_income","bank_interest_expense","bank_net_interest_income","bank_service_income",
 "bank_service_expense","bank_net_service_income","bank_fx_net_income","bank_trading_securities_net",
 "bank_investment_securities_net","bank_other_operating_net","bank_dividend_and_capital_income",
 "revenue","bank_operating_expenses","bank_pre_provision_operating_profit","bank_provision_expense",
 "pretax_profit","income_tax_current","income_tax_deferred","net_profit",
 "bank_non_controlling_profit","net_profit_attributable"]
components=["bank_net_interest_income","bank_net_service_income","bank_fx_net_income",
"bank_trading_securities_net","bank_investment_securities_net","bank_other_operating_net",
"bank_dividend_and_capital_income"]
checks=0
for period in periods:
 x=rows[period]
 assert x["symbol"]=="MBB" and "hợp nhất" in x["report_type"].lower()
 assert x["unit"]=="triệu VND" and x["bank_income_statement_review"]["source_pdf_page"]==6
 verified=set(x.get("financial_line_items_manually_verified_fields",[]))
 for name in required:
  assert isinstance(x.get(name),(int,float)) and name in verified,(period,name)
 eqs=[
  x["bank_interest_income"]+x["bank_interest_expense"]-x["bank_net_interest_income"],
  x["bank_service_income"]+x["bank_service_expense"]-x["bank_net_service_income"],
  sum(x[k] for k in components)-x["revenue"],
  x["revenue"]+x["bank_operating_expenses"]-x["bank_pre_provision_operating_profit"],
  x["bank_pre_provision_operating_profit"]+x["bank_provision_expense"]-x["pretax_profit"],
  x["income_tax_current"]+x["income_tax_deferred"]+x["income_tax"],
  x["pretax_profit"]-x["income_tax"]-x["net_profit"],
  x["net_profit"]-x["bank_non_controlling_profit"]-x["net_profit_attributable"]
 ]
 assert all(n==0 for n in eqs),(period,eqs)
 assert all(x[k]<0 for k in ("bank_interest_expense","bank_service_expense","bank_operating_expenses","bank_provision_expense","income_tax_current"))
 assert x["source_url"].startswith("https://static2.vietstock.vn/data/HOSE/")
 checks+=len(eqs)
print(f"PASS: 7 MBB consolidated income quarters, signed B03a 8 checks per quarter, {checks}/56 exact accounting identities")
