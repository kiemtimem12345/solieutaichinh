#!/usr/bin/env python3
"""PLX Q4 2025 two signed ORIGINAL vintages, source-exact VND comparison.

This intentionally DOES NOT mark standalone Q4 cashflow PASS: published
2026-01-29 Q4 differs materially from signed KPMG-audited FY 2025
2026-03-31. Checks separate signed source identities and both candidate Q4
quarter bridges; quarantines conflicting quarterly CFO/CFI/CFF, FX and
dividend until source-version reconciliation. Q3/Q2 PASS untouched.
"""
import json
from decimal import Decimal
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/"data/financials-PLX.json").read_text("utf-8"))
source=(root/"reports/source-audits/PLX-2025Q4-original-vs-audited-FY2025-exact-vnd.txt").read_text("utf-8")
parsed={}
scope=None
for line in source.splitlines():
    if line.startswith("# BEGIN "):
        scope=line.removeprefix("# BEGIN ").strip()
        parsed[scope]={}
        continue
    if line.startswith("# END "):
        scope=None
        continue
    if not line or line.startswith("#"):continue
    name,val=line.split()
    assert scope in parsed and name not in parsed[scope] and val.lstrip("-").isdigit(),line
    parsed[scope][name]=int(val)
assert set(parsed)=={"first_issued_Q4","audited_FY2025","signed_Q3_9M"}
a,b,c=parsed["first_issued_Q4"],parsed["audited_FY2025"],parsed["signed_Q3_9M"]
q=next(x for x in data["items"] if x["period"]=="2025-Q4" and "hợp nhất" in x["report_type"])
q3=next(x for x in data["items"] if x["period"]=="2025-Q3" and "hợp nhất" in x["report_type"])
parent=next(x for x in data["items"] if x["period"]=="2026-Q3" and x["source_validation"].get("scope")=="parent_company")
s=q["source_validation"]
assert q["verification_status"]=="signed_original_visual_verified_B01_B02_B03_12m_audited_FY_2025_vintage_conflict_quarter_cash_blocked"
assert s["manually_visual_reviewed"] is True
assert s["audited_vintage_has_material_conflicts"] is True and s["standalone_q4_cashflow_qa_pass"] is False
assert s["original_first_issued_signed_pdf_sha256"]=="35a0f637ffbb0ecf5161337f5289e5e2572dc5655ff865d2d5c8eca592187e61"
assert s["audited_FY2025_signed_pdf_sha256"]=="5570d8cdb64de8f7978f6ef0a753afd08311a08e0dceb7f10a85b90e744b1735"
assert (s["original_first_issued_signed_pdf_bytes"],s["original_first_issued_signed_pdf_pages"])==(13759900,31)
assert (s["audited_FY2025_signed_pdf_bytes"],s["audited_FY2025_signed_pdf_pages"])==(12190357,85)
assert s["original_first_issued_visually_reviewed_pages"]==[2,3,4,5,6,7]
assert s["audited_FY2025_visually_reviewed_pages"]==[6,7,8,9,10,11,12,13,14]
assert s["original_recovery_workflow_run"]==44684657529
assert s["original_recovery_artifact_id"]==14606265504
assert q["cashflow_period_basis"]=="quarterly_q4_vintage_reconciliation_pending"
assert q["cashflow_ytd_period_basis"]=="twelve_months"
assert q["unit"]=="triệu VND"
def million(k):
    x=Decimal(str(q[k]))*Decimal(1000000)
    assert x==x.to_integral_value(),(k,x)
    return int(x)
mapping={"total_assets":"B01_total_assets","current_assets":"B01_current_assets",
 "non_current_assets":"B01_noncurrent_assets","total_liabilities":"B01_total_liabilities",
 "current_liabilities":"B01_current_liabilities","long_term_liabilities":"B01_long_term_liabilities",
 "equity":"B01_equity","cash_and_equivalents":"B01_cash",
 "revenue":"B02_quarter_net_revenue","gross_revenue":"B02_quarter_gross_revenue",
 "revenue_deductions":"B02_quarter_deductions","cost_of_goods_sold":"B02_quarter_cogs",
 "gross_profit":"B02_quarter_gross_profit","operating_profit":"B02_quarter_operating_profit",
 "other_profit":"B02_quarter_other_profit","pretax_profit":"B02_quarter_pretax_profit",
 "income_tax_current":"B02_quarter_current_tax","income_tax_deferred":"B02_quarter_deferred_tax",
 "net_profit":"B02_quarter_net_profit","net_profit_attributable":"B02_quarter_parent_pat",
 "non_controlling_interest_profit":"B02_quarter_nci_pat",
 "revenue_ytd":"B02_year_net_revenue","net_profit_ytd":"B02_year_net_profit",
 "operating_cash_flow_ytd":"B03_year_cfo","investing_cash_flow_ytd":"B03_year_cfi",
 "financing_cash_flow_ytd":"B03_year_cff","net_cash_change_ytd":"B03_year_net",
 "foreign_exchange_effect_ytd":"B03_year_fx","cash_ending":"B03_year_end",
 "capital_expenditure_ytd":"B03_year_capex","dividends_paid_ytd":"B03_year_dividends_paid"}
