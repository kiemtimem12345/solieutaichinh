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

q1=q
q=next(x for x in rows if x["period"]=="2025-Q2")
expected_q2={"total_assets":39836855495573,"current_assets":1670664264716,"total_liabilities":28011398121569,"equity":11825457374004,"revenue":947061532948,"cost_of_goods_sold":-559905028658,"gross_profit":387156504290,"pretax_profit":174792130420,"net_profit":151354968040,"net_profit_attributable":130646154036,"operating_cash_flow":106923794612,"investing_cash_flow":-56563230826,"financing_cash_flow":320373505231,"capital_expenditure":-1729671252,"dividends_paid":0,"foreign_exchange_effect":0,"net_cash_change":370734069017,"cash_beginning":199704731714,"cash_ending":570438800731}
for k,x in expected_q2.items():
    assert v(k)==x,(k,v(k),x)
assert v("total_assets")==v("total_liabilities")+v("equity")
assert v("gross_profit")==v("revenue")+v("cost_of_goods_sold")
assert v("net_cash_change")==sum(v(k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
assert v("cash_ending")==v("cash_beginning")+v("net_cash_change")+v("foreign_exchange_effect")
assert v("cash_ending")==v("cash_and_equivalents")
assert v("net_profit")==v("net_profit_attributable")+v("net_profit_non_controlling_interests")
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","capital_expenditure","dividends_paid","foreign_exchange_effect","net_cash_change"):
    assert v(k+"_ytd")==v(k)+int(Decimal(q1[k+"_ytd"])*1000000),k
assert abs(q["roa"]-q["net_profit"]*400/q["average_total_assets"])<Decimal("0.000000001")
assert abs(q["roe"]-q["net_profit"]*400/q["average_equity"])<Decimal("0.000000001")
review=q["source_validation"]["reviewed_h1"]["values_vnd_except_eps"]
assert review["operating_cash_flow_ytd"]==329979766592
assert review["investing_cash_flow_ytd"]==-175542244583
assert review["financing_cash_flow_ytd"]==107067358312
assert review["cash_ending"]==570438756758
assert review["cash_ending"]==review["cash_beginning"]+review["net_cash_change_ytd"]
assert review["net_cash_change_ytd"]==sum(review[k+"_ytd"] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
print("HHV Q2: signed original, YTD bridge, ratio and reviewed vintage assertions passed")

q2=q
q=next(x for x in rows if x["period"]=="2025-Q3")
expected_q3={"total_assets":40049891402240,"current_assets":1671374841880,"total_liabilities":28072551732830,"equity":11977339669410,"revenue":913523162056,"cost_of_goods_sold":-523983362860,"gross_profit":389539799196,"pretax_profit":173726941297,"net_profit":152404295407,"net_profit_attributable":128868247423,"net_profit_non_controlling_interests":23536047983,"operating_cash_flow":-9315723795,"investing_cash_flow":-8643953400,"financing_cash_flow":-77856256337,"capital_expenditure":-12606427642,"dividends_paid":0,"foreign_exchange_effect":0,"net_cash_change":-95815933532,"cash_beginning":570438800731,"cash_ending":474622867199}
for k,x in expected_q3.items():
    assert v(k)==x,(k,v(k),x)
assert v("total_assets")==v("total_liabilities")+v("equity")
assert v("gross_profit")==v("revenue")+v("cost_of_goods_sold")
assert v("net_cash_change")==sum(v(k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
assert v("cash_ending")==v("cash_beginning")+v("net_cash_change")+v("foreign_exchange_effect")
assert v("cash_ending")==v("cash_and_equivalents")
# The printed source has two one-VND differences; retain rather than force balance.
assert v("net_profit")-v("net_profit_attributable")-v("net_profit_non_controlling_interests")==1
assert v("net_profit_ytd")-int(Decimal(q2["net_profit_ytd"])*1000000)-v("net_profit")==-1
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","capital_expenditure","dividends_paid","foreign_exchange_effect","net_cash_change"):
    assert v(k+"_ytd")==v(k)+int(Decimal(q2[k+"_ytd"])*1000000),k
assert abs(q["roa"]-q["net_profit"]*400/q["average_total_assets"])<Decimal("0.000000001")
assert abs(q["roe"]-q["net_profit"]*400/q["average_equity"])<Decimal("0.000000001")
print("HHV Q3: source assertions, quarter cash bridge and explicit one-VND printed exceptions passed")
