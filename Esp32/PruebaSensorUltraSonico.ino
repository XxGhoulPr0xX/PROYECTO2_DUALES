#include <NewPing.h>

#define TRIG_PIN 1
#define ECHO_PIN 2
#define MAX_DISTANCE 200  // Distancia máxima a medir (en cm)

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
    Serial.begin(9600);
    Serial.println("Iniciando prueba del sensor ultrasónico");
    Serial.println("Mostrando lecturas de distancia...");
}

void loop() {
    static unsigned long ultimo_tiempo = 0;
    const unsigned intervalo = 500;  // Intervalo entre lecturas (ms)
    
    if (millis() - ultimo_tiempo >= intervalo) {
        ultimo_tiempo = millis();
        
        // Obtener distancia en centímetros
        unsigned int distancia = sonar.ping_cm();
        
        // Mostrar resultado
        if (distancia == 0) {
            Serial.println("Fuera de rango");
        } else {
            Serial.print("Distancia: ");
            Serial.print(distancia);
            Serial.println(" cm");
        }
    }
}