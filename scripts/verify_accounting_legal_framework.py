#!/usr/bin/env python3
"""Read-only accounting/legal-quality GATES, not a legal compliance opinion.

Enforce exact VND-source accounting identities against VIX signed 2025 RIÊNG
originals; refuse scope, unit, period basis, EPS, off-B01 client cash, or
unrecorded source-vintage substitutions. Flag 2026 unreviewed periods.
Rules mapped to Luật Kế toán, VAS 01/21/24, TT210/2014/TT-BTC as amended by
TT334/2016, TT99/2025 scoped review, Luật Doanh nghiệp and disclosure law.
"""
import argparse
from decimal import Decimal
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FRAME=ROOT/"reports/accounting-legal-validation-framework.json"
DATA=ROOT/"data/financials-VIX.json"
SOURCE2=ROOT/"reports/source-audits/VIX-2025Q1Q2-original-B01-B02-exact-vnd.json"
CASH2=ROOT/"reports/source-audits/VIX-2025Q1Q2-original-cash-vnd.json"
SOURCE3=ROOT/"reports/source-audits/VIX-2025Q3-original-B01-B02-B03-exact-vnd.json"
SOURCE4=ROOT/"reports/source-audits/VIX-2025Q4-original-B01-B02-B03-exact-vnd.json"
PLX=ROOT/"data/financials-PLX.json"
PLX_SOURCES=ROOT/"reports/source-audits/PLX-2026Q1-B01-cross-source-tolerance.json"
M=Decimal(1000000)
FLOWS=("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","capital_expenditure")
B01_EXTRA={"current_financial_assets","current_other_assets","financial_assets_provision",
           "financial_assets_prepay","financial_services_receivables",
           "financial_other_receivables","financial_receivables_provision",
           "long_term_financial_assets","other_non_current_assets"}

class AccountingSourceError(AssertionError):
    pass

def must(condition,code):
    if not condition:
        raise AccountingSourceError(code)

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def money(row,key):
    val=row.get(key)
    must(type(val) in (int,float),f"VAL_NOT_NUMERIC:{key}")
    d=Decimal(str(val))*M
    must(d==d.to_integral_value(),f"INVALID_VND_PRECISION:{key}")
    return int(d)

def check_policy(p):
    must(p["version"]=="2026-11-21.1","POLICY_VERSION")
    by_id={i["id"]:i for i in p["sources"]}
    must(len(by_id)==len(p["sources"]) and len(by_id)>=8,"POLICY_SOURCE_MISSING")
    must(all(str(x["url"]).startswith("https://") for x in by_id.values()),"POLICY_SOURCE_URL")
    r=p["regimes"]
    must("SEC_ACCOUNT_210" in r["securities_2025"]["special"],"SPECIAL_FORM_2025")
    must("SEC_ACCOUNT_334" in r["securities_2026"]["special"],"SPECIAL_FORM_2026")
    must(r["securities_2025"]["not_general_ttc99"] is True,"2025_VS_2026_REGIME")
    must(r["securities_2026"]["enterprise_99_interaction"]=="NEEDS_FORM_AND_EFFECTIVE_SCOPE_REVIEW","2026_OVERLAY_UNRESOLVED")
    must(Decimal(p["tolerances"]["user_accepted_relative_subtotal_percent"])==Decimal("0.1"),"TOLERANCE_RULE")
    must(p["tolerances"]["never_auto_legal_clearance"] is True,"LEGAL_CERTIFICATION_NOT_AUTOMATIC")
    return by_id

