#!/usr/bin/env python3
"""Read-only public HTTP audit to find live recoverable frontend assets.

Only print URLs/status/content type/size and resource paths. Never use credentials or perform writes.
"""
import urllib.request, urllib.error, re, hashlib, socket
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit
URLS = [
 "https://solieutaichinh.online/",
 "https://www.solieutaichinh.online/",
 "https://solieutaichinh.online/index.html",
 "https://www.solieutaichinh.online/index.html",
 "https://www.solieutaichinh.online/assets/app.js",
 "https://solieutaichinh.online/data/category-data.json",
]
class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        url=a.get("src") if tag in ("script","img") else a.get("href") if tag=="link" else None
        if url and not url.startswith(("data:","javascript:")):
            self.items.append(url)
def check(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; SiteRecoveryAudit/1.0)","Accept":"text/html,application/json,*/*"})
    try:
        with urllib.request.urlopen(req,timeout=16) as r:
            body=r.read(3_000_000)
            typ=r.headers.get("content-type","")
            print(f"HTTP {url}: status={r.status}, final={r.url}, type={typ.split(';')[0]}, bytes_sampled={len(body)}, sha256={hashlib.sha256(body).hexdigest()[:14]}")
            if "text/html" in typ and url.endswith(("/", "index.html")):
                parser=Assets()
                parser.feed(body.decode("utf-8","replace"))
                title=re.search(r"<title[^>]*>(.*?)</title",body.decode("utf-8","replace"),re.I|re.S)
                if title: print("TITLE: "+re.sub(r"\s+"," ",title.group(1))[:130])
                for asset in sorted(set(parser.items))[:50]:
                    u=urljoin(r.url,asset)
                    if urlsplit(u).hostname in ("solieutaichinh.online","www.solieutaichinh.online"):
                        print("SAME_ORIGIN_ASSET: "+u[:240])
                print("HTML_ASSET_COUNT: "+str(len(parser.items)))
    except urllib.error.HTTPError as e:
        print(f"HTTP {url}: status={e.code}, type={e.headers.get('content-type','')}")
    except Exception as e:
        print(f"HTTP {url}: ERROR={type(e).__name__} ({str(e)[:120]})")
for u in URLS:
    check(u)
