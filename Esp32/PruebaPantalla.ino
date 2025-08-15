//TFT_MISO	12
//TFT_MOSI	13
//TFT_SCLK	14
//TFT_CS	15 (Chip Select)
//TFT_DC	2 (Data/Command)
//TFT_RST	4 (Conectado al RST del ESP32 o a 3.3V)
//TFT_LED	21 (Backlight)
#include <TFT_eSPI.h>
TFT_eSPI tft = TFT_eSPI();

void setup() {
    tft.init();
    tft.setRotation(1); // Ajusta la orientación si es necesario
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextSize(2);
    tft.drawString("Hola Mundo!", 50, 120);
}

void loop() {}