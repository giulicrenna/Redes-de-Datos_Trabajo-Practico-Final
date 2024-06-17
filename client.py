import requests
from server.py import NewNobel

HOST: str = "127.0.0.1"
PORT: str = "8000"

base_url: str = HOST + ':' + PORT

def get_all_nobels(username: str, password: str):
    response = requests.get(f"{base_url}/all_nobels/{username}/{password}")
    return response.json if response.status.code == 200 else (response.status, response.txt)

def get_nobel_by_year(username: str, password: str, year: str):
    response = requests.get(f"{base_url}/nobel_by_year/{username}/{password}/{year}")
    return response.json if response.status.code == 200 else (response.status, response.txt)

def get_nobel_by_category(username: str, password: str, category: str):
    response = requests.get(f"{base_url}/nobel_by_category/{username}/{password}/{category}")
    return response.json if response.status.code == 200 else (response.status, response.txt)

def get_all_categories(username: str, password: str):
    response = requests.get(f"{base_url}/get_all_categories/{username}/{password}")
    return response.json if response.status.code == 200 else (response.status, response.txt)

def add_nobel(username: str, password: str, nobel_data: NewNobel):
    response = requests.post(f"{base_url}/add_nobel/{username}/{password}", json = nobel_data)


def create_user_api(username: str, password: str):
    response = response.post(f"{base_url}/create_user/{username}/{password}")

def change_password_api(username: str, password: str, new_password: str):
    response = response.post(f"{base_url}/change_password/{username}/{password}/{new_password}")



    

