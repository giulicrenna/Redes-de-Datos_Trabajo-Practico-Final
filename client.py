import requests
import sys
import json
from colorama import init, Fore, Style
import json

HOST: str = "http://localhost"
PORT: str = "8000"

base_url: str = HOST + ':' + PORT

def get_all_nobels(username: str, password: str): #OK
    response = requests.get(f"{base_url}/all_nobels/{username}/{password}")
    if response.status_code == 200:
        data: dict = json.loads(response.text)
        print(json.dumps(data, indent=4))
    return response.status_code, response.text

def get_nobel_by_year(username: str, password: str, year: str): #OK
    response = requests.get(f"{base_url}/nobel_by_year/{username}/{password}/{year}")
    if response.status_code == 200:
        data: dict = json.loads(response.text)
        print(json.dumps(data, indent=4))
    return response.status_code, response.text

def get_nobel_by_category(username: str, password: str, category: str): #OK
    response = requests.get(f"{base_url}/nobel_by_category/{username}/{password}/{category}")
    if response.status_code == 200:
        data: dict = json.loads(response.text)
        print(json.dumps(data, indent=4))
    return response.status_code, response.text

def get_all_categories(username: str, password: str): #OK
    response = requests.get(f"{base_url}/get_all_categories/{username}/{password}/")
    if response.status_code == 200:
        data: dict = response.json()["available_categories"]
        for k, i in enumerate(data):
            print(f'{k+1}: {i}')
            
    return response.status_code, response.text

def add_nobel(username: str, password: str, nobel_data: dict):
    response = requests.post(f"{base_url}/add_nobel/{username}/{password}", json = nobel_data)
    return response.text if response.status_code == 200 else (response.status_code, response.text)

def delete_nobel(username: str, password: str, nobel_data: dict):
    response = requests.put(f"{base_url}/delete_nobel/{username}/{password}", json = nobel_data)
    return response.text if response.status_code == 200 else (response.status_code, response.text)

def update_nobel(username: str, password: str, nobel_data: dict):
    response = requests.put(f"{base_url}/delete_nobel/{username}/{password}", json = nobel_data)
    return response.text if response.status_code == 200 else (response.status_code, response.text)

def validate_user(username: str, password:str):
    response = requests.get(f"{base_url}/validate_user/{username}/{password}")
    return json.loads(response.text)

def create_user(username: str, password: str):
    response = requests.post(f"{base_url}/create_user/{username}/{password}")
    return "Usuario creado correctamente." if response.status_code == 200 else (response.status_code, response.text)

def change_password(username: str, password: str, new_password: str):
    response = requests.post(f"{base_url}/change_password/{username}/{password}/{new_password}")
    return "Modificación de contraseña realizada correctamente." if response.status_code == 200 else (response.status_code, response.text)

def _get_nobel_data() -> list[dict]:
    print("Ingrese datos del premio Nobel")
    year = input("Ingrese año: ")
    category = input("Ingrese categoría: ")
    id: str = input("Ingrese id: ")
    nombre: str = input("Ingrese nombre: ")
    apellido: str = input("Ingrese apellido: ")
    motivacion: str = input("Ingrese motivacion: ")
    compartido: str = input("Ingrese si es compartido. 0 para no compartidos: ")
    laureates: list[dict] = [
        {
          "id": id,
          "firstname": nombre,
          "surname": apellido,
          "motivation": motivacion,
          "share": compartido
        }
    ]
    nobel_data = {
        "year": year,
        "category": category,
        "laureates": laureates            }
    return nobel_data

def _menu_acciones() -> None:
    print("Acciones:")
    print(Fore.BLUE+"1. Listar Premios Nobel")
    print(Fore.BLUE+"2. Listar categorías")
    print(Fore.BLUE+"3. Buscar Premio Nobel por categoría")
    print(Fore.BLUE+"4. Buscar Premio Nobel por año")
    print(Fore.BLUE+"5. Agregar un Premio Nobel")
    print(Fore.BLUE+"6. Modificar un Premio Nobel")
    print(Fore.BLUE+"7. Eliminar un Premio Nobel")
    print(Fore.BLUE+"9. Cambiar Contraseña")
    print(Fore.RED+"0. Salir")



init(autoreset=True)

def actions_menu(user:str, password:str):
    """
    Menú de acciones. Solicita una entrada de teclado
    y ejecuta la acción correspondiente.
    """
    _menu_acciones()

    while True:
        try:
            teclado: str = int(input("Ingrese opción: "))
        except ValueError:
            print(Fore.RED+"Por favor, ingrese un número válido.")
            continue

        #Lista Premios Nobel
        if teclado == 1: 
            get_all_nobels(user, password)            #OK
            _menu_acciones()

        #Lista Premios Nobel por categoría
        elif teclado == 2:                          #OK
            get_all_categories(user, password)
            _menu_acciones()

        #Buscar Premios Nobel por categoría
        elif teclado == 3: 
            category = input("Ingrese categoría: ")
            get_nobel_by_category(user, password, category)     #OK
            continue

        #Buscar Premios Nobel por años
        elif teclado == 4:                                  #OK
            year = input("Ingrese año: ")
            get_nobel_by_year(user, password, year)
            continue
            
        #Agregar Premio Nobel
        elif teclado == 5:                          #OK
            nobel_data = _get_nobel_data()
            add_nobel(user, password, nobel_data)
            continue
            
        #Actualizar Premio Nobel
        elif teclado == 6:                          #PROBAR
            nobel_data = _get_nobel_data()
            update_nobel(user, password, nobel_data)
            continue
            
        #Borrar Premio Nobel                            #PROBAR
        elif teclado == 7:
            nobel_data = _get_nobel_data()
            delete_nobel(user, password, nobel_data)
            continue
        
        #Salir
        elif teclado == 0:
            print(Fore.BLUE+"Gracias por usar el Software")
            sys.exit()

        elif teclado == 9:
            new_password:str = input("Ingrese nueva contraseña: ")
            change_password(user, new_password)
            actions_menu(user, password,new_password)
            continue
        
        else:
            print(Fore.RED+"####################")
            print(Fore.RED+"Por favor, ingrese una opción válida.")
            print(Fore.RED+"####################")
            _menu_acciones()
            continue


def main():
    """
    Función principal del programa. Solicita una entrada de teclado
    y ejecuta la acción correspondiente.
    """
    print(Fore.BLUE+"Bienvenido al Software de Premios Nobel")
    print(Fore.BLUE+"Pulse una tecla para continuar: ")
    print(Fore.LIGHTBLUE_EX+"1. Iniciar Sesión")
    print(Fore.LIGHTBLUE_EX+"2. Crear Cuenta")
    print(Fore.LIGHTRED_EX+"0. Salir")

    try:
        teclado: str = int(input('> '))
    except ValueError:
        print(Fore.RED+"Por favor, ingrese un número válido.")
        main()
        
    if teclado == 0:
        print(Fore.BLUE+"Gracias por usar el Software")
        sys.exit()
    if teclado == 1:
        username: str = input("Ingrese su nombre de usuario: ")
        password: str = input("Ingrese su contraseña: ")
        
        if validate_user(username, password)['status'] == 'allowed':
            print(Fore.GREEN+"Inicio de sesión exitoso")
            print(Fore.BLUE+"Bienvenido", username)
            actions_menu(username, password)
        else:
            print(Fore.RED+"Usuario o contraseña incorrectos")
            main()  
    elif teclado == 2:
        username: str = input("Ingrese su nombre de usuario: ")
        password: str = input("Ingrese su contraseña: ")
        create_user(username, password)
        main()
        
main()
