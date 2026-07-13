# ESP32 피에조 펌웨어 계약

펌웨어는 계류삭 연결 고리의 피에조 압전센서에서 진동 주파수를 측정해 AWS IoT Core로 발행한다.

## 장치 설정값

| 설정 | 예시 | 의미 |
|---|---|---|
| `THING_NAME` | `piezo-mooring-05` | AWS IoT Thing 이름이자 `source.deviceId` |
| `LINE_ID` | `mooring-05` | Backend에서 이 센서에 배정한 계류삭 |
| `SITE_ID` | `busan` | 설치 사이트 |
| `BERTH_ID` | `PNC-1` | 현재 운영 선석 |

MQTT topic은 `aesentinel/{THING_NAME}/piezo`다. 메시지는
[`piezo-frequency-event.v1.json`](https://github.com/AWS-PBL-6/docs/blob/main/packages/contracts/schemas/iot/piezo-frequency-event.v1.json)을
통과해야 한다. `eventId`는 측정마다 새로 만들고 UTC ISO 8601 시각을 사용한다.

Backend는 topic 센서 ID, `source.deviceId`, 배정된 `LineStatus.sensorId`를 비교한다.
불일치하면 `SENSOR_LINE_MISMATCH`, 미배정 라인이면 `LINE_SENSOR_NOT_BOUND`로 거부한다.
