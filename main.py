from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from fastapi.responses import JSONResponse

# Модель для фильма без ID (для обычного добавления)
class Film(BaseModel):
    director: str
    title: str
    year: int

# Модель для фильма с ID (для восстановления)
class FilmWithID(BaseModel):
    id: int
    director: str
    title: str
    year: int

app = FastAPI()

@app.get("/")
def read_root():
    return "Nikita Petrovich is the best teacher in the world!!! thank for the domen)"

# Получить фильм по ID
@app.get("/film/{film_id}")
def get_film(film_id: int):
    conn = sqlite3.connect("first_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `Films` WHERE `id`=?;", (film_id,))
    film = cursor.fetchone()
    conn.close()
    
    if film:
        return {
            "id": film[0],
            "title": film[1],
            "director": film[2],
            "year": film[3]
        }
    else:
        return JSONResponse(
            status_code=404,
            content={"message": f"Film with id {film_id} not found!"}
        )

# Получить все фильмы
@app.get("/all_films")
def get_all_films():
    conn = sqlite3.connect("first_base.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `Films` ORDER BY `id`;")
    rows = cursor.fetchall()
    conn.close()
    
    films = []
    for row in rows:
        films.append({
            "id": row[0],
            "title": row[1],
            "director": row[2],
            "year": row[3]
        })
    return films

# Добавить новый фильм (ID автоматически)
@app.post("/new_film")
def new_film(data: Film):
    conn = sqlite3.connect("first_base.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO `Films` (`Title`, `Director`, `Year`) VALUES(?, ?, ?)",
        (data.title, data.director, data.year)
    )
    
    # получить айди последнего добавленного фильма
    film_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "message": "Film added successfully!",
        "film": {
            "id": film_id,
            "title": data.title,
            "director": data.director,
            "year": data.year
        }
    }

# востановление фильма после удаления
@app.post("/restore_film/{film_id}")
def restore_film(film_id: int, data: Film):
    conn = sqlite3.connect("first_base.db")
    cursor = conn.cursor()
    
    # проверка занят ли айди
    cursor.execute("SELECT * FROM `Films` WHERE `id`=?", (film_id,))
    existing_film = cursor.fetchone()
    
    if existing_film:
        conn.close()
        return JSONResponse(
            status_code=400,
            content={
                "message": f"ID {film_id} is already taken!",
                "existing_film": {
                    "id": existing_film[0],
                    "title": existing_film[1],
                    "director": existing_film[2],
                    "year": existing_film[3]
                }
            }
        )
    
    # Восстановить фильм с ID
    cursor.execute(
        "INSERT INTO `Films` (`id`, `Title`, `Director`, `Year`) VALUES(?, ?, ?, ?)",
        (film_id, data.title, data.director, data.year)
    )

    conn.commit()
    conn.close()

    return {
        "message": f"Film successfully restored with ID {film_id}!",
        "film": {
            "id": film_id,
            "title": data.title,
            "director": data.director,
            "year": data.year
        }
    }

# Удалить фильм по ID
@app.delete("/film/{film_id}")
def delete_film(film_id: int):
    conn = sqlite3.connect("first_base.db")
    cursor = conn.cursor()
    
    # проверка существует ли ваще фильм
    cursor.execute("SELECT * FROM `Films` WHERE `id`=?", (film_id,))
    film = cursor.fetchone()
    
    if not film:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"message": f"Film with id {film_id} not found!"}
        )
    
    # сохранять инфу о удаленном фильме
    deleted_film = {
        "id": film[0],
        "title": film[1],
        "director": film[2],
        "year": film[3]
    }
    
    # Удаляем фильм
    cursor.execute("DELETE FROM `Films` WHERE `id`=?", (film_id,))
    conn.commit()
    conn.close()
    
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Film with id {film_id} successfully deleted!",
            "deleted_film": deleted_film
        }
    )

# Статистика
@app.get("/id_stats")
def get_id_stats():
    conn = sqlite3.connect("first_base.db")
    cursor = conn.cursor()
    
    # все ID
    cursor.execute("SELECT id FROM `Films` ORDER BY id")
    ids = cursor.fetchall()
    
    # минимальный свободный ID
    cursor.execute("SELECT MIN(id) FROM `Films`")
    min_id = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT MAX(id) FROM `Films`")
    max_id = cursor.fetchone()[0] or 0
    
    used_ids = [id[0] for id in ids]
    
    conn.close()
    
    return {
        "total_films": len(used_ids),
        "used_ids": used_ids,
        "min_id": min_id,
        "max_id": max_id,
        "available_ids": [i for i in range(1, max_id + 2) if i not in used_ids]
    }

# uvicorn main:app --reload