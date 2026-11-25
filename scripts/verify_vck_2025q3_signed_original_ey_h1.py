#!/usr/bin/env python3
"""Signed VPS/VCK Q3 2025 original ZIP PDF vs EY-audited H1 cash, exact VND.
No 2024 and no brokerage customer cash in issuer B01/B03.
"""
import copy,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCK-2025Q3-VPS-original-signed-EY-H1-vnd.json"
H1=ROOT/"reports/source-audits/VCK-2025Q2-VPSS-original-and-EY-H1-vintage-vnd.json"
DATA=ROOT/"data/financials-VCK.json"
M=Decimal("1000000")
def read(p):return json.loads(p.read_text("utf-8"))
def value(row,key):
    x=row.get(key)
    assert type(x) in (int,float),(key,x)
    d=Decimal(str(x))*M
    assert d==d.to_integral_value(),(key,d)
    return int(d)
def source_checks(s,h1):
    assert s["ticker"]=="VCK" and s["filing_symbol"]=="VPSS" and s["period"]=="2025-Q3"
    assert s["archive_sha256"]=="1eb8c56340d1006d5818eaf69bb415c627ea5339c47c6e435404c0ef89cbfdf4"
    assert s["original_pdf_sha256"]=="f266a63e92f12c97e84c34d93e549e94eb1b0e26cc40ba7c3002a4548efefd4f"
    assert s["original_pdf_pages"]==39 and s["original_pdf_bytes"]==2235421
    assert s["source_inspection_run"]==44932687219
    assert s["source_artifact_id"]==14718411957
    assert s["original_pdf_member"].startswith("VI_Baocaotaichinh_")
    assert "issuer" in s["scope"] and s["client_cash_outside_issuer_assets"] is True
    f=s["original_exact_vnd_fields"];assert len(f)==63
    N=lambda k:int(f[k])
    audited=h1["h1_audited"]
    assert audited["signed_date"]=="2025-09-19" and audited["signed_by"]=="Ernst & Young Vietnam Limited"
    a=audited["cashflow_6m"]
    P=lambda k:int(a[k])
    q={k:N(k+"_ytd")-P({ "operating_cash_flow":"CFO",
         "investing_cash_flow":"CFI","financing_cash_flow":"CFF",
         "net_cash_change":"net"}[k]) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
    q["cash_beginning"]=P("ending")
    q["cash_ending"]=N("cash_ending_ytd")
    assert {k:int(v) for k,v in s["q3_standalone_cash_signed_9M_minus_EY_6M_vnd"].items()}==q
    assert N("revenue_ytd")-int(h1["original_vnd_fields"]["revenue_ytd"])==N("revenue")
    assert N("pretax_profit_ytd")-int(h1["original_vnd_fields"]["pretax_profit_ytd"])==N("pretax_profit")
    assert N("net_profit_ytd")-int(h1["original_vnd_fields"]["net_profit_ytd"])==N("net_profit")
    assert N("income_tax_ytd")-int(h1["original_vnd_fields"]["income_tax_ytd"])==N("income_tax")
    identities={
        "assets":N("current_assets")+N("non_current_assets")-N("total_assets"),
        "balance":N("total_assets")-N("total_liabilities")-N("equity"),
        "liabs":N("current_liabilities")+N("long_term_liabilities")-N("total_liabilities"),
        "current_assets":N("financial_assets_current")+N("other_current_assets")-N("current_assets"),
        "non_current_assets":sum(N(k) for k in ("financial_assets_noncurrent","fixed_assets","long_term_construction_in_progress","other_non_current_assets"))-N("non_current_assets"),
        "fixed_assets":N("securities_fixed_tangible")+N("securities_fixed_intangible")-N("fixed_assets"),
        "rev_components":sum(N(k) for k in ("securities_fvtpl_gain","securities_htm_interest_income","securities_loan_interest_income","securities_brokerage_revenue","securities_depository_revenue","securities_financial_advice_revenue","securities_other_revenue"))-N("revenue"),
        "opex_components":sum(N(k) for k in ("securities_fvtpl_loss","securities_self_trading_expense","securities_brokerage_expense","securities_depository_expense","securities_financial_advice_expense"))-N("securities_operating_expense"),
        "operating":N("revenue")-N("securities_operating_expense")+N("financial_income")-N("financial_expense")-N("admin_expense")-N("operating_profit"),
        "other":N("other_income")-N("other_expense")-N("other_profit"),
        "pretax":N("operating_profit")+N("other_profit")-N("pretax_profit"),
        "profit":N("pretax_profit")-N("income_tax")-N("net_profit"),
        "ytd_op":N("revenue_ytd")-N("securities_operating_expense_ytd")+N("financial_income_ytd")-N("financial_expense_ytd")-N("admin_expense_ytd")-N("operating_profit_ytd"),
        "ytd_pretax":N("operating_profit_ytd")+N("other_profit_ytd")-N("pretax_profit_ytd"),
        "ytd_profit":N("pretax_profit_ytd")-N("income_tax_ytd")-N("net_profit_ytd"),
        "q3_revenue_bridge":N("revenue_ytd")-int(h1["original_vnd_fields"]["revenue_ytd"])-N("revenue"),
        "q3_pretax_bridge":N("pretax_profit_ytd")-int(h1["original_vnd_fields"]["pretax_profit_ytd"])-N("pretax_profit"),
        "q3_tax_bridge":N("income_tax_ytd")-int(h1["original_vnd_fields"]["income_tax_ytd"])-N("income_tax"),
        "q3_profit_bridge":N("net_profit_ytd")-int(h1["original_vnd_fields"]["net_profit_ytd"])-N("net_profit"),
        "ytd_cashflow":sum(N(k+"_ytd") for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))-N("net_cash_change_ytd"),
        "ytd_cash_bridge":N("cash_beginning_reported_ytd")+N("net_cash_change_ytd")-N("cash_ending_ytd"),
        "cash_B01_B03":N("cash_and_equivalents")-N("cash_ending_ytd"),
        "quarterly_cashflow":q["operating_cash_flow"]+q["investing_cash_flow"]+q["financing_cash_flow"]-q["net_cash_change"],
        "quarterly_cash_bridge":q["cash_beginning"]+q["net_cash_change"]-q["cash_ending"],
        "q3_prior_H1_cash":q["cash_beginning"]-P("ending"),
    }
    assert len(identities)==25 and set(identities)==set(s["checks_exact_vnd"])
    assert all(v==0 for v in identities.values()),identities
    assert all(s["checks_exact_vnd"][k]=="0" for k in identities)
    assert N("cash_and_equivalents")!=N("client_brokerage_cash_ending_ytd")
    return q
