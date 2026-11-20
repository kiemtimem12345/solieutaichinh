#!/usr/bin/env python3
"""Signed-original PLX consolidated Q3 2026 and reviewed H1 2026, exact VND.

Q3 original PLX consolidated signed 30 Oct 2026 (36 pages, B01 pp2-4,
B02 p5, 9M B03 pp6-7): SHA256 e0b6cfd9...
H1 2026 reviewed KPMG signed 28 Aug 2026 (83 pages, B03 pp12-13):
SHA256 e26c0d58...
Quarter Q3 cash = original nine months less same-scope reviewed H1 six months.
Separate parent Q3 issuer B03 CFF typo remains QUARANTINED.
"""
import json
from decimal import Decimal
from pathlib import Path
data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-PLX.json").read_text("utf-8"))
rows=[r for r in data["items"] if r["period"]=="2026-Q3"]
assert len(rows)==2
q=next(r for r in rows if r["source_validation"]["scope"]=="consolidated")
parent=next(r for r in rows if r["source_validation"]["scope"]=="parent_company")
assert q["symbol"]=="PLX" and q["unit"]=="triệu VND"
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_q3_standalone_cash"
assert q["cashflow_period_basis"]=="quarter" and q["cashflow_ytd_period_basis"]=="nine_months"
assert q["source_validation"]["source_figures_unit"]=="VND"
assert q["eps"]==q["diluted_eps"]==835 and q["eps_ytd"]==2163
src=q["source_validation"]
assert src["original_q3_issuer_signed_pdf_sha256"]=="e0b6cfd9463c211970d0172aa8d258b8983b84ea472d59e0a242aed9ddf5c587"
assert src["original_q3_issuer_signed_pdf_pages"]==36
assert src["original_q3_issuer_signed_pdf_bytes"]==16084820
assert src["original_q3_visually_reviewed_pdf_pages"]==[2,3,4,5,6,7]
assert src["reviewed_h1_consolidated_issuer_pdf_sha256"]=="e26c0d58e991895d3704c6b2417953b2fd962255af5197a33e24ed944bf3ccd6"
assert src["reviewed_h1_consolidated_issuer_pdf_pages"]==83
assert src["reviewed_h1_consolidated_issuer_pdf_bytes"]==23713656
assert src["reviewed_h1_cashflow_visually_verified_pdf_pages"]==[12,13]
assert src["mirror_recovery_workflow_run"]==44666024791
assert src["mirror_recovery_artifact"]==14596614646
assert src["manually_visual_reviewed"] and src["full_b01_b02_b03_visual_reviewed"]
assert q["financial_line_items_extracted_fields"]==q["financial_line_items_manually_verified_fields"]
assert len(q["financial_line_items_extracted_fields"])==108
assert src["financial_source_fields_count"]==111
assert parent["source_validation"]["b03_cashflow_discrepancy_vnd"]=="87654015000"
assert not parent["source_validation"]["full_b01_b02_b03_visual_reviewed"]
assert all(parent.get(k) is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_ending"))

def v(k):
 return int((Decimal(str(q[k]))*Decimal(1000000)).to_integral_exact())
def s(*keys):
 return sum(v(k) for k in keys)
H={k:int(x) for k,x in src["original_h1_b03_source_vnd"].items()}
EXPECTED={
 "total_assets":109008605779427,"current_assets":82061675824229,
 "non_current_assets":26946929955198,"total_liabilities":77649612814671,
 "current_liabilities":76650577786933,"long_term_liabilities":999035027738,
 "equity":31358992964756,"cash_and_equivalents":6121677239224,
 "cash_only":4901906261210,"cash_equivalents_only":1219770978014,
 "short_term_investments":22285611233092,"short_term_receivables":20238334747526,
 "inventory":29295778097315,"fixed_assets":14438757021493,
 "gross_revenue":138524433268084,"revenue":138481753151156,
 "cost_of_goods_sold":131178675012184,"gross_profit":7303078138972,
 "pretax_profit":1790008444119,"net_profit":1363096640781,
 "net_profit_attributable":1240939185012,"non_controlling_interest_profit":122157455769,
 "revenue_ytd":373225984756314,"net_profit_ytd":3752865949549,
 "operating_cash_flow_ytd":-2487945351739,
 "investing_cash_flow_ytd":-6928744654125,
 "financing_cash_flow_ytd":7960585978080,
 "net_cash_change_ytd":-1456104027784,
 "cash_beginning_reported_ytd":7591431856806,
 "foreign_exchange_effect_ytd":-13650589798,
 "cash_ending":6121677239224,
 "capital_expenditure_ytd":-2372350829048,
 "dividends_paid_ytd":-1393990271569,
 "operating_cash_flow":-3432488607178,
 "investing_cash_flow":-12907578379264,
 "financing_cash_flow":16138238975341,
 "net_cash_change":-201828011101,
 "cash_beginning":6345980799984,
 "foreign_exchange_effect":-22475549659,
 "capital_expenditure":-773959104832,
 "dividends_paid":-1227987400207
}
for k,val in EXPECTED.items():
 assert v(k)==val,(k,v(k),val)

checks={
 "b01_total":v("total_assets")-s("total_liabilities","equity"),
 "b01_assets":v("total_assets")-s("current_assets","non_current_assets"),
 "b01_liabilities":v("total_liabilities")-s("current_liabilities","long_term_liabilities"),
 "b01_cash_split":v("cash_and_equivalents")-s("cash_only","cash_equivalents_only"),
 "b01_current_assets":v("current_assets")-s("cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
 "b01_noncurrent_assets":v("non_current_assets")-s("long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
 "b02_revenue":v("gross_revenue")-s("revenue_deductions","revenue"),
 "b02_gross_profit":v("revenue")-s("cost_of_goods_sold","gross_profit"),
 "b02_operating_profit":v("gross_profit")+v("financial_income")-s("financial_expense","selling_expense","admin_expense")+v("profit_from_associates")-v("operating_profit"),
 "b02_other_profit":v("other_income")-s("other_expense","other_profit"),
 "b02_pretax":v("operating_profit")+v("other_profit")-v("pretax_profit"),
 "b02_income_tax":s("income_tax_current","income_tax_deferred")-v("income_tax"),
 "b02_net_profit":v("pretax_profit")-s("income_tax","net_profit"),
 "b02_pat_split":v("net_profit")-s("net_profit_attributable","non_controlling_interest_profit"),
 "b02_ytd_revenue":v("gross_revenue_ytd")-s("revenue_deductions_ytd","revenue_ytd"),
 "b02_ytd_gross_profit":v("revenue_ytd")-s("cost_of_goods_sold_ytd","gross_profit_ytd"),
 "b02_ytd_operating_profit":v("gross_profit_ytd")+v("financial_income_ytd")-s("financial_expense_ytd","selling_expense_ytd","admin_expense_ytd")+v("profit_from_associates_ytd")-v("operating_profit_ytd"),
 "b02_ytd_pretax":s("operating_profit_ytd","other_profit_ytd")-v("pretax_profit_ytd"),
 "b02_ytd_income_tax":s("income_tax_current_ytd","income_tax_deferred_ytd")-v("income_tax_ytd"),
 "b02_ytd_net_profit":v("pretax_profit_ytd")-s("income_tax_ytd","net_profit_ytd"),
 "b02_ytd_pat_split":v("net_profit_ytd")-s("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
 "b03_ytd_operating_before_wc":s("cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v("cf_operating_before_working_capital_ytd"),
 "b03_ytd_operating":s("cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_trading_securities_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_receipts_ytd","cf_other_operating_payments_ytd")-v("operating_cash_flow_ytd"),
 "b03_ytd_investing":s("capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_other_longterm_investment_ytd","cf_other_investment_recovery_ytd","cf_interest_dividends_received_ytd")-v("investing_cash_flow_ytd"),
 "b03_ytd_financing":s("cf_share_issue_proceeds_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","dividends_paid_ytd")-v("financing_cash_flow_ytd"),
 "b03_ytd_net":s("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v("net_cash_change_ytd"),
 "b03_ytd_bridge":s("cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v("cash_ending"),
 "b03_cross_balance":v("cash_and_equivalents")-v("cash_ending"),
 "b03_h1_net":H["operating_cash_flow_ytd"]+H["investing_cash_flow_ytd"]+H["financing_cash_flow_ytd"]-H["net_cash_change_ytd"],
 "b03_h1_bridge":H["cash_beginning_reported_ytd"]+H["net_cash_change_ytd"]+H["foreign_exchange_effect_ytd"]-H["cash_ending"],
 "q3_cfo":v("operating_cash_flow_ytd")-H["operating_cash_flow_ytd"]-v("operating_cash_flow"),
 "q3_cfi":v("investing_cash_flow_ytd")-H["investing_cash_flow_ytd"]-v("investing_cash_flow"),
 "q3_cff":v("financing_cash_flow_ytd")-H["financing_cash_flow_ytd"]-v("financing_cash_flow"),
 "q3_net":v("net_cash_change_ytd")-H["net_cash_change_ytd"]-v("net_cash_change"),
 "q3_fx":v("foreign_exchange_effect_ytd")-H["foreign_exchange_effect_ytd"]-v("foreign_exchange_effect"),
 "q3_capex":v("capital_expenditure_ytd")-H["capital_expenditure_ytd"]-v("capital_expenditure"),
 "q3_dividends":v("dividends_paid_ytd")-H["dividends_paid_ytd"]-v("dividends_paid"),
 "q3_cash_begin":H["cash_ending"]-v("cash_beginning"),
 "q3_net_sections":s("operating_cash_flow","investing_cash_flow","financing_cash_flow")-v("net_cash_change"),
 "q3_cash_bridge":s("cash_beginning","net_cash_change","foreign_exchange_effect")-v("cash_ending"),
}
assert len(checks)==40
assert all(residual==0 for residual in checks.values()),checks
assert set(checks)==set(src["statement_identity_residuals_vnd"])
assert all(int(val)==0 for val in src["statement_identity_residuals_vnd"].values())
assert src["q3_standalone_cashflow_status"]=="verified_signed_9m_minus_reviewed_signed_h1_same_consolidated_scope_and_cash_bridge_exact"
assert src["original_parent_q3_cff_anomaly_isolated"].startswith("Parent Q3 signed PDF")
print("PASS PLX 2026 Q3 consolidated signed original B01/B02/B03 108 VND numeric fields + 3 EPS, 40 source exact-VND identities; 9M-minus-reviewed-H1 Q3 standalone CFO/CFI/CFF and cash bridge 0 VND. Parent Q3 87,654,015,000 VND printed CFF anomaly remains blocked.")
