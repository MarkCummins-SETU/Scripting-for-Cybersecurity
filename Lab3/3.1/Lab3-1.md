# Command Line Power Lab

## Table of Contents

- [Overview](#overview)
- [Learning Outcomes](#learning-outcomes)
- [Setup & Getting Started](#setup--getting-started)
- [1. Basic Command-Line Power](#1-basic-command-line-power)
- [2. Bash Scripting Basics](#2-bash-scripting-basics)
- [3. Bash Functions & Simple Utilities](#3-bash-functions--simple-utilities)
- [4. Processing Text and Data](#4-processing-text-and-data)
- [5. Fetching Data with `curl` & `wget`](#5-fetching-data-with-curl--wget)
- [6. Hashing and Verification](#6-hashing-and-verification)
- [7. Putting It All Together — Mini Project](#7-putting-it-all-together---mini-project)
- [8. Reflection & Further Reading](#8-reflection--further-reading)
- [Appendix: Cheatsheet & Useful One-Liners](#appendix-cheatsheet--useful-one-liners)

---

## Overview
This lab guides you through essential command-line skills used extensively in cybersecurity: piping and redirection, text processing, automation with Bash, using `curl`/`wget` for web interaction, parallel host discovery, hashing, and combining small tools to build workflows. 

## Learning Outcomes
By the end of this lab you should be able to:

- Chain commands using pipes and redirection to build data-processing workflows.
- Write simple Bash scripts and functions to automate tasks.
- Use `grep`, `cut`, `sort`, `uniq`, and `xargs` to parse and act on textual data.
- Fetch web resources and interact with APIs using `curl` and `wget`.
- Produce cryptographic digests using `hashlib` (Python) and `openssl`.
- Combine the above tools into a small automation script.

---

## Setup & Getting Started

1. Confirm you have a Bash shell. The terminal on our Codespaces should be perfect.
2. Verify the following utilities are available:
   - `bash`, `grep`, `awk`, `cut`, `sort`, `uniq`, `xargs`  
   - `curl`, `wget`, `ping`, `ss` or `netstat`  
   - `python3` (for hashing examples)  

Run this quick check in your terminal:

```bash
echo "Hello, $(whoami)! Your lab starts now." && python3 --version && curl --version >/dev/null && wget --version >/dev/null
```

If any command fails, install the missing package using your distro's package manager (e.g. `apt`, `dnf`, `pacman`, `brew`). If you're using our usual Codespaces then everything should be working fine.

---

## 1. Basic Command-Line Power 

### Concept
Commands can be piped together; small tools do one thing well. Aliases shorten frequent commands.

### Demo commands

```bash
# chain and conditionals
ls -l | grep "\.sh$"
echo "Done!" && echo "Success" || echo "Fail"

# alias examples
alias ll='ls -la'
alias ports='ss -tuln'
```

### Exercise 1 

Create an alias called `myip` that prints IPv4 addresses from `ip a`. Make it persistent by adding it to `~/.bashrc`.

**Hint**:
```bash
echo "alias myip='ip -4 addr show | grep -oP "(?<=inet\s)\d+(\.\d+){3}"' >> ~/.bashrc
source ~/.bashrc
```

---

## 2. Bash Scripting Basics 

### Concept
A Bash script is a text file with a shebang (`#!/bin/bash`) and executable permissions.

### Example: `sysinfo.sh`

```bash
#!/bin/bash
# sysinfo.sh - small system info script

echo "Running system info..."
hostname
uptime
df -h
```

Save, make executable and run:
```bash
chmod +x sysinfo.sh
./sysinfo.sh
```

### Exercise 2 

Write `whoami.sh` that prints:

```
User: <your username>
Current dir: <where you are>
Date: <today’s date>
```

**Hints**: `whoami`, `pwd`, `date`

---

## 3. Bash Functions & Simple Utilities 

### Concept
Functions let you define commands inside your shell or `.bashrc` without creating separate files.

### Example 1 — `ping_sweep()`

```bash
ping_sweep() {
  subnet="172.17.0"
  for i in {1..10}; do
    ip="$subnet.$i"
    (ping -c1 -W1 $ip &>/dev/null && echo "[+] $ip alive") &
  done
  wait
}
```

Run with:
```bash
ping_sweep
```

#### Exercise 3a (5 min)
Modify `ping_sweep` so it accepts a subnet prefix as an argument:

Usage:
```bash
ping_sweep 10.0.0
```

#### Example 2 — `up()` simple checker

```bash
up() { ping -c1 "$1" &>/dev/null && echo "$1 is up" || echo "$1 is down"; }
```

Try:
```bash
up 8.8.8.8
up 172.17.0.1
```

#### Example 3 — `rot13()` fun

```bash
rot13() { echo "$1" | tr 'A-Za-z' 'N-ZA-Mn-za-m'; }
```

Try:
```bash
rot13 "Hello World"
rot13 "Uryyb Jbeyq"
```

#### Exercise 3b 
Create `check_ips()` that reads a filename and prints only the live IPs found in the file. Save output to `alive_hosts.txt`.

Hint: use `grep -Eo` to extract IPv4 addresses and `ping -c1 -W1` to test them.

---

## 4. Processing Text and Data 

### Concept
Small text utilities let you filter, extract fields, and build commands dynamically.

| Command | Purpose |
|---------|---------|
| `grep`  | search text using regex |
| `cut`   | extract fields by delimiter |
| `sort`  | sort lines |
| `uniq`  | remove or count duplicates |
| `xargs` | build/execute commands from input |

### Examples

```bash
# find users with bash shells
cat /etc/passwd | grep bash | cut -d: -f1

# word frequency from webpage
curl -sL example.com | tr -cs '[:alnum:]' '\n' | sort | uniq -c | sort -nr | head
```

### `xargs` examples

```bash
# ping two IPs from a single line
echo "8.8.8.8 1.1.1.1" | xargs -n1 ping -c1

# fetch headers for a list of urls
cat urls.txt | xargs -n1 curl -I
```

### Exercise 4 

Given `/etc/passwd`, list usernames that begin with `s` and output them sorted and unique.

**Hint**:
```bash
grep '^s' /etc/passwd | cut -d: -f1 | sort | uniq
```

---

## 5. Fetching Data with `curl` & `wget` 

### `curl` — quick web requests and APIs

```bash
# simple GET
curl https://example.com

# save to a file
curl -o index.html https://example.com

# follow redirects
curl -L https://bit.ly/something

# headers only
curl -I https://example.com

# POST data
curl -X POST -d "user=admin&pass=1234" https://httpbin.org/post

# pretty-print JSON (if jq installed)
curl -s https://api.ipify.org?format=json | jq .
```

### `wget` — reliable downloads and mirroring

```bash
# download file
wget https://example.com/file.txt

# resume
wget -c https://example.com/bigfile.iso

# mirror site
wget -r -np -k https://example.com/

# download multiple files from list
wget -i urls.txt
```

### Exercises 
1. Use `curl` to fetch your public IP: `curl -s https://api.ipify.org?format=json`
2. Use `curl -I` to get headers from three different sites.
3. Create `downloads/` and use `wget -P downloads/ <url>` to save a file.

---

## 6. Hashing and Verification 

### Concept
Hashes (digests) are used for integrity checks and quick identity of data.

### Python-based `hashit` helper

```bash
hashit() {
  algo=${1:-sha256}
  shift
  if [ -z "$algo" ]; then
    echo "Usage: hashit <algo> <string_or_file> or pipe data"
    return 1
  fi
  if [ ! -t 0 ]; then
    # piped data
    python3 - "$algo" <<'PY'
import sys, hashlib
algo = sys.argv[1]
data = sys.stdin.buffer.read()
try:
    h = hashlib.new(algo)
except (ValueError, TypeError):
    sys.stderr.write(f"Algorithm not supported: {algo}\n")
    sys.exit(2)
h.update(data)
sys.stdout.write(h.hexdigest())
PY
    return
  fi
  for t in "$@"; do
    if [ -f "$t" ]; then
      python3 - "$algo" "$t" <<'PY'
import sys, hashlib
algo = sys.argv[1]
path = sys.argv[2]
try:
    h = hashlib.new(algo)
except (ValueError, TypeError):
    sys.stderr.write(f"Algorithm not supported: {algo}\n")
    sys.exit(2)
with open(path, 'rb') as f:
    for chunk in iter(lambda: f.read(8192), b''):
        h.update(chunk)
sys.stdout.write(h.hexdigest())
PY
    else
      python3 - "$algo" "$t" <<'PY'
import sys, hashlib
algo = sys.argv[1]
s = sys.argv[2].encode()
try:
    h = hashlib.new(algo)
except (ValueError, TypeError):
    sys.stderr.write(f"Algorithm not supported: {algo}\n")
    sys.exit(2)
h.update(s)
sys.stdout.write(h.hexdigest())
PY
    fi
  done
}
```

### Examples

```bash
hashit md5 "admin"
echo -n "secret" | hashit sha256
hashit blake2b /path/to/file.bin
```

### Exercise 6 

Use `hashit` to compute the `sha256` of `/etc/hosts` and compare the output with `sha256sum /etc/hosts`.

**Note:** `sha256sum` is a native command that may be more convenient for files: `sha256sum /etc/hosts`.

---

## 7. Putting It All Together — Mini Project (≈15 min)

### Project: `url_checker.sh`

Write a script that:
1. Reads `urls.txt` (one URL per line)
2. Uses `curl -o /dev/null -s -w "%{http_code}"` to check each URL
3. Prints only those with HTTP status `200`

Starter script:
```bash
#!/bin/bash
infile=${1:-urls.txt}
while IFS= read -r url; do
  [ -z "$url" ] && continue
  code=$(curl -o /dev/null -s -w "%{http_code}" "$url")
  if [ "$code" = "200" ]; then
    echo "[OK] $url"
  else
    echo "[FAIL $code] $url"
  fi
done < "$infile"
```

---

## 8. Reflection & Further Reading 

**Questions to consider:**

- Which commands would you use to automate subnet scanning and reporting?  
- How would you integrate Python scripts into a larger Bash-based automation pipeline?  

**Resources:**

- The Art of Command Line — https://github.com/jlevy/the-art-of-command-line  
- explainshell — https://explainshell.com  
- Bash Hackers Wiki — https://wiki.bash-hackers.org  
- OverTheWire: Bandit — https://overthewire.org/wargames/bandit/

---

## Appendix: Cheatsheet & Useful One-Liners

```bash
# Quick helpers
alias ll='ls -la'
rot13() { echo "$1" | tr 'A-Za-z' 'N-ZA-Mn-za-m'; }
up() { ping -c1 "$1" &>/dev/null && echo "$1 is up" || echo "$1 is down"; }

# Basic network enumerate (change subnet)
subnet="192.168.1"
for i in {1..254}; do (ping -c1 -W1 $subnet.$i &>/dev/null && echo "[+] $subnet.$i") & done; wait

# Extract emails from text files
grep -Eo "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}" *.txt | sort -u

# Word frequency
curl -sL example.com | tr -cs '[:alnum:]' '\n' | sort | uniq -c | sort -nr | head

# xargs example: request a list of urls
cat urls.txt | xargs -n1 -P4 curl -I

# Hash a string
python3 -c "import hashlib; print(hashlib.sha256(b'admin').hexdigest())"
```

---

