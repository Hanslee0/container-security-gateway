# Container Security Gateway

컨테이너 이미지를 배포하기 전에 취약점을 스캔하고, 정책 기준에 따라 배포 가능 여부를 판단하는 보안 게이트웨이 프로젝트

-----

## 구현 기능

- Trivy 스캔
- 결과 정리
- OPA 정책 판단
- 배포 차단
- 기본 리포트 생성

-----

## 추가 예정 기능

- Falco 런타임 이상행위 탐지
- 웹 대시보드
- CI/CD 연동

-----

## 1단계: 기본 스캔 환경 구축 + Trivy 스캔 결과 저장

1. 작업 환경을 Ubuntu-22.04 WSL로 정함
2. Docker 연결 확인
3. 프로젝트 폴더 구조 구성
4. Trivy 설치
5. 첫 번째 이미지 스캔 실행
6. 핵심 정보 추출용 Python 스크립트 작성

추려내는 정보:

- 이미지 이름
- 심각도별 취약점 개수
- CVE ID
- 취약점 심각도
- 취약한 패키지명
- 현재 설치된 버전
- 수정 가능한 버전
- 취약점 제목
- 취약점 설명

명령어:

trivy image nginx:1.21 --scanners vuln --timeout 15m --format json --output scans/nginx-1.21-result.json

-----

## 2단계: OPA 기반 배포 판단 기능 구현

1. OPA 설치
2. 배포 판단 정책 파일 작성
3. normalized.json을 OPA 입력값으로 사용
4. OPA 정책을 실행하여 배포 가능 여부 판단
5. ALLOW / HOLD / BLOCK 결과 확인

정책 기준:

- CRITICAL 취약점 1개 이상 → BLOCK
- CRITICAL은 없지만 HIGH 취약점 3개 이상 → HOLD
- 그 외 → ALLOW

명령어:

opa eval --input scans/nginx-1.21-normalized.json --data policies/deploy_policy.rego "data.deploy.decision" --format pretty

-----

## 3단계: 기본 리포트 생성

1. OPA 판단 결과를 decision.json으로 저장
2. normalized.json과 decision.json을 입력값으로 사용
3. 이미지명, 판단 결과, 판단 사유를 리포트에 포함
4. 심각도별 취약점 개수와 주요 CVE 목록 출력
5. Markdown 형식의 기본 리포트 생성

명령어:

python3 scripts/generate_report.py scans/nginx-1.21-normalized.json scans/nginx-1.21-decision.json reports/nginx-1.21-report.md

-----

## 4단계: 배포 차단 로직 구현

1. OPA 판단 결과인 decision.json을 읽음
2. 결과가 BLOCK이면 배포 차단
3. 결과가 HOLD이면 배포 보류
4. 결과가 ALLOW이면 배포 가능 처리

처리 기준:

- ALLOW → 배포 가능
- HOLD → 배포 보류
- BLOCK → 배포 차단

명령어:

python3 scripts/enforce_policy.py scans/nginx-1.21-decision.json nginx:1.21

-----

## 5단계: 전체 자동화 스크립트 작성

1. Trivy 스캔, 결과 정리, OPA 판단, 리포트 생성, 배포 차단을 하나의 스크립트로 통합
2. 이미지 이름을 입력하면 전체 보안 검사 흐름이 자동으로 실행됨
3. OPA 판단 결과에 따라 ALLOW / HOLD / BLOCK 처리
4. BLOCK이면 배포 차단, HOLD면 배포 보류, ALLOW면 배포 가능 처리

명령어:

./security-gate.sh nginx:1.21

-----

## 6단계: 여러 이미지 테스트

1. 여러 컨테이너 이미지를 대상으로 security-gate.sh를 수동 실행
2. 이미지별 Trivy 스캔, 정규화, OPA 판단, 리포트 생성 흐름 확인
3. 이미지별 ALLOW / HOLD / BLOCK 결과 비교

