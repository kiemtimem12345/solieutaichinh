#!/usr/bin/env python3
"""HEAD-only security check. Never download or print contents of private paths."""
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import sys

BASE = "https://solieutaichinh.online"
PRIVATE_PATHS = [
    "/.git/config",
    "/.git/HEAD",
    "/.env",
    "/restore-source/",
    "/restore-stage-ui-20261119/",
]
def main():
    failures=[]
    for path in PRIVATE_PATHS:
        req = Request(BASE + path + "?sec=20261119", method="HEAD",
                      headers={"User-Agent":"so-lieu-privacy-probe/1.0",
                               "Cache-Control":"no-cache"})
        try:
            with urlopen(req, timeout=15) as response:
                status = response.status
                # No response body is read, even on unexpected 200 responses.
        except HTTPError as exc:
            status=exc.code
        except URLError as exc:
            print(f"::error::Cannot verify private path {path}: {type(exc).__name__}")
            failures.append(path)
            continue
        if status in (403, 404, 410):
            print(f"PASS: private path blocked {path} HTTP {status}")
        else:
            print(f"::error::Private path unexpectedly returned HTTP {status}: {path}")
            failures.append(path)
    if failures:
        print(f"::error::Public webroot privacy checks failed: {len(failures)}")
        return 1
    print("PASS: all five private or non-public paths unavailable via public HTTP HEAD.")
    return 0
if __name__=="__main__":
    sys.exit(main())
