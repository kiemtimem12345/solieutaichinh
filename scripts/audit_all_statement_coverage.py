#!/usr/bin/env python3
"""Read-only audit of every published financial JSON, without reprocessing validated data.

Read statement field definitions directly from the original dashboard JS, then
distinguish a numeric stored value from a verified one. Never convert missing to
zero; never merge parent and consolidated reports with the same quarter.
"""
import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
JS = (ROOT / "assets" / "app.js").read_text("utf-8")
START = "2025-Q1"
END = "2026-Q3"
PERIODS = [f"{year}-Q{q}" for year in (2025, 2026) for q in range(1,5) if START <= f"{year}-Q{q}" <= END]
BANKS = set("MBB ACB BID CTG SHB STB TCB TPB VCB VPB".split())
BROKERS = set("HCM SHS SSI TCX VCI VCK VDS VIX VND".split())
CORE = ("total_assets", "total_liabilities", "equity", "revenue", "pretax_profit", "net_profit")


def keys(section):
    return list(dict.fromkeys(re.findall(r"\bkey:\s*'([^']+)'", section)))


def statement_fields():
    begin = JS.index("if (activeStatement === 'income') {")
    end = JS.index("if (activeStatement === 'cashflow')", begin)
    chunk = JS[begin:end]
    bank = chunk[chunk.index("if (activeIndustry === 'banking')"):chunk.index("if (activeIndustry === 'securities')")]
    broker = chunk[chunk.index("if (activeIndustry === 'securities')"):chunk.index("const genericIncomeRows")]
    general = chunk[chunk.index("const genericIncomeRows"):chunk.index("return genericIncomeRows")]
    return {"bank": keys(bank), "broker": keys(broker), "general": keys(general)}


def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def kind(row):
    label = str(row.get("report_type") or "").lower()
    if any(flag in label for flag in ("không ghi nhãn", "chưa xác nhận", "phạm vi chưa", "chờ xác nhận")):
        return "unconfirmed"
    if re.search(r"riêng(?:\s+lẻ|\s+[a-z]|$)|công ty mẹ|cty mẹ|congtyme", label) and "hợp nhất" not in label:
        return "parent"
    if "hợp nhất" in label:
        return "consolidated"
    return "unconfirmed"


def rows_audit():
    manifests = statement_fields()
    results = []
    all_files = sorted(DATA.glob("financials-*.json"))
    if len(all_files) != 32:
        raise ValueError(f"Expected 32 tracked financials-*.json, got {len(all_files)}")
    for path in all_files:
        obj = json.loads(path.read_text("utf-8-sig"))
        ticker = path.stem.removeprefix("financials-").upper()
        if obj.get("symbol") != ticker:
            raise ValueError(f"Ticker mismatch for {path.name}")
        group = "bank" if ticker in BANKS else "broker" if ticker in BROKERS else "general"
        required = manifests[group]
        byperiod = {}
        for row in obj.get("items", []):
            period = str(row.get("period") or "")
            if period not in PERIODS:
                raise ValueError(f"{ticker}: out-of-scope period {period}")
            report_scope = kind(row)
            byperiod.setdefault(period, []).append(row)
        covered = []
        missing = []   # No record at all, not merely no consolidated scope
        unconfirmed = []
        parent_only = []
        no_consolidated = []
        for period in PERIODS:
            records = byperiod.get(period, [])
            consolidated = [r for r in records if kind(r) == "consolidated"]
            if not consolidated:
                no_consolidated.append(period)
                if not records:
                    missing.append(period)
                elif any(kind(r) == "unconfirmed" for r in records):
                    unconfirmed.append(period)
                else:
                    parent_only.append(period)
                continue
            if len(consolidated) > 1:
                raise ValueError(f"{ticker}: multiple consolidated records for {period}")
            row = consolidated[0]
            stored = [k for k in required if is_number(row.get(k))]
            accepted = set(row.get("financial_line_items_manually_verified_fields") or [])
            rejected = set(row.get("financial_line_items_rejected_fields") or [])
            verified = [k for k in stored if k in accepted and k not in rejected]
            gaps = [k for k in required if k not in stored or k in rejected]
            scope_warning = bool(
                row.get("source_validation", {}).get("scope_validation_required") or
                row.get("source_validation", {}).get("manual_review_blocking_automatic_extraction")
            )
            cash_keys = ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow", "net_cash_change")
            quarter_cash_missing = [k for k in cash_keys if not is_number(row.get(k))]
            covered.append({
                "period": period, "raw": len(stored), "verified": len(verified), "expected": len(required),
                "quarter_cash_missing": quarter_cash_missing,
                "missing": gaps, "scope_warning": scope_warning,
                "source_url": row.get("source_url"),
                "verification_status": row.get("verification_status"),
                "detail_status": row.get("financial_line_items_status"),
                "core_missing": [k for k in CORE if not is_number(row.get(k))],
            })
        numerator = sum(x["raw"] for x in covered)
        denominator = len(covered) * len(required)
        results.append({
            "symbol": ticker, "group": group, "periods": len(covered),
            "missing_periods": missing, "no_consolidated_periods": no_consolidated,
            "unconfirmed_scope_periods": unconfirmed, "parent_only_periods": parent_only,
            "sources": sum(bool(x["source_url"]) for x in covered),
            "available": numerator, "possible": denominator,
            "coverage_percent": round(100 * numerator / denominator, 1) if denominator else 0.0,
            "verified": sum(x["verified"] for x in covered), "period_details": covered,
            "unknown_scope_count": sum(kind(r) == "unconfirmed" for rows in byperiod.values() for r in rows),
        })
    return results, manifests


