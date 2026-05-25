#!/bin/bash

IMAGE="$1"
ENVIRONMENT="dev"
DEPLOY_OPTION=""

if [ "$2" = "--deploy" ]; then
  DEPLOY_OPTION="--deploy"
elif [ -n "$2" ]; then
  ENVIRONMENT="$2"
fi

if [ "$3" = "--deploy" ]; then
  DEPLOY_OPTION="--deploy"
fi

if [ -z "$IMAGE" ]; then
  echo "사용법: ./security-gate.sh <image-name> [dev|staging|prod] [--deploy]"
  echo "예시: ./security-gate.sh nginx:1.21 dev"
  echo "예시: ./security-gate.sh nginx:1.21 staging"
  echo "예시: ./security-gate.sh nginx:1.21 prod"
  echo "예시: ./security-gate.sh nginx:latest prod --deploy"
  exit 1
fi

SAFE_IMAGE=$(echo "$IMAGE" | sed 's#[/:]#-#g')

RAW_RESULT="scans/${SAFE_IMAGE}-result.json"
NORMALIZED_RESULT="scans/${SAFE_IMAGE}-normalized.json"
DECISION_RESULT="scans/${SAFE_IMAGE}-decision.json"
REPORT_FILE="reports/${SAFE_IMAGE}-report.md"
POLICY_FILE="policies/deploy_policy.rego"

echo "==================================="
echo "[SECURITY GATE] 시작"
echo "==================================="
echo "이미지: $IMAGE"
echo "배포 환경: $ENVIRONMENT"
echo ""

echo "----- 1. Trivy 취약점 스캔 -----"
trivy image "$IMAGE" \
  --scanners vuln \
  --timeout 15m \
  --format json \
  --output "$RAW_RESULT"

echo "[OK] Trivy 스캔 결과 저장: $RAW_RESULT"
echo ""

echo "----- 2. Trivy 결과 정규화 -----"
python3 scripts/normalize_trivy.py "$RAW_RESULT" "$NORMALIZED_RESULT" "$ENVIRONMENT"

echo "[OK] 정규화 결과 저장: $NORMALIZED_RESULT"
echo ""

echo "----- 3. OPA 정책 판단 -----"
opa eval \
  --input "$NORMALIZED_RESULT" \
  --data "$POLICY_FILE" \
  "data.deploy.decision" \
  --format pretty > "$DECISION_RESULT"

echo "[OK] OPA 판단 결과 저장: $DECISION_RESULT"
cat "$DECISION_RESULT"
echo ""

echo "----- 4. 기본 리포트 생성 -----"
python3 scripts/generate_report.py \
  "$NORMALIZED_RESULT" \
  "$DECISION_RESULT" \
  "$REPORT_FILE"

echo "[OK] 리포트 생성 완료: $REPORT_FILE"
echo ""

echo "----- 5. 배포 허용 / 보류 / 차단 처리 -----"

if [ "$DEPLOY_OPTION" = "--deploy" ]; then
  python3 scripts/enforce_policy.py "$DECISION_RESULT" "$IMAGE" --deploy --container-name "${SAFE_IMAGE}-demo"
  EXIT_CODE=$?
else
  python3 scripts/enforce_policy.py "$DECISION_RESULT" "$IMAGE"
  EXIT_CODE=$?
fi

echo ""
echo "==================================="
echo "[SECURITY GATE] 완료"
echo "==================================="
echo "원본 스캔 결과: $RAW_RESULT"
echo "정규화 결과: $NORMALIZED_RESULT"
echo "정책 판단 결과: $DECISION_RESULT"
echo "기본 리포트: $REPORT_FILE"

exit $EXIT_CODE
