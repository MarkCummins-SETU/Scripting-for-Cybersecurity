# Lab 2.3 — Attack Pattern Detection & Reporting 

In this lab we'll be adding some complex functionality onto our log analyser tool. There are a few bits of complicated code in this section, you're given most of the code so hopefully its not overwhelming. We'll use the snippets provided to add functionality to our final projects. The concepts are very common and you'll see similar ideas repeating. So keep the snippets are reference. 

Next Week we'll be starting on our first assignment, which will pull together all the bits from the last few labs.So make sure you at least understand anything we've done todate.

**Learning Outcomes**

* Parse timestamps and convert them into Python datetime objects.
* Detect time-windowed events (e.g., ≥5 failed attempts within 10 minutes).
* Build structured JSON records for detected incidents.
* Produce a simple visualisation (bar chart) of top attacking IPs (optional).

---

## Setup

* We'll need matplotlib installed (for bonus section on plotting): `pip install matplotlib`
* Provided files: `sample_auth_small.log`
* Starter script: `lab2.3_starter.py`


---

## Task 1 — Parse auth lines into timestamp lists (25 minutes)

1. Let's start again by looking at our starter script and try understand what exactly it is doing, then run the script to ensure parsing works.  
2. For each IP, store a sorted list of datetime objects representing failed attempt times.  
3. Use per_ip_timestamps[ip].sort() after populating.  

**Hints**

* If a timestamp fails to parse, print the offending line for debugging.
* Use datetime.strptime with format "%Y %b %d %H:%M:%S" when prepending year 2025.

**Expected sample printout**

```python
{
  "203.0.113.45": [
      "Mar 10 13:45:01",
      "Mar 10 13:45:12",
      "Mar 10 13:45:25",
      "Mar 10 13:45:37",
      ...
  ],
  "203.0.113.46": [
      "Mar 10 13:46:42",
      "Mar 10 13:46:55",
      "Mar 10 13:47:10",
      ...
  ],
  "198.51.100.99": [
      "Mar 10 13:50:30",
      "Mar 10 13:50:43",
      ...
  ],
  "203.0.113.200": [
      "Mar 10 13:53:02",
      "Mar 10 13:53:14",
      ...
  ],
  ...
}
```

## Task 2 — Detect brute-force bursts (45 minutes)

* Goal: For each IP, detect any window where ≥5 failures occur within 10 minutes.

To solve this we're going to using 'sliding window' technique that will allow us to search efficiently across large log files..  

> Algorithm (sliding window):
> * For each IP get the sorted timestamp list t0...tn.
> * For each timestamp t[i], find the index j such that t[j] - t[i] <= 10 minutes and t[j+1] - t[i] > 10 minutes (or j is last).
> * If j - i + 1 >= 5, record an incident with:
> * IP
> * count of attempts in that window
> * first timestamp t[i]
> * last timestamp t[j]

Starter code snippet

```python
from datetime import timedelta

incidents = []
window = timedelta(minutes=10)
for ip, times in per_ip_timestamps.items():
    times.sort()
    n = len(times)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and (times[j+1] - times[i]) <= window:
            j += 1
        count = j - i + 1
        if count >= 5:
            incidents.append({
                "ip": ip,
                "count": count,
                "first": times[i].isoformat(),
                "last": times[j].isoformat()
            })
            # advance i past this cluster to avoid duplicate overlapping reports:
            i = j + 1
        else:
            i += 1
```

---

* Print number of incidents and the first 5 incidents.

**Expected sample**

```
Detected 3 brute-force incidents
{'ip': '203.0.113.45', 'count': 7, 'first': '2025-03-10T13:55:01', 'last': '2025-03-10T13:58:02'}
...
```

## Task 3 — Generate report & (optional) bar chart (30 minutes)

*Save incidents to bruteforce_incidents.txt (pretty printed)
* Create a summary of top offending IPs (total failed counts) and save to output report.
* Optional: plot a bar chart of top 10 attacker IPs using matplotlib:


```python
import matplotlib.pyplot as plt
# sample data
ips = ['203.0.113.45','203.0.113.46','198.51.100.99']
counts = [45, 32, 20]
plt.figure(figsize=(8,4))
plt.bar(ips, counts)
plt.title("Top attacker IPs")
plt.xlabel("IP")
plt.ylabel("Failed attempts")
plt.tight_layout()
plt.savefig("top_attackers.png")
plt.show()
```

**Troubleshooting & Hints**

* If datetime.strptime throws an error, print the line and the ts_str for debugging.
* Ensure lists are sorted before sliding-window logic.
* For large logs, avoid an O(n^2) algorithm; sliding window using two pointers is O(n) per IP (the snippet provided is linear because i and j only move forward).
* When testing, reduce the log to a subset (first 500 lines) for speed, then run full log.
