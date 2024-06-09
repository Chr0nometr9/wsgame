import asyncio
import websockets as ws
from collections import defaultdict
from random import choice
from room import Room
from user import User

from messages import *

temp_room_locks = defaultdict(asyncio.Lock)
rooms = {}

async def handler(websocket: ws.WebSocketClientProtocol, path):
    room_name = path.strip("/")

    current_user = User(websocket)
    await current_user.login_procedure()

    await temp_room_locks[room_name].acquire()
    
    if room_name not in rooms:
        rooms[room_name] = Room()
    room: Room = rooms[room_name]

    if room.players_count < room.max_players_count:
        await room.add_player(current_user)
        if room.is_full():
            asyncio.create_task(room.battle())
    elif room.is_full():
        await current_user.send(c2_pack(room_is_full_err)) 
        await websocket.close()
        return
    
    temp_room_locks[room_name].release()

    try:
        async for command in current_user.websocket:
            if room.current_player is current_user:
                await current_user.commands_queue.put(command)

    finally:
        await room.remove_player(websocket)

async def main():
    async with ws.serve(handler, "localhost", 8765):
        await asyncio.Future()
asyncio.run(main())
