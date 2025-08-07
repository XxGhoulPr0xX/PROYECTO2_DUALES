import cv2
import numpy as np
from collections import Counter
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
import os

class WasteCameraDetector:
    def __init__(self, model_path, confianza=0.75, camara=1, num_frames=5):
        self.model = self.load_model(model_path)
        self.cap = cv2.VideoCapture(camara)
        self.conf_threshold = confianza
        self.class_labels = {0: 'No Biodegradable', 1: 'Biodegradable'}
        self.class_colors = {0: (0, 255, 0), 1: (0, 0, 255)}
        self.pausado = False
        self.num_frames = num_frames
        self.frames_capturados = []
        self.resultado_final = None
        self.confianza_promedio = 0.0
        self.frame_resultado = None

    def load_model(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        return load_model(model_path)
    
    def capturar_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: No se pudo capturar el frame.")
            return None
        return cv2.flip(frame, 1)

    def preprocess_frame(self, frame):
        resized = cv2.resize(frame, (224, 224))
        img_array = np.expand_dims(resized, axis=0)
        return preprocess_input(img_array)
    
    def procesar_frame(self, frame):
        if frame is None:
            return None, 0.0
        processed = self.preprocess_frame(frame)
        predictions = self.model.predict(processed, verbose=0)[0]
        predicted_class = np.argmax(predictions)
        confidence = np.max(predictions)
        if confidence >= self.conf_threshold:
            label = self.class_labels[predicted_class]
            return label, float(confidence)
        return None, 0.0

    def analizar_frames_capturados(self):
        if not self.frames_capturados:
            return None, 0.0
        
        resultados = []
        confianzas = []
        
        for frame in self.frames_capturados:
            label, confidence = self.procesar_frame(frame)
            if label:
                resultados.append(label)
                confianzas.append(confidence)
        if not resultados:
            return None, 0.0
        conteo = Counter(resultados)
        resultado_final = conteo.most_common(1)[0][0]
        confianza_promedio = np.mean([conf for lbl, conf in zip(resultados, confianzas) if lbl == resultado_final])
        
        return resultado_final, confianza_promedio

    def dibujar_resultados(self, frame):
        if frame is None:
            return None
            
        if self.pausado:
            if self.resultado_final:
                texto = f"Resultado: {self.resultado_final} ({self.confianza_promedio*100:.1f}%)"
                color = self.class_colors[0] if self.resultado_final == "Biodegradable" else self.class_colors[1]
                cv2.putText(frame, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(frame, "Presione 'c' para continuar", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            else:
                texto = f"Capturando: {len(self.frames_capturados)}/{self.num_frames} frames"
                cv2.putText(frame, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        else:
            cv2.putText(frame, "Presione 'p' para analizar", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return frame

    def pausar(self):
        if not self.pausado:
            self.pausado = True
            self.frames_capturados = []
            self.resultado_final = None

    def continuar(self):
        if self.pausado:
            self.pausado = False
            self.resultado_final = None
            self.frames_capturados = []

    def obtener_deteccion(self):
        frame = self.capturar_frame()
        if self.pausado:
            if frame is not None and len(self.frames_capturados) < self.num_frames:
                self.frames_capturados.append(frame.copy())
            if len(self.frames_capturados) == self.num_frames and self.resultado_final is None:
                self.resultado_final, self.confianza_promedio = self.analizar_frames_capturados()
                self.frame_resultado = frame.copy()
        frame_mostrar = self.frame_resultado if (self.pausado and self.resultado_final) else frame
        frame_mostrar = self.dibujar_resultados(frame_mostrar)
        
        if frame_mostrar is not None:
            cv2.imshow("Waste Detection", frame_mostrar)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            return "salir"
        elif key & 0xFF == ord('p') and not self.pausado:
            self.pausar()
        elif key & 0xFF == ord('c') and self.pausado:
            self.continuar()
        
        return self.resultado_final if self.resultado_final else None
    
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Python\\Modelos\\Identificacion de images\\predictWaste12.h5"
    detector = WasteCameraDetector(model_path, confianza=0.70, camara=0, num_frames=5)
    
    while True:
        resultado = detector.obtener_deteccion()
        if resultado == "salir":
            break