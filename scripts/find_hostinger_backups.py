#!/usr/bin/env python3
"""Read-only scan for a nearby archived frontend in known Hostinger folders."""
import base64,hashlib,os,socket,stat,sys
import paramiko
BASE="/home/u154814653/domains/solieutaichinh.online"
HOME="/home/u154814653"
FINGERPRINT="SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
CANDIDATES=[
 HOME+"/.builds", BASE+"/.builds", BASE+"/backups",BASE+"/backup",
 BASE+"/private_html", BASE+"/releases", BASE+"/public_html/.builds",
 BASE+"/public_html/backups",HOME+"/backups",
]
SAFE_EXT=(".html",".htm",".css",".js",".zip",".tar",".gz")
def run():
 if os.getenv("SFTP_USERNAME")!="u154814653" or not os.getenv("SFTP_PASSWORD"):
  print("::error::SFTP credentials are not configured");return 2
 t=None;s=None
 try:
  sock=socket.create_connection(("195.35.62.53",65002),timeout=12)
  t=paramiko.Transport(sock);t.get_security_options().key_types=("ssh-ed25519",)
  t.start_client(timeout=15)
  key=t.get_remote_server_key()
  fp="SHA256:"+base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode().rstrip("=")
  if key.get_name()!="ssh-ed25519" or fp!=FINGERPRINT:
   print("::error::SSH host key mismatch");return 2
  t.auth_password("u154814653",os.environ["SFTP_PASSWORD"],fallback=False)
  if not t.is_authenticated(): print("::error::SFTP auth failed");return 1
  s=paramiko.SFTPClient.from_transport(t)
  print("PASS: read-only Hostinger backup candidate scan")
  for candidate in CANDIDATES:
   try:
    a=s.stat(candidate)
    if not stat.S_ISDIR(a.st_mode):
     print("CHECK: candidate exists but is not directory:",candidate);continue
    items=s.listdir_attr(candidate)
    print("FOUND: candidate directory",candidate,"entries",len(items))
    matches=[]
    for item in items:
     n=item.filename
     # Restrict log to public frontend-looking file types or obvious backup directories.
     if n.lower().endswith(SAFE_EXT) or n.lower() in ("public_html","assets","css","js","build","dist","site","website","backup","backups"):
      if not n.startswith("."): matches.append(n)
    print("Candidate frontend/backup entries:",", ".join(matches[:35]) if matches else "(none found at this depth)")
   except FileNotFoundError: print("MISSING:",candidate)
   except PermissionError: print("DENIED:",candidate)
   except OSError as e: print("ERROR:",candidate, "errno",e.errno)
  print("No files were modified.")
  return 0
 except Exception as exc:
  print("::error::Candidate scan failed:",type(exc).__name__);return 1
 finally:
  if s is not None:s.close()
  if t is not None:t.close()
if __name__=="__main__":sys.exit(run())
