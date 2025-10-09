# Vim

## Modes
- **Normal mode** → default mode (navigate, issue commands)  
- **Insert mode** → edit text (`i`, `a`, `o`)  
- **Visual mode** → select text (`v`, `V`, `Ctrl+v`)  
- **Command-line mode** → `:` commands (write, quit, search, etc.)  

---

## Starting & Exiting
- `vim file.txt` → open file  
- `:q` → quit  
- `:q!` → quit without saving  
- `:w` → save  
- `:wq` or `:x` → save and quit  
- `ZZ` → save and quit (shortcut)  

---

## Navigation
- `h` → left  
- `l` → right  
- `j` → down  
- `k` → up  
- `0` → beginning of line  
- `^` → first non-blank of line  
- `$` → end of line  
- `gg` → top of file  
- `G` → bottom of file  
- `:n` → go to line *n*  
- `Ctrl+d` → half page down  
- `Ctrl+u` → half page up  

---

## Inserting Text
- `i` → insert before cursor  
- `I` → insert at beginning of line  
- `a` → append after cursor  
- `A` → append at end of line  
- `o` → open new line below  
- `O` → open new line above  

---

## Editing
- `x` → delete char under cursor  
- `dd` → delete line  
- `D` → delete from cursor to end of line  
- `yy` → yank (copy) line  
- `yw` → yank word  
- `p` → paste after cursor  
- `P` → paste before cursor  
- `u` → undo  
- `Ctrl+r` → redo  
- `.` → repeat last command  

---

## Visual Mode
- `v` → charwise selection  
- `V` → linewise selection  
- `Ctrl+v` → blockwise selection  
- `y` → yank selection  
- `d` → delete selection  
- `>` / `<` → indent / unindent selection  

---

## Search & Replace
- `/pattern` → search forward  
- `?pattern` → search backward  
- `n` → repeat search  
- `N` → repeat search in opposite direction  
- `:%s/foo/bar/g` → replace all *foo* with *bar*  
- `:%s/foo/bar/gc` → replace with confirm  

---

## Buffers & Windows
- `:e file` → open another file  
- `:bn` → next buffer  
- `:bp` → previous buffer  
- `:bd` → delete buffer  
- `:sp file` → split window horizontally  
- `:vsp file` → split window vertically  
- `Ctrl+w w` → cycle windows  

---

## Marks & Jumps
- `ma` → set mark *a* at cursor  
- `` `a `` → jump to mark *a*  
- `` '' `` → jump back to last position  

---

## Configuration
- `:set number` → show line numbers  
- `:set relativenumber` → relative line numbers  
- `:syntax on` → enable syntax highlighting  
- `:set tabstop=4` → set tab width  
- `:set expandtab` → use spaces instead of tabs  
- `:set autoindent` → enable auto-indentation  

---

## Practical Notes
- **hjkl** = movement keys in normal mode.  
- Prefix commands with numbers: `10j` moves down 10 lines.  
- Combine operators + motions: `d$` = delete to end of line, `y}` = yank paragraph.  
- Use `.vimrc` to persist preferred settings.  