import subprocess
from analysis.risk_engine import add_finding

# Binaries commonly abused for privilege escalation (GTFOBins-style)
HIGH_RISK_BINARIES = [
    "bash", "sh", "dash",
    "python", "python3", "perl", "ruby",
    "find", "vim", "vi", "less", "more",
    "awk", "nmap", "tar", "cp", "mv"
]

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().splitlines()
    except:
        return []

def scan_suid_sgid():
    print("[*] Scanning for SUID / SGID binaries...")
    print("[*] This may take a moment. Scanning filesystem...\n")

    # Exclude virtual / noisy directories for performance
    suid_cmd = (
        "find / \\( -path /proc -o -path /sys -o -path /dev \\) -prune "
        "-o -perm -4000 -type f -print 2>/dev/null"
    )

    sgid_cmd = (
        "find / \\( -path /proc -o -path /sys -o -path /dev \\) -prune "
        "-o -perm -2000 -type f -print 2>/dev/null"
    )

    suid_files = run_cmd(suid_cmd)
    sgid_files = run_cmd(sgid_cmd)

    if not suid_files and not sgid_files:
        print("[-] No SUID/SGID binaries found.\n")
        return

    print("[!] Potential SUID / SGID privilege escalation vectors:\n")

    for binary in suid_files + sgid_files:
        name = binary.split("/")[-1]

        severity = "HIGH" if name in HIGH_RISK_BINARIES else "MEDIUM"

        # Store finding in centralized risk engine
        add_finding(
            category="SUID / SGID Binary",
            title=f"SUID/SGID binary detected: {name}",
            severity=severity,
            description=f"SUID/SGID binary located at {binary}. "
                        f"This binary may allow privilege escalation if abused.",
            mitigation="Remove SUID/SGID bit if not required or restrict file permissions."
        )

        # Print for live output
        print(f"[{severity}] {binary}")

    print("\n" + "-" * 60 + "\n")

