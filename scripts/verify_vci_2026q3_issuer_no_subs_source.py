#!/usr/bin/env python3
"""VCI 2026 Q3 issuer-signed HOSE source, broker-only B01/B02/B03 checks.

Single legal entity, NO SUBSIDIARIES (signed Note1); this is a company
statement, not a separately signed consolidated statement. Accept as
economically equivalent reporting scope only with explicit issuer note.
Cash of brokerage customers is OFF balance sheet and must stay separate.
Source numeric rows manually mapped from issuer PDF text and sampled images;
full page-image inspection/hash is NOT claimed.
"""
from decimal import Decimal
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"reports/source-audits/VCI-2026Q3-issuer-HOSE-original-special-broker-no-subs-vnd.json"
FIN=ROOT/"data/financials-VCI.json"
M=Decimal("1000000")
def read(p): return json.loads(p.read_text("utf-8"))
def src_int(source,key): return int(source[key])
def val(row,key):
    v=row.get(key)
    assert type(v) in (int,float),(key,v)
    result=Decimal(str(v))*M
    assert result==result.to_integral_value(),(key,v,result)
    return int(result)
def verify_source(z):
    f=z["original_vnd_fields"]
    S=lambda k:src_int(f,k)
    checks={
       "assets_components":S("current_assets")+S("non_current_assets")-S("total_assets"),
       "balance":S("total_assets")-S("total_liabilities")-S("equity"),
       "current_assets":39559534902004+S("other_current_assets")-S("current_assets"),
       "q3_operating_profit":S("revenue")-S("securities_operating_expense")+S("financial_income")-S("financial_expense")-S("admin_expense")-S("operating_profit"),
       "q3_pretax":S("operating_profit")+S("other_profit")-S("pretax_profit"),
       "q3_netprofit":S("pretax_profit")-S("income_tax")-S("net_profit"),
       "9m_operating_profit":S("revenue_ytd")-S("securities_operating_expense_ytd")+S("financial_income_ytd")-S("financial_expense_ytd")-S("admin_expense_ytd")-S("operating_profit_ytd"),
       "9m_pretax":S("operating_profit_ytd")+4383349561-S("pretax_profit_ytd"),
       "9m_netprofit":S("pretax_profit_ytd")-S("income_tax_ytd")-S("net_profit_ytd"),
       "cash_sections":S("operating_cash_flow_ytd")+S("investing_cash_flow_ytd")+S("financing_cash_flow_ytd")-S("net_cash_change_ytd"),
       "9m_cash_bridge":S("cash_beginning_reported_ytd")+S("net_cash_change_ytd")-S("cash_ending"),
       "B01_B03_cash":S("cash_and_equivalents")-S("cash_ending"),
       "9m_CFI":S("capital_expenditure_ytd")-50000000000-S("investing_cash_flow_ytd"),
       "9m_CFF":50600000000+38324073000000-31679220000000+S("dividends_paid_ytd")-S("financing_cash_flow_ytd"),
       "client_custody_bridge":S("client_brokerage_cash_beginning_ytd")+S("client_brokerage_cash_change_ytd")-S("client_brokerage_cash_ending_ytd"),
       "client_custody_component":S("client_brokerage_investor_deposits_ending")+S("client_brokerage_clearing_deposits_ending")-S("client_brokerage_cash_ending_ytd"),
    }
    assert all(x==0 for x in checks.values()),checks
    assert S("client_brokerage_cash_ending_ytd")!=S("cash_ending")
    assert S("securities_margin_loans")==17307719353635
    assert len(f)==64
    return checks

def main():
    ledger,data=read(SOURCE),read(FIN)
    assert ledger["ticker"]==data["symbol"]=="VCI" and ledger["period"]=="2026-Q3"
    assert ledger["signed_no_subsidiaries_note"]=="Công ty không có công ty con"
    assert ledger["scope"]=="signed_single_company_financial_statement_no_subsidiaries_not_a_consolidated_report"
    assert ledger["original_pdf_sha256"]=="not_retrieved_in_this_session"
    assert ledger["original_report_pdf_url"].startswith("https://staticfile.hsx.vn/Uploads/UploadDocuments/2506191/")
    check=verify_source(ledger)
    q3=next(x for x in data["items"] if x["period"]=="2026-Q3")
    assert len(data["items"])==7
    assert "không có công ty con" in q3["report_type"].lower()
    assert "tương đương hợp nhất" in q3["report_type"].lower()
    assert q3["source_url"]==ledger["original_report_pdf_url"]
    assert q3["cashflow_period_basis"]=="year_to_date"
    assert q3["q3_standalone_cashflow_status"]=="verified_signed_9M_less_reviewed_H1_exact_VND_bridge"
    sv=q3["source_validation"]
    assert sv["reporter_has_no_subsidiaries_signed_source"] is True
    assert sv["source_is_not_an_explicit_consolidated_report"] is True
    assert sv["client_cash_outside_company_B01_verified"] is True
    assert sv["original_pdf_hash_verified"] is False
    assert sv["screenshot_b03_full_page_not_verified"] is True
    assert sv["source_audit_ledger"]==str(SOURCE.relative_to(ROOT))
    keys=set(ledger["original_vnd_fields"])
    assert keys==set(q3["financial_line_items_manually_verified_fields"])
    assert keys==set(q3["financial_line_items_extracted_fields"])
    assert not (keys&set(q3["financial_line_items_rejected_fields"]))
    for k,amount in ledger["original_vnd_fields"].items():
        assert val(q3,k)==int(amount),(k,val(q3,k),amount)
    quarter_ledger=read(ROOT/"reports/source-audits/VCI-2026Q3-reviewed-H1-signed-Q2-quarter-cash-vnd.json")
    for k,amount in quarter_ledger["quarter_2026q3_derived_vnd"].items():
        assert val(q3,k)==int(amount),(k,val(q3,k),amount)
    # Negative controls: never silently blend brokerage client money into
    # company cash or accept a corrupted source original.
    damaged=json.loads(json.dumps(ledger))
    damaged["original_vnd_fields"]["net_cash_change_ytd"]="-204162840806"
    try: verify_source(damaged)
    except AssertionError: pass
    else: raise AssertionError("Off-by-one change in source cash movement passed")
    damaged=json.loads(json.dumps(ledger))
    damaged["original_vnd_fields"]["total_assets"]="40401402835580"
    try: verify_source(damaged)
    except AssertionError: pass
    else: raise AssertionError("Off-by-one B01 total assets passed")
    print("PASS VCI signed HOSE Q3/2026 no subsidiaries, 64 VND source fields, "
          +str(len(check))+" exact-VND B01 B02 B03/custody identities, 2 negative controls.")
    print("NOT COMPLETE: earlier 6 VCI periods require original signed validation; Q3 standalone B03 verified against visual signed Q2/PwC H1.")
if __name__=="__main__":main()
