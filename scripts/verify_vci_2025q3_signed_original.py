#!/usr/bin/env python3
"""VCI 2025Q3 issuer signed B01/B02/B03 source and reviewed H1 quarterly bridge.

Exact VND checks only. Broker client custody cash excluded from issuer cash.
No new consolidated legal-entity statement is invented when no subsidiaries.
"""
from decimal import Decimal
from pathlib import Path
import copy
import json

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "reports/source-audits/VCI-2025Q3-issuer-signed-9M-minus-H1-vnd.json"
H1 = ROOT / "reports/source-audits/VCI-2025Q2-signed-original-reviewed-H1-exact-VND.json"
FIN = ROOT / "data/financials-VCI.json"
MILLION = Decimal("1000000")
CASH = ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")
def read(path): return json.loads(path.read_text(encoding="utf-8"))
def intval(row,k):
    assert type(row.get(k)) in (float,int),(k,row.get(k))
    result=Decimal(str(row[k]))*MILLION
    assert result==result.to_integral_value(),(k,result)
    return int(result)
def verify_source(ledger,h1):
    assert ledger["ticker"]=="VCI" and ledger["period"]=="2025-Q3"
    assert ledger["source_pdf_sha256"]=="8a2cb804555583a1b7a9a4ae235fe220f2e050a38f1e10117172dec52a69ef68"
    assert ledger["source_pdf_pages"]==48 and ledger["source_pdf_bytes"]==15472278
    assert ledger["source_workflow_run"]==44922406049
    assert ledger["source_artifact_id"]==14713704732
    assert ledger["no_subsidiaries_signed_note"] is True
    assert ledger["client_custody_is_not_company_cash"] is True
    assert ledger["pdf_url"].startswith("https://www.vietcap.com.vn/api/cms-api/uploads/froala/files/20251015")
    fields=ledger["exact_vnd_fields"]
    assert len(fields)==66
    val=lambda k:int(fields[k])
    h=h1["exact_vnd_fields"]
    prior=lambda k:int(h[k])
    identities={
       "assets":val("current_assets")+val("non_current_assets")-val("total_assets"),
       "balance":val("total_assets")-val("total_liabilities")-val("equity"),
       "liabilities":val("current_liabilities")+val("long_term_liabilities")-val("total_liabilities"),
       "current_assets":val("financial_assets_current")+val("other_current_assets")-val("current_assets"),
       "cash_split":val("cash_only")+val("cash_equivalents_only")-val("cash_and_equivalents"),
       "fixed_assets":val("securities_fixed_tangible")+val("securities_fixed_intangible")-val("fixed_assets"),
       "operating_revenue_sum":sum(val(k) for k in
          ("securities_fvtpl_gain","securities_htm_interest_income","securities_loan_interest_income",
           "securities_afs_interest_income","securities_brokerage_revenue","securities_depository_revenue",
           "securities_financial_advice_revenue","securities_consulting_revenue","securities_other_revenue"))-val("revenue"),
       "quarter_operating":val("revenue")-val("securities_operating_expense")+val("financial_income")-
           val("financial_expense")-val("admin_expense")-val("operating_profit"),
       "quarter_tax":val("income_tax_current")+val("income_tax_deferred")-val("income_tax"),
       "quarter_profit":val("pretax_profit")-val("income_tax")-val("net_profit"),
       "ytd_operating":val("revenue_ytd")-val("securities_operating_expense_ytd")+
           val("financial_income_ytd")-val("financial_expense_ytd")-val("admin_expense_ytd")-val("operating_profit_ytd"),
       "ytd_pretax":val("operating_profit_ytd")+val("other_profit_ytd")-val("pretax_profit_ytd"),
       "ytd_profit":val("pretax_profit_ytd")-val("income_tax_ytd")-val("net_profit_ytd"),
       "ytd_minus_h1_revenue":val("revenue_ytd")-prior("revenue_ytd")-val("revenue"),
       "ytd_minus_h1_pretax":val("pretax_profit_ytd")-prior("pretax_profit_ytd")-val("pretax_profit"),
       "ytd_minus_h1_profit":val("net_profit_ytd")-prior("net_profit_ytd")-val("net_profit"),
       "ytd_cash_sections":val("operating_cash_flow_ytd")+val("investing_cash_flow_ytd")+
           val("financing_cash_flow_ytd")-val("net_cash_change_ytd"),
       "ytd_cash_bridge":val("cash_beginning_reported_ytd")+val("net_cash_change_ytd")-val("cash_ending_ytd"),
       "ytd_B01_B03_cash":val("cash_and_equivalents")-val("cash_ending_ytd"),
       "YTD_CFI":val("capital_expenditure_ytd")+231190000-val("investing_cash_flow_ytd"),
       "YTD_CFF":54006240000+25281926000000-21988564000000+val("dividends_paid_ytd")-val("financing_cash_flow_ytd")
    }
    quarterly={k:val(k+"_ytd")-prior(k+"_ytd") for k in CASH}
    quarterly["cash_beginning"]=prior("cash_ending_ytd")
    quarterly["cash_ending"]=val("cash_ending_ytd")
    identities["quarter_cash_sections"]=quarterly["operating_cash_flow"]+quarterly["investing_cash_flow"]+quarterly["financing_cash_flow"]-quarterly["net_cash_change"]
    identities["quarter_cash_bridge"]=quarterly["cash_beginning"]+quarterly["net_cash_change"]-quarterly["cash_ending"]
    assert len(identities)==23, len(identities)
    assert all(v==0 for v in identities.values()),identities
    assert {k:int(v) for k,v in ledger["q3_standalone_cashflow_vnd"].items()}==quarterly
    assert set(identities)==set(ledger["checked_exact_vnd"])
    assert all(int(ledger["checked_exact_vnd"][k])==0 for k in identities)
    return quarterly

