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

q3=q
q=next(x for x in rows if x["period"]=="2025-Q4")
expected_q4={"total_assets":40753441078781,"current_assets":1864835151184,"total_liabilities":28575631091903,"current_liabilities":3558781882006,"long_term_liabilities":25016849209897,"equity":12177809986878,"revenue":1205947447629,"cost_of_goods_sold":-751837439137,"gross_profit":454110008492,"pretax_profit":234827580086,"net_profit":201707917468,"net_profit_attributable":181787828018,"net_profit_non_controlling_interests":19920089450,"operating_cash_flow":1493675116612,"investing_cash_flow":-1198627802985,"financing_cash_flow":-182906719266,"capital_expenditure":-3574203964,"dividends_paid":0,"foreign_exchange_effect":0,"net_cash_change":112140594361,"cash_beginning":474622867199,"cash_ending":586763461560}
for k,x in expected_q4.items():
    assert v(k)==x,(k,v(k),x)
assert v("equity")==8004717114333+4173092872545
assert v("total_assets")==v("total_liabilities")+v("equity")
assert v("total_liabilities")==v("current_liabilities")+v("long_term_liabilities")
assert v("gross_profit")==v("revenue")+v("cost_of_goods_sold")
assert v("net_cash_change")==sum(v(k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
assert v("cash_ending")==v("cash_beginning")+v("net_cash_change")+v("foreign_exchange_effect")
assert v("cash_ending")==v("cash_and_equivalents")
assert v("net_profit")==v("net_profit_attributable")+v("net_profit_non_controlling_interests")
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","capital_expenditure","dividends_paid","foreign_exchange_effect","net_cash_change"):
    assert v(k+"_ytd")==v(k)+int(Decimal(q3[k+"_ytd"])*1000000),k
assert abs(q["roa"]-q["net_profit"]*400/q["average_total_assets"])<Decimal("0.000000001")
assert abs(q["roe"]-q["net_profit"]*400/q["average_equity"])<Decimal("0.000000001")
print("HHV Q4: original source, equity code 400, YTD and ratio regression passed")

# FY audited values remain distinct from original quarter and original YTD.
a=q["source_validation"]["audited_fy"]["values_vnd_except_eps"]
assert a["total_assets"]==40752075682457
assert a["total_liabilities"]==28579498126112
assert a["equity"]==12172577556345
assert a["revenue_ytd"]==3801371595413
assert a["pretax_profit_ytd"]==773401844361
assert a["net_profit_ytd"]==671183550117
assert a["operating_cash_flow_ytd"]==1828883045291
assert a["investing_cash_flow_ytd"]==-1395614000968
assert a["cash_and_equivalents"]==586763423469
assert a["total_assets"]==a["total_liabilities"]+a["equity"]
assert a["net_profit_ytd"]==a["net_profit_attributable_ytd"]+a["net_profit_non_controlling_interests_ytd"]
assert a["net_profit_ytd"]==a["pretax_profit_ytd"]-a["income_tax_current_ytd"]-a["income_tax_deferred_ytd"]
assert a["gross_profit_ytd"]==a["revenue_ytd"]+a["cost_of_goods_sold_ytd"]
assert a["net_profit_ytd"]-v("net_profit_ytd")==-7251236985
assert a["operating_cash_flow_ytd"]-v("operating_cash_flow_ytd")==8299961909
assert a["investing_cash_flow_ytd"]-v("investing_cash_flow_ytd")==-8300000000
print("HHV FY audit: 16 source and distinct-vintage assertions passed")

assert a["financing_cash_flow_ytd"]==-155439497291
assert a["net_cash_change_ytd"]==277829547032
assert a["cash_ending"]==586763423469
assert a["cash_ending"]==a["cash_beginning"]+a["net_cash_change_ytd"]+a["foreign_exchange_effect_ytd"]
assert a["net_cash_change_ytd"]==sum(a[k+"_ytd"] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
assert a["cash_ending"]==a["cash_and_equivalents"]
q=next(x for x in rows if x["period"]=="2026-Q1")
expected_2026q1={"total_assets":41313115720358,"current_assets":2346786197707,"total_liabilities":28426042532398,"equity":12887073187960,"revenue":906967141844,"cost_of_goods_sold":-393494269425,"gross_profit":513472872419,"pretax_profit":244991886750,"net_profit":217338601615,"net_profit_attributable":179908433767,"net_profit_non_controlling_interests":37430167848,"operating_cash_flow":415266432734,"investing_cash_flow":-17037407288,"financing_cash_flow":217218045306,"capital_expenditure":-4365315818,"dividends_paid":0,"foreign_exchange_effect":0,"net_cash_change":615447070752,"cash_beginning":586763423469,"cash_ending":1202210494221}
for k,x in expected_2026q1.items():
    assert v(k)==x,(k,v(k),x)
assert v("total_assets")==v("total_liabilities")+v("equity")
assert v("gross_profit")==v("revenue")+v("cost_of_goods_sold")
assert v("net_cash_change")==sum(v(k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
assert v("cash_ending")==v("cash_beginning")+v("net_cash_change")+v("foreign_exchange_effect")
assert v("cash_ending")==v("cash_and_equivalents")
assert v("net_profit")==v("net_profit_attributable")+v("net_profit_non_controlling_interests")
assert v("cash_beginning")==a["cash_ending"]
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","capital_expenditure","dividends_paid","foreign_exchange_effect","net_cash_change"):
    assert v(k+"_ytd")==v(k)
assert abs(q["roa"]-q["net_profit"]*400/q["average_total_assets"])<Decimal("0.000000001")
assert abs(q["roe"]-q["net_profit"]*400/q["average_equity"])<Decimal("0.000000001")
print("HHV audited B03 and Q1 2026 source and audited opening regression passed")

q1_26=q
q=next(x for x in rows if x["period"]=="2026-Q2")
expected_q2_26={"total_assets":41115938489527,"current_assets":1895697429775,"total_liabilities":28077882861130,"equity":13038055628397,"revenue":970266571976,"gross_profit":440928400793,"pretax_profit":198211967721,"net_profit":171818961733,"net_profit_attributable":144924339711,"operating_cash_flow_ytd":620555019493,"investing_cash_flow_ytd":-611545304688,"financing_cash_flow_ytd":-86937043272,"net_cash_change_ytd":-77927328467,"capital_expenditure_ytd":-16892398367,"cash_beginning_reported_ytd":571723614675,"cash_ending":493796286208}
for k,x in expected_q2_26.items():
    assert v(k)==x,(k,v(k),x)
assert v("total_assets")==v("total_liabilities")+v("equity")
assert v("gross_profit")==v("revenue")+v("cost_of_goods_sold")
assert v("net_profit")==v("net_profit_attributable")+v("net_profit_non_controlling_interests")
assert v("net_cash_change_ytd")==sum(v(k+"_ytd") for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
assert v("cash_ending")==v("cash_beginning_reported_ytd")+v("net_cash_change_ytd")+v("foreign_exchange_effect_ytd")
assert v("cash_ending")==v("cash_and_equivalents")
candidate=q["source_validation"]["candidate_mixed_opening_bridge_vnd"]
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change"):
    assert q[k] is None,k
    assert candidate[k]==v(k+"_ytd")-int(Decimal(q1_26[k+"_ytd"])*1000000),k
assert candidate["opening_basis_adjustment"]==-15039808794
assert candidate["opening_basis_adjustment"]==v("cash_beginning_reported_ytd")-int(Decimal(q1_26["cash_beginning_reported_ytd"])*1000000)
assert candidate["closing_cash"]==candidate["opening_cash_q1"]+candidate["net_cash_change"]+candidate["opening_basis_adjustment"]
print("HHV Q2 2026 source YTD and quarantined quarterly basis regression passed")

h=q["source_validation"]["reviewed_h1"]["values_vnd_except_eps"]
assert h["cash_beginning"]==571735568582
assert h["cash_ending"]==493807311370
assert h["operating_cash_flow_ytd"]==621021245868
assert h["investing_cash_flow_ytd"]==-612012459808
assert h["financing_cash_flow_ytd"]==-86937043272
assert h["cash_ending"]==h["cash_beginning"]+h["net_cash_change_ytd"]
assert h["net_cash_change_ytd"]==sum(h[k+"_ytd"] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))
q=next(x for x in rows if x["period"]=="2026-Q3")
expected_q3_26={"total_assets":41348384624303,"total_liabilities":28097499648185,"equity":13250884976118,"revenue":1114372954058,"cost_of_goods_sold":-642990794046,"gross_profit":471382160012,"pretax_profit":243820059416,"net_profit":212829093874,"net_profit_attributable":186326960359,"operating_cash_flow":186951668944,"investing_cash_flow":-30556832800,"financing_cash_flow":-180104479139,"capital_expenditure":-9834191901,"net_cash_change":-23709642995,"cash_beginning":493807311370,"cash_ending":470097668375}
for k,x in expected_q3_26.items():
    assert v(k)==x,(k,v(k),x)
assert v("total_assets")==v("total_liabilities")+v("equity")
assert v("gross_profit")==v("revenue")+v("cost_of_goods_sold")
assert v("net_profit")==v("net_profit_attributable")+v("net_profit_non_controlling_interests")
assert v("cash_beginning_reported_ytd")==h["cash_beginning"]
assert v("cash_beginning")==h["cash_ending"]
assert v("cash_ending")==v("cash_beginning")+v("net_cash_change")+v("foreign_exchange_effect")
assert v("cash_ending")==v("cash_and_equivalents")
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","capital_expenditure","foreign_exchange_effect","dividends_paid"):
    assert v(k+"_ytd")==v(k)+h[k+"_ytd"]
assert len(rows)==7 and len({x["period"] for x in rows})==7
print("HHV reviewed H1 and Q3 same-basis source regression passed")
