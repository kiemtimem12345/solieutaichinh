#!/usr/bin/env python3
"""GEG Q3/2025 original consolidated signed B01/B02 and 9M B03 regression.

Official GEG original 83-page signed PDF (published 30 Oct 2025); images
p5 B01 assets, p6 B01 liabilities, p7 B02 quarter/9M, p8-9 B03 9M.
Every arithmetic assertion uses Decimal(million VND) -> exact original VND.
"""
import json
from decimal import Decimal
from pathlib import Path

doc=json.loads((Path(__file__).resolve().parents[1]/"data"/"financials-GEG.json").read_text("utf-8"))
rows={r["period"]:r for r in doc["items"] if "hợp nhất" in r.get("report_type","").lower()}
q,f=rows["2025-Q3"],rows["2025-Q4"]
def v(row,k):return int((Decimal(str(row[k]))*Decimal(1000000)).to_integral_exact())
def s(row,*keys):return sum(v(row,k) for k in keys)

assert q["unit"]=="triệu VND"
assert q["verification_status"]=="issuer_signed_original_visual_verified_B01_B02_B03_9m_ytd_and_Q3_standalone_cash"
assert q["source_validation"]["manually_visual_reviewed"] is True
assert q["source_validation"]["original_pdf_total_pages"]==83
assert q["source_validation"]["original_visual_page_numbers"]==[5,6,7,8,9]
assert q["source_validation"]["signed_report_date"]=="2025-10-28"
assert q["eps"]==198 and q["diluted_eps"]==198
assert len(q["financial_line_items_extracted_fields"])==104
assert q["financial_line_items_extracted_fields"]==q["financial_line_items_manually_verified_fields"]
assert v(q,"operating_cash_flow")==300787939022
assert v(q,"investing_cash_flow")==-232035400955
assert v(q,"financing_cash_flow")==-136266702635
assert v(q,"net_cash_change")==-67514164568
assert v(q,"capital_expenditure")==-103386144231
assert v(q,"foreign_exchange_effect")==18111591
assert v(q,"cash_beginning")==473549350030
assert v(q,"cash_beginning")+v(q,"net_cash_change")+v(q,"foreign_exchange_effect")==v(q,"cash_ending")
assert v(q,"net_cash_change")==s(q,"operating_cash_flow","investing_cash_flow","financing_cash_flow")
assert q["source_validation"]["q3_standalone_cashflow_status"]=="derived_from_verified_original_9m_minus_H1_6m"
assert all(x=="0" for x in q["source_validation"]["q3_standalone_residuals_vnd"].values())
original={
"total_assets":15247952050819,"total_liabilities":8674761966494,"equity":6573190084325,
"current_assets":1975118527567,"non_current_assets":13272833523252,
"current_liabilities":950488102304,"long_term_liabilities":7724273864190,
"parent_equity":5008341099594,"non_control_interest_equity":1564848984731,
"cash_and_equivalents":406053297053,"cash_only":95553297053,"cash_equivalents_only":310500000000,
"short_term_investments":378500000000,"short_term_receivables":1099569520475,
"inventory":62960131810,"other_current_assets":28035578229,
"long_term_receivables":100576654702,"fixed_assets":12701094168860,
"construction_in_progress":381389541012,"long_term_investments":54283512223,
"other_non_current_assets":35489646455,
"revenue":671328091438,"cost_of_goods_sold":348638552595,
"gross_profit":322689538843,"financial_income":7288526236,
"financial_expense":194351138463,"share_of_profit_in_associates":625069998,
"admin_expense":37895058681,"operating_profit":98356937933,
"other_income":616491042,"other_expense":247139597,"other_profit":369351445,
"pretax_profit":98726289378,"income_tax_current":18340054977,
"income_tax_deferred":323314089,"income_tax":18663369066,
"net_profit":80062920312,"net_profit_attributable":74645813663,
"non_controlling_interest_profit":5417106649,
"revenue_ytd":2408423088592,"cost_of_goods_sold_ytd":986754876674,
"gross_profit_ytd":1421668211918,"operating_profit_ytd":886961114984,
"pretax_profit_ytd":888112383635,"income_tax_ytd":37388595337,
"net_profit_ytd":850723788298,"net_profit_attributable_ytd":618707408600,
"non_controlling_interest_profit_ytd":232016379698,
"cf_before_working_capital_ytd":1887839677708,
"operating_cash_flow_ytd":856209015015,
"investing_cash_flow_ytd":244031897120,
"financing_cash_flow_ytd":-857979656903,
"net_cash_change_ytd":242261255232,
"cash_beginning_reported_ytd":163717707072,
"foreign_exchange_effect_ytd":74334749,
"cash_ending":406053297053,
"capital_expenditure_ytd":-120055037058,
"dividends_paid_ytd":-346534500,
}
for k,amount in original.items(): assert v(q,k)==amount,(k,v(q,k),amount)
c={
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
"ytd_gross":v(q,"revenue_ytd")-v(q,"cost_of_goods_sold_ytd")-v(q,"gross_profit_ytd"),
"ytd_operating":v(q,"gross_profit_ytd")+v(q,"financial_income_ytd")-v(q,"financial_expense_ytd")+v(q,"share_of_profit_in_associates_ytd")-v(q,"admin_expense_ytd")-v(q,"operating_profit_ytd"),
"ytd_other":v(q,"other_income_ytd")-v(q,"other_expense_ytd")-v(q,"other_profit_ytd"),
"ytd_pretax":v(q,"operating_profit_ytd")+v(q,"other_profit_ytd")-v(q,"pretax_profit_ytd"),
"ytd_tax":v(q,"income_tax_current_ytd")+v(q,"income_tax_deferred_ytd")-v(q,"income_tax_ytd"),
"ytd_net":v(q,"pretax_profit_ytd")-v(q,"income_tax_ytd")-v(q,"net_profit_ytd"),
"ytd_owner_split":v(q,"net_profit_attributable_ytd")+v(q,"non_controlling_interest_profit_ytd")-v(q,"net_profit_ytd"),
"b03_before_wc":s(q,"cf_pretax_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investing_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v(q,"cf_before_working_capital_ytd"),
"b03_cfo":s(q,"cf_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_interest_paid_ytd","cf_taxes_paid_ytd","cf_other_paid_ytd")-v(q,"operating_cash_flow_ytd"),
"b03_cfi":s(q,"capital_expenditure_ytd","cf_disposal_proceeds_ytd","cf_loans_issued_ytd","cf_loans_recovered_ytd","cf_equity_recovery_ytd","cf_investment_income_received_ytd")-v(q,"investing_cash_flow_ytd"),
"b03_cff":s(q,"cf_share_proceeds_ytd","cf_share_repurchase_ytd","cf_borrowings_ytd","cf_debt_repayments_ytd","cf_finance_leases_paid_ytd","dividends_paid_ytd")-v(q,"financing_cash_flow_ytd"),
"b03_net":s(q,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v(q,"net_cash_change_ytd"),
"b03_cash_bridge":s(q,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v(q,"cash_ending"),
"b03_B01_cash":v(q,"cash_ending")-v(q,"cash_and_equivalents"),
"same_fy_beginning":v(q,"cash_beginning_reported_ytd")-v(f,"cash_beginning_reported_ytd")
}
assert len(c)==29 and all(x==0 for x in c.values()),c
assert set(c)==set(q["source_validation"]["statement_identity_residuals_vnd"])
assert all(x=="0" for x in q["source_validation"]["statement_identity_residuals_vnd"].values())
assert f["verification_status"]=="issuer_signed_original_visual_verified_B01_B02_B03_FY_and_Q4_standalone_cash"
assert len(f["financial_line_items_extracted_fields"])==103
assert f["source_validation"]["q4_standalone_cashflow_status"]=="verified_FY_12M_minus_Q3_9M_original_source"
expected={
"operating_cash_flow":76675312018,
"investing_cash_flow":-242110753232,
"financing_cash_flow":-154260611123,
"net_cash_change":-319696052337,
"foreign_exchange_effect":7418532,
"capital_expenditure":-288511522757,
"cash_beginning":406053297053
}
for k,amount in expected.items():
    assert v(f,k)==amount,(k,v(f,k),amount)
    if k!="cash_beginning":
        assert v(f,k)==v(f,k+"_ytd")-v(q,k+"_ytd"),k
    else:
        assert v(f,k)==v(q,"cash_ending")
assert v(f,"cash_beginning")+v(f,"net_cash_change")+v(f,"foreign_exchange_effect")==v(f,"cash_ending")
assert v(f,"net_cash_change")==s(f,"operating_cash_flow","investing_cash_flow","financing_cash_flow")
assert all(x=="0" for x in f["source_validation"]["q4_standalone_residuals_vnd"].values())
assert len(f["source_validation"]["q4_B02_12M_minus_9M_vs_original_quarter_residuals_vnd"])==18
assert all(x=="0" for x in f["source_validation"]["q4_B02_12M_minus_9M_vs_original_quarter_residuals_vnd"].values())
assert v(f,"revenue")==v(f,"revenue_ytd")-v(q,"revenue_ytd")
assert v(f,"net_profit")==v(f,"net_profit_ytd")-v(q,"net_profit_ytd")
assert v(f,"net_profit_attributable")==v(f,"net_profit_attributable_ytd")-v(q,"net_profit_attributable_ytd")
print("PASS: GEG Q3 original 96 fields and 29 exact VND B01 B02 9M B03 checks, Q4 FY-minus-9M standalone cash (3 identities) and B02 cross-period 18 checks")
