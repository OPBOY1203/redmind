# Engagement Report – Inlanefreight Live Exercise

## Engagement Overview
**Target Organization:** Inlanefreight  
**Access Provided:** Foothold host via CAT5’s team  
**Entry Method:** VPN / Pwnbox with RDP access to initial foothold  

---

## Objectives
- Demonstrate exploitation and obtain an interactive shell from:
  - A Windows host or server  
  - A Linux host or server  
  - A Web application  
- Identify the shell environment and validate user access on compromised hosts.  

---

## Credentials & Infrastructure
- **Attack VM:** `10.129.114.238`  
- **Foothold Host:** `172.16.1.5`  
- **Credentials:**  
  - User: `htb-student`  
  - Password: `HTB_@cademy_stdnt!`  

---

## Host 1 – Windows Server
- **IP:** `172.16.1.11`  
- **Hostname:** `shells-winsvr`  

### Exploitation
Initial enumeration identified Apache Tomcat running with exposed administrative access.  
- Created a malicious `.war` reverse shell payload using `msfvenom`.  
- Uploaded the payload through the Tomcat Manager interface (using harvested credentials).  
- Triggered execution to establish a reverse shell session.  
- Retrieved flag located in `C:\Shares\dev-share`.  

**Notes:**  
Although a metasploit module was available, it failed during testing. A manual `.war` deployment approach was more reliable and aligned with observed service exposure.  

---

## Host 2 – Linux Web Server
- **IP:** `172.16.1.12`  
- **VHOST:** `blog.inlanefreight.local`  
- **Distribution:** `ubuntu 4ubuntu0.3`  

### Exploitation
Web application banner disclosure on the main page indicated exploitable conditions.  
- Identified a custom exploit module (`50064.rb`) referenced on the target website.  
- Imported the module into Metasploit manually.  
- Executed the exploit, resulting in shell access.  
- Verified the uploaded shell was written in **PHP**.  
- Retrieved required flag from the target.  

**Notes:**  
This engagement provided practical experience in importing and executing non-default Metasploit modules.  

---

## Host 3 – Windows SMB Server
- **IP:** `172.16.1.13`  
- **Hostname:** `shells-winblue`  

### Exploitation
Enumeration identified SMB services vulnerable to EternalBlue (MS17-010).  
- Leveraged the Metasploit `eternalblue` module to gain SYSTEM-level access.  
- Navigated to `C:\Users\Administrator\Desktop\` and extracted `Skills-flag.txt`.  

**Flag Extracted:** `One-H0st-Down!`  

---

## Tools Utilized
- `nmap`, `msfvenom`, `metasploit-framework`  
- RDP client  
- Custom reverse shell payloads (`.war`, PHP)  

---

## Key Takeaways
- Manual payload deployment can be more effective than relying solely on pre-packaged modules.  
- Importing and executing custom Metasploit modules is an essential skill when default exploit sets are insufficient.  
- Classic SMB vulnerabilities (e.g., EternalBlue) remain a valid attack path when unpatched systems are discovered.  

---