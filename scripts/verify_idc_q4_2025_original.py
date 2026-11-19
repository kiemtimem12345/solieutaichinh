#!/usr/bin/env python3
"""Verify issuer signed IDC 2025 Q4 consolidated B01/B02 & FY B03 at exact VND.

The audit FY2025 independent year-end cash source and original issuer Q4 agree
with Q1/2026 opening. H1/2026 version differs by 890,796,892 VND.
This test preserves original published source vintages and does not fabricate
standalone Q2/2026 cash flows; Q4/2025 derives from signed Q3/2025 original.
"""
import json
from decimal import Decimal
from pathlib import Path

data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-IDC.json").read_text("utf-8"))
rows={x["period"]:x for x in data["items"]}
q,a,h,z=(rows[k] for k in ("2025-Q4","2026-Q1","2026-Q2","2025-Q3"))
def V(obj,k):
    return int((Decimal(str(obj[k]))*Decimal(1000000)).to_integral_exact())
def S(obj,*keys):return sum(V(obj,k) for k in keys)

assert q["symbol"]=="IDC" and q["unit"]=="triệu VND"
assert q["report_type"].startswith("BCTC hợp nhất IDC Q4/2025")
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_fy_and_q4_standalone_cash"
assert q["cashflow_period_basis"]=="year_to_date"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["source_unit"]=="VND"
assert q["source_validation"]["normalized_unit"]=="triệu VND"
assert len(q["financial_line_items_extracted_fields"])==109
assert q["financial_line_items_extracted_fields"]==q["financial_line_items_manually_verified_fields"]
assert q["roa"] is None and q["roe"] is None
assert q["eps"]==1183 and q["diluted_eps"]==1183
assert all(q.get(k) is not None for k in (
    "operating_cash_flow","investing_cash_flow","financing_cash_flow",
    "net_cash_change","cash_beginning","capital_expenditure",
    "dividends_paid","foreign_exchange_effect"))

e=q["source_validation"]["audited_year_end_comparative"]
assert e["issuer_original_pdf_sha256"]=="1ca45cd909f038d6b5a54123280b2e92b9d7dab92c52ba3c85fac5f9b0483d5f"
assert e["issuer_original_pdf_bytes"]==17108337 and e["issuer_original_pdf_page_count"]==67
assert e["original_visual_review_pages"]==[8,9,10,11,12,13,14]
assert e["audited_fy_2025_annual_report_pdf_sha256"]=="8eae4129eef2e3ae88b4f9ff1559a6d4cb3fd03a7a893e9030439eac9055e25b"
assert e["audited_fy_2025_pdf_pages"]==138
assert e["standalone_q4_b03_deferred_until_2025Q3_original_9m"] is False
assert e["issuer_reclassification_note_unverified"] is True

original={
 "total_assets":23201490679523,"total_liabilities":14938459787767,"equity":8263030891756,
 "current_assets":9856822003191,"non_current_assets":13344668676332,
 "cash_and_equivalents":553052678239,"cash_only":78561249834,
 "cash_equivalents_only":474491428405,"short_term_investments":6807014517859,
 "short_term_receivables":1157155456553,"inventory":1298623568803,
 "other_current_assets":40975781737,"fixed_assets":2930540421499,
 "investment_property":2574138152669,"long_term_construction_in_progress":7094244324724,
 "long_term_financial_investments":210787245431,
 "current_liabilities":5620500395796,"long_term_liabilities":9317959391971,
 "non_controlling_interest_equity":1803656728358,
 "gross_revenue":2160206044440,"revenue_deductions":67932722,
 "revenue":2160138111718,"cost_of_goods_sold":1453163128638,
 "gross_profit":706974983080,"financial_income":108952409062,
 "financial_expense":42472227098,"interest_expense":43891490863,
 "selling_expense":18592495992,"admin_expense":92138853752,
 "profit_from_associates":180518355,"operating_profit":662904333655,
 "other_income":10212684319,"other_expense":13897429941,
 "other_profit":-3684745622,"pretax_profit":659219588033,
 "income_tax_current":142577559905,"income_tax_deferred":-23353093110,
 "income_tax":119224466795,"net_profit":539995121238,
 "net_profit_attributable":449103567116,
 "non_controlling_interest_profit":90891554122,
 "revenue_ytd":8588149771546,"cost_of_goods_sold_ytd":5528143612263,
 "gross_profit_ytd":3060006159283,"pretax_profit_ytd":2917745400503,
 "net_profit_ytd":2354081075050,
 "operating_cash_flow_ytd":3913940809873,
 "investing_cash_flow_ytd":-7009893958684,
 "financing_cash_flow_ytd":1460905190082,
 "net_cash_change_ytd":-1635047958729,
 "cash_beginning_reported_ytd":2188037806317,
 "foreign_exchange_effect_ytd":62830651,"cash_ending":553052678239,
 "capital_expenditure_ytd":-3103468210215,
 "dividends_paid_ytd":-1300232590297,
 "cf_operating_before_working_capital_ytd":3763669124939,
}
for k,expected in original.items():
    assert V(q,k)==expected,(k,V(q,k),expected)
