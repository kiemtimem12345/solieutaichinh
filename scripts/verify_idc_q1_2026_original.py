#!/usr/bin/env python3
"""IDC consolidated Q1/2026 source images 8–14, 22 exact VND identities.

Flags a material 890,796,892 VND conflict between Q1 original 2025 year-end
cash and H1 original year-end cash. Does NOT publish Q2 standalone CFO/CFI/CFF
as a validated quarter when its issuer-source cash bridge cannot reconcile.
"""
import json
from decimal import Decimal
from pathlib import Path

rows={q["period"]:q for q in json.loads((Path(__file__).resolve().parents[1]/"data/financials-IDC.json").read_text("utf-8"))["items"]}
q,h=rows["2026-Q1"],rows["2026-Q2"]
def v(r,k):return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
def s(r,*ks):return sum(v(r,k) for k in ks)

assert q["unit"]=="triệu VND" and q["eps"]==q["diluted_eps"]==713
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_q1_2026_with_H1_opening_cash_vintage_discrepancy"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["issuer_pdf_sha256"]=="229a1ff9af9d3e1bffd777a0c9b92b4bd5cbee5bc02765f02bee5778c2b2085b"
assert q["source_validation"]["issuer_pdf_bytes"]==16372834
assert q["source_validation"]["visual_page_numbers"]==[8,9,10,11,12,13,14]
assert q["source_validation"]["source_pdf_scope"].startswith("Consolidated")
assert q["roa"] is None and q["roe"] is None
assert q["cashflow_period_basis"]=="year_to_date"
assert len(q["financial_line_items_extracted_fields"])==88
assert set(q["financial_line_items_extracted_fields"])==set(q["financial_line_items_manually_verified_fields"])

source={
 "total_assets":23539502630420,
 "current_assets":10087525251101,"non_current_assets":13451977379319,
 "total_liabilities":14689764458605,"current_liabilities":5593032195552,
 "long_term_liabilities":9096732263053,"equity":8849738171815,
 "cash_and_equivalents":800729495703,"cash_only":135939495703,
 "cash_equivalents_only":664790000000,"short_term_investments":6841660868866,
 "short_term_receivables":1039082103804,"inventory":1336544952533,
 "other_current_assets":69507830195,"fixed_assets":2875737262368,
 "investment_property":2620881388223,"long_term_construction_in_progress":7214736246995,
 "long_term_financial_investments":211213674735,
 "non_controlling_interest_equity":2123268090778,
 "gross_revenue":1485625112674,"revenue_deductions":100472253,
 "revenue":1485524640421,"cost_of_goods_sold":1096785999513,
 "gross_profit":388738640908,"financial_income":131515653570,
 "financial_expense":58967381247,"interest_expense":58741206811,
 "selling_expense":18525479401,"admin_expense":53853448503,
 "profit_from_associates":407741448,
 "operating_profit":389315726775,"pretax_profit":420297126978,
 "income_tax_current":83687912608,"income_tax_deferred":-1297966689,
 "net_profit":337907181059,"net_profit_attributable":270595917639,
 "non_controlling_interest_profit":67311263420,
 "operating_cash_flow_ytd":197524137001,"investing_cash_flow_ytd":-68608251477,
 "financing_cash_flow_ytd":118757627185,"net_cash_change_ytd":247673512709,
 "cash_beginning_reported_ytd":553052678239,"foreign_exchange_effect_ytd":3304755,
 "cash_ending":800729495703,"capital_expenditure_ytd":-271870359512,
 "dividends_paid_ytd":-36631499200,
}
for k,amount in source.items():assert v(q,k)==amount,(k,v(q,k),amount)
assert q["financial_line_items_rejected_values"]["invalid_comparative_eps_vnd"]==902

