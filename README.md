# AE-Sentinel Edge / IoT

ESP32 피에조 센서, 로컬 publisher, IoT 계정 인프라의 책임 경계다.

## 반드시 지킬 계약

- 센서는 볼라드가 아니라 **각 계류삭의 선박 측 연결 고리(아이·스플라이스 인근)**에 한 대씩 부착한다.
- AWS IoT Thing 이름을 `sensorId`와 `source.deviceId`로 동일하게 사용한다.
- 원시 topic은 `aesentinel/{sensorId}/piezo`다.
- payload의 `lineId`는 관리자가 해당 센서에 배정한 계류삭과 일치해야 한다.
- 위험도는 센서가 계산하지 않는다. 펌웨어는 실제 `freqHz`와 환경값만 전송한다.

팀 간 전체 흐름은 [협업 인터페이스 계약](https://github.com/AWS-PBL-6/docs/blob/main/docs/contracts/team-collaboration-interfaces.md),
현장 등록·검증 절차는 [센서 운영 가이드](https://github.com/AWS-PBL-6/docs/blob/main/docs/operations/sensor-event-piezo-guide.md),
기계 검증 스키마는 [IoT JSON Schema](https://github.com/AWS-PBL-6/docs/blob/main/packages/contracts/schemas/iot/piezo-frequency-event.v1.json)를 따른다.

## 디렉토리

- `esp32-firmware/`: 센서 샘플링·특징 추출·MQTT 발행 펌웨어
- `publisher-simulator/`: 하드웨어 없이 동일 계약으로 발행하는 시뮬레이터
- `infra/`: IoT Thing·Rule·권한 인프라(추가 시 IaC로 관리)
