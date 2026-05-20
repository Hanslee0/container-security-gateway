# Container Security Gateway

컨테이너 이미지를 배포하기 전에 Trivy로 취약점을 스캔하고,  
정책 판단에 필요한 핵심 정보를 추출하는 보안 게이트웨이 프로젝트

## 현재 구현 단계

Trivy 스캔
결과 정리
OPA 정책 판단
배포 차단
기본 리포트

Falco 런타임 이상행위 탐지
웹 대시보드
CI/CD 연동


----1단계: 기본 스캔 환경 구축 + Trivy 스캔 결과 저장
1. 작업환경 ubuntu로 정함
2. Docker 연결 확인
3. 프로젝트 폴더 구조 구성
4. Trivy 설치
5. 첫 번째 이미지 스캔 실행 
6. 핵심 정보 추출용 Python 스크립트 작성

(추려내는 정보: 

이미지 이름
심각도별 취약점 개수
CVE ID
취약점 심각도
취약한 패키지명
현재 설치된 버전
수정 가능한 버전
취약점 제목
취약점 설명)

명령어: (trivy image nginx:1.21 --scanners vuln --timeout 15m --format json --output scans/nginx-1.21-result.json)

--------2단계: OPA 기반 배포 판단 기능 구현

OPA 설치
배포 판단 정책 파일 작성
normalized.json을 OPA 입력값으로 사용
OPA 정책을 실행하여 배포 가능 여부 판단
ALLOW / HOLD / BLOCK 결과 확인

(정책 기준:

CRITICAL 취약점 1개 이상 → BLOCK
CRITICAL은 없지만 HIGH 취약점 3개 이상 → HOLD
그 외 → ALLOW)

명령어: opa eval \
  --input scans/nginx-1.21-normalized.json \
  --data policies/deploy_policy.rego \
  "data.deploy.decision" \
  --format pretty
