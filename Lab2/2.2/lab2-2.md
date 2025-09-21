# Lab 2.2 — Data Structures & Counting

**Learning outcomes**

* Read text files line-by-line in Python.  
* Use dictionaries to count occurrences (frequency counting).  
* Sort dictionary items and select the top N entries.  
* Export simple results to CSV.  

---

## Setup

* Review the steps from lab 2 if needed and use the same repo as last week called  `lab-02` then open a new codespace for this lab.  
* You can use the provided `sample_auth_small.log` for testing your scripts.
* Toy can use the starter script file: `lab2-2_starter.py`

---

## Task 1 — Extract unique IPs (20 minutes)

Run python `lab2-2_starter.py` to see starter behavior.

Modify or create a small script to:

Read each line in `sample_auth_small.log`.

Extract IP addresses and build a set() of unique IPs.

Print:

Total lines read.

Number of unique IPs.

First 10 unique IPs (sorted).

Hints

Use line.split() and search for the token from.

Use set() to keep unique items.

Expected output example

Lines read: 120
Unique IPs: 18
First 10 IPs: ['192.0.2.13', '198.51.100.22', '203.0.113.45', ...]

Task 2 — Count failed login attempts per IP (30 minutes)

Using defaultdict(int) (or normal dict) count how many failed attempts each IP has.

Only count lines containing Failed password or Invalid user.

Print the counts for all IPs.

Starter snippet

from collections import defaultdict

counts = defaultdict(int)
with open("sample_auth_small.log") as f:
    for line in f:
        if "Failed password" in line or "Invalid user" in line:
            # extract ip
            ip = parse_line_for_ip(line)
            if ip:
                counts[ip] += 1
print(counts)


Expected output sample

defaultdict(<class 'int'>, {'203.0.113.45': 12, '203.0.113.46': 8, '198.51.100.99': 5})

Instructor demo (15 minutes)

Instructor shows:

How to sort dictionary items by value: sorted(counts.items(), key=lambda kv: kv[1], reverse=True)

How to print top N (e.g., top 5).

Quick explanation of CSV writing.

Task 3 — Top 5 attacker IPs and CSV export (25 minutes)

Produce a list of top 5 IPs by failed attempts and print them nicely:

Format: Rank. IP — Count

Write the full counts dictionary to failed_counts.csv with headers ip,failed_count.

Run your script on the larger mixed_logs_5000.log and time how long it takes. Print the elapsed time.

Timing hint

import time
start = time.time()
# run counting
end = time.time()
print("Elapsed:", end-start, "seconds")


Expected console output

Top 5 attacker IPs:
1. 203.0.113.45 — 45
2. 203.0.113.46 — 32
3. 198.51.100.99 — 20
...
Wrote failed_counts.csv
Elapsed: 0.12 seconds

Deliverables (at end of lab)

labA_solution.py (your final script).

failed_counts.csv (generated).

Short README (1 paragraph) describing how to run the script.

Simple assessment checklist (for TA/instructor)

Script runs without error on sample_auth_small.log. (Pass)

Counts look sensible and CSV file is present. (Pass)

Top 5 printed and sorted. (Merit)

Timed and ran on mixed_logs_5000.log and note added. (Distinction)

Extensions (if time)

Improve parse_line_for_ip to support parentheses, commas, or trailing punctuation.

Filter out known "good" IPs (e.g., Googlebot) before counting.

Add command-line args to specify input file and top-N.

Safety & Ethics

Remind students these logs are synthetic. Always respect privacy and law when handling real logs.
