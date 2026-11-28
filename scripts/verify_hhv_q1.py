from decimal import Decimal
from pathlib import Path
import json
rows=json.loads(Path("data/financials-HHV.json").read_text(),parse_float=Decimal)["items"]
q=next(x for x in rows if x["period"]=="2025-Q1")
def v(k):
    return int(Decimal(q[k])*1000000)
expected={"total_assets":39260780257975,"current_assets":1319202977153,"short_term_receivables":975265129193,"total_liabilities":27989634411692,"equity":11271145846283,"revenue":735015629632,"cost_of_goods_sold":-348848244749,"gross_profit":386167384883,"pretax_profit":194446822732,"net_profit":172967606188,"net_profit_attributable":146236819496,"operating_cash_flow":229299895953,"investing_cash_flow":-123479013757,"financing_cash_flow":-215050026919,"capital_expenditure":-56814127533,"dividends_paid":0,"foreign_exchange_effect":0,"net_cash_change":-109229144723,"cash_beginning":308933876437,"cash_ending":199704731714,"cash_and_equivalents":199704731714}
for k,x in expected.items():
    assert v(k)==x,(k,v(k),x)
assert v("total_assets")==v("total_liabilities")+v("equity")
assert v("gross_profit")==v("revenue")+v("cost_of_goods_sold")
assert v("net_cash_change")==sum(v(k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
assert v("cash_ending")==v("cash_beginning")+v("net_cash_change")+v("foreign_exchange_effect")
assert v("cash_ending")==v("cash_and_equivalents")
assert v("net_profit")==v("net_profit_attributable")+v("net_profit_non_controlling_interests")
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","capital_expenditure","dividends_paid","foreign_exchange_effect","net_cash_change"):
    assert v(k)==v(k+"_ytd"),k
assert abs(q["roa"]-q["net_profit"]*400/q["average_total_assets"])<Decimal("0.000000001")
assert abs(q["roe"]-q["net_profit"]*400/q["average_equity"])<Decimal("0.000000001")
print("HHV Q1: 36 exact source, accounting, YTD and ratio assertions passed")