테스트 이미지:

- nginx:1.21
- alpine:latest
- alpine:3.18
- python:3.8-slim

명령어 예시:

./security-gate.sh nginx:1.21
./security-gate.sh alpine:latest
./security-gate.sh alpine:3.18
./security-gate.sh python:3.8-slim


-----

## 7단계: 정책 기준 세분화

1. 배포 환경을 dev / staging / prod로 구분
2. 환경별로 서로 다른 보안 정책 기준 적용
3. dev는 개발 환경이므로 완화된 기준 적용
4. staging은 운영 전 검증 환경이므로 중간 기준 적용
5. prod는 실제 운영 환경이므로 가장 엄격한 기준 적용
6. 같은 이미지라도 배포 환경에 따라 ALLOW / HOLD / BLOCK 결과가 달라질 수 있도록 구현

정책 기준:

prod 환경
- CRITICAL 1개 이상 → BLOCK
- HIGH 3개 이상 → HOLD
- UNKNOWN 5개 이상 → HOLD
- 그 외 → ALLOW

staging 환경
- CRITICAL 3개 이상 → BLOCK
- CRITICAL 1개 이상 → HOLD
- HIGH 5개 이상 → HOLD
- 그 외 → ALLOW

dev 환경
- CRITICAL 5개 이상 → BLOCK
- HIGH 10개 이상 → HOLD
- 그 외 → ALLOW

명령어:

./security-gate.sh nginx:1.21 dev
./security-gate.sh nginx:1.21 staging
./security-gate.sh nginx:1.21 prod


-----

## 8단계: 리포트 개선

1. 기존 기본 리포트에 배포 환경 정보를 추가
2. 전체 취약점 개수와 심각도별 개수 표시
3. 수정 가능한 취약점 개수 표시
4. CRITICAL/HIGH 취약점 비율 계산
5. 많이 탐지된 취약 패키지 Top 5 출력
6. 주요 조치 대상 CVE 목록 출력
7. 판단 결과별 권장 조치와 재검사 명령어 추가

명령어:

python3 scripts/generate_report.py scans/nginx-1.21-normalized.json scans/nginx-1.21-decision.json reports/nginx-1.21-report.md

-----

## 9단계: AI 한국어 대응 가이드 생성

1. OPA 판단 결과와 정규화된 취약점 정보를 AI 입력값으로 사용
2. AI는 배포 허용/차단을 판단하지 않고, OPA 판단 결과를 설명하는 역할만 수행
3. 이미지명, 배포 환경, 취약점 요약, 주요 CVE 정보를 바탕으로 한국어 대응 가이드 생성
4. 개발자가 이해하기 쉬운 판단 요약, 주요 위험 요소, 권장 조치, 재검사 안내를 Markdown 형식으로 출력

명령어:

python3 scripts/generate_ai_guide.py scans/nginx-1.21-normalized.json scans/nginx-1.21-decision.json reports/nginx-1.21-ai-guide.md

생성 결과:

reports/nginx-1.21-ai-guide.md

-----

## 10단계: AI 가이드 자동화 스크립트 통합

1. 기존 security-gate.sh에 AI 한국어 대응 가이드 생성 단계를 추가
2. GEMINI_API_KEY가 설정되어 있으면 AI 가이드를 자동 생성
3. API 키가 없으면 AI 가이드 생성만 건너뛰고 기존 보안 검사 흐름은 계속 실행
4. Trivy 스캔, 결과 정리, OPA 판단, 리포트 생성, AI 가이드 생성, 배포 차단을 하나의 명령어로 실행

명령어:

./security-gate.sh nginx:1.21 prod

생성 결과:

reports/nginx-1.21-report.md
reports/nginx-1.21-ai-guide.md

## 전체 흐름

Trivy 스캔

↓

결과 정리
↓

OPA 정책 판단
↓

기본 리포트 생성
↓

배포 허용 / 보류 / 차단