from src.data_manipulation import (remove_nobel,
                                   nobels_handler,
                                   validate_user,
                                   create_user,
                                   change_password,
                                   add_nobel_data)
from typing import IO, Any, List
from pydantic import BaseModel
import uvicorn
import fastapi
import os
import requests 
import json

if not 'nobels.json' in os.listdir('data'):
    with open('data/nobels.json', 'w') as f:
        json.dump(requests.get('https://api.nobelprize.org/v1/prize.json').json(), f)

app: fastapi.FastAPI = fastapi.FastAPI()

class Laureates(BaseModel):
    id: str
    firstname: str
    surname: str
    motivation: str
    share: str

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
def create_user_endpoint(username: str, password: str):
    if not create_user(username, password):
        raise fastapi.HTTPException(status_code=400, detail="La creación falló")
    
    return fastapi.HTTPException(status_code=200)

@app.post('/change_password/{username}/{password}/{new_password}')
def change_password_endpoint(username: str, password: str, new_password: str):
    if not change_password(username, password, new_password):
        return fastapi.HTTPException(status_code=401)
    
    return fastapi.HTTPException(status_code=200)

@app.delete('/delete_nobel/{username}/{password}/laureate_id')
def delete_nobel_api(username: str, password: str, laureate_id: str):
    if not validate_user(username, password):
        raise fastapi.HTTPException(status_code=401, detail="Unauthorized")
    
    data: IO[Any] | None = nobels_handler()
    new_data: dict[str, dict[str, Any]] = {"prizes" : []}
    
    for nobel in data["prizes"]:
        try:
            if laureate_id not in [laureates["id"] for laureates in nobel["laureates"]]:
                new_data["prizes"].append(nobel)
            else:
                print("Found: ", nobel)
        except:
            pass
        
    remove_nobel(new_data)
    
    return fastapi.HTTPException(status_code=200)

@app.get('/validate_user/{username}/{password}')
def validate_user_api(username: str, password:str):
    if not validate_user(username, password):
        return {"status":"notAllowed"}
        
    return {"status":"allowed"}

if __name__ == "__main__":
    uvicorn.run('server:app',
                host="localhost",
                port=8000,
                reload=True)