checks={
 "balance":v(q,"total_assets")-s(q,"total_liabilities","equity"),
 "asset_classes":v(q,"total_assets")-s(q,"current_assets","non_current_assets"),
 "liab_classes":v(q,"total_liabilities")-s(q,"current_liabilities","long_term_liabilities"),
 "cash_components":v(q,"cash_and_equivalents")-s(q,"cash_only","cash_equivalents_only"),
 "current_asset_classes":v(q,"current_assets")-s(q,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
 "noncurrent_asset_classes":v(q,"non_current_assets")-s(q,"long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
 "equity_classes":v(q,"equity")-s(q,"share_capital","share_premium","other_owner_capital","asset_revaluation_difference","development_investment_fund","retained_earnings","non_controlling_interest_equity"),
 "revenue":v(q,"gross_revenue")-v(q,"revenue_deductions")-v(q,"revenue"),
 "gross_profit":v(q,"revenue")-v(q,"cost_of_goods_sold")-v(q,"gross_profit"),
 "operating_profit":v(q,"gross_profit")+v(q,"financial_income")-v(q,"financial_expense")-v(q,"selling_expense")-v(q,"admin_expense")+v(q,"profit_from_associates")-v(q,"operating_profit"),
 "other_profit":v(q,"other_income")-v(q,"other_expense")-v(q,"other_profit"),
 "pretax_profit":v(q,"operating_profit")+v(q,"other_profit")-v(q,"pretax_profit"),
 "tax_components":v(q,"income_tax")-s(q,"income_tax_current","income_tax_deferred"),
 "net_profit":v(q,"pretax_profit")-v(q,"income_tax")-v(q,"net_profit"),
 "net_parent_nci":v(q,"net_profit")-s(q,"net_profit_attributable","non_controlling_interest_profit"),
 "cf_section_net":s(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v(q,"net_cash_change_ytd"),
 "cf_bridge":s(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v(q,"cash_ending"),
 "cf_B01_cash":v(q,"cash_and_equivalents")-v(q,"cash_ending"),
 "cf_before_wc":s(q,"cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd")-v(q,"cf_operating_before_working_capital_ytd"),
 "cf_operating":s(q,"cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_payments_ytd")-v(q,"operating_cash_flow_ytd"),
 "cf_investing":s(q,"capital_expenditure_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_interest_dividends_received_ytd")-v(q,"investing_cash_flow_ytd"),
 "cf_financing":s(q,"cf_share_issue_proceeds_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","dividends_paid_ytd")-v(q,"financing_cash_flow_ytd"),
}
assert len(checks)==22 and all(x==0 for x in checks.values()),checks
assert set(checks)==set(q["source_validation"]["statement_identity_residuals_vnd"])
assert all(x=="0" for x in q["source_validation"]["statement_identity_residuals_vnd"].values())

comparison=q["source_validation"]["h1_2026_opening_cash_comparison"]
assert comparison["source_vintage_mismatch_not_allocated"] is True
assert comparison["issuer_note_confirmation_pending"] is True
assert int(comparison["q1_2026_original_cash_start_vnd"])==553052678239
assert int(comparison["h1_2026_original_cash_start_vnd"])==553943475131
opening=v(h,"cash_beginning_reported_ytd")-v(q,"cash_beginning_reported_ytd")
assert opening==890796892
assert int(comparison["h1_minus_q1_opening_cash_vnd"])==opening
assert h["source_validation"]["q2_cashflow_provisional_does_not_pass_source_vintage_bridge"] is True
assert h["source_validation"]["q2_cashflow_quarter_status"].startswith("deferred_due_to_890796892")
assert all(h.get(k) is None for k in (
   "operating_cash_flow","investing_cash_flow","financing_cash_flow",
   "net_cash_change","cash_beginning","foreign_exchange_effect"))
keys=("operating_cash_flow","investing_cash_flow","financing_cash_flow",
      "net_cash_change","foreign_exchange_effect","capital_expenditure","dividends_paid")
provisional=h["source_validation"]["q2_arithmetic_only_cash_flow_provisional_vnd"]
for k in keys:
    assert int(provisional[k])==v(h,k+"_ytd")-v(q,k+"_ytd")
assert int(provisional["cash_beginning"])==v(q,"cash_ending")
assert int(provisional["operating_cash_flow"])+int(provisional["investing_cash_flow"])+int(provisional["financing_cash_flow"])==int(provisional["net_cash_change"])
gap=int(provisional["cash_beginning"])+int(provisional["net_cash_change"])+int(provisional["foreign_exchange_effect"])-v(h,"cash_ending")
assert gap==-890796892
assert int(h["source_validation"]["q2_cashflow_quarter_bridge_error_vnd"])==gap
assert int(comparison["q2_derived_quarter_cash_bridge_residual_vnd"])==gap
assert gap+opening==0
for k in ("revenue","pretax_profit","net_profit","net_profit_attributable"):
    assert v(q,k)+v(h,k)==v(h,k+"_ytd"),k
assert set(comparison["other_B02_quarters_H1_exact_residuals_vnd"].values())=={"0"}
print("PASS: IDC 2026 Q1 original B01/B02/B03 22 exact-VND source checks; EPS 713 corrected; cross-vintage Q2 cash bridge -890,796,892 VND flagged, no fabricated Q2 standalone cash")
