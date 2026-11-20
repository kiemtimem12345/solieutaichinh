#!/usr/bin/env python3
"""PLX 2026 Q2 issuer signed consolidated and H1 reviewed-vintage source QA.

Q2 original signed 30 Jul 2026, PDF 36p SHA 925339... B01 pp2-4,
B02 p5 and H1-YTD B03 pp6-7 scanned, visually read.
Q2 cash quarter = Q2 original 6M minus *same Jan-1 presentation* Q1 signed
3M. KPMG-reviewed H1 signed 28 Aug 2026 PDF 83p is ANOTHER SOURCE VINTAGE,
whose original cash bridge is separately reconciled, not silently merged.
"""
import json
from decimal import Decimal
from pathlib import Path
root=Path(__file__).resolve().parents[1]
D=json.loads((root/"data/financials-PLX.json").read_text("utf-8"))
q1=next(x for x in D["items"] if x["period"]=="2026-Q1" and "hợp nhất" in x["report_type"])
q2=next(x for x in D["items"] if x["period"]=="2026-Q2" and "hợp nhất" in x["report_type"])
s=q2["source_validation"]
groups={}
name=None
for line in (root/"reports/source-audits/PLX-2026Q2-consolidated-signed-original-vnd.txt").read_text(encoding="utf-8").splitlines():
    if line.startswith("# BEGIN "):
        name=line[8:].strip()
        assert name not in groups
        groups[name]={}
        continue
    if line.startswith("# END "):name=None;continue
    if not line or line.startswith("#"):continue
    k,num=line.split()
    assert name in groups and k not in groups[name] and num.lstrip("-").isdigit(),line
    groups[name][k]=int(num)
v=groups["B01_B02_B03_Q2_ISSUER"]
details=groups["B01_Q2_COMPONENTS"]
h=groups["H1_KPMG_REVIEWED_2026"]
assert (len(v),len(details),len(h))==(104,37,10)
assert s["original_source_vnd_fields_count"]==104
assert s["original_B01_detail_vnd_fields_count"]==37
def amount(row,k):
    assert isinstance(row.get(k),(int,float)) and not isinstance(row[k],bool),(row["period"],k)
    n=Decimal(str(row[k]))*1000000
    assert n==n.to_integral_value(),(k,n)
    return int(n)
