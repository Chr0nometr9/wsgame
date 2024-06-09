import asyncio
import websockets

users = []

async def echo(websocket):
    users.append(websocket)
    print("Client connected")
    async for message in websocket:
        try:
            for user in users:
                await user.send(message)
        except websockets.ConnectionClosed:
            users.remove(websocket)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())