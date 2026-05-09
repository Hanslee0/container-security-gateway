# Container Security Gateway

컨테이너 이미지를 배포하기 전에 Trivy로 취약점을 스캔하고,  
정책 판단에 필요한 핵심 정보를 추출하는 보안 게이트웨이 프로젝트입니다.

## 현재 구현 단계

1. Ubuntu-22.04 WSL 환경 구성
2. Docker 연결 확인
3. 프로젝트 폴더 구조 구성
4. Trivy 설치
5. nginx:1.21 이미지 스캔 실행
6. Trivy 원본 JSON에서 핵심 정보를 추출하는 Python 스크립트 작성

## 폴더 구조

```text
container-security-gateway/
├── scans/
├── reports/
├── policies/
├── scripts/
│   └── normalize_trivy.py
└── README.md
