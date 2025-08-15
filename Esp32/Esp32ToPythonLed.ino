//CS	15 (Chip Select)
//RST	4 
//DC	2 (Data/Command)
//MOSI	13
//SCLK	14
//LED	21 (Backlight)
//MISO	12
//TRIG 1
//ECHO 3
//SERVO 12
#include <NewPing.h>
#include <ESP32Servo.h>
#include <TFT_eSPI.h>

#define TRIG_PIN 1
#define ECHO_PIN 3
#define SERVO_PIN 12
#define MAX_DISTANCE 10 

TFT_eSPI tft = TFT_eSPI();
NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
Servo servoMotor;

const byte angulos[2] = {0, 180};
const char comandos[2] = {'B','N'};
const int velocidad = 10;

void setup() {
    Serial.begin(9600);
    servoMotor.attach(SERVO_PIN);
    servoMotor.write(90);
    
    // Inicialización de la pantalla TFT
    tft.init();
    tft.setRotation(1);
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextSize(2);
}

void mostrarMensajeTemporal(String mensaje) {
    tft.fillScreen(TFT_BLACK);  // Limpiar pantalla
    tft.drawString(mensaje, 50, 120);  // Mostrar mensaje
    delay(5000);  // Esperar 5 segundos
    tft.fillScreen(TFT_BLACK);  // Borrar mensaje
}

void moverServoSuave(int anguloObjetivo) {
    int posicionActual = servoMotor.read();
    int incremento = (anguloObjetivo > posicionActual) ? 1 : -1;
    
    while (posicionActual != anguloObjetivo) {
        posicionActual += incremento;
        if ((incremento == 1 && posicionActual > anguloObjetivo) || 
            (incremento == -1 && posicionActual < anguloObjetivo)) {
            posicionActual = anguloObjetivo;
        }
        servoMotor.write(posicionActual);
        delay(velocidad);
    }
}

void moverYVolverSuave(int anguloObjetivo) {
    moverServoSuave(anguloObjetivo);
    delay(500);
    moverServoSuave(90);
}

void procesarComando(byte cmd) {
    for (int i = 0; i < 2; i++) {
        if (cmd == comandos[i] || cmd == tolower(comandos[i])) {
            Serial.println("recibido");
            moverYVolverSuave(angulos[i]);
            if (cmd == 'B') {
                mostrarMensajeTemporal("Basura Biodegradable detectada");
            } else {
                mostrarMensajeTemporal("Basura No-Biodegradable detectada");
            }
            return;
        }
    }
    Serial.println("comando_invalido");
}

void loop() {
    static unsigned long ultima_deteccion = 0;
    unsigned long tiempo_actual = millis();
    int distancia = sonar.ping_cm();
    
    if (distancia > 0 && distancia < 10 && tiempo_actual - ultima_deteccion > 3000) {
        ultima_deteccion = tiempo_actual;
        Serial.println("objeto detectado");
        unsigned long inicio_espera = tiempo_actual;
        
        while (millis() - inicio_espera < 2000) {
            if (Serial.available() > 0) {
                byte entrada = Serial.read();
                procesarComando(entrada);
                break;
            }
            delay(50);
        }
    }
    delay(100);
}