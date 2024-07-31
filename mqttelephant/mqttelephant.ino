#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Wi-Fi network credentials
const char* ssid = "Qwertyuiop";        // Replace with your WiFi SSID
const char* password = "abcde12345";    // Replace with your WiFi password

// Define GPIO pins using integer values
const int D1_PIN = 5;  // GPIO5(red:elephant(danger))
const int D2_PIN = 4;  // GPIO4(blue:monkey,parrot , peacock.......)
const int D3_PIN = 0;  // GPIO0(green:human)

// MQTT broker details
const char* mqtt_broker = "test.mosquitto.org";
const int mqtt_port = 1883;
const char* mqtt_topic = "agri9urd/user1/sensor1/dettype";

// Create WiFi and MQTT client objects
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  // Start the Serial Monitor
  Serial.begin(115200);

    // Initialize GPIO pins
  pinMode(D1_PIN, OUTPUT);
  pinMode(D2_PIN, OUTPUT);
  pinMode(D3_PIN, OUTPUT);
  digitalWrite(D1_PIN, LOW);
  digitalWrite(D2_PIN, LOW);
  digitalWrite(D3_PIN, LOW);

  // Connect to the Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());

  // Configure the MQTT client
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  // Connect to the MQTT broker
  reconnect();
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
    // Print the received message
  Serial.println(message);
  Serial.println();
  

    // Control GPIO pins based on the message
  if (message == "{'elephant'}") {
    digitalWrite(D1_PIN, HIGH);
    delay(10000); // Keep the pin high for 10 seconds
    digitalWrite(D1_PIN, LOW);
  } else if (message == "human") {
    digitalWrite(D2_PIN, HIGH);
    delay(10000); // Keep the pin high for 10 seconds
    digitalWrite(D2_PIN, LOW);
  } else if (message == "monkey" || message == "parrot"){
    digitalWrite(D3_PIN, HIGH);
    delay(10000); // Keep the pin high for 10 seconds
    digitalWrite(D3_PIN, LOW);
  }else {
    // Do nothing for other values
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a unique client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Subscribe to the topic
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
