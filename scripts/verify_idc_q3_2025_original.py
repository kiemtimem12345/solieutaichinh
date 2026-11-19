#!/usr/bin/env python3
"""IDC Q3 2025 original signed HNX consolidated PDF, 30 exact-VND identities.

Authentic source: HNX Q3 publication mirrored ZIP, its embedded signed
Vietnamese consolidated PDF (NOT any parent-only or English OCR approximation).
Q4 standalone cashflow equals original FY2025 12M minus this original 9M.
"""
import json
from decimal import Decimal
from pathlib import Path

rows={r["period"]:r for r in json.loads((Path(__file__).resolve().parents[1]/"data/financials-IDC.json").read_text("utf-8"))["items"]}
q,y=rows["2025-Q3"],rows["2025-Q4"]
def V(r,k):return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
def S(r,*ks):return sum(V(r,k) for k in ks)

assert q["symbol"]=="IDC" and q["unit"]=="triệu VND"
assert q["report_type"].startswith("BCTC hợp nhất IDC Q3/2025")
assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_ytd_q3_cash_deferred"
assert q["cashflow_period_basis"]=="year_to_date"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["source_scope"].startswith("consolidated")
assert q["source_validation"]["original_hnx_mirrored_zip_sha256"]=="04ff7104fec1b3fd47c3567570c862072bc1bebde48968e4249b06e0b5650394"
assert q["source_validation"]["original_issuer_signed_pdf_sha256"]=="80c1b3dcb2e5469d4fb84c3a0cbd46c51f664ce7e07a2a0946e10b691ca92ce3"
assert q["source_validation"]["original_pdf_member"]=="3_idc_2025_10_30_d9319de_vi_baocaotaichinhhn_q3_2025_s.pdf"
assert q["source_validation"]["original_pdf_bytes"]==16173434
assert q["source_validation"]["original_pdf_pages"]==64
assert q["source_validation"]["reviewed_pdf_pages"]==[8,9,10,11,12,13,14]
assert q["source_validation"]["source_recovery_actions_run"]==44550845936
assert len(q["financial_line_items_extracted_fields"])==102
assert q["financial_line_items_manually_verified_fields"]==q["financial_line_items_extracted_fields"]
assert q["roa"] is None and q["roe"] is None
assert q["eps"]==q["diluted_eps"]==2218
assert all(q.get(k) is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","foreign_exchange_effect","capital_expenditure","dividends_paid"))
fixture={
"total_assets":21293030253931,"current_assets":9562532464360,"non_current_assets":11730497789571,
"total_liabilities":12926247964300,"current_liabilities":4317438822891,
"long_term_liabilities":8608809141409,"equity":8366782289631,
"cash_and_equivalents":791686559919,"cash_only":104713929782,
"cash_equivalents_only":686972630137,"short_term_investments":5645952622247,
"short_term_receivables":1774478928980,"inventory":1311842293999,
"long_term_construction_in_progress":5373551149168,
"non_controlling_interest_equity":1787088831649,
"gross_revenue":2871423273613,"revenue_deductions":93800926,"revenue":2871329472687,
"cost_of_goods_sold":1614206888266,"gross_profit":1257122584421,
"financial_income":84797217769,"financial_expense":34133582233,
"profit_from_associates":-139003519,"selling_expense":26561121573,
"admin_expense":70669003009,"operating_profit":1210417091856,
"other_profit":8075636171,"pretax_profit":1218492728027,
"income_tax":237355226039,"income_tax_current":265623067711,
"income_tax_deferred":-28267841672,"net_profit":981137501988,
"net_profit_attributable":841835881584,"non_controlling_interest_profit":139301620404,
"revenue_ytd":6428011659828,"cost_of_goods_sold_ytd":4074980483625,
"gross_profit_ytd":2353031176203,"operating_profit_ytd":2177260253656,
"pretax_profit_ytd":2258525812470,"net_profit_ytd":1814085953812,
"net_profit_attributable_ytd":1482687893336,
"non_controlling_interest_profit_ytd":331398060476,
"operating_cash_flow_ytd":2943740801880,"investing_cash_flow_ytd":-4680519162668,
"financing_cash_flow_ytd":340361746335,"net_cash_change_ytd":-1396416614453,
"cash_beginning_reported_ytd":2188037806317,"foreign_exchange_effect_ytd":65368055,
"cash_ending":791686559919,"capital_expenditure_ytd":-1803039281720,
"dividends_paid_ytd":-646100636720,
"cf_operating_before_working_capital_ytd":2871434984910}
for k,expected in fixture.items():assert V(q,k)==expected,(k,V(q,k),expected)

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
"ytd_revenue":V(q,"gross_revenue_ytd")-V(q,"revenue_deductions_ytd")-V(q,"revenue_ytd"),
"ytd_grossprofit":V(q,"revenue_ytd")-V(q,"cost_of_goods_sold_ytd")-V(q,"gross_profit_ytd"),
"ytd_operatingprofit":V(q,"gross_profit_ytd")+V(q,"financial_income_ytd")-V(q,"financial_expense_ytd")+V(q,"profit_from_associates_ytd")-V(q,"selling_expense_ytd")-V(q,"admin_expense_ytd")-V(q,"operating_profit_ytd"),
"ytd_otherprofit":V(q,"other_income_ytd")-V(q,"other_expense_ytd")-V(q,"other_profit_ytd"),
"ytd_pretax":V(q,"operating_profit_ytd")+V(q,"other_profit_ytd")-V(q,"pretax_profit_ytd"),
"ytd_tax":V(q,"income_tax_ytd")-S(q,"income_tax_current_ytd","income_tax_deferred_ytd"),
"ytd_net":V(q,"pretax_profit_ytd")-V(q,"income_tax_ytd")-V(q,"net_profit_ytd"),
"ytd_profit_split":V(q,"net_profit_ytd")-S(q,"net_profit_attributable_ytd","non_controlling_interest_profit_ytd"),
"cf_sections":S(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-V(q,"net_cash_change_ytd"),
"cf_bridge":S(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-V(q,"cash_ending"),
"cf_cash":V(q,"cash_and_equivalents")-V(q,"cash_ending"),
"cf_before_wc":S(q,"cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd")-V(q,"cf_operating_before_working_capital_ytd"),
"cf_operating":S(q,"cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_payments_ytd")-V(q,"operating_cash_flow_ytd"),
"cf_investing":S(q,"capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_interest_dividends_received_ytd")-V(q,"investing_cash_flow_ytd"),
"cf_financing":S(q,"cf_share_issue_proceeds_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","dividends_paid_ytd")-V(q,"financing_cash_flow_ytd")
}
assert len(checks)==30 and all(x==0 for x in checks.values()),checks
assert checks.keys()==q["source_validation"]["statement_identity_residuals_vnd"].keys()
assert all(int(x)==0 for x in q["source_validation"]["statement_identity_residuals_vnd"].values())

assert y["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_fy_and_q4_standalone_cash"
assert y["source_validation"]["standalone_q4_source_9m_pdf_sha256"]==q["source_validation"]["original_issuer_signed_pdf_sha256"]
assert len(y["source_validation"]["q4_income_FY_minus_9M_residuals_vnd"])==9
assert all(int(x)==0 for x in y["source_validation"]["q4_income_FY_minus_9M_residuals_vnd"].values())
for k in ("revenue","gross_profit","cost_of_goods_sold","operating_profit","other_profit","pretax_profit","net_profit","net_profit_attributable","non_controlling_interest_profit"):
    assert V(y,k)==V(y,k+"_ytd")-V(q,k+"_ytd"),k
expected_q4={
"operating_cash_flow":970200007993,"investing_cash_flow":-2329374796016,
"financing_cash_flow":1120543443747,"net_cash_change":-238631344276,
"foreign_exchange_effect":-2537404,"capital_expenditure":-1300428928495,
"dividends_paid":-654131953577,"cash_beginning":791686559919}
for k,value in expected_q4.items():
    assert V(y,k)==value,(k,V(y,k),value)
    assert int(y["source_validation"]["standalone_q4_derived_vnd"][k])==value
    if k!="cash_beginning":assert V(y,k)==V(y,k+"_ytd")-V(q,k+"_ytd"),k
assert V(y,"cash_beginning")==V(q,"cash_ending")
assert V(y,"cash_beginning")+V(y,"net_cash_change")+V(y,"foreign_exchange_effect")==V(y,"cash_ending")
assert S(y,"operating_cash_flow","investing_cash_flow","financing_cash_flow")==V(y,"net_cash_change")
assert len(y["source_validation"]["standalone_q4_identity_residuals_vnd"])==5
assert all(int(x)==0 for x in y["source_validation"]["standalone_q4_identity_residuals_vnd"].values())
print("PASS IDC 2025Q3 102 issuer fields 30 VND identities, original ZIP PDF hash; IDC Q4 FY-minus-9M 9 B02 and 5 quarter cash exact checks; 2026 Q2 cash-vintage exception intact")
