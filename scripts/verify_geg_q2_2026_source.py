#!/usr/bin/env python3
"""Validate GEG Q2/2026 consolidated B01/B02 and 6M B03 from signed original scan.

Issuer scan obtained from Vietstock mirror; original page images 4-8 manually
reviewed, GitHub Actions run 44520387543 artifact 14526818741. Do not
derive standalone Q2 B03 before Q1 source same scope is verified.
"""
import json
from decimal import Decimal
from pathlib import Path
doc=json.loads((Path(__file__).resolve().parents[1]/"data/financials-GEG.json").read_text("utf-8"))
q=[r for r in doc["items"] if r["period"]=="2026-Q2" and "hợp nhất" in r.get("report_type","").lower()]
assert len(q)==1,q
r=q[0]
def v(k):return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
def s(*keys):return sum(v(k) for k in keys)
assert r["unit"]=="triệu VND"
assert r["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_h1_ytd_q2_standalone_cash_deferred"
assert r["cashflow_period_basis"]=="year_to_date"
assert r["source_validation"]["original_pdf_sha256"]=="e5c84e9cb42b1698481b12f426544cfad517894d46d3d0f37a1e9e53575f00d5"
assert r["source_validation"]["original_pdf_bytes"]==2341291
assert r["source_validation"]["original_pdf_pages_total"]==43
assert r["source_validation"]["visually_reviewed_original_pdf_pages"]==[4,5,6,7,8]
assert r["source_validation"]["manually_visual_reviewed"] is True
assert len(r["financial_line_items_extracted_fields"])==101
assert set(r["financial_line_items_extracted_fields"])==set(r["financial_line_items_manually_verified_fields"])
assert r["eps"]==22 and r["diluted_eps"]==21
assert r["roa"] is None and r["roe"] is None
assert all(r.get(k) is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","capital_expenditure","dividends_paid","foreign_exchange_effect"))
anchors={
 "total_assets":15481663386076,"total_liabilities":8730633735292,"equity":6751029650784,
 "current_assets":1795327105425,"non_current_assets":13686336280651,
 "cash_and_equivalents":100327178533,"fixed_assets":12889071805876,
 "short_term_investments":399347389553,"short_term_receivables":1089342589419,
 "inventory":59335951480,"non_control_interest_equity":1570575747143,
 "revenue":580335207100,"cost_of_goods_sold":342819635918,
 "gross_profit":237515571182,"financial_income":5360349632,
 "financial_expense":183296067795,"interest_expense":183236981159,
 "admin_expense":41821936719,"share_of_profit_associates":904922295,
 "operating_profit":18662838595,"pretax_profit":18568717509,
 "income_tax_current":10500368887,"income_tax_deferred":-83657192,
 "income_tax":10416711695,"net_profit":8152005814,
 "net_profit_attributable":28179986219,"non_controlling_interest_profit":-20027980405,
 "revenue_ytd":1347714407034,"pretax_profit_ytd":304983996509,
 "net_profit_ytd":271805979210,
 "operating_cash_flow_ytd":722160976132,
 "investing_cash_flow_ytd":-732448267884,
 "financing_cash_flow_ytd":35658808670,
 "net_cash_change_ytd":25371516918,
 "foreign_exchange_effect_ytd":13217270,
 "cash_beginning_reported_ytd":74942444345,
 "cash_ending":100327178533,
 "capital_expenditure_ytd":-653270670725,
 "cf_share_issue_ytd":20000000,
 "cf_borrowing_proceeds_ytd":751518963283,
 "cf_borrowing_repayments_ytd":-710817288298,
 "cf_finance_lease_repayments_ytd":-4991802915,
 "dividends_paid_ytd":-71063400,
}
for key,exact in anchors.items():
    assert v(key)==exact,(key,v(key),exact)
C={
 "b01_assets_liabilities_equity":v("total_assets")-s("total_liabilities","equity"),
 "b01_assets_sections":v("total_assets")-s("current_assets","non_current_assets"),
 "b01_liabilities_sections":v("total_liabilities")-s("current_liabilities","long_term_liabilities"),
 "b01_current_assets":v("current_assets")-s("cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
 "b01_longterm_assets":v("non_current_assets")-s("long_term_receivables","fixed_assets","construction_in_progress","long_term_investments","other_noncurrent_assets"),
 "b01_cash":v("cash_and_equivalents")-s("cash_only","cash_equivalents_only"),
 "b01_equity_split":v("equity")-s("parent_equity","non_control_interest_equity"),
 "b01_parent_equity":v("parent_equity")-s("share_capital","additional_paid_in_capital","development_fund","retained_earnings"),
 "b02_gross":v("revenue")-v("cost_of_goods_sold")-v("gross_profit"),
 "b02_sales":v("sales_gross")-v("revenue"),
 "b02_operating":v("gross_profit")+v("financial_income")-v("financial_expense")-v("admin_expense")+v("share_of_profit_associates")-v("operating_profit"),
 "b02_other":v("other_income")-v("other_expense")-v("other_profit"),
 "b02_pretax":v("operating_profit")+v("other_profit")-v("pretax_profit"),
 "b02_tax":v("income_tax")-s("income_tax_current","income_tax_deferred"),
 "b02_net":v("pretax_profit")-v("income_tax")-v("net_profit"),
 "b02_owner_nci":v("net_profit")-s("net_profit_attributable","non_controlling_interest_profit"),
 "b02_halfyear_gross":v("revenue_ytd")-v("cost_of_goods_sold_ytd")-v("gross_profit_ytd"),
 "b02_halfyear_sales":v("sales_gross_ytd")-v("revenue_ytd"),
 "b02_halfyear_operating":v("gross_profit_ytd")+v("financial_income_ytd")-v("financial_expense_ytd")-v("admin_expense_ytd")+v("share_of_profit_associates_ytd")-v("operating_profit_ytd"),
 "b02_halfyear_other":v("other_income_ytd")-v("other_expense_ytd")-v("other_profit_ytd"),
 "b02_halfyear_pretax":v("operating_profit_ytd")+v("other_profit_ytd")-v("pretax_profit_ytd"),
 "b02_halfyear_tax":v("income_tax_ytd")-s("income_tax_current_ytd","income_tax_deferred_ytd"),
 "b02_halfyear_net":v("pretax_profit_ytd")-v("income_tax_ytd")-v("net_profit_ytd"),
 "b02_halfyear_owner_nci":v("net_profit_ytd")-s("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
 "b03_sections":v("net_cash_change_ytd")-s("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"),
 "b03_cash_bridge":v("cash_beginning_reported_ytd")+v("net_cash_change_ytd")+v("foreign_exchange_effect_ytd")-v("cash_ending"),
 "b03_to_b01_cash":v("cash_ending")-v("cash_and_equivalents"),
 "b03_investment":v("investing_cash_flow_ytd")-s("capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_loans_issued_ytd","cf_loans_recovered_ytd","cf_equity_investment_ytd","cf_interest_dividends_received_ytd"),
 "b03_financing":v("financing_cash_flow_ytd")-s("cf_share_issue_ytd","cf_borrowing_proceeds_ytd","cf_borrowing_repayments_ytd","cf_finance_lease_repayments_ytd","dividends_paid_ytd"),
 "b03_operating_adjustments":v("cf_cash_before_wc_ytd")-s("cf_pretax_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd"),
 "b03_cfo_components":v("operating_cash_flow_ytd")-s("cf_cash_before_wc_ytd","cf_receivables_change_ytd","cf_inventory_change_ytd","cf_payables_change_ytd","cf_prepaid_change_ytd","cf_interest_paid_ytd","cf_taxes_paid_ytd","cf_other_operating_paid_ytd"),
}
assert len(C)==31 and all(val==0 for val in C.values()),C
assert {k:str(val) for k,val in C.items()}==r["source_validation"]["statement_identity_residuals_vnd"]
assert r["financial_line_items_rejected_values"]["auto_eps_old_vnd"]==70
assert r["financial_line_items_rejected_values"]["auto_diluted_eps_old_vnd"]==-14956
assert v("dividends_paid_ytd")!=v("cf_finance_lease_repayments_ytd")
assert not any(x["period"] < "2025-Q1" for x in doc["items"])
print("PASS GEG consolidated Q2/2026: 101 source fields, 31 exact VND accounting identities, issuer-signed source PDF pages 4-8, EPS and dividend misreads quarantined, standalone Q2 cash withheld until Q1 verified")
