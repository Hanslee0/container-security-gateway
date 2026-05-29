# Container Security Report

## 1. 최종 요약

- 생성 시간: 2026-05-29 20:15:50
- 이미지명: `nginx:1.21`
- 배포 환경: `prod`
- 최종 판단: **BLOCK**
- 판단 사유: prod environment: CRITICAL vulnerabilities found: 28

`nginx:1.21` 이미지는 `prod` 환경 기준에서 **BLOCK** 처리되었습니다. 주요 사유는 `prod environment: CRITICAL vulnerabilities found: 28`이며, CRITICAL 취약점 28개와 HIGH 취약점 144개가 확인되었습니다.

## 2. 취약점 요약

| 항목 | 개수 |
|---|---:|
| 전체 취약점 | 672 |
| CRITICAL | 28 |
| HIGH | 144 |
| MEDIUM | 287 |
| LOW | 198 |
| UNKNOWN | 15 |
| 수정 가능한 취약점 | 396 |
| CRITICAL/HIGH 비율 | 25.6% |

## 3. 많이 탐지된 취약 패키지 Top 5

| 순위 | 패키지명 | 취약점 개수 |
|---:|---|---:|
| 1 | libtiff5 | 72 |
| 2 | curl | 60 |
| 3 | libcurl4 | 60 |
| 4 | libssl1.1 | 32 |
| 5 | openssl | 32 |

## 4. 주요 조치 대상 CVE

CRITICAL/HIGH 취약점 중 우선 확인이 필요한 항목입니다.

| CVE ID | Severity | Package | Installed Version | Fixed Version |
|---|---|---|---|---|
| CVE-2021-22945 | CRITICAL | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-32207 | CRITICAL | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-32221 | CRITICAL | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u5 |
| CVE-2023-23914 | CRITICAL | curl | 7.74.0-1.3+deb11u1 |  |
| CVE-2023-38545 | CRITICAL | curl | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u10 |
| CVE-2021-22945 | CRITICAL | libcurl4 | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-32207 | CRITICAL | libcurl4 | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u2 |
| CVE-2022-32221 | CRITICAL | libcurl4 | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u5 |
| CVE-2023-23914 | CRITICAL | libcurl4 | 7.74.0-1.3+deb11u1 |  |
| CVE-2023-38545 | CRITICAL | libcurl4 | 7.74.0-1.3+deb11u1 | 7.74.0-1.3+deb11u10 |
| CVE-2019-8457 | CRITICAL | libdb5.3 | 5.3.28+dfsg1-0.8 |  |
| CVE-2024-45491 | CRITICAL | libexpat1 | 2.2.10-2+deb11u3 | 2.2.10-2+deb11u6 |
| CVE-2024-45492 | CRITICAL | libexpat1 | 2.2.10-2+deb11u3 | 2.2.10-2+deb11u6 |
| CVE-2022-27404 | CRITICAL | libfreetype6 | 2.10.4+dfsg-1 | 2.10.4+dfsg-1+deb11u1 |
| CVE-2026-33845 | CRITICAL | libgnutls30 | 3.7.1-5 | 3.7.1-5+deb11u10 |

## 5. 권장 조치

- 현재 이미지는 정책 기준을 위반했으므로 배포하지 않는 것을 권장합니다.
- CRITICAL 취약점 또는 정책 위반 항목을 먼저 조치해야 합니다.
- 베이스 이미지를 최신 버전으로 교체하거나 취약 패키지를 업데이트해야 합니다.
- 조치 후 동일한 명령어로 다시 스캔하여 정책 통과 여부를 확인해야 합니다.

## 6. 재검사 명령어

취약점 조치 후 아래 명령어로 다시 검사할 수 있습니다.

`./security-gate.sh nginx:1.21 prod`

## 7. 참고

- 본 리포트는 Trivy 스캔 결과와 OPA 정책 판단 결과를 기반으로 생성되었습니다.
- AI 분석은 포함하지 않은 기본 개선 리포트입니다.
- 실제 운영 환경에서는 조직의 보안 정책에 맞게 판단 기준을 조정해야 합니다.
