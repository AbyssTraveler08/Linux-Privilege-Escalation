<div align="center">

# 🐧 Linux Privilege Escalation Audit Toolkit

**A detection-focused Linux auditing utility for surfacing configuration weaknesses and generating TXT/JSON findings.**

<img src="https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Focus-Linux%20Security-0A66C2?style=for-the-badge&logo=linux&logoColor=white" alt="Linux security" />
<img src="https://img.shields.io/badge/Mode-Detection%20Only-475569?style=for-the-badge" alt="Detection only" />

</div>

---

## 🔎 Overview

The Linux Privilege Escalation Audit Toolkit automates several local enumeration checks that can help defenders and system administrators identify risky Linux configuration. It gathers system information and inspects SUID/SGID binaries, permissions, scheduled jobs, systemd services, sudo rules, and kernel-version signals.

The toolkit is designed for **assessment and reporting, not exploitation**. Findings need to be reviewed in context; a flagged configuration is not automatically exploitable.

## ✨ What it checks

- **System context:** user, group, operating-system, and kernel information.
- **SUID/SGID files:** enumerates binaries with privilege-related permission bits.
- **Weak permissions:** searches for selected writable files and directories.
- **Cron jobs:** checks scheduled-task locations and associated permissions.
- **systemd services:** examines service configuration paths and permissions.
- **Sudo rules:** reviews the current user's delegated privileges.
- **Kernel awareness:** reports potential concerns based on kernel information.
- **Reports:** emits human-readable TXT and machine-readable JSON findings.

## 🧭 Workflow

~~~text
Collect local system context
           |
           v
Run modular enumeration checks
           |
           v
Collect permissions / service / sudo findings
           |
           v
Prioritize and summarize observations
           |
           v
Write TXT and JSON reports
~~~

## 🧰 Requirements

- Linux system (Kali Linux or a disposable Linux VM is a convenient lab).
- Python 3.
- Standard Linux utilities used by the scanners, including `find`, `systemctl`, `sudo`, and `uname`.

The current project is organized as Python modules and does not list a separate pip requirements file at the repository root.

## ⚙️ Installation and usage

~~~bash
git clone https://github.com/AbyssTraveler08/Linux-Privilege-Escalation.git
cd Linux-Privilege-Escalation
python3 main.py
~~~

Run from the repository root so Python can resolve the `modules` and `reports` packages. The program displays its banner, executes the checks, and prints the generated report paths.

Use your normal unprivileged account first. Some checks may return incomplete information or UNKNOWN when permissions are restricted; that is preferable to assuming the condition is safe. If elevated access is needed for a specific authorized audit, understand the implications before rerunning.

## 🗂️ Code structure

| Path | Purpose |
|---|---|
| **main.py** | Orchestrates the audit |
| **modules/system_info.py** | Collects local system context |
| **modules/suid_scan.py** | SUID/SGID enumeration |
| **modules/permission_scan.py** | Permission checks |
| **modules/cron_scan.py** | Scheduled task checks |
| **modules/service_scan.py** | systemd service checks |
| **modules/sudo_scan.py** | Sudo rule review |
| **modules/kernel_scan.py** | Kernel-version awareness |
| **reports/report_generator.py** | TXT and JSON report output |

## 📄 Reporting and interpretation

Review each finding's context, affected path, severity, and remediation guidance before making system changes. The tool does not automatically change permissions, rewrite service configurations, or exploit a finding.

## 🧪 Validation suggestions

- Run in a disposable Linux VM and save the baseline output.
- Compare results between a standard user and an intentionally configured test VM.
- Verify a flagged file or service manually before changing it.
- Check that TXT/JSON reports are created and valid.
- Record false positives and inaccessible checks.

## 🛡️ Safe use

Use only on Linux hosts you own or are explicitly authorized to assess. Avoid copying sensitive audit output to public repositories. Do not apply remediation automatically without reviewing its operational impact.

## 🗺️ Roadmap

- Add automated unit tests and benign fixture environments.
- Improve output schemas and report timestamps.
- Add configuration to exclude irrelevant paths.
- Link findings to clear remediation and evidence fields.
- Improve kernel advisory matching with maintained data sources.

## 👤 Author

**Amar Kant Yadav** · [GitHub profile](https://github.com/AbyssTraveler08)

## 📄 License

See the repository's LICENSE file.

---

<div align="center">Practical enumeration for defensive Linux hardening and security learning.</div>
