# Lab 1 — HTTP Basics: Requests, HTML Parsing & Response Analysis 

In this lab we'll learn foundational web reconnaissance skills in Python — making HTTP requests, parsing HTML, extracting metadata, and analyzing response headers.  

---

## Safety & Ethics
This lab and the following few labs covers fingerprinting and reconnaissance techniques that can be misused, and may be illegal if use incorrectly. 

Students must only run scans against local VMs or sites listed in the lab, or explicitly authorised targets where written permission exists.  
Unauthorized scanning or probing of third-party systems or networks is **illegal, so be careful**. You have been warned!!.  

---

## Learning objectives

By the end of this lab you should be able to:

- Use `requests` to send HTTP requests and handle common response codes.
- Parse HTML with `BeautifulSoup` to extract titles, meta tags, and forms.
- Collect and interpret HTTP response headers for basic fingerprinting.
- Write modular Python scripts with error handling and structured JSON outputs.
- Reflect on how reconnaissance data can be used responsibly.

---

## Time plan (approx.)

| Phase | Activity | Time |
|-------|----------|------|
| 1 | Setup & warm-up | 30 min |
| 2 | HTTP requests & header analysis | 60 min |
| 3 | HTML parsing & metadata extraction | 75 min |
| 4 | Header fuzzing & optional challenges | 45 min |
| 5 | Reflection & submission prep | 30 min |

---

## Pre-lab setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate     # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```

3. Confirm you can reach the lab targets provided by the instructor. Example quick test:
   ```python
   import requests
   r = requests.get("http://localhost:8001")
   print(r.status_code)
   ```

> Instructor note: provide 2–3 local web apps (e.g. `http://localhost:8001`, `http://localhost:8002/login`, `http://localhost:8003/blog`) with slight variations in headers, meta tags and forms so students observe differences.

---

## Phase 1 — Warm-up & small demo (30 min)

- Instructor demo: run `curl -I http://localhost:8001` and `curl http://localhost:8001` to show headers and body.
- Quick Python demo (interactive) showing `requests.get()` and printing `response.status_code`, `response.headers`, and `response.text[:200]`.

---

## Phase 2 — HTTP Requests & Header Analysis (60 min)

### Task 2.1 — Basic GET with `requests`

Create a file `lab1_get.py`:

```python
#!/usr/bin/env python3
# lab1_get.py
import requests
import sys

def simple_get(url):
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        print(f"[+] URL: {url}")
        print(f"    Status Code: {r.status_code}")
        print(f"    Final URL:   {r.url}")
        print(f"    Content-Type: {r.headers.get('Content-Type', 'N/A')}")
        print(f"    Server:       {r.headers.get('Server', 'N/A')}")
        print(f"    Content-Length: {r.headers.get('Content-Length', 'Unknown')}")
        return r
    except requests.exceptions.RequestException as e:
        print(f"[!] Request error for {url}: {e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python lab1_get.py <url>")
        sys.exit(1)
    simple_get(sys.argv[1])
```

**Exercises:**

- Run against each lab URL. Observe status codes (200 / 301 / 404 / 500).
- Try non-existent paths (`/thispagedoesnotexist`) and note the behavior.
- Inspect `Server` header values and discuss what they might reveal.

---

### Task 2.2 — Collecting headers across many pages

Create a script to query a list of URLs and save header summaries to `headers.json`:

```python
#!/usr/bin/env python3
# lab1_collect_headers.py
import requests, json, sys

def collect(urls, out_file="headers.json"):
    results = []
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            results.append({
                "url": url,
                "status": r.status_code,
                "final_url": r.url,
                "server": r.headers.get("Server"),
                "content_type": r.headers.get("Content-Type"),
                "content_length": r.headers.get("Content-Length")
            })
        except requests.exceptions.RequestException as e:
            results.append({"url": url, "error": str(e)})
    with open(out_file, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"Wrote {len(results)} entries to {out_file}")

if __name__ == '__main__':
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python lab1_collect_headers.py <url1> <url2> ...")
        sys.exit(1)
    collect(urls)
```

**Exercises:**

- Run for all lab targets and view `headers.json`.
- Discuss variations and what is actionable information.

---

## Phase 3 — HTML Parsing & Metadata Extraction (75 min)

### Task 3.1 — Extract title, meta description, and forms

Create `lab1_parse.py`:

