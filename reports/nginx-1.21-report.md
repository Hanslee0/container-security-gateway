# Container Security Report

- 생성 시간: 2026-05-25 17:00:52
- 이미지명: `nginx:1.21`

## 1. 정책 판단 결과

- 결과: **BLOCK**
- 사유: Critical vulnerabilities found: 26

## 2. 취약점 요약

| Severity | Count |
|---|---:|
| CRITICAL | 26 |
| HIGH | 156 |
| MEDIUM | 263 |
| LOW | 211 |
| UNKNOWN | 13 |

## 3. 주요 취약점 목록

CRITICAL/HIGH 취약점 중 일부를 표시합니다.

| CVE ID | Severity | Package | Installed Version | Fixed Version |
|---|---|---|---|---|
| CVE-2022-3715 | HIGH | bash | 5.1-2+b3 |  |
| CVE-2021-22945 | CRITICAL | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-32207 | CRITICAL | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-32221 | CRITICAL | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u5 |
| CVE-2023-23914 | CRITICAL | curl | 7.74.0-1.3+deb11u1 |  |
| CVE-2023-38545 | CRITICAL | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u10 |
| CVE-2021-22946 | HIGH | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-22576 | HIGH | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-27775 | HIGH | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-27781 | HIGH | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-27782 | HIGH | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-42916 | HIGH | curl | 7.74.0-1.3+deb11u1 |  |
| CVE-2022-43551 | HIGH | curl | 7.74.0-1.3+deb11u1 |  |
| CVE-2023-27533 | HIGH | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u8 |
| CVE-2023-27534 | HIGH | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u8 |

## 4. 권장 조치

- Critical 취약점이 존재하므로 현재 이미지는 배포하지 않는 것을 권장합니다.
- 베이스 이미지를 최신 버전으로 교체하거나 취약 패키지를 업데이트해야 합니다.
- 수정 후 Trivy 스캔과 OPA 정책 판단을 다시 실행해야 합니다.

## 5. 참고

- 본 리포트는 Trivy 스캔 결과와 OPA 정책 판단 결과를 기반으로 생성되었습니다.
- AI 분석은 포함하지 않은 기본 리포트입니다.
- 실제 운영 환경에서는 조직의 보안 정책에 맞게 판단 기준을 조정해야 합니다.
