#!/usr/bin/env python3
"""Stage only verified JSON, filtering financial periods before 2025-Q1."""
import json
import pathlib
import shutil
import sys
import zipfile
from validate import check, ARCHIVE, ROOT, FINANCIAL, normalized_financial, FIRST_ALLOWED, MAX_PERIODS

def main():
    names = check()
    target = ROOT / "deploy" / "data"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    excluded = 0
    with zipfile.ZipFile(ARCHIVE) as archive:
        for name in names:
            dest = target / pathlib.PurePosixPath(name).name
            raw = archive.read(name)
            obj = json.loads(raw.decode("utf-8-sig"))
            if FINANCIAL.fullmatch(name):
                obj, count = normalized_financial(obj, name)
                excluded += count
                raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            dest.write_bytes(raw)
    staged = sorted(target.glob("*.json"))
    if len(staged) != 41:
        sys.exit(f"Expected 41 staged JSON files, got {len(staged)}")
    for path in staged:
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        if path.name.startswith("financials-"):
            periods = [row["period"] for row in obj["items"]]
            if not periods or len(periods) > MAX_PERIODS or any(p < FIRST_ALLOWED for p in periods):
                sys.exit(f"Invalid staged periods in {path.name}")
    print(f"PASS: staged 41 JSON; excluded {excluded} pre-2025/excess periods; no UI files staged.")

if __name__ == "__main__":
    main()
