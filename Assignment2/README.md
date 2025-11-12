

Key constraint (ethical): Students must run their tool only against the lab targets provided by the instructor or against an isolated VM image. Submissions must include a signed statement (electronic checkbox in LMS) confirming authorization.

Requirements (must be implemented)

Implement a command-line Python program named recon.py with the following functionality and flags:

--targets : path to a file containing one host per line (IP or hostname, optionally with port host:port).

--ports : either a comma-separated list or range spec (e.g., 80,443,8000-8100) to probe for each host.

--workers : number of concurrent workers for TCP probing (default 20).

--http : if set, attempt HTTP requests to discovered HTTP(S) services and extract title, meta description, and Server header.

--tls : if set, attempt to retrieve TLS certificate info for ports that appear to speak TLS.

--output : path prefix for results; produce results.json and results.csv.

--timeout : per-connection timeout in s
ChatGPT said:
Nice — makes sense. Below is a harder, production-quality project specification for your 2nd-year cybersecurity class. I’m being direct: this version forces students to think like an engineer (concurrency, resilience, real output schema, testing, packaging) and like an analyst (fingerprinting, TLS checks, evidence collection, ethics). Use it as-is or copy/paste into your LMS.

# Recon tool — Project specification

**Overview:** Using the skills from the labs, students will build a production-style, command-line Python reconnaissance tool recon.py that probes targets, enumerates services and HTTP apps, inspects TLS, fingerprints web stacks, and emits machine-readable reports. Emphasize concurrency, testability, robust error handling, reproducible outputs, and ethical compliance.

## Required deliverables (every student) - A git repository with:

1. recon.py (executable CLI entry point)
2. requirements.txt (List any packages to be included)
3. README.md with quickstart and examples
4. AUTHORISATION.txt (see above)
5. Example targets.txt used in testing
6. results.json and results.csv produced by your tool on the example targets
7. STYLE.md (short paragraph on design decisions & known limitations)
8. A short demo (max 5 minutes) showing the tool running on the example targets and explaining outputs, and program features.
9. Project Report, in got Repo, but also submitted to Blackboard with all required sections.



Mandatory program behavior & CLI flags
Implement recon.py with these flags and behaviors. Use argparse or equivalent.

Basic required flags (you already listed — must implement these exactly):

--targets PATH         Path to file (one host per line; allow host or host:port)
--ports PORTS          Comma list or ranges (e.g., 80,443,8000-8100)
--workers N            Concurrent TCP workers (default 20)
--http                 If set: probe discovered HTTP(S) services and extract title, meta description, Server header
--tls                  If set: attempt TLS retrieval for ports that speak TLS
--output PREFIX        Path prefix for results; tool writes PREFIX.results.json and PREFIX.results.csv
--timeout S            Per-connection timeout in seconds (float OK)
Additional required functionality (this is the “more challenging” part)
Implement the following features (all required):

TCP connect scan (not raw SYN)

For each host and each port in --ports, attempt a TCP connect.

Record status (open, closed, filtered/timeout).

Banner collection

For open ports, try to read the initial banner (up to 4096 bytes) using a non-blocking recv with configured timeout.

Save raw banner (hex-safe or base64 if binary) in results.

HTTP(S) probing

If the port responds and appears HTTP (basic heuristic: first bytes start with HTTP/ or response to GET), or if --http is passed:

Attempt http://host:port/ (and https:// if TLS detected or port commonly used).

Extract: HTTP status code, final URL (after redirects), HTML <title>, <meta name="description"> content if present, Server header, Set-Cookie headers (brief summary), and response body sample (first 4KiB).

Follow at most 5 redirects. Respect --timeout.

TLS certificate analysis (if --tls):

Perform a TLS handshake (SNI set to host) for ports that appear to speak TLS.

Extract:

Subject CN, SANs, Issuer CN, Validity period (notBefore, notAfter), public-key type/size, signature algorithm.

Whether the certificate is expired at runtime.

Chain length and whether a verification attempt to system CA would succeed (report success/failure).

