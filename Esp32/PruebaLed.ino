#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Wire.h>

// Definiciones para la pantalla OLED
#define SCREEN_WIDTH 128    // Ancho de la pantalla en píxeles
#define SCREEN_HEIGHT 64    // Alto de la pantalla en píxeles
#define OLED_RESET -1       // Pin de reset (se usa -1 para ESP32)

// Definir los pines de I2C para ESP32 S2 Mini
#define I2C_SDA_PIN 8
#define I2C_SCL_PIN 9

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(115200);

  // Inicializa la comunicación I2C con los pines correctos antes de la pantalla.
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);

  // Inicializa la pantalla OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Dirección I2C: 0x3C
    Serial.println(F("Error en la inicialización de la pantalla OLED"));
    for(;;); // Detiene el programa
  }

  // Limpia el buffer de la pantalla y la apaga
  display.clearDisplay();
  display.display();

  // Configura el texto a mostrar
  display.setTextSize(1);          // Tamaño del texto
  display.setTextColor(SSD1306_WHITE); // Color del texto (blanco)
  display.setCursor(0, 0);         // Posición del cursor (X, Y)

  // Muestra el mensaje en la pantalla
  display.println("Hola");
  display.println("Mundo!");

  // Muestra el buffer en la pantalla física
  display.display();
}

void loop() {
  // Este bucle se mantiene vacío para este ejemplo
}