import platform
import subprocess

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().strip()
    except:
        return "Unknown"

def scan_kernel():
    print("[*] Scanning kernel version and security posture...\n")

    kernel = run_cmd("uname -r")
    os_info = run_cmd("cat /etc/os-release | grep PRETTY_NAME")

    print(f"Kernel Version : {kernel}")
    print(f"OS Info        : {os_info}\n")

    findings = []

    # Basic heuristic checks
    try:
        major = int(kernel.split(".")[0])
        minor = int(kernel.split(".")[1])

        # Very old kernels (generic heuristic)
        if major < 4:
            findings.append("Kernel version is extremely old (pre-4.x).")

        elif major == 4 and minor < 15:
            findings.append("Kernel version is outdated and likely vulnerable.")

    except:
        findings.append("Unable to parse kernel version reliably.")

    if findings:
        print("[!] Kernel-related security concerns detected:\n")
        for f in findings:
            print(f"[HIGH] {f}")

        print("\nSuggested Mitigation:")
        print(" - Update kernel to latest stable version")
        print(" - Apply vendor security patches")
        print(" - Enable automatic security updates\n")
    else:
        print("[+] Kernel version appears reasonably up-to-date.\n")

    print("-" * 60 + "\n")
