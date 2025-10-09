# HTB: Blue

## Engagement Overview

**Target:** Blue    
**Box IP:** 10.10.10.40     
**Local IP:** 10.10.14.10   
**Date:** 2025-07-10

---

### Objectives

- Exploit SMBv1 vulnerability (EternalBlue/MS17-010) to gain remote shell access
- Capture user and root flags

---

## Service Enumeration

```bash
# Nmap (condensed)
nmap -sC -sV -oN nmap.txt 10.10.10.40
```

**Relevant output (condensed):**
```
PORT    STATE SERVICE      VERSION
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows 7 Professional 7601 SP1
```

Host details indicate Windows 7 Professional SP1, SMBv1 enabled and vulnerable; guest account access allowed.

---

## Initial Access

### Methodologies & Exploitation

**Vulnerability:** CVE-2017-0144 (EternalBlue / SMBv1 RCE)

**Attempts & tools used:**

- Metasploit `windows/smb/ms17_010_eternalblue` (initial attempt — failed)
- Manual PoC from ExploitDB (`42031.py`) — modified and executed successfully

**Notes:** Modern tooling sometimes fails against older exploits; manual adaptation of PoC/payload was required to get a working shell.

**Execution (conceptual):**

```bash
# adapted PoC execution (details preserved in original notes)
python3 42031.py --target 10.10.10.40 --payload <adjusted-shell>
```

**Result:** Remote shell obtained (SYSTEM level in this case).

---

## Privilege Escalation

Not applicable — initial exploit yielded SYSTEM-level access.

---

## House Cleaning / Post-Exploitation

- No persistence left on target
- No extra uploads beyond exploit payload

**Flags (captured):**
- `user.txt`: `0c4f3a9386dba985686ce78e58237c6d`
- `root.txt`: `b6b9cccdf6904e9ffdb0110122a50a43`

---

## Tools Utilized
- nmap
- Python (modified ExploitDB PoC `42031.py`)
- Metasploit (attempted)

---

## Key Takeaways
- EternalBlue remains a high-value legacy exploit; manual tuning of PoCs/payloads may be necessary.
- Understand the exploit internals — modern modules can fail on older targets without adjustments.
