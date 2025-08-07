# Diseño e Implementación de un Contenedor de Basura Inteligente Basado en Inteligencia Artificial en Infotec

## 📌 Descripción General
Proyecto de sistema embebido basado en ESP32-S2 para la clasificación automatizada de residuos. El sistema detecta objetos mediante un sensor, analiza los frames capturados y activa actuadores para organizar la basura de forma eficiente.

## 🚀 Características Principales
- **Detección de objetos**: Sensor de entrada para detectar presencia de residuos
- **Procesamiento de frames**: Análisis de imágenes con inteligencia artificial esperando 5 segundos para mayor precisión
- **Control de actuadores**: Sistema de actuadores para clasificar residuos según tipo
- **Arquitectura embebida**: Implementación optimizada para ESP32-S2

## 🧩 Componentes Principales
1. **ESP32-S2** - Unidad de control central
2. **Sensor de detección**
3. **Sistema de actuadores**
4. **Protocolo de procesamiento de señales**

## ⚙️ Flujo de Trabajo
1. **Detección**: El sensor identifica la presencia de un objeto
2. **Delay**: 5 segundos de espera para estabilización
3. **Análisis**: Procesamiento de frames capturados
4. **Ejecución**: ESP32 activa los actuadores correspondientes para clasificar la basura

## 📬 Contribuciones
Contribuciones bienvenidas. Por favor, crea un issue antes de enviar un pull request.
