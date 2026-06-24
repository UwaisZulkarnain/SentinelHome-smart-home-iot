#include <Arduino.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>
#include "config.h"

DHT dht(DHT_PIN, DHT_TYPE);
WiFiServer server(80);

const char* SUPABASE_URL = "https://ubcyktzfiylqirzpdqnu.supabase.co";
const char* SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViY3lrdHpmaXlscWlyenBkcW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE4MDkxNjQsImV4cCI6MjA5NzM4NTE2NH0.Gu0jBFdVnsBMFF2VWliTnoKtBqCt_-IwSQfnoe2ts9c";

unsigned long lastDHT = 0, lastPIR = 0, lastMQ2 = 0, buzzerStart = 0, lastSupabase = 0;
bool buzzerOn = false, motion = false, gas = false;
float temp = 0, hum = 0;
int nightModeOverride = -1;  // -1 = auto (use real clock), 0 = force day, 1 = force night
unsigned long motionStartTime = 0;
unsigned long motionLastSeenHigh = 0;
unsigned long motionDurationSec = 0;
bool motionActive = false;
int currentClass = 0;
String currentReason = "normal";
bool cachedNight = false;
unsigned long lastNightCheck = 0;
bool supabasePushEnabled = false;

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

  WiFi.begin("Uwais iph", "sarrah123");
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 20) {
    delay(500);
    tries++;
  }
  Serial.print("IP:");
  Serial.println(WiFi.localIP());

  configTime(8 * 3600, 0, "pool.ntp.org", "time.nist.gov");
  Serial.println("Syncing time...");
  struct tm timeinfo;
  int ntpTries = 0;
  while (!getLocalTime(&timeinfo) && ntpTries < 10) {
    delay(500);
    ntpTries++;
  }
  if (getLocalTime(&timeinfo)) {
    Serial.printf("Time synced: %02d:%02d:%02d\n", timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);
  } else {
    Serial.println("NTP sync failed, will retry in background");
  }

  server.begin();

  for (int i = 20; i > 0; i--) {
    Serial.printf("Warmup:%ds\n", i);
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(1000);
  }
  digitalWrite(LED_PIN, HIGH);
  Serial.println("Ready");
}

bool isNight();
void classify();
void pushToSupabase() {
  if (WiFi.status() != WL_CONNECTED) return;
  HTTPClient http;
  String url = String(SUPABASE_URL) + "/rest/v1/sensor_readings";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("apikey", SUPABASE_KEY);
  http.addHeader("Authorization", String("Bearer ") + SUPABASE_KEY);
  http.addHeader("Prefer", "return=minimal");
  String body = "{\"temperature\":" + String(temp, 1) +
                ",\"humidity\":" + String(hum, 1) +
                ",\"motion\":" + String(motion ? 1 : 0) +
                ",\"gas\":" + String(gas ? 1 : 0) +
                ",\"alarm\":" + String(buzzerOn ? 1 : 0) +
                ",\"is_night\":" + String(isNight() ? 1 : 0) +
                ",\"motion_duration_sec\":" + String(motionDurationSec) +
                ",\"alert_class\":" + String(currentClass) +
                ",\"reason\":\"" + currentReason + "\"}";
  int code = http.POST(body);
  Serial.printf("Supabase: %d\n", code);
  http.end();
}

bool isNight() {
  if (nightModeOverride == 1) return true;
  if (nightModeOverride == 0) return false;
  unsigned long now = millis();
  if (now - lastNightCheck >= 3600000UL || lastNightCheck == 0) {
    struct tm timeinfo;
    if (getLocalTime(&timeinfo)) {
      int hour = timeinfo.tm_hour;
      cachedNight = (hour >= 22 || hour < 7);
    }
    lastNightCheck = now;
  }
  return cachedNight;
}

