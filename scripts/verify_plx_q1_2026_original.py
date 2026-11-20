#!/usr/bin/env python3
"""PLX 2026-Q1 signed consolidated original accounting validation.

A full 36-page issuer signed original was visually inspected on 20 Nov 2026:
B01 pp2–4, B02 p5, B03 pp6–7. ALL 34 valid financial identities in
the originally PRINTED source pass at exact VND. But two B01 subtotals
DO NOT match displayed components, each above the user's 0.01% threshold:
receivables 9,083,970,186 VND; current liabilities 9,088,965,442 VND.
The comparative cash reclassification is now source-verified: FY2025 cash
minus Q1 opening cash equals the increase in B01 code 165 (other current
assets), exactly the opening "Tien gui tai Quy Binh on gia" in Q1 Note 16:
3,087,558,817,574 VND. It is noncash and is NOT CFO/CFI/CFF. The two
signed B01 detailed-subtotal discrepancies remain unresolved and blocked.

The 2026 Q1 basic EPS source cell is blank. Code 70 is a row ID, not EPS.
Diluted EPS source row71 is -521 VND/share. Keep basic EPS null.
"""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
doc=json.loads((ROOT/"data/financials-PLX.json").read_text(encoding="utf-8"))
q=next(x for x in doc["items"] if x["period"]=="2026-Q1" and "hợp nhất" in x["report_type"].lower())
s=q["source_validation"]
groups={}
group=None
for line in (ROOT/"reports/source-audits/PLX-2026Q1-consolidated-signed-original-vnd.txt").read_text(encoding="utf-8").splitlines():
    if line.startswith("# BEGIN "):
        group=line[8:].strip()
        assert group not in groups
        groups[group]={}
        continue
    if line.startswith("# END "): group=None;continue
    if not line or line.startswith("#"):continue
    k,v=line.split()
    assert group in groups and k not in groups[group] and v.lstrip("-").isdigit(),line
    groups[group][k]=int(v)
V=groups["SOURCE_B01_B02_B03"]
D=groups["ORIGINAL_B01_DETAIL"]
O=groups["SOURCE_OPENING_COMPARATIVE"]
R=groups["OPENING_CASH_RECLASSIFICATION"]
assert (len(V),len(D))==(82,55)
def value(k):
    assert isinstance(q.get(k),(float,int)) and not isinstance(q[k],bool),(k,q.get(k))
    raw=Decimal(str(q[k]))*1000000
    assert raw==raw.to_integral_value(),(k,raw)
    return int(raw)
for k,v in V.items():
    assert value(k)==v,(k,value(k),v)
for k in ("gross_revenue","revenue_deductions","revenue","cost_of_goods_sold","gross_profit","pretax_profit","net_profit","net_profit_attributable","non_controlling_interest_profit","income_tax","income_tax_current","income_tax_deferred"):
    assert value(k+"_ytd")==V[k]
for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure","dividends_paid"):
    assert value(k)==V[k+"_ytd"]
