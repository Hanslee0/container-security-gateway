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