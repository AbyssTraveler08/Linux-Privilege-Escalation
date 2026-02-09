import os
import subprocess

CRON_PATHS = [
    "/etc/crontab",
    "/etc/cron.d",
    "/etc/cron.hourly",
    "/etc/cron.daily",
    "/etc/cron.weekly",
    "/etc/cron.monthly"
]

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().splitlines()
    except:
        return []

def is_writable(path):
    return os.access(path, os.W_OK)

def scan_cron_jobs():
    print("[*] Scanning for cron job vulnerabilities...\n")

    findings = []

    for path in CRON_PATHS:
        if not os.path.exists(path):
            continue

        # Case 1: crontab file
        if os.path.isfile(path):
            if is_writable(path):
                findings.append(("WRITABLE CRONTAB", path))
            continue

        # Case 2: cron directories
        for root, dirs, files in os.walk(path):
            for name in files:
                full_path = os.path.join(root, name)

                # Writable cron script
                if is_writable(full_path):
                    findings.append(("WRITABLE CRON SCRIPT", full_path))

    if not findings:
        print("[-] No cron job vulnerabilities found.\n")
        return

    print("[!] Potential cron-based privilege escalation:\n")
    for issue, path in findings:
        print(f"[HIGH] {issue}: {path}")

    print("\n" + "-" * 60 + "\n")
