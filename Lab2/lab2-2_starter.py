# lab2-2_starter.py
import csv
from collections import defaultdict

LOGFILE = "sample_auth_small.log"  # change to your file

def parse_line_for_ip(line):
    """
    Very simple parser: looks for the substring ' from <IP> ' and returns the IP.
    Returns None if no IP found.
    """
    if " from " in line:
        parts = line.split()
        # simple approach: find 'from' token and take next token as IP
        try:
            idx = parts.index("from")
            ip = parts[idx+1]
            # strip any trailing punctuation
            return ip.strip()
        except (ValueError, IndexError):
            return None
    return None

def read_logs_and_collect_failed_ips(filename):
    """
    Reads filename and returns a dictionary mapping IP -> count of failed attempts.
    """
    counts = defaultdict(int)
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # look only for FAILED lines (simplified)
            if "Failed password" in line or "Invalid user" in line:
                ip = parse_line_for_ip(line)
                if ip:
                    counts[ip] += 1
    return counts

def write_counts_to_csv(counts, outname="failed_counts.csv"):
    with open(outname, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ip", "failed_count"])
        for ip, cnt in counts.items():
            writer.writerow([ip, cnt])

if __name__ == "__main__":
    counts = read_logs_and_collect_failed_ips(LOGFILE)
    print("Raw counts:", dict(counts))
    # write CSV
    write_counts_to_csv(counts)
    print("Wrote failed_counts.csv")
