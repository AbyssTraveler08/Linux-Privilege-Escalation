import json
from datetime import datetime
from analysis.risk_engine import get_all_findings, has_findings

def generate_txt_report():
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.write("Linux Privilege Escalation Security Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated on: {datetime.now()}\n\n")

        if not has_findings():
            f.write("No privilege escalation issues detected.\n")
            return filename

        for finding in get_all_findings():
            f.write(f"Severity   : {finding['severity']}\n")
            f.write(f"Category   : {finding['category']}\n")
            f.write(f"Title      : {finding['title']}\n")
            f.write(f"Description: {finding['description']}\n")
            f.write(f"Mitigation : {finding['mitigation']}\n")
            f.write("-" * 50 + "\n")

    return filename


def generate_json_report():
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    data = {
        "generated_at": datetime.now().isoformat(),
        "total_findings": len(get_all_findings()),
        "findings": get_all_findings()
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    return filename
