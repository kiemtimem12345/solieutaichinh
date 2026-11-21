#!/usr/bin/env python3
"""VCI Q2/2025 issuer-signed B01 B02, PwC-reviewed 6M B03 minus signed Q1.

Checks exact VND, Q2 issuer 47p scan hash, independent reviewed H1 negative
cashflow signs, no subsidiaries, no broker client cash conflation.
"""
from pathlib import Path
from decimal import Decimal
import copy, json
ROOT=Path(__file__).resolve().parents[1]
AUD=ROOT/"reports/source-audits/VCI-2025Q2-signed-original-reviewed-H1-exact-VND.json"
Q1=ROOT/"reports/source-audits/VCI-2025Q1-signed-original-visual-vnd.json"
FIN=ROOT/"data/financials-VCI.json"
M=Decimal("1000000")
def read(p): return json.loads(p.read_text(encoding="utf-8"))
def asint(row,key):
    assert type(row.get(key)) in (float,int),(key,row.get(key))
    value=Decimal(str(row[key]))*M
    assert value==value.to_integral_value(),(key,value)
    return int(value)
def assert_source(ledger,q1):
    assert ledger["ticker"]=="VCI" and ledger["period"]=="2025-Q2"
    report=ledger["q2_as_filed"]
    assert report["source_pdf_sha256"]=="70c08fb3733de0e582bd8a35870d2d52253d1972b07ba9675539f22ad8a7e761"
    assert report["pdf_bytes"]==8011665 and report["pdf_pages"]==47
    assert report["source_inspection_workflow_run"]==44921419236
    assert report["preview_artifact_id"]==14714430008
    assert ledger["reviewed_H1"]["issuer_original_url"].startswith("https://www.vietcap.com.vn/")
    assert ledger["reviewed_H1"]["basis"].startswith("same issuer")
    assert ledger["scope"].startswith("securities_company_no_subsidiaries")
    f=ledger["exact_vnd_fields"]
    assert len(f)==57
    s=lambda k:int(f[k])
    q=s
    q1v=lambda k:int(q1["original_vnd_fields"][k])
    checks={
      "B01_current_plus_noncurrent":q("current_assets")+q("non_current_assets")-q("total_assets"),
      "B01_total_liab_plus_equity":q("total_assets")-q("total_liabilities")-q("equity"),
      "B01_current_plus_long_liab":q("current_liabilities")+q("long_term_liabilities")-q("total_liabilities"),
      "B01_current_financial_other":q("financial_assets_current")+q("other_current_assets")-q("current_assets"),
      "B01_fixed_tangible_intangible":q("securities_fixed_tangible")+q("securities_fixed_intangible")-q("fixed_assets"),
      "B02_operating":q("revenue")-q("securities_operating_expense")+q("financial_income")-q("financial_expense")-q("admin_expense")-q("operating_profit"),
      "B02_pretax":q("operating_profit")+q("other_profit")-q("pretax_profit"),
      "B02_tax":q("income_tax_current")+q("income_tax_deferred")-q("income_tax"),
      "B02_profit":q("pretax_profit")-q("income_tax")-q("net_profit"),
      "B02_6M_from_Q1_revenue":q("revenue_ytd")-q1v("revenue")-q("revenue"),
      "B02_6M_from_Q1_pretax":q("pretax_profit_ytd")-q1v("pretax_profit")-q("pretax_profit"),
      "B02_6M_from_Q1_net":q("net_profit_ytd")-q1v("net_profit")-q("net_profit"),
      "B03_6M_sections":q("operating_cash_flow_ytd")+q("investing_cash_flow_ytd")+q("financing_cash_flow_ytd")-q("net_cash_change_ytd"),
      "B03_6M_cash":q("cash_beginning_reported_ytd")+q("net_cash_change_ytd")-q("cash_ending_ytd"),
      "B03_to_B01_cash":q("cash_and_equivalents")-q("cash_ending_ytd"),
      "B03_no_client_cash":int(q("cash_ending_ytd")==q("client_brokerage_cash_ending_ytd"))
    }
    assert len(checks)==16 and all(v==0 for v in checks.values()),checks
    assert all(str(v)=="0" for v in ledger["checks_exact_vnd"].values())
    h=ledger["reviewed_H1"]["source_cashflow_lines"]
    for code,key in (("60","operating_cash_flow_ytd"),("70","investing_cash_flow_ytd"),("80","financing_cash_flow_ytd"),("90","net_cash_change_ytd"),("101","cash_beginning_reported_ytd"),("103","cash_ending_ytd")):
        assert int(h[code])==q(key),(code,key,h[code],q(key))
    assert int(h["80"])<0 and int(h["90"])<0,"As-filed scanned total sign ambiguity must resolve using reviewed signed H1"
    quarter={k:q(k+"_ytd")-q1v(k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
    quarter["cash_beginning"],quarter["cash_ending"]=q1v("cash_ending"),q("cash_ending_ytd")
    assert quarter["operating_cash_flow"]+quarter["investing_cash_flow"]+quarter["financing_cash_flow"]==quarter["net_cash_change"]
    assert quarter["cash_beginning"]+quarter["net_cash_change"]==quarter["cash_ending"]
    assert {k:int(v) for k,v in ledger["q2_standalone_vnd"].items()}==quarter
    return checks,quarter
def verify(ledger,q1,data):
    checks,quarter=assert_source(ledger,q1)
    assert data["symbol"]=="VCI" and len(data["items"])==7
    cur=next(row for row in data["items"] if row["period"]=="2025-Q2")
    prev=next(row for row in data["items"] if row["period"]=="2025-Q1")
    assert cur["unit"]=="triệu VND"
    assert "không có công ty con" in cur["report_type"].lower()
    assert cur["verification_status"]=="issuer_signed_Q2_B01_B02_reviewed_H1_B03_quarter_verified_no_subs"
    assert "issuer_signed_original_2025Q1" in prev["verification_status"]
    assert cur["cashflow_period_basis"]=="year_to_date"
    assert cur["source_url"]==ledger["q2_as_filed"]["source_pdf_url"]
    sv=cur["source_validation"]
    assert sv["issuer_original_pdf_sha256"]==ledger["q2_as_filed"]["source_pdf_sha256"]
    assert sv["source_audit_ledger"]==str(AUD.relative_to(ROOT))
    assert sv["b03_negative_CFF_and_net_confirmed_from_PwC_reviewed_H1"] is True
    assert sv["manual_review_blocking_automatic_extraction"] is False
    assert sv["source_is_not_an_explicit_consolidated_report"] is True
    assert sv["reporter_has_no_subsidiaries_signed_source"] is True
    assert sv["client_cash_outside_company_B01_verified"] is True
    assert set(cur["cashflow_quarter_manually_verified_fields"])==set(quarter)
    approved=set(cur["financial_line_items_manually_verified_fields"])
    for k,v in ledger["exact_vnd_fields"].items():
        assert k in approved and asint(cur,k)==int(v),(k,v,cur.get(k))
    for k,v in quarter.items():
        assert k in approved and asint(cur,k)==int(v),(k,v,cur.get(k))
    assert asint(cur,"foreign_exchange_effect_ytd")==0
    assert asint(cur,"broker_customer_deposits")==int(ledger["exact_vnd_fields"]["client_brokerage_cash_ending_ytd"])
    assert asint(cur,"cash_ending_ytd")==asint(cur,"cash_ending")
    assert asint(cur,"net_profit_attributable")==asint(cur,"net_profit")
    assert asint(cur,"broker_afs_assets")==asint(cur,"securities_afs_assets")
    return checks
def main():
    ledger,q1,data=read(AUD),read(Q1),read(FIN)
    checks=verify(ledger,q1,data)
    for corruption in ("signed_net_1vnd","web_cash_1vnd","wrong_client_deposit","wrong_h1_sign"):
        a,b,c=copy.deepcopy(ledger),copy.deepcopy(q1),copy.deepcopy(data)
        r=next(x for x in c["items"] if x["period"]=="2025-Q2")
        if corruption=="signed_net_1vnd":a["exact_vnd_fields"]["net_cash_change_ytd"]=str(int(a["exact_vnd_fields"]["net_cash_change_ytd"])+1)
        elif corruption=="web_cash_1vnd":r["cash_ending"]+=0.000001
        elif corruption=="wrong_client_deposit":r["broker_customer_deposits"]=r["cash_ending"]
        else:a["reviewed_H1"]["source_cashflow_lines"]["80"]="4135035939750"
        try: verify(a,b,c)
        except (AssertionError,ValueError,TypeError): pass
        else: raise AssertionError("Negative test passed "+corruption)
    print("PASS VCI 2025Q2 scanned signed as-filed and issuer PwC-reviewed 6M,",
          len(ledger["exact_vnd_fields"]),"source VND fields,",len(checks),"exact equations,",
          "4 negative tests; scope and client cash isolated.")
    print("VCI 2025Q3/Q4, 2026Q1/Q2 remain unverified; prior PASS quarters not rerun.")
if __name__=="__main__":main()
