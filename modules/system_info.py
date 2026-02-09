import os
import platform
import subprocess

def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().strip()
    except:
        return "N/A"

def collect_system_info():
    print("[*] Collecting system information...\n")

    user = run_cmd("whoami")
    uid = os.getuid()
    groups = run_cmd("id")
    kernel = run_cmd("uname -r")
    os_info = run_cmd("cat /etc/os-release | grep PRETTY_NAME")

    privilege = "ROOT" if uid == 0 else "NON-ROOT"

    print(f"User            : {user}")
    print(f"UID             : {uid}")
    print(f"Groups          : {groups}")
    print(f"Kernel Version  : {kernel}")
    print(f"OS Info         : {os_info}")
    print(f"Privilege Level : {privilege}")
    print("\n" + "-" * 60 + "\n")
