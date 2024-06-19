from src.data_manipulation import (users_handler,
                                   nobels_handler,
                                   validate_user,
                                   create_user,
                                   change_password,
                                   add_nobel_data)
from typing import IO, Any, List
from pydantic import BaseModel
import uvicorn
import fastapi

"""
endpoints:
/delete_nobel/{username}/{password}
/validate_user/{username}/{password}
/delete_nobel/{username}/{password}

"""

app: fastapi.FastAPI = fastapi.FastAPI()

class Laureates(BaseModel):
    id: int
    firstname: str
    surname: str
    motivation: str
    share: int

class NewNobel(BaseModel):
    year: str
    category: str
    laureates: list[Laureates]

@app.get("/all_nobels/{username}/{password}")
def get_all_nobels(username: str, password: str):
    if not validate_user(username, password):
        return fastapi.HTTPException(status_code=401)
    
    nobels_file: IO[Any] | None = nobels_handler()
    
    return nobels_file

@app.get("/nobel_by_year/{username}/{password}/{year}")
def get_nobel_by_year(username: str, password: str, year: str):
    if not validate_user(username, password):
        raise fastapi.HTTPException(status_code=401, detail="Unauthorized")
    
    nobels_file: IO[Any] | None = nobels_handler()
    
    prizes_by_year: List[dict[str, Any]] = [prize for prize in nobels_file["prizes"] if prize["year"] == year]
    return prizes_by_year

@app.get("/nobel_by_category/{username}/{password}/{category}")
def get_nobel_by_category(username: str, password: str, category: str):
    if not validate_user(username, password):
        raise fastapi.HTTPException(status_code=401, detail="Unauthorized")
    
    nobels_file: IO[Any] | None = nobels_handler()
    
    prizes_by_category: List[dict[str, Any]] = [prize for prize in nobels_file["prizes"] if prize["category"] == category]
    return prizes_by_category

@app.get("/get_all_categories/{username}/{password}")
def get_all_categories(username: str, password: str):
    if not validate_user(username, password):
        raise fastapi.HTTPException(status_code=401, detail="Unauthorized")
    
    nobels_file: IO[Any] | None = nobels_handler()
    categories: list[str] = []
    
    for prize in nobels_file["prizes"]:
        if prize["category"] not in categories:
            categories.append(prize["category"])
    
    return {"available_categories" : categories}


@app.post("/add_nobel/{username}/{password}")
def add_nobel(username: str, password: str, nobel_data: NewNobel):
    if not validate_user(username, password):
        raise fastapi.HTTPException(status_code=401, detail="Unauthorized")
    
    add_nobel_data(nobel_data.model_dump())
    
    return {"detail": "Nobel prize added successfully"}

@app.post("/create_user/{username}/{password}")
def create_user_api(username: str, password: str):
    if not create_user(username, password):
        raise fastapi.HTTPException(status_code=400, detail="La creación falló")
    


    return fastapi.HTTPException(status_code=200)

@app.post('/change_password/{username}/{password}/{new_password}')
def change_password_api(username: str, password: str, new_password: str):
    if not change_password(username, password, new_password):
        return fastapi.HTTPException(status_code=401)
    change_password
    return fastapi.HTTPException(status_code=200)

@app.put('/delete_nobel/{username}/{password}')
def delete_nobel_api(username: str, password: str, nobel_data: Laureates):
    if nobel_data.id not in nobels_handler():
        return fastapi.HTTPException(status_code=404)
    
    nobels_handler().remove(nobel_data.id)
    return fastapi.HTTPException(status_code=200)


@app.put('/update_nobel/{username}/{password}')
def update_nobel_api(username: str, password: str, nobel_data: NewNobel):
    check: bool = (nobels_handler.laureates[id] == nobel_data.laureates[id] and nobel_data.laureates[id] != None and 
            nobel_data.year == nobels_handler.year and nobel_data.category == nobels_handler.category)
    
    if not check:
        return fastapi.HTTPException(status_code=404)

    nobels_handler.laureates['firstname'] = nobel_data.firstname
    nobels_handler.laureates['surname'] = nobel_data.surname
    nobels_handler.laureates['motivation'] = nobel_data.motivation
    nobels_handler.laureates['share'] = nobel_data.share
    
    return fastapi.HTTPException(status_code=200)

@app.get('/validate_user/{username}/{password}')
def validate_user_api(username: str, password:str):
    if not validate_user(username, password):
        print('IF API')
        {"status":"nowAllow"}
    else:
        return {"status":"allow"}




if __name__ == "__main__":
    uvicorn.run('server:app',
                host="localhost",
                port=8000,
                reload=True)
