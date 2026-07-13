import json
import random
import time
from datetime import datetime, timezone

from awscrt import mqtt
from awsiot import mqtt_connection_builder


AWS_IOT_ENDPOINT = "a1ufy9lg12m67z-ats.iot.ap-northeast-2.amazonaws.com"
CLIENT_ID = "factorypulse_gateway_01"

PATH_TO_CERT = "certs/device.pem.crt"
PATH_TO_KEY = "certs/private.pem.key"
PATH_TO_ROOT_CA = "certs/AmazonRootCA1.pem"

TOPIC = "factorypulse/sensor/uno_01"


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
        ae_value = random.randint(0, 1023)

        payload = {
            "device_id": "uno_01",
            "machine_id": "MOTOR_01",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ae_value": ae_value,
            "peak_value": ae_value,
            "event_count": 1 if ae_value > 700 else 0
        }

        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(payload),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )[0].result()

        print("Published:", payload)
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped")

finally:
    mqtt_connection.disconnect().result()
    print("Disconnected")