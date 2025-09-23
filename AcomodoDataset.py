import os
import shutil
from PIL import Image  

extensiones_imagen = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
bi = ["cardboard", "paper", "food organics", "vegetation", "textile trash"]
nb = ["glass", "metal", "plastic", "miscellaneous trash"]

def listar_carpetas(ruta,b,n):
    elementos = os.listdir(ruta)   
    carpetas = [elemento for elemento in elementos if os.path.isdir(os.path.join(ruta, elemento))]

    for carpeta in carpetas:
        if carpeta.lower() in bi:
            moverArchivos(f"{ruta}//{carpeta}",b)
        elif carpeta.lower() in nb:
            moverArchivos(f"{ruta}//{carpeta}",n)

def moverArchivos(carpeta_origen, directorio_destino):
    archivos = [f for f in os.listdir(carpeta_origen) if os.path.isfile(os.path.join(carpeta_origen, f))]
    for archivo in archivos:
        origen_path = os.path.join(carpeta_origen, archivo)
        destino_path = os.path.join(directorio_destino, archivo)
        contador = 1
        nombre_base, extension = os.path.splitext(archivo)
        while os.path.exists(destino_path):
            nuevo_nombre = f"{nombre_base}_{contador}{extension}"
            destino_path = os.path.join(directorio_destino, nuevo_nombre)
            contador += 1
        shutil.move(origen_path, destino_path)

def cambiarNombreArchivos(directorio, prefijo, nuevo_tamaño=(200, 200)):
    archivos = [f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))]
    archivos.sort()
    for i, archivo in enumerate(archivos, 1):
        origen_path = os.path.join(directorio, archivo)
        nuevo_nombre = f"{prefijo}{i:04d}{os.path.splitext(archivo)[1]}"
        nuevo_path = os.path.join(directorio, nuevo_nombre)
        if os.path.splitext(archivo)[1].lower() in extensiones_imagen:
            with Image.open(origen_path) as img:
                img_redimensionada = img.resize(nuevo_tamaño, Image.Resampling.LANCZOS)
                img_redimensionada.save(nuevo_path)
            os.remove(origen_path)
        else:
            os.rename(origen_path, nuevo_path)

def main(ruta1, ruta2, b, n):
    print("Procesando primera ruta...")
    listar_carpetas(ruta1, b, n)
    
    print("\nProcesando segunda ruta...")
    listar_carpetas(ruta2, b, n)
    
    print("\nRenombrando archivos biodegradables...")
    cambiarNombreArchivos(b, "biodegradable", (200, 200))
    
    print("\nRenombrando archivos no biodegradables...")
    cambiarNombreArchivos(n, "nobiodegradable", (200, 200))
    
    print("\n¡Proceso completado!")

if __name__ == "__main__":
    ruta1="C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Dataset bio y no-bio\\realwaste-main"
    ruta2="C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Dataset bio y no-bio\\dataset-resized"
    b="C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Dataset bio y no-bio\\B"
    n="C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\2° Proyecto\\Dataset bio y no-bio\\N"
    if not os.path.exists(b):
        os.makedirs(b)
    if not os.path.exists(n):
        os.makedirs(n)
    main(ruta1, ruta2, b, n)