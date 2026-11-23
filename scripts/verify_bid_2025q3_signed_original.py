#!/usr/bin/env python3
"""BID 2025-Q3 source-ledger financial accounting test, read-only.

Signed Q3 37-page original B01/B03/B04 + reviewed 2025H1 56-page Deloitte
cash and income. VND units: million. Q3 cash is 9M - reviewed H1.
Never mistake 9M B04 cash before working capital for final bank CFO.
"""
from copy import deepcopy
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/BID-2025Q3-signed-9M-reviewedH1-exact-million-VND.json"
FIN = ROOT / "data/financials-BID.json"
OLD_H1 = ROOT / "reports/source-audits/BID-2025Q2-first-issued-vs-reviewed-H1-million-vnd.json"

def verify(a: dict, data: dict, prior: dict) -> int:
    assert a["symbol"] == "BID" and a["period"] == "2025-Q3" and a["scope"] == "consolidated"
    assert a["unit"] == "triệu VND"
    assert a["q3_source"]["sha256"] == "5283ee384a660d7b7c419a98d3960fe6c30dedf14fd36058443a869442586262"
    assert a["q3_source"]["pages"] == 37 and a["q3_source"]["bytes"] == 16522028
    assert a["q3_source"]["visual_B01_pages"] == [4, 5] and a["q3_source"]["visual_B03_pages"] == [7]
    assert a["q3_source"]["visual_B04_pages"] == [8, 9]
    assert a["h1_reviewed"]["sha256"] == prior["reviewed_h1"]["sha256"] == "d55bbf4993c254d4a5275af7f75b8e717f7f397b04141a499a671833236d0f41"
    assert a["h1_reviewed"]["B03_6m"] == prior["B03_H1_reviewed_6m"]
    assert a["h1_reviewed"]["B04_6m"] == prior["B04_H1_reviewed_6m"]
    b, q, y, c = a["B01_q3"], a["B03_q3"], a["B03_9m"], a["B04_9m"]
    h3, h4, qc = a["h1_reviewed"]["B03_6m"], a["h1_reviewed"]["B04_6m"], a["B04_q3_from_reviewedH1"]
    E = {}
    E["B01_balance"] = b["total_assets"] - b["total_liabilities"] - b["total_equity"]
    E["B01_assets"] = sum(b[k] for k in (
        "cash_vault","central_bank_deposits","interbank_assets","trading_securities",
        "derivative_assets","net_customer_loans","investment_securities",
        "longterm_investments","fixed_assets","other_assets")) - b["total_assets"]
    E["B01_liabilities"] = sum(b[k] for k in (
        "government_liabilities","interbank_liabilities","customer_deposits",
        "derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities")) - b["total_liabilities"]
    E["B01_equity"] = sum(b[k] for k in (
        "bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity")) - b["total_equity"]
    E["B03_Q3_interest"] = q["interest_income"] + q["interest_expense"] - q["net_interest"]
    E["B03_Q3_services"] = q["service_income"] + q["service_expense"] - q["services_net"]
    E["B03_Q3_other"] = q["other_income"] + q["other_expense"] - q["other_net"]
    income_cols = ("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income")
    E["B03_Q3_seven_components"] = sum(q[k] for k in income_cols) - q["operating_income"]
    E["B03_9m_seven_components"] = sum(y[k] for k in income_cols) - y["operating_income"]
    E["B03_Q3_before_prov"] = q["operating_income"] - q["operating_expenses"] - q["before_provision"]
    E["B03_9m_before_prov"] = y["operating_income"] - y["operating_expenses"] - y["before_provision"]
    E["B03_Q3_pretax"] = q["before_provision"] - q["credit_provision"] - q["pretax_profit"]
    E["B03_9m_pretax"] = y["before_provision"] - y["credit_provision"] - y["pretax_profit"]
    E["B03_Q3_tax"] = q["tax_current"] + q["tax_deferred"] - q["income_tax"]
    E["B03_Q3_PAT"] = q["pretax_profit"] - q["income_tax"] - q["net_profit"]
    E["B03_9m_PAT"] = y["pretax_profit"] - y["income_tax"] - y["net_profit"]
    E["B03_Q3_NCI"] = q["net_profit"] - q["noncontrolling_profit"] - q["parent_profit"]
    E["B03_9m_NCI"] = y["net_profit"] - y["noncontrolling_profit"] - y["parent_profit"]
    # The original current Q3 B03 and independently reviewed H1 must bridge
    # all 16 source financial statement line items with zero difference.
    for key in (
        "net_interest","services_net","FX_net","trading_net","invest_net",
        "other_net","contribution_income","operating_income","operating_expenses",
        "before_provision","credit_provision","pretax_profit","income_tax",
        "net_profit","noncontrolling_profit","parent_profit"
    ):
        E["B03_Q3_9M_minus_H1_" + key] = y[key] - h3[key] - q[key]
    E["B04_pre_WC"] = sum(c[k] for k in (
        "interest_received","interest_paid","services_cash","trading_fx_cash",
        "other_cash","recovered_bad_debt_cash","staff_cash","tax_paid"
    )) - c["before_wc_cash"]
    asset_keys = ("asset_interbank","asset_securities","asset_derivatives",
                  "asset_customer_loans","asset_credit_provisions","asset_other")
    liability_keys = ("liability_government","liability_interbank",
                      "liability_customer_deposits","liability_valuable_papers",
                      "liability_trust","liability_derivatives","liability_other")
    E["B04_CFO_after_WC"] = c["before_wc_cash"] + sum(c[k] for k in asset_keys) + sum(c[k] for k in liability_keys) - c["cfo"]
    E["B04_CFI"] = sum(c[k] for k in ("capex","disposal_proceeds","disposal_costs","investment_dividends")) - c["cfi"]
    E["B04_CFF"] = sum(c[k] for k in ("financing_new_equity","financing_new_debt","financing_repaid_debt")) - c["cff"]
    E["B04_9M_cashflow"] = c["cfo"] + c["cfi"] + c["cff"] - c["net_cash_change"]
    E["B04_9M_cash_openclose"] = c["opening_cash"] + c["net_cash_change"] - c["closing_cash"]
    for part in ("cfo","cfi","cff","net_cash_change"):
        E["B04_Q3_9M_minus_H1_" + part] = c[part] - h4[part] - qc[part]
    E["B04_Q3_open"] = qc["opening_cash"] - h4["closing_cash"]
    E["B04_Q3_close"] = qc["closing_cash"] - c["closing_cash"]
    E["B04_Q3_cashflow"] = qc["cfo"] + qc["cfi"] + qc["cff"] - qc["net_cash_change"]
    E["B04_Q3_openclose"] = qc["opening_cash"] + qc["net_cash_change"] - qc["closing_cash"]
    E["B04_Q3_investing_components"] = sum(qc[k] for k in (
        "capex","disposal_proceeds","disposal_costs","investment_dividends")) - qc["cfi"]
    E["B04_Q3_financing_components"] = sum(qc[k] for k in (
        "financing_new_equity","financing_new_debt","financing_repaid_debt")) - qc["cff"]
    E["B04_opening_same_fiscal_year"] = c["opening_cash"] - h4["year_open_cash"]
    assert len(E) >= 45 and all(value == 0 for value in E.values()), E
    assert c["cfo"] == 111840462 and c["before_wc_cash"] == 36296638 and c["before_wc_cash"] != c["cfo"]
    assert qc["cfo"] == 21370660 and qc["cfi"] == -418818 and qc["cff"] == 1110001
    assert qc["net_cash_change"] == 22061843 and qc["opening_cash"] == 427523403
    assert qc["closing_cash"] == 449585246
    assert data["symbol"] == "BID" and len(data["items"]) == 7
    assert [x["period"] for x in data["items"]] == [
        "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"
    ]
    row = data["items"][2]
    assert row["unit"] == "triệu VND" and "hợp nhất" in row["report_type"].lower()
    assert row["verification_status"] == "issuer_signed_BID_2025Q3_consolidated_B01_B03_B04_reviewedH1_quarter_exact_verified"
    source = row["source_validation"]
    assert source["manually_visual_reviewed"] and source["original_pdf_hash_verified"]
    assert source["source_audit_ledger"] == str(LEDGER.relative_to(ROOT))
    assert source["original_pdf_sha256"] == a["q3_source"]["sha256"]
    assert source["H1_source_pdf_sha256"] == a["h1_reviewed"]["sha256"]
    assert source["source_B03_Q3_16_exact_direct_income_9M_less_H1"]
    assert source["bank_B04_Q3_cash_from_9M_minus_reviewed_H1"]
    assert source["bank_B04_before_working_capital_NOT_CFO"] == c["before_wc_cash"]
    assert row["total_assets"] == b["total_assets"] and row["total_liabilities"] == b["total_liabilities"]
    assert row["equity"] == b["total_equity"] and row["pretax_profit"] == q["pretax_profit"]
    assert row["net_profit"] == q["net_profit"] and row["net_profit_attributable"] == q["parent_profit"]
    assert row["revenue"] == q["operating_income"]
    assert row["operating_cash_flow"] == qc["cfo"] and row["investing_cash_flow"] == qc["cfi"]
    assert row["financing_cash_flow"] == qc["cff"] and row["net_cash_change"] == qc["net_cash_change"]
    assert row["cash_beginning"] == qc["opening_cash"] and row["cash_ending"] == qc["closing_cash"]
    assert row["operating_cash_flow_ytd"] == c["cfo"] and row["investing_cash_flow_ytd"] == c["cfi"]
    assert row["financing_cash_flow_ytd"] == c["cff"] and row["net_cash_change_ytd"] == c["net_cash_change"]
    assert row["roa"] == round(4*100*q["net_profit"]/((b["total_assets"]+data["items"][1]["total_assets"])/2),2) == 0.80
    assert row["roe"] == round(4*100*q["net_profit"]/((b["total_equity"]+data["items"][1]["equity"])/2),2) == 14.72
    for prefix, ledger_rows in (
        ("b01_q3",b),("b03_q3",q),("b03_9m",y),
        ("b04_9m",c),("b04_q3",qc)
    ):
        for k,value in ledger_rows.items():
            assert row["signed_source_"+prefix+"_"+k] == value, (prefix,k)
    assert all(row["period"][:4] != "2024" for row in data["items"])
    assert data["items"][0]["verification_status"] == "issuer_signed_BID_2025Q1_consolidated_B01_B03_B04_exact_VND_verified"
    assert data["items"][1]["verification_status"] == "issuer_signed_BID_2025Q2_first_issued_B01_B03_reviewedH1_minus_Q1_B04_verified"
    assert data["items"][3]["verification_status"] == "issuer_signed_BID_2025Q4_first_issued_B01_B03_FY_audited_minus_signed9M_B04_verified"
    assert data["items"][4]["verification_status"] == "issuer_signed_BID_2026Q1_consolidated_B01_B03_B04_direct_exact_verified"
    assert data["items"][5]["verification_status"] == "issuer_signed_BID_2026Q2_first_issued_B01_B03_reviewed_H1_minus_signed_Q1_B04_verified"
    assert data["items"][-1]["verification_status"] == "issuer_signed_BID_2026Q3_consolidated_B01_B03_B04_reviewedH1_quarter_verified"
    return len(E)

