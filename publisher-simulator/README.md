# 피에조 Publisher Simulator

실제 ESP32가 없어도 펌웨어와 같은 MQTT 계약을 검증하는 발표·통합 테스트 도구를 둔다.

## 발행 원칙

- topic: `aesentinel/{sensorId}/piezo`
- payload: [`iot-piezo-frequency-event.v1.json`](https://github.com/AWS-PBL-6/docs/blob/main/packages/contracts/examples/iot-piezo-frequency-event.v1.json)
- `source.deviceId`: topic의 `{sensorId}`와 동일
- `payload.lineId`: Backend에서 그 센서에 배정한 계류삭과 동일
- 측정값: `freqHz > 0`; 위험도·장력 추정치는 보내지 않음

정상 시나리오 외에 중복 센서 배정, 잘못된 `lineId`, PENDING 라인 이벤트도 테스트해
각각 `SENSOR_IN_USE`, `SENSOR_LINE_MISMATCH`, `LINE_SENSOR_NOT_BOUND`가 발생하는지 확인한다.
