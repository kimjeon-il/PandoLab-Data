# 연구자료 색인

지도에 실제 입력할 수 있는 역사 정보의 정본 조사 기록은 [통합 조사 정책](research/policy.json)·[공통 스키마](research/schema.json) 및 [자동 색인](research/catalog.json)으로 관리합니다.

- [객체별 종합 조사서](entities/states/): 국가·속령 등 하나의 객체에 한 기록. 존속기간·국명·국기·상위/하위객체 등 조사 상태와 관련 사건 ID.
- [변동 사건 조사서](events/): 실제 입력 가능한 효력일·관계·국명·영토 변경 사건. 국가·연도별로 보고서를 따로 복제하지 않습니다.
- [공간자료 검증서](geography/borders/): 국경·도서의 실제 귀속·형상·원본 벡터 근거 및 검증 상태. 변동이 검증되지 않은 후보는 사건으로 등록하지 않습니다.
- [사료 목록](sources/references.json) · [순환 진행기록](research/progress.json): 두 자동 조사(GEO-LIFE, GEO-TIME)의 커서와 공통 원자료.

연도별·국가별 조회는 catalog.json의 `byYear`·`byEntity`를 사용합니다. `node tools/reports/build-history-index.mjs` 명령으로 색인을 재생성할 수 있으나 새 정보 검증·GIS 적용은 별도 승인 단계입니다.

기존 GEO-LIFE-034~037, GEO-TIME-033 Markdown과 두 진행기록의 원문은 새 JSON 기록의 `provenance.snapshotUrl`이 가리키는 불변 Git 판본에서 열람할 수 있습니다. 기존 도시 입력 검토 자료([reports/places](places/))와 원본 GIS·개발·수계 검증 증거는 경로를 변경하지 않았습니다.
