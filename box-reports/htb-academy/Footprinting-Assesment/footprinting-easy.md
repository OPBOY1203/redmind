# Footprinting – Easy Lab

## Engagement Overview

We were commissioned by **Inlanefreight Ltd** to test three internal servers. The first target is an internal DNS server. Our objective is to gather as much information as possible without using aggressive exploits. A flag (`flag.txt`) was placed on the server to measure success.  

Known intel: credentials `ceil:qwer1234`.

---

## Objectives

- Enumerate the target.
- Gain access using discovered information.
- Locate and extract the `flag.txt`.

---

## Service Enumeration

**Nmap Scan:**

```bash
PORT     STATE SERVICE VERSION
21/tcp   open  ftp
| 220 ProFTPD Server (ftp.int.inlanefreight.htb)
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2
53/tcp   open  domain  ISC BIND 9.16.1
2121/tcp open  ftp
| 220 ProFTPD Server (Ceil's FTP)
```

---

## Initial Access

- FTP (21): Empty, root-owned. No value.
- SSH: Password authentication failed, certificate required.
- FTP (2121): Login with `ceil:qwer1234` successful. Retrieved SSH keys:
  - `id_rsa` (private key)
  - `id_rsa.pub`
  - `authorized_keys`

**Access via SSH with stolen private key:**

```bash
ssh ceil@10.129.150.116 -i id_rsa
```

---

## Post-Exploitation

Located flag in `/home/flag/flag.txt`:

```bash
HTB{--SNIP--}
```

---

## Tools Utilized

- `nmap`
- `ftp`
- `ssh`

---

## Key Takeaways

- Multiple FTP instances exposed sensitive data.
- Poor key hygiene: user’s private SSH key stored in accessible FTP directory.
- Lateral access achieved without exploitation.