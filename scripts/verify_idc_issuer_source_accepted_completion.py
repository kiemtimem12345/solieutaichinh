#!/usr/bin/env python3
"""IDC issuer-source standardized completion with disclosed TT99/TT43 cash vintage exception.

Only signed source B01/B02 and 3M/6M/9M YTD B03 are source PASS.
Closing the *case* never publishes a standalone 2026-Q2 CFO/CFI/CFF
derived across incompatible reporting vintages. Audited FY2026 recheck.
"""
from decimal import Decimal
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
FIN=ROOT/"data/financials-IDC.json"
LEDGER=ROOT/"reports/source-audits/IDC-2026Q2-issuer-source-accepted-closure-pending-audited-FY2026.json"
NOTE=ROOT/"reports/source-audits/IDC-2026Q1-vs-H1-TT43-source-policy-and-Note41-B03-comparatives.json"
MILLION=Decimal(1000000)
CASH_KEYS=("CFO","CFI","CFF","net","fx","opening","ending")
FIELDMAP={"CFO":"operating_cash_flow_ytd","CFI":"investing_cash_flow_ytd",
          "CFF":"financing_cash_flow_ytd","net":"net_cash_change_ytd",
          "fx":"foreign_exchange_effect_ytd","opening":"cash_beginning_reported_ytd",
          "ending":"cash_ending"}
def load(path):return json.loads(path.read_text(encoding="utf-8"))
def as_int(data,field):return int(data[field])
def from_row(row,field):
    value=row[field]
    assert type(value) in (int,float),(row["period"],field,value)
    amount=Decimal(str(value))*MILLION
    assert amount==amount.to_integral_value(),(field,value)
    return int(amount)
def check_cash(cash):
    assert sum(as_int(cash,k) for k in ("CFO","CFI","CFF"))==as_int(cash,"net")
    assert as_int(cash,"opening")+as_int(cash,"net")+as_int(cash,"fx")==as_int(cash,"ending")