Detect obvious weak parameters (RSA < 2048, ECDSA curve less secure than secp256r1, MD5 signature) and flag them.

Fingerprint web-application / CMS heuristic

Combine headers, banners, response body patterns, well-known file checks to suggest likely server/CMS/stack (e.g., Apache, Nginx, IIS, WordPress, Drupal, Django, Express, Tomcat). At minimum, implement:

Check for wp-login.php, xmlrpc.php for WordPress.

Check /robots.txt and /sitemap.xml presence.

Compute a favicon hash (first download /favicon.ico, take SHA256 of bytes) and include it in output (students need not compare to a database, but should include the hash).

Simple WAF detection via common headers (X-Sucuri-ID, Server: cloudflare, X-Mod-Security).

Structured output

Produce JSON (primary) and CSV (secondary). JSON schema must be consistent and include:

per-target -> per-port -> service metadata (see Output schema below).

CSV should be a flattened summary: one row per discovered open service with key columns (host, port, proto, service_hint, http_status, title, server_header, cert_subject_cn, cert_notAfter, banner_snippet, fingerprint_tags).

Concurrency & rate control

Respect --workers for TCP connects.

HTTP and TLS probes spawned after discovery should be done concurrently but limited (e.g., same worker pool).

Implement a simple global rate limiter (e.g., max X requests/sec) to avoid flooding — choose sane defaults and document them.

Resilience

Partial failures must not crash the tool. For unhandled exceptions, log stack trace to stderr and continue.

Support a --retry N flag (default 1) to retry transient failures with exponential backoff.

Resume & idempotence

If an output file already exists, recon.py should have --resume flag that loads previous results and only probes missing items. If resuming, append a resumed: true flag in JSON metadata.

Logging & verbosity

--verbose or -v for debug logs; default is minimal progress output.

All errors must be logged with clear messages.

Tests

Unit tests for parsing ports, concurrency logic, JSON writer, and fingerprint heuristics.

