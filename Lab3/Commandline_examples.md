# The power of the Command Line

# Some quick examples

### Search all files in /etc for the word password
```bash
grep -r "password" /etc 2>/dev/null | head
```
### Rename all .jpeg to .jpg
```bash
for f in *.jpeg; do mv "$f" "${f%.jpeg}.jpg"; done
```
### Find all listening ports and print only port numbers
```bash
ss -tuln | awk 'NR>1 {print $5}' | cut -d: -f2 | sort -nu
```
### Extract all email addresses from a text dump
```bash
grep -Eo "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}" *.txt | sort -u
```

# Alias Examples:

```bash
alias ll='ls -lh --color=auto'

alias ports='ss -tuln'

alias top10='du -h * | sort -hr | head'
```
