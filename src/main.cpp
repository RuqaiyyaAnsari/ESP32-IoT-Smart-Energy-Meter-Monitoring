#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>
#include "readings.h"   // src folder mein hona chahiye

// ===== Wokwi settings =====
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";
const char* MQTT_HOST = "10.106.199.110";
const int   MQTT_PORT = 1883;
const char* METER_ID  = "K2-MTR-0001";
// Public broker hai, isliye unique naam rakho
const char* CLIENT_ID = "k2demo-ruqaiyya-mtr0001";
const char* TOPIC_PREFIX = "k2demo/ruqaiyya/meters/";
// ==========================

const unsigned long INTERVAL_MS = 5000;   // har 5 sec mein 1 reading

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
int idx = 0;
unsigned long seq = 0;
unsigned long lastSend = 0;

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("WiFi connecting to: ");
  Serial.println(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());
}

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("MQTT connecting...");
    if (mqtt.connect(CLIENT_ID)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.println(mqtt.state());
      delay(2000);
    }
  }
}

String isoTimeUTC() {
  time_t now = time(nullptr);
  struct tm t;
  gmtime_r(&now, &t);
  char buf[25];
  strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%SZ", &t);
  return String(buf);
}

void setup() {
  Serial.begin(115200);
  connectWiFi();

  configTime(0, 0, "pool.ntp.org");
  Serial.print("Time sync");
  int t = 0;
  while (time(nullptr) < 100000 && t < 40) {   // max ~8 sec wait
    delay(200);
    Serial.print(".");
    t++;
  }
  Serial.println(" done");

  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setBufferSize(512);
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  if (millis() - lastSend >= INTERVAL_MS) {
    lastSend = millis();

    JsonDocument doc;
    doc["meter_id"] = METER_ID;
    doc["ts"]       = isoTimeUTC();
    doc["seq"]      = seq++;
    doc["kwh"]      = KWH[idx];
    doc["voltage"]  = VOLT[idx];
    doc["current"]  = CURR[idx];

    char payload[256];
    serializeJson(doc, payload);

    String topic = String(TOPIC_PREFIX) + METER_ID + "/readings";
    bool ok = mqtt.publish(topic.c_str(), payload);
    Serial.println(String(ok ? "SENT " : "FAIL ") + topic + " -> " + payload);

    idx = (idx + 1) % N_READINGS;
  }
}