#!/usr/bin/env python3
"""Exact-VND GEG 9M vs reviewed H1 B03 bridge, independent of Q2 original version.

Do not change GEG Q2 standalone NULL until signed current-period Q1 same-basis
cash is available. The reviewed-basis Q3 result is an audited-source
calculation, not an automatic production migration.
"""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
N=Decimal(1000000)
FIN=ROOT/"data/financials-GEG.json"
H1=ROOT/"reports/source-audits/GEG-2026H1-user-uploaded-reviewed-note37-current-cashflow-version.json"
Q2=ROOT/"reports/source-audits/GEG-2026Q2-note11-pledged-cash-opening-reclassification-vnd.json"
YTD9={"CFO":1156568657472, "CFI":-1374338221742, "CFF":238886926705,
      "net_cash_flow":21117362435, "fx":-2682959,
      "opening_cash":74942444345, "ending_cash":96057123821}
FIELDS={"CFO":"operating_cash_flow","CFI":"investing_cash_flow",
        "CFF":"financing_cash_flow","net_cash_flow":"net_cash_change",
        "fx":"foreign_exchange_effect","opening_cash":"cash_beginning",
        "ending_cash":"cash_ending"}
def check_cash(row):
    assert sum(int(row[k]) for k in ("CFO","CFI","CFF"))==int(row["net_cash_flow"])
    assert int(row["opening_cash"])+int(row["net_cash_flow"])+int(row["fx"])==int(row["ending_cash"])
def source_version(a,b):
    original=b["version_facts"]["q1_signed_original"]["year_open_cash_equivalents_vnd"]
    pre=b["version_facts"]["q2_signed_original"]["year_open_cash_equivalents_vnd"]
    move=11422218903
    assert int(original["cash_only"])==int(pre["cash_only"])==46702358323
    assert int(original["cash_equivalents"])-int(pre["cash_equivalents"])==move
    # EY reviewed H1 PDF B01 p11 classifies the same amount from code111,
    # not from code112 as in the original quarterly Q2 initial filing.
    ey_cash=35280139420
    ey_equiv=39662304925
    assert int(original["cash_only"])-ey_cash==move
    assert int(original["cash_equivalents"])==ey_equiv
    assert ey_cash+ey_equiv==int(pre["cash_total"])==74942444345
    assert a["reviewed_h1_uploaded_source"]["sha256"]=="c5fcba1374cea2e2fc6e82eb66ccd4cf49320bd4a412c4c3f834d60c16ba700e"
    assert a["reviewed_h1_uploaded_source"]["note37_pdf_page"]==73
def main():
    a=json.loads(H1.read_text("utf-8"));b=json.loads(Q2.read_text("utf-8"))
    x=json.loads(FIN.read_text("utf-8"))["items"]
    q2=next(v for v in x if v["period"]=="2026-Q2" and "hợp nhất" in v["report_type"].lower())
    q3=next(v for v in x if v["period"]=="2026-Q3" and "hợp nhất" in v["report_type"].lower())
    h={k:int(a["reviewed_h1_2026_vnd"][k]) for k in FIELDS}
    initial={k:int(a["originally_reported_q2_2026_vnd"][k]) for k in FIELDS}
    check_cash(h);check_cash(initial);check_cash(YTD9);source_version(a,b)
    assert q2["cashflow_period_basis"]=="year_to_date"
    for field in ("operating_cash_flow","investing_cash_flow","financing_cash_flow",
                  "net_cash_change","cash_beginning","capital_expenditure",
                  "foreign_exchange_effect","dividends_paid"):
        assert q2[field] is None,(field,q2[field])
    old={}
    for k,field in FIELDS.items():
        v=q3[field];assert type(v) in (int,float),(field,v)
        old[k]=int(Decimal(str(v))*N)
    check_cash(old)
    for k in ("CFO","CFI","CFF","net_cash_flow","fx"):
        assert YTD9[k]-initial[k]==old[k],("original source Q3",k)
    assert old["opening_cash"]==initial["ending_cash"]
    assert old["ending_cash"]==YTD9["ending_cash"]
    revised={k:YTD9[k]-h[k] for k in ("CFO","CFI","CFF","net_cash_flow","fx")}
    revised["opening_cash"]=h["ending_cash"]
    revised["ending_cash"]=YTD9["ending_cash"]
    check_cash(revised)
    expected={"CFO":448662906453,"CFI":-639871926621,"CFF":186959810890,
              "net_cash_flow":-4249209278,"fx":-15900229,
              "opening_cash":100322233328,"ending_cash":96057123821}
    assert revised==expected
    assert h["ending_cash"]!=initial["ending_cash"]
    assert a["decision"]["standalone_q2_cashflow_still_blocked"] is True
    # Negative guard: an off-by-one change in the signed 9M CFO breaks its statement.
    bad=dict(YTD9);bad["CFO"]+=1
    try:check_cash(bad)
    except AssertionError:pass
    else:raise AssertionError("tampered signed 9M CFO passed")
    print("PASS GEG Q3 2026: original Q2 and EY-reviewed H1 two versions,"
          " 9M signed source, exact VND reconciliations, code111 vs code112 reclassification,"
          " 2 cash bridges and negative test. Q2 standalone remains NULL.")
    print("REVIEWED H1 Q3 CFO CFI CFF NET FX",*(str(revised[k]) for k in ("CFO","CFI","CFF","net_cash_flow","fx")))
if __name__=="__main__":main()
