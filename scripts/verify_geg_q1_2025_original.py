#!/usr/bin/env python3
"""Issuer original GEG 2025 Q1 (83-page signed consolidated PDF) exact VND regression.

Checks all B01/B02/3M B03 statement identities, Q1+Q2 equal reported H1,
and independently derives Q2 standalone CFO/CFI/CFF/FX/cash with exact VND.
"""
import json
from decimal import Decimal
from pathlib import Path
doc=json.loads((Path(__file__).resolve().parents[1]/"data"/"financials-GEG.json").read_text("utf-8"))
rows={q["period"]:q for q in doc["items"] if "hợp nhất" in q.get("report_type","").lower()}
q,h=rows["2025-Q1"],rows["2025-Q2"]
def v(r,k):
    return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
def s(r,*keys):return sum(v(r,k) for k in keys)

assert q["unit"]=="triệu VND" and q["eps"]==1056 and q["diluted_eps"]==1056
assert q["verification_status"]=="issuer_signed_original_visual_verified_B01_B02_B03_Q1_and_3m"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["original_pdf_total_pages"]==83
assert q["source_validation"]["original_visual_page_numbers"]==[7,8,9,10,11]
assert q["source_validation"]["signed_report_date"]=="2025-04-28"
assert q["source_validation"]["original_pdf_sha256"]=="not_computed_source_url_and_images_verified"
assert q["roa"] is None and q["roe"] is None
assert len(q["financial_line_items_extracted_fields"])==104
assert q["financial_line_items_extracted_fields"]==q["financial_line_items_manually_verified_fields"]
assert q["source_url"]=="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/GEG_Baocaotaichinh_Q1_2025_Hopnhat.pdf"
expected={
"total_assets":15707017796798,"total_liabilities":9329804140173,
"equity":6377213656625,"current_assets":1895627338896,
"non_current_assets":13811390457902,"current_liabilities":829890405609,
"long_term_liabilities":8499913734564,"parent_equity":4809647975997,
"non_control_interest_equity":1567565680628,"cash_and_equivalents":175400032558,
"cash_only":90585243252,"cash_equivalents_only":84814789306,
"short_term_investments":233000000000,"short_term_receivables":1324423442385,
"inventory":116979271799,"other_current_assets":45824592154,
"long_term_receivables":232851726241,"fixed_assets":13096704851102,
"construction_in_progress":269441051893,"long_term_investments":176968177125,
"other_non_current_assets":35424651541,"revenue":1112755859981,
"cost_of_goods_sold":286668495975,"gross_profit":826087364006,
"financial_income":7837526270,"financial_expense":187421671779,
"share_of_profit_in_associates":3450715502,"admin_expense":44874042418,
"operating_profit":605079891581,"other_profit":214843849,
"pretax_profit":605294735430,"income_tax_current":30035228409,
"income_tax_deferred":-37686501526,"income_tax":-7651273117,
"net_profit":612946008547,"net_profit_attributable":378240835561,
"non_controlling_interest_profit":234705172986,
"operating_cash_flow_ytd":62310535515,
"investing_cash_flow_ytd":76527759434,
"financing_cash_flow_ytd":-127159459528,
"net_cash_change_ytd":11678835421,
"cash_beginning_reported_ytd":163717707072,
"foreign_exchange_effect_ytd":3490065,
"cash_ending":175400032558,
"capital_expenditure_ytd":-1199715023,
"dividends_paid_ytd":-221374400,
}
for k,amount in expected.items():assert v(q,k)==amount,(k,v(q,k),amount)
checks={
"b01_assets":v(q,"total_assets")-s(q,"current_assets","non_current_assets"),
"b01_balance":v(q,"total_assets")-s(q,"total_liabilities","equity"),
"b01_liabilities":v(q,"total_liabilities")-s(q,"current_liabilities","long_term_liabilities"),
"b01_owner_equity":v(q,"equity")-s(q,"parent_equity","non_control_interest_equity"),
"b01_current_assets":v(q,"current_assets")-s(q,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"b01_noncurrent_assets":v(q,"non_current_assets")-s(q,"long_term_receivables","fixed_assets","construction_in_progress","long_term_investments","other_non_current_assets"),
"b01_cash":v(q,"cash_and_equivalents")-s(q,"cash_only","cash_equivalents_only"),
"b02_gross":v(q,"revenue")-v(q,"cost_of_goods_sold")-v(q,"gross_profit"),
"b02_operating":v(q,"gross_profit")+v(q,"financial_income")-v(q,"financial_expense")+v(q,"share_of_profit_in_associates")-v(q,"selling_expense")-v(q,"admin_expense")-v(q,"operating_profit"),
"b02_other":v(q,"other_income")-v(q,"other_expense")-v(q,"other_profit"),
"b02_pretax":v(q,"operating_profit")+v(q,"other_profit")-v(q,"pretax_profit"),
"b02_tax":v(q,"income_tax_current")+v(q,"income_tax_deferred")-v(q,"income_tax"),
"b02_net":v(q,"pretax_profit")-v(q,"income_tax")-v(q,"net_profit"),
"b02_nci":v(q,"net_profit_attributable")+v(q,"non_controlling_interest_profit")-v(q,"net_profit"),
"b03_before_wc":s(q,"cf_pretax_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investing_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v(q,"cf_before_working_capital_ytd"),
"b03_cfo":s(q,"cf_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_taxes_paid_ytd","cf_other_paid_ytd")-v(q,"operating_cash_flow_ytd"),
"b03_cfi":s(q,"capital_expenditure_ytd","cf_disposal_proceeds_ytd","cf_loans_issued_ytd","cf_loans_recovered_ytd","cf_equity_investments_ytd","cf_equity_recovery_ytd","cf_investment_income_received_ytd")-v(q,"investing_cash_flow_ytd"),
"b03_cff":s(q,"cf_borrowings_ytd","cf_debt_repayments_ytd","cf_finance_leases_paid_ytd","dividends_paid_ytd")-v(q,"financing_cash_flow_ytd"),
"b03_net":s(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v(q,"net_cash_change_ytd"),
"b03_cash_bridge":s(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v(q,"cash_ending"),
"b03_B01_cash":v(q,"cash_ending")-v(q,"cash_and_equivalents"),
"q1_vs_H1_revenue":v(q,"revenue")-v(h,"revenue_ytd")+v(h,"revenue"),
"q1_vs_H1_cogs":v(q,"cost_of_goods_sold")-v(h,"cost_of_goods_sold_ytd")+v(h,"cost_of_goods_sold"),
"q1_vs_H1_gross":v(q,"gross_profit")-v(h,"gross_profit_ytd")+v(h,"gross_profit"),
"q1_vs_H1_pretax":v(q,"pretax_profit")-v(h,"pretax_profit_ytd")+v(h,"pretax_profit"),
"q1_vs_H1_net":v(q,"net_profit")-v(h,"net_profit_ytd")+v(h,"net_profit"),
"q1_vs_H1_parent":v(q,"net_profit_attributable")-v(h,"net_profit_attributable_ytd")+v(h,"net_profit_attributable"),
"same_FY_beginning":v(q,"cash_beginning_reported_ytd")-v(h,"cash_beginning_reported_ytd"),
}
assert len(checks)==28 and all(val==0 for val in checks.values()),checks
assert set(checks)==set(q["source_validation"]["statement_identity_residuals_vnd"])
assert all(x=="0" for x in q["source_validation"]["statement_identity_residuals_vnd"].values())
for field in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","capital_expenditure","foreign_exchange_effect","dividends_paid"):
    assert v(q,field)==v(q,field+"_ytd"),field
assert v(q,"cash_beginning")==v(q,"cash_beginning_reported_ytd")
assert h["verification_status"]=="issuer_signed_original_visual_verified_B01_B02_B03_H1_ytd_and_Q2_standalone_cash"
assert len(h["financial_line_items_extracted_fields"])==104
assert h["source_validation"]["q2_standalone_cashflow_status"]=="derived_from_verified_original_H1_6m_minus_Q1_3m"
assert h["source_validation"]["q2_standalone_source_Q1_original_pdf"]==q["source_url"]
expected_q2={
"operating_cash_flow":493110540478,
"investing_cash_flow":399539538641,
"financing_cash_flow":-594553494740,
"net_cash_change":298096584379,
"capital_expenditure":-15469177804,
"foreign_exchange_effect":52733093,
"dividends_paid":-75482900,
"cash_beginning":175400032558,
}
for k,amount in expected_q2.items():
    assert v(h,k)==amount,(k,v(h,k),amount)
    if k!="cash_beginning":assert v(h,k)==v(h,k+"_ytd")-v(q,k+"_ytd"),k
assert v(h,"cash_beginning")==v(q,"cash_ending")
assert v(h,"cash_beginning")+v(h,"net_cash_change")+v(h,"foreign_exchange_effect")==v(h,"cash_ending")
assert v(h,"net_cash_change")==s(h,"operating_cash_flow","investing_cash_flow","financing_cash_flow")
assert all(x=="0" for x in h["source_validation"]["q2_standalone_residuals_vnd"].values())
print("PASS: GEG 2025Q1 issuer original B01 B02 3M B03 exact 28 VND identities, H1 cross-proof, source verified Q2 standalone cash bridge; 7/7 consolidated periods source checked")
