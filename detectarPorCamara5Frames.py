import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
import os

class Camera:
    def __init__(self, ruta, camara=1,confianza=0.70):
        self.cap = cv2.VideoCapture(camara)
        self.confianza=confianza
        self.pausado = False
        self.frame_pausa = None
        self.modelo = self.cargarModelo(ruta)  # Cargamos el modelo al inicializar
        self.frames_guardados = []
        self.class_labels = {0: 'No Biodegradable', 1: 'Biodegradable'}

    def inicarCamara(self):
        self.ret, self.frame = self.cap.read()

    def cargarModelo(self,ruta):
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Model file not found at {ruta}")
        return load_model(ruta)

    def pausarC(self):
        if not self.pausado:
            self.pausado = True
            self.frame_pausa = self.obtenerUltimoF()
            print("Cámara pausada")

    def continuarC(self):
        if self.pausado:
            self.pausado = False
            self.frame_pausa = None
            print("Cámara continuada")

    def obtenerUltimoF(self):
        if self.pausado:
            return self.frame_pausa if self.frame_pausa is not None else None
        if not self.ret:
            print("Error: No se pudo capturar el frame.")
            return None
        return cv2.flip(self.frame, 1)

    def guardarFrame(self):
        for _ in range(5):
            self.inicarCamara()  # Reiniciar el frame
            frame = self.obtenerUltimoF()
            if frame is not None:
                self.frames_guardados.append(frame.copy())
                cv2.imshow("Cámara", frame)  # Muestra el frame actual
                cv2.waitKey(200)  # Espera 200ms (0.2s) entre frames

    
    def preprocess_frame(self, frame):
        resized = cv2.resize(frame,(224, 224))
        img_array = np.expand_dims(resized, axis=0)
        return preprocess_input(img_array)
        
    def analizarFramesGuardados(self):
        print("Analisis ejeuctado de los siguientes 5 frames")
        self.guardarFrame()
        total_confidence = 0.0
        predictions_count = {0: 0, 1: 0}  # Contador de predicciones por clase
        
        for frame in self.frames_guardados:
            if frame is None:
                continue
                
            processed = self.preprocess_frame(frame)
            predictions = self.modelo.predict(processed, verbose=0)[0]
            predicted_class = np.argmax(predictions)
            confidence = np.max(predictions)
            
            if confidence >=self.confianza:
                predictions_count[predicted_class] += 1
                total_confidence += confidence
        if sum(predictions_count.values()) == 0:
            return None, 0.0
        predominant_class = max(predictions_count, key=predictions_count.get)
        avg_confidence = total_confidence / sum(predictions_count.values())
        
        return self.class_labels[predominant_class], avg_confidence

    def run(self):
        self.inicarCamara()
        frame = self.obtenerUltimoF()
        if frame is not None:
            cv2.imshow("Cámara", frame)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            return "salir"
        elif key & 0xFF == ord('p'):
            self.pausarC()
        elif key & 0xFF == ord('c'):
            self.continuarC()
        elif key & 0xFF == ord('a'):
            self.frames_guardados=[]
            resultado, confianza = self.analizarFramesGuardados()
            if resultado:
                print(f"Resultado del análisis: {resultado} (Confianza promedio: {confianza:.2f})")
            else:
                print("No se detectaron objetos válidos en los frames")
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camara = Camera("C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Python\\Modelos\\Identificacion de images\\predictWaste12.h5", camara=0,confianza=0.70)
    while True:
        resultado = camara.run()
        if resultado == "salir":
            break