assert value("cash_beginning")==O["opening_cash_on_Q1_2026_B01_B03"]
def summed(t,*keys):return sum(t[k] for k in keys)
checks={
"b01_asset_classes":V["total_assets"]-summed(V,"current_assets","non_current_assets"),
"b01_balance_sheet":V["total_assets"]-summed(V,"total_liabilities","equity"),
"b01_liability_classes":V["total_liabilities"]-summed(V,"current_liabilities","long_term_liabilities"),
"b01_current_asset_classes":V["current_assets"]-summed(V,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"b01_noncurrent_asset_classes":V["non_current_assets"]-summed(V,"long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
"b01_cash_split":V["cash_and_equivalents"]-summed(V,"cash_only","cash_equivalents_only"),
"b01_short_investments":V["short_term_investments"]-summed(D,"short_invest_trading","short_invest_provision","short_invest_HtM"),
"b01_inventory":V["inventory"]-summed(D,"inventory_gross","inventory_provision"),
"b01_other_current":V["other_current_assets"]-summed(D,"other_current_prepay","other_current_VAT","other_current_tax","other_current_other"),
"b01_noncurrent_receivables":V["long_term_receivables"]-summed(D,"long_receivables_customer","long_receivables_other","long_receivables_provision"),
"b01_fixed_assets":V["fixed_assets"]-summed(D,"fixed_assets_tangible","fixed_assets_intangible"),
"b01_investment_property":V["investment_property"]-summed(D,"investment_property_gross","investment_property_depr"),
"b01_longterm_investments":V["long_term_financial_investments"]-summed(D,"long_invest_associates","long_invest_others","long_invest_provision","long_invest_HTM"),
"b01_other_noncurrent":V["other_non_current_assets"]-summed(D,"other_noncurrent_prepaid","other_noncurrent_deferredtax","other_noncurrent_other"),
"b01_equity_details":V["equity"]-summed(D,"equity_charter","equity_premium","equity_other_owner","equity_treasury","equity_asset_reval","equity_fx_delta","equity_development_fund","equity_other_fund")-V["retained_earnings"]-V["non_controlling_interest_equity"],
"b01_long_liability_details":V["long_term_liabilities"]-summed(D,"long_liab_customer_advances","long_liab_accrued_expenses","long_liab_unearned_revenue","long_liab_other","long_liab_borrowings","long_liab_deferredtax","long_liab_provision"),
"b01_opening_from_audited":O["opening_total_assets"]-O["opening_total_liabilities"]-O["opening_equity"],
"b02_revenue":V["gross_revenue"]-summed(V,"revenue_deductions","revenue"),
"b02_gross":V["revenue"]-summed(V,"cost_of_goods_sold","gross_profit"),
"b02_operating":V["gross_profit"]+V["financial_income"]+V["profit_from_associates"]-summed(V,"financial_expense","selling_expense","admin_expense","operating_profit"),
"b02_other":V["other_income"]-summed(V,"other_expense","other_profit"),
"b02_pretax":V["operating_profit"]+V["other_profit"]-V["pretax_profit"],
"b02_tax":V["income_tax_current"]+V["income_tax_deferred"]-V["income_tax"],
"b02_aftertax":V["pretax_profit"]-V["income_tax"]-V["net_profit"],
"b02_parent_NCI":V["net_profit"]-V["net_profit_attributable"]-V["non_controlling_interest_profit"],
"b03_pretax_matches_B02":V["cf_pretax_profit_ytd"]-V["pretax_profit"],
"b03_preWC":summed(V,"cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-V["cf_operating_before_working_capital_ytd"],
"b03_CFO":summed(V,"cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_trading_securities_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_receipts_ytd","cf_other_operating_payments_ytd")-V["operating_cash_flow_ytd"],
"b03_CFI":summed(V,"capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_other_longterm_investment_ytd","cf_other_investment_recovery_ytd","cf_interest_dividends_received_ytd")-V["investing_cash_flow_ytd"],
"b03_CFF":summed(V,"cf_share_issue_proceeds_ytd","cf_repurchase_shares_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","cf_finance_lease_repayments_ytd","dividends_paid_ytd")-V["financing_cash_flow_ytd"],
"b03_net":V["operating_cash_flow_ytd"]+V["investing_cash_flow_ytd"]+V["financing_cash_flow_ytd"]-V["net_cash_change_ytd"],
"b03_cashbridge":O["opening_cash_on_Q1_2026_B01_B03"]+V["net_cash_change_ytd"]+V["foreign_exchange_effect_ytd"]-V["cash_ending"],
"b03_ending_agrees_B01":V["cash_ending"]-V["cash_and_equivalents"],
"b03_opening_agrees_B01":O["opening_cash_on_Q1_2026_B01_B03"]-V["cash_beginning_reported_ytd"],
}
assert len(checks)==34
assert all(v==0 for v in checks.values()),{k:v for k,v in checks.items() if v}
anom_recv=V["short_term_receivables"]-summed(D,"recv_customers","recv_advances","recv_other","recv_provision","recv_pending")
anom_liab=V["current_liabilities"]-summed(D,"current_liab_suppliers","current_liab_customer_advances","current_liab_dividend_payable","current_liab_taxes","current_liab_employees","current_liab_accruals","current_liab_unearned_revenue","current_liab_other","current_liab_borrowings","current_liab_provision","current_liab_staff_fund","current_liab_stabilization")
anom_open=O["opening_cash_on_Q1_2026_B01_B03"]-O["FY2025_audited_cash_ending"]
assert (anom_recv,anom_liab,anom_open)==(9083970186,9088965442,-3087558817574)
assert Decimal(anom_recv)/Decimal(V["short_term_receivables"])*100>Decimal("0.01")
assert Decimal(anom_liab)/Decimal(V["current_liabilities"])*100>Decimal("0.01")
assert s["signed_original_b01_short_receivables_unexplained_difference_vnd"]==str(anom_recv)
assert s["signed_original_b01_current_liabilities_unexplained_difference_vnd"]==str(anom_liab)
assert s["opening_cash_Q1_minus_FY2025_audited_vnd"]==str(anom_open)
assert s["b01_subgroups_exceed_001percent_tolerance"] is True
assert s["full_b01_component_arithmetic_passed"] is False
# FY2025 audited -> Q1 as-filed comparative: only a reclassification.
assert len(R)==7
fund=R["q1_2026_note16_opening_price_stabilization_deposit"]
assert fund==3087558817574
assert R["fy2025_audited_cash"]==O["FY2025_audited_cash_ending"]
assert R["q1_2026_opening_cash"]==O["opening_cash_on_Q1_2026_B01_B03"]
assert R["fy2025_audited_cash"]-R["q1_2026_opening_cash"]==fund
assert R["q1_2026_opening_other_current_assets"]-R["fy2025_audited_other_current_assets"]==fund
assert R["q1_2026_opening_other_current_other"]-R["fy2025_audited_other_current_other"]==fund
assert (R["fy2025_audited_cash"]+R["fy2025_audited_other_current_assets"]==
        R["q1_2026_opening_cash"]+R["q1_2026_opening_other_current_assets"])
assert (R["q1_2026_opening_other_current_other"]-fund==
        R["fy2025_audited_other_current_other"])
assert s["opening_cash_Q1_minus_FY2025_audited_vnd"]==str(-fund)
assert s["opening_cash_reclassification_status"]=="verified_exact_vnd_note16_and_FY2025_audited"
assert s["Q1_2026_note16_opening_price_stabilization_deposit_vnd"]==str(fund)
for k in ("FY2025_audited_other_current_assets","Q1_2026_opening_other_current_assets",
          "FY2025_audited_other_current_other","Q1_2026_opening_other_current_other"):
    assert s[k+"_vnd"]==str(R[k.lower().replace("fy2025","fy2025").replace("q1_2026","q1_2026")]),k
assert s["opening_cash_reclassification_evidence"]["Q1_signed_pdf_note16_page"]==21
assert s["opening_cash_reclassification_evidence"]["cash_from_B01_code"]=="110"
assert s["opening_cash_reclassification_evidence"]["other_current_asset_to_B01_code"]=="165"
assert s["opening_cash_reclassification_exact_destination_explanation"].startswith("VERIFIED:")
# Neither source-reported B01 subtotal may be accepted as reconciled absent a signed erratum.
assert s["b01_subgroups_explanation_status"].endswith("requires_official_erratum")
assert s["b01_full_pass_blocked_until_official_correction"] is True
assert s["full_b01_component_arithmetic_passed"] is False
assert s["original_B01_opening_cash_reclassified_as_printed"] is True
assert s["original_B03_comparative_prior_year_reclassified_as_printed"] is True
assert s["manually_visual_reviewed"] and s["full_b01_b02_b03_visual_reviewed"]
assert s["source_scope"]=="consolidated"
assert s["original_issuer_signed_pdf_sha256"]=="158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f4bc5f9"
assert (s["original_issuer_signed_pdf_bytes"],s["original_issuer_signed_pdf_pages"])==(7990499,36)
assert (s["original_source_recovery_workflow"],s["original_source_artifact_id"])==(44687366816,14606503712)
assert s["original_visually_reviewed_pages"]==[2,3,4,5,6,7]
assert s["signed_original_exact_vnd_identity_count"]==34
assert s["signed_original_exact_vnd_identity_max_residual"]==0
assert s["B02_basic_EPS_Q1_2026_printed_cell_blank"] is True
assert q["eps"] is None and q["eps_ytd"] is None
assert q["diluted_eps"]==q["diluted_eps_ytd"]==-521
assert q["cashflow_period_basis"]=="quarter"
assert q["cashflow_ytd_period_basis"]=="three_months"
assert q["verification_status"]=="signed_original_visual_B01_B02_B03_Q1_2026_34_exact_vnd_checks_with_B01_subgroup_and_opening_cash_vintage_exceptions"
roa=Decimal(4*V["net_profit"])/((Decimal(O["opening_total_assets"])+V["total_assets"])/2)*100
roe=Decimal(4*V["net_profit"])/((Decimal(O["opening_equity"])+V["equity"])/2)*100
assert round(roa,2)==Decimal("-2.76") and round(roe,2)==Decimal("-9.07")
assert (q["roa"],q["roe"])==(-2.76,-9.07)
parent=next(x for x in doc["items"] if x["period"]=="2026-Q3" and x["source_validation"].get("scope")=="parent_company")
assert parent["source_validation"]["b03_cashflow_discrepancy_vnd"]=="87654015000"
assert parent.get("financing_cash_flow") is None
print("PASS: PLX Q1 2026 signed original 36p, 82 monetary VND source fields; 34 exact identities zero VND. B01 mismatches receivables 9,083,970,186 and current liabilities 9,088,965,442 VND QUARANTINED; opening cash reclassification +3,087,558,817,574 VND to restricted price-stabilization-fund deposits in B01 code165 VERIFIED from Note 16; basic EPS blank, diluted -521, Q1 CFO+CFI+CFF and cash bridge exact. 2026 parent Q3 CFF source error still blocked.")