def check_b01(b):
    must(b["total_assets"]==b["total_liabilities"]+b["equity"],"B01_BALANCE")
    must(b["total_assets"]==b["current_assets"]+b["non_current_assets"],"B01_ASSETS")
    must(b["total_liabilities"]==b["current_liabilities"]+b["long_term_liabilities"],"B01_LIABILITIES")
    must(b["current_assets"]==b["current_financial_assets"]+b["current_other_assets"],"B01_CURRENT")
    must(b["non_current_assets"]==b["long_term_financial_assets"]+b["fixed_assets"]+b["other_non_current_assets"],"B01_NONCURRENT")
    assets=("cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets",
            "broker_lending_assets","financial_assets_provision","broker_receivables",
            "financial_assets_prepay","financial_services_receivables",
            "financial_other_receivables","financial_receivables_provision")
    must(sum(b[k] for k in assets)==b["current_financial_assets"],"B01_FINANCIAL_DETAILS")

def check_b02(c):
    must(c["pretax_profit"]-c["income_tax"]==c["net_profit"],"B02_PRETAX_TAX_NET")
    must(c["income_tax"]==c["income_tax_current"]+c["income_tax_deferred"],"B02_TAX_PARTS")
    must(c["broker_total_operating_revenue"]==c["revenue"],"B02_REVENUE")
    must(c["broker_operating_expenses"]==c["broker_total_operating_expenses"],"B02_OPERATING_EXPENSES")
    must(c["broker_net_operating_profit"]==(
         c["revenue"]-c["broker_total_operating_expenses"]
         +c["financial_income"]-c["financial_expense"]-c["admin_expense"]),"B02_OPERATING_PROFIT")
    must(c["pretax_profit"]==c["broker_net_operating_profit"]+c["other_profit"],"B02_OTHER_PROFIT")

def check_b03(m,b):
    must(sum(m[k] for k in FLOWS[:3])==m["net_cash_change"],"B03_CF_CLASSIFICATIONS")
    must(m["cash_beginning"]+m["net_cash_change"]==m["cash_ending"],"B03_CASH_BRIDGE")
    must(m["cash_ending"]==b["cash_and_equivalents"],"B03_B01_CASH")