void classify() {
  bool night = isNight();
  int tempClass = 0;
  if (temp >= 40) tempClass = 3;
  else if (temp >= 35) tempClass = 2;
  else if (temp >= 30) tempClass = 1;

  int humClass = 0;
  if (hum >= 80) humClass = 2;
  else if (hum >= 70) humClass = 1;

  int motionClass = 0;
  if (night) {
    if (motionDurationSec >= 15) motionClass = 3;
    else if (motionDurationSec >= 5) motionClass = 2;
    else if (motionDurationSec > 0) motionClass = 1;
  } else {
    if (motionDurationSec >= 60) motionClass = 2;
    else if (motionDurationSec >= 30) motionClass = 1;
  }

  // Priority waterfall
  if (gas && night && motionClass == 3) { currentClass = 3; currentReason = "gas_and_intrusion"; }
  else if (gas && temp >= 35) { currentClass = 3; currentReason = "gas_and_hot"; }
  else if (gas) { currentClass = 3; currentReason = "gas_only"; }
  else if (temp >= 40) { currentClass = 3; currentReason = "extreme_heat"; }
  else if (night && motionClass == 3) { currentClass = 3; currentReason = "night_intrusion"; }
  else if (tempClass == 2 && humClass == 2) { currentClass = 2; currentReason = "hot_humid"; }
  else if (tempClass == 2) { currentClass = 2; currentReason = "hot"; }
  else if (humClass == 2) { currentClass = 2; currentReason = "critical_humidity"; }
  else if (night && motionClass == 2) { currentClass = 2; currentReason = "night_sustained_motion"; }
  else if (!night && motionClass == 2) { currentClass = 2; currentReason = "day_unusual_motion"; }
  else if (tempClass == 1 && humClass == 1) { currentClass = 1; currentReason = "warm_humid"; }
  else if (tempClass == 1) { currentClass = 1; currentReason = "warm"; }
  else if (humClass == 1) { currentClass = 1; currentReason = "humid"; }
  else if (night && motionClass == 1) { currentClass = 1; currentReason = "night_brief_motion"; }
  else if (!night && motionClass == 1) { currentClass = 1; currentReason = "day_lingering_motion"; }
  else { currentClass = 0; currentReason = "normal"; }
}

void loop() {
  unsigned long now = millis();

  if (now - lastDHT >= 2000) {
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t) && !isnan(h)) { 
      temp = t; hum = h;
      Serial.printf("T:%.1f H:%.1f M:%d G:%d A:%d N:%d DUR:%lu CLASS:%d REASON:%s\n",
        temp, hum, motion?1:0, gas?1:0, buzzerOn?1:0, isNight()?1:0, motionDurationSec, currentClass, currentReason.c_str());
    }
    lastDHT = now;
  }

  if (now - lastPIR >= 500) {
    bool rawMotion = digitalRead(PIR_PIN) == HIGH;
    if (rawMotion) {
      motionLastSeenHigh = now;
      if (!motionActive) {
        motionActive = true;
        motionStartTime = now;
      }
      motionDurationSec = (now - motionStartTime) / 1000;
    } else {
      // debounce: only clear if LOW for 2+ continuous seconds
      if (motionActive && (now - motionLastSeenHigh >= 2000)) {
        motionActive = false;
        motionDurationSec = 0;
      }
    }
    motion = motionActive;
    lastPIR = now;
  }
  if (now - lastMQ2 >= 1000) {
    gas = digitalRead(MQ2_PIN) == LOW;
    lastMQ2 = now;
  }

  classify();

  if (now - lastSupabase >= 2000 && supabasePushEnabled) {
    pushToSupabase();
    lastSupabase = now;
  }

  if (currentClass >= 2 && !buzzerOn) {
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
    if (req.indexOf("/supabase?on=1") != -1) {
      supabasePushEnabled = true;
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.println("{\"supabasePush\":\"enabled\"}");
      client.stop();
      return;
    }
    if (req.indexOf("/supabase?on=0") != -1) {
      supabasePushEnabled = false;
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.println("{\"supabasePush\":\"disabled\"}");
      client.stop();
      return;
    }
    if (req.indexOf("/night?on=1") != -1) {
      nightModeOverride = 1;
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.println("{\"nightMode\":\"forced_on\"}");
      client.stop();
      return;
    }
    if (req.indexOf("/night?on=0") != -1) {
      nightModeOverride = 0;
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.println("{\"nightMode\":\"forced_off\"}");
      client.stop();
      return;
    }
    if (req.indexOf("/night?auto=1") != -1) {
      nightModeOverride = -1;
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.println("{\"nightMode\":\"auto\"}");
      client.stop();
      return;
    }
    if (req.indexOf("/data") != -1) {
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.printf("{\"t\":%.1f,\"h\":%.1f,\"m\":%d,\"g\":%d,\"a\":%d,\"n\":%d,\"dur\":%lu,\"class\":%d,\"reason\":\"%s\",\"push\":%d}\n",
        temp, hum, motion?1:0, gas?1:0, buzzerOn?1:0, isNight()?1:0, motionDurationSec, currentClass, currentReason.c_str(), supabasePushEnabled?1:0);
    }
    client.stop();
  }
  delay(10);
}