assert V(q,"interest_expense")>V(q,"financial_expense"), "Issuer printed interest line, not an OCR transcription error"
checks={
 "balance":V(q,"total_assets")-S(q,"total_liabilities","equity"),
 "asset_classes":V(q,"total_assets")-S(q,"current_assets","non_current_assets"),
 "liab_classes":V(q,"total_liabilities")-S(q,"current_liabilities","long_term_liabilities"),
 "cash_components":V(q,"cash_and_equivalents")-S(q,"cash_only","cash_equivalents_only"),
 "current_asset_classes":V(q,"current_assets")-S(q,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
 "noncurrent_asset_classes":V(q,"non_current_assets")-S(q,"long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
 "equity_classes":V(q,"equity")-S(q,"share_capital","share_premium","other_owner_capital","asset_revaluation_difference","development_investment_fund","retained_earnings","non_controlling_interest_equity"),
 "revenue":V(q,"gross_revenue")-V(q,"revenue_deductions")-V(q,"revenue"),
 "gross_profit":V(q,"revenue")-V(q,"cost_of_goods_sold")-V(q,"gross_profit"),
 "operating_profit":V(q,"gross_profit")+V(q,"financial_income")-V(q,"financial_expense")+V(q,"profit_from_associates")-V(q,"selling_expense")-V(q,"admin_expense")-V(q,"operating_profit"),
 "other_profit":V(q,"other_income")-V(q,"other_expense")-V(q,"other_profit"),
 "pretax_profit":V(q,"operating_profit")+V(q,"other_profit")-V(q,"pretax_profit"),
 "tax":V(q,"income_tax")-S(q,"income_tax_current","income_tax_deferred"),
 "net_profit":V(q,"pretax_profit")-V(q,"income_tax")-V(q,"net_profit"),
 "profit_split":V(q,"net_profit")-S(q,"net_profit_attributable","non_controlling_interest_profit"),
 "fy_net_revenue":V(q,"gross_revenue_ytd")-V(q,"revenue_deductions_ytd")-V(q,"revenue_ytd"),
 "fy_gross_profit":V(q,"revenue_ytd")-V(q,"cost_of_goods_sold_ytd")-V(q,"gross_profit_ytd"),
 "fy_operating_profit":V(q,"gross_profit_ytd")+V(q,"financial_income_ytd")-V(q,"financial_expense_ytd")+V(q,"profit_from_associates_ytd")-V(q,"selling_expense_ytd")-V(q,"admin_expense_ytd")-V(q,"operating_profit_ytd"),
 "fy_other_profit":V(q,"other_income_ytd")-V(q,"other_expense_ytd")-V(q,"other_profit_ytd"),
 "fy_pretax_profit":V(q,"operating_profit_ytd")+V(q,"other_profit_ytd")-V(q,"pretax_profit_ytd"),
 "fy_net_profit":V(q,"pretax_profit_ytd")-V(q,"income_tax_ytd")-V(q,"net_profit_ytd"),
 "fy_parent_nci":V(q,"net_profit_ytd")-S(q,"net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
 "cf_sections":S(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-V(q,"net_cash_change_ytd"),
 "cf_cash_bridge":S(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-V(q,"cash_ending"),
 "cf_b01_cash":V(q,"cash_and_equivalents")-V(q,"cash_ending"),
 "cf_before_working_capital":S(q,"cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd")-V(q,"cf_operating_before_working_capital_ytd"),
 "cf_operating":S(q,"cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_payments_ytd")-V(q,"operating_cash_flow_ytd"),
 "cf_investing":S(q,"capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_interest_dividends_received_ytd")-V(q,"investing_cash_flow_ytd"),
 "cf_financing":S(q,"cf_share_issue_proceeds_ytd","cf_share_repurchase_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","dividends_paid_ytd")-V(q,"financing_cash_flow_ytd")
}
assert len(checks)==29 and all(x==0 for x in checks.values()),checks
assert checks.keys()==q["source_validation"]["statement_identity_residuals_vnd"].keys()
assert all(x=="0" for x in q["source_validation"]["statement_identity_residuals_vnd"].values())

assert int(e["audited_closing_cash_vnd"])==V(q,"cash_ending")
assert int(e["q4_issuer_closing_cash_vnd"])==V(q,"cash_ending")
assert int(e["q1_original_2026_opening_cash_vnd"])==V(a,"cash_beginning_reported_ytd")==V(q,"cash_ending")
assert int(e["h1_original_2026_opening_cash_vnd"])==V(h,"cash_beginning_reported_ytd")
assert V(h,"cash_beginning_reported_ytd")-V(q,"cash_ending")==890796892
assert e["q4_vs_audited_cash_residual_vnd"]=="0"
assert e["q1_vs_audited_cash_residual_vnd"]=="0"
assert e["h1_vs_audited_cash_residual_vnd"]=="890796892"
assert h["source_validation"]["audited_fy2025_cash_cross_vintage"]["quarterly_cashflow_still_deferred"] is True
assert all(h.get(k) is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","foreign_exchange_effect"))
assert q["financial_line_items_rejected_values"]["auto_operating_cash_flow_ytd_million_vnd"]==836453742
assert q["financial_line_items_rejected_values"]["auto_financing_cash_flow_ytd_million_vnd"]==371657217
assert q["source_validation"]["audited_year_end_comparative"]["issuer_reclassification_note_unverified"] is True
assert q["source_validation"]["standalone_q4_cashflow_status"]=="verified_FY2025_12M_minus_signed_IDC_Q3_9M_same_consolidated_scope"
assert q["source_validation"]["standalone_q4_source_9m_pdf_sha256"]=="80c1b3dcb2e5469d4fb84c3a0cbd46c51f664ce7e07a2a0946e10b691ca92ce3"
assert V(q,"operating_cash_flow")==970200007993
assert V(q,"investing_cash_flow")==-2329374796016
assert V(q,"financing_cash_flow")==1120543443747
assert V(q,"net_cash_change")==-238631344276
assert V(q,"foreign_exchange_effect")==-2537404
assert V(q,"capital_expenditure")==-1300428928495
assert V(q,"dividends_paid")==-654131953577
assert V(q,"cash_beginning")==791686559919
assert V(q,"cash_beginning")==V(z,"cash_ending")
assert V(q,"cash_beginning")+V(q,"net_cash_change")+V(q,"foreign_exchange_effect")==V(q,"cash_ending")
assert S(q,"operating_cash_flow","investing_cash_flow","financing_cash_flow")==V(q,"net_cash_change")
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure","dividends_paid"):
    assert V(q,k)==V(q,k+"_ytd")-V(z,k+"_ytd"),k
assert len(q["source_validation"]["standalone_q4_identity_residuals_vnd"])==5
assert all(int(x)==0 for x in q["source_validation"]["standalone_q4_identity_residuals_vnd"].values())
assert len(q["source_validation"]["q4_income_FY_minus_9M_residuals_vnd"])==9
assert all(int(x)==0 for x in q["source_validation"]["q4_income_FY_minus_9M_residuals_vnd"].values())
for k in ("revenue","gross_profit","cost_of_goods_sold","operating_profit","other_profit","pretax_profit","net_profit","net_profit_attributable","non_controlling_interest_profit"):
    assert V(q,k)==V(q,k+"_ytd")-V(z,k+"_ytd"),k
print("PASS IDC 2025 Q4 original 29 identities, 8 quarter-derived fields, 5 Q4 cash checks and 9 B02 crosschecks; H1 2026 remains quarantined")

