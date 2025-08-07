# Diseño e Implementación de un Contenedor de Basura Inteligente Basado en Inteligencia Artificial en Infotec

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.8+-orange)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-yellowgreen)

## 📌 Descripción
Sistema automatizado que clasifica residuos en 2 categorías (Biodegradable/No Biodegradable) usando visión por computadora (CNN con ResNet50) y controla un sistema mecánico mediante ESP32. Ofrece dos modos de análisis: tiempo real y por captura de 5 frames.

## 🧩 Componentes Principales

### 🔌 `conexionEsp32.py`
- Manejo de comunicación serial con ESP32
- Timeout configurable (1s por defecto)
- Envío con confirmación de recepción
- Buffer clearing automático

### 📷 `detectarPorCamara5Frames.py` (Versión multicaptura)
- **Modo 5 Frames**: Captura y analiza 5 imágenes consecutivas
- Preprocesamiento con ResNet50
- Umbral de confianza ajustable (default: 70%)
- Visualización en tiempo real
- Control por teclado (pausa/continuar/analizar)

### 🖼️ `pruebaModelos.py`
- Validación con imágenes estáticas
- Muestra probabilidades por clase
- Soporta múltiples formatos (JPG, PNG, etc.)
- Visualización con matplotlib

### 🤖 `PythonToEsp32_v2.py`
- Integración completa del flujo:
  1. Espera detección ultrasónica
  2. Activa análisis por cámara
  3. Procesa resultados
  4. Envía comando a ESP32
- Protección contra envíos repetidos
- Temporizador configurable

### ⚙️ `Esp32ToPython.ino`
- Control preciso de servo (movimiento suave)
- Detección por ultrasonido (HC-SR04)
- Protocolo serial optimizado
- Mecanismo anti-rebote

## 🛠️ Instalación
```bash
git clone https://github.com/XxGhoulPr0xX/PROYECTO2_DUALES.git
cd PROYECTO2_DUALES
pip install -r requirements.txt
```

**Requisitos adicionales:**
- TensorFlow 2.8+
- OpenCV 4.5+
- pyserial 3.5+

## ⚙️ Configuración Hardware
| Componente       | Conexión ESP32 | Notas                     |
|------------------|----------------|---------------------------|
| Sensor HC-SR04   | TRIG:GPIO1, ECHO:GPIO2 | Rango 2-10 cm   |
| Servo SG90       | GPIO13         | Movimiento 0°-180°        |

## 📊 Modelo de Clasificación
- **Arquitectura**: ResNet50 modificada
- **Clases**: 
  - 0: Biodegradable 
  - 1: No Biodegradable
- **Precisión**: 92% (dataset de validación)
- **Input Size**: 224x224 px

## 🚀 Uso
1. Cargar sketch `Esp32ToPython.ino` al ESP32
2. Ejecutar sistema principal:
```bash
python PythonToEsp32_v2.py
```
3. Flujo de operación:
   - El sensor ultrasónico detecta objeto
   - El sistema captura 5 frames consecutivos
   - Analiza cada frame y promedia resultados
   - Envía comando ('B' o 'N') al ESP32
   - El servo se posiciona según la clasificación

**Atajos de teclado (modo cámara):**
- `P`: Pausar captura
- `C`: Continuar captura
- `A`: Analizar frames manualmente
- `Q`: Salir

## 🔄 Versiones Disponibles
| Versión          | Ventajas                     | Uso Recomendado         |
|------------------|------------------------------|-------------------------|
| Tiempo Real      | Menor latencia               | Objetos estáticos       |
| 5 Frames         | Mayor precisión              | Objetos en movimiento   |

## 📌 Notas Técnicas
- **Confianza mínima**: Ajustable en código (default: 70%)
- **Tiempo de análisis**: 5 segundos (configurable)
- **Protocolo Serial**:
  - ESP32 → Python: "objeto detectado"
  - Python → ESP32: 'B' (Biodegradable), 'N' (No biodegradable)

> 💡 **Tip**: Para calibrar el sensor ultrasónico, usar `PruebaSensorUltraSonico.ino`. La distancia óptima de detección es 5-8 cm.

## 📊 Estructura del Proyecto
```
/proyecto-clasificacion
├── /Modelos
│   └── tu_modelo.h5          # Modelo preentrenado
├── /Arduino
│   └── Esp32ToPython.ino          # Firmware ESP32
├── /TEST                          # Imágenes de prueba
├── conexionEsp32.py               # Módulo de comunicación
├── detectarPorCamara5Frames.py    # Versión multicaptura
├── pruebaModelos.py               # Validador estático
├── PythonToEsp32_v2.py            # Sistema principal
```