def main():
    data,ledger,note=load(FIN),load(LEDGER),load(NOTE)
    assert data["symbol"]==ledger["ticker"]==note["ticker"]=="IDC"
    assert ledger["case_status"]=="completed_source_accepted_with_disclosed_accounting_vintage_exception_pending_audited_FY2026"
    assert data["ticker_processing_completion"]["status"]=="completed_issuer_source_verified_with_accounting_vintage_exception_pending_audited_fy2026"
    assert data["ticker_processing_completion"]["processing_case_closed_with_qualified_exception"] is True
    assert ledger["case_closure_policy"]["q2_CFO_CFI_CFF_standalone_fields_remain_null"] is True
    assert ledger["annual_followup"]["status"]=="wait_for_official_audited_fy2026_consolidated_issuer_report"
    items=data["items"]
    assert len(items)==7 and len(set(x["period"] for x in items))==7
    q1,q2,q3=[next(x for x in items if x["period"]==period and "hợp nhất" in x["report_type"].lower()) for period in ("2026-Q1","2026-Q2","2026-Q3")]
    assert q1["unit"]==q2["unit"]==q3["unit"]=="triệu VND"
    assert q2["cashflow_period_basis"]=="year_to_date"
    assert q2["source_validation"]["case_closure_status"]=="completed_issuer_source_accepted_with_disclosed_TT99_TT43_comparability_exception"
    assert q2["source_validation"]["case_closure_evidence"]==str(LEDGER.relative_to(ROOT))
    assert q2["source_validation"]["IDC_Q2_2026_standalone_cashflow_promotion_blocked_current_basis"] is True
    assert q2["source_validation"]["issuer_Q1_2026_signed_restated_TT43_B03_not_yet_recovered"] is True
    assert q2["source_validation"]["closure_policy_no_regular_reprocessing"] is True
    for key in ("operating_cash_flow","investing_cash_flow","financing_cash_flow",
                "net_cash_change","cash_beginning","foreign_exchange_effect",
                "capital_expenditure","dividends_paid"):
        assert q2[key] is None,(key,q2[key])
    for rowname,row in (("q1_original_3m",q1),("q2_issuer_original_6m",q2),("q3_issuer_original_9m",q3)):
        src=ledger["source_statements_vnd"][rowname]
        check_cash(src)
        for key,field in FIELDMAP.items():
            assert from_row(row,field)==as_int(src,key),(rowname,key)
    assert q1["source_url"]==note["Q1_original"]["url"]
    assert q2["source_validation"]["issuer_pdf_sha256"]==ledger["source_basis"]["q2_original"]["sha256_pdf"]
    assert ledger["source_basis"]["q1_signed_original"]["sha256"]==note["Q1_original"]["sha256"]
    assert ledger["source_basis"]["h1_reviewed"]["sha256"]==note["H1_reviewed"]["sha256"]
    assert ledger["source_basis"]["q3_original"]["sha256"]==q3["source_validation"]["issuer_pdf_sha256"]
    prior=ledger["signed_note41_2025_prior_comparative"]
    assert as_int(prior,"opening_cash_balance_adjustment_vnd")==890796892
    assert sum(int(x) for x in prior["five_2025_prior_B03_line_reclasses_vnd"].values())==0
    assert prior["sum_2025_prior_B03_reclass_vnd"]=="0"
    assert ledger["q2_quarter_cash_bridge_cross_vintage"]["mixed_Q1_to_Q2_cash_residual_vnd"]=="-890796892"
    assert ledger["q2_quarter_cash_bridge_cross_vintage"]["separate_opening_noncash_reclassification_vnd"]=="890796892"
    assert ledger["q2_quarter_cash_bridge_cross_vintage"]["arithmetic_adjusted_residual_vnd"]=="0"
    qa=ledger["source_statements_vnd"]["q2_cross_vintage_arithmetic_only_NOT_PUBLISHED"]
    for key in ("CFO","CFI","CFF","net","fx"):
        derived=as_int(ledger["source_statements_vnd"]["q2_issuer_original_6m"],key)-as_int(ledger["source_statements_vnd"]["q1_original_3m"],key)
        assert derived==as_int(qa,key),(key,derived)
    assert as_int(qa,"CFO")+as_int(qa,"CFI")+as_int(qa,"CFF")==as_int(qa,"net")
    bridge=(as_int(ledger["source_statements_vnd"]["q2_issuer_original_6m"],"ending")
            -as_int(qa,"opening_Q1_as_filed")-as_int(qa,"net")-as_int(qa,"fx"))
    assert bridge==890796892
    # Different-sign residual convention: note ledger uses original Q1 opening plus
    # Q2 provisional flow minus H1 end, namely -890796892.
    assert -bridge==as_int(ledger["q2_quarter_cash_bridge_cross_vintage"],"mixed_Q1_to_Q2_cash_residual_vnd")
    assert as_int(qa,"opening_Q1_as_filed")+as_int(qa,"net")+as_int(qa,"fx")+bridge==as_int(ledger["source_statements_vnd"]["q2_issuer_original_6m"],"ending")
    a=ledger["source_statements_vnd"]["q3_issuer_original_9m"]
    b=ledger["source_statements_vnd"]["q2_issuer_original_6m"]
    q=ledger["source_statements_vnd"]["q3_issuer_derived_standalone_pass"]
    check_cash(q)
    for k in ("CFO","CFI","CFF","net","fx"):
        assert as_int(a,k)-as_int(b,k)==as_int(q,k)
    assert as_int(b,"ending")==as_int(q,"opening")
    for k,field in (("CFO","operating_cash_flow"),("CFI","investing_cash_flow"),
                    ("CFF","financing_cash_flow"),("net","net_cash_change"),
                    ("fx","foreign_exchange_effect"),("opening","cash_beginning")):
        assert from_row(q3,field)==as_int(q,k)
    # Negative proof: an unearned standalone Q2 value must not pass.
    tamper=dict(q2);tamper["operating_cash_flow"]=0
    assert tamper["operating_cash_flow"] is not None and q2["operating_cash_flow"] is None
    assert ledger["case_closure_policy"]["not_an_assertion_of_regulatory_noncompliance"] is True
    assert ledger["case_closure_policy"]["source_only_2026Q2_standalone_B03_not_signed_same_basis"] is True
    print("PASS IDC 7/7 issuer-source periods + qualified-complete closure; Q1 3M/Q2 6M/Q3 9M exact-VND B03,")
    print("  2025 Note41 comparative changes sum zero, 890,796,892 opening reclassification explained,")
    print("  Q3 9M-H1 standalone bridge 0 VND; Q2 standalone CFO/CFI/CFF remain NULL; revisit FY2026 audited.")
if __name__=="__main__":
    main()
