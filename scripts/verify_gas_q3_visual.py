#!/usr/bin/env python3
"""Verify GAS Q3 2025 scanned original issuer B01/B02/B03 by source identity.

B03 9M and H1 opening balance differ by 15,534,247 VND; do not silently
adjust the source. The quarterly cash bridge must carry that flag.
"""
import json
from decimal import Decimal
from pathlib import Path

data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-GAS.json").read_text("utf-8"))
rows={x["period"]:x for x in data["items"]}
a,h,q=rows["2025-Q1"],rows["2025-Q2"],rows["2025-Q3"]
v=lambda r,k: int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
checks=q["source_validation"]["statement_identity_residuals_vnd"]
assert len(checks)==21 and all(val=="0" for val in checks.values()),checks
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["reviewed_pages"]==[4,5,6,7]
assert q["source_validation"]["h1_vs_9m_beginning_cash_difference_vnd"]=="-15534247"
assert q["source_validation"]["q3_cash_bridge_discrepancy_vnd"]=="15534247"
assert q["source_validation"]["q3_cash_bridge_discrepancy_percent_of_closing"] < 0.01
assert q["unit"]=="triệu VND" and q["eps"]==1067
assert not isinstance(q.get("dividends_paid"),(float,int)), "Don't infer Q3 dividend from H1 missing mark"
assert v(q,"admin_expense")==525973477554
assert v(q,"cash_beginning_reported_ytd")==5567983431468
assert v(h,"cash_beginning_reported_ytd")==5567998965715
assert v(q,"net_profit")==2612819725552
assert v(q,"total_assets")==93864613349663
assert v(q,"revenue")==35690134900226
assert v(q,"operating_cash_flow_ytd")==12549166835674
assert v(q,"investing_cash_flow_ytd")==-5572856958369
assert v(q,"financing_cash_flow_ytd")==-904798734792
assert v(q,"total_assets")==v(q,"equity")+v(q,"total_liabilities")
assert v(q,"revenue")-v(q,"cost_of_goods_sold")==v(q,"gross_profit")
assert v(q,"pretax_profit")-v(q,"income_tax")==v(q,"net_profit")
assert v(q,"net_profit_attributable")+v(q,"non_controlling_interest_profit")==v(q,"net_profit")
assert v(q,"operating_cash_flow_ytd")+v(q,"investing_cash_flow_ytd")+v(q,"financing_cash_flow_ytd")==v(q,"net_cash_change_ytd")
assert v(q,"cash_beginning_reported_ytd")+v(q,"net_cash_change_ytd")+v(q,"foreign_exchange_effect_ytd")==v(q,"cash_ending")
assert v(a,"revenue")+v(h,"revenue")+v(q,"revenue")==91445984719394
assert v(a,"pretax_profit")+v(h,"pretax_profit")+v(q,"pretax_profit")==12616462294746
assert v(a,"net_profit")+v(h,"net_profit")+v(q,"net_profit")==10184201250527
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure"):
    assert v(q,k+"_ytd")-v(h,k+"_ytd")==v(q,k),k
assert v(q,"operating_cash_flow")+v(q,"investing_cash_flow")+v(q,"financing_cash_flow")==v(q,"net_cash_change")
assert v(h,"cash_ending")==v(q,"cash_beginning")
assert v(q,"cash_beginning")+v(q,"net_cash_change")+v(q,"foreign_exchange_effect")-v(q,"cash_ending")==15534247
verified=set(q.get("financial_line_items_manually_verified_fields") or [])
assert len(verified)==50 and verified==set(q["financial_line_items_extracted_fields"])
print("PASS: GAS Q3/2025 issuer-scanned PDF visual; 50 fields, 21 exact checks, quarter/YTD cash flow and flagged 15,534,247 VND opening variance")
