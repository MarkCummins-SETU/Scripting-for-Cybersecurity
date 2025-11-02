# Lab 1 — HTTP Basics: Requests, HTML Parsing & Response Analysis 

In this lab we'll learn foundational web reconnaissance skills in Python — making HTTP requests, parsing HTML, extracting metadata, and analyzing response headers.  


## Safety & Ethics
This lab and the following few labs covers fingerprinting and reconnaissance techniques that can be misused, and may be illegal if use incorrectly. 

Students must only run scans against local VMs or sites listed in the lab, or explicitly authorised targets where written permission exists.  
Unauthorized scanning or probing of third-party systems or networks is **illegal, so be careful**. You have been warned!!.  


## Learning objectives

By the end of this lab you should be able to:

- Use `requests` to send HTTP requests and handle common response codes.
- Parse HTML with `BeautifulSoup` to extract titles, meta tags, and forms.
- Collect and interpret HTTP response headers for basic fingerprinting.
- Write modular Python scripts with error handling and structured JSON outputs.
- Reflect on how reconnaissance data can be used responsibly.


## Initial Lab setup

1. Create and activate a new codespace virtual environment:

2. Install dependencies from the terminal:
   ```bash
   pip install requests beautifulsoup4
   ```

3. Confirm you can reach the lab targets. Example quick test:
   ```python
   import requests
   r = requests.get("http://scanme.namp.org")
   print(r.status_code)
   ```

> Check out the meaning of the returned [status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). 


## Phase 1 — Warm-up: Guided Step-by-Step Exercises 

Follow these steps, and run each listed command, record the results, and answer the short questions after each step in a text file called **phase1_notes.txt**  

The curl -i command is used to include the HTTP response headers in the output when making an HTTP request.  
Normally, when you run: ```curl https://example.com```  

You only get the response body — the content returned by the server (like HTML, JSON, etc.).  
But when you add the -i (or --include) flag: ```curl -i https://example.com```  

You get both the headers and the body, for example:

```bash
HTTP/1.1 200 OK
Date: Sat, 02 Nov 2025 16:25:00 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 1256
Connection: keep-alive
Server: Apache

<!doctype html>
<html>
<head>...</head>
<body>...</body>
</html>
```

**Common Uses**
Debugging HTTP responses  
To inspect what headers the server sends (cookies, content type, caching info, etc.)  

⚙️ Related Options
```bash
-I or --head	                     Fetch only the headers (no body).      
-v or --verbose	                  Show full request and response (headers, connection info, etc.).      
-s	Silent mode (no progress meter). Often combined as -sI for script use.      
```

### Step 1 — Quick HTTP header check with curl 

On the terminal in your codespace try run:
```bash
curl -I http://scanme.nmap.org
```

**What to look for: **  

- The first line shows the HTTP status (e.g. HTTP/1.1 200 OK or HTTP/1.1 301 Moved Permanently). That tells you whether the request succeeded or was redirected.  
- Server: often reveals the web server software (e.g. nginx/1.18.0, Apache/2.4.41). This is a quick fingerprint.  
- Content-Type: tells you what kind of payload to expect (HTML, JSON, etc.).  
- Location: appears on redirects and shows the new URL the client should follow.  

**Questions to answer in phase1_notes.txt:** 

1. What status line did you get and what does it mean?  

2. What is the Server header value? Is it specific (nginx/1.22) or generic?


### Step 2 — Fetch the full page body

On the terminal in your codespace try run:
```bash
curl http://scanme.nmap.org-o scanme.html
head -n 40 scanme.html
```

> Inspect the saved file and copy the first 10 non-empty lines into your phase1_page_head.txt.

**Questions to answer in phase1_notes.txt:** 

1. What is the <title> of the page (if present)?

2. Do you see any <form> elements? What are their action attributes (copy them)?

### Step 3 — Compare curl and requests 

> Run this quick Python snippet and save output to phase1_requests_output.txt:
```python3
import requests
r = requests.get("http://scanme.nmap.org", timeout=5)
print("Status:", r.status_code)
print("Final URL:", r.url)
print("Server header:", r.headers.get("Server"))
print("Content-Type:", r.headers.get("Content-Type"))
print("First 200 chars of body:\\n", r.text[:200].replace('\n','\\n'))
```

> Paste the printed output into phase1_requests_output.txt.

**What to look for:**

- Compare the Status and Final URL with the curl results. requests follows redirects by default; curl -I does not unless you use -L.   
- The Server header in Python should match the curl output; mismatches indicate different server behavior depending on client.  
- The start of the body helps confirm the page content and encoding.  


**Questions to answer in phase1_notes.txt:** 

1. Did requests and curl report the same status and server header?

2. If different, what header or other factor might explain it (redirects, default headers, user agent)?

### Step 4 — Inspect headers with a different User-Agent 

> Run this quick Python snippet and save output to phase1_requests_output.txt:
```bash
curl -i  -A "MyTestAgent/1.0" https://httpbin.org/headers
curl -i  https://httpbin.org/headers
```

**What to look for:**

- Some servers change behavior based on the User-Agent. They may block, redirect, or return different content-lengths.  
- Web application firewalls or simple server rules sometimes detect known scanning agents and respond differently.  

**Questions to answer in phase1_notes.txt:** 

1. Did the response change (status, server header, content-length) when the User-Agent was MyTestAgent/1.0?

2. If it had changed, what could that mean about the server’s defenses?

### Step 5 — Short synthesis

Open phase1_notes.txt and append a 4–6 line summary answering:

What three pieces of information from the steps above would be most useful in a reconnaissance report, and why?

One quick defensive suggestion an admin could use to reduce information leakage from headers.

End of Phase 1. Save all files (phase1_*.txt, phase1_page.html) into your lab folder — these will be referenced in later labs.
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
