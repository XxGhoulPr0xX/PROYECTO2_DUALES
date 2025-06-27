#include <ESP32Servo.h>

#define SERVO_PIN 13

Servo servoMotor;

const byte angulos[2] = {0, 180};
const char comandos[2] = {'b', 'n'};
const int velocidad = 20;


void setup() {
    Serial.begin(9600);
    servoMotor.attach(SERVO_PIN);  
    servoMotor.write(90);
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

void loop() {
    if (Serial.available() > 0) {
        byte entrada = Serial.read();
        entrada = tolower(entrada);
        for (int i = 0; i < 2; i++) {
            if (entrada == comandos[i]) {
                Serial.print("Moviendo suavemente a ");
                Serial.print(angulos[i]);
                Serial.println("°");     
                moverYVolverSuave(angulos[i]);
                break;
            }
        }
    }
    delay(100);
}