def main_checks(rows,framework,audit2,cash2,audit3,audit4):
    sources={
        "2025-Q1":{"b01":audit2["sources"]["2025-Q1"]["b01"],
                   "b02":audit2["sources"]["2025-Q1"]["b02"],
                   "b03":cash2["signed_q1_vnd"],
                   "sha":audit2["sources"]["2025-Q1"]["issuer_sha256"],
                   "eps_ytd":audit2["sources"]["2025-Q1"]["eps_ytd"],"eps_quarter":255},
        "2025-Q2":{"b01":audit2["sources"]["2025-Q2"]["b01"],
                   "b02":audit2["sources"]["2025-Q2"]["b02"],
                   "b03":cash2["signed_h1_vnd"],
                   "sha":audit2["sources"]["2025-Q2"]["issuer_sha256"],
                   "eps_ytd":audit2["sources"]["2025-Q2"]["eps_ytd"],"eps_quarter":None},
        "2025-Q3":{"b01":audit3["b01"],"b02":audit3["b02_quarter"],
                   "b03":audit3["b03_9m_ytd"],"sha":audit3["source"]["issuer_sha256"],
                   "eps_ytd":audit3["b02_9m_ytd"]["eps_ytd"],"eps_quarter":None},
        "2025-Q4":{"b01":audit4["b01"],"b02":audit4["b02_q4"],
                   "b03":audit4["b03_original_12m"],"sha":audit4["provenance"]["q4_pdf_sha256"],
                   "eps_ytd":audit4["b02_original_12m"]["eps_ytd"],"eps_quarter":None}
    }
    must(set(rows)==set(framework["baseline_vix"]["completed_separate_2025"]+
                       framework["baseline_vix"]["pending_2026"]),"SCOPE_PERIOD_COUNT")
    prev_quarter_cash=None
    prev_ytd_cf={k:0 for k in FLOWS}
    prev_b02_ytd={k:0 for k in ("revenue","pretax_profit","net_profit")}
    review=[]
    checked=[]
    for period in framework["baseline_vix"]["completed_separate_2025"]:
        row=rows[period]
        src=sources[period]
        b,c,m=src["b01"],src["b02"],src["b03"]
        s=row.get("source_validation",{})
        must(row["period"]==period and row["symbol"]=="VIX","WRONG_TICKER_PERIOD")
        must("riêng" in row["report_type"].lower() and "hợp nhất" not in row["report_type"].lower(),"SEPARATE_VS_CONSOLIDATED")
        must(row["unit"]=="triệu VND","VND_VS_MILLION_UNIT")
        must(row["verification_status"].startswith("issuer_signed_"),"FALSIFIED_SOURCE_PASS")
        must(s.get("source_scope_verified") is True and s.get("source_scope")=="separate","UNVERIFIED_SCOPE")
        must(s.get("full_b01_b02_b03_visual_reviewed") is True,"UNVERIFIED_SCANNED_IMAGES")
        must(s.get("original_issuer_pdf_sha256")==src["sha"],"SOURCE_VINTAGE_HASH")
        must(row.get("cashflow_period_basis")=="quarter","WRONG_B03_QUARTER_PERIOD")
        check_b01(b);check_b02(c);check_b03(m,b)
        for key,exact in b.items():
            if key in B01_EXTRA or key=="client_brokerage_cash_off_balance":
                continue
            must(money(row,key)==exact,f"B01_SOURCE:{period}:{key}")
        for key,exact in c.items():
            must(money(row,key)==exact,f"B02_SOURCE:{period}:{key}")
        must(money(row,"cash_and_equivalents")==b["cash_and_equivalents"],"B01_B03_SOURCE_CASH")
        must(money(row,"client_brokerage_cash_off_balance")==b["client_brokerage_cash_off_balance"],"OFF_BALANCE_CLIENT_VALUE")
        must(row.get("broker_customer_deposits") is None,"CLIENT_DEPOSITS_MIXED_IN_FIRM_B01")
        must(row.get("net_profit_attributable") is None,"SEPARATE_NOT_CONSOLIDATED")
        must(row.get("eps")==src["eps_quarter"] and row.get("eps_ytd")==src["eps_ytd"],"EPS_QUARTER_VS_YTD")
        must(money(row,"cash_beginning")==(
              m["cash_beginning"] if prev_quarter_cash is None else prev_quarter_cash),"CASH_CONTINUITY_VAS24")
        must(money(row,"cash_ending")==m["cash_ending"],"CASH_ENDING_VAS24")
        for key in FLOWS:
            must(money(row,key)==m[key]-prev_ytd_cf[key],f"CASH_QTR_YTD:{period}:{key}")
            must(money(row,key+"_ytd")==m[key],f"CASH_YTD:{period}:{key}")
        must(money(row,"net_cash_change")==sum(money(row,k) for k in FLOWS[:3]),"QUARTER_CFO_CFI_CFF")
        must(money(row,"cash_beginning")+money(row,"net_cash_change")==money(row,"cash_ending"),"QUARTER_CASH_BRIDGE")
        prev_quarter_cash=m["cash_ending"]
        prev_ytd_cf={k:m[k] for k in FLOWS}
        ytd={}
        for key in ("revenue","pretax_profit","net_profit"):
            if period=="2025-Q1":
                actual=c[key]
            elif period=="2025-Q2":
                actual=audit2["sources"]["2025-Q2"]["official_b02_ytd_"+key]
            elif period=="2025-Q3":
                actual=audit3["b02_9m_ytd"][key]
            else:
                actual=audit4["b02_original_12m"][key]
            must(actual==prev_b02_ytd[key]+c[key],f"B02_QTR_YTD:{period}:{key}")
            must(money(row,key+"_ytd")==actual,f"B02_PUBLISHED_YTD:{period}:{key}")
            ytd[key]=actual
        prev_b02_ytd=ytd
        checked.append({"period":period,"scope":"separate","accounting_checks":"PASS_ACCOUNTING_SOURCE_CHECKS",
                        "cash_end_vnd":str(m["cash_ending"]),"signed_source_sha256":src["sha"],
                        "form":"securities_TT210_334",
                        "disclosure_legal_status":"NOT_CERTIFIED_REQUIRE_OFFICIAL_EVIDENCE_REVIEW"})
    for period in framework["baseline_vix"]["pending_2026"]:
        row=rows[period]
        s=row.get("source_validation",{})
        if period=="2026-Q1":
            must(row.get("verification_status")==
                 "issuer_signed_2026Q1_partial_core_B01_B02_B03_verified_FULL_DETAIL_PENDING",
                 "VIX_Q1_2026_NOT_PARTIAL_SOURCE")
            must(s.get("accounting_specialist_form_2026_verified") is True and
                 s.get("core_only_is_not_financial_full_pass") is True,
                 "VIX_Q1_2026_FALSE_FINANCIAL_PASS")
            must(s.get("original_pdf_sha256_pending") is True and
                 s.get("source_signed_pdf_sha256") is None,
                 "VIX_Q1_2026_FALSE_VERIFIED_PDF_HASH")
            must(s.get("source_scope")=="separate" and s.get("source_scope_verified"),
                 "VIX_Q1_2026_WRONG_REPORT_SCOPE")
            form="TT334/2016 B01-CTCK B02-CTCK B03b-CTCK explicitly shown in issuer original"
            missing="full issuer B01/B02/B03 signed detail, PDF binary SHA and legal disclosure evidence"
        else:
            must(row.get("verification_status")=="manual_review_required_pending_extraction",
                 f"UNSUPPORTED_PASS_WITHOUT_ORIGINAL:{period}")
            form="CTCK 2026 special form not yet verified from signed issuer file"
            missing="signed original B01/B02/B03, detailed notes and full legal disclosure evidence"
        must(s.get("full_b01_b02_b03_visual_reviewed") is not True,
             f"2026_PREMATURE_REVIEW_PASS:{period}")
        review.append({"period":period,"financial_source_status":"REVIEW_REQUIRED",
            "legal_regime":form, "missing":missing})
    return checked,review

