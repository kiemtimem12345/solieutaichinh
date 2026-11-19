#!/usr/bin/env python3
"""GAS issuer visual Q1/Q2 2026: independent source/quarter checks in exact VND.

Both source PDF image sets are reviewed; preserve unverified comparative
restatements as explicit anomalies instead of overwriting validated periods.
"""
import json
from decimal import Decimal
from pathlib import Path

data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-GAS.json").read_text("utf-8"))
q={row["period"]:row for row in data["items"]}
a,b,old=q["2026-Q1"],q["2026-Q2"],q["2025-Q4"]
def v(r,k):
    return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
def s(r,*names): return sum(v(r,k) for k in names)
def ck(r):
    checks={
        "assets":v(r,"total_assets")-s(r,"current_assets","non_current_assets"),
        "balance":v(r,"total_assets")-s(r,"total_liabilities","equity"),
        "liabilities":v(r,"total_liabilities")-s(r,"current_liabilities","long_term_liabilities"),
        "current_assets":v(r,"current_assets")-s(r,"cash_and_equivalents","short_term_investments","short_term_receivables","inventory","other_current_assets"),
        "net_revenue":s(r,"sales_gross")-s(r,"revenue_deductions","revenue"),
        "gross":v(r,"revenue")-s(r,"cost_of_goods_sold","gross_profit"),
        "operating":s(r,"gross_profit","financial_income","share_of_profit_in_associates")-s(r,"financial_expense","selling_expense","admin_expense","operating_profit"),
        "other":s(r,"other_income")-s(r,"other_expense","other_profit"),
        "pretax":s(r,"operating_profit","other_profit")-v(r,"pretax_profit"),
        "tax":v(r,"pretax_profit")-s(r,"income_tax_current","income_tax_deferred","net_profit"),
        "attributable":s(r,"net_profit_attributable","non_controlling_interest_profit")-v(r,"net_profit"),
        "cf_sections":s(r,"operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd")-v(r,"net_cash_change_ytd"),
        "cf_bridge":s(r,"cash_beginning_reported_ytd","net_cash_change_ytd","foreign_exchange_effect_ytd")-v(r,"cash_ending"),
        "cf_equals_B01":v(r,"cash_and_equivalents")-v(r,"cash_ending"),
        "cf_pretax_adjustments":s(r,"cf_pretax","cf_depreciation","cf_provisions","cf_fx_revaluation","cf_investment_gains","cf_interest_expense")-v(r,"cash_operating_before_wc"),
        "cf_wc":s(r,"cash_operating_before_wc","cf_receivables","cf_inventory","cf_payables","cf_prepaid","cf_interest_paid","cf_taxes_paid","cf_other_receipts","cf_other_payments")-v(r,"operating_cash_flow_ytd"),
        "cf_investing":s(r,"capital_expenditure_ytd","cf_loans_issued","cf_loans_recovered","cf_interest_dividends_received")+(v(r,"cf_investment_recovery") if r is a else v(r,"cf_asset_disposal"))-v(r,"investing_cash_flow_ytd"),
        "cf_financing":s(r,"cf_borrowing_proceeds","cf_borrowing_repayments")+(v(r,"dividends_paid_ytd") if r is b else 0)-v(r,"financing_cash_flow_ytd"),
    }
    assert len(checks)==18 and all(value==0 for value in checks.values()), checks
    assert all(value=="0" for value in r["source_validation"]["statement_identity_residuals_vnd"].values())
    assert set(checks)==set(r["source_validation"]["statement_identity_residuals_vnd"])
    return checks

assert a["unit"]==b["unit"]=="triệu VND"
assert a["eps"]==1220 and b["eps"]==2385
assert a["roa"] is None and b["roa"] is None and a["roe"] is None and b["roe"] is None
assert a["verification_status"]==b["verification_status"]=="issuer_original_pdf_visual_verified_b01_b02_b03_with_cross_report_anomalies_flagged"
for r,pages,sha,n_fields in (
    (a,[4,5,6,7],"853ad22dfe045d2477d9e027fa3d161a9eb2bed37c2a37bec8942fa815008deb",49),
    (b,[3,4,5,6],"118f3b092ddce271d87051734c4c789d18b82a65dc7ace39ce83beedeea46e56",50)):
    assert r["source_validation"]["manually_visual_reviewed"] is True
    assert r["source_validation"]["reviewed_pages"]==pages
    assert r["source_validation"]["issuer_pdf_sha256"]==sha
    assert r["source_validation"]["unresolved_comparative_presentation_differences"] is True
    assert len(r["financial_line_items_manually_verified_fields"])==n_fields
    assert set(r["financial_line_items_extracted_fields"])==set(r["financial_line_items_manually_verified_fields"])
    ck(r)

expected={
    "2026-Q1":{"total_assets":92923423491919,"total_liabilities":22333645606660,"equity":70589777885259,
        "revenue":38019609031268,"pretax_profit":3754683655851,"net_profit":2994115272577,
        "operating_cash_flow_ytd":-468939629618,"investing_cash_flow_ytd":599484606752,
        "financing_cash_flow_ytd":314542385295,"cash_ending":7321907295672},
    "2026-Q2":{"total_assets":102869897500506,"total_liabilities":32615256063103,"equity":70254641437403,
        "revenue":43249135951689,"pretax_profit":7443056154493,"net_profit":6021399337485,
        "operating_cash_flow_ytd":7038604357979,"investing_cash_flow_ytd":-2828965984641,
        "financing_cash_flow_ytd":-42216621345,"cash_ending":11055638145352},
}
for period,vals in expected.items():
    for k,raw in vals.items(): assert v(q[period],k)==raw,(period,k,v(q[period],k),raw)

for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","foreign_exchange_effect","capital_expenditure"):
    assert v(a,k)==v(a,k+"_ytd")
    assert v(b,k)==v(b,k+"_ytd")-v(a,k+"_ytd"),k
assert v(a,"cash_beginning")==v(a,"cash_beginning_reported_ytd")
assert v(b,"cash_beginning")==v(a,"cash_ending")
assert s(b,"cash_beginning","net_cash_change","foreign_exchange_effect")==v(b,"cash_ending")

# The original figures are contradictory across statements; deliberately flag and retain.
assert v(old,"total_assets")==93531511866676
assert 93568198109790-v(old,"total_assets")==36686243114
assert v(a,"cash_beginning_reported_ytd")-v(old,"cash_ending")==-15534247
h1={"revenue":81268744982957,"cost_of_goods_sold":68967158848778,
    "gross_profit":12301586134179,"pretax_profit":11207899960622,
    "net_profit":9025674760340,"net_profit_attributable":8804699596334}
deltas={k:v(a,k)+v(b,k)-val for k,val in h1.items()}
assert deltas=={"revenue":0,"cost_of_goods_sold":10160150278,
    "gross_profit":-10160150278,"pretax_profit":-10160150278,
    "net_profit":-10160150278,"net_profit_attributable":-10160150278}
assert v(b,"cf_pretax")-h1["pretax_profit"]==11034262367
assert "dividends_paid" not in a and "dividends_paid" not in b
print("PASS: GAS 2026 Q1/Q2 36 source-image exact VND identities, 99 fields, Q2 YTD-minus-Q1 B03; flagged 36,686,243,114 / 10,160,150,278 / 11,034,262,367 VND anomalies")
