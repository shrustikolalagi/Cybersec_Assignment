# Assignment Structure

### Section 1 – Linux & Bash Scripting (20 Points)
| File | Description |
|---|---|
| `section_1/section1_commands.txt` | All 10 Linux commands with explanations |
| `Port_report.sh` | Bash port scanner script – accepts target IP as argument |
| `port_report_results.txt` | Sample output from port_report.sh |

**How to run:**
```bash
chmod +x Port_report.sh
./Port_report.sh 127.0.0.1
```

---

### Section 2 – Python Security Scripting (20 Points)
| File | Description |
|---|---|
| `password_checker.py` | Password strength checker – score based evaluation |
| `password_output.txt` | Sample output from password_checker.py |
| `network_scanner.py` | TCP port scanner using sockets |
| `network_scanner_output.txt` | Sample scan results |
| `results.txt` | Additional scan results |

**How to run:**
```bash
# Password Checker
python3 password_checker.py MyPass@123 output.txt

# Network Scanner
python3 network_scanner.py 127.0.0.1 21,22,80,443,3306 scan_results.txt
```

---

### Section 3 – Networking Basics (15 Points)
| File | Description |
|---|---|
| `section_3/section3_networking.pdf` | OSI model, IP addressing, protocols + screenshots |

**Topics Covered:**
- OSI Model – all 7 layers with example protocols
- Public vs Private IP addressing
- TCP vs UDP differences
- NAT explanation
- Practical network analysis with screenshots

---

### Section 4 – C Programming (15 Points)
| File | Description |
|---|---|
| `pointer_basics.c` | Pointer declaration, dereferencing, and modification |
| `pointer_basics.txt` | Output of pointer_basics.c |
| `Buffer_test.c` | Buffer overflow demonstration using strcpy() |
| `Buffer_test.txt` | Output of buffer_test.c |
| `port_scanner.c` | TCP port scanner in C using POSIX sockets |
| `port_scanner_result.txt` | Output of c_port_scanner.c |

**How to compile and run:**
```bash
# Pointer basics
gcc -o pointer_basics pointer_basics.c
./pointer_basics

# Buffer test
gcc -o buffer_test Buffer_test.c
./buffer_test

# Port scanner
gcc -o port_scanner port_scanner.c
./port_scanner
```

---

### Section 5 – Nmap & Lua NSE Scripts (15 Points)
| File | Description |
|---|---|
| `http-server-info.nse` | Custom NSE script – extracts server info from HTTP ports |
| `http-server-info.txt` | Output of NSE script on scanme.nmap.org |
| `section_5/section5_nmap.pdf` | All 5 Nmap scans with screenshots and explanations |

**Nmap scans performed on scanme.nmap.org:**
```bash
# Scan 1 - Ping scan
sudo nmap -sn scanme.nmap.org

# Scan 2 - SYN scan top 100 ports
sudo nmap -sS --top-ports 100 scanme.nmap.org

# Scan 3 - Service version detection port 80
sudo nmap -sV -p 80 scanme.nmap.org

# Scan 4 - OS detection
sudo nmap -O scanme.nmap.org

# Scan 5 - Default NSE scripts
sudo nmap -sC scanme.nmap.org
```

**Custom NSE script output:**
```
PORT   STATE SERVICE
80/tcp open  http
| http-server-info:
|   HTTP Status Code : 200
|   Server           : Apache/2.4.7 (Ubuntu)
|_  Page Title       : Go ahead and ScanMe!
```

**How to run custom NSE script:**
```bash
nmap -Pn --script=./http-server-info.nse -p 80 --script-timeout 60 scanme.nmap.org
```

---

### Section 6 – JavaScript & XSS (10 Points)
| File | Description |
|---|---|
| `section_6/keylogger.html` | JavaScript keylogger demo with security explanations |
| `section_6/section6_xss.pdf` | XSS payloads tested on Juice Shop with screenshots |

**XSS Payloads tested on local Juice Shop instance:**
```
1. <script>alert('XSS')</script>
2. <img src=x onerror=alert('XSS')>
3. <svg/onload=alert('XSS')>
4. <img src=x onerror=alert(document.cookie)>
5. <img src=x onerror="document.body.innerHTML='HACKED'">
```

> ⚠️ All XSS testing was performed on a **local Juice Shop instance only**.
> No unauthorized systems were targeted.

---

## Tools & Environment
| Tool | Version |
|---|---|
| OS | Kali Linux |
| GCC | Default Kali |
| Python | Python 3 |
| Nmap | 7.95 |
| Juice Shop | Local Docker instance |

---

## Important Notes
- All Nmap scans were performed on `scanme.nmap.org` — an **authorized** target
- No unauthorized systems were scanned or tested
- All code written and tested on Kali Linux

---
