# 지도 분석 결과물

이 폴더는 코퍼스 원본·훈련 입력·모델 바이너리와 분리한 **완료 결과**를 보관합니다.

- `plugin-migration/`: 지오리퍼런스·지도 플러그인 완료 결과 및 GIS 내보내기 파일. 공통 런타임·플랫폼 검증 8개는 `runtime-verification.json`으로 통합하고, 대형 개별 job/GeoPackage 결과는 분리 보존합니다. 원본 지도와 혼합하지 않습니다.
- `windows-runtime-2026-10-23.json`: 동일한 Windows 네이티브 테스트에서 생성된 8개 중간·최종 JSON을 원문 객체별로 합친 보존용 기록이며 **현재 Viewer의 테스트 성공 판정이 아닙니다**.
- `source-inventory-dimensions.json`: 지도 원본 인벤토리의 치수 분석 결과.

반복 콘솔 출력 `*.log`와 삭제된 구형 작업트리의 절대 경로만 포함한 `corpus-inventory.json`은 현행 정본이 아니어서 제외했습니다. 삭제 전 원시 데이터는 Git 커밋 `65450c3a7894`에서 확인할 수 있습니다. 원본은 `../corpus/*/sources/`, 학습 입력은 `../corpus/*/{labels,derived}/`, 가중치는 `../models/`에 있습니다.
