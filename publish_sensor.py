import json
import time
from datetime import datetime, timezone

import serial
from awscrt import mqtt
from awsiot import mqtt_connection_builder


SERIAL_PORT = "COM8"
SERIAL_BAUD = 9600

AWS_IOT_ENDPOINT = "a1ufy9lg12m67z-ats.iot.ap-northeast-2.amazonaws.com"
CLIENT_ID = "factorypulse_gateway_01"

PATH_TO_CERT = "certs/device.pem.crt"
PATH_TO_KEY = "certs/private.pem.key"
PATH_TO_ROOT_CA = "certs/AmazonRootCA1.pem"

TOPIC = "factorypulse/sensor/uno_01"

import os

print("ENDPOINT:", AWS_IOT_ENDPOINT)
print("CLIENT_ID:", CLIENT_ID)
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
        # 1200,532
        if "," not in line:
            print("Skip:", line)
            continue

        parts = line.split(",")

        if len(parts) != 2:
            print("Invalid:", line)
            continue

        try:
            time_ms = int(parts[0])
            ae_value = int(parts[1])
        except ValueError:
            print("Header or invalid line:", line)
            continue

        payload = {
            "device_id": "uno_01",
            "machine_id": "MOTOR_01",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "time_ms": time_ms,
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

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    ser.close()
    mqtt_connection.disconnect().result()
    print("Disconnected.")