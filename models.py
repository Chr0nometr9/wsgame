import random
from messages import *

class Unit:
    def __init__(self, name, hp, max_dmg):
        self.name = name
        self.hp = hp
        self.max_dmg = max_dmg

    def take_damage(self, dmg):
        self.hp -= dmg

    def is_alive(self):
        return self.hp > 0


class Hero(Unit):
    def __init__(self, name):
        super().__init__(name, 100, 30)
        self.ap = 8
        self.defence_flag = False

    def reset_turn(self):
        self.defence_flag = False
        self.ap = 8

    def attack_enemy(self, enemy_list, enemy_id_choice):
        current_damage = self.attack(enemy_list[enemy_id_choice])
        self.ap -= 5
        return current_damage

    def attack(self, target: Unit):
        current_damage = random.randint(int(0.75 * self.max_dmg), self.max_dmg)
        target.take_damage(current_damage)
        return current_damage

    def defend(self):
        self.defence_flag = True
        self.ap -= 3

    def get_state(self):
        hero_state = {message_key: "HERO_STATE", "HERO_NAME": self.name, "HERO_HP": self.hp, "HERO_AP": self.ap, "HERO_MAX_DMG": self.max_dmg}
        return hero_state


class Enemy(Unit):
    def __init__(self, name, hp, max_dmg):
        super().__init__(name, hp, max_dmg)

    def attack(self, target):
        current_damage = random.randint(int(0.75 * self.max_dmg), self.max_dmg)
        if target.defence_flag:
            current_damage //= 2
        target.take_damage(current_damage)
        return current_damage
    
    def get_state(self):
        enemy_state = {message_key: "ENEMY_STATE", "ENEMY_NAME": self.name, "ENEMY_HP": self.hp, "ENEMY_MAX_DMG": self.max_dmg}
        return enemy_state

