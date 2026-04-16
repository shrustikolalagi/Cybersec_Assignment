#!/bin/bash

# port_report.sh - Port Scanner Report Script


# --- Check if target IP is provided ---
if [ -z "$1" ]; then
    echo "============================================"
    echo "  Usage: ./port_report.sh <target_ip>"
    echo "  Example: ./port_report.sh 192.168.1.1"
    echo "============================================"
    exit 1
fi

TARGET="$1"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
OUTPUT_FILE="scan_${TARGET}_${DATE}.txt"
PORTS=(21 22 80 443 3306)
OPEN_COUNT=0

# --- Port service names for display ---
declare -A PORT_NAMES
PORT_NAMES[21]="FTP"
PORT_NAMES[22]="SSH"
PORT_NAMES[80]="HTTP"
PORT_NAMES[443]="HTTPS"
PORT_NAMES[3306]="MySQL"

# --- Write header to output file ---
{
    echo "============================================"
    echo "  Port Scan Report"
    echo "  Target   : $TARGET"
    echo "  Date     : $(date)"
    echo "  Scanner  : port_report.sh"
    echo "============================================"
    echo ""
} | tee "$OUTPUT_FILE"

echo "[*] Starting scan on $TARGET ..."
echo ""

# --- Scan each port ---
for PORT in "${PORTS[@]}"; do
    SERVICE="${PORT_NAMES[$PORT]}"

    # Use /dev/tcp to check port (timeout 2 seconds)
    if (timeout 2 bash -c "echo >/dev/tcp/$TARGET/$PORT") 2>/dev/null; then
        STATUS="OPEN"
        OPEN_COUNT=$((OPEN_COUNT + 1))
    else
        STATUS="CLOSED"
    fi

    LINE="  Port $PORT ($SERVICE): $STATUS"
    echo "$LINE" | tee -a "$OUTPUT_FILE"
done

# --- Write summary ---
{
    echo ""
    echo "============================================"
    echo "  SCAN SUMMARY"
    echo "  Total ports scanned : ${#PORTS[@]}"
    echo "  Total open ports    : $OPEN_COUNT"
    echo "============================================"
} | tee -a "$OUTPUT_FILE"

echo ""
echo "[*] Results saved to: $OUTPUT_FILE"
