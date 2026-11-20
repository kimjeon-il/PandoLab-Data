# 지도 분석 학습 모델

이 디렉터리는 **실제 체크포인트가 있는 모델과 모델 자체에 필수적인 메타데이터**만 둡니다. 현재 남겨 둔 `macro-v4/`의 `boundary.onnx`·`boundary.pt`는 학습 산출물이지만 `boundary.manifest.json`의 `trainingOnly=true`, `releaseApproved=false`이므로 서비스 승인된 모델로 취급하지 않습니다.

가중치가 없던 옛 `diverse-v1/v2`, `macro-v1/v2/v3/v5`, `usgs-publisher-v1` 학습·진단 자료는 `../results/model-evaluations/`로 옮겼거나 중복 로그를 제거했습니다. 학습 입력·원본 도면은 `../corpus/`에서 분리 관리합니다.
