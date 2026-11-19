#!/usr/bin/env python3
"""Verify VDS consolidated 2026-Q2 B01 and B02 scanned original at exact VND.

Issuer original 29 July 2026 PDF pages 6-8 B01 and 11-13 B02, checked as
images. Securities B02 revenue must use code 20 not its FVTPL component.
Separate 6M B03 is verified in verify_vds_q2h1_q3cash_bridge.py.
"""
import json
from decimal import Decimal
from pathlib import Path

data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-VDS.json").read_text("utf-8"))
q=next(r for r in data["items"] if r["period"]=="2026-Q2")
def v(k):
    return int((Decimal(str(q[k]))*Decimal(1000000)).to_integral_exact())
def s(*keys):
    return sum(v(k) for k in keys)
assert q["unit"]=="triệu VND" and q["eps"]==q["diluted_eps"]==134
assert q["roa"] is None and q["roe"] is None
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_h1_q2_standalone_cash_deferred"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["issuer_original_visual_artifact"].endswith("and others")
assert q["source_validation"]["issuer_pdf_sha256"]=="d16188e1e63da279e5214af46271dfd67dab4d26c20c2d77c78cb1db56200410"
assert q["source_validation"]["issuer_b01_b02_original_pdf_pages"]==[6,7,8,11,12,13]
assert set(q["financial_line_items_extracted_fields"])==set(q["financial_line_items_manually_verified_fields"])
assert len(q["financial_line_items_manually_verified_fields"])==87
assert q["operating_cash_flow"] is None and q["investing_cash_flow"] is None and q["financing_cash_flow"] is None
assert q["selling_expense"] is None
src={
"total_assets":7906589387452,"total_liabilities":4892114272349,"equity":3014475115103,
"current_assets":6637898183061,"non_current_assets":1268691204391,
"financial_current_assets":6619450438640,"other_current_assets":18447744421,
"financial_noncurrent_assets":1177520336212,"fixed_assets":49396644981,
"construction_in_progress":653595750,"other_noncurrent_assets":41120627448,
"current_liabilities":4888996386336,"long_term_liabilities":3117886013,
"cash_and_equivalents":801617758652,"cash_only":576617758652,"cash_equivalents_only":225000000000,
"broker_fvtpl_assets":1061476078606,"broker_held_to_maturity_assets":20000000000,
"broker_lending_assets":4289666502091,"broker_afs_assets":434797280000,
"broker_financial_assets_impairment":-44212240217,"broker_receivables":36737345980,
"broker_other_short_term_financial_receivables_net":19367713528,
"broker_noncurrent_held_to_maturity_assets":1100000000000,"broker_noncurrent_other_investments":77520336212,
"broker_short_term_borrowings":2776900000000,"broker_short_term_bonds":1998900000000,
"retained_earnings":363368457472,"non_control_interest_equity":-56506662501,
"revenue":262152978583,"revenue_ytd":458846424238,
"broker_fvtpl_gain":74785440340,"broker_htm_income":18225781764,
"broker_lending_income":123834858318,"broker_afs_interest_income":2000000000,
"broker_brokerage_revenue":36840270210,"broker_custody_revenue":2060235845,
"broker_financial_advisory_revenue":3661772728,"broker_other_operating_income":744619378,
"broker_total_operating_revenue":262152978583,
"broker_total_operating_expenses":157186798783,"broker_operating_expenses":157186798783,
"broker_fvtpl_loss":41166314626,"broker_afs_reclassification_loss":675956030,
"broker_loan_loss_and_borrowing_provision":75865908788,"broker_trading_expense":955756099,
"broker_brokerage_expense":32444203873,"broker_custody_expense":2002099304,
"broker_advisory_expense":3464127651,"broker_other_service_expense":612432412,
"financial_income":5473235995,"financial_expense":21800613791,
"interest_expense":15880539449,"admin_expense":45931870444,
"operating_profit":42706931560,"other_income":11985948,"other_expense":6512002,
"other_profit":5473946,"pretax_profit":42712405506,
"income_tax":9613460295,"income_tax_current":14004787251,"income_tax_deferred":-4391326956,
"net_profit":33098945211,"net_profit_attributable":36516641493,"non_controlling_interest_profit":-3417696282,
"securities_operating_expense_ytd":341668738203,
"financial_income_ytd":15457780956,"financial_expense_ytd":34527225824,"admin_expense_ytd":91436924760,
"operating_profit_ytd":6671316407,"other_income_ytd":12531402,"other_expense_ytd":6512002,
"other_profit_ytd":6019400,"pretax_profit_ytd":6677335807,"income_tax_ytd":3069191042,
"net_profit_ytd":3608144765,"net_profit_attributable_ytd":8131939292,
"non_controlling_interest_profit_ytd":-4523794527}
for k,x in src.items():
    assert v(k)==x,(k,v(k),x)
