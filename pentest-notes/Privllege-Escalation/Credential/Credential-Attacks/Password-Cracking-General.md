# General Password Cracking

This file covers core password cracking techniques using John the Ripper (JtR) and Hashcat.  
Each subsection explains **what the technique is, why it’s useful, and how to run it**.  

---

## [John the Ripper](https://github.com/openwall/john)

### Single Crack Mode
Useful for **quick wins against Linux accounts**, where usernames and passwords may overlap (e.g., username reused as password).  
Generates password candidates automatically from usernames in the hash file.  

```bash
# Create a test passwd file with a username and hash
echo -n r0lf:$6$ues25dIanlctrWxg$nZHVz2z4kCy1760Ee28M1xtHdGoy0C2cYzZ8l2sVa1kIa8K9gAcdBP.GI6ng/qA4oaMrgElZ1Cb9OeXO4Fvy3/:0:0:Rolf Sebastian:/home/r0lf:/bin/bash > passwd

# Run John in single crack mode
john --single passwd
```

---

### Wordlist Mode w/ Format Specified
When the password is not guessable by username, use **wordlists** with a defined hash format.  
Always identify the hash type first, or cracking will fail.  

```bash
# Identify the hash type
hashid -j 193069ceb0461e1d40d216e32c79c704

# Save the hash to file
echo -n 193069ceb0461e1d40d216e32c79c704 > hash.txt

# Crack using John with rockyou and specific format
john --wordlist=/usr/share/seclists/rockyou.txt --format=ripemd-128 hash.txt
```

---

## [Hashcat](https://github.com/hashcat/hashcat)

### General Syntax
Hashcat is more powerful and supports GPU acceleration. Always run **hashid** to confirm format before selecting a `-m` mode.  

```bash
# Example identifying the hash type and format
hashid -m '$1$FNr44XZC$wQxY6HHLrgrGX0e1195k.1'

# Basic syntax
hashcat -a 0 -m <hash-mode> <hashfile> <wordlist/rule/mask>
```

---

### Dictionary Attack
Best for quick hits using large wordlists (rockyou, seclists). Combine with rules to expand coverage.  

```bash
# Basic dictionary attack
hashcat -a 0 -m 0 e3e3ec5831ad5e7288241960e5d4fdb8 /usr/share/wordlists/rockyou.txt

# Dictionary + rules
hashcat -a 0 -m 0 1b0556a75770563578569ae21392630c /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

---

### Mask Attack
Mask attacks (`-a 3`) allow you to brute force within a defined keyspace, instead of trying every possibility. 
Ideal when you know **password length or structure** (e.g., “six letters + two numbers”).  

```bash
# Example: one uppercase, four lowercase, one digit, one special
hashcat -a 3 -m 0 1e293d6912d074c0fd15844d803400dd '?u?l?l?l?l?d?s'
```
