#!/usr/bin/env python3
"""VCI Q1/2025: issuer-original 34-page scanned signed B01/B02/B03 + Note1, exact VND.

Visual source only, not OCR. 2025Q1 issuer had no subsidiaries; no formal
consolidated report is invented. Client-custody money excluded from issuer B03.
"""
from decimal import Decimal
from pathlib import Path
import copy
import json

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/VCI-2025Q1-signed-original-visual-vnd.json"
DATA = ROOT / "data/financials-VCI.json"
MILLION = Decimal("1000000")
ALIAS = {
  "broker_fvtpl_assets": "securities_fvtpl_assets",
  "broker_held_to_maturity_assets": "securities_htm_short",
  "broker_lending_assets": "securities_margin_loans",
  "broker_afs_assets": "securities_afs_assets",
  "broker_held_to_maturity_income": "securities_htm_interest_income",
  "broker_custody_revenue": "securities_depository_revenue",
  "broker_total_operating_revenue": "revenue",
}
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def exact(row,key):
    assert type(row.get(key)) in (int,float), (key,row.get(key))
    amount = Decimal(str(row[key])) * MILLION
    assert amount == amount.to_integral_value(),(key,amount)
    return int(amount)

def verify_source(ledger):
    assert ledger["ticker"]=="VCI" and ledger["period"]=="2025-Q1"
    assert ledger["original_pdf_sha256"]=="7be015c6a66aee0387047aa80535da1bf8133ad9d9872c43285847b531dfd69f"
    assert ledger["original_pdf_size_bytes"]==13356823 and ledger["pdf_pages"]==34
    assert ledger["signed_date"]=="2025-04-18"
    assert ledger["signed_no_subsidiaries_note"]=="Công ty không có công ty con"
    assert ledger["no_subsidiaries_note_pdf_page"]==19
    assert ledger["source_images"]["B01"]==[5,6,7]
    assert ledger["source_images"]["B02"]==[10,11,12]
    assert ledger["source_images"]["B03_company"]==[13,14]
    assert ledger["source_images"]["artifact_id"]==14713441571
    fields=ledger["original_vnd_fields"]
    assert len(fields)==48
    f=lambda k:int(fields[k])
    check={
      "B01_assets_current_plus_noncurrent": f("current_assets")+f("non_current_assets")-f("total_assets"),
      "B01_assets_liabilities_equity":f("total_assets")-f("total_liabilities")-f("equity"),
      "B01_current_financial_other":23269197505865+f("other_current_assets")-f("current_assets"),
      "B01_cash_B03_cash":f("cash_and_equivalents")-f("cash_ending"),
      "B02_operating":f("revenue")-f("securities_operating_expense")+f("financial_income")-f("financial_expense")-f("admin_expense")-f("operating_profit"),
      "B02_other":f("other_income")-f("other_expense")-f("other_profit"),
      "B02_pretax":f("operating_profit")+f("other_profit")-f("pretax_profit"),
      "B02_income_tax_split":f("income_tax_current")+f("income_tax_deferred")-f("income_tax"),
      "B02_net":f("pretax_profit")-f("income_tax")-f("net_profit"),
      "B03_cashflow_sections":f("operating_cash_flow")+f("investing_cash_flow")+f("financing_cash_flow")-f("net_cash_change"),
      "B03_cash_open_end":f("cash_beginning")+f("net_cash_change")-f("cash_ending"),
    }
    assert len(check)==11
    assert all(x==0 for x in check.values()),check
    assert all(ledger["checks_exact_vnd"][k]=="0" for k in ledger["checks_exact_vnd"])
    return check

def verify(ledger,data):
    checked=verify_source(ledger)
    assert data["symbol"]=="VCI" and len(data["items"])==7
    q1=next(x for x in data["items"] if x["period"]=="2025-Q1")
    assert q1["unit"]=="triệu VND"
    assert "không có công ty con" in q1["report_type"].lower()
    assert q1["verification_status"]=="issuer_signed_original_2025Q1_B01_B02_B03_core_verified_no_subs"
    assert q1["source_url"]==ledger["original_pdf_url"]
    sv=q1["source_validation"]
    assert sv["issuer_original_pdf_sha256"]==ledger["original_pdf_sha256"]
    assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
    assert sv["reporter_has_no_subsidiaries_signed_source"] is True
    assert sv["source_is_not_an_explicit_consolidated_report"] is True
    assert sv["source_verified_B01_B02_B03"] is True
    assert sv["client_cash_outside_company_B01_verified"] is True
    assert sv["manual_review_blocking_automatic_extraction"] is False
    assert q1["cashflow_period_basis"]=="year_to_date"
    approved=set(q1["financial_line_items_manually_verified_fields"])
    f=ledger["original_vnd_fields"]
    assert set(f).issubset(approved)
    for k,source in f.items():
        assert exact(q1,k)==int(source),(k,exact(q1,k),source)
    for k,source_key in ALIAS.items():
        assert exact(q1,k)==int(f[source_key]),(k,q1[k],f[source_key])
    for key in ("operating_cash_flow","investing_cash_flow","financing_cash_flow",
                "net_cash_change","cash_beginning","cash_ending"):
        ytd_key=key + "_ytd" if key!="cash_beginning" else "cash_beginning_reported_ytd"
        if key=="cash_ending": ytd_key="cash_ending_ytd"
        assert exact(q1,key)==exact(q1,ytd_key),(key,ytd_key)
    assert exact(q1,"cash_ending") != 0
    assert exact(q1,"broker_afs_assets")==7523915401233
    assert exact(q1,"fixed_assets")==42697960952
    assert exact(q1,"income_tax")==60239238272
    assert exact(q1,"broker_custody_revenue")==2650375165
    return checked

def main():
    ledger,data=read(LEDGER),read(DATA)
    checks=verify(ledger,data)
    # Negative controls: 1 VND source mutation, 1 VND production cash mutation,
    # or reuse of incorrect OCR AFS scalar must be rejected.
    for case in ("tax_1VND", "cash_1VND", "AFS_OCR"):
        a,b=copy.deepcopy(ledger),copy.deepcopy(data)
        if case=="tax_1VND":
            a["original_vnd_fields"]["income_tax"]=str(int(a["original_vnd_fields"]["income_tax"])+1)
        elif case=="cash_1VND":
            next(x for x in b["items"] if x["period"]=="2025-Q1")["cash_ending"]+=0.000001
        else:
            next(x for x in b["items"] if x["period"]=="2025-Q1")["broker_afs_assets"]=8
        try: verify(a,b)
        except (AssertionError,TypeError,ValueError): pass
        else: raise AssertionError("Corrupt source/production passed "+case)
    print(f"PASS VCI Q1 2025 48 exact-VND signed source cells, {len(checks)} B01 B02 B03 identities,")
    print("signed Note1 no subsidiaries, three negative controls and custody exclusion.")
    print("OTHER PERIODS PENDING: VCI Q2/2025 through Q2/2026; Q3/2026 was separately verified.")
if __name__=="__main__":main()
