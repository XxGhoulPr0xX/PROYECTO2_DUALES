from conexionEsp32 import *
from detectarPorCamara import *
import time

class PythonToArduino:
    def __init__(self, path_model, confianza, puerto, baudrate):
        self.alpha = WasteCameraDetector(path_model, confianza)
        self.charlie = conexionEsp32(puerto, baudrate)
        self.timeDetection = 2  # Time to keep detecting after object is detected
        self.lastCommand = None
        self.timeOfLastSend = 0
        self.shippingInterval = 0.5  # Minimum time between commands
        self.bandera = False  # Flag to control detection state
        if not self.charlie.establecerConexion():
            raise RuntimeError("No se pudo conectar al ESP32")

    def mapearClaseToComando(self, clase):
        clases = {
            "Biodegradable": ord('B'),
            "No biodegradable": ord('N')
        }
        return clases.get(clase, None) 

    def enviarBytes(self, comando):
        if comando is not None:
            if not self.charlie.enviarRespuesta(comando, esperar_confirmacion=True):
                print("⚠️ Fallo en la comunicación con ESP32")
            else:
                print(f"[CONSOLA] Enviando comando: {chr(comando)} ({comando}) - Comunicación exitosa")

    def ejecutar(self):        
        try:
            while True:
                if self.bandera is False:
                    mensaje = self.charlie.esperandoMensaje()
                    if mensaje == "objeto detectado":
                        self.bandera = True
                        self.alpha.continuar()
                        print("🔍 Iniciando detección...")
                        tiempo_inicio = time.time()
                        self.lastCommand = None
                
                if self.bandera is True:
                    clase_actual = self.alpha.obtener_deteccion()
                    if time.time() - tiempo_inicio >= self.timeDetection:
                        self.bandera = False
                        self.alpha.pausar()
                        print("⏸️ Cámara pausada, esperando nuevo objeto...")
                        continue
                    if clase_actual in ["Biodegradable", "No biodegradable"]:
                        comando = self.mapearClaseToComando(clase_actual)
                        if (comando is not None and comando != self.lastCommand and 
                            (time.time() - self.timeOfLastSend) >= self.shippingInterval):
                            self.enviarBytes(comando)
                            self.lastCommand = comando
                            self.timeOfLastSend = time.time()
                        else:
                            print(f"[CONSOLA] Clase repetida - No se envía ({clase_actual})")
        except KeyboardInterrupt:
            self.alpha.pausar()
            self.charlie.cerrarConexion()
            print("\nPrograma terminado")
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