# 보고서 파일 구조·확장자 및 보존 정책

`PandoLab-library/reports/` 전체에 적용합니다. **이 문서가 디렉터리 구조·확장자·파일명·중복 정리의 정본**이며, 역사 연구의 입력 자격과 스키마는 [history/policy.json](history/policy.json)·[history/schema.json](history/schema.json)을 따릅니다.

## 1. 분리 원칙

1. 입력 연구 **정본**, 원본 GIS·도면 **사료**, 실험 **검증 증거**, 재생성 **산출물**, 실제 **실행 코드**를 구분합니다. 확장자만 변경해서 코드나 원본을 일반 보고서로 위장하지 않습니다.
2. 역사 조사 저장 기준은 **국가·속령별(객체당 하나의 JSON)** 및 **10년 단위(실제 변동 사건당 JSON 하나)**입니다. 대륙별 조사는 순환 일정일 뿐 폴더 분류 기준이 아니며, 50년/대륙별 일괄 보고서를 새로 만들지 않습니다.
3. 일반 텍스트 편집기, VS Code, GitHub에서 열람·편집 가능해야 합니다. Python/Jupyter·별도 빌드·새 GIS 설치를 보고서 편집의 선행 요건으로 두지 않습니다. 색인은 선택적으로 기존 Node.js 표준 기능으로 갱신합니다.
4. 출처·권리/판본·CRS·해시·다른 브랜치의 실제 소비 경로가 걸린 원본과 고유 검증 증거는 단지 디렉터리 통일을 위해 이동·삭제하지 않습니다. 역사 연구와 기술 증거의 정본을 섞지 않습니다.

## 2. 공식 폴더 트리

```text
reports/
├── README.md                     # 전체 탐색 색인
├── POLICY.md                     # 이 정책
├── history/                      # 1801년 이후 입력용 역사 조사
│   ├── countries/                # 국가·속령·역사 정치체별 단일 JSON
│   │   └── korean-empire.json
│   ├── decades/                  # 변동 사건 JSON: 효력 연도 기준
│   │   ├── 1800-1809/            # 1801년 이후부터만 조사
│   │   ├── 1890-1899/
│   │   └── 2020-2029/
│   ├── geography/
│   │   ├── borders/              # 국경·도서·영토 형상 근거
│   │   ├── cities/               # 필요 시 생성
│   │   └── rivers/               # 필요 시 생성
│   ├── sources/references.json   # 출처 정본
│   ├── policy.json               # 역사 입력·조사 정책
│   ├── schema.json               # 역사 JSON 스키마
│   ├── progress.json             # 순환 조사 진행 커서
│   └── catalog.json              # 국가·기간별 파생 색인
├── borders/                      # GIS 영토·국경 기술 자료
│   ├── data/
│   ├── history/
│   ├── reconstruction/
│   └── validation/
├── hydro/                        # 수계 재구성·보정·검증
│   ├── names/
│   ├── calibration/
│   ├── connectivity/
│   └── releases/
├── development/                  # 개발·성능·릴리스 기술 증거
│   ├── ci/
│   ├── integrations/
│   ├── native/
│   ├── performance/
│   ├── releases/
│   ├── rendering/
│   ├── storage/
│   └── ui/
├── map-analysis/                 # 원본 지도 코퍼스·분석 모델·검증
│   ├── corpus/
│   ├── models/
│   └── results/                    # 완료된 분석·실행·출력 결과
└── places/                       # 도시·지명 원장 및 고정된 입력 자료
```

예시에 없는 다른 10년대 디렉터리는 필요할 때만 만듭니다. `borders/`, `hydro/`, `development/`, `map-analysis/`, `places/`는 **현재 유효하며, 경로에 의존하는 자료를 보존하는 공식 영역**입니다. 연구용 자료라는 이유로 모두 `history/`로 이동하지 않습니다.

## 3. 확장자 허용 기준

| 확장자 | 사용 대상 | 보존·변환 규칙 |
| --- | --- | --- |
| `.json` | 역사 국가·사건·공간 정본, 정책/스키마/색인, 기술 검증의 구조화된 결과 | UTF-8; 출처·상태·날짜 정밀도 보존. 다른 형식의 본문 복제 금지 |
| `.md` | 정식 정책·탐색 색인·필수 출처 고지와 설명 | JSON 정본과 중복되는 일지·대륙별/기간별 별도 보고서 생성 금지 |
| `.tsv` | 사람이 비교하기 쉬운 표, 간단한 원본 측정값 | 열 제목 포함·UTF-8; 수식/매크로 배제 |
| `.csv` | 외부 공급 자료·기존 코드와 연결된 표 | 입력 원본의 인코딩·열·구분자 유지; 신규 수작업 표는 TSV 우선 |
| `.geojson` | 벡터 형상·지리 피처 | CRS·공유 경계·원본/파생 관계 검증; 설명문 보고서로 대체 금지 |
| `.jsonl`, `.ndjson` | 대규모 순차 진단/기계 이벤트 자료 | 필요한 경우에만 유지, 각 줄 독립 JSON |
| `.txt`, `.log` | 고유 재현 근거가 있는 원시 출력·공급 원문 | 빈 로그·결론과 동일한 중복 추적은 정리 |
| `.png`, `.jpg`, `.svg` | 출처 이미지·화면/위상 검증 증거 | 중복 캡처 정리, 실제 비교에 필요한 증거는 보존 |
| `.pdf`, `.html`, `.xml` | 원사료·법령·판권·공식 도면·기존 검증 원문 | 원본 포맷·권리·링크를 보존; 문서 형식 변경은 별도 검토 |
| `.gpkg`, `.shp`, `.shx`, `.dbf`, `.gz`, `.zip` 및 바이너리 | GIS 원본·압축 패키지·모델·오라클 | 파일셋/해시/CRS·소비자 확인 없이 일괄 변환·이동 금지 |
| `.mjs`, `.js`, `.cpp` | 실행 코드 또는 원본 결합 재현 절차 | 일반 보고서 아님; 새 공용 코드는 `tools/`에, 증거에 필요한 기존 코드는 근거와 함께 유지 |

