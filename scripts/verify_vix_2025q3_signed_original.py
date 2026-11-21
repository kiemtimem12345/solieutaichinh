#!/usr/bin/env python3
"""VIX 2025 Q3 issuer original RIÊNG B01/B02/B03 QA — exact VND.

VND monetary cells visually transcribed from original issuer scanned PDF pages
8–11, 13–15, 16–17. Mirror financial pages identical (only disclosure cover p2 differs).
Strictly no VND/thousand/million confusion, wrong FVTPL signs or mixing H1/9M.
"""
from decimal import Decimal
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
VND=Decimal("1000000")
Q3_LEDGER=ROOT/"reports/source-audits/VIX-2025Q3-original-B01-B02-B03-exact-vnd.json"
H1_CASH=ROOT/"reports/source-audits/VIX-2025Q1Q2-original-cash-vnd.json"
H1_B02=ROOT/"reports/source-audits/VIX-2025Q1Q2-original-B01-B02-exact-vnd.json"
DATA=ROOT/"data/financials-VIX.json"
EXTRA_B01={"current_financial_assets","current_other_assets","financial_assets_provision",
           "financial_assets_prepay","financial_services_receivables","financial_other_receivables",
           "financial_receivables_provision","long_term_financial_assets","other_non_current_assets"}
FLOW=("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","capital_expenditure")

def million(v):
    assert type(v) in (float,int),v
    d=Decimal(str(v))*VND
    assert d==d.to_integral_value(),d
    return int(d)

def verify_source(z):
    b,c,m=z["b01"],z["b02_quarter"],z["b03_9m_ytd"]
    checks={
    "b01_balance":b["total_liabilities"]+b["equity"]-b["total_assets"],
    "b01_assets":b["current_assets"]+b["non_current_assets"]-b["total_assets"],
    "b01_liabilities":b["current_liabilities"]+b["long_term_liabilities"]-b["total_liabilities"],
    "b01_current_assets":b["current_financial_assets"]+b["current_other_assets"]-b["current_assets"],
    "b01_noncurrent":b["long_term_financial_assets"]+b["fixed_assets"]+b["other_non_current_assets"]-b["non_current_assets"],
    "b01_financial_detail":sum(b[k] for k in (
       "cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets",
       "broker_lending_assets","financial_assets_provision","broker_receivables",
       "financial_assets_prepay","financial_services_receivables",
       "financial_other_receivables","financial_receivables_provision"))-b["current_financial_assets"],
    "b02_revenues":sum(c[k] for k in (
       "broker_fvtpl_gain","broker_held_to_maturity_income","broker_lending_income",
       "broker_brokerage_revenue","broker_underwriting_revenue",
       "broker_custody_revenue","broker_financial_advisory_revenue"))-c["revenue"],
    "b02_expenses":sum(c[k] for k in (
       "broker_fvtpl_loss","broker_trading_expense","broker_brokerage_expense",
       "broker_custody_expense","broker_advisory_expense","broker_other_operating_expense"))-c["broker_total_operating_expenses"],
    "b02_operations":c["revenue"]-c["broker_total_operating_expenses"]
       +c["financial_income"]-c["financial_expense"]-c["admin_expense"]-c["broker_net_operating_profit"],
    "b02_other":c["other_income"]-c["other_expense"]-c["other_profit"],
    "b02_pretax":c["broker_net_operating_profit"]+c["other_profit"]-c["pretax_profit"],
    "b02_tax":c["income_tax_current"]+c["income_tax_deferred"]-c["income_tax"],
    "b02_profit":c["pretax_profit"]-c["income_tax"]-c["net_profit"],
    "b03_cashflow":sum(m[k] for k in FLOW[:3])-m["net_cash_change"],
    "b03_cashbridge":m["cash_beginning"]+m["net_cash_change"]-m["cash_ending"]
    }
    assert len(checks)==15 and all(x==0 for x in checks.values()),checks
    assert m["cash_ending"]==b["cash_and_equivalents"]
    assert c["broker_fvtpl_loss"]==-11207793585, "Original Q3 loss row 21 is signed negative"
    assert m["operating_cash_flow"]==-7221911471398
    assert m["net_cash_change"]==216374778602
    return checks