At least one integration test that spins up a simple local HTTP server (use Python's http.server) and verifies --http extraction.

No external scanners

Students may not call external binaries (nmap/masscan/nikto). They may use Python libraries (allowed list below). Violations → fail.

Allowed / Recommended libraries
(you may allow other standard libraries but require disclosure in README)

Standard library: socket, ssl, concurrent.futures, asyncio (if used), argparse, json, csv, hashlib, logging, re, time

Networking / HTTP: requests or httpx or aiohttp (students must pick and state choice)

TLS parsing: cryptography (for certificate parsing) OR ssl + pyOpenSSL

Testing: pytest

Packaging: pip, poetry or minimal requirements.txt

Students must not shell out to nmap, masscan, curl, or similar.

Output schema (example — minimal required fields)
JSON: top-level object

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
CSV: one row per (host,port)
Columns (must include): host,port,open,status_code,title,server_header,cert_subject_cn,cert_notAfter,banner_snippet,fingerprint_tags

Example CLI usage
# basic
python recon.py --targets targets.txt --ports 80,443,8000-8010 --workers 50 --http --tls --output lab1 --timeout 3

# resume
python recon.py --targets targets.txt --ports 1-1024 --output lab1 --resume

# with retries and verbose logging
python recon.py --targets t.txt --ports 80,443 --workers 30 --http --tls --retry 3 -v
Testing & grading harness (instructor)
Provide simple example targets (local VMs) and a reference results.json. Grading scripts should:

Run python recon.py on provided targets.txt with time limit (e.g., 15 minutes).

Compare JSON keys and CSV rows for correctness.

Run unit tests with pytest.

Marking rubric (example)
Total 100 marks.

Core functionality (50)

TCP scanning & correct open/closed detection: 15

HTTP extraction (title, meta, server): 10

TLS cert extraction & expiry detection: 10

Structured JSON + CSV output format & correctness: 10

Respect for --timeout, --workers: 5

Robustness & concurrency (15)

No crashes on network errors: 5

Concurrency works and speed reasonable: 5

Resume support and retries: 5

Code quality & tests (15)

Unit tests exist and pass: 6

Readme, Dockerfile, packaging: 4

Logging, CLI help, code style: 5

Fingerprinting & extras (10)

Reasonable fingerprint heuristics (CMS, WAF flags, favicon hash): 5

Useful banner parsing + chain of evidence: 5

Ethics & deliverables (10)

AUTHORIZATION.txt present + LMS checkbox: 5

Demo video + example outputs included: 5

Extra credit (up to 10 bonus):

Implement TLS cipher scanning and detect weak ciphers. (+4)

Implement favicon hash DB lookup to identify frameworks (+3)

Implement HTTP method brute/OPTIONS analysis and report unsafe methods (PUT/DELETE). (+3)

Late policy: decide locally; strongly recommend no late code unless documented.

Common pitfalls (callouts — be brutal)
Don’t swallow exceptions silently — failing silently is worse than failing loudly. Log the error and continue.

Avoid naive blocking per-target loops. Students who do single-threaded connect->http->tls will time out on moderately sized lists.

Don’t assume port 443 always TLS: try handshake detection before blindly SSL-wrapping.

Avoid storing raw binary as plain text in JSON — use base64 or hex for non-UTF8 banners.

Tests must not depend on external internet. Use local servers/VMs.

Example test target set (suggested for instructor)
lab1-vm1 → HTTP on 80 (nginx), TLS on 8443 (self-signed), demonstrates redirect.

lab1-vm2 → WordPress on 8080, has /wp-login.php.

lab1-vm3 → Plain TCP banner (custom service) on port 9000.

Provide these VM images or containers to students.

Grading automation tips (instructor)
Provide a small Python grader that:

Runs tool with fixed args,

Loads JSON and verifies presence/format of mandatory fields,

Verifies a small list of expected open ports and expected header values,

Runs unit tests and checks for AUTHORIZATION.txt.

Give students a deterministic seed lab so results are reproducible.

Milestones for students (recommended)
Week 1: CLI + port parsing + single-host TCP connect

Week 2: Concurrency + banner grabbing + JSON writer

Week 3: HTTP probe + HTML parsing (title/meta) + CSV writer

Week 4: TLS retrieval + cert parsing + resume support

Week 5: Tests + Dockerfile + README + demo

Submission checklist for students (must include)
 recon.py executable

 requirements.txt / pyproject.toml

 README.md with run examples

 AUTHORIZATION.txt with signature line

 results.json and results.csv (from provided example targets)

 Dockerfile

 tests/ with pytest tests

 Demo video uploaded to LMS

 LMS authorization checkbox checked

Quick example of expected JSON fragment (concrete)
{
  "targets": {
    "192.0.2.10": {
      "ports": {
        "80": {
          "status": "open",
          "banner": "HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\n...",
          "service_hint": "http",
          "http": {
            "status_code": 200,
            "title": "Lab VM",
            "meta_description": "demo",
            "server_header": "nginx/1.18.0",
            "final_url": "http://192.0.2.10/",
            "favicon_sha256": "8a4b..."
          }
        }
      }
    }
  }
}
Final blunt advice (TL;DR — you asked for brutal honesty)
This spec forces students to write software, not glue scripts. Expect many to panic at concurrency and TLS parsing — those are the real engineering gates. Grade harshly on reproducibility and tests; sloppy tools that “worked on my machine” are worthless. If you want to reduce workload, remove resume support and rate-limiter, but keep TLS and HTTP fingerprinting — those teach real, transferable skills.

Want me to:

produce a ready-made recon.py reference implementation (annotated, testable), or

craft the automated grader and example VM configs?

Say which and I’ll give a concrete plan and starter code.


## AUTHORISATION.txt

A file AUTHORISATION.txt inside the repo with a one-line statement:
```bash
I certify that I had explicit permission to run this tool against all submitted targets. — <Full Name>, <Student ID>, <Date>.
```

> Failure to include will be an automatic fail (no negotiation). No excuses.

> nmap.scanme.org, example.com are both acceptable targets, if you use anything else then include evidence that you have permission to scan the site.

## Project Report
Details that must be included in report.




