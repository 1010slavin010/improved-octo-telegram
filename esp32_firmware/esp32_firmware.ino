/* AgroSentry / KisanSense ESP32 sensor node
   Sensors: analog soil moisture + LDR
   Optional DHT11 can be added later.
*/
#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

IPAddress local_IP(192, 168, 31, 57);
IPAddress gateway(192, 168, 31, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);

const char* serverUrl = "http://YOUR_PC_IP:8000/api/telemetry";
#define SOIL_PIN 34
#define LIGHT_PIN 35

WebServer server(80);
float soilMoisturePercent = 0;
float lightLux = 0;
float temperatureC = 25.0;
float humidityPercent = 60.0;
unsigned long lastPostTime = 0;
const unsigned long postInterval = 3000;

void readSensors() {
  int rawSoil = analogRead(SOIL_PIN);
  soilMoisturePercent = map(rawSoil, 3200, 1400, 0, 100);
  soilMoisturePercent = constrain(soilMoisturePercent, 0.0, 100.0);

  int rawLight = analogRead(LIGHT_PIN);
  lightLux = map(rawLight, 0, 4095, 100, 75000);
}

String sensorJson() {
  readSensors();
  String json = "{";
  json += "\"soil_moisture\":" + String(soilMoisturePercent, 1) + ",";
  json += "\"light_lux\":" + String(lightLux, 0) + ",";
  json += "\"temperature\":" + String(temperatureC, 1) + ",";
  json += "\"humidity\":" + String(humidityPercent, 1);
  json += "}";
  return json;
}

void handleData() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", sensorJson());
}

void sendDataToServer() {
  if (WiFi.status() != WL_CONNECTED) return;
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int code = http.POST(sensorJson());
  Serial.printf("Telemetry POST: %d\n", code);
  http.end();
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  WiFi.config(local_IP, gateway, subnet, primaryDNS);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
  server.on("/data", HTTP_GET, handleData);
  server.begin();
}

void loop() {
  server.handleClient();
  if (millis() - lastPostTime > postInterval) {
    lastPostTime = millis();
    sendDataToServer();
  }
}
