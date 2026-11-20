# 모델별 실험 및 평가 결과

실제 학습용 코퍼스나 모델 가중치가 아닌 **진단·평가·실험 이력**을 모델 버전별로 보관합니다. 이전 `models/{version}/`에서 이동한 파일은 상대 디렉터리 구조(예: `diagnostics/` 및 `auxiliary-diagnostics/`)를 보존해 진단 JSON의 `previewFile`과 미리보기 이미지가 연결되도록 했습니다.

`macro-v1`·`macro-v2`·`macro-v3`·`diverse-v1`·`diverse-v2`의 기존 `boundary.manifest.json`은 모형 계보의 **과거 기록**이며 체크포인트가 이 위치에 있다는 뜻이 아닙니다. 독립 평가·릴리스 승인은 이 이동으로 새로 확보되지 않습니다.
