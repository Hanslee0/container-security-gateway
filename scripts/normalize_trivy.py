import json
import sys
from pathlib import Path


def normalize_trivy(input_path, output_path, environment="dev"):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    image_name = data.get("ArtifactName", "unknown")

    summary = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "UNKNOWN": 0
    }

    vulnerabilities = []

    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []) or []:
            severity = vuln.get("Severity", "UNKNOWN")

            if severity not in summary:
                summary[severity] = 0

            summary[severity] += 1

            vulnerabilities.append({
                "id": vuln.get("VulnerabilityID"),
                "severity": severity,
                "package": vuln.get("PkgName"),
                "installed_version": vuln.get("InstalledVersion"),
                "fixed_version": vuln.get("FixedVersion", ""),
                "title": vuln.get("Title", "")
            })

    normalized = {
    "image": image_name,
    "environment": environment,
    "summary": summary,
    "vulnerabilities": vulnerabilities
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    print(f"[OK] Normalized result saved to {output_path}")
    print(f"[SUMMARY] {summary}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/normalize_trivy.py <input_json> <output_json> [environment]")
        sys.exit(1)

    environment = sys.argv[3] if len(sys.argv) >= 4 else "dev"
    normalize_trivy(sys.argv[1], sys.argv[2], environment)