assert len(mapping)==31 and len(q["financial_line_items_manually_verified_fields"])==31
for k,val in mapping.items():assert million(k)==a[val],(k,million(k),a[val])
assert q["eps"]==350 and q["eps_ytd"]==1681
checks={
 "q4_b01_assets":a["B01_total_assets"]-a["B01_current_assets"]-a["B01_noncurrent_assets"],
 "q4_b01_liab_equity":a["B01_total_assets"]-a["B01_total_liabilities"]-a["B01_equity"],
 "q4_b01_liab_split":a["B01_total_liabilities"]-a["B01_current_liabilities"]-a["B01_long_term_liabilities"],
 "q4_b02_revenue":a["B02_quarter_gross_revenue"]-a["B02_quarter_deductions"]-a["B02_quarter_net_revenue"],
 "q4_b02_gross_profit":a["B02_quarter_net_revenue"]-a["B02_quarter_cogs"]-a["B02_quarter_gross_profit"],
 "q4_b02_pretax":a["B02_quarter_operating_profit"]+a["B02_quarter_other_profit"]-a["B02_quarter_pretax_profit"],
 "q4_b02_pat":a["B02_quarter_pretax_profit"]-a["B02_quarter_current_tax"]-a["B02_quarter_deferred_tax"]-a["B02_quarter_net_profit"],
 "q4_b02_parent_NCI":a["B02_quarter_net_profit"]-a["B02_quarter_parent_pat"]-a["B02_quarter_nci_pat"],
 "q4_fy_reported_net":a["B03_year_cfo"]+a["B03_year_cfi"]+a["B03_year_cff"]-a["B03_year_net"],
 "q4_fy_reported_bridge":a["B03_year_begin"]+a["B03_year_net"]+a["B03_year_fx"]-a["B03_year_end"],
 "q4_fy_reported_cross_b01":a["B03_year_end"]-a["B01_cash"],
 "q4_fy_pat_9m_plus_Q4":a["B02_year_net_profit"]-a["B02_quarter_net_profit"]-c["B02_9m_net_profit"],
 "audited_b01_liab_equity":b["B01_total_assets"]-b["B01_total_liabilities"]-b["B01_equity"],
 "audited_b02_revenue":b["B02_year_gross_revenue"]-b["B02_year_deductions"]-b["B02_year_net_revenue"],
 "audited_b02_gross":b["B02_year_net_revenue"]-b["B02_year_cogs"]-b["B02_year_gross_profit"],
 "audited_b02_pretax":b["B02_year_operating_profit"]+b["B02_year_other_profit"]-b["B02_year_pretax_profit"],
 "audited_b02_pat":b["B02_year_pretax_profit"]-b["B02_year_current_tax"]-b["B02_year_deferred_tax"]-b["B02_year_net_profit"],
 "audited_B03_net":b["B03_year_cfo"]+b["B03_year_cfi"]+b["B03_year_cff"]-b["B03_year_net"],
 "audited_B03_bridge":b["B03_year_begin"]+b["B03_year_net"]+b["B03_year_fx"]-b["B03_year_end"],
 "audited_B03_B01":b["B03_year_end"]-b["B01_cash"],
}
def candidate(z):
    x={k:z["B03_year_"+k]-c["B03_9m_"+k] for k in ("cfo","cfi","cff","net","fx")}
    x["begin"]=c["B03_9m_end"]
    x["end"]=z["B03_year_end"]
    x["dividends"]=z["B03_year_dividends_paid"]-c["B03_9m_dividends"]
    return x
for key,z in (("q4_filed",a),("audited",b)):
    can=candidate(z)
    meta=s["original_Q4_as_filed_cashflow_candidate_VND"] if key=="q4_filed" else s["audited_FY2025_minus_signed_Q3_9M_cashflow_candidate_VND"]
    assert {k:str(v) for k,v in can.items()}==meta
    checks[key+"_q4_net"]=can["cfo"]+can["cfi"]+can["cff"]-can["net"]
    checks[key+"_q4_bridge"]=can["begin"]+can["net"]+can["fx"]-can["end"]
assert len(checks)==24,len(checks)
assert all(x==0 for x in checks.values()),{k:x for k,x in checks.items() if x}
deltas={
"assets":b["B01_total_assets"]-a["B01_total_assets"],
"liabilities":b["B01_total_liabilities"]-a["B01_total_liabilities"],
"equity":b["B01_equity"]-a["B01_equity"],
"CFO":b["B03_year_cfo"]-a["B03_year_cfo"],
"CFI":b["B03_year_cfi"]-a["B03_year_cfi"],
"CFF":b["B03_year_cff"]-a["B03_year_cff"],
"net_cash_change":b["B03_year_net"]-a["B03_year_net"],
"FX":b["B03_year_fx"]-a["B03_year_fx"],
"cash_ending":b["B03_year_end"]-a["B03_year_end"],
"net_profit_ytd":b["B02_year_net_profit"]-a["B02_year_net_profit"],
"revenue_ytd":b["B02_year_net_revenue"]-a["B02_year_net_revenue"],
}
assert {k:str(v) for k,v in deltas.items()}==s["annual_source_differences_vnd"]
assert deltas["cash_ending"]==-127355301578
assert deltas["assets"]==-261123285444
assert deltas["net_profit_ytd"]==-11333439242
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","cash_beginning","capital_expenditure","dividends_paid"):
    assert q.get(k) is None,k
assert candidate(a)["dividends"]==53608752723
assert candidate(b)["dividends"]==-146879152932
assert q3["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_reviewed_h1_q3cash_with_other_income_expense_and_dividend_vintage_exceptions"
assert parent["source_validation"]["b03_cashflow_discrepancy_vnd"]=="87654015000"
print("PASS: PLX Q4 original signed 31p and FY audited signed 85p: 31 exact VND first-issued fields, 24 zero-VND source/cash identities, material audited FY vintage conflict isolated; Q4 quarterly cash withheld, Q3 PASS and parent Q3-2026 issuer CFF issue unchanged.")
