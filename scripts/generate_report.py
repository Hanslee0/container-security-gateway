import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_text(value):
    if value is None:
        return ""
    return str(value).replace("|", "/")


def count_fixable(vulnerabilities):
    return sum(1 for v in vulnerabilities if v.get("fixed_version"))


def get_top_packages(vulnerabilities, limit=5):
    packages = [
        v.get("package", "unknown")
        for v in vulnerabilities
        if v.get("package")
    ]
    return Counter(packages).most_common(limit)


def get_priority_vulnerabilities(vulnerabilities, limit=15):
    priority_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
        "UNKNOWN": 4
    }

    sorted_vulns = sorted(
        vulnerabilities,
        key=lambda v: priority_order.get(v.get("severity", "UNKNOWN"), 5)
    )

    return [
        v for v in sorted_vulns
        if v.get("severity") in ["CRITICAL", "HIGH"]
    ][:limit]


def make_summary_sentence(result, reason, image, environment, summary):
    critical = summary.get("CRITICAL", 0)
    high = summary.get("HIGH", 0)

    if result == "BLOCK":
        return (
            f"`{image}` 이미지는 `{environment}` 환경 기준에서 **BLOCK** 처리되었습니다. "
            f"주요 사유는 `{reason}`이며, CRITICAL 취약점 {critical}개와 HIGH 취약점 {high}개가 확인되었습니다."
        )

    if result == "HOLD":
        return (
            f"`{image}` 이미지는 `{environment}` 환경 기준에서 **HOLD** 처리되었습니다. "
            f"즉시 배포하기보다는 보안 검토 또는 취약점 조치 후 재검사가 필요합니다."
        )

    if result == "ALLOW":
        return (
            f"`{image}` 이미지는 `{environment}` 환경 기준에서 **ALLOW** 처리되었습니다. "
            f"현재 정책 기준에서는 배포 가능한 상태입니다."
        )

    return (
        f"`{image}` 이미지에 대한 정책 판단 결과를 확인할 수 없습니다. "
        f"OPA 판단 결과와 입력 파일을 다시 확인해야 합니다."
    )


def make_recommendations(result, environment):
    if result == "BLOCK":
        return [
            "현재 이미지는 정책 기준을 위반했으므로 배포하지 않는 것을 권장합니다.",
            "CRITICAL 취약점 또는 정책 위반 항목을 먼저 조치해야 합니다.",
            "베이스 이미지를 최신 버전으로 교체하거나 취약 패키지를 업데이트해야 합니다.",
            "조치 후 동일한 명령어로 다시 스캔하여 정책 통과 여부를 확인해야 합니다."
        ]

    if result == "HOLD":
        return [
            "현재 이미지는 즉시 배포하기보다 보안 검토가 필요합니다.",
            "HIGH 취약점 또는 CRITICAL 취약점 존재 여부를 우선 확인해야 합니다.",
            "운영 환경 배포 전 주요 취약점에 대한 조치 계획을 수립해야 합니다.",
            "예외적으로 배포해야 한다면 보안 담당자의 승인 절차가 필요합니다."
        ]

    if result == "ALLOW":
        return [
            "현재 정책 기준에서는 배포가 가능합니다.",
            "단, LOW/MEDIUM 취약점이 남아 있을 수 있으므로 정기적인 이미지 업데이트가 필요합니다.",
            "운영 환경에서는 배포 전 최신 이미지로 한 번 더 스캔하는 것을 권장합니다."
        ]

    return [
        "정책 판단 결과가 명확하지 않습니다.",
        "decision.json 파일과 OPA 정책 파일을 다시 확인해야 합니다."
    ]


