#!/usr/bin/env python3
# Lightweight daily note launcher

import os
from datetime import datetime
import subprocess
import shutil

# Config
template_path = "daily_template.md"
output_dir    = "daily"

# Helpers
def ordinal(n: int) -> str:
    # 1 -> 1st, 2 -> 2nd, 3 -> 3rd, 4 -> 4th, 11->11th...
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def formatted_date(dt: datetime) -> str:
    # Matches {{date:dddd, MMMM Do, YYYY}}
    # e.g., "Sunday, August 10th, 2025"
    weekday = dt.strftime("%A")
    month   = dt.strftime("%B")
    year    = dt.strftime("%Y")
    day_ord = ordinal(int(dt.strftime("%d")))
    return f"{weekday}, {month} {day_ord}, {year}"

def open_with_xed(path: str):
    # Prefer system xed; scrub Python env
    env = os.environ.copy()
    for var in ("PYTHONHOME", "PYTHONPATH", "VIRTUAL_ENV", "PYENV_VERSION"):
        env.pop(var, None)
    # Make sure /usr/bin is early
    env["PATH"] = "/usr/bin:" + env.get("PATH", "")
    xed_bin = "/usr/bin/xed" if os.path.exists("/usr/bin/xed") else shutil.which("xed") or "xed"
    subprocess.run([xed_bin, path], env=env, check=False)

def main():
    today = datetime.now()
    fname_date = today.strftime("%Y-%m-%d")
    out_path = os.path.join(output_dir, f"{fname_date}.md")
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(out_path):
        # Don’t overwrite; just open
        open_with_xed(out_path)
        return

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the date placeholder if present
    date_str = formatted_date(today)
    if "{{date:dddd, MMMM Do, YYYY}}" in content:
        content = content.replace("{{date:dddd, MMMM Do, YYYY}}", date_str, 1)
    else:
        # If template doesn’t have the token, put a header at the top
        header = f"# Daily Journal - {date_str}\n\n"
        content = header + content

    # Write new file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Open it
    open_with_xed(out_path)

if __name__ == "__main__":
    main()
