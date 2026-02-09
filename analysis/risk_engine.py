from datetime import datetime

FINDINGS = []

SEVERITY_ORDER = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}

def add_finding(category, title, severity, description, mitigation):
    FINDINGS.append({
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "title": title,
        "severity": severity,
        "description": description,
        "mitigation": mitigation
    })

def get_all_findings():
    return sorted(
        FINDINGS,
        key=lambda x: SEVERITY_ORDER.get(x["severity"], 0),
        reverse=True
    )

def has_findings():
    return len(FINDINGS) > 0