def generate_report(normalized_path, decision_path, output_path):
    normalized = load_json(normalized_path)
    decision = load_json(decision_path)

    image = normalized.get("image", "unknown")
    environment = normalized.get("environment", "dev")
    summary = normalized.get("summary", {})
    vulnerabilities = normalized.get("vulnerabilities", [])

    result = decision.get("result", "UNKNOWN")
    reason = decision.get("reason", "No reason provided")

    total_count = sum(summary.values())
    critical_count = summary.get("CRITICAL", 0)
    high_count = summary.get("HIGH", 0)
    medium_count = summary.get("MEDIUM", 0)
    low_count = summary.get("LOW", 0)
    unknown_count = summary.get("UNKNOWN", 0)

    fixable_count = count_fixable(vulnerabilities)
    critical_high_count = critical_count + high_count

    if total_count > 0:
        critical_high_ratio = round((critical_high_count / total_count) * 100, 2)
    else:
        critical_high_ratio = 0

    top_packages = get_top_packages(vulnerabilities)
    priority_vulns = get_priority_vulnerabilities(vulnerabilities)

    summary_sentence = make_summary_sentence(
        result,
        reason,
        image,
        environment,
        summary
    )

    recommendations = make_recommendations(result, environment)

    safe_image_name = image.replace("/", "-").replace(":", "-")
    rescan_command = f"./security-gate.sh {image} {environment}"

    lines = []

    lines.append("# Container Security Report")
    lines.append("")
    lines.append("## 1. 최종 요약")
    lines.append("")
    lines.append(f"- 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 이미지명: `{image}`")
    lines.append(f"- 배포 환경: `{environment}`")
    lines.append(f"- 최종 판단: **{result}**")
    lines.append(f"- 판단 사유: {reason}")
    lines.append("")
    lines.append(summary_sentence)
    lines.append("")

    lines.append("## 2. 취약점 요약")
    lines.append("")
    lines.append("| 항목 | 개수 |")
    lines.append("|---|---:|")
    lines.append(f"| 전체 취약점 | {total_count} |")
    lines.append(f"| CRITICAL | {critical_count} |")
    lines.append(f"| HIGH | {high_count} |")
    lines.append(f"| MEDIUM | {medium_count} |")
    lines.append(f"| LOW | {low_count} |")
    lines.append(f"| UNKNOWN | {unknown_count} |")
    lines.append(f"| 수정 가능한 취약점 | {fixable_count} |")
    lines.append(f"| CRITICAL/HIGH 비율 | {critical_high_ratio}% |")
    lines.append("")

    lines.append("## 3. 많이 탐지된 취약 패키지 Top 5")
    lines.append("")
    lines.append("| 순위 | 패키지명 | 취약점 개수 |")
    lines.append("|---:|---|---:|")

    if top_packages:
        for index, (package, count) in enumerate(top_packages, start=1):
            lines.append(f"| {index} | {safe_text(package)} | {count} |")
    else:
        lines.append("| - | - | - |")

    lines.append("")

    lines.append("## 4. 주요 조치 대상 CVE")
    lines.append("")
    lines.append("CRITICAL/HIGH 취약점 중 우선 확인이 필요한 항목입니다.")
    lines.append("")
    lines.append("| CVE ID | Severity | Package | Installed Version | Fixed Version |")
    lines.append("|---|---|---|---|---|")

    if priority_vulns:
        for vuln in priority_vulns:
            lines.append(
                f"| {safe_text(vuln.get('id'))} "
                f"| {safe_text(vuln.get('severity'))} "
                f"| {safe_text(vuln.get('package'))} "
                f"| {safe_text(vuln.get('installed_version'))} "
                f"| {safe_text(vuln.get('fixed_version'))} |"
            )
    else:
        lines.append("| - | - | - | - | - |")

    lines.append("")

    lines.append("## 5. 권장 조치")
    lines.append("")

    for item in recommendations:
        lines.append(f"- {item}")

    lines.append("")

    lines.append("## 6. 재검사 명령어")
    lines.append("")
    lines.append("취약점 조치 후 아래 명령어로 다시 검사할 수 있습니다.")
    lines.append("")
    lines.append(f"`{rescan_command}`")
    lines.append("")

    lines.append("## 7. 참고")
    lines.append("")
    lines.append("- 본 리포트는 Trivy 스캔 결과와 OPA 정책 판단 결과를 기반으로 생성되었습니다.")
    lines.append("- AI 분석은 포함하지 않은 기본 개선 리포트입니다.")
    lines.append("- 실제 운영 환경에서는 조직의 보안 정책에 맞게 판단 기준을 조정해야 합니다.")
    lines.append("")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Improved report saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 scripts/generate_report.py <normalized_json> <decision_json> <output_report>")
        sys.exit(1)

    generate_report(sys.argv[1], sys.argv[2], sys.argv[3])