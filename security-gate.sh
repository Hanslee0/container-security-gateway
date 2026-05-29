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

# ----- 입력값 검증 -----

# 1. 배포 환경 화이트리스트 검증
case "$ENVIRONMENT" in
  dev|staging|prod)
    ;;
  *)
    echo "오류: 배포 환경은 dev, staging, prod 중 하나여야 합니다."
    echo "입력된 값: $ENVIRONMENT"
    exit 1
    ;;
esac

# 2. 세 번째 인자가 있다면 --deploy만 허용
if [ -n "$3" ] && [ "$3" != "--deploy" ]; then
  echo "오류: 세 번째 인자는 --deploy만 사용할 수 있습니다."
  echo "입력된 값: $3"
  exit 1
fi

# 3. 컨테이너 이미지명 형식 검증
if [[ ! "$IMAGE" =~ ^[a-zA-Z0-9._/:@-]+$ ]]; then
  echo "오류: 올바르지 않은 컨테이너 이미지명 형식입니다."
  echo "이미지명에는 영문자, 숫자, '.', '_', '-', '/', ':', '@'만 사용할 수 있습니다."
  exit 1
fi

# 3-1. 이미지 태그 또는 digest 필수 검증
if [[ ! "$IMAGE" =~ @sha256:[a-fA-F0-9]{64}$ && ! "$IMAGE" =~ :[^/]+$ ]]; then
  echo "오류: 이미지 태그 또는 digest를 명시해야 합니다."
  echo "예시: nginx:1.21 또는 nginx@sha256:<digest>"
  exit 1
fi

# 4. prod 환경에서는 latest 태그 사용 제한
if [ "$ENVIRONMENT" = "prod" ] && [[ "$IMAGE" == *":latest" ]]; then
  echo "오류: prod 환경에서는 latest 태그를 사용할 수 없습니다."
  echo "명확한 버전 태그를 사용하세요. 예: nginx:1.21"
  exit 1
fi

SAFE_IMAGE=$(echo "$IMAGE" | sed 's#[/:]#-#g')

RAW_RESULT="scans/${SAFE_IMAGE}-result.json"
NORMALIZED_RESULT="scans/${SAFE_IMAGE}-normalized.json"
DECISION_RESULT="scans/${SAFE_IMAGE}-decision.json"
REPORT_FILE="reports/${SAFE_IMAGE}-report.md"
AI_GUIDE_FILE="reports/${SAFE_IMAGE}-ai-guide.md"
POLICY_FILE="policies/deploy_policy.rego"


echo "==================================="
echo "[SECURITY GATE] 시작"
echo "==================================="
echo "이미지: $IMAGE"
echo "배포 환경: $ENVIRONMENT"
echo ""

echo "----- 1. Trivy 취약점 스캔 -----"
if ! trivy image "$IMAGE" \
  --scanners vuln \
  --timeout 15m \
  --format json \
  --output "$RAW_RESULT"; then

  echo "[ERROR] Trivy 스캔 실패"
  echo "입력한 값이 존재하지 않는 컨테이너 이미지이거나 접근할 수 없는 이미지일 수 있습니다."
  echo "입력값: $IMAGE"
  exit 1
fi

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

echo "----- 5. AI 한국어 대응 가이드 생성 -----"

if [ -n "$GEMINI_API_KEY" ]; then
  python3 scripts/generate_ai_guide.py \
    "$NORMALIZED_RESULT" \
    "$DECISION_RESULT" \
    "$AI_GUIDE_FILE"

  echo "[OK] AI 가이드 생성 완료: $AI_GUIDE_FILE"
else
  echo "[SKIP] GEMINI_API_KEY가 설정되지 않아 AI 가이드 생성을 건너뜁니다."
fi

echo ""

echo "----- 6. 배포 허용 / 보류 / 차단 처리 -----"

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
echo "AI 대응 가이드: $AI_GUIDE_FILE"

exit $EXIT_CODE
