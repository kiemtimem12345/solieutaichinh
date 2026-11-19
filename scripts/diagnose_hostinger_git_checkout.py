#!/usr/bin/env python3
"""Read-only audit: is public_html an auto-updated Git repository checkout?

Never print raw .git/config, origin URLs, userinfo, access tokens or private
contents. Only print whether origin matches known public repository.
"""
import base64, hashlib, os, socket, stat, sys, datetime, re
import paramiko
USER="u154814653"
ROOT="/home/u154814653/domains/solieutaichinh.online/public_html"
FP="SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
KNOWN={"README-SFTP.md","scripts",".github","CNAME",
       "so-lieu-hostinger-restore-2026-11-18-fixed.zip",
       "PROJECT-CHECKPOINT-2026-11-18-2335-sftp-data-restored-ui-pending.md"}
def fingerprint(k):
    return "SHA256:"+base64.b64encode(hashlib.sha256(k.asbytes()).digest()).decode().rstrip("=")
def read_small(sftp,path,limit=65536):
    st=sftp.lstat(path)
    if not stat.S_ISREG(st.st_mode) or st.st_size>limit:return None
    with sftp.open(path,"rb") as r:return r.read(limit).decode("utf-8","replace")
def main():
    if os.environ.get("SFTP_USERNAME")!=USER or not os.environ.get("SFTP_PASSWORD"):
        print("::error::SSH secrets missing");return 2
    t=s=None
    try:
        sock=socket.create_connection(("195.35.62.53",65002),12)
        t=paramiko.Transport(sock);t.get_security_options().key_types=("ssh-ed25519",)
        t.start_client(timeout=15);key=t.get_remote_server_key()
        if key.get_name()!="ssh-ed25519" or fingerprint(key)!=FP:
            print("::error::SSH host key mismatch");return 2
        t.auth_password(USER,os.environ["SFTP_PASSWORD"],fallback=False)
        if not t.is_authenticated():print("::error::SSH auth failed");return 2
        s=paramiko.SFTPClient.from_transport(t)
        names={i.filename:i for i in s.listdir_attr(ROOT)}
        print("PASS: read-only webroot diagnostic", "entry_count=",len(names))
        print("PUBLIC_ROOT_GIT_DIR:",".git" in names and stat.S_ISDIR(names[".git"].st_mode))
        print("MATCHES_REPO_TOPLEVEL_FILES:",len(KNOWN.intersection(names)),"/",len(KNOWN))
        for name in sorted(KNOWN.intersection(names)):
            item=names[name]
            print("MATCH:",name,"type=","DIR" if stat.S_ISDIR(item.st_mode) else "FILE",
                  "mtime_utc=",datetime.datetime.fromtimestamp(item.st_mtime,datetime.timezone.utc).isoformat())
        print("INDEX_PRESENT:","index.html" in names)
        print("DATA_PRESENT:","data" in names and stat.S_ISDIR(names["data"].st_mode))
        try:
            config=read_small(s,ROOT+"/.git/config")
            if config is None:
                print("GIT_ORIGIN: unavailable or not a regular text file")
            else:
                origin=[]
                in_origin=False
                for line in config.splitlines():
                    line=line.strip()
                    if line.startswith("["):
                        in_origin=('[remote "origin"]' in line)
                    if in_origin and line.startswith("url") and "=" in line:
                        origin.append(line.split("=",1)[1].strip())
                for url in origin:
                    # Report only the verified public repo name, never raw
                    # URL (may include credentials in userinfo/query).
                    expected=bool(re.search(r"github[.]com[:/]kiemtimem12345/solieutaichinh(?:[.]git)?(?:$|[?/#])",url,re.I))
                    print("GIT_ORIGIN_MATCHES_PROJECT_REPO:",expected)
                if not origin:
                    print("GIT_ORIGIN: no origin remote configured")
        except FileNotFoundError:
            print("GIT_CONFIG: not found")
        try:
            head=read_small(s,ROOT+"/.git/HEAD",1024)
            if head and head.strip().startswith("ref: refs/heads/"):
                print("GIT_BRANCH:",head.strip().split("/")[-1][:80])
            else:
                print("GIT_HEAD: detached or inaccessible")
        except FileNotFoundError:
            print("GIT_HEAD: not found")
        print("No remote modifications.")
        return 0
    except Exception as e:
        print("::error::Diagnostic failed:",type(e).__name__);return 1
    finally:
        if s is not None:s.close()
        if t is not None:t.close()
if __name__=="__main__":sys.exit(main())
