import asyncio
import websockets

async def handle_connection(websocket):
    try:
        message = await websocket.recv()
        print(f"Mensaje recibido de ESP32: {message}")

        response_message = "Como estas esp32?"
        await websocket.send(response_message)
        print(f"Respondiendo a ESP32: {response_message}")

        confirmation = await websocket.recv()
        print(f"Confirmación recibida de ESP32: {confirmation}")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Conexión cerrada con ESP32. Código: {e.code}, Razón: {e.reason}")

async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())