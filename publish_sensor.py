import json
import os
import time
import uuid
from datetime import datetime, timezone

import serial
from awscrt import mqtt
from awsiot import mqtt_connection_builder


SERIAL_PORT = "COM8"
SERIAL_BAUD = 9600

AWS_IOT_ENDPOINT = "a1ufy9lg12m67z-ats.iot.ap-northeast-2.amazonaws.com"

# topic의 {sensorId} = source.deviceId = 관리 화면에서 lineId에 배정한 sensorId
SENSOR_ID = "factorypulse_gateway_01"
CLIENT_ID = SENSOR_ID


PATH_TO_CERT = "certs/device.pem.crt"
PATH_TO_KEY = "certs/private.pem.key"
PATH_TO_ROOT_CA = "certs/AmazonRootCA1.pem"

# aesentinel/{sensorId}/piezo — IoT Rule이 이 topic을 구독해 Lambda를 호출한다
TOPIC = f"aesentinel/{SENSOR_ID}/piezo"


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def build_event(freq_hz, occurred_at):
    # topicSensorId는 보내지 않는다. IoT Rule이 topic에서 읽어 추가한다.
    return {
        "schemaVersion": "1.0.0",
        "eventType": "piezo.frequency.detected",
        "eventId": f"evt-{uuid.uuid4()}",
        "traceId": f"trc-{uuid.uuid4()}",
        "occurredAt": occurred_at,
        "sentAt": utc_now_iso(),
        "source": {
            "account": "iot",
            "service": "esp32-piezo",
            "deviceId": SENSOR_ID,
        },
        "payload": {
            "siteId": SITE_ID,
            "berthId": BERTH_ID,
            "lineId": LINE_ID,
            "freqHz": freq_hz,
        },
    }


print("ENDPOINT:", AWS_IOT_ENDPOINT)
print("CLIENT_ID:", CLIENT_ID)
print("TOPIC:", TOPIC)
print("CERT EXISTS:", os.path.exists(PATH_TO_CERT), PATH_TO_CERT)
print("KEY EXISTS:", os.path.exists(PATH_TO_KEY), PATH_TO_KEY)
print("ROOT CA EXISTS:", os.path.exists(PATH_TO_ROOT_CA), PATH_TO_ROOT_CA)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=AWS_IOT_ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    ca_filepath=PATH_TO_ROOT_CA,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print("Connecting to AWS IoT Core...")
mqtt_connection.connect().result()
print("Connected to AWS IoT Core.")

print(f"Opening Bluetooth serial port {SERIAL_PORT}...")
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=2)
time.sleep(2)
print("Bluetooth serial opened.")

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if not line:
            continue

        # Arduino output example:
        # 28.5
        try:
            freq_hz = float(line)
        except ValueError:
            print("Skip:", line)
            continue

        occurred_at = utc_now_iso()

        # freqHz는 0보다 큰 값만 전송한다
        if freq_hz <= 0:
            print("Skip non-positive freqHz:", freq_hz)
            continue

        event = build_event(freq_hz, occurred_at)

        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(event),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )[0].result()

        print("Published:", event)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    ser.close()
    mqtt_connection.disconnect().result()
    print("Disconnected.")
