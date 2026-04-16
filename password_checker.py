#!/usr/bi/env python3
"""
password_checker.py - Password Strength Checker

"""

import re
import sys


def check_password_strength(password: str) -> dict:
    checks = {
        "length":    len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digits":    bool(re.search(r"\d", password)),
        "special":   bool(re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>?/\\|`~]", password)),
    }

    score = sum(checks.values())

    if score <= 2:
        rating = "Weak"
    elif score <= 4:
        rating = "Medium"
    else:
        rating = "Strong"

    recommendations = []
    if not checks["length"]:
        recommendations.append("Use at least 8 characters.")
    if not checks["uppercase"]:
        recommendations.append("Add at least one uppercase letter (A-Z).")
    if not checks["lowercase"]:
        recommendations.append("Add at least one lowercase letter (a-z).")
    if not checks["digits"]:
        recommendations.append("Include at least one digit (0-9).")
    if not checks["special"]:
        recommendations.append("Include at least one special character (!@#$%^&* ...).")

    return {
        "password": password,
        "score":    score,
        "rating":   rating,
        "checks":   checks,
        "recommendations": recommendations,
    }


def format_report(result: dict) -> str:
    check_labels = {
        "length":    "Length >= 8",
        "uppercase": "Uppercase letter",
        "lowercase": "Lowercase letter",
        "digits":    "Digit (0-9)",
        "special":   "Special character",
    }

    lines = []
    lines.append("=" * 46)
    lines.append("       PASSWORD STRENGTH CHECKER REPORT")
    lines.append("=" * 46)
    lines.append(f"  Password : {'*' * len(result['password'])}")
    lines.append(f"  Score    : {result['score']} / 5")
    lines.append(f"  Rating   : {result['rating']}")
    lines.append("-" * 46)
    lines.append("  Criteria Check:")
    for key, passed in result["checks"].items():
        status = "✔  PASS" if passed else "✘  FAIL"
        lines.append(f"    [{status}]  {check_labels[key]}")
    lines.append("-" * 46)

    if result["recommendations"]:
        lines.append("  Recommendations:")
        for tip in result["recommendations"]:
            lines.append(f"    • {tip}")
    else:
        lines.append("  Great job! Your password meets all criteria.")

    lines.append("=" * 46)
    return "\n".join(lines)


def main():
    # ── Check arguments ──────────────────────────────────────────
    if len(sys.argv) != 3:
        print("=" * 46)
        print("  Usage  : python3 password_checker.py <password> <output_file>")
        print("  Example: python3 password_checker.py MyPass@123 results.txt")
        print("=" * 46)
        sys.exit(1)

    password    = sys.argv[1]
    output_file = sys.argv[2]

    # ── Check password ───────────────────────────────────────────
    result = check_password_strength(password)
    report = format_report(result)

    # ── Print to terminal ────────────────────────────────────────
    print(report)

    # ── Save to file ─────────────────────────────────────────────
    with open(output_file, "w") as f:
        f.write(report + "\n")

    print(f"\n[*] Results saved to: {output_file}")


if __name__ == "__main__":
    main()
