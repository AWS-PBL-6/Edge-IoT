# 피에조 Publisher Simulator

실제 ESP32가 없어도 펌웨어와 같은 MQTT 계약을 검증하는 발표·통합 테스트 도구를 둔다.

## 발행 원칙

- topic: `aesentinel/{sensorId}/piezo`
- payload: [`iot-piezo-frequency-event.v2.json`](https://github.com/AWS-PBL-6/docs/blob/main/packages/contracts/examples/iot-piezo-frequency-event.v2.json)
- `source.deviceId`: topic의 `{sensorId}`와 동일
- `lineId`·`siteId`·`berthId`: 전송하지 않음(Backend가 현재 센서 배정에서 조회)
- 측정값: `freqHz > 0`; 위험도·장력 추정치는 보내지 않음
- heartbeat: `aesentinel/{sensorId}/heartbeat`에 30초마다 발행; MQTT clientId는 sensorId와 동일

정상 시나리오 외에 중복 센서 배정, 미배정 센서, topic/body 센서 ID 불일치도 테스트해
각각 `SENSOR_IN_USE`, `SENSOR_NOT_BOUND`, `VALIDATION_ERROR`가 발생하는지 확인한다.
