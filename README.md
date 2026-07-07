# AE-Sentinel Edge / IoT

Edge 센서 수집, MQTT publish, IoT Account 인프라를 관리하는 저장소다.

## 역할

- ESP32 센서 샘플링
- FFT / feature extraction
- MQTT publish
- 발표 및 로컬 검증용 simulator
- IoT Core / IoT Rule / 디바이스 정책

## 구조

```text
esp32-firmware/
  src/
  include/
publisher-simulator/
  src/
infra/
  iot-account/
```

## 계약 기준

- contracts canonical source: `AWS-PBL-6/docs`
- Backend 로 보내는 payload 는 `ae-feature-event.v1.json` 을 따른다.
