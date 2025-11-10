# Lab 4.2 — Sockets & Port Probing 


In this lab We'll lok at TCP/UDP probing with `socket`, implement concurrency, perform lightweight banner grabbing, and start basic service fingerprinting.  

## Safety / Ethics

**Only** run scans against provided lab targets, local VMs, or systems for which you have explicit permission. Keep scans light (small worker counts, short timeouts) and record all activity in `lab4-2_activity.log`.


## Learning objectives

By the end of this lab you should be able to:

- Use Python `socket` to attempt TCP and (basic) UDP connections.
- Implement concurrent port scans using `concurrent.futures.ThreadPoolExecutor`.
- Write robust code with timeouts and exception handling.
- Perform simple banner grabs for service hints (HTTP, SMTP, SSH).
- Save scan results to CSV/JSON and produce a short summary.
- Understand safe scanning practices and rate-limiting.


## Initial Lab Setup

1. Reuse the same Codespaces virtual environment from Lab 4.1, or create a new one:

3. Create a lab folder and an activity log:
   ```bash
   mkdir lab4_2
   cd lab4_2
   touch lab4-2_activity.log
   ```


## Phase 1 — Quick primer on sockets 

**Step 1 — Interactive socket test**

Run this quick Python snippet to understand TCP connect behavior and timeouts. 

```python
# quick_socket_demo.py
import socket, sys, time

host = "scanme.nmap.org"
port = 22  # try different ports

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3.0)  # 3 second timeout
start = time.time()
try:
    s.connect((host, port))
    print(f"Connected to {host}:{port}")
    s.close()
except socket.timeout:
    print("Connection timed out")
except socket.error as e:
    print(f"Socket error: {e}")
finally:
    print(f"Elapsed: {time.time()-start:.2f}s")
```

> Run the quick_socket_demo.py and try connect to lots of different common ports (80,443,21,8080 etc)

**What you should observe / talk-through:**

- `connect()` returns quickly for open ports; for closed ports it may raise `ConnectionRefusedError`.
- For filtered ports (blocked by firewall) `connect()` may time out.
- Timeouts prevent your program from blocking indefinitely — always set them.


## Phase 2 — Single-port probe & CLI 

### Task 2.1 — Implement `lab4-2_probe.py` (single-port checker)

Create `lab4-2_probe.py`:

```python
#!/usr/bin/env python3
# lab4-2_probe.py
import socket, sys

def probe_tcp(host, port, timeout=3.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, int(port)))
        s.close()
        return True, None
    except socket.timeout:
        return False, "timeout"
    except ConnectionRefusedError:
        return False, "refused"
    except socket.gaierror:
        return False, "name_error"
    except Exception as e:
        return False, str(e)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python lab4-2_probe.py <host> <port> [timeout]")
        sys.exit(1)
    host = sys.argv[1]
    port = sys.argv[2]
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
    open_, reason = probe_tcp(host, port, timeout)
    if open_:
        print(f"{host}:{port} is OPEN")
    else:
        print(f"{host}:{port} is CLOSED ({reason})")
```

**Exercises:**

