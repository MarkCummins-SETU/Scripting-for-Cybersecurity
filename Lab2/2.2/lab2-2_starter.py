# lab2-2_starter.py
import csv
from collections import defaultdict

LOGFILE = "sample_auth_small.log"  # change filename if needed

def simple_parser(line):
    """
    looks for the substring ' port ' and returns the following port number.
    Returns None if no matching substring found.
    """
    if " port " in line:
        parts = line.split() # splits the line into tokens, seperates by spaces by default
        try:
            anchor = parts.index("port")    # Find the position of the token "port", our anchor
            port = parts[anchor+1]          # the port value will be next token, anchor+1
            return port.strip()             # strip any trailing punctuation

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

## This is the main block that will run first. 
## It will call any functions from above that we might need.
if __name__ == "__main__":

    with open(LOGFILE, "r") as f:
        for line in f:
            print (simple_parser(line.strip()))
    
