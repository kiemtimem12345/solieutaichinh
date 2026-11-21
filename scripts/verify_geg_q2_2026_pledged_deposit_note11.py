#!/usr/bin/env python3
"""GEG 2026-Q2 restricted deposit accounting source-vintage bridge (exact VND).

Signed GEG 2026-Q2 B09-DN/HN note11 PDF p24 explicitly reclassifies
2026 opening bank guarantees 11,422,218,903 VND as B01 code165 other
current assets; original Q1/2025FY showed the same number among cash
equivalents code112. THIS resolves 2026 year-opening re-presentation, not
the unverified 2026Q1 period-end collateral balance. Q2 standalone
quarter CFO/CFI/CFF MUST stay null until a same-vintage quarter bridge.
"""
from pathlib import Path
from decimal import Decimal
import json
R=Path(__file__).resolve().parents[1]
LEDGER=R/"reports/source-audits/GEG-2026Q2-note11-pledged-cash-opening-reclassification-vnd.json"
FIN=R/"data/financials-GEG.json"
N=Decimal("1000000")

def v(row,key):
    x=row.get(key)
    assert type(x) in (int,float),(key,x)
    y=Decimal(str(x))*N
    assert y==y.to_integral_value()
    return int(y)

def evidence(a):
    b=a["version_facts"]["q1_signed_original"]["year_open_cash_equivalents_vnd"]
    c=a["version_facts"]["q2_signed_original"]["year_open_cash_equivalents_vnd"]
    nn=lambda x: int(x)
    note=a["signed_note11"]
    assert a["symbol"]=="GEG" and a["scope"]=="consolidated" and a["currency"]=="VND"
    assert a["version_facts"]["q1_signed_original"]["sha256"]=="d8dade2f270452432a190bedddb46736523cc3a74b783ae1a2f82b76a5e74d5b"
    assert a["version_facts"]["q2_signed_original"]["sha256"]=="e5c84e9cb42b1698481b12f426544cfad517894d46d3d0f37a1e9e53575f00d5"
    assert a["version_facts"]["q2_signed_original"]["note11_original_PDF_page_1based"]==24
    assert note["at_2026_year_open_vnd"]=="11422218903"
    assert note["at_2026_h1_end_vnd"]=="54079653068"
    assert note["statement_B01_code"]=="165"
    assert b["cash_only"]==c["cash_only"]=="46702358323"
    assert b["current_assets_total"]==c["current_assets_total"]=="1776350024277"
    assert nn(b["cash_only"])+nn(b["cash_equivalents"])==nn(b["cash_total"])
    assert nn(c["cash_only"])+nn(c["cash_equivalents"])==nn(c["cash_total"])
    delta=nn(b["cash_equivalents"])-nn(c["cash_equivalents"])
    assert delta==nn(c["other_current_assets"])-nn(b["other_current_assets"])
    assert delta==nn(b["cash_total"])-nn(c["cash_total"])
    assert delta==nn(c["other_current_asset_pledged_deposit_code165"])==nn(note["at_2026_year_open_vnd"])
    assert nn(b["cash_total"])+nn(b["other_current_assets"])==nn(c["cash_total"])+nn(c["other_current_assets"])
    m=a["reconciliation"]
    x=m["q2_source_YTD_subtraction_provisional_vnd"]
    assert sum(int(x[k]) for k in ("CFO","CFI","CFF"))==int(x["net_cash"])==5905179105
    assert int(x["fx"])==-12574718
    assert int(m["q2_signed_cash_balance_change_vnd"])==-5529614516
    assert int(m["q2_signed_cash_balance_change_vnd"])-int(x["net_cash"])-int(x["fx"])==-delta
    assert m["quarter_cashbridge_unreconciled_without_restatement_vnd"]=="-11422218903"
    assert a["caution"]["same_amount_remained_restricted_at_Mar31_NOT_proven"] is True
    assert a["caution"]["quarter_cash_bridge_with_current_signed_Q1_end_2026_not_zero"] is True
    assert a["caution"]["do_not_fabricate_Q2_standalone_CFO_CFI_CFF"] is True
    return delta

