#!/usr/bin/env python3
"""CTG 2026 Q1 signed B02/B03/B04 and H1 signed Q2 minus Q1 exact FX-aware bank financials.
Preserve signed prior 2025 and Q3/2026 and the source-version checkpoint.
"""
import json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/CTG-2026Q1Q2-original-signed-bank-million-vnd.json"
OLDQ3=ROOT/"reports/source-audits/CTG-2026Q3-consolidated-original-9M-minus-H1-million-vnd.json"
DATA=ROOT/"data/financials-CTG.json"
S1="issuer_signed_CTG_2026Q1_original_B02a_B03a_B04a_FX_exact_verified"
S2="issuer_signed_CTG_2026Q2_original_B02a_B03a_H1_minus_signed_Q1_B04a_FX_exact_verified"
H1_SHA="f7453816648cac21536621e09d4e52a40e8ce9fcdbaf824981b3b997a8197318"
def check(a,prior,d):
 assert (a["symbol"],a["scope"],a["unit"])==("CTG","hợp nhất","triệu VND")
 s=a["source"]
 assert s["Q1_sha256"]=="0bec0f8f23b6786814f57daaedf21ce6c139a761b1168580bf1a1fdf0cfe216d"
 assert s["Q1_pages"]==62 and s["Q1_bytes"]==6340703 and s["H1_pages"]==61 and s["H1_bytes"]==6703623
 assert s["H1_sha256"]==H1_SHA==prior["original_H1"]["pdf_sha256"]
 assert s["source_run"] in (45369747279,45369836579,45368731358)
 b1,p1,c1=(a["Q1"][k] for k in ("B02","B03","B04"))
 b2,p2=(a["Q2"][k] for k in ("B02","B03"))
 h=a["H1"]["B04"];q=a["Q2_standalone_cash_H1_minus_Q1"]
 def sm(o,ks):return sum(o[k] for k in ks)
 E={}
 for name,b in (("Q1",b1),("H1",b2)):
  E[name+"_assets"]=sm(b,("cash_vault","deposits_sbv","interbank_assets","trading_securities","derivative_assets","customer_loans_net","investment_securities","long_term_investments","fixed_assets","other_assets"))-b["total_assets"]
  E[name+"_liabs"]=sm(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs","trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
  E[name+"_equity"]=sm(b,("capital","reserves","fx_equity","retained","minority"))-b["equity"]
  E[name+"_balance"]=b["total_assets"]-b["total_liabilities"]-b["equity"]
 for name,p in (("Q1",p1),("Q2",p2)):
  E[name+"_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
  E[name+"_service"]=p["services_income"]+p["services_expense"]-p["services_net"]
  E[name+"_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
  E[name+"_before_provision"]=sm(p,("net_interest","services_net","fx_net","trading_net","investment_net","other_net","dividends"))-p["opex"]-p["before_provision"]
  E[name+"_pbt"]=p["before_provision"]-p["provision"]-p["pbt"]
  E[name+"_tax"]=p["tax_current"]+p["tax_deferred"]-p["tax"]
  E[name+"_pat"]=p["pbt"]-p["tax"]-p["pat"]
  E[name+"_parent"]=p["pat"]-p["minority_pat"]-p["parent_pat"]
 E["Q1_preWC"]=sm(c1,("interest_cash","interest_cash_paid","services_cash","other_trading_cash","other_cash","bad_debt_recovery","staff_admin_cash","taxes_paid"))-c1["pre_wc"]
 E["Q1_CFO"]=c1["pre_wc"]+c1["working_assets"]+c1["working_liabs"]-c1["cfo"]
 E["Q1_CFI"]=sm(c1,("capex","asset_disposal","asset_disposal_cost","dividend_investments"))-c1["cfi"]
 E["Q1_net"]=c1["cfo"]+c1["cfi"]+c1["cff"]-c1["net"]
 E["Q1_FX"]=c1["opening"]+c1["net"]+c1["fx"]-c1["closing"]
 E["H1_CFO"]=h["pre_wc"]+h["working_assets"]+h["working_liabs"]-h["cfo"]
 E["H1_net"]=h["cfo"]+h["cfi"]+h["cff"]-h["net"]
 E["H1_FX"]=h["opening"]+h["net"]+h["fx"]-h["closing"]
 E["Q2_net"]=q["cfo"]+q["cfi"]+q["cff"]-q["net"]
 E["Q2_FX"]=q["opening"]+q["net"]+q["fx"]-q["closing"]
 for k in ("cfo","cfi","cff","net","fx"):E["Q2_delta_"+k]=h[k]-c1[k]-q[k]
 assert len(E)==39 and all(v==0 for v in E.values()),E
 assert a["source_exact_residuals"]==E
 assert (b1["total_assets"],b1["total_liabilities"],b1["equity"])==(2924176928,2735484770,188692158)
 assert (b2["total_assets"],b2["total_liabilities"],b2["equity"])==(2962003670,2761789368,200214302)
 assert (p1["pbt"],p1["pat"],p2["pbt"],p2["pat"])==(11139360,8960041,14728745,11783490)
 assert (c1["cfo"],c1["cfi"],c1["cff"],c1["net"],c1["fx"],c1["opening"],c1["closing"])==(127479653,-315503,0,127164150,85384,451745475,578995009)
 assert (h["cfo"],h["cfi"],h["cff"],h["net"],h["fx"],h["closing"])==(91368142,-667411,0,90700731,-23535,542422671)
 assert (q["cfo"],q["cfi"],q["cff"],q["net"],q["fx"],q["opening"],q["closing"])==(-36111511,-351908,0,-36463419,-108919,578995009,542422671)
 assert prior["original_source_million_vnd"]["cfo_H1"]==h["cfo"]
 assert prior["original_source_million_vnd"]["open_H1"]==h["opening"]
 assert prior["original_source_million_vnd"]["close_H1"]==h["closing"]
 assert d["symbol"]=="CTG" and [x["period"] for x in d["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert all(d["items"][i]["verification_status"].startswith("issuer_signed_CTG") for i in range(7))
 assert [d["items"][i]["verification_status"] for i in (4,5)]==[S1,S2]
 assert d["items"][6]["source_validation"]["original_pdf_sha256"]=="0f1a77f5b3e799a6a67175a893727862ea094c8545c3250b2d36f6594b6e038e"
 for idx,b,p,c,y in ((4,b1,p1,c1,c1),(5,b2,p2,q,h)):
  row=d["items"][idx];v=row["source_validation"]
  assert v["Q1_original_pdf_hash_verified"] and v["Q1_original_pdf_sha256"]==s["Q1_sha256"]
  assert v["H1_original_pdf_sha256"]==H1_SHA
  assert v["all_source_balance_and_income_identities_exact"] and v["bank_B04_true_CFO_and_FX_cash_exact"]
  assert v["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
  mapped={"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["equity"],
   "revenue":p["before_provision"]+p["opex"],"pretax_profit":p["pbt"],"net_profit":p["pat"],
   "net_profit_attributable":p["parent_pat"],"bank_non_controlling_profit":p["minority_pat"],
   "operating_cash_flow":c["cfo"],"investing_cash_flow":c["cfi"],"financing_cash_flow":c["cff"],
   "net_cash_change":c["net"],"cashflow_fx":c["fx"],"cash_beginning":c["opening"],"cash_ending":c["closing"],
   "operating_cash_flow_ytd":y["cfo"],"investing_cash_flow_ytd":y["cfi"],
   "financing_cash_flow_ytd":y["cff"],"net_cash_change_ytd":y["net"],"cashflow_fx_ytd":y["fx"]}
  for k,val in mapped.items():assert row[k]==val,(row["period"],k,row.get(k),val)
  for name,obj in (("b02a",b),("b03a",p),("b04a_ytd",y)):
   for k,val in obj.items():assert row["signed_source_"+name+"_"+k]==val,(row["period"],name,k)
  assert row["eps"] is None and row["unit"]=="triệu VND"
 assert d["items"][4]["roa"]==1.26 and d["items"][4]["roe"]==19.37
 assert d["items"][5]["roa"]==1.6 and d["items"][5]["roe"]==24.15
 assert all(x["period"]>="2025-Q1" for x in d["items"])
 return len(E)
def main():
 a=json.loads(LEDGER.read_text("utf8"));o=json.loads(OLDQ3.read_text("utf8"));d=json.loads(DATA.read_text("utf8"))
 n=check(a,o,d)
 cases=["source_sha","H1_sha","source_sum","Q1_assets","Q2_assets","Q1_liabs","Q2_liabs","Q1_PBT","Q2_PAT","Q1_CFO","Q1_preWC_confusion","Q1_CFI","Q1_FX","Q1_cash",
 "H1_CFO","H1_FX","H1_cash","Q2_CFO","Q2_CFI","Q2_CFF","Q2_FX","Q2_cash","Q2_preWC_confusion",
 "Q1_EPS","Q2_EPS","2025_locked","Q3_locked","2024_period","falsified_original_hash","missing_source_review"]
 for case in cases:
  aa,oo,dd=copy.deepcopy(a),copy.deepcopy(o),copy.deepcopy(d)
  bb,pp,cc=(aa["Q1"][k] for k in ("B02","B03","B04"))
  b2,p2=aa["Q2"]["B02"],aa["Q2"]["B03"];h=aa["H1"]["B04"];q=aa["Q2_standalone_cash_H1_minus_Q1"]
  r1,r2=dd["items"][4],dd["items"][5]
  if case=="source_sha":aa["source"]["Q1_sha256"]="0"*64
  elif case=="H1_sha":aa["source"]["H1_sha256"]="0"*64
  elif case=="source_sum":aa["source_exact_residuals"]["Q1_CFO"]=1
  elif case=="Q1_assets":bb["total_assets"]+=1
  elif case=="Q2_assets":b2["total_assets"]+=1
  elif case=="Q1_liabs":bb["total_liabilities"]+=1
  elif case=="Q2_liabs":b2["total_liabilities"]+=1
  elif case=="Q1_PBT":pp["pbt"]+=1
  elif case=="Q2_PAT":p2["pat"]+=1
  elif case=="Q1_CFO":r1["operating_cash_flow"]+=1
  elif case=="Q1_preWC_confusion":r1["operating_cash_flow"]=cc["pre_wc"]
  elif case=="Q1_CFI":cc["cfi"]+=1
  elif case=="Q1_FX":cc["fx"]+=1
  elif case=="Q1_cash":r1["cash_ending"]+=1
  elif case=="H1_CFO":h["cfo"]+=1
  elif case=="H1_FX":h["fx"]+=1
  elif case=="H1_cash":h["closing"]+=1
  elif case=="Q2_CFO":r2["operating_cash_flow"]+=1
  elif case=="Q2_CFI":q["cfi"]+=1
  elif case=="Q2_CFF":q["cff"]+=1
  elif case=="Q2_FX":q["fx"]+=1
  elif case=="Q2_cash":r2["cash_ending"]+=1
  elif case=="Q2_preWC_confusion":r2["operating_cash_flow"]=h["pre_wc"]
  elif case=="Q1_EPS":r1["eps"]=999
  elif case=="Q2_EPS":r2["eps"]=999
  elif case=="2025_locked":dd["items"][0]["verification_status"]="pending"
  elif case=="Q3_locked":dd["items"][6]["verification_status"]="pending"
  elif case=="2024_period":dd["items"].append({"period":"2024-Q4"})
  elif case=="falsified_original_hash":r1["source_validation"]["Q1_original_pdf_sha256"]="0"*64
  elif case=="missing_source_review":r2["source_validation"]["Q1_original_pdf_hash_verified"]=False
  try:check(aa,oo,dd)
  except (AssertionError,TypeError,IndexError,KeyError):pass
  else:raise AssertionError("CTG source tamper escaped: "+case)
 print(f"PASS CTG signed 2026Q1 and H1-minus-Q1 2026Q2: {n} zero source identities, {len(cases)} negative tamper guards; all seven CTG periods issuer signed")
 print("PASS CTG Q1 CFO +127,479,653, Q2 CFO -36,111,511, H1 +91,368,142, FX-aware cash 578,995,009 / 542,422,671")
if __name__=="__main__":main()
