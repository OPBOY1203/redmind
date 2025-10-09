# Tmux commands and shortcuts

## Session Management
- Start new session:  
  `tmux`  

- Start with name:  
  `tmux new -s myname`  

- Attach:  
  `tmux a`  

- Attach named:  
  `tmux a -t myname`  

- List sessions:  
  `tmux ls`  

- Kill session:  
  `tmux kill-session -t myname`  

- Kill all sessions:  
  `tmux ls | awk '{print $1}' | tr -d ':' | xargs kill`  

---

## Prefix Key
- Default: `Ctrl+b`  
- (Commonly remapped to `Ctrl+a`)  

---

## Sessions
- `:new<CR>` → new session  
- `s` → list sessions  
- `$` → rename session  

---

## Windows (Tabs)
- `c` → create window  
- `w` → list windows  
- `n` → next window  
- `p` → previous window  
- `f` → find window  
- `,` → rename window  
- `&` → kill window  

---

## Panes (Splits)
- `%` → vertical split  
- `"` → horizontal split  
- `o` → swap panes  
- `q` → show pane numbers  
- `x` → kill pane  
- `+` → break pane into new window  
- `-` → restore pane from window  
- `Space` → toggle layouts  
- `{` → move pane left  
- `}` → move pane right  
- `z` → zoom toggle  

---

## Sync Panes
Enable across window:  
`:setw synchronize-panes on`  

Disable:  
`:setw synchronize-panes off`  

---

## Resize Panes
- `PREFIX : resize-pane -D` → resize down  
- `PREFIX : resize-pane -U` → resize up  
- `PREFIX : resize-pane -L` → resize left  
- `PREFIX : resize-pane -R` → resize right  
- Append number for amount:  
  `resize-pane -D 20`  

---

## Copy Mode
- Enter: `PREFIX [`  
- Exit: `Enter` or `q`  
- Enable vi keys:  
  `setw -g mode-keys vi`  

### Movement (vi mode)
- `h`/`l` → left/right  
- `j`/`k` → down/up  
- `0`/`$` → line start/end  
- `w`/`b` → next/prev word  
- `/pattern` → search forward  
- `?pattern` → search backward  

### Actions
- `Space` → start selection  
- `Enter` → copy selection  
- `p` → paste buffer  

---

## Misc
- `d` → detach  
- `t` → big clock  
- `?` → list shortcuts  
- `:` → command prompt  

---

## Common Config Options
```bash
# Remap prefix from 'C-b' to 'C-a'
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Mouse support
set -g mouse on

# 256 color terminal
set -g default-terminal "screen-256color"

# Activity alerts
setw -g monitor-activity on
set -g visual-activity on

# Center window list
set -g status-justify centre

# Vi-style keys in copy mode
setw -g mode-keys vi

# List of decent plugins - install tpm and "prefix +I"
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'jaclu/tmux-menus'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @plugin 'tmux-plugins/tmux-logging'

# Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)
run '~/.tmux/plugins/tpm/tpm'

# X clipboard support with yank plugin
set -g @yank_selection_mouse 'clipboard'
set -g @yank_selection 'clipboard'
```

## Zsh Helper for tmux

### Small helper you can drop in your .zshrc or .bashrc

Launching `tmux_main` from the terminal creates (or reattaches to) a session named `main`.

- **Window 1 – `main`**: Opens in the corresponding folder with two horizontal split panes.
- **Window 2 – `openvpn`**: Opens in the `openvpn` folder, then returns focus to the `main` window.

```bash
# add to ~/.zshrc, then: source ~/.zshrc
tmux_main() {
  local session="main"

  # attach if it already exists
  if tmux has-session -t "$session" 2>/dev/null; then
    tmux attach -t "$session"
    return
  fi

  # window 0: "main" in ~/tmux
  tmux new-session -d -s "$session" -n "main" -c "$HOME/tmux"

  # split panes (you used -v; swap to -h for side-by-side)
  tmux split-window -v -t "${session}:0" -c "$HOME/tmu"

  # window 1: "openvpn" in ~/vpn (create detached so it doesn't steal focus)
  tmux new-window -d -t "${session}:" -n "openvpn" -c "$HOME/vpn"

  # ensure we start on first window, left/top pane
  tmux select-window -t "${session}:0"
  tmux select-pane   -t "${session}:0.0"

  # attach
  tmux attach -t "$session"
}
```

