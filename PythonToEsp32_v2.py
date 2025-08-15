from conexionEsp32 import *
from detectarPorCamara5Frames import *
import time

class PythonToArduino:
    def __init__(self, path_model, confianza, puerto, baudrate,camara):
        self.alpha = Camera(path_model,camara,confianza)
        self.charlie = conexionEsp32(puerto, baudrate)
        self.bandera = False 
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
                        start_time = time.time()
                        while (time.time() - start_time) <= 5:
                            self.alpha.inicarCamara()
                if self.bandera:
                    self.alpha.frames_guardados = []
                    resultado, confianza = self.alpha.analizarFramesGuardados()
                    if resultado:
                        print(f"Resultado: {resultado} (Confianza: {confianza:.2f})")
                        comando = self.mapearClaseToComando(resultado)
                        self.enviarBytes(comando)
                        self.bandera = False
                        cv2.destroyWindow("Cámara")

        except Exception as e:
            print(f"Error inesperado: {str(e)}")
        finally:
            cv2.destroyAllWindows()