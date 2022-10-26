#Python
from doctest import Example
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Nahir" # declarar ejemplo automatico por separado
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


class Person(PersonBase):    
    password: str = Field(..., min_length=8)

class PersonOut(PersonBase):
    pass


# ==============================================
    # Request Body automáticos
    # class Config: 
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Luciano",
    #             "last_name": "Labudia",
    #             "age": 31,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }


#===============================

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World"}

# Request and Response Body
@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Federico" #ejemplo de Path individual
    ),
    age: Optional[str] = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
    )
):
    return {name: age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123 #ejemplo de Path individual
        )
):
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123 #ejemplo de Path individual
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict() #convertir a diccionario
    results.update(location.dict()) #unir el diccionario, swagger no soporta otra forma q no sea esta
    return results

