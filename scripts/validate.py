#!/usr/bin/env python3
"""Validate the archived financial snapshots; never publish the archived UI."""
import json
import pathlib
import re
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "so-lieu-hostinger-restore-2026-11-18-fixed.zip"

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
        financials = [n for n in data if n.startswith("data/financials-")]
        other = [n for n in data if not n.startswith("data/financials-")]
        if len(data) != 41 or len(financials) != 32 or len(other) != 9:
            raise ValueError(f"Expected 32 financial + 9 auxiliary JSON; got {len(financials)} + {len(other)}")
        for name in data:
            obj = json.loads(z.read(name).decode("utf-8-sig"))
            if not isinstance(obj, (dict, list)):
                raise ValueError(f"Unexpected JSON root in {name}")
        app = z.read("assets/app.js")
        result = subprocess.run(["node", "--check", "-"], input=app, capture_output=True, check=False)
        if result.returncode:
            raise ValueError(f"Archived JavaScript fails syntax check: {result.stderr.decode(errors='replace')}")
        if b"kiemtimem123/so-lieu" in app:
            print("NOTICE: Archive contains a legacy GitHub fallback URL. Archived JavaScript is NOT deployed.")
    print("PASS: 32 financial JSON + 9 auxiliary JSON; archived JavaScript syntax valid.")
    return data

if __name__ == "__main__":
    try:
        check()
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, UnicodeError) as exc:
        sys.exit(f"FAIL: {exc}")
