# Microsoft SQL Server

## Common Attack Paths

### Enumeration
- [ ] Nmap scripts → `nmap -p1433 --script=ms-sql* <target>`
- [ ] Login test with `sqsh` or `mssqlclient.py`
- [ ] Query server info → `SELECT @@version`
- [ ] Check for linked servers

### Attack Paths
- Weak creds (`sa/blank`, `sa/password`)
- Enable or abuse `xp_cmdshell` for OS command exec
- Linked servers → pivot to other DBs/hosts
- Pass-the-Hash / Kerberos authentication abuse

### Auxiliary Notes
- SQL authentication may fall back to NTLM — relay attacks possible.
- Watch for stored procedures with elevated privileges.
- Post-ex → dump DB contents or pivot deeper into AD.

---

## General Enumeration

```bash
sudo nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 10.129.201.248
```

### Msfconsole

```bash
# msfconsole scan
msf6 use auxiliary(scanner/mssql/mssql_ping

# Connecting 
python3 mssqlclient.py Administrator@10.129.201.248 -windows-auth
```

### Clients

- mssql-cli,  SQL Server PowerShell,  HeidiSQL,  SQLPro,  Impacket's mssqlclient.py


### Database information

| Default System Database | Description |
| --- |  --- |
| master | Tracks all system information for an SQL server instance |
| model | Template database that acts as a structure for every new database created. Any setting changed in the model database will be reflected in any new database created after changes to the model database |
| msdb | The SQL Server Agent uses this database to schedule jobs & alerts |
| tempdb | Stores temporary objects |
| resource | Read-only database containing system objects included with SQL server |

### Service Information

- [MSSQL Cheat Sheet](https://pentestmonkey.net/cheat-sheet/sql-injection/mssql-sql-injection-cheat-sheet)
