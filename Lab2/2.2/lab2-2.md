# Lab 2.2 — Data Structures & Counting

**Learning outcomes**

* Read text files line-by-line in Python.  
* Use dictionaries to count occurrences (frequency counting).  
* Sort dictionary items and select the top N entries.  
* Export simple results to CSV.  

---

## Setup

* Review the steps from [lab 2-1](../2.1/lab2-1.md) if needed and use the same repo as last week called  `lab-02` then open a new codespace for this lab.  
* You can use the provided [sample_auth_small.log](sample_auth_small.log) for testing your scripts.
* You should use the starter script file: [lab2-2_starter.py](lab2-2_starter.py)

---

## Task 1 — Extract unique IPs (25 minutes)

Before we jump into any tasks, have a quick look at this weeks starter script [lab2-2_starter.py](lab2-2_starter.py) and see if you can figure out what exactly it does.  

In the last lab we used regex to find all pattern's that match an IP address from the log files, but what if we had packet capture data with source and destination IP adresses? What if we only wanted to extract the source IPs and not all IPs?  

A better technique (especially with sturctured data like log files) is to use **token-based extraction**. So we basically want to split each line into seperate words or `tokens`. Then we look for a fixed string that we can use as an anchor point and then take the next token. Lets try with an example.

```
Mar 10 13:45:01 host1 sshd[1001]: Failed password for invalid user admin from 203.0.113.45 port 52300 ssh2
Mar 10 13:45:12 host1 sshd[1001]: Failed password for invalid user admin from 203.0.113.45 port 52301 ssh2
```

In the snippet from our logfile, we can see that if we wanted to extracted the port numbers, we could find the anchor string 'port' and then read the next value to get the port number. Below is a brief function from our starter script that attempts to do just that. Try get the function to work, then use it as a basis for your own function "ip_parse(line)" that uses **token-based extraction** to read the IP addresses from the logs. 

```python
def simple_parser(line):
    """
    looks for the substring ' port ' and returns the following port number.
    Returns None if no matching substring found.
    """
    if " port " in line:
        parts = line.split(). # splits the line into tokens, seperates by spaces by default
        try:
            anchor = parts.index("port")    # Find the position of the token "port", our anchor
            port = parts[anchor+1]          # the port value will be next token, anchor+1
            return port.strip()             # strip any trailing punctuation

        except (ValueError, IndexError):
            return None

    return None
```

> **Task 1.1**: Write you own ip_parse(line) function to extract all the IPs using **token-based extraction** for any line passed to it.  

> **Task 1.2**:  
> 1. Read each line in `sample_auth_small.log`.  
> 2. Extract IP addresses and build a set() of unique IPs.  
> 3.  Print:  
> * Total lines read.  
> * Number of unique IPs.  
> * First 10 unique IPs (sorted).  

** Hints **

* Use line.split() and search for the token from.  
* Use set() to keep unique items.  
* Use the function sorted(s) to sort a set or list

** Expected output example ** 

```bash
Lines read: 120
Unique IPs: 18
First 10 IPs: ['192.0.2.13', '198.51.100.22', '203.0.113.45', ...]
```

## Task 2 — Count failed login attempts per IP (30 minutes)

* Using defaultdict(int) (or normal dict) count how many failed attempts each IP has.  
* Only count lines containing Failed password or Invalid user.  
* Print the counts for all IPs.  

** Starter snippet **

```python
from collections import defaultdict

counts = defaultdict(int)           # Create a dictionary to keep track of IPs

with open("sample_auth_small.log") as f:
    for line in f:
        if "Failed password" in line or "Invalid user" in line:
            # extract ip
            ip = ip_parse(line)
            if ip:
                counts[ip] += 1
print(counts)
```

** Expected output sample **

defaultdict(<class 'int'>, {'203.0.113.45': 12, '203.0.113.46': 8, '198.51.100.99': 5})



## Task 3 — Top 5 attacker IPs and export (35 minutes)

* Produce a list of top 5 IPs by failed attempts and print them nicely:  
* Format: Rank. IP — Count. 
* Write the full counts dictionary to failed_counts.txt with headers ip,failed_count.  
* Run your script on the larger mixed_logs_5000.log and time how long it takes. Print the elapsed time.  

> You can use the follow snippet to help you sort your dictionary and return n elements.  
> Dictionaries can't be sorted easily hence the strange looking code. We'll cover what exactly it's doing in the next lecture.

```python
def top_n(counts, n=5):
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:n]
```

** Timing hint ** 

```python
import time
start = time.time()
# run counting
end = time.time()
print("Elapsed:", end-start, "seconds")
```

** Expected console output **

```
Top 5 attacker IPs:
1. 203.0.113.45 — 45
2. 203.0.113.46 — 32
3. 198.51.100.99 — 20
...

Wrote failed_counts.txt
Elapsed: 0.12 seconds
```


## Safety & Ethics

** Log files can contain a huge amount of valuable company data, so never share real logs in public repos. The logs for this lab are synthetic, and created just for our lab. Always respect privacy and company data when handling real logs. **
