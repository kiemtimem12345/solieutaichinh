#!/usr/bin/env python3
"""Stage precisely 41 *current Git-tracked* JSON files for guarded Hostinger FTPS.

The immutable November 18 recovery ZIP is provenance only and must NEVER be
used as the deployment payload after financial snapshots are corrected in Git.
No HTML/JS/CSS or private paths are staged; no remote deletion is done.
Staged bytes must be SHA-256-identical to the source-controlled data/*.json.
"""
import hashlib
import json
from pathlib import Path
import shutil
import sys

try:
    from validate import ROOT, FIRST_ALLOWED, MAX_PERIODS, normalized_financial, check
except ImportError:
    from scripts.validate import ROOT, FIRST_ALLOWED, MAX_PERIODS, normalized_financial, check


def main():
    # Preserve original archive integrity as independent provenance. It does
    # not authorize or supply bytes to the publish staging directory.
    check()

    src = ROOT / "data"
    if not src.is_dir():
        raise ValueError("Missing source-controlled data directory")
    files = sorted(src.glob("*.json"))
    financial = [p for p in files if p.name.startswith("financials-")]
    if len(files) != 41 or len(financial) != 32:
        raise ValueError(
            f"Expected 41 current Git JSON files and 32 financials, "
            f"found {len(files)} and {len(financial)}"
        )

    target = ROOT / "deploy" / "data"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    for path in files:
        if path.parent != src:
            raise ValueError("Nested or non-data source rejected")
        raw = path.read_bytes()
        doc = json.loads(raw.decode("utf-8-sig"))
        if path.name.startswith("financials-"):
            rel = "data/" + path.name
            normalized, excluded = normalized_financial(doc, rel)
            if excluded:
                raise ValueError(
                    f"Current Git financial JSON contains excluded historical rows: {rel}"
                )
            # normalized_financial returns a sorted view for cutoff validation,
            # but staging MUST NOT rewrite source JSON or shuffle report scopes.
            periods = [r["period"] for r in doc["items"]]
            if (
                not periods
                or any(period < FIRST_ALLOWED for period in periods)
                or len(set(periods)) > MAX_PERIODS
            ):
                raise ValueError(f"Out-of-scope report periods in {rel}")
            if normalized.get("symbol") != path.stem.removeprefix("financials-"):
                raise ValueError(f"Ticker mismatch in {rel}")
        staged = target / path.name
        staged.write_bytes(raw)
        if hashlib.sha256(staged.read_bytes()).digest() != hashlib.sha256(raw).digest():
            raise ValueError(f"Staged JSON bytes differ from Git source: {path.name}")

    print(
        "PASS: staged exactly 41 current Git-tracked JSON (32 financial + 9 auxiliary); "
        "all SHA-256 match. Immutable restore ZIP checked but NEVER staged. "
        "No UI, secrets or earlier-period data uploaded."
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, UnicodeError) as exc:
        sys.exit(f"FAIL: safe JSON staging aborted: {exc}")
