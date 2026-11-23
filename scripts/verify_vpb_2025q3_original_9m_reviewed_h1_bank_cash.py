#!/usr/bin/env python3
"""VPB Q3/2025 signed original issuer ZIP B02a B03a, 9M B04a less reviewed H1 bank-cash QA.
Reject OCR pre-working-capital CFO, wrong original capital, year-to-date cash displayed as Q3,
forged FX or CFF, and premature completion of other periods.
"""
from copy import deepcopy
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/VPB-2025Q3-original-9M-reviewedH1-bank-B02a-B03a-B04a-million-vnd.json"
H1_LEDGER=ROOT/"reports/source-audits/VPB-2025Q2-original-reviewedH1-B02a-B03a-B04a-million-vnd.json"
DATA=ROOT/"data/financials-VPB.json"
STATUS="issuer_signed_VPB_2025Q3_original_B02a_B03a_9M_minus_reviewedH1_B04a_verified"
Q1_STATUS="issuer_signed_VPB_2025Q1_consolidated_B02a_B03a_B04a_cash_opening_corrected_verified"
Q2_STATUS="issuer_signed_VPB_2025Q2_original_B02a_B03a_reviewed_H1_minus_Q1_bank_B04a_verified"

def verify(a,f,prev):
    assert (a["symbol"],a["period"],a["scope"],a["unit"])==("VPB","2025-Q3","consolidated","triệu VND")
    z=a["sources"]["original_zip"];u=a["sources"]["issuer_lookup"]
    assert (z["archive_sha256"],z["archive_bytes"],z["original_pdf_sha256"],z["original_pdf_bytes"],
        z["original_pdf_pages"],z["lookup_member_sha256"],z["source_run"])==(
       "cfd78534904b1cb7e95a91b1f798ee3d1fe6fb051ed24eaae28a5edca4348474",7781593,
       "8161383cd1b2c3101f96dd9ac245e5699846baf802dd0277d2167096e1d736f5",6614156,
       95,"dc47ad04aa480c50c169bf840ab435468f2cafa1274c7d9e840f171c8ff58406",45247116874)
    assert (u["sha256"],u["bytes"],u["pages"],u["B02a_pages"],u["B03a_page"],u["B04a_pages"])==(
       z["lookup_member_sha256"],1503053,95,[5,6],8,[9,10])
    assert a["sources"]["reviewed_H1"]["sha256"] == prev["sources"]["reviewed_H1"]["sha256"]
    assert a["B04a_reviewed_H1"]==prev["B04a_reviewed_H1"]
    assert a["prior_Q2_B02a"] == {"assets":1104718510,"equity":152182685}
    b,p,c,h,q=(a[k] for k in ("B02a","B03a","B04a_original_9M","B04a_reviewed_H1","B04a_standalone_Q3"))
    def ss(x, keys):return sum(x[k] for k in keys)
    E={}
    E["B02_assets"]=ss(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities",
      "derivative_assets","customer_loans_net","purchased_debt_net","investment_securities",
      "longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
    E["B02_liabs"]=ss(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs",
      "trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
    E["B02_equity"]=ss(b,("capital","funds","retained","minority"))-b["total_equity"]
    E["B02_balanced"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
    E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
    E["B03_service"]=p["service_income"]+p["service_expense"]-p["services_net"]
    E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
    E["B03_operating"]=ss(p,("net_interest","services_net","FX_net","trading_net",
       "invest_net","other_net","contribution_income"))-p["operating_income"]
    E["B03_pre_provision"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
    E["B03_provision"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
    E["B03_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
    E["B03_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
    E["B03_parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
    E["B04_preWC"]=ss(c,("interest_cash_received","interest_cash_paid","services_cash",
       "fx_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
    E["B04_true_CFO"]=c["pre_wc_cash"]+ss(c,("assets_interbank","assets_securities",
       "assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other",
       "liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers",
       "liabs_trust","liabs_derivatives","liabs_other"))-c["CFO"]
    E["B04_CFI"]=c["capex"]+c["asset_disposals"]+c["investment_distributions"]-c["CFI"]
    E["B04_CFF"]=c["dividends"]-c["CFF"]
    E["B04_9M_net"]=c["CFO"]+c["CFI"]+c["CFF"]+c["FX_effect"]-c["net_cash_change"]
    E["B04_9M_cash"]=c["opening_cash"]+c["net_cash_change"]-c["closing_cash"]
    E["H1_begin"]=h["opening_cash"]-c["opening_cash"]
    for k in ("CFO","CFI","CFF","net_cash_change","FX_effect"):
        E["Q3_9M_lessH1_"+k]=c[k]-h[k]-q[k]
    E["Q3_start"]=h["closing_cash"]-q["opening_cash"]
    E["Q3_close"]=c["closing_cash"]-q["closing_cash"]
    E["Q3_net"]=q["CFO"]+q["CFI"]+q["CFF"]+q["FX_effect"]-q["net_cash_change"]
    E["Q3_cash"]=q["opening_cash"]+q["net_cash_change"]-q["closing_cash"]
    E["Q3_capex"]=c["capex"]-h["capex"]-q["capex"]
    assert len(E)>=28 and all(v==0 for v in E.values()),E
    assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(1178298568,1018753281,159545287)
    assert (p["operating_income"],p["pretax_profit"],p["net_profit"],p["parent_profit"])==(20137556,9166297,7363737,7275479)
    assert (c["pre_wc_cash"],c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["opening_cash"],c["closing_cash"])==(
      33575584,27397628,-31788,-3968172,23397668,143002784,166400452)
    assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["opening_cash"],q["closing_cash"],q["FX_effect"])==(
      4043752,-2135,0,4041617,162358835,166400452,0)
    assert c["pre_wc_cash"]!=c["CFO"] and c["net_cash_change"]!=c["CFO"]
    assert (f["symbol"],[x["period"] for x in f["items"]])==("VPB",
      ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"])
    assert [x["verification_status"] for x in f["items"]]==[
      Q1_STATUS,Q2_STATUS,STATUS,"issuer_signed_VPB_2025Q4_original_B02a_B03a_EY_FY_minus_signed9M_bank_B04a_verified",
      "issuer_signed_VPB_2026Q1_original_B02a_B03a_B04a_true_CFO_verified","issuer_signed_VPB_2026Q2_original_B02a_B03a_reviewed_H1_minus_Q1_B04a_verified",
      "auto_extracted_pending_visual_review"]
    assert f["items"][1]["cash_ending"]==q["opening_cash"]
    assert f["items"][1]["operating_cash_flow_ytd"]==h["CFO"]
    row=f["items"][2];sv=row["source_validation"]
    assert row["unit"]=="triệu VND" and row["verification_status"]==STATUS
    assert sv["original_zip_sha256"]==z["archive_sha256"] and sv["original_zip_hash_verified"]
    assert sv["original_pdf_sha256"]==z["original_pdf_sha256"]
    assert sv["issuer_lookup_pdf_sha256"]==u["sha256"]
    assert sv["issuer_lookup_matches_ZIP_member"]
    assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
    assert sv["original_B02a_B03a_9M_B04a_pages_checked"] and sv["bank_9M_minus_reviewed_H1_cash_bridge_exact"]
    assert sv["manually_visual_reviewed"] and sv["no_2024_dashboard_periods"]
    mp={
      "total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],
      "equity":b["total_equity"],"revenue":p["operating_income"],
      "pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
      "net_profit_attributable":p["parent_profit"],"bank_cash_on_hand":b["cash_vault"],
      "bank_deposits_at_state_bank":b["deposits_SBV"],
      "bank_deposits_and_loans_to_credit_institutions":b["interbank_assets"],
      "bank_deposits_and_borrowings_from_credit_institutions":b["interbank_liabs"],
      "bank_customer_deposits":b["customer_deposits"],"bank_customer_loans":b["customer_loans_net"],
      "bank_purchased_debt_net":b["purchased_debt_net"],"bank_other_assets":b["other_assets"],
      "fixed_assets":b["fixed_assets"],"retained_earnings":b["retained"],
      "bank_net_interest_income":p["net_interest"],"bank_net_service_income":p["services_net"],
      "bank_operating_expenses":p["operating_expenses"],"bank_provision_expense":p["credit_provision"],
      "bank_pre_provision_operating_profit":p["before_provision"],"income_tax":p["income_tax"],
      "income_tax_current":p["income_tax_current"],"income_tax_deferred":p["income_tax_deferred"],
      "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],
      "financing_cash_flow":q["CFF"],"net_cash_change":q["net_cash_change"],
      "cash_beginning":q["opening_cash"],"cash_ending":q["closing_cash"],"cashflow_fx":q["FX_effect"],
      "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
      "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],
      "cash_beginning_reported_ytd":c["opening_cash"],"cash_ending_ytd":c["closing_cash"],
      "capital_expenditure":q["capex"],"capital_expenditure_ytd":c["capex"]
    }
    for k,v in mp.items():assert row[k]==v,(k,row.get(k),v)
    for prefix,raw in (("b02a",b),("b03a",p),("b04a_9m",c)):
        for k,v in raw.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
    assert row["roa"]==round(400*p["net_profit"]/((a["prior_Q2_B02a"]["assets"]+b["total_assets"])/2),2)==2.58
    assert row["roe"]==round(400*p["net_profit"]/((a["prior_Q2_B02a"]["equity"]+b["total_equity"])/2),2)==18.9
    assert not any(x["period"].startswith("2024") for x in f["items"])
    return len(E),len(mp)

def main():
    a=json.loads(LEDGER.read_text("utf-8"))
    f=json.loads(DATA.read_text("utf-8"))
    prior=json.loads(H1_LEDGER.read_text("utf-8"))
    n,m=verify(a,f,prior)
    cases=("assets","liabs","PAT","operating_income","tax","CFO_preWC","CFO_changed",
      "CFI_changed","Q3_wrong_CFO","Q3_wrong_CFF","Q3_wrong_cash","bad_FX",
      "bad_zip_sha","bad_original_sha","bad_H1_vintage","bad_YTD_open","bad_roa",
      "bad_Q1","bad_Q2","premature_Q4","add_2024")
    for kind in cases:
        aa,ff,pp=deepcopy(a),deepcopy(f),deepcopy(prior)
        if kind=="assets":aa["B02a"]["total_assets"]+=1
        elif kind=="liabs":ff["items"][2]["total_liabilities"]+=1
        elif kind=="PAT":ff["items"][2]["net_profit"]+=1
        elif kind=="operating_income":aa["B03a"]["operating_income"]+=1
        elif kind=="tax":aa["B03a"]["income_tax_current"]+=1
        elif kind=="CFO_preWC":ff["items"][2]["operating_cash_flow_ytd"]=33575584
        elif kind=="CFO_changed":aa["B04a_original_9M"]["CFO"]+=1
        elif kind=="CFI_changed":aa["B04a_original_9M"]["CFI"]+=1
        elif kind=="Q3_wrong_CFO":ff["items"][2]["operating_cash_flow"]=27397628
        elif kind=="Q3_wrong_CFF":ff["items"][2]["financing_cash_flow"]=-3968172
        elif kind=="Q3_wrong_cash":aa["B04a_standalone_Q3"]["closing_cash"]+=1
        elif kind=="bad_FX":aa["B04a_standalone_Q3"]["FX_effect"]=100
        elif kind=="bad_zip_sha":aa["sources"]["original_zip"]["archive_sha256"]="0"*64
        elif kind=="bad_original_sha":aa["sources"]["original_zip"]["original_pdf_sha256"]="0"*64
        elif kind=="bad_H1_vintage":pp["B04a_reviewed_H1"]["CFO"]+=1
        elif kind=="bad_YTD_open":ff["items"][2]["cash_beginning_reported_ytd"]=162358835
        elif kind=="bad_roa":ff["items"][2]["roa"]=0
        elif kind=="bad_Q1":ff["items"][0]["verification_status"]="corrupted"
        elif kind=="bad_Q2":ff["items"][1]["cash_ending"]+=1
        elif kind=="premature_Q4":ff["items"][3]["verification_status"]="premature_verified"
        elif kind=="add_2024":ff["items"].append({"period":"2024-Q4"})
        try:verify(aa,ff,pp)
        except (AssertionError,KeyError,TypeError,IndexError):pass
        else:raise AssertionError("VPB Q3 source tamper escaped: "+kind)
    print(f"PASS VPB 2025Q3 original 95p ZIP and issuer lookup PDF: {n} exact identities, {m} normalized checks, {len(cases)} negative tamper guards")
    print("PASS bank Q3 original 9M minus reviewed H1: CFO +4,043,752 CFI -2,135 CFF 0 net +4,041,617 cash 162,358,835 to 166,400,452 million VND")
    print("PASS prior VPB signed Q1/Q2 unchanged, later four quarters provisional and no 2024 dashboard periods")

if __name__=="__main__":main()