def main():
    ledger=json.loads(LEDGER.read_text("utf-8"))
    fin=json.loads(FIN.read_text("utf-8"))
    previous=json.loads(OLD_H1.read_text("utf-8"))
    n=verify(ledger,fin,previous)
    for case in ("balance","income","cash","published_cash","prior","hash","h1_source","ratio","bad_pre_wc"):
        a,d,p=deepcopy(ledger),deepcopy(fin),deepcopy(previous)
        if case=="balance":a["B01_q3"]["total_assets"]+=1
        elif case=="income":a["B03_9m"]["net_profit"]+=1
        elif case=="cash":a["B04_9m"]["cfo"]+=1
        elif case=="published_cash":d["items"][2]["operating_cash_flow"]=36296638
        elif case=="prior":d["items"][1]["verification_status"]="unverified"
        elif case=="hash":a["q3_source"]["sha256"]="0"*64
        elif case=="h1_source":p["B04_H1_reviewed_6m"]["cfo"]+=1
        elif case=="ratio":d["items"][2]["roe"]=99
        elif case=="bad_pre_wc":a["B04_9m"]["before_wc_cash"]=111840462
        try:verify(a,d,p)
        except (AssertionError,KeyError,TypeError):pass
        else:raise AssertionError("Uncaught corruption "+case)
    print(f"PASS BID Q3 2025 signed original PDF 37p, Deloitte H1 reviewed 56p; {n} exact B01 B03 B04/quarter identities, 16 direct income bridges, 9 corruption controls.")
    print("PASS BID Q3 2025 standalone CFO 21,370,660 CFI -418,818 CFF +1,110,001 net +22,061,843; original 2025Q1 Q2 and 2026Q3 unchanged.")
if __name__=="__main__":main()
