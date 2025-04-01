from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# 2. Исходные данные
items = [
    {'id': 1, 'name': 'Ноутбук', 'price': 1000, 'description': 'Ноут'},
    {'id': 2, 'name': 'Телефон', 'price': 500, 'description': 'Теха'},
    {'id': 3, 'name': 'Планшет', 'price': 300, 'description': 'Доска'},
    {'id': 4, 'name': 'Монитор', 'price': 200, 'description': 'Мини телефизор'},
    {'id': 5, 'name': 'Клавиатура', 'price': 50, 'description': 'Стиралка'},
]

# Эндпоинт 1
@app.get("/items/", response_model=List[dict])
def get_items(
    name: Optional[str] = Query(None, min_length=2),
    min_price: Optional[float] = Query(None, gt=0),
    max_price: Optional[float] = Query(None, gt=0),
    limit: int = Query(10, le=100),
):
    if max_price and min_price and max_price < min_price:
        raise HTTPException(400, "Максимальная цена должна быть больше минимальной")
    
    filtered_items = []
    for item in items:
        if name and name.lower() not in item['name'].lower():
            continue
        if min_price and item['price'] < min_price:
            continue
        if max_price and item['price'] > max_price:
            continue
        filtered_items.append(item)
    
    return filtered_items[:limit]

# Эндпоинт 2
@app.get("/items/{item_id}", response_model=dict)
def get_item(item_id: int = Path(..., gt=0)):
    for item in items:
        if item['id'] == item_id:
            return item
    raise HTTPException(404, "Товар не найден")

# Эндпоинт 3
@app.post("/items/", response_model=dict, status_code=201)
def create_item(item: Item):  # Используем модель Item вместо Items
    new_id = items[-1]['id'] + 1 if items else 1
    new_item = {
        'id': new_id,
        'name': item.name,
        'price': item.price,
        'description': item.description
    }
    items.append(new_item)
    return new_item