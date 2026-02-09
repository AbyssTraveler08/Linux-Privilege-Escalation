import subprocess
import os

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().splitlines()
    except:
        return []

def scan_weak_permissions():
    print("[*] Scanning for weak file & directory permissions...\n")

    findings = []

    # 1. World-writable files
    print("[*] Checking for world-writable files...")
    ww_files = run_cmd(
        "find / \\( -path /proc -o -path /sys -o -path /dev \\) -prune "
        "-o -type f -perm -0002 -print 2>/dev/null"
    )

    for f in ww_files:
        findings.append(("WORLD-WRITABLE FILE", f))

    # 2. World-writable directories
    print("[*] Checking for world-writable directories...")
    ww_dirs = run_cmd(
        "find / \\( -path /proc -o -path /sys -o -path /dev \\) -prune "
        "-o -type d -perm -0002 -print 2>/dev/null"
    )

    for d in ww_dirs:
        findings.append(("WORLD-WRITABLE DIR", d))

    # 3. Writable root-owned files
    print("[*] Checking for writable root-owned files...")
    writable_root_files = run_cmd(
        "find / -user root -writable -type f 2>/dev/null"
    )

    for f in writable_root_files:
        findings.append(("WRITABLE ROOT FILE", f))

    if not findings:
        print("[-] No weak permissions found.\n")
        return

    print("\n[!] Potential privilege escalation vectors:\n")
    for issue, path in findings:
        print(f"[HIGH] {issue}: {path}")

    print("\n" + "-" * 60 + "\n")
