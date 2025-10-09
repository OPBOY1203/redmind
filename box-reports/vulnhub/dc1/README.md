# Target: VulnHub – DC:1

## Engagement Overview
**Target:** DC:1  
**Box IP:** 192.168.56.104  

---

### Objectives
- Identify CMS vulnerabilities
- Gain initial access via web exploit
- Enumerate users and escalate privilege
- Capture root-level access and final flag

---

## Service Enumeration

**Ports Open:**  
- 22/tcp – OpenSSH 6.0p1  
- 80/tcp – Apache 2.2.22  
- 111/tcp – rpcbind  

**Web Application:**  
- Drupal 7.x identified via HTTP headers and robots.txt  
- `/CHANGELOG.txt` confirmed version range (7.22–7.26)

**Tools Used:**  
- `nmap`, `gobuster`, `whatweb`, `curl`, `mysql`, `enum4linux`, `Metasploit`

---

## Methodologies

- CMS enumeration using gobuster and nmap scripts  
- Manual validation of Drupal version  
- CMS exploit selection via version-matching  
- Post-exploitation MySQL dump and user recon  
- Privilege escalation via local kernel CVE

---

## Initial Access - Drupalgeddon2 (CVE-2018-7600)

**Vulnerability Explanation:**  
Drupal 7.x versions before 7.58 are vulnerable to a remote code execution flaw via the Form API. Crafted requests allow unauthenticated attackers to execute arbitrary code.

**Penetration:**  
- Exploited with Metasploit module `exploit/unix/webapp/drupal_drupalgeddon2`  
- Shell access gained as `www-data`

---

## Privilege Escalation

**Findings:**  
- Valid Drupal MySQL credentials extracted (`dbuser : R0ck3t`)  
- Users and hashes dumped from database (`admin`, `Fred`)  
- Attempted lateral movement via `su`, no match

**Exploit Used:**  
- Dirty COW (CVE-2016-5195), compiled 32-bit variant  
- Exploit created UID 0 user `firefart`, password `dirtycow`

**Result:**  
Root access achieved.

---

## House Cleaning

- Manual user cleanup
- Reverted `/etc/passwd`  
- Removed exploit artifact

---

## Post-Exploitation

**Tools Utilized**
- Metasploit
- MySQL client
- Gobuster
- WhatWeb
- Dirty COW (compiled 32-bit)

---

## Key Takeaways

* Legacy boxes may break due to tooling rot, not skill
* Exploit validation > brute-force cracking
* Enumeration reveals the real narrative
* Drupal boxes often have multiple paths — most are social engineering traps
* Rooting is not always the win — knowing when to pivot is

---

### Status: COMPLETED