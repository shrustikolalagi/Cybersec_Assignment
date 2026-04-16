#!/usr/bin/env python3
"""
network_scanner.py - TCP Port Scanner
CampusPe Cybersecurity Assignment - Section 2.2

Scans a list of TCP ports on a target IP address and reports
whether each port is OPEN or CLOSED. Results are saved to
scan_results.txt and displayed on screen.

Usage:
    python3 network_scanner.py
    (Follow the prompts to enter IP and ports)
"""

import socket
import time
import datetime
import sys


# ─── Configuration ────────────────────────────────────────────────────────────
TIMEOUT       = 1.0          # seconds to wait per connection attempt
OUTPUT_FILE   = "scan_results.txt"

# Common port -> service name mapping
SERVICE_NAMES = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}


# ─── Core Functions ───────────────────────────────────────────────────────────

def scan_port(target_ip: str, port: int) -> bool:
    """
    Attempt a TCP connection to target_ip:port.

    Returns:
        True  if the port is OPEN (connection succeeded)
        False if the port is CLOSED / filtered (connection failed)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        return result == 0          # 0 means connection established
    except (socket.error, OSError):
        return False


def resolve_host(target: str) -> str:
    """Resolve hostname to IP if a hostname was provided."""
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"[!] Cannot resolve host: {target}")
        sys.exit(1)


def parse_ports(port_input: str) -> list:
    """
    Parse a port specification string into a sorted list of integers.
    Supports:
        - Comma-separated values  : "80,443,22"
        - Ranges                  : "1-1024"
        - Mixed                   : "22,80,100-200,443"
    """
    ports = set()
    for part in port_input.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def run_scan(target: str, ports: list) -> list:
    """
    Scan all specified ports and return a list of result dicts.
    Each dict contains: port, service, status.
    """
    results = []
    open_count = 0

    print(f"\n[*] Scanning {target} on {len(ports)} port(s) ...\n")

    for port in ports:
        is_open = scan_port(target, port)
        status  = "OPEN" if is_open else "CLOSED"
        service = SERVICE_NAMES.get(port, "Unknown")

        if is_open:
            open_count += 1

        results.append({"port": port, "service": service, "status": status})
        indicator = "+" if is_open else "-"
        print(f"  [{indicator}] Port {port:5d}  ({service:<15s})  {status}")

    return results, open_count


def save_results(target: str, ports: list, results: list,
                 open_count: int, duration: float) -> None:
    """Write scan results to OUTPUT_FILE."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(OUTPUT_FILE, "w") as f:
        f.write("=" * 52 + "\n")
        f.write("  NETWORK SCAN RESULTS\n")
        f.write("=" * 52 + "\n")
        f.write(f"  Target    : {target}\n")
        f.write(f"  Timestamp : {timestamp}\n")
        f.write(f"  Ports     : {len(ports)} scanned\n")
        f.write(f"  Duration  : {duration:.2f} seconds\n")
        f.write("=" * 52 + "\n\n")

        f.write(f"  {'PORT':<8} {'SERVICE':<16} STATUS\n")
        f.write("  " + "-" * 36 + "\n")
        for r in results:
            f.write(f"  {r['port']:<8} {r['service']:<16} {r['status']}\n")

        f.write("\n" + "=" * 52 + "\n")
        f.write(f"  SUMMARY: {open_count} OPEN port(s) found\n")
        f.write("=" * 52 + "\n")

    print(f"\n[*] Results saved to: {OUTPUT_FILE}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 52)
 #!/usr/bin/env python3
"""
network_scanner.py - TCP Port Scanner
CampusPe Cybersecurity Assignment - Section 2.2

Usage:
    python3 network_scanner.py <target_ip> <ports> <output_file>

Examples:
    python3 network_scanner.py 127.0.0.1 21,22,80,443,3306 results.txt
    python3 network_scanner.py 192.168.1.1 1-1024 scan.txt
    python3 network_scanner.py scanme.nmap.org 22,80,443 output.txt
"""

import socket
import time
import datetime
import sys


# ── Configuration ──────────────────────────────────────────────────
TIMEOUT = 1.0

SERVICE_NAMES = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}


# ── Functions ──────────────────────────────────────────────────────

