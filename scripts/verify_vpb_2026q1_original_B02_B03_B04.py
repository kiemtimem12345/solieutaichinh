#!/usr/bin/env python3
"""VPB original 2026Q1 B02a B03a B04a exact source bank cash verification."""
from pathlib import Path
import json, copy
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"reports/source-audits/VPB-2026Q1-issuer-original-B02a-B03a-B04a-million-vnd.json"
PROD=ROOT/"data/financials-VPB.json"
FY=ROOT/"reports/source-audits/VPB-2025Q4-original-vs-EY-audited-FY-million-vnd.json"
STATUS="issuer_signed_VPB_2026Q1_original_B02a_B03a_B04a_true_CFO_verified"
def verify(a,d,fy):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("VPB","2026-Q1","consolidated","triệu VND")
 s=a["source"]
 assert (s["archive_sha256"],s["english_sha256"],s["vietnamese_sha256"],s["pages"],s["source_run"])==(
 "a592c1ff829656bee45856464f18321405d09bec4068cafde19d71d95b4f9533",
 "77031dda5d88561e2d5029de1f1b6e6e7276331b257b518b9755602b51fef737",
 "614be8877c21ef189da90266c5b059eb0b7d47024444156241725820bb11dcde",91,45251429408)
 b,p,c=a["B02a"],a["B03a"],a["B04a"]
 def ss(x,ks):return sum(x[k] for k in ks)
 E={}
 E["B02_assets"]=ss(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities",
 "derivative_assets","customer_loans_net","purchased_debt_net","investment_securities",
 "longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 E["B02_liabs"]=ss(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs",
 "trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 E["B02_equity"]=ss(b,("capital","funds","retained","minority"))-b["total_equity"]
 E["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["B03_operating"]=ss(p,("net_interest","services_net","FX_net","trading_net",
 "invest_net","other_net","contribution_income"))-p["operating_income"]
 E["B03_preprovision"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["B03_credit"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["B03_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["B03_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["B03_parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 E["B04_preWC"]=ss(c,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash",
 "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["B04_CFO"]=c["pre_wc_cash"]+ss(c,("assets_interbank","assets_securities","assets_derivatives",
 "assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank",
 "liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives","liabs_other"))-c["CFO"]
 E["B04_CFI"]=c["capex"]+c["asset_disposals"]+c["investment_distributions"]-c["CFI"]
 E["B04_net"]=c["CFO"]+c["CFI"]+c["CFF"]+c["FX_effect"]-c["net_cash_change"]
 E["B04_close"]=c["opening_cash"]+c["net_cash_change"]-c["closing_cash"]
 assert len(E)==18 and not any(E.values()),E
 assert b["total_assets"]==1372010032 and b["total_liabilities"]==1185405231 and b["total_equity"]==186604801
 assert (p["operating_income"],p["pretax_profit"],p["net_profit"],p["parent_profit"])==(19908207,7920786,6329468,6198661)
 assert (c["pre_wc_cash"],c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"])==(8426996,12145698,-18002,0,12127696)
 assert (c["opening_cash"],c["closing_cash"],c["FX_effect"])==(196097219,208224915,0)
 assert fy["EY_FY_B04a"]["closing_cash"]==c["opening_cash"]
 assert (fy["EY_FY_B02a"]["total_assets"],fy["EY_FY_B02a"]["total_equity"])==(1260149596,180275629)
 assert len(d["items"])==7 and [x["period"] for x in d["items"]]==[
 "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert all(d["items"][k]["verification_status"].startswith("issuer_signed_VPB_2025Q") for k in range(4))
 assert d["items"][4]["verification_status"]==STATUS
 assert d["items"][5]["verification_status"]=="issuer_signed_VPB_2026Q2_original_B02a_B03a_reviewed_H1_minus_Q1_B04a_verified"
 assert d["items"][6]["verification_status"]=="auto_extracted_pending_visual_review"
 r=d["items"][4];v=r["source_validation"]
 assert v["original_zip_sha256"]==s["archive_sha256"]
 assert v["original_pdf_sha256"]==s["english_sha256"] and v["lookup_pdf_sha256"]==s["vietnamese_sha256"]
 assert v["original_pdf_hash_verified"] and v["CFO_after_working_capital_verified"]
 assert v["prior_2025_Q1_restatement_preserved_not_overwritten"]
 assert v["source_audit_ledger"]==str(AUDIT.relative_to(ROOT))
 fields={"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
 "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
 "net_profit_attributable":p["parent_profit"],"income_tax":p["income_tax"],
 "operating_cash_flow":c["CFO"],"investing_cash_flow":c["CFI"],"financing_cash_flow":c["CFF"],
 "net_cash_change":c["net_cash_change"],"cash_beginning":c["opening_cash"],
 "cash_ending":c["closing_cash"],"eps":p["EPS"]}
 for k,val in fields.items():assert r[k]==val,(k,r.get(k),val)
 for prefix,values in (("b02a",b),("b03a",p),("b04a",c)):
  for k,val in values.items():assert r["signed_source_"+prefix+"_"+k]==val,(prefix,k)
 assert r["roa"]==round(400*p["net_profit"]/((fy["EY_FY_B02a"]["total_assets"]+b["total_assets"])/2),2)==1.92
 assert r["roe"]==round(400*p["net_profit"]/((fy["EY_FY_B02a"]["total_equity"]+b["total_equity"])/2),2)==13.80
 assert a["comparative_2025Q1"]["operating_income"]==15764151
 assert a["comparative_2025Q1"]["pretax_profit"]==5014882
 assert a["comparative_2025Q1"]["net_profit"]==3934954
 assert not any(x["period"].startswith("2024") for x in d["items"])
 return len(E),len(fields)
def main():
 a=json.loads(AUDIT.read_text("utf8"));d=json.loads(PROD.read_text("utf8"));fy=json.loads(FY.read_text("utf8"))
 n,m=verify(a,d,fy)
 tests=("asset","liabs","profit","PAT","CFO","preWC_as_CFO","CFI","CFF","net","cash_start","cash_end",
 "hash","lookup","prior_FY","source_vintage","Q4_prior_corrupt","Q2_2026_fake","Q3_2026_fake","2024_added","ratio","EPS")
 for t in tests:
  aa,dd,ff=copy.deepcopy(a),copy.deepcopy(d),copy.deepcopy(fy)
  if t=="asset":aa["B02a"]["total_assets"]+=1
  elif t=="liabs":dd["items"][4]["total_liabilities"]+=1
  elif t=="profit":aa["B03a"]["pretax_profit"]+=1
  elif t=="PAT":dd["items"][4]["net_profit"]+=1
  elif t=="CFO":aa["B04a"]["CFO"]+=1
  elif t=="preWC_as_CFO":dd["items"][4]["operating_cash_flow"]=8426996
  elif t=="CFI":dd["items"][4]["investing_cash_flow"]+=1
  elif t=="CFF":dd["items"][4]["financing_cash_flow"]=12127696
  elif t=="net":aa["B04a"]["net_cash_change"]+=1
  elif t=="cash_start":dd["items"][4]["cash_beginning"]=143002784
  elif t=="cash_end":dd["items"][4]["cash_ending"]+=1
  elif t=="hash":aa["source"]["archive_sha256"]="0"*64
  elif t=="lookup":dd["items"][4]["source_validation"]["lookup_pdf_sha256"]="0"*64
  elif t=="prior_FY":ff["EY_FY_B04a"]["closing_cash"]+=1
  elif t=="source_vintage":aa["comparative_2025Q1"]["operating_income"]+=1
  elif t=="Q4_prior_corrupt":dd["items"][3]["verification_status"]="bad"
  elif t=="Q2_2026_fake":dd["items"][5]["verification_status"]="verified_without_source"
  elif t=="Q3_2026_fake":dd["items"][6]["verification_status"]="verified_without_source"
  elif t=="2024_added":dd["items"].append({"period":"2024-Q4"})
  elif t=="ratio":dd["items"][4]["roe"]=13.52
  elif t=="EPS":dd["items"][4]["eps"]+=1
  try:verify(aa,dd,ff)
  except (AssertionError,IndexError,KeyError,TypeError):pass
  else:raise AssertionError("VPB 2026 Q1 tamper escaped: "+t)
 print(f"PASS VPB 2026Q1 91p issuer original B02 B03 B04: {n} exact identities, {m} primary fields, {len(tests)} corruption tests")
 print("PASS signed bank CFO 12,145,698, CFI -18,002, CFF 0, net 12,127,696, opening 196,097,219 ending 208,224,915; ROA 1.92%, ROE 13.80%")
if __name__=="__main__":main()
