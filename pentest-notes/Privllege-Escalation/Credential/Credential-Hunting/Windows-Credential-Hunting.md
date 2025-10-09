# Windows Credential Hunting

Methods for locating credentials stored in files, shares, Group Policy, and configuration. Includes LaZagne usage and manual searches.

---

## [LaZagne](https://github.com/AlessandroZ/LaZagne)

The **LaZagne project** is an open source application used to **retrieve lots of passwords** stored on a local computer.

```cmd
# Run LaZagne to dump stored passwords
start LaZagne.exe all

# Verbose mode
start LaZagne.exe all -vv
```

---

## [findstr](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/findstr)

Search for credential keywords across files. Useful for configs and scripts.

```cmd
findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml *.git *.ps1 *.yml
```

---

## Common Credential Locations

- Group Policy (SYSVOL share)
- Scripts in SYSVOL or IT shares
- `web.config` on dev/IT machines
- `unattend.xml` for installation creds
- AD user/computer description fields
- KeePass databases
- Files named like `pass.txt`, `passwords.docx`, `passwords.xlsx`
- SharePoint-hosted documents

### Keywords to Search

```
password
passphrase
key
username
user account
creds
login
pwd
dbpassword
dbcredential
```

---