- Run `python lab4-2_probe.py scanme.nmap.org 22` and `python lab4-2_probe.py scanme.nmap.org 9999` and note results.
- Try a few other common and random ports [List of common ports](https://www.stationx.net/common-ports-cheat-sheet/)
- Save outputs and add a short note in `lab4-2_activity.log` describing what each result means.


## Phase 3 — Range scan with concurrency 

### Task 3.1 — Implement `lab4-2_scan.py` (concurrent range scan)

Create `lab4-2_scan.py`:

```python
#!/usr/bin/env python3
# lab4-2_scan.py
import socket, argparse, concurrent.futures, json, time

def probe_tcp(host, port, timeout=2.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return (port, True, None)
    except socket.timeout:
        return (port, False, "timeout")
    except ConnectionRefusedError:
        return (port, False, "refused")
    except Exception as e:
        return (port, False, str(e))

def parse_port_spec(spec):
    ports = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a,b = part.split("-",1)
            ports.update(range(int(a), int(b)+1))
        else:
            ports.add(int(part))
    return sorted(ports)

def scan_host(host, ports, workers, timeout):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as exe:
        futures = {exe.submit(probe_tcp, host, p, timeout): p for p in ports}
        for fut in concurrent.futures.as_completed(futures):
            results.append(fut.result())
    return sorted(results, key=lambda x: x[0])

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--host", required=True)
    p.add_argument("--ports", default="1-1024")
    p.add_argument("--workers", type=int, default=50)
    p.add_argument("--timeout", type=float, default=1.5)
    p.add_argument("--out", default="scan_results.json")
    args = p.parse_args()

    ports = parse_port_spec(args.ports)
    start = time.time()
    res = scan_host(args.host, ports, args.workers, args.timeout)
    elapsed = time.time() - start
    open_ports = [r for r in res if r[1]]
    print(f"Scan complete in {elapsed:.2f}s — {len(open_ports)} open ports found")
    output = {"host": args.host, "elapsed": elapsed, "results": []}
    for port, open_, reason in res:
        output["results"].append({"port": port, "open": open_, "reason": reason})
    with open(args.out, "w") as fh:
        json.dump(output, fh, indent=2)
    print(f"Wrote results to {args.out}")
```

**Exercises:**

- Run a small scan: `python lab4-2_scan.py --host scanme.nmap.org --ports 20-1024 --workers 30 --timeout 1.0`
- Observe runtime vs. port range vs. workers; record timings in `lab4-2_activity.log`.
- Load `scan_results.json` and identify open ports.

**Talk-through:**

- Increasing `workers` reduces runtime but increases load on both your machine and the target — keep within limits.
- Very small timeouts risk false negatives on slow services.
- try running the previous scan with different amounts of workers and various timeouts and record your observations


## Phase 4 — Banner grabbing & service hints 

### Task 4.1 — Implement `lab4-2_banner.py`

Create `lab4-2_banner.py`:

```python
#!/usr/bin/env python3
# lab4-2_banner.py
import socket, sys, json, time

def grab_banner_tcp(host, port, timeout=2.0, send_bytes=None, read_size=1024):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    banner = ""
    try:
        s.connect((host, port))
        if send_bytes:
            s.sendall(send_bytes)
        try:
            data = s.recv(read_size)
            banner += data.decode(errors='replace')
        except socket.timeout:
            pass
        s.close()
        return True, banner.strip()[:1000]
    except Exception as e:
        return False, str(e)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python lab2_banner.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    # Common probes for HTTP-like services (HTTP/1.0 simple request)
    probes = {
        "generic": None,
        "http_get": b"GET / HTTP/1.0\r\nHost: example\r\n\r\n",
        "smtp_helo": b"HELO example.com\r\n",
        "ssh": None
    }
    # try HTTP first
    ok, banner = grab_banner_tcp(host, port, send_bytes=probes["http_get"])
    if ok and banner:
        print("Banner (HTTP probe):")
        print(banner)
    else:
        ok, banner = grab_banner_tcp(host, port, send_bytes=probes["smtp_helo"])
        if ok and banner:
            print("Banner (SMTP probe):")
            print(banner)
        else:
            ok, banner = grab_banner_tcp(host, port, send_bytes=probes["generic"])
            print("Generic probe result:")
            print(banner)
```

**Exercises:**

- For each open port found in Phase 3, run `python lab4-2_banner.py scanme.nmap.org <port>` and save the banner to `banners.csv` or `banners.json`.
- Note common banner strings like `SSH-2.0-OpenSSH_7.6p1`, `220 smtp.example ESMTP`, `HTTP/1.1 200 OK` and `Server:` headers.

**Talk-through:**

- Banner content often gives service type and version — useful for fingerprinting or vulnerability lookup.
- Some services disable or hide banners; others return generic banners or nothing at all.
- Be careful: sending malformed probes can trigger IDS or break poor services — keep probes minimal.

## Phase 5 — Advanced 

### Task 5.1 — UDP "probe" (basic)

UDP is connectionless; you can't reliably "connect" to know open/closed. But you can send a packet and look for an ICMP port unreachable response (not possible with plain `socket` reliably without raw sockets). For this lab we'll implement a simple UDP probe that sends a small datagram and waits for a response — useful for DNS (port 53) or other UDP services.

```python
# udp_probe.py (simple)
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(2.0)
host = "1.1.1.1" #cloudfare dns try using 8.8.8.8 Google dns and also scanme.nmap.org
port = 53
s.sendto(b"\x00", (host, port))
try:
    data, addr = s.recvfrom(512)
    print("Received reply, service likely up")
except socket.timeout:
    print("No reply (could be closed/filtered or service not responding)")
```

**Notes:** UDP is unreliable; you'll often get no replies, so filter or not responding is most likley. 

### Task 5.2 — Passive hints (TTL and SYN window) — discussion only

- Observing TTL and TCP window sizes from SYN/ACK can offer OS/service hints, but requires raw packets or `scapy` and more privileges. For this lab, discuss trade-offs and ethical concerns. If the instructor permits, you can try a `scapy` exercise in a follow-up session.




## Task 5.1 — Improved UDP probing (reliable-ish checks for UDP services)

**Goal:** Send protocol-appropriate UDP packets to candidate ports (e.g., DNS port 53, NTP 123) and interpret responses; use ICMP “port unreachable” indications where possible. This exercise uses normal UDP sockets (no raw sockets required) and an optional raw-socket helper (requires root) to listen for ICMP unreachable messages for better detection.

> The scripts need to run as `root` (use `sudo`).

## Task 5.3 — Simple UDP probe (stateless, quick) — works for services that respond (DNS, echo)

**Script:** `udp_probe_simple.py`
```python
#!/usr/bin/env python3
# udp_probe_simple.py
import socket, sys, time

def udp_probe(host, port, payload=b"\x00", timeout=2.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        start = time.time()
        s.sendto(payload, (host, port))
        data, addr = s.recvfrom(4096)
        elapsed = time.time() - start
        return {"host": host, "port": port, "reply": data[:200].hex() if isinstance(data, bytes) else str(data), "elapsed": elapsed}
    except socket.timeout:
        return {"host": host, "port": port, "reply": None, "elapsed": None}
    except Exception as e:
        return {"host": host, "port": port, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python udp_probe_simple.py <host> <port> [hex_payload]")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    payload = bytes.fromhex(sys.argv[3]) if len(sys.argv) > 3 else b"\x00"
    print(udp_probe(host, port, payload))
```

**How to run (student):**
```bash
python udp_probe_simple.py 1.1.1.1 53
python udp_probe_simple.py 1.1.11 53 "0000010000010000000000000377777706676f6f676c6503636f6d0000010001"
```

**What to record:**
- Save output to `udp_simple_results.json`.
- Note whether a reply was received.
- Try decode the sent and recieved hex to see what was sent.


## Phase 6 — Wrap-up, saving outputs & reflection 

**Files to save in `lab4-2/` folder:**

- `lab4-2_probe.py`  
- `lab4-2_scan.py`  
- `lab4-2_banner.py`  
- `scan_results.json` (from `lab4-2_scan.py`)  
- `banners.csv` or `banners.json` (banner outputs)  
- `lab4-2_activity.log` (notes: commands run, timings, anomalies)  
- `lab4-2_README.md` — short reflection (max 400 words) answering:
  - What open ports did you find, and which banners were most informative?
  - Any false negatives or timeouts encountered? Why?
  - One defensive recommendation for an admin to reduce information leakage.

**Suggested CSV format for banners (`banners.csv`):**

```
host,port,service_hint,banner_snippet
127.0.0.1,22,SSH,"SSH-2.0-OpenSSH_7.6p1"
127.0.0.1,80,HTTP,"HTTP/1.1 200 OK\nServer: nginx/1.18"
```

## Hints & common pitfalls

- Always set timeouts; default blocking sockets can hang your script.
- Use conservative defaults for `workers` (<50).
- JSON is easier to parse for autograding; CSV is easy to view.
- `ConnectionRefusedError` vs `timeout` — different meanings: refused = remote host replies “no service”; timeout = likely filtered or very slow.
- Banner grabbing must be light: one small request and a short read (`recv(1024)`).

## Optional extensions 

- Add **service fingerprinting heuristics**: match banners or header keywords to known services (e.g., `nginx`, `OpenSSH`, `Postfix`) and produce `service_hint`.
- Add **parallel banner grabbing** after scan results in `lab4-2_scan.py` to speed-up collection (use same `ThreadPoolExecutor`).
- Implement **rate limiting** between requests to a single host (sleep per N requests).
- Build a small **report generator** that reads `scan_results.json` and `banners.json` and outputs a Markdown summary.