checks={
"b01_total_balance":v("total_assets")-s("total_liabilities","equity"),
"b01_asset_classes":v("total_assets")-s("current_assets","non_current_assets"),
"b01_liability_classes":v("total_liabilities")-s("current_liabilities","long_term_liabilities"),
"b01_current_classes":v("current_assets")-s("financial_current_assets","other_current_assets"),
"b01_noncurrent_classes":v("non_current_assets")-s("financial_noncurrent_assets","fixed_assets","construction_in_progress","other_noncurrent_assets"),
"b01_cash_components":v("cash_and_equivalents")-s("cash_only","cash_equivalents_only"),
"b01_financial_current_components":v("financial_current_assets")-s("cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets","broker_lending_assets","broker_afs_assets","broker_financial_assets_impairment","broker_receivables","broker_other_short_term_financial_receivables_net"),
"b01_noncurrent_financial_components":v("financial_noncurrent_assets")-s("broker_noncurrent_held_to_maturity_assets","broker_noncurrent_other_investments"),
"b02_revenue_components":v("revenue")-s("broker_fvtpl_gain","broker_htm_income","broker_lending_income","broker_afs_interest_income","broker_brokerage_revenue","broker_custody_revenue","broker_financial_advisory_revenue","broker_other_operating_income"),
"b02_revenue_duplicate":v("revenue")-v("broker_total_operating_revenue"),
"b02_expense_components":v("broker_total_operating_expenses")-s("broker_fvtpl_loss","broker_afs_reclassification_loss","broker_loan_loss_and_borrowing_provision","broker_trading_expense","broker_brokerage_expense","broker_custody_expense","broker_advisory_expense","broker_other_service_expense"),
"b02_expense_duplicate":v("broker_total_operating_expenses")-v("broker_operating_expenses"),
"b02_operating":v("operating_profit")-v("revenue")-v("financial_income")+s("broker_total_operating_expenses","financial_expense","admin_expense"),
"b02_other":v("other_profit")-v("other_income")+v("other_expense"),
"b02_pretax":v("pretax_profit")-s("operating_profit","other_profit"),
"b02_tax":v("income_tax")-s("income_tax_current","income_tax_deferred"),
"b02_net":v("net_profit")-v("pretax_profit")+v("income_tax"),
"b02_attributable":v("net_profit")-s("net_profit_attributable","non_controlling_interest_profit"),
"b02_ytd_operating":v("operating_profit_ytd")-v("revenue_ytd")-v("financial_income_ytd")+s("securities_operating_expense_ytd","financial_expense_ytd","admin_expense_ytd"),
"b02_ytd_other":v("other_profit_ytd")-v("other_income_ytd")+v("other_expense_ytd"),
"b02_ytd_pretax":v("pretax_profit_ytd")-s("operating_profit_ytd","other_profit_ytd"),
"b02_ytd_net":v("net_profit_ytd")-v("pretax_profit_ytd")+v("income_tax_ytd"),
"b02_ytd_attributable":v("net_profit_ytd")-s("net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
"b01_b03_cash":v("cash_and_equivalents")-v("cash_ending")
}
assert len(checks)==24 and all(x==0 for x in checks.values()),checks
assert set(checks)==set(q["source_validation"]["b01_b02_exact_identity_residuals_vnd"])
assert all(x=="0" for x in q["source_validation"]["b01_b02_exact_identity_residuals_vnd"].values())
prior=q["financial_line_items_prior_values"]["prior_auto_extracted_b01b02_before_issuer_visual_20261119"]
assert q["financial_line_items_rejected_values"]["prior_auto_revenue_million_vnd"]==74785
assert q["financial_line_items_rejected_values"]["prior_auto_eps_vnd"]==501
assert prior["financial_income"]==0
assert prior["broker_total_operating_revenue"]==262153
assert q["source_validation"]["b03_h1_issuer_original_visual_verified"] is True
print("PASS: VDS Q2/2026 consolidated issuer original B01/B02 24 exact-VND identities, 87 source fields, restored securities revenue 262.152bn EPS 134; B03 H1 unchanged, Q2 quarter cash still deferred")
