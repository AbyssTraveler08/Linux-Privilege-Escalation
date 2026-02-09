import subprocess

DANGEROUS_CMDS = [
    "bash", "sh", "python", "python3", "perl", "ruby",
    "vim", "vi", "nano", "less", "more",
    "find", "awk", "nmap", "tar"
]

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().splitlines()
    except:
        return []

def scan_sudo_rules():
    print("[*] Scanning sudo permissions...\n")

    sudo_output = run_cmd("sudo -l")

    if not sudo_output:
        print("[-] Unable to retrieve sudo rules or no sudo access.\n")
        return

    findings = []

    for line in sudo_output:
        line = line.strip()

        if "NOPASSWD" in line:
            findings.append(("NOPASSWD RULE", line))

        if "ALL" in line:
            findings.append(("FULL SUDO ACCESS", line))

        if "*" in line:
            findings.append(("WILDCARD USAGE", line))

        for cmd in DANGEROUS_CMDS:
            if cmd in line:
                findings.append(("DANGEROUS COMMAND", line))
                break

    if not findings:
        print("[-] No dangerous sudo misconfigurations found.\n")
        return

    print("[!] Potential sudo-based privilege escalation:\n")
    for issue, rule in findings:
        print(f"[HIGH] {issue}")
        print(f"       Rule: {rule}\n")

    print("-" * 60 + "\n")
