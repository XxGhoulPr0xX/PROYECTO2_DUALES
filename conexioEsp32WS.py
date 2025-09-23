import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError, InvalidURI, WebSocketException

class WebSocketConnection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = None

    async def _handle_connection(self, websocket):
        print(f"Nuevo cliente conectado desde {websocket.remote_address}")
        try:
            while True:
                message = await websocket.recv()
                print(f"← Recibido del cliente: {message}")
                if message == "objeto identificado":
                    print("Servidor: 'Iniciando detección de IA...'")
                    response = input("Dame el objeto")
                    await websocket.send(response)
                    print(f"→ Enviando al cliente: {response}")
                    received_ack = await websocket.recv()
                    print(f"← Recibido del cliente: {received_ack}")
                    if received_ack == "recibido":
                        print("Servidor: Confirmación 'recibido' por parte del cliente.")                        
                    else:
                        print("Servidor: Se esperaba el mensaje 'recibido' pero se recibió otro.")
                else:
                    print(f"Servidor: Se esperaba 'objeto identificado' pero se recibió '{message}'.")
        except ConnectionClosedError:
            print(f"Conexión con el cliente {websocket.remote_address} cerrada.")
        except Exception as e:
            print(f"Ocurrió un error en la conexión: {e}")

    async def iniciarServidor(self) -> bool:
        try:
            print(f"Iniciando servidor en ws://{self.host}:{self.port}...")
            self.server = await websockets.serve(self._handle_connection, self.host, self.port)
            print("Servidor listo y esperando conexiones.")
            await self.server.wait_closed()
            return True
        except (ConnectionRefusedError, InvalidURI) as e:
            print(f"Error de conexión: {e}")
            return False
        except WebSocketException as e:
            print(f"Error en WebSocket: {e}")
            return False
    
    async def cerrarServidor(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("Servidor WebSocket cerrado.")

async def main():
    host_servidor = "192.168.0.121"
    puerto_servidor = 8765
    servidor = WebSocketConnection(host_servidor, puerto_servidor)
    await servidor.iniciarServidor()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Servidor detenido por el usuario.")