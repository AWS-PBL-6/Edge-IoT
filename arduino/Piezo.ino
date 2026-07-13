#define SENSOR_PIN A1
#define LED_PIN 13

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int value = analogRead(SENSOR_PIN);

  Serial.println(value);

  if (value > 500) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  delay(50);
}