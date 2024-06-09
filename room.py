import asyncio
import websockets as ws
import json
from copy import deepcopy
from random import choice

import rooms_presets
from user import User
from command_manager import CommandManager

from models import *
from messages import *


class Room:
    def __init__(self):
        
        self.players = []
        self.max_players_count = 2
        self.current_turn_index = 0

        self.heroes = []
        self.enemies = deepcopy(rooms_presets.room_1)
        self.inner_lock = asyncio.Lock()
    
    @property
    def players_count(self) -> int:
        return len(self.players)
    
    @property
    def enemies_count(self) -> int:
        return len(self.enemies)

    @property
    def current_player(self) -> User:
        return self.players[self.current_turn_index]
    
    @property
    def current_hero(self) -> Hero: 
        return self.heroes[self.current_turn_index]

    def is_full(self) -> bool:
        return (self.players_count == self.max_players_count)

    async def send_all_players(self, message):
        for player in self.players:
            await player.send_raw_message(message)

    async def send_info_by_key(self, key: str, info: str|int, target_player:User=None):
        message = {key: info}
        message_json = c2_pack(message)
        if target_player is None:
            await self.send_all_players(message_json)
        else:
            await target_player.send_raw_message(message_json)

    async def add_player(self, user: User):
        await self.inner_lock.acquire()
        self.players.append(user)
        await self.send_info_by_key(your_index_key, self.players.index(user), target_player=user)
        self.heroes.append(Hero(name=user.login))
        self.inner_lock.release()
    
    async def remove_player(self, user):
        await self.inner_lock.acquire()
        index = self.players.index(user)
        self.players.pop(index)
        self.heroes.pop(index)
        self.inner_lock.release()

    async def send_room_configuration(self):
        room_configuration = {"PLAYERS_COUNT": self.players_count,
                              "ENEMIES_COUNT": self.enemies_count}
        await self.send_all_players(c2_pack(room_configuration))

    async def send_room_state(self):
        for id, hero in enumerate(self.heroes):
            hero_state = hero.get_state()
            hero_state['HERO_ID'] = id
            await self.send_all_players(c2_pack(hero_state))
        for id, enemy in enumerate(self.enemies):
            enemy_state = enemy.get_state()
            enemy_state['ENEMY_ID'] = id
            await self.send_all_players(c2_pack(enemy_state))
            
    async def enemies_turn(self):
        living_heroes = [hero for hero in self.heroes if hero.is_alive()]
        living_enemies = [enemy for enemy in self.enemies if enemy.is_alive()] 
        for enemy in living_enemies:
            target_hero = choice(living_heroes)
            damage = enemy.attack(target_hero)
            result_dict = {message_key: "ENEMY_ATTACK", 
                           "TARGET_HERO": target_hero.name, 
                           "RESULT": damage}
            await self.send_all_players(c2_pack(result_dict))

    async def battle(self):
        await self.send_all_players(c2_pack(battle_has_begun_msg))
        await self.send_room_configuration()
        
        while True:
            result = None
            while not result == "END":
                await self.send_room_state()
                await self.send_info_by_key(turn_index_key, self.current_turn_index)
                if self.current_hero.is_alive():
                    self.current_hero.reset_turn()
                    command_json = await asyncio.wait_for(self.current_player.commands_queue.get(), timeout=None)
                    command = c2_unpack(command_json)
                    result_dict = CommandManager.process_command(command, self.current_hero, self.heroes, self.enemies)
                    result = result_dict["RESULT"]
                    await self.send_all_players(c2_pack(result_dict))

            
            if self.current_turn_index == self.players_count - 1:
                await self.enemies_turn()

            self.current_turn_index = (self.current_turn_index + 1) % self.players_count 
                

