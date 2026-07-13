#include <SoftwareSerial.h>

#define SENSOR_PIN A1
#define LED_PIN 13

// HC-06 연결
// HC-06 TXD → Arduino D10
// HC-06 RXD ← Arduino D11
SoftwareSerial BTSerial(10, 11);

#define THRESHOLD_HIGH 550
#define THRESHOLD_LOW 450
#define WINDOW_MS 1000UL

void setup() {
  Serial.begin(115200);   // USB 디버깅용
  BTSerial.begin(9600);   // HC-06 기본 속도

  pinMode(LED_PIN, OUTPUT);

  Serial.println("freqHz");
  BTSerial.println("freqHz");
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

  // USB로 출력
  Serial.println(freqHz, 1);

  // HC-06 블루투스로 출력
  BTSerial.println(freqHz, 1);
}