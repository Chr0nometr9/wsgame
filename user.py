import json
from websockets import WebSocketClientProtocol
from asyncio import Queue
from messages import *

logins = set()


async def handle_user_cmd(websocket: WebSocketClientProtocol):
    cmd_c2_json = await websocket.recv()
    return c2_unpack(cmd_c2_json)
 

class User:
    def __init__(self, websocket: WebSocketClientProtocol):
        self.websocket = websocket
        self.login = None
        self.commands_queue = Queue()
        
    async def login_procedure(self):
        await self.websocket.send(c2_pack(wait_login_msg))
        while True:
            command = await handle_user_cmd(self.websocket)
            if not "LOGIN" in command:
                await self.send(c2_pack(process_cmd_err))
            else:
                login = command["LOGIN"]
                if login in logins:
                    await self.send(c2_pack(login_already_exist_err))
                else:
                    logins.add(login)
                    self.login = login
                    break
    
    async def send_raw_message(self, message: str):
        await self.websocket.send(message)

    def __str__(self):
        return self.login