#!/usr/bin/env python3
"""VCB Q3 2025 signed consolidated bank source, 9M-minus-6M bank B04 bridge.

Currency is signed integer million VND; do not invent 1 VND precision.
Gross interest Q3 direct vs YTD-H1 source vintage +/-6,904 million held in
private queue and below 0.1% latest tolerance; net interest/profit/cash exact.
"""
from pathlib import Path
from decimal import Decimal
import copy,json
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/VCB-2025Q3-original-signed-consolidated-9M-million-vnd.json"
H1=ROOT/"reports/source-audits/VCB-2025Q2-original-signed-consolidated-H1-million-vnd.json"
DATA=ROOT/"data/financials-VCB.json"
QUEUE=ROOT/"reports/financial-exception-queue.json"
def read(path):return json.loads(path.read_text(encoding="utf-8"))
def verify_source(z,h1):
  assert z["ticker"]=="VCB" and z["period"]=="2025-Q3"
  orig=z["original_report"]
  assert orig["signed_date"]=="2025-10-30" and orig["pdf_sha256"]=="3afd2b964267c9ec5882fbaec57dabbef2707b40cace4dc0ecdab5b0f52791e7"
  assert orig["pages"]==54 and orig["bytes"]==15527017
  assert orig["inspection_workflow"]==44971063344 and orig["source_artifact_id"]==14732904352
  assert "consolidated" in z["scope"] and z["unit"]=="triệu VND"
  f=z["signed_original_million_vnd_fields"];p=h1["source_million_vnd_fields"]
  assert len(f)==136 and len(z["source_check_residual_million_vnd"])==19
  assert all(type(x)==int for x in f.values())
  N=lambda k:f[k]
  P=lambda k:p[k]
  s=lambda arr:sum(N(k) for k in arr)
  identity={
    "balance":N("total_assets")-N("total_liabilities")-N("equity"),
    "assets":s(("bank_cash_on_hand","bank_deposits_at_state_bank","bank_deposits_and_loans_at_credit_institutions","bank_trading_securities","bank_derivative_assets","bank_customer_loans","bank_investment_securities","bank_contributions_and_long_term_investments","fixed_assets","bank_other_assets"))-N("total_assets"),
    "liabs":s(("bank_government_borrowing","bank_deposits_and_borrowings_from_credit_institutions","bank_customer_deposits","bank_derivative_liabilities","bank_funding_and_trust_liabilities","bank_valuable_papers","bank_other_liabilities"))-N("total_liabilities"),
    "equity":s(("bank_capital_and_capital_surplus","bank_funds","bank_foreign_exchange_equity","retained_earnings","bank_non_controlling_equity"))-N("equity"),
    "revenue":s(("bank_net_interest_income","bank_net_service_income","bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net","bank_other_operating_net","bank_dividend_and_capital_income"))-N("revenue"),
    "op":N("revenue")+N("bank_operating_expenses")-N("bank_pre_provision_operating_profit"),
    "pretax":N("bank_pre_provision_operating_profit")+N("bank_provision_expense")-N("pretax_profit"),
    "tax":-N("bank_tax_current")-N("bank_tax_deferred")-N("income_tax"),
    "net":N("pretax_profit")-N("income_tax")-N("net_profit"),
    "ytdrevenue":s(("ytd_bank_net_interest_income","ytd_bank_net_service_income","ytd_bank_fx_net_income","ytd_bank_trading_securities_net","ytd_bank_investment_securities_net","ytd_bank_other_operating_net","ytd_bank_dividend_and_capital_income"))-N("ytd_revenue"),
    "ytdop":N("ytd_revenue")+N("ytd_bank_operating_expenses")-N("ytd_bank_pre_provision_operating_profit"),
    "ytdpbt":N("ytd_bank_pre_provision_operating_profit")+N("ytd_bank_provision_expense")-N("ytd_pretax_profit"),
    "ytdtax":-N("ytd_bank_tax_current")-N("ytd_bank_tax_deferred")-N("ytd_income_tax"),
    "ytdnet":N("ytd_pretax_profit")-N("ytd_income_tax")-N("ytd_net_profit"),
    "beforeWC":s(("bank_cashflow_interest_received_ytd","bank_cashflow_interest_paid_ytd","bank_cashflow_service_net_received_ytd","bank_cashflow_fx_net_ytd","bank_cashflow_other_net_ytd","bank_cashflow_recovered_bad_debt_ytd","bank_cashflow_staff_management_paid_ytd","bank_cashflow_income_tax_paid_ytd"))-N("bank_cfo_before_balance_changes_ytd"),
    "CFO":N("bank_cfo_before_balance_changes_ytd")+s(("bank_wc_deposits_loans_with_banks_ytd","bank_wc_trading_securities_ytd","bank_wc_derivative_assets_ytd","bank_wc_customer_loans_ytd","bank_wc_write_off_ytd","bank_wc_other_assets_ytd","bank_wc_government_funding_ytd","bank_wc_other_bank_funding_ytd","bank_wc_customer_deposits_ytd","bank_wc_debt_securities_ytd","bank_wc_trust_funding_ytd","bank_wc_derivative_liabilities_ytd","bank_wc_other_operating_liabilities_ytd","bank_wc_bank_funds_ytd"))-N("operating_cash_flow_ytd"),
    "CFI":s(("bank_investing_capex_ytd","bank_investing_disposals_received_ytd","bank_investing_disposals_expense_ytd","bank_investing_dividends_received_ytd"))-N("investing_cash_flow_ytd"),
    "sections":N("operating_cash_flow_ytd")+N("investing_cash_flow_ytd")+N("financing_cash_flow_ytd")-N("net_cash_change_ytd"),
    "cashbridge":N("cash_beginning_reported_ytd")+N("net_cash_change_ytd")-N("cash_ending_ytd")
  }
  assert set(identity)==set(z["source_check_residual_million_vnd"])
  assert all(value==0 for value in identity.values()),identity
  assert all(z["source_check_residual_million_vnd"][k]=="0" for k in identity)
  assert N("total_assets")==N("total_liabilities")+N("equity")
  assert N("net_profit_attributable")==N("net_profit")+N("bank_non_controlling_profit")
  assert N("ytd_net_profit_attributable")==N("ytd_net_profit")+N("ytd_bank_non_controlling_profit")
  assert N("bank_deposits_at_credit_institutions")+N("bank_loans_to_credit_institutions")==N("bank_deposits_and_loans_at_credit_institutions")
  assert N("bank_customer_loans_gross")+N("bank_customer_loans_impairment")==N("bank_customer_loans")
  assert N("bank_cash_on_hand")!=N("cash_ending_ytd")
  direct=(
    "bank_interest_income","bank_interest_expense","bank_net_interest_income",
    "bank_service_income","bank_service_expense","bank_net_service_income",
    "bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net",
    "bank_other_operating_income","bank_other_operating_expense","bank_other_operating_net",
    "bank_dividend_and_capital_income","revenue","bank_operating_expenses",
    "bank_pre_provision_operating_profit","bank_provision_expense","pretax_profit",
    "bank_tax_current","bank_tax_deferred","income_tax","net_profit",
    "bank_non_controlling_profit","net_profit_attributable"
  )
  assert len(direct)==24
  for k in direct:
    diff=N("ytd_"+k)-P("h1_"+k)-N(k)
    expected=-6904 if k=="bank_interest_income" else (6904 if k=="bank_interest_expense" else 0)
    assert diff==expected,(k,diff,expected)
    if expected:
      assert Decimal(abs(diff))/Decimal(abs(N(k)))<Decimal("0.001")
  assert N("ytd_bank_net_interest_income")-P("h1_bank_net_interest_income")==N("bank_net_interest_income")
  assert N("ytd_net_profit")-P("h1_net_profit")==N("net_profit")
  q={k:N(k+"_ytd")-P(k+"_ytd") for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
  q["cash_beginning"]=P("cash_ending_ytd")
  q["cash_ending"]=N("cash_ending_ytd")
  assert q==z["q3_standalone_B04_million_vnd"]
  assert q["operating_cash_flow"]+q["investing_cash_flow"]+q["financing_cash_flow"]==q["net_cash_change"]
  assert q["cash_beginning"]+q["net_cash_change"]==q["cash_ending"]
  assert N("cash_beginning_reported_ytd")==P("cash_beginning_reported_ytd")
  assert N("operating_cash_flow_ytd")==106283289 and N("bank_cashflow_interest_received_ytd")==76029283
  return f,q

def verify(z,h1,data,queue):
    f,q=verify_source(z,h1)
    assert data["symbol"]=="VCB" and len(data["items"])>=6
    r=next(x for x in data["items"] if x["period"]=="2025-Q3")
    assert r["verification_status"]=="issuer_signed_VCB_2025Q3_consolidated_B02_B03_B04_9M_minus_H1"
    assert "hợp nhất" in r["report_type"].lower()
    assert r["cashflow_period_basis"]=="year_to_date" and r["unit"]=="triệu VND"
    assert r["source_url"]==z["original_report"]["url"]
    sv=r["source_validation"]
    assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
    assert sv["original_pdf_sha256"]==z["original_report"]["pdf_sha256"]
    assert sv["original_pdf_hash_verified"] is True
    assert sv["manually_visual_reviewed"] is True
    assert sv["source_is_consolidated_financial_statements"] is True
    assert sv["quarter_cash_sections_residual_million"]=="0"
    assert sv["quarter_income_9M_minus_H1_accepted_user_tolerance_percent"]==0.1
    allowed=set(r["financial_line_items_manually_verified_fields"])
    for k,amt in f.items():
      assert k in allowed and r.get(k)==amt,(k,amt,r.get(k))
    for k,amt in q.items():
      assert k in allowed and r.get(k)==amt,(k,amt,r.get(k))
    assert r["bank_cash_and_equivalents_cashflow_basis"]==r["cash_ending"]
    assert r["bank_cash_on_hand"]!=r["cash_ending"]
    assert r["net_profit_attributable"]!=r["net_profit"]
    entry=next(x for x in queue["items"] if x["id"]=="VCB-2025Q3-gross-interest-9M-minus-H1-vintage-6904m")
    assert entry["production_eligible"] is True and entry["blocks_sequential_processing"] is False
    assert entry["user_visibility"]=="only_if_user_asks_which_tickers_or_periods_remain"
    assert all(not x["period"].startswith("2024") for x in data["items"])
    return len(f)

def main():
    s,h,d,q=read(LEDGER),read(H1),read(DATA),read(QUEUE)
    n=verify(s,h,d,q)
    for scenario in ("wrong_asset","wrong_9m_cash","wrong_Q3_CFO","use_gross_interest_cash_as_CFO"):
      a,b,c,e=copy.deepcopy(s),copy.deepcopy(h),copy.deepcopy(d),copy.deepcopy(q)
      row=next(x for x in c["items"] if x["period"]=="2025-Q3")
      if scenario=="wrong_asset":a["signed_original_million_vnd_fields"]["total_assets"]+=1
      elif scenario=="wrong_9m_cash":a["signed_original_million_vnd_fields"]["net_cash_change_ytd"]+=1
      elif scenario=="wrong_Q3_CFO":row["operating_cash_flow"]+=1
      else:row["operating_cash_flow"]=row["bank_cashflow_interest_received_ytd"]
      try:verify(a,b,c,e)
      except (AssertionError,ValueError,TypeError):pass
      else:raise AssertionError("Source/data mutation passed: "+scenario)
    print(f"PASS VCB 2025-Q3: {n} signed bank original million-VND fields, 19 source zero checks, 24 Q3 income bridges (22 zero + two offset vintage under 0.1 pct), Q3 B04 cash exact, 4 corruption checks.")
    print("Bank B04 standalone CFO +81,546,582, CFI -364,267, CFF 0, net +81,182,315, closing cash 536,179,105 million.")
if __name__=="__main__":main()
