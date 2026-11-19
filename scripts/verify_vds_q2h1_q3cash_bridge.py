#!/usr/bin/env python3
"""Exact VND VDS consolidated Q2/2026 six-month B03 and Q3 9M-minus-H1 cash bridge.

Original VDSC signed Q2 2026 PDF pages 14-16; Q3 2026 PDF pages 14-16.
Q2 B01/B02 and H1 B03 are verified; Q2 standalone B03 from issuer-verified Q1.
"""
import json
from decimal import Decimal
from pathlib import Path

data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-VDS.json").read_text("utf-8"))
rows={q["period"]:q for q in data["items"]}
h,n=rows["2026-Q2"],rows["2026-Q3"]
def v(x,k):
    return int((Decimal(str(x[k]))*Decimal(1000000)).to_integral_exact())
def s(x,*keys):
    return sum(v(x,k) for k in keys)

h1expected={
    "operating_cash_flow_ytd":-2620903680,
    "investing_cash_flow_ytd":-90786936920,
    "financing_cash_flow_ytd":-101950000000,
    "net_cash_change_ytd":-195357840600,
    "cash_beginning_reported_ytd":996975599252,
    "cash_ending":801617758652,
    "cash_and_equivalents":801617758652,
    "capital_expenditure_ytd":-1058807300,
    "investing_asset_disposal_proceeds_ytd":45454,
    "investing_capital_contributions_ytd":-309870000000,
    "investing_recovery_of_capital_ytd":204684043970,
    "investing_dividends_received_ytd":15457780956,
    "financing_borrowing_proceeds_ytd":4555320000000,
    "financing_debt_repayments_ytd":-4657270000000,
}
for k,x in h1expected.items():
    assert v(h,k)==x,(k,v(h,k),x)
assert h["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_and_q2_standalone_cash"
assert h["source_validation"]["b03_h1_issuer_original_visual_verified"] is True
assert h["source_validation"]["manually_visual_reviewed"] is True, "B01/B02 and B03 all source visually verified"
assert h["source_validation"]["b03_original_report_pdf_pages"]==[14,15,16]
assert all(h.get(k) is not None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","foreign_exchange_effect"))
assert v(h,"foreign_exchange_effect_ytd")==0
prior=h["financial_line_items_prior_values"]["prior_auto_extracted_b03_before_issuer_visual_review_20261119"]
assert prior["operating_cash_flow_ytd"]==6677 and prior["foreign_exchange_effect_ytd"]==801618
assert h["financial_line_items_rejected_values"]["stale_auto_extracted_cfo_ytd_million_vnd"]==6677

c2={
 "q2_b03_net":v(h,"net_cash_change_ytd")-s(h,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"),
 "q2_b03_bridge":v(h,"cash_ending")-s(h,"cash_beginning_reported_ytd","net_cash_change_ytd"),
 "q2_b03_cfi":v(h,"investing_cash_flow_ytd")-s(h,"capital_expenditure_ytd","investing_asset_disposal_proceeds_ytd","investing_capital_contributions_ytd","investing_recovery_of_capital_ytd","investing_dividends_received_ytd"),
 "q2_b03_cff":v(h,"financing_cash_flow_ytd")-s(h,"financing_borrowing_proceeds_ytd","financing_debt_repayments_ytd"),
 "q2_b01_cash":v(h,"cash_and_equivalents")-v(h,"cash_ending")
}
assert len(c2)==5 and all(n==0 for n in c2.values()),c2
assert all(str(val)=="0" for val in h["source_validation"]["b03_exact_identity_residuals_vnd"].values())
assert set(c2)==set(h["source_validation"]["b03_exact_identity_residuals_vnd"])

expectedQ3={
 "operating_cash_flow":286822520794,
 "investing_cash_flow":1586289356,
 "financing_cash_flow":-218500000000,
 "net_cash_change":69908810150,
 "capital_expenditure":-458910000,
 "cash_beginning":801617758652,
}
assert n["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_q3_standalone_cash"
assert n["q3_standalone_cashflow_status"]=="original_9m_minus_issuer_verified_h1_6m_same_consolidated_scope"
source=n["source_validation"]
assert source["q3_standalone_cash_flow_source_q2_pdf_url"]==h["source_url"]
assert len(n["financial_line_items_extracted_fields"])==96
for k,x in expectedQ3.items():
    assert v(n,k)==x,(k,v(n,k),x)
    assert int(source["q3_standalone_cash_flow_derived_values_vnd"][k])==x
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","capital_expenditure"):
    assert v(n,k)==v(n,k+"_ytd")-v(h,k+"_ytd"),k
checks={
 "q3_b03_cash_sections":v(n,"net_cash_change")-s(n,"operating_cash_flow","investing_cash_flow","financing_cash_flow"),
 "q3_b03_bridge":v(n,"cash_beginning")+v(n,"net_cash_change")-v(n,"cash_ending"),
 "q3_b03_capex":v(n,"capital_expenditure")-(v(n,"capital_expenditure_ytd")-v(h,"capital_expenditure_ytd"))
}
assert all(value==0 for value in checks.values()),checks
assert all(value=="0" for value in source["q3_standalone_cash_flow_identity_residuals_vnd"].values())
assert set(checks)==set(source["q3_standalone_cash_flow_identity_residuals_vnd"])
assert v(n,"cash_beginning")==v(h,"cash_ending")
assert v(n,"client_brokerage_cash_ending_ytd") != v(n,"cash_ending")
assert v(h,"operating_cash_flow")==-251044721598
assert v(h,"investing_cash_flow")==179751455631
assert v(h,"financing_cash_flow")==14750000000
assert v(h,"net_cash_change")==-56543265967
assert v(h,"cash_beginning")==858161024619
assert v(h,"cash_beginning")+v(h,"net_cash_change")==v(h,"cash_ending")
assert h["source_validation"]["q2_standalone_from_q1_ytd_issuer_verified"] is True
print("PASS: VDS issuer-original H1 B03 5 exact VND checks; Q3 9M-minus-H1 standalone CFO/CFI/CFF 3 exact checks, auto parser CFO/FX corruption quarantined")
