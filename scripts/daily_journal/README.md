# Daily Journal

Reusable **daily journal template** (`daily.md`) and a Python helper script that generates dated entries from it.

## Structure

```bash
daily-journal/
├── daily_template.md
├── daily_journal.py
└── daily/
    └── YYYY-MM-DD.md
    └── ...        
```

## Template

The template file `daily.md` contains the base layout for each daily entry, including a placeholder for the current date:

```markdown
## Daily Journal - {{date:dddd, MMMM Do, YYYY}}

**Focus Areas**: [Python, Red Team, HTB]

---
...etc...
```

When the script runs, it adds `{{date:dddd, MMMM Do, YYYY}}` with the current date in a format like:

```
Sunday, August 10th, 2025
```

## Script Features

- Reads `daily.md` from the root dir.
- Inserts the current date (with proper ordinal suffixes).
- Saves the result to `daily/YYYY-MM-DD.md`.
- If the file already exists for today, it **does not overwrite** it.
- Opens the created/existing file in **xed**.

## Requirements

- **Editor:** `xed` - can be changed on line 38
