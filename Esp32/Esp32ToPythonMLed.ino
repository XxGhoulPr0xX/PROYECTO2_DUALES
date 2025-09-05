#include <Adafruit_GFX.h>       // Librería para gráficos, necesaria para la pantalla OLED
#include <Adafruit_SSD1306.h>   // Librería para el controlador de pantalla SSD1306 (OLED)
#include <Wire.h>               // Librería para la comunicación I2C (necesaria para el OLED)
#include <NewPing.h>            // Librería para el sensor ultrasónico
#include <ESP32Servo.h>         // Librería para el control del servomotor en ESP32

// --- Definiciones de hardware y pines ---

// Dimensiones de la pantalla OLED
#define SCREEN_WIDTH 128    // Ancho de la pantalla en píxeles
#define SCREEN_HEIGHT 64    // Alto de la pantalla en píxeles
#define OLED_RESET -1       // Pin de reset (se usa -1 para ESP32, ya que no es un pin físico)

// Pines para la comunicación I2C con la pantalla OLED
#define I2C_SDA_PIN 8
#define I2C_SCL_PIN 9

// Pines para el sensor ultrasónico y el servomotor
#define TRIG_PIN 1          // Pin del Trigger del sensor ultrasónico
#define ECHO_PIN 3          // Pin del Echo del sensor ultrasónico
#define SERVO_PIN 12        // Pin de control para el servomotor
#define MAX_DISTANCE 10     // Distancia máxima en cm para detectar un objeto

// --- Creación de objetos ---

// Objeto para controlar la pantalla OLED
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
// Objeto para el sensor ultrasónico, con sus pines y distancia máxima
NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
// Objeto para controlar el servomotor
Servo servoMotor;

// --- Constantes del sistema ---

// Ángulos de los movimientos del servo para cada tipo de basura (ej. 0° y 180°)
const byte angulos[2] = {0, 180};
// Comandos seriales esperados para clasificar ('B' para Biodegradable, 'N' para No-biodegradable)
const char comandos[2] = {'B','N'};
// Velocidad del movimiento del servo (menor valor = más rápido)
const int velocidad = 10;

// --- Funciones del sistema ---

/**
 * @brief Muestra un mensaje temporal en la pantalla OLED por 5 segundos.
 * @param mensaje El texto que se mostrará en la pantalla.
 */
void mostrarMensajeTemporal(String mensaje) {
    display.clearDisplay();     // Borra todo el contenido anterior
    display.setCursor(0, 0);    // Coloca el cursor en la esquina superior izquierda
    display.println(mensaje);   // Muestra el mensaje
    display.display();          // Actualiza la pantalla física para que el mensaje sea visible
    delay(5000);                // Espera 5 segundos
    display.clearDisplay();     // Borra la pantalla al terminar el tiempo
    display.display();          // Actualiza la pantalla para que quede en blanco
}

/**
 * @brief Mueve el servomotor de forma suave hacia un ángulo objetivo.
 * @param anguloObjetivo El ángulo al que se desea mover el servo.
 */
void moverServoSuave(int anguloObjetivo) {
    int posicionActual = servoMotor.read();
    // Determina la dirección del movimiento (incremento o decremento)
    int incremento = (anguloObjetivo > posicionActual) ? 1 : -1;
    
    // Bucle para mover el servo paso a paso
    while (posicionActual != anguloObjetivo) {
        posicionActual += incremento;
        // Asegura que el servo no se pase del ángulo objetivo
        if ((incremento == 1 && posicionActual > anguloObjetivo) || 
            (incremento == -1 && posicionActual < anguloObjetivo)) {
            posicionActual = anguloObjetivo;
        }
        servoMotor.write(posicionActual); // Envía el comando de movimiento
        delay(velocidad);                 // Pausa breve para lograr un movimiento suave
    }
}

/**
 * @brief Mueve el servo a un ángulo específico y luego lo regresa al centro.
 * @param anguloObjetivo El ángulo al que se desea mover el servo antes de regresar.
 */
void moverYVolverSuave(int anguloObjetivo) {
    moverServoSuave(anguloObjetivo);
    delay(500);         // Espera medio segundo
    moverServoSuave(90);  // Regresa el servo a la posición central (90°)
}

/**
 * @brief Procesa los comandos recibidos por el puerto serial.
 * @param cmd El byte del comando recibido.
 */
void procesarComando(byte cmd) {
    for (int i = 0; i < 2; i++) {
        // Compara el comando recibido con los comandos definidos ('B' o 'N', ignorando mayúsculas/minúsculas)
        if (cmd == comandos[i] || cmd == tolower(comandos[i])) {
            Serial.println("recibido");
            moverYVolverSuave(angulos[i]);
            // Muestra el mensaje correspondiente en la pantalla OLED
            if (cmd == 'B') {
                mostrarMensajeTemporal("Biodegradable\ndetectada");
            } else {
                mostrarMensajeTemporal("No-Biodegradable\ndetectada");
            }
            return; // Sale de la función después de procesar el comando
        }
    }
    Serial.println("comando_invalido"); // Si el comando no coincide, lo notifica por el serial
}

// --- Configuración inicial (se ejecuta una vez) ---

void setup() {
    Serial.begin(9600);           // Inicia la comunicación serial a 9600 baudios

    // Inicializa la comunicación I2C para la pantalla OLED
    Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);

    // Inicializa la pantalla OLED
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Dirección I2C: 0x3C
        Serial.println(F("Error en la inicializacion de la pantalla OLED"));
        for(;;); // Detiene el programa en caso de error
    }

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);

    // Inicializa el servomotor
    servoMotor.attach(SERVO_PIN); // Asocia el objeto servo al pin físico
    servoMotor.write(90);         // Mueve el servo a la posición central inicial

    // Mensaje de inicio en la pantalla
    display.println("Sistema de");
    display.println("Clasificacion");
    display.println("Iniciado");
    display.display();
    delay(2000);
    display.clearDisplay();
    display.display();
}

// --- Bucle principal del programa ---

void loop() {
    // Variables estáticas para controlar el tiempo entre detecciones y evitar lecturas falsas
    static unsigned long ultima_deteccion = 0;
    unsigned long tiempo_actual = millis();
    int distancia = sonar.ping_cm(); // Obtiene la distancia en centímetros
    
    // Si se detecta un objeto dentro del rango y ha pasado suficiente tiempo desde la última detección
    if (distancia > 0 && distancia < MAX_DISTANCE && tiempo_actual - ultima_deteccion > 3000) {
        ultima_deteccion = tiempo_actual;
        Serial.println("objeto detectado");
        
        display.clearDisplay();
        display.setCursor(0, 0);
        display.println("Objeto detectado!");
        display.println("Esperando comando...");
        display.display();
        
        unsigned long inicio_espera = tiempo_actual;
        
        // Entra en un bucle que espera un comando serial durante 2 segundos
        while (millis() - inicio_espera < 2000) {
            if (Serial.available() > 0) { // Si hay datos disponibles en el puerto serial
                byte entrada = Serial.read(); // Lee el comando
                procesarComando(entrada);    // Procesa el comando
                break;                       // Sale del bucle de espera
            }
            delay(50); // Pequeña pausa para no sobrecargar el bucle
        }
        
        // Limpia la pantalla si no se recibió un comando después de la espera
        display.clearDisplay();
        display.display();
    }
    delay(100); // Pausa al final del bucle para evitar lecturas inestables
}
