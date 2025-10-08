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
# Common command line tools

# Some Example functions
```bash
up() { ping -c1 "$1" &>/dev/null && echo "$1 is up" || echo "$1 is down"; }
```

```bash
check_ips() {
    for ip in $(grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' "$1"); do
        ping -c1 -W1 "$ip" &>/dev/null && echo "$ip alive"
    done
}
```

## bash scripts
Example: Network scanner
```bash
#!/bin/bash
subnet="192.168.1"
for i in {1..254}; do
  ip="$subnet.$i"
  (ping -c1 -W1 $ip &>/dev/null && echo "[+] $ip alive") &
done
wait
```

## Python: Interactive mode:

```bash
python3 -q
>>> import socket
>>> socket.gethostbyname(‘setu.ie’)

# One-liner mode:

python3 -c 'import hashlib;print(hashlib.md5(b"admin").hexdigest())'
```


# wget and curl
