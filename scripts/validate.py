#!/usr/bin/env python3
"""Validate the archived snapshots; keep the immutable ZIP as provenance."""
import json
import pathlib
import re
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "so-lieu-hostinger-restore-2026-11-18-fixed.zip"
FINANCIAL = re.compile(r"data/financials-([A-Z0-9]+)\.json")
PERIOD = re.compile(r"20\d\d-Q[1-4]")
FIRST_ALLOWED = "2025-Q1"
MAX_PERIODS = 20

def normalized_financial(obj, name):
    match = FINANCIAL.fullmatch(name)
    if not match or not isinstance(obj, dict):
        raise ValueError(f"Invalid financial JSON: {name}")
    symbol = match.group(1)
    if obj.get("symbol") != symbol or not isinstance(obj.get("items"), list):
        raise ValueError(f"Invalid symbol/items for {name}")
    periods = set()
    for item in obj["items"]:
        if not isinstance(item, dict):
            raise ValueError(f"Invalid financial period row in {name}")
        period = item.get("period")
        if not isinstance(period, str) or not PERIOD.fullmatch(period):
            raise ValueError(f"Malformed period {period!r} in {name}")
        if period >= FIRST_ALLOWED:
            periods.add(period)
    latest_periods = set(sorted(periods)[-MAX_PERIODS:])
    if not latest_periods:
        raise ValueError(f"No publishable periods after {FIRST_ALLOWED} in {name}")
    # One quarter may legitimately have both parent-only and consolidated
    # report rows. Preserve both; the maximum applies to distinct periods.
    kept = [item for item in obj["items"] if item["period"] in latest_periods]
    kept.sort(key=lambda x: x["period"])
    result = dict(obj)
    result["items"] = kept
    return result, len(obj["items"]) - len(kept)

def check():
    if not ARCHIVE.is_file():
        raise ValueError(f"Missing archive: {ARCHIVE.name}")
    with zipfile.ZipFile(ARCHIVE) as z:
        broken = z.testzip()
        if broken:
            raise ValueError(f"Corrupt ZIP member: {broken}")
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP filenames")
        data = sorted(n for n in names if re.fullmatch(r"data/[^/]+[.]json", n))
        financials = [n for n in data if FINANCIAL.fullmatch(n)]
        other = [n for n in data if n not in financials]
        if len(data) != 41 or len(financials) != 32 or len(other) != 9:
            raise ValueError(f"Expected 32 financial + 9 auxiliary JSON; got {len(financials)} + {len(other)}")
        excluded = 0
        for name in data:
            obj = json.loads(z.read(name).decode("utf-8-sig"))
            if not isinstance(obj, (dict, list)):
                raise ValueError(f"Unexpected JSON root in {name}")
            if name in financials:
                _, count = normalized_financial(obj, name)
                excluded += count
        app = z.read("assets/app.js")
        result = subprocess.run(["node", "--check", "-"], input=app, capture_output=True, check=False)
        if result.returncode:
            raise ValueError(f"Archived JavaScript fails syntax check: {result.stderr.decode(errors='replace')}")
        if b"kiemtimem123/so-lieu" in app:
            print("NOTICE: Archive contains legacy fallback URL; archived JavaScript is NOT deployed.")
    print(f"PASS: 32 financial + 9 auxiliary JSON; exclude {excluded} earlier/extra periods at staging; archive unchanged.")
    return data

if __name__ == "__main__":
    try:
        check()
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, UnicodeError) as exc:
        sys.exit(f"FAIL: {exc}")
