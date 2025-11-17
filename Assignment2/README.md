# Recon tool — Project specification

**Overview:** Using the skills from the labs, students will build a production-style, command-line Python reconnaissance tool recon.py that probes targets, enumerates services and HTTP apps, inspects TLS, fingerprints web stacks, and emits machine-readable reports. Emphasize concurrency, testability, robust error handling, reproducible outputs, and ethical compliance.

- **This is a very challenging project that should be completed as individuals.**
- **The project spec is very detailed, and includes lots of advance tasks that I'd expect only the very best students to complete.**
- **Don't panic. Start with the sample code from the labs, and add one function/feature at a time. Make sure it works well then try add another. Small Steps**
- **Do your best, Implement as much as you can**
- **Feel free to ask me questions (In labs, lecture or online)**  
- **Remeember sloppy tools that “worked on my machine” are worthless**

> You should use the sample code from the labs, however marks will only be awards for additional functionality added to the lab code.



## Required deliverables (every student) - A git repository with:

1. recon.py (executable CLI entry point)
2. requirements.txt (List any packages to be included)
3. README.md with quickstart and examples
4. AUTHORISATION.txt (see below)
5. Example targets.txt used in testing
6. results.json and results.csv produced by your tool on the example targets
7. STYLE.md (short paragraph on design decisions & known limitations)
8. A short video demo (max 5 minutes) showing the tool running on the example targets and explaining outputs, and program features.
9. Project Report, in got Repo, but also submitted to Blackboard with all required sections.


## Program behavior & CLI flags
Implement recon.py with these flags and behaviors. Use argparse or equivalent.

Basic required flags (Must implement these exactly. As many as you can):
```
--targets PATH         Path to file (one host per line; allow host or host:port)  
--ports PORTS          Comma list or ranges (e.g., 80,443,8000-8100)  
--workers N            Concurrent TCP workers (default 20)  
--http                 If set: probe discovered HTTP(S) services and extract title, meta description, Server header  
--tls                  If set: attempt TLS retrieval for ports that speak TLS  
--output PREFIX        Path prefix for results; tool writes PREFIX.results.json and PREFIX.results.csv  
--timeout S            Per-connection timeout in seconds (float OK)  
```

## Implement as much of the following functionality:

1. TCP connect scan (not raw SYN)  
- For each host and each port in --ports, attempt a TCP connect.  
- Record status (open, closed, filtered/timeout).  

2. Banner collection  
- For open ports, try to read the initial banner (up to 4096 bytes) using a non-blocking recv with configured timeout.
- Save raw banner (hex-safe or base64 if binary) in results.

3. HTTP(S) probing
- If the port responds and appears HTTP (basic heuristic: first bytes start with HTTP/ or response to GET), or if --http is passed:
- Attempt http://host:port/ (and https:// if TLS detected or port commonly used).
- Extract: HTTP status code, final URL (after redirects), HTML <title>, <meta name="description"> content if present, Server header, Set-Cookie headers (brief summary), and response body sample (first 4KiB).
- Follow at most 5 redirects. Respect --timeout.

4. TLS certificate analysis (if --tls):
- Perform a TLS handshake (SNI set to host) for ports that appear to speak TLS.
**Extract:**
- Subject CN, SANs, Issuer CN, Validity period (notBefore, notAfter), public-key type/size, signature algorithm.
- Whether the certificate is expired at runtime.
- Chain length and whether a verification attempt to system CA would succeed (report success/failure).
- Detect obvious weak parameters (RSA < 2048, ECDSA curve less secure than secp256r1, MD5 signature) and flag them.

5. Fingerprint web-application / CMS heuristic
- Combine headers, banners, response body patterns, well-known file checks to suggest likely server/CMS/stack (e.g., Apache, Nginx, IIS, WordPress, Drupal, Django, Express, Tomcat). At minimum, implement:
- Check for wp-login.php, xmlrpc.php for WordPress.
- Check /robots.txt and /sitemap.xml presence.
- Compute a favicon hash (first download /favicon.ico, take SHA256 of bytes) and include it in output (students need not compare to a database, but should include the hash).
- Simple WAF detection via common headers (X-Sucuri-ID, Server: cloudflare, X-Mod-Security).

6. Structured output
- Produce JSON (primary) and CSV (secondary). JSON schema must be consistent and include:
- per-target -> per-port -> service metadata (see Output schema below).
- CSV should be a flattened summary: one row per discovered open service with key columns (host, port, proto, service_hint, http_status, title, server_header, cert_subject_cn, cert_notAfter, banner_snippet, fingerprint_tags).

