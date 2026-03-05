import asyncio

import websockets


async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = "Привет, сервер!"
        print(f'Отправка: {message}')
        await websocket.send(message)

        response = await websocket.recv()
        print(f'Ответ от сервера: {response}')


asyncio.run(client())