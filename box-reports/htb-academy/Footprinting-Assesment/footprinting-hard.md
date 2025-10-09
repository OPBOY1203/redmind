# Footprinting – Hard Lab

## Engagement Overview
Target: Internal MX/management server, also functioning as a backup server.  
Goal: Enumerate and recover HTB user’s password.

---

## Objectives
- Enumerate target services.
- Leverage exposed services for credentials.
- Extract HTB’s password.

---

## Service Enumeration
**Nmap Scan**
```bash
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu
110/tcp open  pop3     Dovecot pop3d
143/tcp open  imap     Dovecot imapd
993/tcp open  imaps    Dovecot imapd
995/tcp open  pop3s    Dovecot pop3d
```

**UDP Scan**
```bash
68/udp  open|filtered dhcpc
161/udp open          snmp (net-snmp v3)
```

---

## SNMP Enumeration
- Community string: `backup`
- Discovered via `onesixtyone` and `braa`:
  - Admin email
  - Hostname: `NIXHARD`
  - File: `/opt/tom-recovery.sh`
  - Credentials: `tom:NMds732Js2761`

---

## Initial Access
- IMAP login with `tom` succeeded.  
- Inbox contained OpenSSH private key.  

```bash
ssh tom@10.129.202.20 -i rsa_key
```

---

## Post-Exploitation
**MySQL enumeration:**
```bash
mysql -u tom -p
```
- Database: `users`
- Table: `users`
- Retrieved HTB credentials:
```text
username: HTB
password: ---SNIP---
```

---

## Tools Utilized
- `nmap` (TCP & UDP)
- `onesixtyone`, `braa`
- `openssl s_client`
- `ssh`
- `mysql`

---

## Key Takeaways
- SNMP misconfiguration exposed sensitive recovery script and credentials.
- Email service stored private SSH keys.
- Weak separation of duties: same credentials granted access across IMAP/SSH/MySQL.
- Successfully escalated to extract domain backup user’s credentials.