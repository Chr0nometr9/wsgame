from json import dumps, loads

def c2_pack(raw_dict: dict) -> str:
    c2_dict = {"c2dictionary": True, "data": raw_dict}
    return dumps(c2_dict)

def c2_unpack(c2_json: str) -> dict:
    c2_dict = loads(c2_json)
    raw_dict = c2_dict["data"]
    return raw_dict

#повідомлення від сервера до гравців
message_key = "MESSAGE"
wait_login_msg = {message_key: "WAIT_LOGIN"} # очікується авторизація
battle_has_begun_msg = {message_key: "BATTLE_START"} # битва почалась

#повідомлення з помилками
error_key = "ERROR"
login_already_exist_err = {error_key: "LOGIN_EXIST"} # цей логін вже використовується
process_cmd_err = {error_key: "PROC_CMD"} # помилка обробки команди
room_is_full_err = {error_key: "ROOM_FULL"} # кімната заповнена

#ключі (для json рядків) для передачі ігрової інформації
your_index_key = "YOUR_INDEX"
turn_index_key = "TURN_INDEX"

