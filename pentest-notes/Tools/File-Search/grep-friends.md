# Grep & Friends – Fast Text-Fu

## Common Commands
```bash
# fast search show line numbers (recursive, ignores junk)
rg -n 'pattern'

# search everything, ignore binaries, smart-case, PCRE
rg -nI --hidden -S 'foo\(\d+\)'

# classic recursive grep
grep -Rni --color=always 'pattern' .

# extended regex (alternation)
grep -RniE 'foo|bar'

# quick column slicing
awk -F: '/regex/ {print $1 ":" $2 ":" $3}' file

# print range
sed -n '1,120p' file

# in-place replace (GNU sed)
sed -i 's/old/new/g' **/*.conf
```

---

## Examples
```bash
# Find TODOs except vendor
rg -n 'TODO|FIXME' -g '!vendor' -S

# Find function defs + 2 lines after 
rg -nA2 -P '^\s*(def|func|class)\s+\w+'

# Extract emails
rg -oP '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' *.md | sort -u

# Count HTTP status codes
awk '{a[$9]++} END{for(k in a) print k,a[k]}' access.log | sort -n

# Replace DEBUG with INFO
rg -l 'DEBUG' -g '*.yaml' | xargs -r sed -i 's/\bDEBUG\b/INFO/g'

# Lines not containing pattern
grep -Rnv 'pattern' .  
```

---

## Handy Recipes

### File lists to actions
```bash
# fuzzy pick match
rg -n 'pat' | fzf

# edit all matching files
rg -l 'pat' | xargs -r $EDITOR

# safe delete files
rg -l 'LICENSE' | xargs -r rm -i
```

### Extract fields / values
```bash
# values after key=
rg -o -nP '(?<=^key=).*' file

# extract URLs
rg -oP 'https?://\S+' access.log | sort -u

# extract IPv4 addresses
rg -oP '\b(?:\d{1,3}\.){3}\d{1,3}\b' file | sort -u
```

### Count & rank
```bash
# top words
rg -o '\w+' file | sort | uniq -c | sort -nr | head

# match counts by file
grep -Ric 'pat' . | sort -t: -k2,2nr
```

### Multi-line
```bash
# grep multiline between BEGIN/END
grep -Pzo '(?s)BEGIN.*?END' file

# ripgrep multiline
rg -Up '(?s)BEGIN.*?END'
```

---

## awk – Columns & Filters
```bash
# select specific columns
awk -F: '{print $1,$3,$7}' /etc/passwd

# skip header, print column 2
awk -F, 'NR>1 {print $2}' file.csv

# numbered matches containing ERROR
awk '/ERROR/ {print FNR ":" $0}' logfile

# sum column 3 values > 100
awk '$3 > 100 {sum+=$3} END {print sum}' data.txt

# clean col1 spaces → underscores
awk 'BEGIN{FS=OFS=","} {gsub(/ /,"_",$1); print $1,$2}' in.csv

# histogram of column 1
awk '{a[$1]++} END {for(k in a) print a[k],k}' | sort -nr

# print last field
awk '{print $NF}' file
```

---

## sed – Edit Streams
```bash
# show lines 20–40
sed -n '20,40p' file

# drop comments/blanks
sed -E '/^\s*($|#)/d' file.conf

# replace in-place
sed -i 's/old/new/g' file

# bulk replace in *.conf
find . -name '*.conf' -print0 | xargs -0 sed -i 's/old/new/g'

# replace with capture group
sed -E -i 's/(user=).*/\1admin/' app.env

# insert before match
sed -i '/^\[server\]/i # added by script' config.ini

# append after line 5
sed -i '5a NEW_LINE' file
```

---

## Joins, Intersections, Diffs
```bash
# deduplicate
sort file | uniq

# deduplicate keep order
awk '!seen[$0]++' file

# intersection of two files
grep -Fxf listA.txt listB.txt

# lines in A not in B
grep -Fvx -f B.txt A.txt

# directory differences
diff -qr dir1 dir2
```

---

## Binary / Encoding
```bash
# grep ignoring binary
grep -I -R 'pat' .

# ripgrep ignoring binary
rg -nI 'pat'

# clean encoding
iconv -f utf-8 -t utf-8 -c file > clean.txt
```

---

## Regex Crashpad
```bash
# word boundary
\bfoo\b

# line anchors
^foo
bar$

# repetition/optional
a+
colou?r

# alternation
foo|bar

# character class
[A-Za-z0-9_]

# non-greedy dotall
(?s).*?

# lookbehind
(?<=prefix)thing

# lookahead
thing(?=suffix)

# negative lookahead
(?!bad)
```

---