import json
import sys
from pathlib import Path
from datetime import datetime


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_recommendation(decision_result):
    if decision_result == "BLOCK":
        return [
            "Critical 취약점이 존재하므로 현재 이미지는 배포하지 않는 것을 권장합니다.",
            "베이스 이미지를 최신 버전으로 교체하거나 취약 패키지를 업데이트해야 합니다.",
            "수정 후 Trivy 스캔과 OPA 정책 판단을 다시 실행해야 합니다."
        ]

    if decision_result == "HOLD":
        return [
            "High 등급 취약점이 기준 이상으로 발견되어 배포 보류가 필요합니다.",
            "운영 환경 배포 전 주요 취약점을 우선 조치하는 것이 좋습니다.",
            "조치가 어렵다면 보안 담당자 검토 후 예외 승인 여부를 판단해야 합니다."
        ]

    return [
        "현재 정책 기준에서는 배포가 허용됩니다.",
        "단, Low/Medium 취약점이 존재할 수 있으므로 정기적인 이미지 업데이트가 필요합니다."
    ]


def generate_report(normalized_path, decision_path, output_path):
    normalized = load_json(normalized_path)
    decision = load_json(decision_path)

    image = normalized.get("image", "unknown")
    summary = normalized.get("summary", {})
    vulnerabilities = normalized.get("vulnerabilities", [])

    result = decision.get("result", "UNKNOWN")
    reason = decision.get("reason", "No reason provided")

    critical_high = [
        v for v in vulnerabilities
        if v.get("severity") in ["CRITICAL", "HIGH"]
    ]

    recommendations = make_recommendation(result)

    lines = []

    lines.append("# Container Security Report")
    lines.append("")
    lines.append(f"- 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 이미지명: `{image}`")
    lines.append("")
    lines.append("## 1. 정책 판단 결과")
    lines.append("")
    lines.append(f"- 결과: **{result}**")
    lines.append(f"- 사유: {reason}")
    lines.append("")

    lines.append("## 2. 취약점 요약")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|---|---:|")
    lines.append(f"| CRITICAL | {summary.get('CRITICAL', 0)} |")
    lines.append(f"| HIGH | {summary.get('HIGH', 0)} |")
    lines.append(f"| MEDIUM | {summary.get('MEDIUM', 0)} |")
    lines.append(f"| LOW | {summary.get('LOW', 0)} |")
    lines.append(f"| UNKNOWN | {summary.get('UNKNOWN', 0)} |")
    lines.append("")

    lines.append("## 3. 주요 취약점 목록")
    lines.append("")
    lines.append("CRITICAL/HIGH 취약점 중 일부를 표시합니다.")
    lines.append("")
    lines.append("| CVE ID | Severity | Package | Installed Version | Fixed Version |")
    lines.append("|---|---|---|---|---|")

    for vuln in critical_high[:15]:
        lines.append(
            f"| {vuln.get('id', '')} "
            f"| {vuln.get('severity', '')} "
            f"| {vuln.get('package', '')} "
            f"| {vuln.get('installed_version', '')} "
            f"| {vuln.get('fixed_version', '')} |"
        )

    if not critical_high:
        lines.append("| - | - | - | - | - |")

    lines.append("")
    lines.append("## 4. 권장 조치")
    lines.append("")

    for item in recommendations:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## 5. 참고")
    lines.append("")
    lines.append("- 본 리포트는 Trivy 스캔 결과와 OPA 정책 판단 결과를 기반으로 생성되었습니다.")
    lines.append("- AI 분석은 포함하지 않은 기본 리포트입니다.")
    lines.append("- 실제 운영 환경에서는 조직의 보안 정책에 맞게 판단 기준을 조정해야 합니다.")
    lines.append("")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Report saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 scripts/generate_report.py <normalized_json> <decision_json> <output_report>")
        sys.exit(1)

    generate_report(sys.argv[1], sys.argv[2], sys.argv[3])
