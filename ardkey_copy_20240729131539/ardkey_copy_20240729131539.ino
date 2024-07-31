#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Replace with your network credentials
const char* ssid = "Qwertyuiop";
const char* password = "abcde12345";

// Create an instance of the ESP8266WebServer on port 80
ESP8266WebServer server(80);

// Define the pin for the LED
const int ledPin = 12;  // GPIO5 (D1)

void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP8266 Web Server</h1>";
  html += "<p>Click the buttons to control the LED:</p>";
  html += "<a href=\"/led/on\"><button>Turn LED ON</button></a>";
  html += "<a href=\"/led/off\"><button>Turn LED OFF</button></a>";
  html += "<p>Current LED status: ";
  if (digitalRead(ledPin) == LOW) {
    html += "ON";
  } else {
    html += "OFF";
  }
  html += "</p></body></html>";

  server.send(200, "text/html", html);
}

void handleNotFound() {
  server.send(404, "text/plain", "404: Not Found");
}

void handleLEDOn() {
  digitalWrite(ledPin, LOW); // Turn the LED on (LOW is the voltage level)
  server.sendHeader("Location", "/", true); // Redirect to root URL
  server.send(303); // HTTP 303 See Other
}

void handleLEDOff() {
  digitalWrite(ledPin, HIGH); // Turn the LED off (HIGH is the voltage level)
  server.sendHeader("Location", "/", true); // Redirect to root URL
  server.send(303); // HTTP 303 See Other
}

void setup() {
  // Start the Serial communication to send messages to the computer
  Serial.begin(115200);
  delay(10);

  // Initialize the LED pin as an output
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); // Turn the LED off by default

  // Connect to Wi-Fi network
  Serial.println();
  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Define URL handlers
  server.on("/", handleRoot);
  server.on("/led/on", HTTP_GET, handleLEDOn);
  server.on("/led/off", HTTP_GET, handleLEDOff);
  server.onNotFound(handleNotFound);

  // Start the web server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  // Handle client requests
  server.handleClient();
}