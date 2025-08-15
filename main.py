from PythonToEsp32_v2 import *

if __name__ == "__main__":
    confianza = 0.70
    model_path = "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Python\\Modelos\\Identificacion de images\\predictWaste12.h5"
    com = "COM3"
    serial = 9600
    camara = 0
    try:
        alpha = PythonToArduino(model_path, confianza, com, serial,camara)
        alpha.ejecutar()
    except Exception as e:
        print(f"Error al iniciar el sistema: {str(e)}")