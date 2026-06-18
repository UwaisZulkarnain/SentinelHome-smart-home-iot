#include <Arduino.h>
#include <DHT.h>
#include <WiFi.h>
#include "config.h"

#include <WiFiManager.h>

DHT dht(DHT_PIN, DHT_TYPE);
WiFiServer server(80);

unsigned long lastDHT = 0, lastPIR = 0, lastMQ2 = 0, buzzerStart = 0;
bool buzzerOn = false, motion = false, gas = false;
float temp = 0, hum = 0;

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(MQ2_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(DHT_PIN, INPUT_PULLUP);
  digitalWrite(LED_PIN, HIGH);
  digitalWrite(BUZZER_PIN, LOW);
  dht.begin();

  WiFiManager wm;
  wm.setConfigPortalTimeout(180);
  if (!wm.autoConnect("XIAO-SmartHome")) {
    ESP.restart();
  }
  Serial.println();
  Serial.print("IP:");
  Serial.println(WiFi.localIP());

  server.begin();

  for (int i = 20; i > 0; i--) {
    Serial.printf("Warmup:%ds\n", i);
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(1000);
  }
  digitalWrite(LED_PIN, HIGH);
  Serial.println("Ready");
}

void loop() {
  unsigned long now = millis();

  if (now - lastDHT >= 2000) {
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t) && !isnan(h)) { temp = t; hum = h; }
    lastDHT = now;
  }

  if (now - lastPIR >= 500) {
    motion = digitalRead(PIR_PIN) == HIGH;
    lastPIR = now;
  }

  if (now - lastMQ2 >= 1000) {
    gas = digitalRead(MQ2_PIN) == LOW;
    lastMQ2 = now;
  }

  if ((gas || temp > 35 || hum > 80 || motion) && !buzzerOn) {
    buzzerOn = true; buzzerStart = now;
    digitalWrite(BUZZER_PIN, HIGH);
  }
  if (buzzerOn && now - buzzerStart >= 3000) {
    buzzerOn = false;
    digitalWrite(BUZZER_PIN, LOW);
  }

  digitalWrite(LED_PIN, (buzzerOn || gas) ? ((now/250)%2) : HIGH);

  WiFiClient client = server.available();
  if (client) {
    String req = client.readStringUntil('\r');
    if (req.indexOf("/data") != -1) {
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.printf("{\"t\":%.1f,\"h\":%.1f,\"m\":%d,\"g\":%d,\"a\":%d}\n",
        temp, hum, motion?1:0, gas?1:0, buzzerOn?1:0);
    }
    client.stop();
  }
  delay(10);
}