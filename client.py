import requests
import sys
from colorama import init, Fore, Style

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

def add_nobel(username: str, password: str, nobel_data: dict):
    response = requests.post(f"{base_url}/add_nobel/{username}/{password}", json = nobel_data)
    return response.json if response.status.code == 200 else (response.status, response.txt)

def delete_nobel(username: str, password: str, nobel_data: dict):
    response = requests.delete(f"{base_url}/delete_nobel/{username}/{password}", json = nobel_data)
    return response.json if response.status.code == 200 else (response.status, response.txt)

def update_nobel(username: str, password: str, nobel_data: dict):
    response = requests.patch(f"{base_url}/delete_nobel/{username}/{password}", json = nobel_data)
    return response.json if response.status.code == 200 else (response.status, response.txt)

def validate_user(username: str, password:str):
    response = requests.get(f"{base_url}/validate_user/{username}/{password}")
    return response.json if response.status.code == 200 else (response.status, response.txt)

def create_user(username: str, password: str):
    response = requests.post(f"{base_url}/create_user/{username}/{password}")
    return response.json if response.status.code == 200 else (response.status, response.txt)

def change_password(username: str, password: str, new_password: str):
    response = requests.post(f"{base_url}/change_password/{username}/{password}/{new_password}")
    return response.json if response.status.code == 200 else (response.status, response.txt)

def update_nobel(username: str, password: str, nobel_data: dict):
    response = requests.update()

init(autoreset=True)

def actions_menu(user:str, password:str):
    """
    Menú de acciones. Solicita una entrada de teclado
    y ejecuta la acción correspondiente.
    """
    print("Acciones:")
    print(Fore.BLUE+"1. Listar Premios Nobel")
    print(Fore.BLUE+"2. Listar Premios Nobel por categoría")
    print(Fore.BLUE+"3. Buscar Premio Nobel por categoría")
    print(Fore.BLUE+"4. Buscar Premio Nobel por año")
    print(Fore.BLUE+"5. Agregar un Premio Nobel")
    print(Fore.BLUE+"6. Modificar un Premio Nobel")
    print(Fore.BLUE+"7. Eliminar un Premio Nobel")
    print(Fore.RED+"8. Salir")

    while True:
        try:
            teclado: str = int(input("Ingrese opción:"))
        except ValueError:
            print(Fore.RED+"Por favor, ingrese un número válido.")
            continue

        #Lista Premios Nobel
        if teclado == 1: 
            get_all_nobels(user, password)            

        #Lista Premios Nobel por categoría
        elif teclado == 2:  
            get_nobel_by_category(user, password)

        #Buscar Premios Nobel por categoría
        elif teclado == 3: 
            category = input("Ingrese categoría: ")
            get_nobel_by_category(user, password, category)

        #Buscar Premios Nobel por años
        elif teclado == 4:
            year = input("Ingrese año: ")
            get_nobel_by_year(user, password, year)
            
        #Agregar Premio Nobel
        elif teclado == 5:
            nobel_data = input("Ingrese datos del premio Nobel: ")
            add_nobel(user, password, nobel_data)
            
        #Actualizar Premio Nobel
        elif teclado == 6:
            nobel_data = input("Ingrese datos del premio Nobel: ")
            update_nobel(user, password, nobel_data)
            
        #Borrar Premio Nobel
        elif teclado == 7:
            nobel_data = input("Ingrese datos del premio Nobel: ")
            delete_nobel(user, password, nobel_data)
        
        #Salir
        elif teclado == 8:
            print(Fore.BLUE+"Gracias por usar el Software")
            sys.exit()
        
        else:
            print(Fore.RED+"Por favor, ingrese una opción válida.")
            continue


def main():
    """
    Función principal del programa. Solicita una entrada de teclado
    y ejecuta la acción correspondiente.
    """
    print(Fore.BLUE+"Bienvenido al Software de Premios Nobel")
    print(Fore.BLUE+"Pulse una tecla para continuar:")
    print(Fore.LIGHTBLUE_EX+"1. Iniciar Sesión")
    print(Fore.LIGHTBLUE_EX+"2. Crear Cuenta")
    print(Fore.LIGHTRED_EX+"0. Salir")

    try:
        teclado: str = int(input())
    except ValueError:
        print(Fore.RED+"Por favor, ingrese un número válido.")
        main()
    if teclado == 0:
        print(Fore.BLUE+"Gracias por usar el Software")
        sys.exit()
    elif teclado == 2:
        username: str = input("Ingrese su nombre de usuario: ")
        password: str = input("Ingrese su contraseña: ")
        create_user(username, password)
        main()
    else:
        username: str = input("Ingrese su nombre de usuario: ")
        password: str = input("Ingrese su contraseña: ")
            
        if validate_user(username, password) == 200:
            print(Fore.GREEN+"Inicio de sesión exitoso")
            print(Fore.BLUE+"Bienvenido", username)
            actions_menu(username, password)
        else:
            print(Fore.RED+"Usuario o contraseña incorrectos")
            main()
            
            