def val(k):return amount(q2,k)
def previous(k):return amount(q1,k)
def su(obj,*ks):return sum(obj[k] for k in ks)
for k,x in v.items():assert val(k)==x,(k,val(k),x)
checks={
"b01_asset":v["total_assets"]-su(v,"current_assets","non_current_assets"),
"b01_liab+equity":v["total_assets"]-su(v,"total_liabilities","equity"),
"b01_liability_classes":v["total_liabilities"]-su(v,"current_liabilities","long_term_liabilities"),
"b01_current_assets":v["current_assets"]-su(v,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
"b01_noncurrent_assets":v["non_current_assets"]-su(v,"long_term_receivables","fixed_assets","investment_property","long_term_construction_in_progress","long_term_financial_investments","other_non_current_assets"),
"b01_short_investment":v["short_term_investments"]-su(details,"short_invest_trading","short_invest_provision","short_invest_HTM"),
"b01_receivables":v["short_term_receivables"]-su(details,"recv_customer","recv_advances","recv_other","recv_provision","recv_pending"),
"b01_inventory":v["inventory"]-su(details,"inventory_gross","inventory_provision"),
"b01_othercurrent":v["other_current_assets"]-su(details,"other_cur_prepay","other_cur_VAT","other_cur_tax","other_cur_other"),
"b01_cash":v["cash_and_equivalents"]-su(details,"cash_detail","cash_equivalent_detail"),
"b01_fixed":v["fixed_assets"]-su(details,"fixed_tangible","fixed_intangible"),
"b01_longinvest":v["long_term_financial_investments"]-su(details,"long_invest_associates","long_invest_other","long_invest_provision","long_invest_HTM"),
"b01_otherlong":v["other_non_current_assets"]-su(details,"other_long_prepay","other_long_deferredtax","other_long_other"),
"b01_shortliab":v["current_liabilities"]-su(details,"short_liab_suppliers","short_liab_advances","short_liab_dividends","short_liab_taxes","short_liab_employees","short_liab_accrued","short_liab_unearned","short_liab_other","short_liab_borrowings","short_liab_provisions","short_liab_staff_fund","short_liab_stabilization"),
"b02_quarter_revenue":v["gross_revenue"]-su(v,"revenue_deductions","revenue"),
"b02_quarter_gross":v["revenue"]-su(v,"cost_of_goods_sold","gross_profit"),
"b02_quarter_operating":v["gross_profit"]+v["financial_income"]+v["profit_from_associates"]-su(v,"financial_expense","selling_expense","admin_expense","operating_profit"),
"b02_quarter_other":v["other_income"]-su(v,"other_expense","other_profit"),
"b02_quarter_pretax":v["operating_profit"]+v["other_profit"]-v["pretax_profit"],
"b02_quarter_tax":v["income_tax_current"]+v["income_tax_deferred"]-v["income_tax"],
"b02_quarter_net":v["pretax_profit"]-v["income_tax"]-v["net_profit"],
"b02_quarter_split":v["net_profit"]-v["net_profit_attributable"]-v["non_controlling_interest_profit"],
"b02_ytd_revenue":v["gross_revenue_ytd"]-su(v,"revenue_deductions_ytd","revenue_ytd"),
"b02_ytd_gross":v["revenue_ytd"]-su(v,"cost_of_goods_sold_ytd","gross_profit_ytd"),
"b02_ytd_operating":v["gross_profit_ytd"]+v["financial_income_ytd"]+v["profit_from_associates_ytd"]-su(v,"financial_expense_ytd","selling_expense_ytd","admin_expense_ytd","operating_profit_ytd"),
"b02_ytd_other":v["other_income_ytd"]-su(v,"other_expense_ytd","other_profit_ytd"),
"b02_ytd_pretax":v["operating_profit_ytd"]+v["other_profit_ytd"]-v["pretax_profit_ytd"],
"b02_ytd_tax":v["income_tax_current_ytd"]+v["income_tax_deferred_ytd"]-v["income_tax_ytd"],
"b02_ytd_net":v["pretax_profit_ytd"]-v["income_tax_ytd"]-v["net_profit_ytd"],
"b02_ytd_split":v["net_profit_ytd"]-v["net_profit_attributable_ytd"]-v["non_controlling_interest_profit_ytd"],
"b03_pretax":v["cf_pretax_profit_ytd"]-v["pretax_profit_ytd"],
"b03_preWC":su(v,"cf_pretax_profit_ytd","cf_depreciation_ytd","cf_provisions_ytd","cf_fx_revaluation_ytd","cf_investment_gains_ytd","cf_interest_expense_ytd","cf_other_adjustments_ytd")-v["cf_operating_before_working_capital_ytd"],
"b03_cfo":su(v,"cf_operating_before_working_capital_ytd","cf_receivables_ytd","cf_inventory_ytd","cf_payables_ytd","cf_prepaid_ytd","cf_trading_securities_ytd","cf_interest_paid_ytd","cf_income_taxes_paid_ytd","cf_other_operating_receipts_ytd","cf_other_operating_payments_ytd")-v["operating_cash_flow_ytd"],
"b03_cfi":su(v,"capital_expenditure_ytd","cf_fixed_asset_disposal_proceeds_ytd","cf_bank_placements_ytd","cf_bank_placements_recovered_ytd","cf_other_longterm_investment_ytd","cf_other_investment_recovery_ytd","cf_interest_dividends_received_ytd")-v["investing_cash_flow_ytd"],
"b03_cff":su(v,"cf_share_issue_proceeds_ytd","cf_repurchase_shares_ytd","cf_new_borrowings_ytd","cf_borrowing_repayments_ytd","cf_finance_lease_repayments_ytd","dividends_paid_ytd")-v["financing_cash_flow_ytd"],
"b03_net":su(v,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v["net_cash_change_ytd"],
"b03_bridge":su(v,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v["cash_ending"],
"b03_B01cash":v["cash_ending"]-v["cash_and_equivalents"],
"b02_q1plusQ2_net":v["net_profit_ytd"]-v["net_profit"]-previous("net_profit"),
"b02_q1plusQ2_revenue":v["revenue_ytd"]-v["revenue"]-previous("revenue"),
"b02_q1plusQ2_pretax":v["pretax_profit_ytd"]-v["pretax_profit"]-previous("pretax_profit")
}
assert len(checks)==41,len(checks)
assert all(n==0 for n in checks.values()),{k:n for k,n in checks.items() if n}
qkeys=("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure","dividends_paid")
d={k:v[k+"_ytd"]-previous(k+"_ytd") for k in qkeys}
d["cash_beginning"]=previous("cash_ending")
d["cash_ending"]=v["cash_ending"]
for k,n in d.items():assert val(k)==n,(k,val(k),n)
assert d["cash_beginning"]==10034406335760
assert d["cash_ending"]==6323957202057
assert d["operating_cash_flow"]==-8151521210218
assert d["investing_cash_flow"]==4771932657800
assert d["financing_cash_flow"]==-330860581285
assert d["net_cash_change"]==-3710449133703
assert d["foreign_exchange_effect"]==0
assert d["capital_expenditure"]==-591073777428
assert d["dividends_paid"]==-112351369
assert s["original_6M_minus_Q1_cashflow_signed_exact_vnd"]=={k:str(d[k]) for k in qkeys+("cash_beginning",)}
quarter_checks={
"q2_cfo":d["operating_cash_flow"]-v["operating_cash_flow_ytd"]+previous("operating_cash_flow_ytd"),
"q2_cfi":d["investing_cash_flow"]-v["investing_cash_flow_ytd"]+previous("investing_cash_flow_ytd"),
"q2_cff":d["financing_cash_flow"]-v["financing_cash_flow_ytd"]+previous("financing_cash_flow_ytd"),
"q2_net":d["net_cash_change"]-v["net_cash_change_ytd"]+previous("net_cash_change_ytd"),
"q2_fx":d["foreign_exchange_effect"]-v["foreign_exchange_effect_ytd"]+previous("foreign_exchange_effect_ytd"),
"q2_capex":d["capital_expenditure"]-v["capital_expenditure_ytd"]+previous("capital_expenditure_ytd"),
"q2_dividends":d["dividends_paid"]-v["dividends_paid_ytd"]+previous("dividends_paid_ytd"),
"q2_net_components":d["operating_cash_flow"]+d["investing_cash_flow"]+d["financing_cash_flow"]-d["net_cash_change"],
"q2_cash_bridge":d["cash_beginning"]+d["net_cash_change"]+d["foreign_exchange_effect"]-d["cash_ending"]
}
assert len(quarter_checks)==9 and all(n==0 for n in quarter_checks.values())
assert s["original_Q1_Q2_Jan1_opening_cash_matches"] is True
assert v["cash_beginning_reported_ytd"]==previous("cash_beginning_reported_ytd")==7588239730231
diff={
"net_profit_ytd":h["H1_net_profit_ytd"]-v["net_profit_ytd"],
"revenue_ytd":h["H1_revenue_ytd"]-v["revenue_ytd"],
"pretax_ytd":h["H1_pretax_ytd"]-v["pretax_profit_ytd"],
"operating_cash_flow_ytd":h["H1_CFO"]-v["operating_cash_flow_ytd"],
"investing_cash_flow_ytd":h["H1_CFI"]-v["investing_cash_flow_ytd"],
"financing_cash_flow_ytd":h["H1_CFF"]-v["financing_cash_flow_ytd"],
"net_cash_change_ytd":h["H1_net"]-v["net_cash_change_ytd"],
"foreign_exchange_effect_ytd":h["H1_FX"]-v["foreign_exchange_effect_ytd"],
"cash_beginning_ytd":h["H1_begin_cash"]-v["cash_beginning_reported_ytd"],
"cash_ending":h["H1_end_cash"]-v["cash_ending"],
}
assert {k:str(val) for k,val in diff.items()}==s["KPMG_reviewed_H1_minus_original_6M_source_vintage_vnd"]
assert diff["cash_beginning_ytd"]==3192126575
assert diff["cash_ending"]==22023597927
assert diff["net_profit_ytd"]==7523810667
assert diff["revenue_ytd"]==-171838220315
assert h["H1_CFO"]+h["H1_CFI"]+h["H1_CFF"]==h["H1_net"]
assert h["H1_begin_cash"]+h["H1_net"]+h["H1_FX"]==h["H1_end_cash"]
assert s["KPMG_reviewed_H1_financial_data_must_not_be_mixed_for_Q2_cash_quarter"] is True
assert s["original_issuer_signed_pdf_sha256"]=="925339daf7038fe2adf0ac3ac8277246992ebd00011d90cd1a1b82c079940cc6"
assert (s["original_issuer_signed_pdf_bytes"],s["original_issuer_signed_pdf_pages"])==(15936693,36)
assert s["original_recovery_workflow_run"]==44710991488
assert s["original_recovery_artifact_id"]==14617376536
assert s["original_visually_reviewed_pdf_pages"]==[2,3,4,5,6,7]
assert s["KPMG_reviewed_H1_signed_pdf_sha256"]=="e26c0d58e991895d3704c6b2417953b2fd962255af5197a33e24ed944bf3ccd6"
assert s["KPMG_reviewed_H1_signed_pdf_pages"]==83
assert s["original_source_accounting_identity_passes"]==41
assert s["original_source_max_identity_residual_vnd"]==0
assert q2["verification_status"]=="issuer_original_signed_visual_B01_B02_B03_Q2_2026_41_exact_checks_with_reviewed_H1_vintage_difference"
assert q2["financial_line_items_extracted_fields"]==q2["financial_line_items_manually_verified_fields"]
assert len(q2["financial_line_items_extracted_fields"])==112
assert q2["eps"]==2329 and q2["eps_ytd"]==1676
A=Decimal(q1["total_assets"]*1000000)
B=Decimal(v["total_assets"])
E=Decimal(q1["equity"]*1000000)
F=Decimal(v["equity"])
PAT=Decimal(v["net_profit"])
assert round(4*PAT/((A+B)/2)*100,2)==Decimal("12.56")
assert round(4*PAT/((E+F)/2)*100,2)==Decimal("41.97")
assert (q2["roa"],q2["roe"])==(12.56,41.97)
parent=next(x for x in D["items"] if x["period"]=="2026-Q3" and x["source_validation"].get("scope")=="parent_company")
assert parent["source_validation"]["b03_cashflow_discrepancy_vnd"]=="87654015000"
assert parent.get("financing_cash_flow") is None
print("PASS: PLX Q2/2026 signed original 36p, 104 exact source VND fields and 41 zero-VND statements; 9 Q2 standalone cashflow identities from signed Q1 exact. KPMG H1-reviewed signed 83p differs: +22,023,597,927 closing cash and +7,523,810,667 PAT; versions isolated. Parent PLX Q3/2026 CFF source-error still blocked.")