일반 조사 문서에 `.py`, `.ipynb`, `.xlsx`, `.docx`, 임의 DB 확장자 등을 새로 도입하지 않습니다. 하지만 외부 원본·필수 실행 환경을 일괄 삭제하거나 확장자만 `.txt`로 바꾸지 않습니다.

## 4. 파일명·시기 분류·참조

- 국가·속령: `history/countries/{lowercase-kebab-slug}.json`. 왕정/공화정 전환만으로 국가를 중복 생성하지 않습니다. 존속기간·국명·국기·상위관계의 역사 상태는 같은 객체에 보강합니다.
- 실제 사건: `history/decades/{YYYY-YYYY}/{event-id}.json`. 10년 구간은 `1980-1989`처럼 0년으로 시작합니다. **최초 구간은 1800–1809이나 1801년부터만 조사**합니다. 연도까지 불명확하면 `undated/`에 저장하며 추측하지 않습니다.
- 사건의 정확한 효력일·정밀도는 `date`, 관계국은 `entityKeys`, 국명/국기/속령/영토 변경은 `changes`로 관리합니다. 다자 간 변경은 JSON 한 건을 공유하고 개별 객체의 `eventIds`에서 참조합니다.
- 검증되지 않은 경계 벡터·좌표는 `history/geography/` 증거이지 확인된 `event`가 아닙니다. 사료의 발행일을 국경 효력일로 추정하지 않습니다.
- `history/catalog.json`의 `byCountry`, `byDecade`, `byEntity`, `byYear`는 원본의 ID 참조용 **파생 색인**입니다. 색인에 보고서 전문을 중복 생성하지 않습니다.
- 기술 증거 파일명에 포함된 `YYYY-MM-DD`는 보통 작업일입니다. 이를 역사적 효력일과 혼동하지 않으며, 원본의 소스/버전/측정 판정을 유지합니다.

## 5. 중복 제거·보존·검증

1. 새 보고서 작성 전 국가 키·사건 ID·동일 데이터 출처를 조회하고 기존 정본을 보강합니다. 동일 사건을 두 지역/국가/10년 파일에 복사하지 않습니다.
2. 구조화할 수 있는 검증 결과는 JSON 정본에, 고유한 원시 로그·사진·원도면·재현 기록은 주제별 기술 영역에 보관합니다. 반복·빈 로그나 동일 캡처는 사용처를 확인한 뒤 정리합니다.
3. 고정된 `reports/places/tier1-major-cities-batch*.json`, GIS 원본, 매니페스트, `archive/index.json`과 Git 객체, 저작권 고지, 출처/CRS/해시, 실행 중 체크포인트 및 소스 고정 핀은 보존합니다.
4. 내용을 잃지 않고 폐기된 자료는 Git 커밋의 불변 이력으로 추적합니다. `backup/`·`archive/`·Markdown 복사본을 만들어 중복 복구하지 않으며 Git 이력을 재작성하지 않습니다.
5. 보고서 편집은 국가·지도 정본의 적용 승인이나 배포를 의미하지 않습니다. 보고서만 변경했다면 전체 빌드·GIS 재생성을 실행하지 않습니다.

## 6. 지도 분석의 원본·학습·결과물 분리

- **원본**: `reports/map-analysis/corpus/{dataset}/sources/` 및 `reports/map-analysis/corpus/sources/`에 원도면·원본 이미지·제공처 메타데이터·권리 고지를 보관합니다. 원본 위치와 상대경로가 현행 코퍼스에서 참조되므로 재배치하지 않습니다.
- **학습 입력**: `reports/map-analysis/corpus/{dataset}/labels/`, `derived/`, `corpus*.training.json`과 `reports/map-analysis/models/`의 학습 체크포인트·평가 결과를 구분합니다. 학습에서 사용한 `derived/` 이미지는 단순 임시 출력이 아니라 명세서가 직접 참조하는 입력이므로 자동 삭제하지 않습니다.
- **작업 결과**: 지도 분석·네이티브 실행·플러그인 검증의 완성된 보고/내보내기 결과는 `reports/map-analysis/results/`에 둡니다. 종전 `map-analysis/reports/`의 완료 결과는 `results/`로 이동했으며, 결과 내부 매니페스트의 경로도 갱신합니다.
- **전환 보류**: `corpus/gazetteer-v1/runtime/`의 지명 검색용 분할 인덱스, `models/`의 모델 바이너리와 여러 코퍼스의 상호참조 파일은 외부 소비 경로·해시·학습 명세가 확인되기 전까지 원래 위치에 둡니다. 보류는 새 결과물과 원본을 혼합 저장해도 된다는 허가가 아닙니다.