def main():
    z=json.loads(Q3_LEDGER.read_text("utf-8"))
    h=json.loads(H1_CASH.read_text("utf-8"))
    b02_h=json.loads(H1_B02.read_text("utf-8"))
    doc=json.loads(DATA.read_text("utf-8"))
    row=next(q for q in doc["items"] if q["period"]=="2025-Q3")
    assert (z["ticker"],z["period"],z["scope"],z["original_currency"],row["unit"])==(
       "VIX","2025-Q3","separate","VND","triệu VND")
    assert z["source"]["issuer_sha256"]=="66bafedaede09d88847aa40b7278d559e21adfcd02d51a23fc7735127347f7e9"
    assert z["source"]["pdf_pixel_same_page_count"]==43
    assert z["source"]["pdf_pixel_different_pages"]==[2]
    verify_source(z)
    assert "riêng" in row["report_type"].lower() and "hợp nhất" not in row["report_type"].lower()
    s=row["source_validation"]
    assert s["original_issuer_pdf_sha256"]==z["source"]["issuer_sha256"]
    assert s["source_scope"]=="separate" and s["source_scope_verified"]
    assert s["full_b01_b02_b03_visual_reviewed"] and s["manually_visual_reviewed"]
    assert s["source_signed_original_15_exact_VND_checks"] is True
    assert s["original_vnd_ledger"]==str(Q3_LEDGER.relative_to(ROOT))
    assert s["client_cash_off_balance_separate_from_B01_and_CFO"]
    assert s["eps_quarter_reported_cell_blank"] and row["eps"] is None
    assert row["eps_ytd"]==2692
    assert row["broker_customer_deposits"] is None and row["net_profit_attributable"] is None
    assert row["verification_status"]==(
        "issuer_signed_2025Q3_separate_B01_B02_B03_exact_vnd_9m_minus_H1_quarter_cash")
    assert row["broker_fvtpl_loss"] < 0, "Negative signed expense must stay negative"
    for key,num in z["b01"].items():
        if key in EXTRA_B01:continue
        assert million(row[key])==num,("B01",key,million(row[key]),num)
    for key,num in z["b02_quarter"].items():
        assert million(row[key])==num,("B02",key,million(row[key]),num)
    for key,num in z["b02_9m_ytd"].items():
        if key=="eps_ytd":continue
        assert million(row[key+"_ytd"])==num,(key,num)
    h1=h["signed_h1_vnd"]
    nine=z["b03_9m_ytd"]
    qu={k:nine[k]-h1[k] for k in FLOW}
    qu["cash_beginning"]=h1["cash_ending"]
    qu["cash_ending"]=nine["cash_ending"]
    assert qu["operating_cash_flow"]==-4219617578960
    assert qu["investing_cash_flow"]==-350000000
    assert qu["financing_cash_flow"]==4076000000000
    assert qu["net_cash_change"]==-143967578960
    assert sum(qu[k] for k in FLOW[:3])==qu["net_cash_change"]
    assert qu["cash_beginning"]+qu["net_cash_change"]==qu["cash_ending"]
    assert million(row["cash_and_equivalents"])==nine["cash_ending"]
    assert row["cashflow_period_basis"]=="quarter"
    assert row["cashflow_ytd_period_basis"]=="nine_months"
    for k,val in qu.items():assert million(row[k])==val,("Q3 quarter",k)
    for k,val in nine.items():
        outkey=("cash_beginning_reported_ytd" if k=="cash_beginning" else
                "cash_ending_ytd" if k=="cash_ending" else k+"_ytd")
        assert million(row[outkey])==val,("9M",k)
    for key in ("revenue","pretax_profit","net_profit"):
        assert z["b02_9m_ytd"][key]==(
             b02_h["sources"]["2025-Q2"]["official_b02_ytd_"+key]+z["b02_quarter"][key])
    assert nine["cash_ending"]!=h1["cash_ending"]
    assert abs(million(row["cash_and_equivalents"])-nine["cash_ending"])==0
    # Negative test: a wrong signed-source statement value must not be silently tolerated.
    changed=json.loads(json.dumps(z));changed["b01"]["total_assets"]+=1000000
    try:verify_source(changed)
    except AssertionError:pass
    else:raise AssertionError("Modified original B01 grand total was not detected")
    changed=json.loads(json.dumps(z));changed["b02_quarter"]["broker_fvtpl_loss"] = abs(changed["b02_quarter"]["broker_fvtpl_loss"])
    try:verify_source(changed)
    except AssertionError:pass
    else:raise AssertionError("Original Q3 FVTPL signed negative was not detected")
    print("PASS: VIX separate Q3 2025 signed issuer 44p, B01/B02/B03 15 identities exact VND, "
          "9M minus signed H1 yields standalone Q3 CFO -4,219,617,578,960, CFF +4,076,000,000,000, "
          "cash 1,053,870,185,574 -> 909,902,606,614 exact; 43/44 matching public source images, "
          "EPS quarterly blank and client balances off B01 protected.")

if __name__=="__main__":main()
