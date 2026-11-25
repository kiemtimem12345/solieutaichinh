#!/usr/bin/env python3
"""VCK 2025Q2: signed-source exact VND, EY H1 vintage difference, resolved comparative.

Preserve the historical variance and independently verify the now-resolved row.
"""
from pathlib import Path
import json,copy
from decimal import Decimal

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCK-2025Q2-VPSS-original-and-EY-H1-vintage-vnd.json"
QUEUE=ROOT/"reports/financial-exception-queue.json"
DATA=ROOT/"data/financials-VCK.json"
Q1=ROOT/"reports/source-audits/VCK-2025Q1-VPSS-issuer-signed-standalone-vnd.json"
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def verify(s,queue,data,q1):
    assert s["ticker"]=="VCK" and s["original_filing_symbol"]=="VPSS" and s["period"]=="2025-Q2"
    assert s["as_filed"]["page_count"]==39 and not s["as_filed"]["sha256_verified"]
    assert s["as_filed"]["url"].endswith("VPSS_Baocaotaichinh_Q2_2025.pdf")
    assert "no mandatory consolidated" in s["scope"]
    assert s["h1_audited"]["signed_by"]=="Ernst & Young Vietnam Limited"
    assert s["h1_audited"]["signed_date"]=="2025-09-19"
    assert len(s["original_vnd_fields"])==45 and len(s["checks_exact_vnd"])==20
    N=lambda k:int(s["original_vnd_fields"][k])
    S=lambda k:int(q1["exact_vnd_fields"][k])
    identities={
      "assets":N("current_assets")+N("non_current_assets")-N("total_assets"),
      "balance":N("total_assets")-N("total_liabilities")-N("equity"),
      "liabs":N("current_liabilities")+N("long_term_liabilities")-N("total_liabilities"),
      "current":N("financial_assets_current")+N("other_current_assets")-N("current_assets"),
      "noncurrent":sum(N(k) for k in ("financial_assets_noncurrent","fixed_assets","long_term_construction_in_progress","other_non_current_assets"))-N("non_current_assets"),
      "fixed":N("securities_fixed_tangible")+N("securities_fixed_intangible")-N("fixed_assets"),
      "earnings":N("pretax_profit")-N("income_tax")-N("net_profit"),
      "six_month_earnings":N("pretax_profit_ytd")-N("income_tax_ytd")-N("net_profit_ytd"),
      "operating_profit":N("operating_profit")+N("other_profit")-N("pretax_profit"),
      "h1_operating":N("operating_profit_ytd")+N("other_profit_ytd")-N("pretax_profit_ytd"),
      "revenue_bridge":N("revenue_ytd")-S("revenue")-N("revenue"),
      "tax_bridge":N("income_tax_ytd")-S("income_tax")-N("income_tax"),
      "CFF_sections":N("operating_cash_flow_ytd")+N("investing_cash_flow_ytd")+N("financing_cash_flow_ytd")-N("net_cash_change_ytd"),
      "cash_end":N("cash_beginning_reported_ytd")+N("net_cash_change_ytd")-N("cash_ending_ytd"),
      "q2_cash_sections":0,
      "q2_cash_end":0,
      "reviewed_q2_cash_sections":0,
      "reviewed_q2_cash_end":0,
      "income_Q2_vintage_difference":N("net_profit_ytd")-S("net_profit")-N("net_profit"),
      "pretax_Q2_vintage_difference":N("pretax_profit_ytd")-S("pretax_profit")-N("pretax_profit"),
    }
    for name in list(identities)[14:18]:
        rows=s["q2_standalone_cash_reviewed_h1_vnd"] if name.startswith("reviewed") else s["q2_standalone_cash_original_asfiled_vnd"]
        if name.endswith("_sections"):
            identities[name]=sum(int(rows[k]) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))-int(rows["net_cash_change"])
        else:identities[name]=int(rows["cash_beginning"])+int(rows["net_cash_change"])-int(rows["cash_ending"])
    assert identities["income_Q2_vintage_difference"]==913532383
    assert identities["pretax_Q2_vintage_difference"]==913532383
    for k,val in identities.items():
        assert int(s["checks_exact_vnd"][k])==val,(k,val,s["checks_exact_vnd"][k])
        if "vintage_difference" not in k:assert val==0,(k,val)
    rev=s["h1_audited"]["cashflow_6m"]
    original=s["q2_standalone_cash_original_asfiled_vnd"]
    reviewed=s["q2_standalone_cash_reviewed_h1_vnd"]
    assert int(original["operating_cash_flow"])-int(reviewed["operating_cash_flow"])==605000000
    assert int(original["investing_cash_flow"])-int(reviewed["investing_cash_flow"])==-605000000
    assert int(original["net_cash_change"])==int(reviewed["net_cash_change"])
    assert int(original["cash_ending"])==int(reviewed["cash_ending"])==N("cash_and_equivalents")
    assert int(rev["ending"])==N("cash_ending_ytd")
    assert data["symbol"]=="VCK" and len(data["items"])==7
    row=next(x for x in data["items"] if x["period"]=="2025-Q2")
    assert row["verification_status"]=="issuer_signed_Q2_and_EY_H1_vintage_reconciled"
    assert row["source_validation"]["do_not_publish_unreconciled_quarter"] is False
    assert row["source_validation"]["unreconciled_vintage_queued"] is False
    assert not row.get("scope_review_hold")
    resolution=s["resolution_20261125"]
    assert resolution["status"]=="reconciled_exact_vnd"
    assert s["status"]=="resolved_issuer_signed_Q2_and_EY_H1_vintage_reconciled"
    rr=resolution["source_review"]
    revised=rr["revised_q1_comparative_vnd"]
    assert revised["pretax_profit"]==919386668744 and revised["net_profit"]==735687757488
    assert revised["securities_operating_expense"]==536435699262 and revised["admin_expense"]==83906585251
    assert revised["pretax_profit"]-S("pretax_profit")==913532383
    assert revised["net_profit"]-S("net_profit")==913532383
    assert S("securities_operating_expense")-revised["securities_operating_expense"]==54329401
    assert S("admin_expense")-revised["admin_expense"]==859202982
    assert N("pretax_profit_ytd")-revised["pretax_profit"]-N("pretax_profit")==0
    assert N("net_profit_ytd")-revised["net_profit"]-N("net_profit")==0
    def exact(r,k):
        assert type(r.get(k)) in (int,float),(k,r.get(k))
        v=Decimal(str(r[k]))*Decimal(1000000)
        assert v==v.to_integral_value(),(k,v)
        return int(v)
    for k,v in rr["raw_values_vnd"].items():
        assert exact(row,k)==int(v),(k,exact(row,k),v)
    assert len(rr["checks_exact_vnd"])==40 and all(v==0 for v in rr["checks_exact_vnd"].values())
    assert row["source_review"]["revised_q1_comparative_vnd"]==revised
    for k in ("total_assets","total_liabilities","equity","revenue","pretax_profit","net_profit"):
        assert exact(row,k)==N(k)
    for k,v in reviewed.items():
        assert exact(row,k)==int(v)
    for k,short in (("operating_cash_flow","CFO"),("investing_cash_flow","CFI"),("financing_cash_flow","CFF"),("net_cash_change","net")):
        assert exact(row,k+"_ytd")==int(rev[short])
        assert exact(row,k)==int(rev[short])-S(k)
    first=next(x for x in data["items"] if x["period"]=="2025-Q1")
    nextq=next(x for x in data["items"] if x["period"]=="2025-Q3")
    assert exact(first,"net_profit")==S("net_profit")
    assert exact(first,"cash_ending")==exact(row,"cash_beginning")
    assert exact(nextq,"cash_beginning")==exact(row,"cash_ending")
    assert exact(row,"client_brokerage_cash_ending_ytd")!=exact(row,"cash_ending")
    assert row["eps"]==1232 and row["eps_ytd"]==2523
    assert len(queue["items"])>=1
    entry=next(x for x in queue["items"] if x["id"]=="VCK-2025Q2-signed-vintage-bridge")
    assert entry["status"]=="resolved_exact_vnd" and entry["production_eligible"] is True
    assert entry["user_visibility"]=="only_if_user_asks_which_tickers_or_periods_remain"
    assert entry["evidence_ledger"]==str(SRC.relative_to(ROOT))
    assert queue["continue_processing_other_periods"] is True
    assert not data.get("pre_listing_legacy_reports")
    return len(identities)