def crosscheck_plx_tolerance(policy,plx_doc,audit):
    q=next(x for x in plx_doc["items"] if x["period"]=="2026-Q1"
           and "hợp nhất" in x["report_type"].lower())
    s=q["source_validation"]
    must(q["verification_status"]=="signed_original_B01_B02_B03_Q1_2026_PASS_WITH_TOLERANCE_0p1",
         "PLX_SCOPE_TOLERANCE_VINTAGE")
    must(s["b01_tolerance_status"]=="PASS_WITH_TOLERANCE","PLX_TOLERANCE_STATUS")
    must(s["full_b01_component_arithmetic_passed"] is False and
         s["b01_original_subtotal_discrepancies_still_unexplained"] is True,"PLX_SOURCE_DISCREPANCY_NOT_PRESERVED")
    must(s["b01_forensic_issuer_correction_found"] is False,"PLX_FALSE_ISSUER_ERRATUM")
    must(audit["reconciliation"]["exact_original_component_arithmetic_matches"] is False,"PLX_FALSE_EXACT")
    threshold=Decimal(policy["tolerances"]["user_accepted_relative_subtotal_percent"])
    for code in ("130","310"):
        printed=Decimal(audit["issuer"]["values"][code])
        detail=Decimal(audit["reconciliation"]["original_component_sum_vnd"][code])
        diff=printed-detail
        must(diff==Decimal(audit["reconciliation"]["original_residual_vnd"][code]),"PLX_TOL_RESIDUAL")
        must(printed!=0 and Decimal("0.01")<abs(diff)/abs(printed)*100<=threshold,"PLX_TOL_THRESHOLD")
    must(len(audit["secondary"])>=2,"PLX_MULTISOURCE_REQUIRED")
    must(s["b01_secondary_crosschecks_at_display_precision_passed"] is True,
         "PLX_MULTISOURCE_SOURCE_GATE")
    return {"period":"PLX/2026-Q1/consolidated","decision":"PASS_WITH_TOLERANCE",
            "issuer_source_arithmetic":"NOT_EXACT_UNRESOLVED",
            "legal_compliance":"NOT_CERTIFIED"}

