import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
import os

class WasteCameraDetector:
    def __init__(self, model_path, confianza=0.75,camara=1):
        self.model = self.load_model(model_path)
        self.cap = cv2.VideoCapture(camara)
        self.conf_threshold = confianza
        self.class_labels = {0: 'No Biodegradable', 1: 'Biodegradable'}
        self.class_colors = {0: (0, 255, 0), 1: (0, 0, 255)}
        self.current_label = ""
        self.pausado = False
        self.frame_pausa = None
        self.target_size = (224, 224)

    def load_model(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        return load_model(model_path)
    
    def capturar_frame(self):
        if self.pausado:
            return self.frame_pausa if self.frame_pausa is not None else None
        ret, frame = self.cap.read()
        if not ret:
            print("Error: No se pudo capturar el frame.")
            return None
        return cv2.flip(frame, 1)

    def preprocess_frame(self, frame):
        resized = cv2.resize(frame, self.target_size)
        img_array = np.expand_dims(resized, axis=0)
        return preprocess_input(img_array)
    
    def procesar_frame(self, frame):
        if self.pausado or frame is None:
            return None, 0.0
        processed = self.preprocess_frame(frame)
        predictions = self.model.predict(processed, verbose=0)[0]
        predicted_class = np.argmax(predictions)
        confidence = np.max(predictions)
        if confidence >= self.conf_threshold:
            self.current_label = self.class_labels[predicted_class]
            return self.current_label, float(confidence)
        return None, 0.0

    def dibujar_resultados(self, frame, label, confidence):
        if frame is None:
            return None
        if label:
            color = self.class_colors[0] if label == "Biodegradable" else self.class_colors[1]
            text = f"{label} ({confidence*100:.1f}%)"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        else:
            text = "Buscando deteccion..."
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        return frame

    def pausar(self):
        if not self.pausado:
            self.pausado = True
            self.frame_pausa = self.capturar_frame()
            print("Cámara pausada")

    def continuar(self):
        if self.pausado:
            self.pausado = False
            self.frame_pausa = None
            print("Cámara continuada")

    def obtener_deteccion(self):
        frame = self.capturar_frame()
        label, confidence = self.procesar_frame(frame)
        frame = self.dibujar_resultados(frame, label, confidence)
        if frame is not None:
            cv2.imshow("Waste Detection", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            return "salir"
        elif key & 0xFF == ord('p'):
            self.pausar()
        elif key & 0xFF == ord('c'):
            self.continuar()
        return label
    
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()