```python
#!/usr/bin/env python3
# lab1_parse.py
from bs4 import BeautifulSoup
import requests, json, sys, urllib.parse

def parse_page(url, out_file=None):
    r = requests.get(url, timeout=5)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else None
    meta = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta["content"].strip() if meta and meta.get("content") else None

    forms = []
    for f in soup.find_all("form"):
        method = f.get("method", "GET").upper()
        action = urllib.parse.urljoin(url, f.get("action", ""))
        inputs = []
        for inp in f.find_all("input"):
            inputs.append({
                "name": inp.get("name"),
                "type": inp.get("type"),
                "value": inp.get("value")
            })
        forms.append({"method": method, "action": action, "inputs": inputs})

    result = {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "forms": forms
    }

    if out_file:
        with open(out_file, "w") as fh:
            json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python lab1_parse.py <url> [out_file.json]")
        sys.exit(1)
    parse_page(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
```

**Exercises:**

- Run it against each target and save `page_meta.json` files.
- Inspect forms: are there login forms? hidden fields? suspicious parameters?
- Note title and meta descriptions — are they meaningful?

---

### Task 3.2 — Keyword scanning in page text (optional)

Add a small keyword search to `lab1_parse.py` to count occurrences of keywords like `admin`, `login`, `debug`, `error`.

```python
keywords = ["admin", "login", "debug", "error"]
text = soup.get_text(separator=" ").lower()
kw_counts = {k: text.count(k) for k in keywords}
result["keyword_counts"] = kw_counts
```

**Exercise:** Run and compare counts across different lab sites.

---

## Phase 4 — Header Fuzzing & Hidden Clues (45 min)

### Task 4.1 — User-Agent variation

Create `lab1_header_probe.py`:

```python
#!/usr/bin/env python3
# lab1_header_probe.py
import requests, sys, csv

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl/7.68.0",
    "sqlmap/1.5.4",
    "Nikto/2.1.6",
    "python-requests/2.x"
]

def probe(url, out_csv=None):
    rows = []
    for ua in USER_AGENTS:
        headers = {"User-Agent": ua}
        try:
            r = requests.get(url, headers=headers, timeout=5)
            rows.append({
                "ua": ua,
                "status": r.status_code,
                "server": r.headers.get("Server", ""),
                "length": len(r.text)
            })
        except requests.exceptions.RequestException as e:
            rows.append({"ua": ua, "error": str(e)})
    if out_csv:
        with open(out_csv, "w", newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=["ua","status","server","length","error"])
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
    for r in rows:
        print(r)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python lab1_header_probe.py <url> [out.csv]")
        sys.exit(1)
    probe(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
```

**Exercises:**

- Run the probe and observe differences in `status`, `server`, and `length`.
- Does the server respond differently to `curl`, `sqlmap`, or `Nikto` user agents?

---

### Task 4.2 — Additional header tests (optional)

Try fuzzing or adding headers such as:

- `X-Forwarded-For: 1.2.3.4`
- `Referer: http://evil.example/`
- `Accept-Language: fr-FR`

**Exercise:** Log any changes in response status, body, or headers.

---

## Phase 5 — Reflection & submission (30 min)

Create `lab1_README.md` (max 400 words) addressing:

- Which server headers you observed — were they helpful?
- Differences between the target sites in headers, titles, forms, and keywords.
- One defensive use of this information.
- Ethical precautions you must follow when performing similar reconnaissance.

---

## Deliverables (what to submit)

Include in your submission folder:

- `lab1_get.py`  
- `lab1_collect_headers.py` (or combined script)  
- `lab1_parse.py`  
- `lab1_header_probe.py`  
- `headers.json` and/or `page_meta.json` produced during the lab  
- `lab1_README.md` (reflection and notes)

---

## Hints & common pitfalls

- Always set a timeout on network calls (`timeout=5`) to avoid long blocking waits.
- Use `allow_redirects=True` if you want the final landing page; check `response.history` to see redirects.
- Catch `requests.exceptions.RequestException` to handle connection errors, timeouts, and other problems.
- When joining relative form `action` attributes, use `urllib.parse.urljoin(base, action)`.
- Be mindful of lab rules: low worker counts, no scans against external networks, keep logs.

---

## Optional extension ideas (if you finish early)

- Detect common web frameworks via headers or URL paths (e.g., `X-Powered-By`, `/wp-login.php` → WordPress).
- Save a simple HTML snapshot of each page to a `snapshots/` folder for offline comparison.
- Add CLI flags to output JSON pretty-print or compact mode.
- Implement a small report generator that reads `headers.json` and `page_meta.json` and produces a Markdown summary.

---

If you'd like, I can:
- provide a zipped starter repo with all starter scripts and a `requirements.txt`, or  
- convert this Markdown into a ready-to-commit `lab1/README.md` in the canvas document. Which do you prefer?
