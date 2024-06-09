from user_commands import *
from messages import *
from models import *

class CommandManager:
    @staticmethod
    def process_command(command_dict, current_hero: Hero, heroes, enemies):
        command = command_dict["COMMAND"]
        not_enought_ap_result = {message_key: "COMMAND_RESULT", "RESULT": "NOT_ENOUGHT_AP"}

        if command == end_turn_command:
            result_dict = {message_key: "COMMAND_RESULT",
                           "RESULT": "END"}
            return result_dict
        
        if command == defend_command:
            if current_hero.ap >= defend_command:
                current_hero.defend()
                result_dict = {message_key: "COMMAND_RESULT", 
                                            "CMD": "DEF", 
                                            "HERO": current_hero.name}
                return result_dict
            else:
                return not_enought_ap_result

        if command == simple_attack_command:
            if current_hero.ap >= simple_attack_ap:
                target_enemy_id = command_dict["TARGET_ID"]
                result = current_hero.attack_enemy(enemies, target_enemy_id)
                result_dict = {message_key: "COMMAND_RESULT",
                               "CMD": "ATTACK", 
                               "HERO": current_hero.name,
                               "RESULT": result, 
                               "TARGET": target_enemy_id}
                return result_dict
            else:
                return not_enought_ap_result
