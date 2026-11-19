#!/usr/bin/env python3
"""GEG 2025 Q4 consolidated signed original B01/B02 and FY B03 regression.

Report from original GEG signed PDF (published on HOSE, signed 26 Jan 2026),
visually read source PDF pages 6–10. 2025 FY original cash 86.364bn is
internally exact and matches GEG Q1/2026 original opening cash, whereas
GEG Q2/2026 reports restated comparative 74.942bn. Do not fabricate a
standalone Q2/2026 cash bridge or mix report vintages.
"""
import json
from decimal import Decimal
from pathlib import Path

doc=json.loads((Path(__file__).resolve().parents[1]/"data"/"financials-GEG.json").read_text("utf-8"))
rows={q["period"]:q for q in doc["items"] if "hợp nhất" in q.get("report_type","").lower()}
q=rows["2025-Q4"]
nextq=rows["2026-Q1"]
june=rows["2026-Q2"]
def v(row,k):
    return int((Decimal(str(row[k]))*Decimal(1000000)).to_integral_exact())
def s(row,*keys):
    return sum(v(row,k) for k in keys)

assert q["unit"]=="triệu VND" and q["eps"]==111 and q["diluted_eps"]==570
assert q["verification_status"]=="issuer_signed_original_visual_verified_B01_B02_B03_FY_ytd_Q4_standalone_cash_deferred"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["original_report_signed_on"]=="2026-01-26"
assert q["source_validation"]["original_pdf_total_pages"]==84
assert q["source_validation"]["visual_page_numbers"]==[6,7,8,9,10]
assert "GEG_Baocaotaichinh_Q4_2025_Hopnhat.pdf" in q["source_url"]
assert len(q["financial_line_items_extracted_fields"])==96
assert q["financial_line_items_extracted_fields"]==q["financial_line_items_manually_verified_fields"]
assert all(q.get(k) is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","foreign_exchange_effect","capital_expenditure"))
assert q["cashflow_period_basis"]=="year_to_date"
source={
 "total_assets":15110888031702,"total_liabilities":8613176165875,"equity":6497711865827,
 "current_assets":1793332240030,"non_current_assets":13317555791672,
 "current_liabilities":884097585558,"long_term_liabilities":7729078580317,
 "parent_equity":4964645836433,"non_control_interest_equity":1533066029394,
 "cash_and_equivalents":86364663248,"cash_only":46702358323,"cash_equivalents_only":39662304925,
 "short_term_investments":335162676704,"short_term_receivables":1279925753264,
 "inventory":46144766536,"other_current_assets":45734380278,
 "long_term_receivables":54322639850,"fixed_assets":12506295684512,
 "construction_in_progress":666224607122,"long_term_investments":57611864671,
 "other_non_current_assets":33100995517,
 "revenue":590444253989,"cost_of_goods_sold":297744769538,"gross_profit":292699484451,
 "financial_income":7405857236,"financial_expense":129223283175,"interest_expense":128720727251,
 "share_of_profit_in_associates":201824614,"admin_expense":80029939227,
 "operating_profit":91053943899,"other_profit":-501732145,
 "pretax_profit":90552211754,"income_tax_current":-5791447756,
 "income_tax_deferred":288594688,"income_tax":-5502853068,
 "net_profit":96055064822,"net_profit_attributable":83445048823,
 "non_controlling_interest_profit":12610015999,
 "revenue_ytd":2998867342581,"cost_of_goods_sold_ytd":1284499646212,
 "gross_profit_ytd":1714367696369,
 "pretax_profit_ytd":978664595389,"net_profit_ytd":946778853120,
 "net_profit_attributable_ytd":702152457423,
 "cf_before_working_capital_ytd":2301958106781,
 "operating_cash_flow_ytd":932884327033,
 "investing_cash_flow_ytd":1921143888,
 "financing_cash_flow_ytd":-1012240268026,
 "net_cash_change_ytd":-77434797105,
 "cash_beginning_reported_ytd":163717707072,
 "foreign_exchange_effect_ytd":81753281,
 "cash_ending":86364663248,
 "capital_expenditure_ytd":-408566559815,
 "dividends_paid_ytd":-76830949700,
}
for k,amount in source.items():
    assert v(q,k)==amount,(k,v(q,k),amount)
checks={
 "b01_assets":v(q,"total_assets")-s(q,"current_assets","non_current_assets"),
 "b01_balance":v(q,"total_assets")-s(q,"total_liabilities","equity"),
 "b01_debt":v(q,"total_liabilities")-s(q,"current_liabilities","long_term_liabilities"),
 "b01_equity_split":v(q,"equity")-s(q,"parent_equity","non_control_interest_equity"),
 "b01_current_assets":v(q,"current_assets")-s(q,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
 "b01_longterm_assets":v(q,"non_current_assets")-s(q,"long_term_receivables","fixed_assets","construction_in_progress","long_term_investments","other_non_current_assets"),
 "b01_cash":v(q,"cash_and_equivalents")-s(q,"cash_only","cash_equivalents_only"),
 "b02_gross":v(q,"revenue")-v(q,"cost_of_goods_sold")-v(q,"gross_profit"),
 "b02_operating":v(q,"gross_profit")+v(q,"financial_income")-v(q,"financial_expense")+v(q,"share_of_profit_in_associates")-v(q,"selling_expense")-v(q,"admin_expense")-v(q,"operating_profit"),
 "b02_other":v(q,"other_income")-v(q,"other_expense")-v(q,"other_profit"),
 "b02_pretax":s(q,"operating_profit","other_profit")-v(q,"pretax_profit"),
 "b02_income_tax":s(q,"income_tax_current","income_tax_deferred")-v(q,"income_tax"),
 "b02_net":v(q,"pretax_profit")-v(q,"income_tax")-v(q,"net_profit"),
 "b02_parent_nci":s(q,"net_profit_attributable","non_controlling_interest_profit")-v(q,"net_profit"),
 "annual_gross":v(q,"revenue_ytd")-v(q,"cost_of_goods_sold_ytd")-v(q,"gross_profit_ytd"),
 "annual_operating":v(q,"gross_profit_ytd")+v(q,"financial_income_ytd")-v(q,"financial_expense_ytd")+v(q,"share_of_profit_in_associates_ytd")-v(q,"admin_expense_ytd")-v(q,"operating_profit_ytd"),
 "annual_other":v(q,"other_income_ytd")-v(q,"other_expense_ytd")-v(q,"other_profit_ytd"),
 "annual_pretax":s(q,"operating_profit_ytd","other_profit_ytd")-v(q,"pretax_profit_ytd"),
 "annual_tax":s(q,"income_tax_current_ytd","income_tax_deferred_ytd")-v(q,"income_tax_ytd"),
 "annual_net":v(q,"pretax_profit_ytd")-v(q,"income_tax_ytd")-v(q,"net_profit_ytd"),
 "annual_nci":s(q,"net_profit_attributable_ytd","non_controlling_interest_profit_ytd")-v(q,"net_profit_ytd"),
 "b03_before_wc":s(q,"cf_pretax_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investing_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v(q,"cf_before_working_capital_ytd"),
 "b03_cfo":s(q,"cf_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_taxes_paid_ytd","cf_other_paid_ytd")-v(q,"operating_cash_flow_ytd"),
 "b03_cfi":s(q,"capital_expenditure_ytd","cf_disposal_proceeds_ytd","cf_loans_issued_ytd","cf_loans_recovered_ytd","cf_equity_recovery_ytd","cf_investment_income_received_ytd")-v(q,"investing_cash_flow_ytd"),
 "b03_cff":s(q,"cf_share_proceeds_ytd","cf_share_repurchase_ytd","cf_borrowings_ytd","cf_debt_repayments_ytd","cf_finance_leases_paid_ytd","dividends_paid_ytd")-v(q,"financing_cash_flow_ytd"),
 "b03_net":s(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v(q,"net_cash_change_ytd"),
 "b03_cash_bridge":s(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v(q,"cash_ending"),
 "b01_b03_cash":v(q,"cash_and_equivalents")-v(q,"cash_ending"),
 "prior_q1_opening_consistency":v(q,"cash_ending")-v(nextq,"cash_beginning_reported_ytd")
}
assert len(checks)==29 and all(x==0 for x in checks.values()),checks
assert set(checks)==set(q["source_validation"]["b01_b02_b03_identity_residuals_vnd"])
assert all(x=="0" for x in q["source_validation"]["b01_b02_b03_identity_residuals_vnd"].values())
assert v(q,"cash_ending")==86364663248
assert v(nextq,"cash_beginning_reported_ytd")==86364663248
assert v(june,"cash_beginning_reported_ytd")==74942444345
assert v(q,"cash_ending")-v(june,"cash_beginning_reported_ytd")==11422218903
assert q["source_validation"]["difference_vs_2026q2_q3_audited_comparative_2025cash_vnd"]=="11422218903"
assert q["source_validation"]["source_vintage_discrepancy_unresolved"] is True
assert q["source_validation"]["q4_standalone_cashflow_status"].startswith("deferred")
print("PASS: GEG 2025 Q4 original signed 96 fields, 29 zero VND B01/B02/FY B03 identities; Q4 original matches 2026Q1 opening; 11,422,218,903 source vintage divergence is flagged")
