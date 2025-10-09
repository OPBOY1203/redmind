# Repo Sync Script

A simple Bash utility to automatically sync a local Git repository with its remote counterpart.  
This script is designed to run cleanly from cron jobs or manual execution without requiring interactive input.

---

## Features

- `set -euo pipefail` for safe execution
- Pulls the latest changes from the remote
- Adds and commits local changes
- Pushes updates back to the remote
- Works with SSH key authentication and GTK keyring via **keychain
