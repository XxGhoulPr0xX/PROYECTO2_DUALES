import cv2

def getCameraList():
    camaras = []
    for i in range(0, 10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camaras.append(i)
            cap.release()
    return camaras

camarasDisponibles = getCameraList()

if not camarasDisponibles:
    print("No se encontraron cámaras disponibles.")
else:
    print("Cámaras disponibles:")
    for camara in camarasDisponibles:
        print(f"- Cámara número: {camara}")    
