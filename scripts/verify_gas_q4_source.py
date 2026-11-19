#!/usr/bin/env python3
"""GAS original 2025 Q4 consolidated balance, P&L and cash flow regression.

Quarter 4 B02 is current-quarter column; B03 is full-year YTD, with Q4 cash
flow obtained from original FY less original Q3 9M YTD. Preserve issuer parent
profit 237,144 VND 4Q-vs-FY difference; <= project tolerance, never force 0.
"""
import json
from decimal import Decimal
from pathlib import Path
data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-GAS.json").read_text(encoding="utf-8"))
rows={x["period"]:x for x in data["items"]}
q1,q2,q3,q4=(rows[p] for p in ("2025-Q1","2025-Q2","2025-Q3","2025-Q4"))
v=lambda obj,key:int((Decimal(str(obj[key]))*Decimal(1000000)).to_integral_exact())
src=q4["source_validation"]
assert src["manually_visual_reviewed"] is False and src["visual_review_pending"] is True
assert q4["unit"]=="triệu VND" and q4["eps"]==558
assert q4["cashflow_period_basis"]=="year_to_date"
assert not q4.get("financial_line_items_manually_verified_fields"),"Do not claim visual PDF PASS"
assert len(q4["financial_line_items_extracted_fields"])==51
assert len(src["source_checks_vnd"])==23 and all(z=="0" for z in src["source_checks_vnd"].values())
checks=0
def eq(k,a,b):
 global checks
 assert a==b,(k,a,b,a-b)
 checks+=1
eq("assets",v(q4,"current_assets")+v(q4,"non_current_assets"),v(q4,"total_assets"))
eq("source balances",v(q4,"total_liabilities")+v(q4,"equity"),v(q4,"total_assets"))
eq("liability components",v(q4,"current_liabilities")+v(q4,"long_term_liabilities"),v(q4,"total_liabilities"))
eq("current asset subtotal",sum(v(q4,k) for k in ("cash_and_equivalents","short_term_investments","short_term_receivables","inventory"))+889281613049,v(q4,"current_assets"))
eq("gross",v(q4,"revenue")-v(q4,"cost_of_goods_sold"),v(q4,"gross_profit"))
eq("operating",v(q4,"gross_profit")+v(q4,"financial_income")-v(q4,"financial_expense")+v(q4,"share_of_profit_in_associates")-v(q4,"selling_expense")-v(q4,"admin_expense"),v(q4,"operating_profit"))
eq("other",v(q4,"other_income")-v(q4,"other_expense"),v(q4,"other_profit"))
eq("pretax",v(q4,"operating_profit")+v(q4,"other_profit"),v(q4,"pretax_profit"))
eq("income tax",v(q4,"income_tax_current")+v(q4,"income_tax_deferred"),v(q4,"income_tax"))
eq("net",v(q4,"pretax_profit")-v(q4,"income_tax"),v(q4,"net_profit"))
eq("NCI",v(q4,"net_profit_attributable")+v(q4,"non_controlling_interest_profit"),v(q4,"net_profit"))
for field,expected in (("revenue",135129055328395),("pretax_profit",14359435183859),("net_profit",11571631226008)):
 eq("FY sum of four quarters "+field,sum(v(z,field) for z in (q1,q2,q3,q4)),expected)
eq("FY cashflow",v(q4,"operating_cash_flow_ytd")+v(q4,"investing_cash_flow_ytd")+v(q4,"financing_cash_flow_ytd"),v(q4,"net_cash_change_ytd"))
eq("FY cash bridge",v(q4,"cash_beginning_reported_ytd")+v(q4,"net_cash_change_ytd")+v(q4,"foreign_exchange_effect_ytd"),v(q4,"cash_ending"))
eq("FY CFI original components",-2330869042369+5480-47754759986135+42042139868239-30167798761+16000000000+1339113087354,v(q4,"investing_cash_flow_ytd"))
eq("FY CFF original components",10167798761+1108894654657-1361786169625-5109438694779,v(q4,"financing_cash_flow_ytd"))
eq("Q4 cashflows",v(q4,"operating_cash_flow")+v(q4,"investing_cash_flow")+v(q4,"financing_cash_flow"),v(q4,"net_cash_change"))
eq("Q4 bridge",v(q4,"cash_beginning")+v(q4,"net_cash_change")+v(q4,"foreign_exchange_effect"),v(q4,"cash_ending"))
for field in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure","dividends_paid"):
 eq("Q4 = FY less nine months "+field,v(q4,field+"_ytd")-v(q3,field+"_ytd"),v(q4,field))
eq("Q4 begins from Q3 closing cash",v(q3,"cash_ending"),v(q4,"cash_beginning"))
eq("FY dividends",v(q4,"dividends_paid_ytd"),-5109438694779)
eq("cash at 31/12",v(q4,"cash_ending"),6876468282085)
delta=sum(v(z,"net_profit_attributable") for z in (q1,q2,q3,q4))-11414339911686
assert delta==237144 and src["parent_shareholder_profit_quarters_minus_fy_vnd"]=="237144"
assert Decimal(delta)/Decimal(11414339911686)*100 < Decimal("0.01")
assert q4["source_validation"]["fy_opening_cash_matches_9m_source"] is True
print(f"PASS: GAS Q4 consolidated 51 numeric fields; 23 exact reported identities plus {checks} regression checks; 237,144 VND parent profit exception <0.01%")
