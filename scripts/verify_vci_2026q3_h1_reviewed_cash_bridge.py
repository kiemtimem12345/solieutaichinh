#!/usr/bin/env python3
"""VCI exact-VND 2026 Q3 quarter B03: visual Q2 as-filed / PwC reviewed H1 against signed 9M.

No OCR numbers; no invented Q2-only cash, no client-custody cash.
"""
from decimal import Decimal
from pathlib import Path
import copy
import json

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/VCI-2026Q3-reviewed-H1-signed-Q2-quarter-cash-vnd.json"
SIGNED = ROOT / "reports/source-audits/VCI-2026Q3-issuer-HOSE-original-special-broker-no-subs-vnd.json"
FIN = ROOT / "data/financials-VCI.json"
FIELDS = ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow",
          "net_cash_change", "cash_beginning", "cash_ending")
FLOW = FIELDS[:4]
MILLION = Decimal("1000000")

def read(p):
    return json.loads(p.read_text(encoding="utf-8"))

def cash_check(rows):
    c = {k: int(rows[k]) for k in FIELDS}
    assert c["operating_cash_flow"]+c["investing_cash_flow"]+c["financing_cash_flow"]==c["net_cash_change"], c
    assert c["cash_beginning"]+c["net_cash_change"]==c["cash_ending"], c
    return c

def verify(ledger, source, data):
    assert ledger["ticker"] == source["ticker"] == data["symbol"] == "VCI"
    assert ledger["scope"].startswith("single issuer company financial reports with no subsidiaries")
    h1src, q2src = ledger["h1_reviewed_source"], ledger["q2_as_filed_source"]
    assert h1src["mirror_sha256"] == "1ea814d02563a136d11d718c62c1ffc3c08463ffaf12369c517111cd26f6b9af"
    assert q2src["mirror_sha256"] == "a8fec422bac195c1b4d9743a995da35ec5066fa6dc0f951e6fbb36f2218823b5"
    assert h1src["pages"] == 98 and h1src["visual_pdf_pages"] == [16, 17]
    assert q2src["pages"] == 48 and q2src["visual_pdf_pages"] == [13, 14]
    assert h1src["source_text_searchable"] is False and q2src["source_text_searchable"] is False
    assert ledger["source_review"]["artifact_id"] == 14712970890
    assert ledger["source_review"]["render_method"].startswith("pdftoppm JPEG")
    h1 = cash_check(h1src["cashflow_vnd"])
    q2_signed = cash_check(q2src["cashflow_vnd"])
    assert h1 == q2_signed, "Q2 original differs from reviewed H1 6M cash: vintage mismatch"
    src9m = source["original_vnd_fields"]
    nine = {k:int(src9m[k+"_ytd"]) for k in FLOW}
    nine["cash_beginning"] = int(src9m["cash_beginning_reported_ytd"])
    nine["cash_ending"] = int(src9m["cash_ending"])
    assert cash_check({k:str(v) for k,v in nine.items()}) == nine
    assert ledger["q3_signed_9m_source"]["cashflow_vnd"] == {k:str(v) for k,v in nine.items()}
    q3 = {k:nine[k]-h1[k] for k in FLOW}
    q3["cash_beginning"],q3["cash_ending"] = h1["cash_ending"],nine["cash_ending"]
    cash_check({k:str(v) for k,v in q3.items()})
    assert {k:int(v) for k,v in ledger["quarter_2026q3_derived_vnd"].items()} == q3
    rows = {r["period"]:r for r in data["items"]}
    assert len(rows)==7 and len(data["items"])==7
    row = rows["2026-Q3"]
    assert row["cashflow_period_basis"] == "year_to_date"
    assert row["q3_standalone_cashflow_status"] == "verified_signed_9M_less_reviewed_H1_exact_VND_bridge"
    assert row["cashflow_quarter_basis"] == "signed_2026_9M_minus_reviewed_signed_H1_6M"
    assert row["source_validation"]["cashflow_q3_standalone_reviewed_h1_q2_source_ledger"] == str(LEDGER.relative_to(ROOT))
    assert row["source_validation"]["q3_quarter_cashflow_exact_vnd_bridge_residual"] == "0"
    assert row["source_validation"]["h1_vs_q2_same_6m_cashflow_exact_match"] is True
    assert row["source_validation"]["source_is_not_an_explicit_consolidated_report"] is True
    assert row["source_validation"]["screenshot_b03_full_page_not_verified"] is True
    assert row["source_validation"]["original_pdf_hash_verified"] is False
    assert row["source_validation"]["client_cash_outside_company_B01_verified"] is True
    assert set(row["cashflow_quarter_manually_verified_fields"]) == set(FIELDS)
    for k, v in q3.items():
        assert type(row.get(k)) in (int, float), (k,row.get(k))
        actual = Decimal(str(row[k])) * MILLION
        assert actual == Decimal(v),(k,actual,v)
    # Historical Q2 source quarantine can now be lifted only after signed Q1
    # was independently verified and the six-month-minus-Q1 cash bridge passed.
    q2_row = rows["2026-Q2"]
    new_q2_ledger_path = ROOT / "reports/source-audits/VCI-2026Q2-original-reviewed-H1-and-Q1-cash-bridge-vnd.json"
    new_q2_ledger = read(new_q2_ledger_path)
    assert q2_row["q2_standalone_cashflow_status"] == "signed_original_H1_minus_signed_Q1_exact_VND_zero_residual"
    assert q2_row["source_validation"]["source_audit_ledger"] == str(new_q2_ledger_path.relative_to(ROOT))
    assert q2_row["source_validation"]["signed_q2_H1_six_month_B03_vs_reviewed_6M_exact_match"] is True
    assert q2_row["source_validation"]["q2_quarter_cash_bridge_residual_vnd"] == "0"
    assert new_q2_ledger["reviewed_H1_PwC"]["sha256"] == h1src["mirror_sha256"]
    assert new_q2_ledger["as_filed_Q2"]["sha256"] == q2src["mirror_sha256"]
    q2 = {k:int(v) for k,v in new_q2_ledger["standalone_2026q2_cashflow_vnd"].items()}
    cash_check({k:str(v) for k,v in q2.items()})
    assert q2["cash_ending"] == h1["cash_ending"]
    assert q2["cash_beginning"] + q2["net_cash_change"] == h1["cash_ending"]
    for k in FIELDS:
        actual=Decimal(str(q2_row[k]))*MILLION
        assert actual==Decimal(q2[k]),(k,actual,q2[k])
    # Custody cash must not substitute for issuer cash.
    assert int(src9m["client_brokerage_cash_ending_ytd"]) != q3["cash_ending"]
    assert "Công ty không có công ty con" == source["signed_no_subsidiaries_note"]
    return q3

