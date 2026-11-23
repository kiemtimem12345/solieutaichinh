#!/usr/bin/env python3
"""BID 2025Q4 signed first-issue vs audited FY source-vintage finance validator.

Source hashes and exact million-VND bank B01/B03/B04 identities, with strict
Q4 direct original profit and audited FY–signed 9M quarter cash separation.
Never make up an adjustment to force two accounting vintages to agree.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/BID-2025Q4-signed-original-vs-audited-FY-million-vnd.json"
PRIOR = ROOT / "reports/source-audits/BID-2025Q3-signed-9M-reviewedH1-exact-million-VND.json"
DATA = ROOT / "data/financials-BID.json"

def audit(a: dict, earlier: dict, data: dict) -> int:
    assert a["symbol"] == "BID" and a["period"] == "2025-Q4"
    assert a["scope"] == "consolidated" and a["unit"] == "triệu VND"
    qs, fs, source_ref = a["signed_Q4_original"], a["signed_FY_audited"], a["signed_Q3_9m_ref"]
    assert qs["sha256"] == "b7accd1729cac4897cfe3380cc8f6e03996a96ff842d3c31c3b95a7eb7dd2899"
    assert fs["sha256"] == "eda4f1d0a930ffefef851ead7932b401364114727efdfe909cffa6cd08c5cd7e"
    assert qs["pages"] == 37 and qs["bytes"] == 14597961
    assert fs["pages"] == 74 and fs["bytes"] == 16408061
    assert qs["visual_B01_pages"] == [4, 5] and qs["visual_B03_pages"] == [7] and qs["visual_B04_pages"] == [8, 9]
    assert fs["visual_B01_pages"] == [9, 10] and fs["visual_B03_pages"] == [12] and fs["visual_B04_pages"] == [13, 14]
    assert source_ref["source_pdf_sha256"] == earlier["q3_source"]["sha256"]
    assert source_ref["source_ledger"] == str(PRIOR.relative_to(ROOT))
    assert source_ref["B03_9m"] == earlier["B03_9m"]
    assert source_ref["B04_9m"] == earlier["B04_9m"]
    b, b_audited = a["B01_Q4_first_issued"], a["B01_FY_audited"]
    q, fy, ya = a["B03_Q4_first_issued"], a["B03_FY_first_issued"], a["B03_FY_audited"]
    nine, orig_cf, audited_cf, qc = source_ref["B03_9m"], a["B04_FY_first_issued"], a["B04_FY_audited"], a["B04_Q4_auditedFY_minus_signed9m"]
    prior_cf = source_ref["B04_9m"]
    delta = a["original_to_audited_FY_deltas"]
    e = {}
    e["B01_Q4_assets_liabs_equity"] = b["total_assets"]-b["total_liabilities"]-b["total_equity"]
    e["B01_Q4_assets_classes"] = sum(b[k] for k in (
        "cash_vault","central_bank_deposits","interbank_assets","trading_securities",
        "derivative_assets","net_customer_loans","investment_securities","longterm_investments",
        "fixed_assets","other_assets"))-b["total_assets"]
    e["B01_Q4_liability_classes"] = sum(b[k] for k in (
        "government_liabilities","interbank_liabilities","customer_deposits",
        "derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["total_liabilities"]
    e["B01_Q4_equity_classes"] = sum(b[k] for k in (
        "bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity"))-b["total_equity"]
    e["B01_FY_audited_balance"] = b_audited["total_assets"]-b_audited["total_liabilities"]-b_audited["total_equity"]
    for key, orig_key in (("assets","total_assets"),("liabilities","total_liabilities"),("equity","total_equity")):
        e["B01_vintage_"+key] = b_audited[orig_key]-b[orig_key]-delta[key]
    income_keys=("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income")
    e["Q4_B03_net_interest"] = q["gross_interest_income"]+q["interest_expense"]-q["net_interest"]
    e["Q4_B03_services"] = q["gross_service_income"]+q["service_expense"]-q["services_net"]
    e["Q4_B03_other"] = q["other_income"]+q["other_expense"]-q["other_net"]
    e["Q4_B03_opincome"] = sum(q[k] for k in income_keys)-q["operating_income"]
    for name, rec in (("first_FY",fy),("audited_FY",ya)):
        e[name+"_B03_opincome"] = sum(rec[k] for k in income_keys)-rec["operating_income"]
        e[name+"_B03_before_prov"] = rec["operating_income"]-rec["operating_expenses"]-rec["before_provision"]
        e[name+"_B03_provision"] = rec["before_provision"]-rec["credit_provision"]-rec["pretax_profit"]
        e[name+"_B03_PAT"] = rec["pretax_profit"]-rec["income_tax"]-rec["net_profit"]
        e[name+"_B03_NCI"] = rec["net_profit"]-rec["noncontrolling_profit"]-rec["parent_profit"]
    e["Q4_B03_before_prov"] = q["operating_income"]-q["operating_expenses"]-q["before_provision"]
    e["Q4_B03_pretax"] = q["before_provision"]-q["credit_provision"]-q["pretax_profit"]
    e["Q4_B03_tax"] = q["tax_current"]+q["tax_deferred"]-q["income_tax"]
    e["Q4_B03_aftertax"] = q["pretax_profit"]-q["income_tax"]-q["net_profit"]
    e["Q4_B03_parent"] = q["net_profit"]-q["noncontrolling_profit"]-q["parent_profit"]
    b03_keys=(
        "net_interest","services_net","FX_net","trading_net","invest_net",
        "other_net","contribution_income","operating_income","operating_expenses",
        "before_provision","credit_provision","pretax_profit","income_tax",
        "net_profit","noncontrolling_profit","parent_profit"
    )
    for k in b03_keys:
        e["Q4_direct_first_FY_minus_9M_"+k] = fy[k]-nine[k]-q[k]
    for k,delta_key in (
        ("operating_income","operating_income"),("operating_expenses","operating_expenses"),
        ("before_provision","before_provision"),("credit_provision","credit_provision"),
        ("pretax_profit","pretax_profit"),("income_tax","income_tax"),
        ("net_profit","net_profit"),("noncontrolling_profit","noncontrolling_profit"),
        ("parent_profit","parent_profit")
    ):
        e["audited_FY_minus_first_FY_"+k]=ya[k]-fy[k]-delta[delta_key]
    for name,rec in (("original",orig_cf),("audited",audited_cf)):
        e[name+"_B04_total"]=rec["CFO"]+rec["CFI"]+rec["CFF"]-rec["net_cash_change"]
        e[name+"_B04_cash"]=rec["opening_cash"]+rec["net_cash_change"]-rec["closing_cash"]
    for k in ("CFO","CFI","CFF","net_cash_change"):
        e["Q4_audited_FY_minus_9M_"+k] = audited_cf[k]-prior_cf[{"CFO":"cfo","CFI":"cfi","CFF":"cff","net_cash_change":"net_cash_change"}[k]]-qc[k]
        e["audited_minus_original_"+k] = audited_cf[k]-orig_cf[k]-delta[k]
    e["Q4_cash_open"] = qc["opening_cash"]-prior_cf["closing_cash"]
    e["Q4_cash_end"] = qc["closing_cash"]-audited_cf["closing_cash"]
    e["Q4_cash_sum"] = qc["CFO"]+qc["CFI"]+qc["CFF"]-qc["net_cash_change"]
    e["Q4_cash_continuity"] = qc["opening_cash"]+qc["net_cash_change"]-qc["closing_cash"]
    e["cash_vintage_close"] = audited_cf["closing_cash"]-orig_cf["closing_cash"]-delta["closing_cash"]
    e["preWC_vintage"] = (audited_cf["cash_before_working_capital_not_CFO"]-orig_cf["cash_before_working_capital_not_CFO"]-delta["cash_before_working_capital"])
    assert len(e) >= 65 and all(v == 0 for v in e.values()), (len(e), {k:v for k,v in e.items() if v})
    assert orig_cf["cash_before_working_capital_not_CFO"] == 54096862
    assert audited_cf["cash_before_working_capital_not_CFO"] == 54114415
    assert audited_cf["CFO"] == 192940485 and audited_cf["CFO"] != audited_cf["cash_before_working_capital_not_CFO"]
    assert q["pretax_profit"]==14230489 and q["net_profit"]==11542620
    assert ya["pretax_profit"]==37787518 and delta["pretax_profit"]==-75372
    assert (qc["CFO"],qc["CFI"],qc["CFF"],qc["net_cash_change"])==(81100023,-352358,-55221,80692444)
    assert (qc["opening_cash"],qc["closing_cash"])==(449585246,530277690)
    assert data["symbol"]=="BID" and [v["period"] for v in data["items"]]==[
        "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
    row=data["items"][3]
    assert row["verification_status"]=="issuer_signed_BID_2025Q4_first_issued_B01_B03_FY_audited_minus_signed9M_B04_verified"
    assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
    sv=row["source_validation"]
    assert sv["manually_visual_reviewed"] and sv["original_pdf_hash_verified"]
    assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
    assert sv["original_pdf_sha256"]==qs["sha256"]
    assert sv["FY_audited_source_pdf_sha256"]==fs["sha256"]
    assert sv["Q3_9M_source_pdf_sha256"]==earlier["q3_source"]["sha256"]
    assert sv["source_Q4_direct_B03_matches_FY_first_issued_minus_signed9M_exact"]
    assert sv["bank_B04_Q4_auditedFY_minus_signed9M_exact"]
    assert sv["source_vintage_difference_first_issued_vs_audited_FY"]==delta
    mapped={
        "total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
        "revenue":q["operating_income"],"pretax_profit":q["pretax_profit"],"net_profit":q["net_profit"],
        "net_profit_attributable":q["parent_profit"],"income_tax":q["income_tax"],
        "bank_cash_on_hand":b["cash_vault"],"bank_deposits_at_state_bank":b["central_bank_deposits"],
        "bank_deposits_and_loans_to_credit_institutions":b["interbank_assets"],
        "bank_customer_loans":b["net_customer_loans"],"bank_trading_securities":b["trading_securities"],
        "bank_investment_securities":b["investment_securities"],
        "bank_contributions_and_long_term_investments":b["longterm_investments"],
        "fixed_assets":b["fixed_assets"],"bank_other_assets":b["other_assets"],
        "bank_deposits_and_borrowings_from_credit_institutions":b["interbank_liabilities"],
        "bank_customer_deposits":b["customer_deposits"],"bank_valuable_papers":b["valuable_papers"],
        "bank_funding_and_trust_liabilities":b["trust_liabilities"],
        "bank_other_liabilities":b["other_liabilities"],
        "bank_net_interest_income":q["net_interest"],"bank_net_service_income":q["services_net"],
        "bank_fx_net_income":q["FX_net"],"bank_other_operating_net":q["other_net"],
        "bank_dividend_and_capital_income":q["contribution_income"],
        "bank_operating_expenses":q["operating_expenses"],
        "bank_pre_provision_operating_profit":q["before_provision"],
        "bank_provision_expense":q["credit_provision"],"bank_non_controlling_profit":q["noncontrolling_profit"],
        "operating_profit":q["before_provision"],
        "operating_cash_flow_ytd":audited_cf["CFO"],"investing_cash_flow_ytd":audited_cf["CFI"],
        "financing_cash_flow_ytd":audited_cf["CFF"],"net_cash_change_ytd":audited_cf["net_cash_change"],
        "cash_beginning_reported_ytd":audited_cf["opening_cash"],"cash_ending_ytd":audited_cf["closing_cash"],
        "operating_cash_flow":qc["CFO"],"investing_cash_flow":qc["CFI"],
        "financing_cash_flow":qc["CFF"],"net_cash_change":qc["net_cash_change"],
        "cash_beginning":qc["opening_cash"],"cash_ending":qc["closing_cash"]
    }
    assert set(mapped)==set(row["financial_line_items_manually_verified_fields"])
    for field,expected in mapped.items():
        assert type(row[field]) is int and row[field]==expected, (field,row.get(field),expected)
    for prefix,items in (
        ("b01_Q4",b),("b01_FY_audited",b_audited),
        ("b03_Q4",q),("b03_FY_first_issued",fy),
        ("b03_FY_audited",ya),("b03_9m",nine),
        ("b04_FY_first_issued",orig_cf),("b04_FY_audited",audited_cf),("b04_Q4",qc)
    ):
        for key,value in items.items():
            assert row["signed_source_"+prefix+"_"+key]==value, (prefix,key)
    assert row["roa"]==round(4*100*q["net_profit"]/((b["total_assets"]+data["items"][2]["total_assets"])/2),2)==1.44
    assert row["roe"]==round(4*100*q["net_profit"]/((b["total_equity"]+data["items"][2]["equity"])/2),2)==27.03
    assert all(data["items"][i]["verification_status"].startswith("issuer_signed") for i in (0,1,2,6))
    assert data["items"][4]["verification_status"] == "issuer_signed_BID_2026Q1_consolidated_B01_B03_B04_direct_exact_verified"
    assert data["items"][5]["verification_status"] == "issuer_signed_BID_2026Q2_first_issued_B01_B03_reviewed_H1_minus_signed_Q1_B04_verified"
    assert all(not x["period"].startswith("2024") for x in data["items"])
    return len(e)

def main()->None:
    a=json.loads(LEDGER.read_text("utf-8"))
    prev=json.loads(PRIOR.read_text("utf-8"))
    fin=json.loads(DATA.read_text("utf-8"))
    n=audit(a,prev,fin)
    for case in ("asset","profit","FY_audited_profit","cash","cash_published","vintage","hash","prior","before_wc","q4_sign"):
        led,history,d=deepcopy(a),deepcopy(prev),deepcopy(fin)
        if case=="asset":led["B01_Q4_first_issued"]["total_assets"]+=1
        elif case=="profit":led["B03_Q4_first_issued"]["net_profit"]+=1
        elif case=="FY_audited_profit":led["B03_FY_audited"]["pretax_profit"]+=1
        elif case=="cash":led["B04_FY_audited"]["CFO"]+=1
        elif case=="cash_published":d["items"][3]["operating_cash_flow"]+=1
        elif case=="vintage":led["original_to_audited_FY_deltas"]["CFO"]+=1
        elif case=="hash":led["signed_FY_audited"]["sha256"]="0"*64
        elif case=="prior":d["items"][2]["verification_status"]="unverified"
        elif case=="before_wc":led["B04_FY_first_issued"]["cash_before_working_capital_not_CFO"]=192956384
        elif case=="q4_sign":led["B04_Q4_auditedFY_minus_signed9m"]["CFF"]*=(-1)
        try:audit(led,history,d)
        except (AssertionError,KeyError,TypeError):pass
        else:raise AssertionError("source corruption not detected: "+case)
    print(f"PASS BID 2025Q4 first issued 37p vs audited FY2025 74p: {n} exact accounting/quarter/vintage checks, 16 direct Q4 income bridges, 10 tamper controls.")
    print("PASS audited 2025 FY minus issuer signed 9M quarterly B04: CFO +81,100,023 CFI -352,358 CFF -55,221 net +80,692,444 million VND.")
    print("PASS Q4 first-issued direct B03 preserved; audited-version PBT -75,372 and FY CFO -15,899 separately attributed; 2026Q1,Q2 remain provisional.")
if __name__=="__main__":
    main()
