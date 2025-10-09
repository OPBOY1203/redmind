# MySQL

## Common Attack Paths

### Enumeration
- [ ] Banner grab → `mysql -u root -p -h <target>`
- [ ] Nmap NSE → `nmap --script=mysql* -p3306 <target>`
- [ ] Query version → `SELECT @@version;`

### Attack Paths
- Default creds (`root/root`, no password)
- File read/write via `LOAD DATA INFILE` / `SELECT INTO OUTFILE`
- User-defined functions (UDF) for local privilege escalation
- Abuse MySQL for pivoting via user grants

### Auxiliary Notes
- Often exposed internally with weak auth.
- Post-ex → dump user tables, look for creds in cleartext.
- If filesystem accessible, webshell dropper via OUTFILE.

---

## General Enumeration

*Common Commands*

`sudo nmap 10.129.14.128 -sV -sC -p3306 --script mysql*`

```bash
mysql -u root -h 10.129.14.132

mysql -u root -pP4SSw0rd -h 10.129.14.128
```

*Example 1*

```bash
mysql> show databases;

+--------------------+
| Database |
+--------------------+
| information\_schema |
| mysql |
| performance\_schema |
| sys |
| users |
+--------------------+

5 rows in set (0.00 sec)

mysql> use users;

Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed

mysql> show tables;

+-----------------+
| Tables\_in\_users |
+-----------------+
| users |
+-----------------+

1 row in set (0.00 sec)

mysql> show columns from users;

+----------+-------------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id | int | YES | | NULL | |
| username | varchar(50) | YES | | NULL | |
| password | varchar(50) | YES | | NULL | |
+----------+-------------+------+-----+---------+-------+

3 rows in set (0.00 sec)

mysql> SELECT \* FROM users WHERE username LIKE "HTB";

+------+----------+------------------------------+
| id | username | password |
+------+----------+------------------------------+
| 150 | HTB | theflagisherenormally |
+------+----------+------------------------------+

1 row in set (0.00 sec)
```

*Example 2*

```bash
mysql> use sys;
mysql> show tables;

+-----------------------------------------------+
| Tables_in_sys                                 |
+-----------------------------------------------+
| host_summary                                  |
| host_summary_by_file_io                       |
| host_summary_by_file_io_type                  |
| host_summary_by_stages                        |
| host_summary_by_statement_latency             |
| host_summary_by_statement_type                |
| innodb_buffer_stats_by_schema                 |
| innodb_buffer_stats_by_table                  |
| innodb_lock_waits                             |
| io_by_thread_by_latency                       |
|...SNIP...                                     |
| x$waits_global_by_latency                     |
+-----------------------------------------------+

mysql> select host, unique_users from host_summary;

+-------------+--------------+
| host        | unique_users |
+-------------+--------------+
| 10.129.14.1 |            1 |
| localhost   |            2 |
+-------------+--------------+

2 rows in set (0,01 sec)
```

### Command Reference


| Command | Description |
| --- |  --- |
| mysql -u user -ppassword -h IP address | Connect to the MySQL server, no space on password |
| show databases; | Show all databases. |
| use database; | Select one of the existing databases. |
| show tables; | Show all available tables in the selected database. |
| show columns from table; | Show all columns in the selected table. |
| select \* from table; | Show everything in the desired table. |
| select \* from table> where column = "string>; | Search for needed string in the desired table. |

### Reference manuals

- [MySQL Manual](https://dev.mysql.com/doc/refman/8.0/en/system-schema.html#:~:text=The%20mysql%20schema%20is%20the,used%20for%20other%20operational%20purposes)
- [MySQL Cheat Sheet](https://www.bytebase.com/reference/mysql/how-to/top-mysql-commands-with-examples/)
