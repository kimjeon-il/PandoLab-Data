# 연구자료 색인

지도에 실제 입력할 수 있는 역사 정보의 정본 조사 기록은 [통합 조사 정책](research/policy.json)·[공통 스키마](research/schema.json) 및 [자동 색인](research/catalog.json)으로 관리합니다.

- [객체별 종합 조사서](entities/states/): 국가·속령 등 하나의 객체에 한 기록. 존속기간·국명·국기·상위/하위객체 등 조사 상태와 관련 사건 ID.
- [변동 사건 조사서](events/): 실제 입력 가능한 효력일·관계·국명·영토 변경 사건. 국가·연도별로 보고서를 따로 복제하지 않습니다.
- [공간자료 검증서](geography/borders/): 국경·도서의 실제 귀속·형상·원본 벡터 근거 및 검증 상태. 변동이 검증되지 않은 후보는 사건으로 등록하지 않습니다.
- [사료 목록](sources/references.json) · [순환 진행기록](research/progress.json): 두 자동 조사(GEO-LIFE, GEO-TIME)의 커서와 공통 원자료.

연도별·국가별 조회는 catalog.json의 `byYear`·`byEntity`를 사용합니다. `node tools/reports/build-history-index.mjs` 명령으로 색인을 재생성할 수 있으나 새 정보 검증·GIS 적용은 별도 승인 단계입니다.

기존 GEO-LIFE-034~037, GEO-TIME-033 Markdown과 두 진행기록의 원문은 새 JSON 기록의 `provenance.snapshotUrl`이 가리키는 불변 Git 판본에서 열람할 수 있습니다. 기존 도시 입력 검토 자료([reports/places](places/))와 원본 GIS·개발·수계 검증 증거는 경로를 변경하지 않았습니다.

### 기술 증거 및 원본 자료

- 개발 성능·기술 검증: `reports/development/` — 성능 측정값·비교·재현 근거
- GIS 실행·국경 검증: `reports/borders/validation/`, `reports/development/native/` — 원본 좌표·CRS·검증 증거
- 수계 검증: `reports/hydro/` — 연결성·지명·보정·배포 증거
- 수계 원본: `assets/data/hydro/` — 원본·매니페스트·출처·파생 관계

기술 자료는 역사 입력 조사 색인 `reports/research/catalog.json`에 포함하지 않습니다. 중복 로그·동일 캡처·불필요한 CI 추적 자료만 참조 관계를 확인하여 정리합니다.

### P1 기술자료 통합 (2026-11-20)

- [현대 국경 원본·후보 통합 검증서 색인](borders/validation/modern-raw-source-20261110/merged-source-validation-index.json): 짝을 이루는 94개 증거를 47개 객체별 검증서로 통합. 단독 원본 증거 39개 유지.
- [수계 재구성 공통 도구](hydro/names/reconstruction-2026-10-09/shared/README.md): 중복 스크립트 95개(원본 12종)를 공통 복구·검사·지오메트리 구현과 배치별 정책표로 정리. 원본 Git SHA는 [버전 매핑](hydro/names/reconstruction-2026-10-09/shared/version-map.json)에 보관.
- [WebGL2 측정 실행 메타데이터](development/rendering/project-common-lod-2026-11-10/evidence/world-webgl2.metadata.json): 동일한 두 측정본을 `world-webgl2.json` 정본 하나로 통합.
