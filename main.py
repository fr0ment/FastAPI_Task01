from fastapi import FastAPI, Query, HTTPException
from math import sqrt
import random

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "ilya"}

@app.get("/about")
def show_about_me():
    return {"name": "ilya",
            "age": 20,
            "group": "T-323901",
            "country": "Russia",
            "city": "Tagil",
            }   
@app.get("/rnd")
def show_random():
    return {"random": random.randint(1, 10)}

@app.get("/t_square")
def calculate_triangle_area(a: float = Query(gt=0), b: float = Query(gt=0), c: float = Query(gt=0)):
    if a + b <= c or a + c <= b or b + c <= a:
        raise HTTPException(status_code=400, detail="Данные стороны не образуют правильного треугольника.")
    perimeter = a + b + c
    s = perimeter / 2
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    return {"периметр": perimeter, "площадь": area}