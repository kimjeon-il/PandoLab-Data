# 보고서·연구자료 색인

전체 폴더 트리, 확장자 및 명명·보존·삭제 규칙의 정본: **[보고서 구조·확장자 정책](POLICY.md)**. 일반 텍스트와 원본 자료를 바로 열어 볼 수 있으며 Python·노트북·별도 빌드가 필요하지 않습니다.

## 역사 입력 조사 (1801년 이후)

- [국가·속령별 종합 기록](history/countries/): 국가·속령·역사 정치체당 JSON 정본 한 개.
- [10년 단위 실제 변동 사건](history/decades/): `1980-1989/`와 같이 분류한 사건별 JSON. 국가별 중복 파일을 만들지 않습니다.
- [공간 근거](history/geography/): 영토·국경·도서·도시/하천의 형상 검증 및 보류.
- [역사 조사 정책](history/policy.json), [JSON 스키마](history/schema.json), [출처 원장](history/sources/references.json), [조사 진행](history/progress.json), [자동 색인](history/catalog.json).

`history/catalog.json`은 국가별 `byCountry`, 10년별 `byDecade`, 기존 `byEntity`·`byYear` 조회를 지원합니다. 최초 10년 폴더 `1800-1809`에는 1801년 이후 사건만 기록합니다. 정확한 효력일이 불명확하면 날짜 정밀도를 보존하고 사건을 추정해 만들지 않습니다.

색인 갱신은 기존 Node.js 환경에서 `node tools/reports/build-history-index.mjs`를 실행합니다. 보고서 열람·편집에는 실행이 필요하지 않습니다.

## 기술자료 및 보호되는 원본

- [국경·영토 자료](borders/) — `data/`, `history/`, `reconstruction/`, `validation/`
- [수계](hydro/) — `names/`, `calibration/`, `connectivity/`, `releases/` (원본 수계 파일은 `assets/data/hydro/`)
- [개발 검증](development/) — `performance/`, `rendering/`, `ui/`, `storage/`, `native/`, `integrations/`, `releases/`, `ci/`
- [지도 분석](map-analysis/) — `corpus/`(원본·학습 입력), `models/`(학습 모델), `results/`(완료 결과)
- [도시·지명 자료](places/) — 승인/검토 정보, 고정된 입력 배치와 원본 매니페스트

기술자료는 역사 조사 정본과 구분하며, 소비 경로·해시·출처·권리 고지·재현 관계를 검증하지 않고 일괄 이동하거나 확장자를 바꾸지 않습니다.

## 완료된 검증 결과 탐색

- [국경 검증 보존·삭제 이력](borders/validation/README.md), [삭제된 일회성 검증 파일 색인](borders/validation/RETIRED-ONE-OFF-INDEX.json). 국가별 원본 후보와 배치별 요약을 구분합니다.
- [개발 검증 통합 기준](development/README.md), [삭제된 구형 개발 산출물 색인](development/RETIRED-EVIDENCE-INDEX.json). P6.2 릴리스와 원격 브랜치 통합의 완료 내역은 각 하위 폴더의 `consolidated-*.json`에 보관합니다.
- [지도 분석 구조](map-analysis/README.md), [지도 분석 결과](map-analysis/results/README.md), [구형 모델 평가 이력](map-analysis/results/model-evaluations/README.md), [학습 모델](map-analysis/models/README.md).