def main():
    ledger, source, data = read(LEDGER),read(SIGNED),read(FIN)
    q3=verify(ledger,source,data)
    # Fail-closed controls: an off-by-1 VND source, an invalid quarter, or client cash substitution fails.
    for bad_case in ("h1_end", "q3_signed_net", "website_cash"):
        a,b,c=copy.deepcopy(ledger),copy.deepcopy(source),copy.deepcopy(data)
        if bad_case=="h1_end":
            a["h1_reviewed_source"]["cashflow_vnd"]["cash_ending"]=str(int(a["h1_reviewed_source"]["cashflow_vnd"]["cash_ending"])+1)
        elif bad_case=="q3_signed_net":
            b["original_vnd_fields"]["net_cash_change_ytd"]=str(int(b["original_vnd_fields"]["net_cash_change_ytd"])+1)
        else:
            next(r for r in c["items"] if r["period"]=="2026-Q3")["cash_ending"]=Decimal("999")
        try: verify(a,b,c)
        except (AssertionError,TypeError,ValueError): pass
        else: raise AssertionError("corruption passed: "+bad_case)
    print("PASS VCI Q3 2026 signed 9M minus Q2-as-filed/PwC-reviewed H1 exact-VND cashflow,")
    print("  Q3 CFO/CFI/CFF/net:",*[str(q3[k]) for k in FLOW])
    print("  quarter cash beginning/end:",q3["cash_beginning"],q3["cash_ending"])
    print("  2 source 6M variants exact equal, 4 bridges, 3 corruption controls, Q2 standalone separately source-verified with Q1 bridge.")
if __name__=="__main__":
    main()
