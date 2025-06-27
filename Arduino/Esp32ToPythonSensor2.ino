#include <ESP32Servo.h>

#define SERVO_PIN 13
#define SENSOR_IR_PIN 4

Servo servoMotor;

const byte angulos[2] = {50, 130};
const char comandos[2] = {'B','N'};
const int velocidad = 10;

void setup() {
    Serial.begin(9600);
    servoMotor.attach(SERVO_PIN);
    servoMotor.write(90);
    pinMode(SENSOR_IR_PIN, INPUT);
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
    delay(1000);
    moverServoSuave(90);
}

void procesarComando(byte cmd) {
    for (int i = 0; i < 2; i++) {
        if (cmd == comandos[i] || cmd == tolower(comandos[i])) {
            Serial.println("recibido");
            moverYVolverSuave(angulos[i]);
            return;
        }
    }
    Serial.println("comando_invalido");
}

void loop() {
    static unsigned long ultima_deteccion = 0;
    unsigned long tiempo_actual = millis();
    bool objetoInfrarrojo = (digitalRead(SENSOR_IR_PIN) == LOW);

    if (objetoInfrarrojo && (tiempo_actual - ultima_deteccion > 3000)) {
        ultima_deteccion = tiempo_actual;
        Serial.println("objeto detectado");
        unsigned long inicio_espera = tiempo_actual;
        while ((millis() - inicio_espera) < 2000) {
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