import subprocess
import os
import re

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().splitlines()
    except:
        return []

def is_writable(path):
    return os.access(path, os.W_OK)

def scan_systemd_services():
    print("[*] Scanning for misconfigured systemd services...\n")

    findings = []

    # List running services
    services = run_cmd(
        "systemctl list-units --type=service --state=running --no-pager --no-legend"
    )

    for svc in services:
        service_name = svc.split()[0]

        # Get service details
        exec_start = run_cmd(f"systemctl show {service_name} -p ExecStart")
        user = run_cmd(f"systemctl show {service_name} -p User")

        exec_path = ""
        run_user = "root"

        if exec_start:
            match = re.search(r'ExecStart=.*?(/[^ ;]+)', exec_start[0])
            if match:
                exec_path = match.group(1)

        if user and "User=" in user[0] and user[0] != "User=":
            run_user = user[0].split("=")[1]

        # Only care about root services
        if run_user != "root" or not exec_path:
            continue

        # Check writable executable
        if os.path.exists(exec_path) and is_writable(exec_path):
            findings.append(("WRITABLE EXECSTART FILE", service_name, exec_path))

        # Check writable parent directory
        parent_dir = os.path.dirname(exec_path)
        if os.path.exists(parent_dir) and is_writable(parent_dir):
            findings.append(("WRITABLE EXECSTART DIR", service_name, parent_dir))

    if not findings:
        print("[-] No misconfigured systemd services found.\n")
        return

    print("[!] Potential systemd-based privilege escalation:\n")
    for issue, service, path in findings:
        print(f"[HIGH] {issue}")
        print(f"     Service : {service}")
        print(f"     Path    : {path}\n")

    print("-" * 60 + "\n")
