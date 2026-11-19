#!/usr/bin/env python3
"""GEG Q1/2026 signed 82-page consolidated B01/B02/B03 original exact-VND gate.

Q2/2026 H1 original cash opening differs from original Q1 cash opening by
11,422,218,903 VND; do not force a standalone Q2 cash bridge or overwrite
any signed original. Use Decimal to retain last-unit exactness.
"""
import json
from decimal import Decimal
from pathlib import Path
rows=json.loads((Path(__file__).resolve().parents[1]/"data/financials-GEG.json").read_text("utf-8"))["items"]
q=next(r for r in rows if r["period"]=="2026-Q1" and "hợp nhất" in r["report_type"].lower())
h=next(r for r in rows if r["period"]=="2026-Q2" and "hợp nhất" in r["report_type"].lower())
def v(r,k):
    return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
def s(r,*ks):
    return sum(v(r,k) for k in ks)
src=q["source_validation"]
assert q["unit"]=="triệu VND" and q["eps"]==577 and q["diluted_eps"]==550
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_q1_3m_with_cross_vintage_opening_cash_exception"
assert src["manually_visual_reviewed"] is True
assert src["original_pdf_sha256"]=="d8dade2f270452432a190bedddb46736523cc3a74b783ae1a2f82b76a5e74d5b"
assert src["original_pdf_bytes"]==4082692 and src["original_pdf_pages_total"]==82
assert src["visually_reviewed_original_pdf_pages"]==[6,7,8,9,10]
assert q["cashflow_period_basis"]=="year_to_date"
assert len(q["financial_line_items_extracted_fields"])==90
assert set(q["financial_line_items_extracted_fields"])==set(q["financial_line_items_manually_verified_fields"])
assert q["roa"] is None and q["roe"] is None
assert src["source_unit"]=="VND" and src["normalized_unit"]=="triệu VND"
assert src["comparable_q2_quarter_cash_flow_blocked"] is True
values={
"total_assets":15135066404510,"total_liabilities":8374006488064,"equity":6761059916446,
"current_assets":1954801640627,"non_current_assets":13180264763883,
"cash_and_equivalents":105856793049,"short_term_investments":310507676704,
"short_term_receivables":1419494957548,"inventory":53383397796,
"fixed_assets":12306921915949,"construction_in_progress":739628606009,
"current_liabilities":745118568386,"long_term_liabilities":7628887919678,
"parent_equity":5171058145686,"non_control_interest_equity":1590001770760,
"revenue":767379199934,"cost_of_goods_sold":280414635779,"gross_profit":486964564155,
"financial_income":3976415409,"financial_expense":165243270859,
"admin_expense":41100578261,"share_of_profit_associates":618707130,
"operating_profit":285215837574,"other_profit":1199441426,
"pretax_profit":286415279000,"income_tax_current":23323328690,
"income_tax_deferred":-562023086,"income_tax":22761305604,
"net_profit":263653973396,"net_profit_attributable":206675501563,
"non_controlling_interest_profit":56978471833,
"operating_cash_flow_ytd":213327143465,"investing_cash_flow_ytd":-26739175041,
"financing_cash_flow_ytd":-167121630611,"net_cash_change_ytd":19466337813,
"cash_beginning_reported_ytd":86364663248,"foreign_exchange_effect_ytd":25791988,
"cash_ending":105856793049,"capital_expenditure_ytd":-74740950292,
"cf_cash_before_wc_ytd":647013283761,
"cf_borrowing_proceeds_ytd":118768900472,
"cf_borrowing_repayments_ytd":-283300842033,
"cf_finance_lease_repayments_ytd":-2561189850,
"dividends_paid_ytd":-28499200,
}
for k,amount in values.items():
    assert v(q,k)==amount,(k,v(q,k),amount)
