from conexionEsp32 import *
from detectarPorCamara_RT import *
import time

class PythonToArduino:
    def __init__(self, path_model, confianza, puerto, baudrate,camara):
        self.alpha = WasteCameraDetector(path_model, confianza,camara)
        self.charlie = conexionEsp32(puerto, baudrate)
        self.timeDetection = 5  # Tiempo de detección con cámara (5 segundos)
        self.lastCommand = None
        self.timeOfLastSend = 0
        self.shippingInterval = 0.5  # Tiempo mínimo entre comandos
        self.bandera = False  # Controla si la cámara debe estar activa
        self.lastValidDetection = None  # Almacena la última detección válida
        if not self.charlie.establecerConexion():
            raise RuntimeError("No se pudo conectar al ESP32")

    def mapearClaseToComando(self, clase):
        clases = {
            "Biodegradable": ord('B'),
            "No Biodegradable": ord('N')
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
                if not self.bandera:
                    mensaje = self.charlie.esperandoMensaje()
                    if mensaje == "objeto detectado":
                        self.bandera = True
                        self.lastValidDetection = None
                        self.alpha.continuar()
                        print("🔍 Sensor activado: Iniciando detección por cámara ({} segundos)...".format(self.timeDetection))
                        tiempo_inicio = time.time()
                if self.bandera:
                    clase_actual = self.alpha.obtener_deteccion()
                    if clase_actual:
                        self.lastValidDetection = clase_actual
                        print(f"[CONSOLA] Clase detectada: {clase_actual} (Guardada para envío)")
                    if time.time() - tiempo_inicio >= self.timeDetection:
                        if self.lastValidDetection:
                            comando = self.mapearClaseToComando(self.lastValidDetection)
                            self.enviarBytes(comando)
                            time.sleep(0.1)
                        else:
                            print("[CONSOLA] Ninguna detección válida en el período de 5 segundos")
                        self.alpha.pausar()
                        self.bandera = False
                        print("⏸️ Cámara pausada, esperando nuevo objeto...")

        except KeyboardInterrupt:
            self.alpha.pausar()
            self.charlie.cerrarConexion()
            print("\nPrograma terminado por el usuario")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
        finally:
            self.alpha.pausar()
            self.charlie.cerrarConexion()
            print("Sistema detenido completamente")

if __name__ == "__main__":
    confianza = 0.60
    model_path = "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Python\\Modelos\\Identificacion de images\\predictWaste12.h5"
    com = "COM3"
    serial = 9600
    camara = 1
    try:
        beta = PythonToArduino(model_path, confianza, com, serial,camara)
        beta.ejecutar()
    except Exception as e:
        print(f"Error al iniciar el sistema: {str(e)}")