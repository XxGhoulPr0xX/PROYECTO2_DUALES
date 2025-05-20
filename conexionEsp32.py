import serial
import time

class conexionEsp32:
    def __init__(self, puerto, baudrate):
        self.puerto = puerto
        self.baudrate = baudrate
        self.arduino = None

    def establecerConexion(self):
        try:
            self.arduino = serial.Serial(
                port=self.puerto,
                baudrate=self.baudrate,
                timeout=1,
                write_timeout=1
            )
            time.sleep(2)
            print(f"Conexión establecida en {self.puerto} @ {self.baudrate} bauds")
            return True
        except Exception as e:
            print(f"Error de conexión: {str(e)}")
            return False

    def esperandoMensaje(self, timeout=2.0):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.arduino.in_waiting > 0:
                try:
                    mensaje = self.arduino.readline().decode().strip()
                    if mensaje:
                        print(f"← Recibido de Arduino: {mensaje}")
                        return mensaje
                except UnicodeDecodeError:
                    continue
        return None

    def enviarRespuesta(self, data, esperar_confirmacion=True, timeout=1.0):
        try:
            self.arduino.reset_input_buffer()
            self.arduino.reset_output_buffer()
            if isinstance(data, int):
                bytes_envio = bytes([data])
            else:
                bytes_envio = data.encode('utf-8')
            print(f"→ Enviando a Arduino: {data} | Bytes: {bytes_envio}")
            self.arduino.write(bytes_envio)
            if esperar_confirmacion:
                confirmacion = self.esperandoMensaje(timeout)
                return confirmacion == "recibido"
            return True
        except Exception as e:
            print(f"Error en envío: {str(e)}")
            return False

    def cerrarConexion(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("Conexión cerrada")