7. Concurrency & rate control
- Respect --workers for TCP connects.
- HTTP and TLS probes spawned after discovery should be done concurrently but limited (e.g., same worker pool).
- Implement a simple global rate limiter (e.g., max X requests/sec) to avoid flooding — choose sane defaults and document them.

8. Resilience
- Partial failures must not crash the tool. For unhandled exceptions, log stack trace to stderr and continue.
- Support a --retry N flag (default 1) to retry transient failures with exponential backoff.
- Resume & idempotence
- If an output file already exists, recon.py should have --resume flag that loads previous results and only probes missing items. If resuming, append a resumed: true flag in JSON metadata.

9. Logging & verbosity
- --verbose or -v for debug logs; default is minimal progress output.
- All errors must be logged with clear messages.
  

## No external scanners

Students may not call external binaries (nmap/masscan/nikto). They may use Python libraries (allowed list below). Violations → fail.

### Allowed / Recommended libraries

> You may allow other standard libraries but require disclosure in README

- Standard library: socket, ssl, concurrent.futures, asyncio (if used), argparse, json, csv, hashlib, logging, re, time
- Networking / HTTP: requests or httpx or aiohttp (students must pick and state choice)
- TLS parsing: cryptography (for certificate parsing) OR ssl + pyOpenSSL

## Output schema (example — minimal required fields)
JSON: top-level object
```
{
  "meta": {
    "run_started": "2025-11-12T12:34:56Z",
    "args": { "...": "..." },
    "resumed": false
  },
  "targets": {
    "192.0.2.1": {
      "ports": {
        "80": {
          "status": "open",
          "banner": "base64-or-utf8-snippet",
          "service_hint": "http",
          "http": {
            "url": "http://192.0.2.1:80/",
            "final_url": "...",
            "status_code": 200,
            "title": "Example",
            "meta_description": "desc",
            "server_header": "nginx/1.18",
            "cookies": ["sessionid=...; HttpOnly"],
            "favicon_sha256": "abcd..."
          },
          "tls": null,
          "fingerprint_tags": ["nginx", "wordpress?"],
          "scanned_at": "2025-11-12T12:35:01Z"
        },
        "443": {
          "status": "open",
          "tls": { "subject_cn": "example.com", "notAfter": "...", "expired": false, "weak_params": [] }
        }
      }
    }
  }
}
```
CSV: one row per (host,port)
Columns (must include): host,port,open,status_code,title,server_header,cert_subject_cn,cert_notAfter,banner_snippet,fingerprint_tags

Example CLI usage
### basic
python recon.py --targets targets.txt --ports 80,443,8000-8010 --workers 50 --http --tls --output lab1 --timeout 3

### resume
python recon.py --targets targets.txt --ports 1-1024 --output lab1 --resume

### with retries and verbose logging
python recon.py --targets t.txt --ports 80,443 --workers 30 --http --tls --retry 3 -v
Testing & grading harness (instructor)
Provide simple example targets (local VMs) and a reference results.json. 



# Marking rubric (Total 100 marks)

**Core functionality (45)**  
-TCP scanning & correct open/closed detection: (+10)
-HTTP extraction (title, meta, server): (+10)  
-TLS cert extraction & expiry detection: (+10)  
-Structured JSON + CSV output format & correctness: (+10)  
-Respect for --timeout, --workers: (+5)  

**Robustness & concurrency (15)**  
- No crashes on network errors: (+5)
- Concurrency works and speed reasonable: (+5)
- Resume support and retries: (+5)

**Code quality (5)**  
- Repo layout and structure (+2)
- Readme (+1)
- Logging, CLI help, code style: (+2)

**Fingerprinting & extras (15)**  
- Reasonable fingerprint heuristics (CMS, WAF flags, favicon hash): (+3)
- Useful banner parsing + chain of evidence: (+3)
- Implement TLS cipher scanning and detect weak ciphers. (+3)
- Implement favicon hash DB lookup to identify frameworks (+3)
- Implement HTTP method brute/OPTIONS analysis and report unsafe methods (PUT/DELETE). (+3)

**Report & Demonstration (20)**  
- Demo video presentation: (+10)
- Final Report (+10)


## AUTHORISATION.txt

A file AUTHORISATION.txt inside the repo with a one-line statement:
```bash
I certify that I had explicit permission to run this tool against all submitted targets. — <Full Name>, <Student ID>, <Date>.
```

> Failure to include will be an automatic fail (no negotiation). No excuses.

> nmap.scanme.org, example.com are both acceptable targets, if you use anything else then include evidence that you have permission to scan the site.

## Project Report
Details that must be included in report.
- Title page
- Link to Github Repo (Private + add me)
- References
- Clearly outline features implemented or attempted.
- Reflection on project, how difficult was it, what you learned or struglled with etc.
