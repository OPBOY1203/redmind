# Web Enumeration - Attack Path

## Attack Path (Web Enumeration)

**Automation / OSINT**  

- Run FinalRecon or Recon-ng to gather initial intelligence.  
- Supplement with theHarvester and SpiderFoot for emails, subdomains, and banners.  
- Reference OSINT Framework for manual lookups.  

**Surface Expansion (Crawling)**  

- Map the site with Burp/ZAP spiders.  
- Use Scrapy/ReconSpider for structured crawling.  
- Goal: expand directories, params, and hidden links.  

**Fingerprinting**  

- curl headers and redirects.  
- wafw00f for WAF detection.  
- Nikto for outdated software and misconfigurations.  

**Deep Discovery (vHosts / Hidden Domains)**  

- Gobuster/ffuf/Feroxbuster for vHosts and dirs.  
- crt.sh lookups for certificate-registered subdomains.  

**Pivot**  
- Feed new hosts/domains back into Step 1 and repeat cycle.  

------

## Recon Automation / OSINT
Begin with broad automated tools to map out domains, subdomains, emails, IPs, and basic service info.

### **[FinalRecon](https://github.com/thewhiteh4t/FinalRecon)**

>FinalRecon is an all in one **automatic web reconnaissance** tool written in python. Goal of FinalRecon is to provide an **overview** of the target in a **short** amount of time while maintaining the **accuracy** of results. Instead of executing **several tools** one after another it can provide similar results keeping dependencies **small and simple**.

```bash
./finalrecon.py --headers --whois --url http://target.com
```

- **[Recon-ng](https://github.com/lanmaster53/recon-ng)**   modular recon framework
- **[theHarvester](https://github.com/laramies/theHarvester)**   gather emails, subdomains, banners
- **[SpiderFoot](https://github.com/smicallef/spiderfoot)**   OSINT automation (DNS, crawling, IPs, social)
- **[OSINT Framework](https://osintframework.com/)**   manual resource directory

------

## Crawling / Surface Expansion

Map the application s structure, directories, and links. This expands the **attack surface** before fuzzing.

- **Burp Suite Spider**   proxy-based, integrates with active testing
- **OWASP ZAP**   automated crawler/scanner (CLI/headless available)

### **[Scrapy](https://github.com/scrapy/scrapy)** - Web scraping framework

```bash
pip3 install scrapy
scrapy startproject proj
```

### **[ReconSpider](https://github.com/bhavsec/reconspider)**

ReconSpider is most Advanced Open Source Intelligence (OSINT) Framework  for scanning IP Address, Emails, Websites, Organizations and find out  information from different sources.

```bash
python3 ReconSpider.py http://example.com
```

------

## Fingerprinting Services

Identify protections, configurations, and potential weaknesses.

### **curl**

```bash
curl -I https://target.com
```

### [**wafw00f**](https://github.com/EnableSecurity/wafw00f) - Web Application Firewall Fingerprinting Tool.

```bash
pip3 install git+https://github.com/EnableSecurity/wafw00f
wafw00f target.com
```

### **[Nikto](https://github.com/sullo/nikto)** - Web server scanner

```bash
nikto -h target.com -Tuning b
```

------

## Virtual Host & Hidden Domain Discovery

After mapping the obvious, move into discovering **hidden vHosts, staging sites, or subdomains**.

### **Gobuster**

```bash
gobuster vhost -u http://<IP> -w <wordlist> --append-domain
```

### **[ffuf](https://github.com/ffuf/ffuf)**

ffuf is a fast web fuzzer written in Go that allows typical directory discovery, virtual host discovery (without DNS records) and GET and POST parameter fuzzing.

```bash
ffuf -u http://site.htb:8080/FUZZ \
-w /usr/share/seclists/Discovery/Web-Content/common.txt:FUZZ -e .html
```

### **[Feroxbuster](https://github.com/epi052/feroxbuster)**  - Recursive directory/vHost discovery

Uses brute force combined with a wordlist to search for unlinked content in target directories. 

**crt.sh lookup**

```
curl -s "https://crt.sh/?q=target.com&output=json" | jq -r '.[].name_value' | sort -u
```

------

## Key Notes

- Run recon in **layers**: light | medium | heavy.
- Crawling helps define scope before fuzzing (saves time & noise).
- Fingerprinting early prevents wasted effort against protected endpoints.
- Always loop back findings: new subdomains | repeat crawling/fingerprinting.