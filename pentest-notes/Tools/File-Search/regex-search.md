# YAML tag search

## Basics - ripgrep

```bash
# Files containing a given tag anywhere (fast)
rg -n "#tag:Web-Recon" .

# YAML front matter only (between --- and ---)
rg -nU "^---[\s\S]*?^---" -g "*.md"   # preview blocks
```

## Search tags in YAML front matter

```bash
# Has tag "cred-hunt" in tags: [...]
rg -nU '^-{3}[\s\S]*?^tags:\s*\[[^\]]*\bcred-hunt\b[^\]]*\][\s\S]*?^-{3}' -g "*.md"

# Same but tools:
rg -nU '^-{3}[\s\S]*?^tools:\s*\[[^\]]*\bnetexec\b[^\]]*\][\s\S]*?^-{3}' -g "*.md"
```

## OR / AND logic

```bash
# OR: has either cred-hunt or web-recon
rg -nU '^-{3}[\s\S]*?^tags:\s*\[[^\]]*\b(cred-hunt|web-recon)\b[^\]]*\][\s\S]*?^-{3}' -g "*.md"

# AND (two passes): must have both
rg -lU '^-{3}[\s\S]*?^tags:\s*\[[^\]]*\bcred-hunt\b[^\]]*\][\s\S]*?^-{3}' -g "*.md" \
| xargs rg -nU '^-{3}[\s\S]*?^tags:\s*\[[^\]]*\bweb-recon\b[^\]]*\][\s\S]*?^-{3}'
```

## List all unique tags across repo

```bash
# Grab tag arrays, split, clean, sort unique
rg -nU '^\s*tags:\s*\[[^]]*\]' -g "*.md" \
| sed -E 's/.*\[(.*)\].*/\1/' \
| tr ',' '\n' | tr -d '[] "' | sed '/^$/d' \
| sort -fu
```

## Files missing tags (audit)

```bash
# Front matter present but no tags key
rg -lU '^-{3}[\s\S]*?^-{3}' -g "*.md" \
| xargs rg -L '^\s*tags:\s*\['
```

## Extract front matter as JSON (with yq)

```bash
# Show tags for each file
for f in $(fd -e md); do
  yq -oy '.tags' "$f" 2>/dev/null | sed "s/^/$f: /"
done

# Files with tag "ssh"
for f in $(fd -e md); do
  yq -oy '.tags' "$f" 2>/dev/null | grep -qi '\bssh\b' && echo "$f"
done
```

## Inline hash-style tags (your #tag:& )

```bash
# Find any inline #tag:<word>
rg -n '#tag:[A-Za-z0-9_-]+' -g "*.md"

# Files that reference Web-Recon anywhere inline
rg -n '#tag:Web-Recon' -g "*.md"
```

## VS Code quick patterns

- In  Use Regular Expression  mode:
  - Front matter block: `(?s)^---.*?---`
  - Tags array contains word: `(?s)^---.*?tags:\s*\[[^\]]*\bcred-hunt\b[^\]]*\].*?---`

## Rename tags safely

```bash
# cred-hunt -> credential-hunting inside tags arrays only
rg -nU '(^---[\s\S]*?^tags:\s*\[[^\]]*)\bcred-hunt\b' -g "*.md" \
| cut -d: -f1 | sort -u \
| xargs -I{} perl -0777 -pe 'BEGIN{$^I=".bak"} s/(^---[\s\S]*?^tags:\s*\[[^\]]*)\bcred-hunt\b/$1credential-hunting/gm' -i {}
```

------

If you don t have `rg`/`fd`/`yq`:

```bash
sudo apt-get install ripgrep fd-find yq
# fd might install as fdfind; alias it:
alias fd=fdfind
```

One-liner to **search any of `tags/tools/service`** 

```bash
WORD="ssh"
rg -nU "^-{3}[\\s\\S]*?^(tags|tools|service):\\s*\\[[^]]*\\b${WORD}\\b[^]]*\\][\\s\\S]*?^-{3}" -g "*.md"
```