def verify(ledger,h1,data):
    qtr=verify_source(ledger,h1)
    assert data["symbol"]=="VCI" and len(data["items"])==7
    row=next(x for x in data["items"] if x["period"]=="2025-Q3")
    assert "không có công ty con" in row["report_type"].lower()
    assert row["verification_status"]=="issuer_signed_Q3_2025_B01_B02_9M_B03_original_verified_no_subs"
    assert row["unit"]=="triệu VND" and row["cashflow_period_basis"]=="year_to_date"
    assert row["q3_standalone_cashflow_status"]=="signed_original_9M_minus_reviewed_H1_exact_vnd_verified"
    assert row["source_url"]==ledger["pdf_url"]
    v=row["source_validation"]
    assert v["issuer_original_pdf_sha256"]==ledger["source_pdf_sha256"]
    assert v["source_audit_ledger"]==str(S.relative_to(ROOT))
    assert v["manual_review_blocking_automatic_extraction"] is False
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["reporter_has_no_subsidiaries_signed_source"] is True
    assert v["client_cash_outside_company_B01_verified"] is True
    assert v["quarter_cash_bridge_residual_vnd"]=="0"
    assert set(row["cashflow_quarter_manually_verified_fields"])==set(qtr)
    approved=set(row["financial_line_items_manually_verified_fields"])
    for k,amount in ledger["exact_vnd_fields"].items():
        assert k in approved and intval(row,k)==int(amount),(k,row.get(k),amount)
    for k,amount in qtr.items():
        assert k in approved and intval(row,k)==amount,(k,row.get(k),amount)
    assert intval(row,"broker_afs_assets")==intval(row,"securities_afs_assets")
    assert intval(row,"broker_fvtpl_assets")==intval(row,"securities_fvtpl_assets")
    assert intval(row,"cash_ending")==intval(row,"cash_ending_ytd")
    assert intval(row,"net_profit_attributable")==intval(row,"net_profit")
    return qtr

def main():
    src,prior,rows=read(S),read(H1),read(FIN)
    qtr=verify(src,prior,rows)
    for failure in ("bad_cfo_1vnd","bad_assets_1vnd","wrong_website_q3_cash","false_positive_cff"):
        a,b,c=copy.deepcopy(src),copy.deepcopy(prior),copy.deepcopy(rows)
        r=next(x for x in c["items"] if x["period"]=="2025-Q3")
        if failure=="bad_cfo_1vnd":
            a["exact_vnd_fields"]["operating_cash_flow_ytd"]=str(int(a["exact_vnd_fields"]["operating_cash_flow_ytd"])+1)
        elif failure=="bad_assets_1vnd":
            a["exact_vnd_fields"]["total_assets"]=str(int(a["exact_vnd_fields"]["total_assets"])+1)
        elif failure=="wrong_website_q3_cash":
            r["cash_ending"]+=0.000001
        else: r["financing_cash_flow"]=-abs(r["financing_cash_flow"])
        try: verify(a,b,c)
        except (AssertionError,ValueError,TypeError): pass
        else: raise AssertionError("Corruption not detected: "+failure)
    print(f"PASS VCI Q3 2025: {len(src['exact_vnd_fields'])} exact VND issuer source fields, 23 equations,")
    print("4 deliberate corruption controls, no subsidiaries, independent customer custody excluded.")
    print("Q3 company cashflow CFO CFI CFF net:",*(str(qtr[k]) for k in CASH))
    print("NOT COMPLETED: VCI Q4/2025, Q1/2026 and Q2/2026 still require signed-source checks.")
if __name__=="__main__": main()
