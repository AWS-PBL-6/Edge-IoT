import json
import random
import time
import uuid
from datetime import datetime, timezone

from awscrt import mqtt
from awsiot import mqtt_connection_builder


AWS_IOT_ENDPOINT = "a1ufy9lg12m67z-ats.iot.ap-northeast-2.amazonaws.com"

# topic의 {sensorId} = source.deviceId = 관리 화면에서 lineId에 배정한 sensorId
SENSOR_ID = "factorypulse_gateway_01"
CLIENT_ID = SENSOR_ID

SITE_ID = "yard-a"
BERTH_ID = "berth-02"
# 관리 화면에 등록된 계류삭 lineId (미등록이면 LINE_NOT_FOUND)
LINE_ID = "mooring-20260713-86204c88"

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
print("Connected.")

try:
    while True:
        freq_hz = round(random.uniform(20.0, 40.0), 1)

        event = build_event(freq_hz, utc_now_iso())

        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(event),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )[0].result()

        print("Published:", event)
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped")

finally:
    mqtt_connection.disconnect().result()
    print("Disconnected")