`reports/map-analysis/README.md`에 현재 탐색 경로와 신규 파일의 분류 예시를 제공합니다. 정리 대상의 원문을 `backup`·추가 산출물로 복사하지 않으며, 구형 경로가 필요하면 이동 이전 Git 판본을 참조합니다.

## 7. 검증 보고서의 완료 이후 유지 방식

- **국경 검증**: `borders/validation/`에서 완료된 일회성 재현 스크립트·중복 콘솔 출력을 제거하고 `RETIRED-ONE-OFF-INDEX.json`으로 이전 경로·Git blob SHA를 추적합니다. 같은 배치의 개별 국가 검증은 `modern-raw-source-20261110/{batch}/source-validation-rollup.json` 또는 `evidence-rollup.json` 등으로 묶습니다. 통합 JSON의 `records[].content`/ `records[].data`가 원래 판정을 보유하고, 미적용 후보의 파일 내용은 해당 Git 커밋에서 찾습니다. 국경 원본 형상·좌표·원사료는 이러한 정리만으로 폐기하지 않습니다.
- **개발 검증**: 종료된 구형 UI 릴리스·브랜치 통합의 검사 증거는 `development/ui/*/consolidated-release.json`, `development/integrations/*/consolidated-integration.json` 등 하나의 범주별 결과물로 유지합니다. 원시 로그, 완성 뒤의 일회성 스크립트·캡처, 임시 상태는 `development/RETIRED-EVIDENCE-INDEX.json`을 통해 이전 Git 판본에서 추적합니다. 과거의 성공/실패 기록을 현재 코드의 테스트 승인으로 해석하지 않습니다.
- **지도 분석**: 외부 원본·권리 문서는 `map-analysis/corpus/*/sources/`, 학습용 레이블과 참조 파생 이미지는 `corpus/*/{labels,derived}/`, 모델 가중치·체크포인트는 `map-analysis/models/`에 둡니다. 실제 평가·진단·미배포 실험 결과는 `map-analysis/results/model-evaluations/`, 기타 실행 결과는 `map-analysis/results/`로 분리합니다. 승인되지 않은 학습 산출물은 현재 서비스에 배포된 모델이 아닙니다.
- **완료 후 정리 순서**: 정본 식별 → 구조화된 최종 결과 통합 → 고유 원본·소비 경로·출처 보호 → 불필요한 파일 제거 → Git 이전 경로 기록 → 색인 갱신. 폴더 통합만으로 실제 GIS 데이터 적용, 현재 코드 검증, 서비스 배포를 수행한 것으로 기록하지 않습니다.

## 8. 지도 분석 같은 종류 파일 통합 규칙

1. 구형 모델의 평가·학습 보고서는 모델 버전별 `results/model-evaluations/{version}/evaluation.json` 하나로, 활성/미승인 가중치 주변의 비실행 연구 요약은 `models/{version}/training-evaluation.json`으로 묶습니다. 가중치·모델 매니페스트·진단용 벡터/이미지와 실제 독립 입력을 함께 묶지 않습니다.
2. `corpus/quality-v2/selected/sources/source-provenance.json`은 같은 코퍼스의 공급처 18건의 라이선스·출처·해시 통합 원장이고, `derived/derived-metadata.json`은 변환 이미지 5건의 메타데이터 통합 원장입니다. 원본 지도·이미지 자체는 이동하지 않습니다.
3. `results/plugin-migration/runtime-verification.json`은 과거 플랫폼 검사 판정을 하나로 모은 보존 기록입니다. 바이너리 내보내기·개별 대형 job 결과는 삭제하지 않습니다.
4. JSON 통합 시 `records[기존 상대경로].content`와 Git blob SHA를 함께 보존합니다. 완성된 증거 이미지는 외부 파일로 두고 상대경로를 유지합니다.
5. **검색 인덱스/학습 입력 예외**: `corpus/gazetteer-v1/runtime/names`(4,096), `records`(256), `manifest.json`(1)은 4,353개의 검색 파생 파일이며 보고서가 아닙니다. `corpus/*/labels`, 훈련 명세서 및 실제 GIS 파일도 코드 소비자가 직접 읽으므로 현재 분할을 유지합니다. 이 데이터의 파일 수를 줄이려면 검색·학습 로더와 파일별 해시 계약을 동시에 개편해야 합니다. 검증 없이 경로만 삭제하거나 JSON을 합치지 않습니다.
