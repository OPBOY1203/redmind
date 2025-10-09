# HTB: Jerry

## Engagement Overview

**Target:** Jerry   
**Box IP:** 10.10.10.95     
**Local IP:** 10.10.16.9    
**Date:** 2025-07-30    

---

### Objectives

- Enumerate Tomcat service and discover valid manager credentials.  
- Upload a WAR payload to get a SYSTEM-level shell.  
- Capture `user.txt` and `root.txt` (SYSTEM).

---

## Service Enumeration

```bash
nmap -sC -sV -A -o nmap.txt 10.10.10.95
```

**Relevant output (condensed):**
- 8080/tcp open http Apache Tomcat/Coyote JSP engine 1.1 (Tomcat 7.0.88)

Host identified as Windows Server 2012 R2.

---

## Initial Access

### Tomcat manager login discovery

- Used Metasploit auxiliary scanner for Tomcat manager credentials: `tomcat:s3cret` discovered via `scanner/http/tomcat_mgr_login`.  
- Valid credentials allowed Manager deployment privileges.

### WAR upload → Meterpreter (SYSTEM)

- Used `exploit/multi/http/tomcat_mgr_upload` to upload a WAR and run a staged payload, resulting in meterpreter session as `JERRY$` which escalated to `NT AUTHORITY\SYSTEM` (process spawn and `whoami` confirm).

```text
# meterpreter session snippet (conceptual)
meterpreter > getuid
Server username: JERRY$
meterpreter > shell
C:\apache-tomcat-7.0.88> whoami
nt authority\system
```

---

## Privilege Escalation

Not applicable — initial exploit yielded SYSTEM-level access.

---

## House Cleaning / Post-Exploitation

- No persistent uploads retained beyond temporary payload deployment.  
- No further persistence actions performed.

**Flags captured:**  
- `user.txt`: `7004dbcef0f854e0fb401875f26ebd00`  
- `root.txt`: `b6b9cccdf6904e9ffdb0110122a50a43`

---

## Tools Utilized
- nmap, metasploit (tomcat scanner + war deploy)

---

## Key Takeaways
- Tomcat manager with weak credentials is a simple direct path to SYSTEM on Windows boxes when upload is permitted.  
- Automated auxiliary modules are useful to find manager creds quickly; WAR deployments still work when Manager is enabled.  