ident={
"b01_balance":v(q,"total_assets")-s(q,"total_liabilities","equity"),
"b01_assets_sections":v(q,"total_assets")-s(q,"current_assets","non_current_assets"),
"b01_debt_sections":v(q,"total_liabilities")-s(q,"current_liabilities","long_term_liabilities"),
"b01_current_assets":v(q,"current_assets")-s(q,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"b01_noncurrent_assets":v(q,"non_current_assets")-s(q,"long_term_receivables","fixed_assets","construction_in_progress","long_term_investments","other_noncurrent_assets"),
"b01_cash":v(q,"cash_and_equivalents")-s(q,"cash_only","cash_equivalents_only"),
"b01_equity_split":v(q,"equity")-s(q,"parent_equity","non_control_interest_equity"),
"b01_parent_equity":v(q,"parent_equity")-s(q,"share_capital","additional_paid_in_capital","development_fund","retained_earnings"),
"b02_sales":v(q,"sales_gross")-v(q,"revenue"),
"b02_gross":v(q,"revenue")-v(q,"cost_of_goods_sold")-v(q,"gross_profit"),
"b02_operating":v(q,"gross_profit")+v(q,"financial_income")-v(q,"financial_expense")-v(q,"admin_expense")+v(q,"share_of_profit_associates")-v(q,"operating_profit"),
"b02_other":v(q,"other_income")-v(q,"other_expense")-v(q,"other_profit"),
"b02_pretax":v(q,"operating_profit")+v(q,"other_profit")-v(q,"pretax_profit"),
"b02_tax":v(q,"income_tax")-s(q,"income_tax_current","income_tax_deferred"),
"b02_net":v(q,"pretax_profit")-v(q,"income_tax")-v(q,"net_profit"),
"b02_owner_nci":v(q,"net_profit")-s(q,"net_profit_attributable","non_controlling_interest_profit"),
"b03_sections":v(q,"net_cash_change_ytd")-s(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"),
"b03_cash_bridge":v(q,"cash_beginning_reported_ytd")+v(q,"net_cash_change_ytd")+v(q,"foreign_exchange_effect_ytd")-v(q,"cash_ending"),
"b03_cash_equals_b01":v(q,"cash_ending")-v(q,"cash_and_equivalents"),
"b03_investing":v(q,"investing_cash_flow_ytd")-s(q,"capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_loans_issued_ytd","cf_loans_recovered_ytd","cf_equity_investment_ytd","cf_interest_dividends_received_ytd"),
"b03_financing":v(q,"financing_cash_flow_ytd")-s(q,"cf_share_issue_ytd","cf_borrowing_proceeds_ytd","cf_borrowing_repayments_ytd","cf_finance_lease_repayments_ytd","dividends_paid_ytd"),
"b03_adjustments":v(q,"cf_cash_before_wc_ytd")-s(q,"cf_pretax_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd"),
"b03_cfo":v(q,"operating_cash_flow_ytd")-s(q,"cf_cash_before_wc_ytd","cf_receivables_change_ytd","cf_inventory_change_ytd","cf_payables_change_ytd","cf_prepaid_change_ytd","cf_interest_paid_ytd","cf_taxes_paid_ytd","cf_other_operating_paid_ytd"),
}
assert len(ident)==23 and all(x==0 for x in ident.values()),ident
assert {k:str(x) for k,x in ident.items()}==src["statement_identity_residuals_vnd"]
assert q["financial_line_items_rejected_values"]["old_eps_basic_vnd"]==70
for field in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","capital_expenditure","dividends_paid","foreign_exchange_effect"):
    assert v(q,field)==v(q,field+"_ytd"),field
assert v(q,"cash_beginning")==v(q,"cash_beginning_reported_ytd")
assert v(h,"revenue_ytd")==v(q,"revenue")+v(h,"revenue")
assert v(h,"net_profit_ytd")==v(q,"net_profit")+v(h,"net_profit")
assert v(h,"net_profit_attributable_ytd")==v(q,"net_profit_attributable")+v(h,"net_profit_attributable")
opening_gap=v(q,"cash_beginning_reported_ytd")-v(h,"cash_beginning_reported_ytd")
assert opening_gap==11422218903
quarter_cash=v(h,"cash_ending")-v(q,"cash_ending")
quarter_net=v(h,"net_cash_change_ytd")-v(q,"net_cash_change_ytd")
quarter_fx=v(h,"foreign_exchange_effect_ytd")-v(q,"foreign_exchange_effect_ytd")
assert quarter_cash==-5529614516
assert quarter_net==5905179105 and quarter_fx==-12574718
assert quarter_cash-quarter_net-quarter_fx==-11422218903
assert h["source_validation"]["q2_cash_bridge_recomputed_residual_vnd"]=="-11422218903"
assert h["source_validation"]["q2_quarter_only_cash_flow_status"]=="blocked_cross_source_year_opening_cash_difference_11422218903_vnd"
for field in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","capital_expenditure"):
    assert h[field] is None, ("do not fabricate quarterly Q2",field)
assert h["source_validation"]["original_pdf_sha256"]=="e5c84e9cb42b1698481b12f426544cfad517894d46d3d0f37a1e9e53575f00d5"
print("PASS GEG signed issuer 2026Q1: 90 fields, 23 exact-VND B01 B02 B03 identities; H1 revenue/net matched; Q2 cash opening source-vintage gap 11,422,218,903 VND documented, Q2 standalone blocked")
