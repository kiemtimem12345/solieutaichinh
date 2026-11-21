#!/usr/bin/env python3
"""Exact-VND VIX 2025Q1/Q2 separate signed B03 source regression.

Guard against previous scraper mapping PRETAX PROFIT as CFO, wrong CFI signs,
and treating 2025-H1 year-to-date cashflow as standalone Q2.
NO 0.1%-tolerance applies to wrong category/scope/sign/year-to-date basis.
"""
from decimal import Decimal
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"reports/source-audits/VIX-2025Q1Q2-original-cash-vnd.json"
DATA=ROOT/"data/financials-VIX.json"
FIELDS=("operating_cash_flow","investing_cash_flow","financing_cash_flow",
        "net_cash_change","cash_beginning","cash_ending","capital_expenditure")
FLOW=("operating_cash_flow","investing_cash_flow","financing_cash_flow",
      "net_cash_change","capital_expenditure")
VND=Decimal("1000000")

def v(row,key):
    value=row.get(key)
    assert type(value) in (int,float),(key,value)
    exact=Decimal(str(value))*VND
    assert exact == exact.to_integral_value(),(key,exact)
    return int(exact)

def check_source(data):
    q1=data["signed_q1_vnd"]
    h1=data["signed_h1_vnd"]
    assert set(q1)==set(FIELDS) and set(h1)==set(FIELDS)
    assert q1["operating_cash_flow"] == -1331196257095
    assert h1["operating_cash_flow"] == -3002293892438
    assert q1["cash_beginning"]==h1["cash_beginning"]==693527828012
    assert q1["cash_ending"]==487051070917
    assert h1["cash_ending"]==1053870185574
    for record in (q1,h1):
        assert sum(record[k] for k in FLOW[:3]) == record["net_cash_change"]
        assert record["cash_beginning"]+record["net_cash_change"]==record["cash_ending"]
    q2={k:h1[k]-q1[k] for k in FLOW}
    q2["cash_beginning"]=q1["cash_ending"]
    q2["cash_ending"]=h1["cash_ending"]
    assert q2["operating_cash_flow"]==-1671097635343
    assert q2["investing_cash_flow"]==1416750000
    assert q2["financing_cash_flow"]==2236500000000
    assert q2["net_cash_change"]==566819114657
    assert q2["cash_beginning"]+q2["net_cash_change"]==q2["cash_ending"]
    assert sum(q2[k] for k in FLOW[:3])==q2["net_cash_change"]
    return q1,h1,q2

def main():
    audit=json.loads(AUDIT.read_text(encoding="utf-8"))
    assert (audit["ticker"],audit["report_scope"],audit["currency"])==("VIX","separate","VND")
    src=audit["sources"]
    assert src["2025-Q1"]["issuer_sha256"]==src["2025-Q1"]["mirror_sha256"]
    assert src["2025-Q2"]["issuer_sha256"]!=src["2025-Q2"]["mirror_sha256"]
    assert src["2025-Q2"]["pixel_different_pages"]==[2]
    assert set(src["2025-Q2"]["pixel_same_pages"])==set(range(1,44))-{2}
    assert src["2025-Q2"]["financial_report_page_render_match"]
    q1,h1,q2=check_source(audit)
    doc=json.loads(DATA.read_text(encoding="utf-8"))
    rows={x["period"]:x for x in doc["items"]}
    assert set(("2025-Q1","2025-Q2")).issubset(rows)
    for p,amounts,ytd,basis in (("2025-Q1",q1,q1,"three_months"),("2025-Q2",q2,h1,"six_months")):
        row=rows[p]
        assert "riêng" in row["report_type"].lower() and "hợp nhất" not in row["report_type"].lower()
        assert row["unit"]=="triệu VND"
        for key,exact in amounts.items():assert v(row,key)==exact,(p,key)
        assert v(row,"cash_and_equivalents")==amounts["cash_ending"]
        for key in FLOW:assert v(row,key+"_ytd")==ytd[key],(p,key)
        assert v(row,"cash_beginning_reported_ytd")==ytd["cash_beginning"]
        assert v(row,"cash_ending_ytd")==ytd["cash_ending"]
        assert row["cashflow_period_basis"]=="quarter" and row["cashflow_ytd_period_basis"]==basis
        assert row["operating_cash_flow"]!=row["pretax_profit"],"Old erroneous CFO==pretax mapping"
        assert row["verification_status"]==("issuer_original_B01_cash_and_B03_2025_"+
          ("Q1" if p=="2025-Q1" else "H1_Q2_standalone")+"_visual_vnd_PASS_B01B02_remaining_pending")
        s=row["source_validation"]
        assert s["b01_cash_and_B03_original_source_visual_verified"] is True
        assert s["b01_b02_full_visual_reviewed"] is False
        assert s["manually_visual_reviewed"] is False # Partial visual, not whole B01/B02.
        assert s["b03_2025_cashflow_verification_status"].endswith("0_VND_residual")
        assert s["original_issuer_pdf_sha256"]==src[p]["issuer_sha256"]
        assert s["b03_source_ledger_path"]==str(AUDIT.relative_to(ROOT))
        assert s["b03_2025_YTD_original_exact_vnd"]=={k:str(n) for k,n in ytd.items()}
        assert s["b03_2025_quarter_original_or_signed_derived_exact_vnd"]=={k:str(n) for k,n in amounts.items()}
    assert v(rows["2025-Q2"],"cash_beginning")==v(rows["2025-Q1"],"cash_ending")
    assert v(rows["2025-Q2"],"cash_ending")==v(rows["2025-Q2"],"cash_and_equivalents")
    # Negative tests: error must be caught even if a tolerance would be numerically small.
    clone={**audit,"signed_q1_vnd":{**q1,"operating_cash_flow":abs(q1["operating_cash_flow"])}}
    try:check_source(clone)
    except AssertionError:pass
    else:raise AssertionError("Wrong CFO sign was accepted")
    clone={**audit,"signed_h1_vnd":{**h1,"cash_ending":h1["cash_ending"]+1000000}}
    try:check_source(clone)
    except AssertionError:pass
    else:raise AssertionError("Broken cash bridge was accepted")
    print("PASS: VIX issuer signed separate B03 Q1/H1 original vs Q2 derived standalone exact VND; "
          "Q1 CFO -1,331,196,257,095; Q2 CFO -1,671,097,635,343; source 0-VND bridges; "
          "cash matches B01; Q2 financial pages same across issuer/Vietstock (except cover p2); "
          "B01/B02 other fields NOT full PASS.")

if __name__=="__main__":
    main()
