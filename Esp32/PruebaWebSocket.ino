#include <WiFi.h>
#include <WebSocketsClient.h>

const char* ssid = "IZZI-FA5D";
const char* password = "QJY5MDZYWMLD";
const char* websocket_server_host = "192.168.0.121";
const uint16_t websocket_server_port = 8765;

WebSocketsClient webSocket;
bool initialMessageSent = false;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch (type) {
    case WStype_DISCONNECTED:
        Serial.printf("[WSc] Desconectado!\n");
        initialMessageSent = false; // Resetear la bandera para enviar de nuevo al reconectar
        break;
    case WStype_CONNECTED:
        Serial.printf("[WSc] Conectado a url: %s\n", payload);
        break;
    case WStype_TEXT:
        Serial.printf("[WSc] Mensaje recibido: %s\n", payload);
        webSocket.sendTXT("Bien python, haciendo de cliente");
        Serial.println("Confirmacion de recibido enviada.");
        break;
    default:
        break;
    }
}

void setup() {
    Serial.begin(115200);

    Serial.printf("Conectando a %s\n", ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi conectado.");
    Serial.print("Dirección IP: ");
    Serial.println(WiFi.localIP());

    webSocket.begin(websocket_server_host, websocket_server_port, "/");
    webSocket.onEvent(webSocketEvent);
    webSocket.setReconnectInterval(5000);
}

void loop() {
    webSocket.loop();

  // Enviar el mensaje inicial solo si está conectado y no se ha enviado
    if (webSocket.isConnected() && !initialMessageSent) {
        webSocket.sendTXT("ESP32: Hola desde ESP32");
        Serial.println("Mensaje inicial enviado al servidor.");
        initialMessageSent = true;
    }
}