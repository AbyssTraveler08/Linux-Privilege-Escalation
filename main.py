#!/usr/bin/env python3
from reports.report_generator import generate_txt_report, generate_json_report
from modules.kernel_scan import scan_kernel
from modules.sudo_scan import scan_sudo_rules
from modules.service_scan import scan_systemd_services
from modules.cron_scan import scan_cron_jobs
from modules.permission_scan import scan_weak_permissions
from modules.system_info import collect_system_info
from modules.suid_scan import scan_suid_sgid
import os
import sys
from modules.system_info import collect_system_info

def banner():
    print("=" * 60)
    print(" Linux Privilege Escalation Automation Toolkit")
    print(" Developed by: Abyss")
    print("=" * 60)
    print("[!] Educational use only. No exploitation performed.\n")

def main():
    banner()
    collect_system_info()
    scan_suid_sgid()
    scan_weak_permissions()
    scan_cron_jobs()
    scan_systemd_services()
    scan_sudo_rules()
    scan_kernel()

    print("[*] Generating reports...\n")
    txt = generate_txt_report()
    jsn = generate_json_report()

    print(f"[+] TXT Report saved as  : {txt}")
    print(f"[+] JSON Report saved as : {jsn}")


if __name__ == "__main__":
    main()
