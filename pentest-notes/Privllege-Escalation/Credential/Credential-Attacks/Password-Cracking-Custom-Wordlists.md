# Custom Wordlists with [CeWL](https://github.com/digininja/CeWL) & [Hashcat](https://hashcat.net/hashcat/)

This file explains how to build **target-specific password wordlists** using OSINT, CeWL, and rules.  
Custom lists are vital when default lists (like rockyou) fail because real users often base passwords on personal details.  

---

## Step 1: Gather OSINT & Build Base HTML
Collect details like names, DOB, pets, hobbies, employer, etc.  
Save them into a simple HTML file (`target.html`) for CeWL to crawl.  

```html
<!DOCTYPE html>
<html>
<head><title>Target Profile</title></head>
<body>
  <h1>John Doe</h1>
  <ul>
    <li>Born: March 14, 1985</li>
    <li>Works at: Acme Corp</li>
    <li>Lives in: Toronto, ON</li>
    <li>Dog: Rover</li>
    <li>Hockey fan</li>
  </ul>
</body>
</html>
```

Run a quick local server so CeWL can crawl it:  

```bash
python3 -m http.server 8000
```

---

## Step 2: Use CeWL to Extract Keywords
CeWL extracts words and numbers from HTML content. Great for harvesting personal keywords.  

```bash
# Crawl target.html and save words with numbers
cewl -d 1 -m 2 --with-numbers -w target_initial.txt http://localhost:8000/target.html

# Count entries
wc -l target_initial.txt
```

Optional: expand with deeper crawl of the real target site.  

```bash
cewl -w target_extended.txt -d 3 -m 4 https://target-site.com
```

---

## Step 3: Combine & Clean Wordlists
Merge multiple sources and remove duplicates.  

```bash
cat target_initial.txt target_extended.txt > combined_wordlist.txt
sort -u combined_wordlist.txt -o combined_unique.txt
```

---

## Step 4: Crack with Hashcat + Rules
Use Hashcat with rule files to apply realistic mutations (years, symbols).  

```bash
hashcat -m [hash-mode] -r append_year.rule -r append_special.rule hashes.txt combined_unique.txt
```

---

## Step 5: Iterate
- Add cracked words back to the base list.  
- Re-run CeWL or adjust rules.  
- Refine until you cover realistic keyspaces.  

---

## Example Walkthrough
Target: Jordan Smith, born Aug 12, 1990, works at MapleTech, lives in Winnipeg, dog named Buddy, hockey fan.  

```bash
# Extract with CeWL
cewl -d 1 -m 2 --with-numbers -w jordan_init.txt http://localhost:8000/target.html

# Crack with Hashcat using custom list
hashcat -m 0 hashes.txt jordan_init.txt -r append_year.rule -r append_special.rule
```
