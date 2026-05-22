import argparse
import json
import subprocess
import sys


def load_decision(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_deploy(image, container_name):
    command = [
        "docker",
        "run",
        "-d",
        "--name",
        container_name,
        image
    ]

    print("[DEPLOY] 배포 명령 실행:")
    print(" ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("[DEPLOY] 배포 실패")
        print(result.stderr)
        sys.exit(result.returncode)

    print("[DEPLOY] 배포 성공")
    print(f"[CONTAINER ID] {result.stdout.strip()}")


def main():
    parser = argparse.ArgumentParser(
        description="OPA 정책 판단 결과를 기반으로 배포 허용/차단을 수행합니다."
    )

    parser.add_argument(
        "decision_json",
        help="OPA 판단 결과 JSON 파일 경로"
    )

    parser.add_argument(
        "image",
        help="배포 대상 컨테이너 이미지 이름"
    )

    parser.add_argument(
        "--deploy",
        action="store_true",
        help="ALLOW인 경우 실제 docker run을 실행합니다."
    )

    parser.add_argument(
        "--container-name",
        default="security-gate-demo",
        help="실제 배포 시 사용할 컨테이너 이름"
    )

    args = parser.parse_args()

    decision = load_decision(args.decision_json)

    result = decision.get("result", "UNKNOWN").upper()
    reason = decision.get("reason", "No reason provided")

    print("===================================")
    print("[SECURITY GATE] 배포 정책 판단 결과")
    print("===================================")
    print(f"이미지: {args.image}")
    print(f"판단 결과: {result}")
    print(f"사유: {reason}")
    print("")

    if result == "BLOCK":
        print("[DEPLOY] 배포가 차단되었습니다.")
        print("[ACTION] Critical 취약점 조치 후 다시 스캔해야 합니다.")
        sys.exit(1)

    if result == "HOLD":
        print("[DEPLOY] 배포가 보류되었습니다.")
        print("[ACTION] 보안 담당자 검토 또는 취약점 조치가 필요합니다.")
        sys.exit(2)

    if result == "ALLOW":
        print("[DEPLOY] 정책 기준상 배포가 허용되었습니다.")

        if args.deploy:
            run_deploy(args.image, args.container_name)
        else:
            print("[DEPLOY] 실제 배포는 실행하지 않았습니다.")
            print("[INFO] 실제 배포 테스트는 --deploy 옵션을 사용하세요.")

        sys.exit(0)

    print("[ERROR] 알 수 없는 정책 결과입니다.")
    sys.exit(3)


if __name__ == "__main__":
    main()
