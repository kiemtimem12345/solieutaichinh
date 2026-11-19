#!/usr/bin/env python3
"""Verify the restored public dashboard serves every tracked asset/JSON byte-for-byte.

No SSH credentials, no remote writes, no requests to third-party data providers.
May run immediately after a Hostinger Git deployment (bounded HTTP retries).
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

SITE = "https://solieutaichinh.online"
ALLOWED_HOSTS = {"solieutaichinh.online", "www.solieutaichinh.online"}
RETRIES = (0, 2, 5, 9, 15, 25)  # Auto-deploy and edge caches can lag GitHub main by ~1 min
VERIFY_TOKEN = (os.environ.get("GITHUB_SHA") or "local-verify")[:16]

def validate_checkout():
    snapshots = sorted(Path("data").glob("*.json"))
    financial = [p for p in snapshots if p.name.startswith("financials-")]
    if len(snapshots) != 41 or len(financial) != 32:
        raise ValueError(f"Expected 41 JSON (32 financial); got {len(snapshots)} ({len(financial)} financial)")
    for path in snapshots:
        obj = json.loads(path.read_text(encoding="utf-8"))
        if path.name.startswith("financials-"):
            expected_symbol = path.stem.removeprefix("financials-")
            if obj.get("symbol") != expected_symbol or not isinstance(obj.get("items"), list):
                raise ValueError("Invalid symbol/items in " + path.name)
            rows = obj["items"]
            if len(rows) > 20 or any(str(x.get("period", "")) < "2025-Q1" for x in rows):
                raise ValueError("Period scope violates 2025-Q1 cutoff or 20-period limit: " + path.name)
    js = Path("assets/app.js").read_text(encoding="utf-8")
    if js.find("{ url: 'data/'") == -1 or "kiemtimem123/so-lieu" in js:
        raise ValueError("App JS does not prefer the correct local data source")
    if "payload = await res.json();" not in js:
        raise ValueError("Research library JSON response parsing is missing")
    return snapshots

def check_one(relative_path):
    if relative_path == "/":
        expected = Path("index.html").read_bytes()
        url = SITE + "/"
    else:
        expected = Path(relative_path).read_bytes()
        url = SITE + "/" + quote(relative_path, safe="/")
    digest = sha256(expected).hexdigest()
    errs = []
    for delay in RETRIES:
        if delay:
            time.sleep(delay)
        try:
            req = Request(url + "?verify=" + VERIFY_TOKEN, headers={
                "Accept": "*/*",
                "Accept-Encoding": "identity",
                "Cache-Control": "no-cache",
                "User-Agent": "so-lieu-recovery-healthcheck/1.0",
            })
            with urlopen(req, timeout=18) as response:
                if urlsplit(response.url).hostname not in ALLOWED_HOSTS:
                    raise ValueError("Unexpected cross-origin redirect")
                if response.status != 200:
                    raise ValueError("HTTP " + str(response.status))
                actual = response.read(3_000_000)
                content_type = (response.headers.get("content-type") or "").lower()
                if relative_path.endswith(".json"):
                    if "html" in content_type:
                        raise ValueError("JSON URL returned HTML")
                    json.loads(actual)
                if sha256(actual).hexdigest() != digest:
                    raise ValueError(f"Body SHA-256 differs from tracked Git content ({len(actual)} vs {len(expected)} bytes)")
                return (relative_path, True, "")
        except (HTTPError, URLError, TimeoutError, ValueError, OSError) as exc:
            errs.append(type(exc).__name__ + ":" + str(exc)[:80])
    return (relative_path, False, errs[-1])

def main():
    snapshots = validate_checkout()
    targets = ["/", "index.html", "assets/app.js", "assets/styles.css"] + [
        path.as_posix() for path in snapshots
    ]
    failures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(check_one, name): name for name in targets}
        for f in as_completed(futures):
            name, ok, issue = f.result()
            if not ok:
                failures.append((name, issue))
                print(f"FAIL: {name}: {issue}", flush=True)
    if failures:
        print(f"::error::Production HTTP/SHA256 verification FAILED: {len(failures)}/{len(targets)} checks")
        return 1
    print(f"PASS: {len(targets)}/{len(targets)} HTTPS URLs serve exact tracked Git content (SHA256).")
    print("PASS: original homepage HTML, JS, CSS and all 41 JSON files (32 financial + 9 auxiliary).")
    print("PASS: same-origin data is primary; GitHub fallback repo corrected; <=20 periods from 2025-Q1.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
