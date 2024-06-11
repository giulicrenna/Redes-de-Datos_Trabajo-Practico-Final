from typing import IO, Any
import os
import json
import hashlib


NOBELS_PATH: str = os.path.join(os.getcwd(), 'data', 'nobels.json')
USERS_PATH: str = os.path.join(os.getcwd(), 'data', 'users.json')

def hash_password(password: str) -> str:
    hasher: Any = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()

def users_handler() -> IO[Any] | None:
    try:
        if not os.path.exists(USERS_PATH):
            return json.dumps({"Error" : "No se pudo abrir el archivo"})
        
        with open(USERS_PATH, 'r+') as file_handler:
            data = json.load(file_handler)
            return data
        
    except IOError as e:
        print(f"No se pudo abrir el archivo: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"No se pudo decodificar el archivo: {e}")
        return None

def validate_user(username: str, password: str) -> bool:
    users = users_handler()
    if users is None:
        return False

    for user in users["users"]:
        if user['username'] == username and user['password'] == hash_password(password):
            return True
    
    return False

def create_user(username: str, password: str) -> bool:
    users = users_handler()
   
    if users is None:
        return False
    
    for user in users["users"]:
        if user['username'] == username:
            return False
    
    users["users"].append({"username": username, "password": hash_password(password)})
    
    with open(USERS_PATH, 'w') as file_handler:
        json.dump(users, file_handler, indent=4)
    
    return True
 
def change_password(username: str, old_password: str, new_password: str) -> bool:
    users = users_handler()
    
    if users is None:
        return False
    
    for user in users["users"]:
        if user['username'] == username and user['password'] == hash_password(old_password):
            user["password"] = hash_password(new_password)
            return True
    
    return False

def nobels_handler() -> IO[Any] | None:
    try:
        if not os.path.exists(NOBELS_PATH):
            return json.dumps({"Error" : "No se pudo abrir el archivo"})
        
        with open(NOBELS_PATH, 'r+') as file_handler:
            data = json.load(file_handler)
            return data
    except IOError as e:
        print(f"No se pudo abrir el archivo: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"No se pudo decodificar el archivo: {e}")
        return None
    
def add_nobel_data(nobel_data: dict) -> bool:
    nobels = nobels_handler()
    
    if nobels is None:
        return False
    nobels["prizes"].append(nobel_data)
    
    with open(NOBELS_PATH, 'w') as file_handler:
        json.dump(nobels, file_handler, indent=4)
    
    return True
 
 
 