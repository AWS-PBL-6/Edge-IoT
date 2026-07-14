# ESP32 피에조 펌웨어 계약

펌웨어는 계류삭 연결 고리의 피에조 압전센서에서 진동 주파수를 측정해 AWS IoT Core로 발행한다.

## 장치 설정값

| 설정 | 예시 | 의미 |
|---|---|---|
| `THING_NAME` | `piezo-mooring-05` | AWS IoT Thing 이름이자 `source.deviceId` |

MQTT topic은 `aesentinel/{THING_NAME}/piezo`다. 메시지는
[`piezo-frequency-event.v2.json`](https://github.com/AWS-PBL-6/docs/blob/main/packages/contracts/schemas/iot/piezo-frequency-event.v2.json)을
통과해야 한다. `eventId`는 측정마다 새로 만들고 UTC ISO 8601 시각을 사용한다.

펌웨어는 `lineId`·`siteId`·`berthId`를 저장하거나 전송하지 않는다. Backend는 topic의 센서
ID로 현재 `LineStatus.sensorId` 배정을 조회하며, 미배정 센서는 `SENSOR_NOT_BOUND`로 거부한다.

## 온라인 상태 heartbeat

- MQTT `clientId`는 반드시 `THING_NAME`과 동일하게 연결한다.
- `aesentinel/{THING_NAME}/heartbeat`에 [heartbeat JSON](https://github.com/AWS-PBL-6/docs/blob/main/packages/contracts/examples/iot-sensor-heartbeat.v1.json)을 30초마다 발행한다.
- 측정값 발행도 heartbeat로 인정하지만, 측정 주기와 무관한 전용 heartbeat를 유지한다.
- Backend는 AWS IoT 연결/해제 lifecycle 이벤트를 즉시 반영하고 120초 무응답이면 오프라인 처리한다.
