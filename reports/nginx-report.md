# Container Security Report

## 1. 최종 요약

- 생성 시간: 2026-05-29 20:28:28
- 이미지명: `nginx`
- 배포 환경: `dev`
- 최종 판단: **HOLD**
- 판단 사유: dev environment: HIGH vulnerabilities are 10 or more: 33

`nginx` 이미지는 `dev` 환경 기준에서 **HOLD** 처리되었습니다. 즉시 배포하기보다는 보안 검토 또는 취약점 조치 후 재검사가 필요합니다.

## 2. 취약점 요약

| 항목 | 개수 |
|---|---:|
| 전체 취약점 | 233 |
| CRITICAL | 2 |
| HIGH | 33 |
| MEDIUM | 72 |
| LOW | 119 |
| UNKNOWN | 7 |
| 수정 가능한 취약점 | 9 |
| CRITICAL/HIGH 비율 | 15.02% |

## 3. 많이 탐지된 취약 패키지 Top 5

| 순위 | 패키지명 | 취약점 개수 |
|---:|---|---:|
| 1 | curl | 17 |
| 2 | libcurl4t64 | 17 |
| 3 | libc-bin | 11 |
| 4 | libc6 | 11 |
| 5 | libheif-plugin-dav1d | 10 |

## 4. 주요 조치 대상 CVE

CRITICAL/HIGH 취약점 중 우선 확인이 필요한 항목입니다.

| CVE ID | Severity | Package | Installed Version | Fixed Version |
|---|---|---|---|---|
| CVE-2026-42496 | CRITICAL | perl-base | 5.40.1-6 |  |
| CVE-2026-8376 | CRITICAL | perl-base | 5.40.1-6 |  |
| CVE-2026-5773 | HIGH | curl | 8.14.1-2+deb13u3 |  |
| CVE-2026-6276 | HIGH | curl | 8.14.1-2+deb13u3 |  |
| CVE-2026-5773 | HIGH | libcurl4t64 | 8.14.1-2+deb13u3 |  |
| CVE-2026-6276 | HIGH | libcurl4t64 | 8.14.1-2+deb13u3 |  |
| CVE-2026-33164 | HIGH | libde265-0 | 1.0.15-1+b3 |  |
| CVE-2026-25210 | HIGH | libexpat1 | 2.7.1-2 |  |
| CVE-2026-45186 | HIGH | libexpat1 | 2.7.1-2 |  |
| CVE-2026-40356 | HIGH | libgssapi-krb5-2 | 1.21.3-5 | 1.21.3-5+deb13u1 |
| CVE-2025-68431 | HIGH | libheif-plugin-dav1d | 1.19.8-1 |  |
| CVE-2026-32740 | HIGH | libheif-plugin-dav1d | 1.19.8-1 |  |
| CVE-2026-32741 | HIGH | libheif-plugin-dav1d | 1.19.8-1 |  |
| CVE-2026-32882 | HIGH | libheif-plugin-dav1d | 1.19.8-1 |  |
| CVE-2026-41071 | HIGH | libheif-plugin-dav1d | 1.19.8-1 |  |

## 5. 권장 조치

- 현재 이미지는 즉시 배포하기보다 보안 검토가 필요합니다.
- HIGH 취약점 또는 CRITICAL 취약점 존재 여부를 우선 확인해야 합니다.
- 운영 환경 배포 전 주요 취약점에 대한 조치 계획을 수립해야 합니다.
- 예외적으로 배포해야 한다면 보안 담당자의 승인 절차가 필요합니다.

## 6. 재검사 명령어

취약점 조치 후 아래 명령어로 다시 검사할 수 있습니다.

`./security-gate.sh nginx dev`

## 7. 참고

- 본 리포트는 Trivy 스캔 결과와 OPA 정책 판단 결과를 기반으로 생성되었습니다.
- AI 분석은 포함하지 않은 기본 개선 리포트입니다.
- 실제 운영 환경에서는 조직의 보안 정책에 맞게 판단 기준을 조정해야 합니다.
