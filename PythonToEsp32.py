from conexionEsp32 import *
from detectarPorCamara import *

class PythonToArduino:
    def __init__(self, path_model, confianza, puerto, baudrate):
        self.alpha = WasteCameraDetector(path_model, confianza)
        #self.charlie = conexionEsp32(puerto, baudrate)
        self.ultima_clase = None
        self.contador_detecciones = 0
        self.umbral_repeticiones = 1 
        
    def mapearClaseToComando(self, clase):
        clases = {
            "Biodegradable": ord('B'),
            "No biodegradable": ord('N')
        }
        return clases.get(clase, None) 

    def enviarBytes(self, comando):
        if comando is not None:
            print(f"[CONSOLA] Enviando comando: {chr(comando)} ({comando})")

    def ejecutar(self):        
        try:
            while True:
                clase_actual = self.alpha.obtener_deteccion()
                if clase_actual == "salir":
                    break
                if clase_actual in ["Biodegradable", "No biodegradable"]:
                    if clase_actual == self.ultima_clase:
                        self.contador_detecciones += 1
                        if self.contador_detecciones == 0:
                            comando = self.mapearClaseToComando(clase_actual)
                            self.enviarBytes(comando)
                        else:
                            print(f"[CONSOLA] Clase repetida {self.contador_detecciones} veces - No se envía")
                    else:
                        self.ultima_clase = clase_actual
                        self.contador_detecciones = 0
                        comando = self.mapearClaseToComando(clase_actual)
                        self.enviarBytes(comando)
                
        except KeyboardInterrupt:
            print("\nInterrupción por teclado")
        finally:
            print("Sistema detenido")

if __name__ == "__main__":
    confianza = 0.75
    model_path = "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Python\\Modelos\\Identificacion de images\\predictWaste12.h5"
    com = "COM3"
    serial = 9600
    
    try:
        beta = PythonToArduino(model_path, confianza, com, serial)
        beta.ejecutar()
    except Exception as e:
        print(f"Error: {str(e)}")