if __name__=="__main__":
    a,b,c,d=map(read,(SRC,QUEUE,DATA,Q1))
    n=verify(a,b,c,d)
    for scenario in ("bad_balance","profit_vintage_suppressed","wrong_published_profit","wrong_revised_comparator"):
        aa,bb,cc,dd=copy.deepcopy(a),copy.deepcopy(b),copy.deepcopy(c),copy.deepcopy(d)
        if scenario=="bad_balance":
            aa["original_vnd_fields"]["total_assets"]=str(int(aa["original_vnd_fields"]["total_assets"])+1)
        elif scenario=="profit_vintage_suppressed":
            aa["checks_exact_vnd"]["income_Q2_vintage_difference"]="0"
        elif scenario=="wrong_published_profit":next(x for x in cc["items"] if x["period"]=="2025-Q2")["net_profit"]=702214.269107
        else:aa["resolution_20261125"]["source_review"]["revised_q1_comparative_vnd"]["net_profit"]+=1
        try:verify(aa,bb,cc,dd)
        except (AssertionError,TypeError,ValueError):pass
        else:raise AssertionError("Not rejected: "+scenario)
    print(f"PASS VCK Q2 2025 signed 45 source fields, {n} exact-VND checks with explicit historical vintage variance, resolved Q1 comparative, exact published amounts; 4 negative controls.")
    print("VCK Q2/2025 resolved; signed Q1 and later verified quarters preserved.")
