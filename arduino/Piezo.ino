#define SENSOR_PIN A1
#define LED_PIN 13

// 임계값(히스테리시스): 상승 교차 횟수로 주파수를 계산한다
#define THRESHOLD_HIGH 550
#define THRESHOLD_LOW 450

// 측정 창(ms) — 창마다 freqHz 한 줄을 출력한다
#define WINDOW_MS 1000UL

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  unsigned long windowStart = millis();
  unsigned int crossings = 0;
  bool above = false;

  while (millis() - windowStart < WINDOW_MS) {
    int value = analogRead(SENSOR_PIN);

    if (!above && value > THRESHOLD_HIGH) {
      above = true;
      crossings++;
      digitalWrite(LED_PIN, HIGH);
    } else if (above && value < THRESHOLD_LOW) {
      above = false;
      digitalWrite(LED_PIN, LOW);
    }
  }

  float freqHz = crossings * 1000.0 / WINDOW_MS;

  // 게이트웨이(publish_sensor.py)가 이 값을 freqHz로 읽는다
  Serial.println(freqHz, 1);
}
