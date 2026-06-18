#ifndef CONFIG_H
#define CONFIG_H

#include <DHT.h>

// === SENSOR PINS ===
#define PIR_PIN      2
#define MQ2_PIN      5
#define DHT_PIN      9
#define LED_PIN      6
#define BUZZER_PIN   7

// === SENSOR CONFIG ===
#define DHT_TYPE     DHT11  
#define MQ2_WARMUP_MS 20000  // MQ-2 gas sensor modules need approximately 20-30 seconds of warmup before stable readings.
#define PIR_DELAY_MS  2000   // Delay between PIR trigger checks to avoid repeated alarms.
#define MOTION_ALARM_ENABLED 1  // Set to 1 to trigger buzzer on PIR motion, or 0 to monitor motion only.

// === THRESHOLDS ===
#define GAS_THRESHOLD_HIGH 1       // MQ-2 DO pin convention: HIGH = no gas, LOW = gas detected.
#define TEMP_THRESHOLD_HIGH 35.0   // °C - trigger alarm above this temperature.
#define HUM_THRESHOLD_HIGH  80.0   // % - trigger alarm above this humidity.

#endif