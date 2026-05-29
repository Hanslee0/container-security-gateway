import json
import os
import sys
from pathlib import Path

from google import genai


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_priority_vulnerabilities(vulnerabilities, limit=10):
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

    return sorted_vulns[:limit]


def build_prompt(normalized, decision):
    image = normalized.get("image", "unknown")
    environment = normalized.get("environment", "dev")
    summary = normalized.get("summary", {})
    vulnerabilities = normalized.get("vulnerabilities", [])

    result = decision.get("result", "UNKNOWN")
    reason = decision.get("reason", "No reason provided")

    priority_vulns = get_priority_vulnerabilities(vulnerabilities)

    vuln_lines = []
    for v in priority_vulns:
        vuln_lines.append(
            f"- {v.get('id')} / {v.get('severity')} / "
            f"package={v.get('package')} / "
            f"installed={v.get('installed_version')} / "
            f"fixed={v.get('fixed_version')}"
        )

    vuln_text = "\n".join(vuln_lines) if vuln_lines else "- 주요 취약점 없음"

    prompt = f"""
너는 컨테이너 보안 점검 결과를 개발자가 이해하기 쉽게 설명하는 보안 어시스턴트다.

중요 규칙:
- 배포 허용/차단 판단은 이미 OPA가 수행했다.
- 너는 판단을 바꾸면 안 된다.
- 아래 OPA 판단 결과를 기준으로 한국어 대응 가이드를 작성해라.
- 너무 길게 쓰지 말고, 발표 자료나 리포트에 넣기 좋게 작성해라.
- 확실하지 않은 내용은 단정하지 말고 일반적인 권장 조치로 표현해라.

[이미지 정보]
이미지명: {image}
배포 환경: {environment}

[OPA 판단 결과]
결과: {result}
사유: {reason}

[취약점 요약]
CRITICAL: {summary.get("CRITICAL", 0)}
HIGH: {summary.get("HIGH", 0)}
MEDIUM: {summary.get("MEDIUM", 0)}
LOW: {summary.get("LOW", 0)}
UNKNOWN: {summary.get("UNKNOWN", 0)}

[주요 취약점]
{vuln_text}

아래 형식으로 작성해라.

## AI 한국어 대응 가이드

### 1. 판단 요약
- 한두 문장으로 현재 상태 설명

### 2. 주요 위험 요소
- 핵심 위험 요소 2~3개

### 3. 권장 조치
- 개발자가 바로 할 수 있는 조치 3개

### 4. 재검사 안내
- 수정 후 다시 스캔해야 한다는 안내
"""

    return prompt.strip()


def generate_ai_guide(normalized_path, decision_path, output_path):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("[ERROR] GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        print('예시: export GEMINI_API_KEY="your-api-key"')
        sys.exit(1)

    normalized = load_json(normalized_path)
    decision = load_json(decision_path)

    prompt = build_prompt(normalized, decision)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    guide_text = response.text.strip()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(guide_text)
        f.write("\n")

    print(f"[OK] AI guide saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 scripts/generate_ai_guide.py <normalized_json> <decision_json> <output_md>")
        sys.exit(1)

    generate_ai_guide(sys.argv[1], sys.argv[2], sys.argv[3])