def main():
    source=json.loads(LEDGER.read_text(encoding="utf-8"))
    d=json.loads(FIN.read_text(encoding="utf-8"))
    rows={p:next(x for x in d["items"] if x["period"]==p and "hợp nhất" in x["report_type"].lower())
          for p in ("2026-Q1","2026-Q2")}
    delta=evidence(source)
    q,h=rows["2026-Q1"],rows["2026-Q2"]
    for row in (q,h):
        s=row["source_validation"]
        assert s["year_open_cash_reclassification_original_signed_note_source"]==str(LEDGER.relative_to(R))
        assert s["year_open_cash_reclassification_amount_vnd"]==str(delta)
        assert s["year_open_cash_reclassification_classification_proven"] is True
        assert s["year_open_cash_reclassification_from_B01_code112_cash_equivalents_to_code165_other_current_assets"] is True
        assert s["march_31_2026_restricted_deposits_balance_verified"] is False
        assert s["q2_quarter_cashflow_still_blocked_for_unverified_mar31_reclassification"] is True
        assert s["source_opening_cashflow_b03_reconciled_between_different_vintages"] is False
        assert s["b03_q2_ytd_source_verification_remains_passed"] is True
    assert h["source_validation"]["cash_deposit_collateral_note_pdf_page"]==24
    assert h["source_validation"]["cash_deposit_collateral_year_open_vnd"]=="11422218903"
    assert h["source_validation"]["cash_deposit_collateral_H1_end_vnd"]=="54079653068"
    assert h["source_validation"]["q2_cash_bridge_recomputed_residual_vnd"]=="-11422218903"
    assert h["source_validation"]["q2_cf_standalone_status"]=="source_vintage_opening_classification_identified_but_signed_Q1_end_restatement_unavailable"
    assert q["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_q1_3m_with_cross_vintage_opening_cash_exception"
    assert h["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_h1_ytd_q2_standalone_cash_deferred"
    assert h["cashflow_period_basis"]=="year_to_date"
    for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change",
              "capital_expenditure","dividends_paid","foreign_exchange_effect","cash_beginning"):
        assert h[k] is None,(k,h[k])
    assert v(q,"cash_beginning_reported_ytd")==86364663248
    assert v(h,"cash_beginning_reported_ytd")==74942444345
    assert v(q,"cash_ending")==105856793049
    assert v(h,"cash_ending")==100327178533
    assert v(h,"operating_cash_flow_ytd")==722160976132
    assert v(q,"operating_cash_flow_ytd")==213327143465
    assert v(h,"cash_and_equivalents")==v(h,"cash_ending")
    # Negative proof: tamper the signed note then exact comparative bridge must fail.
    bad=json.loads(json.dumps(source))
    bad["signed_note11"]["at_2026_year_open_vnd"]="11422218904"
    try:evidence(bad)
    except AssertionError:pass
    else:raise AssertionError("The comparison accepted an altered pledged-deposit note")
    bad=json.loads(json.dumps(source))
    bad["version_facts"]["q2_signed_original"]["year_open_cash_equivalents_vnd"]["other_current_assets"]="57156599182"
    try:evidence(bad)
    except AssertionError:pass
    else:raise AssertionError("The comparison accepted a tampered B01 code160")
    print("PASS GEG Q2 2026: signed original 2026Q2 B09 p24 note11 11,422,218,903 VND "
          "collateral deposit B01 code165 exactly equals re-presented year-opening "
          "cash equivalents code112 decrease and other current assets code160 increase; "
          "total current assets identical. Q1 Mar31 reclassification not documented, "
          "Q2 standalone CFO/CFI/CFF must stay BLOCKED; 2 negative tests.")
if __name__=="__main__":main()
