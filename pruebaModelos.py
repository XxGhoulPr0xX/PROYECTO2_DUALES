import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import matplotlib.pyplot as plt
import os


class Prueba:
    def __init__(self, imagen, modelo):
        self.modelo = self.loadModel(modelo)
        self.imagen = imagen
        self.clases = {0: 'Biodegradable', 1: 'No biodegradable'}

    def loadModel(self, ruta_modelo):
        if not os.path.exists(ruta_modelo):
            raise FileNotFoundError(f"No se encontró el archivo del modelo en {ruta_modelo}")
        modelo = load_model(ruta_modelo)
        return modelo

    def processImage(self, target_size=(224, 224)):
        if not os.path.exists(self.imagen):
            raise FileNotFoundError(f"No se encontró la imagen en {self.imagen}")
        img = image.load_img(self.imagen, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predictImage(self, modelo, img_array, clases):
        predicciones = modelo.predict(img_array)
        clase_predicha = np.argmax(predicciones[0])
        probabilidad = np.max(predicciones[0])
        nombre_clase = clases[clase_predicha]
        
        return {
            'clase': nombre_clase,
            'probabilidad': float(probabilidad),
            'todas_las_probabilidades': predicciones[0].tolist()
        }

    def showResults(self, ruta_imagen, prediccion, clases):
        img = image.load_img(ruta_imagen)
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.title(f"Predicción: {prediccion['clase']} ({prediccion['probabilidad']*100:.2f}%)")
        plt.axis('off')
        print("\nProbabilidades por clase:")
        for idx, prob in enumerate(prediccion['todas_las_probabilidades']):
            print(f"{clases[idx]}: {prob*100:.2f}%")
        plt.show()

    def run(self):
        try:
            img_array = self.processImage()
            prediccion = self.predictImage(self.modelo, img_array, self.clases)
            self.showResults(self.imagen, prediccion, self.clases)
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":   
    model_path = "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Python\\Modelos\\Identificacion de images\\predictWaste12.h5"
    image_path = "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\TEST\\B\\TEST_BIODEG_HFL_8.jpg"
    alpha = Prueba(image_path, model_path)
    alpha.run()