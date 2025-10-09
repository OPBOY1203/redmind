# Domain Name System

## Common Attack Paths

### Enumeration

- [ ] Zone transfers → `dig axfr @<nameserver> <domain>`
- [ ] Brute subdomains → `dnsrecon -d <domain> -t brt`
- [ ] Reverse lookups → `dnsrecon -r <ip-range>`
- [ ] Identify internal hostnames via misconfigured DNS

### Attack Paths

- Zone transfer → internal host discovery
- Subdomain brute force → hidden apps / staging environments
- Cache poisoning (rare, lab scenarios)
- Exploiting dynamic DNS in AD → privilege escalation

### Auxiliary Notes

- Often overlooked; DNS can leak entire internal hostmap.
- Check both UDP/53 and TCP/53 for transfer attempts.
- Useful pivot point into Active Directory environments.

---

## Passive Enumeration

*Common Commands:*

```bash
dig -x host
dig ns example.com @10.129.14.128
dig CH TXT version.bind 10.129.120.85
dig any example.com @10.129.14.128
dig axfr @nsztm1.digi.ninja zonetransfer.me
```

---

## Active Enumeration

### Subdomain Brute Forcing

### **[DNSEnum](./../Web-Enum/Tools/DNSEnum.md)**

*Recursive Scan:*

```bash
dnsenum --enum example.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r

# With alternate dns
dnsenum --dnsserver 10.129.14.128 --enum -p 0 -s 0 -o subdomains.txt -f /opt/useful/seclists/Discovery/DNS/subdomains-top1million-110000.txt example.com
```

---

## Tools

| Tool                                                    | Description                                                                                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [dnsenum](https://github.com/fwaeytens/dnsenum)         | Comprehensive DNS enumeration tool that supports dictionary and brute-force attacks for discovering subdomains.                 |
| [fierce](https://github.com/mschwager/fierce)           | User-friendly tool for recursive subdomain discovery, featuring wildcard detection and an easy-to-use interface.                |
| [dnsrecon](https://github.com/darkoperator/dnsrecon)    | Versatile tool that combines multiple DNS reconnaissance techniques and offers customisable output formats.                     |
| [amass](https://github.com/owasp-amass/amass)           | Actively maintained tool focused on subdomain discovery, known for its integration with other tools and extensive data sources. |
| [assetfinder](https://github.com/tomnomnom/assetfinder) | Simple yet effective tool for finding subdomains using various techniques, ideal for quick and lightweight scans.               |
| [puredns](https://github.com/d3mondev/puredns)          | Powerful and flexible DNS brute-forcing tool, capable of resolving and filtering results effectively.                           |

---

## Service Information

### Servers

| Server Type                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DNS Root Server              | The root servers of the DNS are responsible for the top-level domains (TLD). As the last instance, they are only requested if the name server does not respond. Thus, a root server is a central interface between users and content on the Internet, as it links domain and IP address. The Internet Corporation for Assigned Names and Numbers (ICANN) coordinates the work of the root name servers. There are 13 such root servers around the globe. |
| Authoritative Nameserver     | Authoritative name servers hold authority for a particular zone. They only answer queries from their area of responsibility, and their information is binding. If an authoritative name server cannot answer a client's query, the root name server takes over at that point. Based on the country, company, etc., authoritative nameservers provide answers to recursive DNS nameservers, assisting in finding the specific web server(s).              |
| Non-authoritative Nameserver | Non-authoritative name servers are not responsible for a particular DNS zone. Instead, they collect information on specific DNS zones themselves, which is done using recursive or iterative DNS querying.                                                                                                                                                                                                                                               |
| Caching DNS Server           | Caching DNS servers cache information from other name servers for a specified period. The authoritative name server determines the duration of this storage.                                                                                                                                                                                                                                                                                             |
| Forwarding Server            | Forwarding servers perform only one function: they forward DNS queries to another DNS server.                                                                                                                                                                                                                                                                                                                                                            |
| Resolver                     | Resolvers are not authoritative DNS servers but perform name resolution locally in the computer or router.                                                                                                                                                                                                                                                                                                                                               |

### Records

| DNS Record | Description                                                                                                                                                                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A          | Returns an IPv4 address of the requested domain as a result.                                                                                                                                                                                      |
| AAAA       | Returns an IPv6 address of the requested domain.                                                                                                                                                                                                  |
| MX         | Returns the responsible mail servers as a result.                                                                                                                                                                                                 |
| NS         | Returns the DNS servers (nameservers) of the domain.                                                                                                                                                                                              |
| TXT        | This record can contain various information. The all-rounder can be used, e.g., to validate the Google Search Console or validate SSL certificates. In addition, SPF and DMARC entries are set to validate mail traffic and protect it from spam. |
| CNAME      | This record serves as an alias for another domain name. If you want the domain www.hackthebox.eu to point to the same IP as hackthebox.eu, you would create an A record for hackthebox.eu and a CNAME record for www.hackthebox.eu.               |
| PTR        | The PTR record works the other way around (reverse lookup). It converts IP addresses into valid domain names.                                                                                                                                     |
| SOA        | Provides information about the corresponding DNS zone and email address of the administrative contact.                                                                                                                                            |