def verify(s,h1,d):
    q=source_checks(s,h1)
    assert d["symbol"]=="VCK" and len(d["items"])==7
    row=next(x for x in d["items"] if x["period"]=="2025-Q3")
    assert row["verification_status"]=="issuer_signed_VCK_Q3_2025_B01_B02_B03_9M_EY_H1_cash_exact_vnd"
    assert row["unit"]=="triệu VND" and row["cashflow_period_basis"]=="year_to_date"
    assert row["source_url"]==s["source_archive_url"]
    v=row["source_validation"]
    assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    assert v["original_pdf_sha256"]==s["original_pdf_sha256"]
    assert v["original_pdf_hash_verified"] is True
    assert v["client_cash_outside_company_B01_verified"] is True
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["ey_audited_H1_cash_quarter_bridge_residual_vnd"]=="0"
    approved=set(row["financial_line_items_manually_verified_fields"])
    for k,amount in s["original_exact_vnd_fields"].items():
        assert k in approved and value(row,k)==int(amount),(k,amount,row.get(k))
    for k,amount in q.items():
        assert k in approved and value(row,k)==amount,(k,amount,row.get(k))
    assert value(row,"cash_ending")==value(row,"cash_ending_ytd")
    assert value(row,"net_profit_attributable")==value(row,"net_profit")
    assert all(x["period"].startswith(("2025-","2026-")) for x in d["items"])
    assert not d.get("pre_listing_legacy_reports")
    # Q2 vintage has now been reconciled; preserve exact H1 and cash links.
    q2=next(x for x in d["items"] if x["period"]=="2025-Q2")
    assert q2["verification_status"]=="issuer_signed_Q2_and_EY_H1_vintage_reconciled"
    assert q2["source_validation"]["unreconciled_vintage_queued"] is False
    assert value(q2,"net_profit")==702214269106
    assert value(q2,"net_profit_ytd")==int(h1["original_vnd_fields"]["net_profit_ytd"])
    assert value(q2,"cash_ending")==value(row,"cash_beginning")
    for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change"):
        assert value(q2,k+"_ytd")+value(row,k)==value(row,k+"_ytd")
    return q
if __name__=="__main__":
    s,h,d=map(read,(SRC,H1,DATA))
    q=verify(s,h,d)
    for type_ in ("source_net_1vnd","data_q3_cfo_1vnd","custody_as_cash"):
        a,b,c=copy.deepcopy(s),copy.deepcopy(h),copy.deepcopy(d)
        row=next(x for x in c["items"] if x["period"]=="2025-Q3")
        if type_=="source_net_1vnd":
            a["original_exact_vnd_fields"]["net_cash_change_ytd"]=str(int(a["original_exact_vnd_fields"]["net_cash_change_ytd"])+1)
        elif type_=="data_q3_cfo_1vnd":row["operating_cash_flow"]+=0.000001
        else:row["cash_ending"]=row["client_brokerage_cash_ending_ytd"]
        try:verify(a,b,c)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("not rejected: "+type_)
    print("PASS VCK 2025 Q3 issuer-signed original 63 exact source values and 25 VND identities, 3 corruption tests.")
    print("Q3 CFO CFI CFF net:",*(q[k] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")))
