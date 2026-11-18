#!/usr/bin/env python3
"""Stage only verified production JSON. No overwrite/delete of website UI."""
import json
import pathlib
import shutil
import sys
import zipfile
from validate import check, ARCHIVE, ROOT

def main():
    names = check()
    target = ROOT / "deploy" / "data"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        for name in names:
            dest = target / pathlib.PurePosixPath(name).name
            raw = archive.read(name)
            json.loads(raw.decode("utf-8-sig"))
            dest.write_bytes(raw)
    staged = list(target.glob("*.json"))
    if len(staged) != 41:
        sys.exit(f"Expected 41 staged JSON files, got {len(staged)}")
    print("PASS: staged 41 JSON files. No HTML, CSS, PHP, JS or provisional data staged.")

if __name__ == "__main__":
    main()