def report(results, manifests):
    ticker_order = ["PLX", "GAS", "VDS", "GEG", "IDC", "MBB"]
    byticker = {item["symbol"]: item for item in results}
    order = ticker_order + sorted(set(byticker) - set(ticker_order))
    full = sum(1 for a in results if len(a["no_consolidated_periods"]) == 0)
    total = sum(a["periods"] for a in results)
    target = len(results) * len(PERIODS)
    absent = sum(len(a["missing_periods"]) for a in results)
    unconfirmed = sum(len(a["unconfirmed_scope_periods"]) for a in results)
    parent_only = sum(len(a["parent_only_periods"]) for a in results)
    if total + absent + unconfirmed + parent_only != target:
        raise ValueError("Audit must classify each symbol-period exactly once")
    lines = [
        "# Kiểm kê độ phủ báo cáo tài chính — Q1/2025 đến Q3/2026",
        "",
        f"Đối tượng: **{len(results)} mã × {len(PERIODS)} kỳ Q1/2025–Q3/2026**, phạm vi **BCTC hợp nhất**.",
        f"Đã nhận diện {total}/{target} cặp mã-kỳ hợp nhất. Phần còn lại gồm: **{absent} hoàn toàn chưa có bản ghi**, "
        f"**{unconfirmed} đã có báo cáo nhưng chưa xác nhận phạm vi**, **{parent_only} chỉ có báo cáo riêng lẻ**. "
        f"{full}/{len(results)} mã có đủ 7 kỳ hợp nhất được nhận diện.",
        "",
        "Độ phủ KQKD bên dưới là **số trường thực sự lưu dạng số trong JSON**; không đồng nghĩa được kiểm chứng. "
        "Ô trắng có thể là chưa trích xuất, N/A theo mẫu báo cáo hoặc đã bị chặn xác minh. "
        "Cột 'xác nhận' chỉ tính trường được đánh dấu xác minh thủ công, không tự suy diễn từ trạng thái toàn báo cáo.",
        "",
        "| Mã | Ngành | Kỳ hợp nhất | Chưa có bản ghi | Phạm vi chưa rõ | Chỉ riêng lẻ | KQKD có giá trị | KQKD xác minh từng dòng |",
        "|---|---|---:|---|---|---|---:|---:|"
    ]
    for symbol in order:
        x = byticker[symbol]
        missing = ", ".join(x["missing_periods"]) or "—"
        unclear = ", ".join(x["unconfirmed_scope_periods"]) or "—"
        parent = ", ".join(x["parent_only_periods"]) or "—"
        lines.append(f"| {symbol} | {x['group']} | {x['periods']}/{len(PERIODS)} | {missing} | {unclear} | {parent} | "
                     f"{x['available']}/{x['possible']} ({x['coverage_percent']}%) | {x['verified']}/{x['possible']} |")
    geg_status = json.loads((DATA / "financials-GEG.json").read_text("utf-8")).get("ticker_processing_completion", {})
    geg_closed = geg_status.get("status") == "completed_issuer_accepted_exception_pending_fy2026_audited_recheck"
    lines.extend([
        "", "## Trạng thái xử lý các trường B03 quý II/2026", "",
        ("GEG đã **đóng theo nguồn doanh nghiệp công bố**, chờ BCTC kiểm toán năm 2026 để kiểm tra lại ngoại lệ." if geg_closed
         else "GEG chưa đóng ngoại lệ trình bày báo cáo."), "",
        "B01/B02 và B03 lũy kế đã xác minh không đồng nghĩa dòng tiền CFO/CFI/CFF quý II đã được kiểm chứng. "
        "Các ô quý II bên dưới phải tiếp tục giữ null khi thiếu chứng cứ cùng cơ sở trình bày.", "",
        "| Mã | Kỳ | Trường B03 quý độc lập chưa có nguồn cùng cơ sở | Tình trạng xử lý |",
        "|---|---|---|---|",
    ])
    q2_reasons = {
        "GEG": "Tiền gửi bảo lãnh 11.422.218.903 VND phân loại lại; chưa xác minh số dư hạn chế 31/03/2026",
        "IDC": "Q1 theo TT99; H1 áp dụng TT43; chưa có B03 Q1/2026 trình bày lại cùng cơ sở",
    }
    for ticker, reason in q2_reasons.items():
        matches = [x for x in byticker[ticker]["period_details"] if x["period"] == "2026-Q2"]
        if not matches:
            raise ValueError(f"{ticker}: consolidated 2026-Q2 missing; cannot assert deferred B03")
        gap = matches[0]["quarter_cash_missing"]
        if not gap:
            raise ValueError(f"{ticker}: Q2 quarterly B03 now populated; revalidate source exception before reporting")
        case_state = ("ĐÃ ĐÓNG THEO NGUỒN GEG — ngoại lệ B03 bảo lưu tới báo cáo kiểm toán năm 2026" if ticker == "GEG" and geg_closed else
                      "CHƯA HOÀN THÀNH — " + reason)
        lines.append(f"| {ticker} | 2026-Q2 | {', '.join(gap)} | {case_state} |")
    lines.extend(["", "## Ưu tiên xử lý tiếp (không làm lại phần đã PASS)", ""])
    for ticker in ticker_order[:-1]:
        if ticker == "GEG" and geg_closed:
            lines.append("- **GEG:** đã hoàn thành theo báo cáo doanh nghiệp; giữ nguyên ngoại lệ B03 quý II và chỉ mở lại khi BCTC kiểm toán năm 2026 hoặc đính chính nguồn phát hành.")
            continue
        x = byticker[ticker]
        details = x["period_details"]
        worst = sorted(details, key=lambda p: (p["raw"]/p["expected"], p["period"]))[:3]
        lines.append(f"- **{ticker}**: chưa có bản ghi {', '.join(x['missing_periods']) or 'không'}; "
                     f"báo cáo khác phạm vi/chưa rõ {len(x['unconfirmed_scope_periods']) + len(x['parent_only_periods'])} kỳ; "
                     f"KQKD thấp nhất: {', '.join(y['period']+' '+str(y['raw'])+'/'+str(y['expected']) for y in worst)}. "
                     "Chỉ cập nhật kỳ/phạm vi có nguồn PDF chính xác.")
    lines.extend(["", "## Nguyên tắc xác minh", "",
       "- Không gộp số riêng lẻ với hợp nhất, không tự coi kỳ chưa có BCTC bằng 0.",
       "- Dữ liệu theo đơn vị gốc (VND, triệu VND hoặc tỷ VND), tỷ lệ chỉ số không chia theo đơn vị tiền.",
       "- Q2 và Q3 B03 là lũy kế: quý riêng phải trừ kỳ lũy kế liền trước cùng phạm vi.",
       "- Sai số **≤0,1%** chỉ cân nhắc với tổng phụ có chứng cứ đối chiếu đa nguồn nhất quán; không áp dụng để bỏ qua sai dấu, kỳ, phạm vi, đơn vị hay sai cầu tiền mặt B03. Lưu chứng cứ PDF/trang.",
       "- Tối đa 20 kỳ, bắt đầu từ Q1/2025; các trường đã được xác minh không trích xuất lại vô cớ.",
       "",
       "## Manifest KQKD đang dùng trên website",
       "",
       " / ".join(f"{group}: {len(fields)} trường" for group, fields in manifests.items()),
       "",
       "Báo cáo chỉ phản ánh dữ liệu đã lưu, không chứng minh sự có/không có của các BCTC tại sở giao dịch.",
       ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    results, manifests = rows_audit()
    md = report(results, manifests)
    if args.write:
        path = ROOT / "reports" / "coverage-audit-2026-11-19.md"
        path.parent.mkdir(exist_ok=True)
        path.write_text(md, encoding="utf-8")
        print("WROTE:", path.relative_to(ROOT))
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
