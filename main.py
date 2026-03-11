from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

class Film(BaseModel):
    director: str
    title: str
    year: int

app = FastAPI()

films = []



@app.get("/")
def read_root():
    return "Nikita Petrovich Best teacher!!! thank for domen)"

# Path параметр 

@app.get("/films/{film_id}")
def get_films(film_id: int):
    return f"The film id is: {film_id}"


# Query параметр
# http://localhost:8000/books2?limit=10&author_name=Pushkin

@app.get("/films2")
def get_films2(limit: int, director_name: str):
    return f"""Films limit is: {limit}, 
        author name is: {director_name}"""

@app.get("/all_films")
def get_all_films():
    conn = sqlite3.connect("first_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `Films`;")
    rows = cursor.fetchall()
    return rows

# POST метод для создания книги

@app.post("/new_film")
def new_film(data: Film):
    conn = sqlite3.connect("first_base.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO `Films` (`Title`, `Director`, `Year`)" \
        "VALUES(?, ?, ?)",
        (data.title, data.director, data.year)
    )

    conn.commit()

    return "Film added!"

# 192.168.0.141

# uvicorn main:app --reload --host 0.0.0.0

# MacOS & Linux: ifconfig
# Windows: ipconfig