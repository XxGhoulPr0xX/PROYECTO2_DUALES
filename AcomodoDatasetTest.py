import os
import shutil
import random

class AcomodoDatasetTestTrain:
    def __init__(self, raiz_origen, dataset_nombre_tt):
        self.RaizOrigen = raiz_origen
        self.DatasetRaiz = dataset_nombre_tt
        
        self.CarpetaEntrenamiento = os.path.join(self.DatasetRaiz, "train")
        self.CarpetaPruebas = os.path.join(self.DatasetRaiz, "test")
        
        self.CantidadImagenes = 2000 
        self.Clases = ["b", "n"]

    def crearCarpetas(self):
        directorios_a_crear = []
        for clase in self.Clases:
            directorios_a_crear.append(os.path.join(self.CarpetaEntrenamiento, clase))
            directorios_a_crear.append(os.path.join(self.CarpetaPruebas, clase))

        for d in directorios_a_crear:
            os.makedirs(d, exist_ok=True)
            print(f"  Directorio creado: {d}")

    def moverImagenes(self):
        for origen_nombre in self.Clases:
            ruta_origen = os.path.join(self.RaizOrigen, origen_nombre) 

            if not os.path.isdir(ruta_origen):
                print(f"ERROR: La carpeta de origen '{ruta_origen}' no existe. Omtiendo.")
                continue

            archivos = [f for f in os.listdir(ruta_origen) if os.path.isfile(os.path.join(ruta_origen, f))]
            random.shuffle(archivos)

            archivos_train = archivos[:self.CantidadImagenes] 
            archivos_test = archivos[self.CantidadImagenes:]

            print(f"\nProcesando carpeta '{origen_nombre}': {len(archivos)} archivos encontrados.")
            print(f"  -> {len(archivos_train)} a 'train'")
            print(f"  -> {len(archivos_test)} a 'test'")

            destino_train = os.path.join(self.CarpetaEntrenamiento, origen_nombre) 
            contador_train = 0
            for archivo in archivos_train:
                ruta_origen_archivo = os.path.join(ruta_origen, archivo)
                ruta_destino_archivo = os.path.join(destino_train, archivo)
                shutil.move(ruta_origen_archivo, ruta_destino_archivo)
                contador_train += 1

            destino_test = os.path.join(self.CarpetaPruebas, origen_nombre) 
            contador_test = 0
            for archivo in archivos_test:
                ruta_origen_archivo = os.path.join(ruta_origen, archivo)
                ruta_destino_archivo = os.path.join(destino_test, archivo)
                shutil.move(ruta_origen_archivo, ruta_destino_archivo)
                contador_test += 1

            print(f"Movimiento de '{origen_nombre}' completado: {contador_train} a train, {contador_test} a test.")

    def run(self):
        self.crearCarpetas()
        self.moverImagenes()

if __name__ == "__main__":
    RaizOrigen = "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Dataset bio y no-bio" 
    NombreDatasetNuevo = "dataset_pruebas" 

    alpha = AcomodoDatasetTestTrain(RaizOrigen, NombreDatasetNuevo)
    alpha.run()