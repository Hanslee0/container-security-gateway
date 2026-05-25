# Container Security Report

- 생성 시간: 2026-05-25 17:02:23
- 이미지명: `python:3.8-slim`

## 1. 정책 판단 결과

- 결과: **BLOCK**
- 사유: Critical vulnerabilities found: 7

## 2. 취약점 요약

| Severity | Count |
|---|---:|
| CRITICAL | 7 |
| HIGH | 43 |
| MEDIUM | 115 |
| LOW | 122 |
| UNKNOWN | 1 |

## 3. 주요 취약점 목록

CRITICAL/HIGH 취약점 중 일부를 표시합니다.

| CVE ID | Severity | Package | Installed Version | Fixed Version |
|---|---|---|---|---|
| CVE-2025-68973 | HIGH | gpgv | 2.2.40-1.1 | 2.2.40-1.1+deb12u2 |
| CVE-2026-4878 | HIGH | libcap2 | 1:2.66-4 | 1:2.66-4+deb12u3 |
| CVE-2023-52425 | HIGH | libexpat1 | 2.5.0-1+deb12u1 | 2.5.0-1+deb12u2 |
| CVE-2025-59375 | HIGH | libexpat1 | 2.5.0-1+deb12u1 |  |
| CVE-2026-25210 | HIGH | libexpat1 | 2.5.0-1+deb12u1 |  |
| CVE-2026-45186 | HIGH | libexpat1 | 2.5.0-1+deb12u1 |  |
| CVE-2026-33845 | CRITICAL | libgnutls30 | 3.7.9-2+deb12u3 | 3.7.9-2+deb12u7 |
| CVE-2026-42010 | CRITICAL | libgnutls30 | 3.7.9-2+deb12u3 | 3.7.9-2+deb12u7 |
| CVE-2025-32988 | HIGH | libgnutls30 | 3.7.9-2+deb12u3 | 3.7.9-2+deb12u5 |
| CVE-2025-32990 | HIGH | libgnutls30 | 3.7.9-2+deb12u3 | 3.7.9-2+deb12u5 |
| CVE-2026-33846 | HIGH | libgnutls30 | 3.7.9-2+deb12u3 | 3.7.9-2+deb12u7 |
| CVE-2026-3833 | HIGH | libgnutls30 | 3.7.9-2+deb12u3 | 3.7.9-2+deb12u7 |
| CVE-2026-42009 | HIGH | libgnutls30 | 3.7.9-2+deb12u3 | 3.7.9-2+deb12u7 |
| CVE-2026-40356 | HIGH | libgssapi-krb5-2 | 1.20.1-2+deb12u2 |  |
| CVE-2026-40356 | HIGH | libk5crypto3 | 1.20.1-2+deb12u2 |  |

## 4. 권장 조치

- Critical 취약점이 존재하므로 현재 이미지는 배포하지 않는 것을 권장합니다.
- 베이스 이미지를 최신 버전으로 교체하거나 취약 패키지를 업데이트해야 합니다.
- 수정 후 Trivy 스캔과 OPA 정책 판단을 다시 실행해야 합니다.

## 5. 참고

- 본 리포트는 Trivy 스캔 결과와 OPA 정책 판단 결과를 기반으로 생성되었습니다.
- AI 분석은 포함하지 않은 기본 리포트입니다.
- 실제 운영 환경에서는 조직의 보안 정책에 맞게 판단 기준을 조정해야 합니다.
