# 모델별 학습·평가 이력

실제 코퍼스·모델 가중치가 아니라 **완료된 학습·평가 문서**를 버전별로 보관합니다. `macro-v1/v2/v3`, `diverse-v1/v2`는 각각 **`{version}/evaluation.json` 1개가 JSON 정본**입니다.

통합본의 `records`에는 옛 상대경로(`diagnostics/diagnostics.json` 등)를 키로 하여 원래 JSON 본문(`content`)과 Git blob SHA가 들어 있습니다. `previewFile`로 지정된 이미지는 해당 버전의 원래 `diagnostics/` 또는 `auxiliary-diagnostics/` 폴더에 그대로 있으며 `evidenceAssetsBase`와 원래 JSON 경로를 조합해 확인합니다. 이미지까지 JSON 본문에 복사하지 않습니다.

`macro-v5`는 독립 실험 1건의 검토 JSON·이미지를 유지합니다. 이 디렉터리의 예전 `boundary.manifest.json`은 과거 모델 계보의 기록이고 배포된 가중치가 존재한다는 의미가 아닙니다. 여기의 결과는 독립 평가나 배포 승인을 새로 입증하지 않습니다.
