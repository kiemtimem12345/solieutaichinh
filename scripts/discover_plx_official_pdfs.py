#!/usr/bin/env python3
"""Find PLX (not subsidiary) Q3 2026 and H1 reviewed PDF links on issuer IR pages.

Read-only HTTP; never scrape passwords, download report bodies, or persist a PDF
in Git. URLs are only printed if the host is the public official Petrolimex
file service. Bounded network requests, limited pages/links.
"""
import html
from html.parser import HTMLParser
import re
import socket
from urllib.parse import urljoin, urlparse, unquote
from urllib.request import Request, urlopen

ISSUER_SITES = [
    "https://plx.petrolimex.com.vn/quan-he-nha-dau-tu.html",
    "https://egat.petrolimex.com.vn/quan-he-nha-dau-tu.html",
    "https://qlpns.petrolimex.com.vn/quan-he-nha-dau-tu.html",
    "https://e.petrolimex.com.vn/quan-he-nha-dau-tu.html",
    "https://w.petrolimex.com.vn/quan-he-nha-dau-tu.html",
]
LABEL_TERMS = ("quý 3 năm 2026", "quý 3/2026", "quý iii/2026",
               "6 tháng năm 2026", "quý 2 năm 2026", "quý 2/2026")
ALLOWED_DOMAINS = {"files.petrolimex.com.vn", "staticfile.hsx.vn"}
class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.current=None
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d=dict(attrs)
            self.current={"href":d.get("href",""),"text":[],"title":d.get("title","")}
    def handle_data(self, data):
        if self.current is not None:
            self.current["text"].append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.current is not None:
            self.links.append(self.current)
            self.current=None

def valid_official_url(u):
    return urlparse(u).scheme == "https" and urlparse(u).hostname in ALLOWED_DOMAINS

def main():
    found=set()
    scanned=0
    for site in ISSUER_SITES:
        try:
            req=Request(site, headers={"User-Agent":"Mozilla/5.0 (compatible; PDFSourceDiscovery/1.0)"})
            with urlopen(req,timeout=16) as response:
                raw=response.read(2_000_000)
                final=response.url
            body=raw.decode("utf-8","replace")
            parser=Reader()
            parser.feed(body)
            scanned+=1
            print(f"PAGE: issuer_IR host={urlparse(final).hostname}, bytes={len(raw)}, anchors={len(parser.links)}")
            match_count=0
            for item in parser.links:
                label=html.unescape(" ".join(item["text"]) + " " + item["title"]).lower()
                link=urljoin(final,item["href"])
                if not any(q in label for q in LABEL_TERMS):
                    continue
                if valid_official_url(link):
                    key=(label[:140].strip(),link)
                    if key in found:continue
                    found.add(key)
                    print("OFFICIAL_PDF_CANDIDATE: "+key[0]+" | "+link)
                    match_count+=1
            # On some issuer pages the link is in an image or an onclick
            # element rather than the anchor. Report only status, no guessing.
            if match_count==0:
                print("NO_DIRECT_PDF_LINK_FOR_TARGET_LABELS:",urlparse(final).hostname)
        except Exception as exc:
            print(f"PAGE_UNAVAILABLE: {urlparse(site).hostname}; reason={type(exc).__name__}")
    print(f"SUMMARY: scanned={scanned}/{len(ISSUER_SITES)} issuer mirrors, matched distinct official PDFs={len(found)}")
    if not found:
        print("RESULT: needs alternate official HOSE disclosure retrieval; do not invent a PDF URL")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