def show_usage():
    print("=" * 55)
    print("  Usage:")
    print("    python3 network_scanner.py <ip> <ports> <file>")
    print("")
    print("  Examples:")
    print("    python3 network_scanner.py 127.0.0.1 21,22,80,443,3306 results.txt")
    print("    python3 network_scanner.py 192.168.1.1 1-100 scan.txt")
    print("    python3 network_scanner.py scanme.nmap.org 22,80,443 out.txt")
    print("=" * 55)
    sys.exit(1)


def parse_ports(port_input: str) -> list:
    """
    Parse port string into sorted list of integers.
    Supports:
        Comma-separated : 22,80,443
        Range           : 1-1024
        Mixed           : 22,80,100-200,443
    """
    ports = set()
    for part in port_input.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def resolve_host(target: str) -> str:
    """Resolve hostname to IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Cannot resolve host: {target}")
        sys.exit(1)


def scan_port(ip: str, port: int) -> bool:
    """Attempt TCP connection. Returns True if port is OPEN."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except (socket.error, OSError):
        return False


def run_scan(target_ip: str, ports: list):
    """Scan all ports and return results list."""
    results = []
    open_count = 0

    print(f"\n[*] Scanning {target_ip} on {len(ports)} port(s)...\n")

    for port in ports:
        is_open  = scan_port(target_ip, port)
        status   = "OPEN" if is_open else "CLOSED"
        service  = SERVICE_NAMES.get(port, "Unknown")

        if is_open:
            open_count += 1

        results.append({"port": port, "service": service, "status": status})

        indicator = "+" if is_open else "-"
        print(f"  [{indicator}] Port {port:<6} ({service:<15}) {status}")

    return results, open_count


def save_results(target: str, ports: list, results: list,
                 open_count: int, duration: float, output_file: str):
    """Save scan results to file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("=" * 55)
    lines.append("  NETWORK SCAN RESULTS")
    lines.append("=" * 55)
    lines.append(f"  Target    : {target}")
    lines.append(f"  Timestamp : {timestamp}")
    lines.append(f"  Ports     : {len(ports)} scanned")
    lines.append(f"  Duration  : {duration:.2f} seconds")
    lines.append("=" * 55)
    lines.append("")
    lines.append(f"  {'PORT':<8} {'SERVICE':<16} STATUS")
    lines.append("  " + "-" * 38)

    for r in results:
        lines.append(f"  {r['port']:<8} {r['service']:<16} {r['status']}")

    lines.append("")
    lines.append("=" * 55)
    lines.append(f"  SUMMARY")
    lines.append(f"  Total Scanned : {len(ports)}")
    lines.append(f"  Open Ports    : {open_count}")
    lines.append(f"  Closed Ports  : {len(ports) - open_count}")
    lines.append("=" * 55)

    report = "\n".join(lines)

    with open(output_file, "w") as f:
        f.write(report + "\n")

    return report


# ── Main ───────────────────────────────────────────────────────────

def main():

    # ── Validate arguments ─────────────────────────────────────────
    if len(sys.argv) != 4:
        show_usage()

    target_input = sys.argv[1]
    port_input   = sys.argv[2]
    output_file  = sys.argv[3]

    # ── Resolve host ───────────────────────────────────────────────
    target_ip = resolve_host(target_input)
    if target_ip != target_input:
        print(f"[*] Resolved {target_input} -> {target_ip}")

    # ── Parse ports ────────────────────────────────────────────────
    try:
        ports = parse_ports(port_input)
    except ValueError:
        print("[!] Invalid port format. Use: 22,80,443  or  1-1024")
        sys.exit(1)

    print("=" * 55)
    print("  CampusPe - Network Port Scanner")
    print("=" * 55)
    print(f"  Target      : {target_input}")
    print(f"  Ports       : {port_input}")
    print(f"  Output File : {output_file}")
    print("=" * 55)

    # ── Scan ───────────────────────────────────────────────────────
    start_time = time.time()
    results, open_count = run_scan(target_ip, ports)
    duration = time.time() - start_time

    # ── Save & display summary ─────────────────────────────────────
    report = save_results(target_ip, ports, results,
                          open_count, duration, output_file)

    print("\n" + "=" * 55)
    print(f"  Scan complete in {duration:.2f} seconds")
    print(f"  Open  : {open_count}")
    print(f"  Closed: {len(ports) - open_count}")
    print("=" * 55)
    print(f"\n[*] Results saved to: {output_file}")


if __name__ == "__main__":
    main()
