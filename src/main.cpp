#include <Arduino.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>
#include "config.h"
#include "model.h"

bool isNight();
void runML();

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
bool pushError = false;
int ml_class_result = 0;
float ml_confidence_result = 0.0;

const float SCALER_MEAN[4]  = {29.737f, 60.312f, 0.0f, 1.249f};
const float SCALER_SCALE[4] = {5.241f, 10.707f, 1.0f, 2.012f};

void runML() {
  // Scale continuous features using StandardScaler constants
  float t_scaled   = (temp - 29.737f) / 5.241f;
  float h_scaled   = (hum  - 60.312f) / 10.707f;
  float g_scaled   = ((gas ? 1.0f : 0.0f) - 0.0f) / 1.0f;
  float dur_scaled = ((float)motionDurationSec - 1.249f) / 2.012f;

  // emlearn expects int16_t features scaled by 100
  // Feature order: [temp, hum, motion, gas, is_night, dur]
  int16_t features[6] = {
    (int16_t)(t_scaled   * 100),
    (int16_t)(h_scaled   * 100),
    (int16_t)(motion ? 1 : 0),
    (int16_t)(g_scaled   * 100),
    (int16_t)(isNight() ? 1 : 0),
    (int16_t)(dur_scaled * 100)
  };

  // Get predicted class
  ml_class_result = model_predict(features, 6);

  // Get confidence via vote proportions
  float proba[4] = {0.0f, 0.0f, 0.0f, 0.0f};
  model_predict_proba(features, 6, proba, 4);
  ml_confidence_result = proba[ml_class_result];
}

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT_PULLUP);
  pinMode(MQ2_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(DHT_PIN, INPUT_PULLUP);
  digitalWrite(BUZZER_PIN, LOW);
  pinMode(STATUS_LED_PIN, OUTPUT);
  digitalWrite(STATUS_LED_PIN, LOW);  // start OFF
  pinMode(SUPABASE_JUMPER_PIN, INPUT_PULLUP);
  pinMode(NIGHT_JUMPER_PIN, INPUT_PULLUP);
  dht.begin();

  // Read jumper state to set Supabase push default
  if (digitalRead(SUPABASE_JUMPER_PIN) == LOW) {
    supabasePushEnabled = true;
  } else {
    supabasePushEnabled = false;
  }

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
    delay(1000);
  }
  Serial.println("Ready");
}

void classify();
void pushToSupabase() {
  if (WiFi.status() != WL_CONNECTED) {
    pushError = true;
    return;
  }
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
                 ",\"reason\":\"" + currentReason + "\"" +
                 ",\"ml_class\":" + String(ml_class_result) +
                 ",\"ml_confidence\":" + String(ml_confidence_result, 3) + "}";
  int code = http.POST(body);
  if (code == 201 || code == 200) {
    pushError = false;
    digitalWrite(STATUS_LED_PIN, HIGH);  // solid ON: success
  } else {
    pushError = true;
  }
  Serial.printf("Supabase: %d\n", code);
  http.end();
}

bool isNight() {
  if (nightModeOverride == 1) return true;
  if (nightModeOverride == 0) return false;
  // auto mode — use NTP
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

  // Hot-swap: check jumper state and update push enable in real time
  static bool lastJumperState = !supabasePushEnabled;
  bool jumperState = (digitalRead(SUPABASE_JUMPER_PIN) == LOW);
  if (jumperState != lastJumperState) {
    supabasePushEnabled = jumperState;
    lastJumperState = jumperState;
  }

  // Status LED: OFF when push disabled
  if (!supabasePushEnabled) {

    pushError = false;
    digitalWrite(STATUS_LED_PIN, LOW);
  }

  // Status LED: blink 1Hz when push error (WiFi down or HTTP error)
  if (supabasePushEnabled && pushError) {
    digitalWrite(STATUS_LED_PIN, (millis() / 500) % 2);
  }
  // Night mode physical jumper — D2/GPIO3 to GND = force night, floating = auto
  if (digitalRead(NIGHT_JUMPER_PIN) == LOW) {
    nightModeOverride = 1;  // jumper in = force night
} else {
    nightModeOverride = 0;  // jumper out = force day
}

  if (now - lastDHT >= 2000) {
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t) && !isnan(h)) { 
      temp = t; hum = h;
      Serial.printf("T:%.1f H:%.1f M:%d G:%d A:%d N:%d DUR:%lu CLASS:%d REASON:%s ML:%d CONF:%.3f\n",
        temp, hum, motion?1:0, gas?1:0, buzzerOn?1:0, isNight()?1:0, motionDurationSec, currentClass, currentReason.c_str(), ml_class_result, ml_confidence_result);
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
    int aoVal = analogRead(MQ2_PIN);
    gas = (aoVal > 3200);
    Serial.printf("MQ2_AO:%d GAS:%d\n", aoVal, gas?1:0);
    lastMQ2 = now;
}

  classify();
  runML();

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
      client.printf("{\"t\":%.1f,\"h\":%.1f,\"m\":%d,\"g\":%d,\"a\":%d,\"n\":%d,\"dur\":%lu,\"class\":%d,\"reason\":\"%s\",\"push\":%d,\"ml_class\":%d,\"ml_conf\":%.3f}\n",
        temp, hum, motion?1:0, gas?1:0, buzzerOn?1:0, isNight()?1:0, motionDurationSec, currentClass, currentReason.c_str(), supabasePushEnabled?1:0, ml_class_result, ml_confidence_result);
    }
    client.stop();
  }
  delay(10);
}