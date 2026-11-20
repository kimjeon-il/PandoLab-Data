# 지도 분석 파일 분류

[전체 보고서 구조 정책](../POLICY.md)의 지도 분석 조항에 따릅니다. 기존 이미지·지도 원본의 재배포 조건과 출처 표기를 유지합니다.

| 구분 | 경로 | 저장 내용 |
| --- | --- | --- |
| 분할 검색 인덱스 | `corpus/gazetteer-v1/runtime/` | 검색용 해시 버킷 4,096개·레코드 버킷 256개 및 경로/해시 매니페스트 1개. 일반 보고서가 아니라 별도 로더가 필요해 현재 분할 유지 |
| 원본 자료 | `corpus/{dataset}/sources/`, `corpus/sources/` | 기관 제공 원본 지도·이미지·ZIP·PDF 및 출처·저작권 메타데이터 |
| 공급처 메타데이터 | `corpus/quality-v2/selected/sources/source-provenance.json` | 원본 지도 18건의 출처·라이선스·해시를 통합한 JSON. 실제 원본 지도는 `sources/`에 그대로 보존 |
| 파생 이미지 메타데이터 | `corpus/quality-v2/selected/derived/derived-metadata.json` | PDF·원도면에서 변환된 이미지 5건의 경로·치수·해시를 통합 |
| 학습 원장 | `corpus/{dataset}/corpus*.training.json`, `labels/` | 학습 표본 목록·원도면/라벨 상대경로·데이터 분할 정보 |
| 학습 중간 입력 | `corpus/{dataset}/derived/` | 학습 명세가 참조하는 변환 이미지·마스크·타일 |
| 학습 모델 | `models/` | 실제 체크포인트, 가중치·학습 메타데이터 및 모델 로컬 검증 의존성 |
| 평가·구형 실험 | `results/model-evaluations/{version}/evaluation.json` | 학습 요약·평가·재현 판정을 버전당 JSON 1개로 통합. 진단 이미지는 별도 보존 |
| 분석 결과 | `results/` | Windows 검증 통합본, 플러그인 검증 `plugin-migration/runtime-verification.json`, GIS 내보내기 결과 |

완료된 평가 결과는 `results/model-evaluations/`에 둡니다. 실제 모델 가중치가 없는 과거 실험은 `models/`에 남겨 실행 가능한 모델로 오인하지 않게 합니다. `models/macro-v4/`의 `.onnx`·`.pt`와 모델 로컬 진단 의존성은 유지하지만 이 모델도 `trainingOnly=true`, `releaseApproved=false`입니다. 완료된 결과의 정본을 `results/` 밖으로 새로 복제하지 않습니다. `corpus/gazetteer-v1/runtime/`의 4,353개 분할 인덱스는 현재 참조 보존을 위해 경로를 유지하며, 원자료가 아니라 검색용 파생 데이터라는 의미입니다. 원본과 학습 자료가 혼재된 기존 코퍼스의 상대경로를 바꾸는 작업은 해당 소비자의 참조·해시 검증과 함께 별도로 해야 합니다. 보고서 정리만으로 별도 빌드·GIS 재생성을 실행하지 않습니다.

## 같은 종류의 JSON 묶음 기준

- **완료된 검증·평가 문서**는 대상 프로젝트·모델 버전별 하나의 JSON을 정본으로 사용합니다. 원문 구조는 `records`(원래 파일명별 `content`)에 남기고 Git blob SHA를 기록합니다.
- **공급처 출처·라이선스 및 파생 이미지 속성**은 집합 메타데이터로 통합합니다. 이미지·PDF·GeoPackage와 학습의 직접 입력은 원래 경로를 유지합니다.
- **직접 읽히는 학습 라벨과 지명 해시 버킷**은 단순 보고서가 아닙니다. `corpus*.training.json`의 `annotations`, `image` 및 `runtime/manifest.json`의 파일별 SHA-256을 실제 로더·생성기와 함께 바꾸기 전에는 합치거나 삭제하지 않습니다.
- 지도 분석의 분할 인덱스 4,353개는 파일 수의 대부분을 차지하지만 중복 보고서가 아닙니다. 사용처·확장 방식 확인 전까지 현재 파일 경로를 유지합니다.
