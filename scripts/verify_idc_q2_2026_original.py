#!/usr/bin/env python3
"""Issuer-original IDC consolidated Q2/2026 B01 B02 6M B03, exact VND.

Signed HNX PDF 30 July 2026 (67 pages), visual source page 8-14. The
original 6M report is same-scope basis for 9M-minus-6M Q3 standalone cash.
"""
import json
from decimal import Decimal
from pathlib import Path

data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-IDC.json").read_text("utf-8"))
rows={x["period"]:x for x in data["items"]}
h,q=rows["2026-Q2"],rows["2026-Q3"]
def v(x,k):
    return int((Decimal(str(x[k]))*Decimal(1000000)).to_integral_exact())
def s(x,*ks):
    return sum(v(x,k) for k in ks)

assert h["symbol"]=="IDC" and h["unit"]=="triệu VND"
assert h["roa"] is None and h["roe"] is None
assert h["eps"]==h["diluted_eps"]==1461 and h["eps_ytd"]==2109
assert h["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_6m_ytd_q2_cash_deferred"
assert h["cashflow_period_basis"]=="year_to_date"
assert h["source_validation"]["manually_visual_reviewed"] is True
assert h["source_validation"]["issuer_pdf_sha256"]=="f0bee9c4554b166380098034650b09c0e45f85da55fd016086f0ef08a596354c"
assert h["source_validation"]["issuer_pdf_zip_sha256"]=="5e5637e71fa303a7968f306b645e95fa391b633126a4aff83fcabeeb412220c6"
assert h["source_validation"]["reviewed_pdf_pages"]==[8,9,10,11,12,13,14]
assert h["source_validation"]["original_pdf_in_zip"].endswith("_vi_baocaotaichinhhn_q2_2026_s.pdf")
assert len(h["financial_line_items_extracted_fields"])==105
assert set(h["financial_line_items_extracted_fields"])==set(h["financial_line_items_manually_verified_fields"])
assert all(h.get(k) is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","foreign_exchange_effect","capital_expenditure","dividends_paid"))
assert h["source_validation"]["legacy_roa_roe_unverified_reset_to_null"] is True

EXPECTED={
 "total_assets":23546025947580,"current_assets":16424882607866,
 "non_current_assets":7121143339714,"total_liabilities":14715877209906,
 "current_liabilities":5609121115090,"long_term_liabilities":9106756094816,
 "equity":8830148737674,"cash_and_equivalents":608684579632,
 "cash_only":176705080732,"cash_equivalents_only":431979498900,
 "short_term_investments":6612747709157,"short_term_receivables":1398487922279,
 "inventory":7737431153217,"fixed_assets":2828137956093,
 "non_controlling_interest_equity":2067621925587,
 "gross_revenue":2270556204685,"revenue_deductions":66825128,
 "revenue":2270489379557,"cost_of_goods_sold":1421483331885,
 "gross_profit":849006047672,"financial_income":144735815482,
 "financial_expense":56657259572,"selling_expense":22117041607,
 "admin_expense":67646607403,"operating_profit":847739958774,
 "pretax_profit":832935368526,"income_tax_current":179411251901,
 "income_tax_deferred":-9809689654,"net_profit":663333806279,
 "net_profit_attributable":609810412292,
 "non_controlling_interest_profit":53523393987,
 "revenue_ytd":3756014019978,"cost_of_goods_sold_ytd":2518269331398,
 "pretax_profit_ytd":1253232495504,"net_profit_ytd":1001240987338,
 "net_profit_attributable_ytd":880406329931,
 "operating_cash_flow_ytd":-5019037910,
 "investing_cash_flow_ytd":412225133057,
 "financing_cash_flow_ytd":-352471108238,
 "net_cash_change_ytd":54734986909,
 "cash_beginning_reported_ytd":553943475131,
 "foreign_exchange_effect_ytd":6117592,"cash_ending":608684579632,
 "capital_expenditure_ytd":-158418483835,
 "dividends_paid_ytd":-74115054425
}
for k,vnd in EXPECTED.items():
    assert v(h,k)==vnd,(k,v(h,k),vnd)

checks={
"balance":v(h,"total_assets")-s(h,"total_liabilities","equity"),
"assets_classes":v(h,"total_assets")-s(h,"current_assets","non_current_assets"),
"debt_classes":v(h,"total_liabilities")-s(h,"current_liabilities","long_term_liabilities"),
"cash_split":v(h,"cash_and_equivalents")-s(h,"cash_only","cash_equivalents_only"),
"current_asset_classes":v(h,"current_assets")-s(h,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"noncurrent_asset_classes":v(h,"non_current_assets")-s(h,"long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
"equity_classes":v(h,"equity")-s(h,"share_capital","share_premium","other_owner_capital","asset_revaluation_difference","development_investment_fund","retained_earnings","non_controlling_interest_equity"),
"net_revenue":v(h,"gross_revenue")-v(h,"revenue_deductions")-v(h,"revenue"),
"gross_profit":v(h,"revenue")-v(h,"cost_of_goods_sold")-v(h,"gross_profit"),
"operating_profit":v(h,"gross_profit")+v(h,"financial_income")-v(h,"financial_expense")-v(h,"selling_expense")-v(h,"admin_expense")+v(h,"profit_from_associates")-v(h,"operating_profit"),
"other_profit":v(h,"other_income")-v(h,"other_expense")-v(h,"other_profit"),
"pretax_profit":v(h,"operating_profit")+v(h,"other_profit")-v(h,"pretax_profit"),
"tax_components":v(h,"income_tax")-s(h,"income_tax_current","income_tax_deferred"),
"net_profit":v(h,"pretax_profit")-v(h,"income_tax")-v(h,"net_profit"),
"net_parent_nci":v(h,"net_profit")-s(h,"net_profit_attributable","non_controlling_interest_profit"),
"net_revenue_ytd":v(h,"gross_revenue_ytd")-v(h,"revenue_deductions_ytd")-v(h,"revenue_ytd"),
"gross_profit_ytd":v(h,"revenue_ytd")-v(h,"cost_of_goods_sold_ytd")-v(h,"gross_profit_ytd"),
"operating_profit_ytd":v(h,"gross_profit_ytd")+v(h,"financial_income_ytd")-v(h,"financial_expense_ytd")-v(h,"selling_expense_ytd")-v(h,"admin_expense_ytd")+v(h,"profit_from_associates_ytd")-v(h,"operating_profit_ytd"),
"other_profit_ytd":v(h,"other_income_ytd")-v(h,"other_expense_ytd")-v(h,"other_profit_ytd"),
"pretax_profit_ytd":v(h,"operating_profit_ytd")+v(h,"other_profit_ytd")-v(h,"pretax_profit_ytd"),
"net_profit_ytd":v(h,"pretax_profit_ytd")-v(h,"income_tax_ytd")-v(h,"net_profit_ytd"),
"net_parent_nci_ytd":v(h,"net_profit_ytd")-s(h,"net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
"cash_flow_6m_sections":s(h,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v(h,"net_cash_change_ytd"),
"cash_flow_6m_open_fx_close":s(h,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v(h,"cash_ending"),
"b01_b03_cash":v(h,"cash_and_equivalents")-v(h,"cash_ending"),
"cash_operating_before_wc":s(h,"cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd")-v(h,"cf_operating_before_working_capital_ytd"),
"cash_operating":s(h,"cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_payments_ytd")-v(h,"operating_cash_flow_ytd"),
"cash_investing":s(h,"capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_interest_dividends_received_ytd")-v(h,"investing_cash_flow_ytd"),
"cash_financing":s(h,"cf_share_issue_proceeds_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","dividends_paid_ytd")-v(h,"financing_cash_flow_ytd")
}
assert len(checks)==29
assert all(x==0 for x in checks.values()),checks
assert set(checks)==set(h["source_validation"]["statement_identity_residuals_vnd"])
assert all(val=="0" for val in h["source_validation"]["statement_identity_residuals_vnd"].values())

quarter={
 "operating_cash_flow":216619259342,
 "investing_cash_flow":93759529850,
 "financing_cash_flow":-449106095224,
 "net_cash_change":-138727306032,
 "foreign_exchange_effect":-23254979,
 "capital_expenditure":-198696957995,
 "dividends_paid":-636417638950,
 "cash_beginning":608684579632
}
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_q3_standalone_cash"
assert q["q3_standalone_cashflow_status"]=="verified_9m_minus_signed_6m_h1_same_consolidated_scope"
assert len(q["financial_line_items_extracted_fields"])==113
for k,rawvnd in quarter.items():
    assert v(q,k)==rawvnd,(k,v(q,k),rawvnd)
    assert int(q["source_validation"]["q3_standalone_cashflow_derived_vnd"][k])==rawvnd
    if k!="cash_beginning":
        assert v(q,k)==v(q,k+"_ytd")-v(h,k+"_ytd"),k
assert v(q,"cash_beginning")==v(h,"cash_ending")
assert v(q,"cash_beginning")+v(q,"net_cash_change")+v(q,"foreign_exchange_effect")==v(q,"cash_ending")
assert v(q,"operating_cash_flow")+v(q,"investing_cash_flow")+v(q,"financing_cash_flow")==v(q,"net_cash_change")
assert v(q,"cash_ending")==v(q,"cash_and_equivalents")
assert all(val=="0" for val in q["source_validation"]["q3_standalone_cashflow_source_checks_vnd"].values())
print("PASS IDC 2026 Q2 issuer-original B01/B02/H1 B03: 105 source fields, 29 exact-VND checks, Q3 9M less verified H1 standalone CFO/CFI/CFF with 4 exact quarterly checks")