def negative_tests(framework,audit2,cash2,audit3,audit4,doc):
    def rejected(fn):
        try:fn()
        except AccountingSourceError:return
        raise AssertionError("Test expected a fail-closed accounting source exception")
    rows={r["period"]:r for r in doc["items"]}
    tampered=json.loads(json.dumps(rows))
    tampered["2025-Q2"]["unit"]="VND"  # old serious error, 1e6 magnitude
    rejected(lambda:main_checks(tampered,framework,audit2,cash2,audit3,audit4))
    tampered=json.loads(json.dumps(rows))
    tampered["2025-Q3"]["operating_cash_flow"]=abs(tampered["2025-Q3"]["operating_cash_flow"])
    rejected(lambda:main_checks(tampered,framework,audit2,cash2,audit3,audit4))
    tampered=json.loads(json.dumps(rows))
    tampered["2025-Q4"]["broker_customer_deposits"]=tampered["2025-Q4"]["client_brokerage_cash_off_balance"]
    rejected(lambda:main_checks(tampered,framework,audit2,cash2,audit3,audit4))
    tampered=json.loads(json.dumps(rows))
    tampered["2026-Q1"]["verification_status"]="PASS_WITH_TOLERANCE"
    rejected(lambda:main_checks(tampered,framework,audit2,cash2,audit3,audit4))
    tampered=json.loads(json.dumps(audit4))
    tampered["b01"]["total_assets"]+=1
    rejected(lambda:(check_b01(tampered["b01"])))
    return 5

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json",action="store_true",help="Emit a JSON report instead of human text")
    args=parser.parse_args()
    policy=read(FRAME)
    check_policy(policy)
    doc=read(DATA)
    must(doc.get("symbol")=="VIX","TICKER")
    must(len(doc["items"])<=20,"PERIOD_STORAGE_MAX20")
    must(all("2025-Q1"<=q["period"]<="2026-Q3" for q in doc["items"]),"OUT_OF_SCOPE_PERIOD")
    rows={x["period"]:x for x in doc["items"]}
    must(len(rows)==len(doc["items"]),"DUPLICATED_PERIOD")
    a2,c2,a3,a4=map(read,(SOURCE2,CASH2,SOURCE3,SOURCE4))
    checked,pending=main_checks(rows,policy,a2,c2,a3,a4)
    plx=crosscheck_plx_tolerance(policy,read(PLX),read(PLX_SOURCES))
    tamper=negative_tests(policy,a2,c2,a3,a4,doc)
    out={"framework_version":policy["version"],
         "financial_checks":{"vix_2025_verified_separate":checked,
                             "vix_2026_pending":pending,
                             "previous_plx_0p1_percent_exception":plx},
         "tamper_fail_closed_tests":tamper,
         "issuer_original_math":"PASS for 2025 signed RIÊNG source and selected PLX preexisting approved exception",
         "legal_or_audit_opinion":"NOT PROVIDED",
         "disclosure_law_compliance":"UNASSESSED: verify official filing dates and corporate documentation"}
    if args.json:print(json.dumps(out,ensure_ascii=False,indent=2))
    else:
        print("PASS ACCOUNTING SOURCE CHECKS: VIX 2025-Q1/Q2/Q3/Q4 exact signed VND "
              "B01+B02+B03; quarter/YTD same source vintage, separate CTCK forms, "
              "cash bridge, EPS, off-B01 client money and 5 negative fail-closed tests.")
        print("PLX 2026-Q1 retains PASS_WITH_TOLERANCE 0.1% with source anomaly visible.")
        print("REVIEW REQUIRED: VIX 2026-Q1/Q2/Q3 source B01/B02/B03, 2026 specialist "
              "regime/TT99 interaction, issuer corporate/legal filing evidence. "
              "No legal certification or audited-opinion assertion.")
if __name__=="__main__":
    main()
