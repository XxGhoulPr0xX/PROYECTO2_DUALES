#include <NewPing.h>
#include <ESP32Servo.h>

#define TRIG_PIN 1
#define ECHO_PIN 2
#define MAX_DISTANCE 20
#define SERVO_PIN 13

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
Servo servoMotor;

const byte angulos[2] = {90, 180};
const char comandos[2] = {'B','N'};

void setup() {
    Serial.begin(9600);
    servoMotor.attach(SERVO_PIN);
    servoMotor.write(0);
}
void procesarComando(byte cmd) {
    for (int i = 0; i < 2; i++) {
        if (cmd == comandos[i] || cmd == tolower(comandos[i])) {
            servoMotor.write(angulos[i]);
            moverMotorAdelante(motorComandos[i]);
            delay(500); // Pequeña pausa antes de resetear servo
            servoMotor.write(0);
            Serial.println("recibido");  // Confirmación
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
            delay(50); // Pequeña pausa para no saturar
        }
    }
    delay(100);
}